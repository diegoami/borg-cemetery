#!/usr/bin/env python3
"""Index pinned cases into class shards of at most eight and a small smoke suite."""
import argparse
from collections import Counter
from pathlib import Path

from death_ids import inventory
from synthetic_suite import local_file, read, sha, write
from encounter_bank import prepare_bank

ROOT = Path(__file__).resolve().parents[1]


def index(cases_path, template_path, output, root=ROOT):
    if output.exists():
        raise ValueError('use a fresh index directory')
    output.relative_to(root)
    template = read(template_path)
    cases = read(cases_path)['cases']
    if not 4 <= len(cases) <= 512:
        raise ValueError('bank requires 4..512 cases')
    families = {r['id']: read(root / r['path'] / 'record.json').get('encounter_family')
                for r in inventory(root)['records']}
    values, observed = {}, []
    for case in cases:
        scenario = read(local_file(root, case['scenario'], case['sha256']))
        if scenario['class_idx'] not in (1, 2, 3, 4) or scenario['id'] != case['id']:
            raise ValueError('invalid caster scenario reference')
        values[case['id']] = scenario
        origin = scenario['origin']
        family = origin.get('encounter_family') or families[origin['parent_death_id']]
        observed.append(dict(id=case['id'], class_idx=scenario['class_idx'], race_idx=scenario['race_idx'],
                             source_life=family, **scenario.get('coverage', {})))
    if len(values) != len(cases):
        raise ValueError('duplicate case ID')
    output.mkdir(parents=True)
    shards, smoke, counts = [], [], {}
    for cls, label in ((1, 'mage'), (2, 'druid'), (3, 'priest'), (4, 'necromancer')):
        entries = [c for c in cases if values[c['id']]['class_idx'] == cls]
        if not entries:
            raise ValueError('bank must include every caster class')
        counts[label] = len(entries)
        for offset in range(0, len(entries), 8):
            path = output / f'{label}-{offset // 8 + 1:02d}.json'
            write(path, dict(template, suite_id=f"{output.name}-{label}-{offset // 8 + 1:02d}", scenarios=entries[offset:offset + 8]))
            shards.append(dict(manifest=path.relative_to(root).as_posix(), sha256=sha(path)))
        options = [c for c in entries if values[c['id']].get('coverage')]
        if len(options) >= 2:
            a = next((c for c in options if values[c['id']]['coverage']['mana_state'] == 'empty'), options[0])
            b = next((c for c in options if c != a and values[c['id']]['coverage']['mana_state'] == 'full'), next(c for c in options if c != a))
            smoke.extend((a, b))
    write(output / 'bank.json', dict(schema='borg-cemetery/encounter-bank@1', id=output.name,
                                     expected_cases=len(cases), shards=shards))
    if len(smoke) == 8:
        write(output / 'smoke-suite.json', dict(template, suite_id=output.name + '-smoke', scenarios=smoke))
    write(output / 'coverage.json', dict(cases=len(cases), class_counts=counts,
        source_lives=len({c['source_life'] for c in observed}),
        equipment_kind_combinations=len({c['equipment_kind_signature'] for c in observed if 'equipment_kind_signature' in c}),
        mana_states=dict(Counter(c.get('mana_state', 'unavailable') for c in observed)),
        observed_coverage=observed, qualified_near_death_coverage='unavailable'))
    prepare_bank(output / 'bank.json', root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('cases', 'template', 'out'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    index(args.cases.resolve(), args.template.resolve(), args.out.resolve())
