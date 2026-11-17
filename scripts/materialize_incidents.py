#!/usr/bin/env python3
"""Freeze nine completed class harvests into an exactly balanced999 saved bank."""
import argparse
from collections import Counter
import importlib.util
import json
import re
from pathlib import Path
import shutil

from curate_encounters import coverage
from native.death_identity import metadata
from synthetic_suite import read, sha, write

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ['Warrior', 'Mage', 'Druid', 'Priest', 'Necromancer', 'Paladin', 'Rogue', 'Ranger', 'Blackguard']


def materialize(inputs, output, tools, baseline, root=ROOT, per_class=111, suite_id="balanced999-incidents"):
    if output.exists():
        raise ValueError('use a fresh immutable bank directory')
    harvests = {}
    for path in inputs.rglob('harvest.json'):
        document = read(path)
        if document.get('schema') != 'borg-cemetery/balanced-incident-harvest@1':
            continue
        cls = document['class_idx']
        if cls in harvests:
            raise ValueError('duplicate class harvest')
        harvests[cls] = (path.parent, document)
    gaps = {CLASSES[c]: len(harvests[c][1]['selected']) if c in harvests else 0 for c in range(9)}
    if per_class not in (2, 111) or any(n != per_class for n in gaps.values()):
        raise ValueError('balanced bank not ready: ' + json.dumps(gaps))
    module = importlib.util.spec_from_file_location('pinned_exporter', tools / 'scripts/native/export-death.py')
    exporter = importlib.util.module_from_spec(module)
    module.loader.exec_module(exporter)
    output.mkdir(parents=True)
    by_class, save_ids, descriptors, gear = {}, set(), [], {}
    spec_hashes = {h[1]["spec_sha256"] for h in harvests.values()}
    if len(spec_hashes) != 1:raise ValueError("class harvest specifications differ")
    exclusions, prior_seeds = set(), set()
    for directory, document in harvests.values():
        spec = read(directory / 'spec.json')
        if 'exclusion' in spec:
            path = root / 'synthetic' / spec['suite_id'] / spec['exclusion']['path']
            if sha(path) != spec['exclusion']['sha256']:raise ValueError('exclusion identity differs')
            prior = read(path);exclusions.update(prior['save_sha256']);prior_seeds.update(prior['source_seeds'])
    for cls in range(9):
        directory, document = harvests[cls]
        build = read(directory / 'build.json')
        attempts = {r['id']: r for r in document['attempts']}
        selected = []
        for case in document['selected']:
            source = directory / 'cases' / case['directory']
            attempt = attempts[case['source_attempt']]
            run = directory / 'attempts' / attempt['id']
            initial = read(source / 'initial-observation.json')
            incident = read(source / 'incident.json')
            summary = attempt['summary']
            config = dict(line.split('=', 1) for line in (run / 'config.txt').read_text().splitlines() if '=' in line)
            family = exporter.run_family(summary, config, 'rust', build['source_sha256'], flags=config['flags'])
            parent = next((p for p in (run / 'native-deaths').glob('*/record.json')), None)
            parent_id = metadata(read(parent), parent.read_bytes(), parent.parent.name)['id'] if parent else None
            if summary.get('dead') and parent_id is None:
                raise ValueError('missing parent natural death record')
            if build['git_rev'] != read(directory / 'spec.json')['source_commit']:raise ValueError('harvest source differs')
            digest = case['save_sha256']
            if digest in exclusions or attempt['seed'] in prior_seeds:raise ValueError('earlier suite overlap')
            if digest in save_ids:
                raise ValueError('duplicate saved state')
            save_ids.add(digest)
            dest = output / 'cases' / case['id']
            dest.mkdir(parents=True)
            for name in ('start.save.gz', 'profile.txt', 'initial-observation.json', 'incident.json'):
                shutil.copyfile(source / name, dest / name)
            checkpoint = incident['checkpoint']
            scenario = dict(schema='borg-cemetery/save-scenario@1', id=case['id'], status='ready_for_restart_trials',
                save='start.save.gz', save_sha256=digest, compressed_sha256=sha(dest / 'start.save.gz'),
                birth_seed=attempt['seed'], race_idx=attempt['race'], class_idx=cls, start_turn=initial['turn'],
                original_endpoint_turn=summary['game_turns'], event_kind=case['incident_type'],
                startup_contract='fresh_borg_saved_engine_rng', borg_memory_restored=False,
                original_continuation_verified=False, independent_life=False,
                baseline_profile='profile.txt', baseline_profile_sha256=sha(dest / 'profile.txt'),
                origin=dict(program='borg-reborn-rs', seed=attempt['seed'], source_commit=build['git_rev'],
                    source_sha256=build['source_sha256'], binary_sha256=build['binary_sha256'],
                    controller=read(directory / 'spec.json').get('core','reborn'), configuration_sha256=read(directory / 'spec.json').get('configuration'),
                    parent_death_id=parent_id, encounter_family=family), checkpoint=checkpoint,
                selection=dict(incident['selection'], lead_engine_turns=incident['selection']['trigger_turn'] - initial['turn']),
                initial_observed={k: initial['status'][k] for k in ('hp', 'max_hp', 'sp', 'max_sp')},
                coverage=coverage(initial), historical_incident=dict(type=case['incident_type'], turn=case['incident_turn'], witness=incident['witness']),
                qualified_near_death=dict(coverage='unavailable', count=None))
            if not scenario['start_turn'] <= scenario['selection']['trigger_turn'] <= case['incident_turn'] <= scenario['start_turn'] + 2000:
                raise ValueError('incident onset/horizon differs')
            write(dest / 'scenario.json', scenario)
            entry = dict(id=case['id'], scenario=(dest / 'scenario.json').relative_to(root).as_posix(), sha256=sha(dest / 'scenario.json'))
            if 'initial_state' in case:
                hashes=re.search(r' p([0-9a-f]{16}) e([0-9a-f]{16}) r([0-9a-f]{16})(?:\s|$)',case['initial_state'])
                if not hashes:raise ValueError('missing initial gear hashes')
                gear[case['id']]=list(hashes.groups())
            selected.append(entry)
            descriptors.append(dict(id=case['id'], class_idx=cls, class_name=CLASSES[cls], type=case['incident_type'],
                                    parent_family=family, source_seed=attempt['seed'], race_idx=attempt['race'], save_sha256=digest, **scenario['coverage']))
        by_class[cls] = selected
    # Round-robin ordering keeps every execution batch mixed, not class-only.
    entries = [by_class[cls][index] for index in range(per_class) for cls in range(9)]
    shards = []
    for offset in range(0, len(entries), 8):
        path = output / 'shards' / f'{offset//8:03d}.json'
        write(path, dict(schema='borg-cemetery/saved-encounter-suite@1', suite_id=f'{suite_id}-{offset//8:03d}',
                         core='reborn', baseline_source_commit=baseline, engine_commit='42cd156ac9f95ddf4311e88dd7ad462292d6d1d6',
                         horizon_engine_turns=2000, wall_seconds=5, scenarios=entries[offset:offset+8]))
        shards.append(dict(manifest=path.relative_to(root).as_posix(), sha256=sha(path)))
    write(output / 'bank.json', dict(schema='borg-cemetery/encounter-bank@1', id=suite_id, expected_cases=per_class*9, shards=shards))
    write(output / 'all-cases.json', dict(cases=entries))
    write(output / 'gear.json',dict(cases={e['id']:gear[e['id']] for e in entries} if gear else {}))
    write(output / 'coverage.json', dict(expected_cases=per_class*9, class_counts={c:per_class for c in CLASSES},
        suite_id=suite_id, harvest_spec_sha256=next(iter(spec_hashes)), source_life_overlap_suite1=0 if prior_seeds else None,
        incident_counts=dict(Counter(d['type'] for d in descriptors)),
        incident_counts_by_class={c:dict(Counter(d['type'] for d in descriptors if d['class_name']==c)) for c in CLASSES},
        source_lives=len({d['parent_family'] for d in descriptors}), unique_saved_starts=len(save_ids),
        equipment_combinations=len({d['equipment_kind_signature'] for d in descriptors}), cases=descriptors,
        qualified_near_death=dict(coverage='unavailable', count=None)))
    return entries


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('inputs','out','tools'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--baseline',default='6d1bca10bc67d02150a1a717f111891976e98069')
    parser.add_argument('--per-class',type=int,default=111)
    parser.add_argument('--suite-id',default='balanced999-incidents')
    args=parser.parse_args()
    entries=materialize(args.inputs.resolve(),args.out.resolve(),args.tools.resolve(),args.baseline,per_class=args.per_class,suite_id=args.suite_id)
    print(len(entries),'balanced incident scenarios frozen')
