#!/usr/bin/env python3
"""Index preserved low-level caster observations; never synthesize engine state."""
import argparse
import hashlib
import subprocess
from pathlib import Path

from synthetic_suite import canonical, local_file, read, write

CASTERS = {'Mage', 'Priest', 'Druid', 'Necromancer'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(root, path):
    return dict(path=path.relative_to(root).as_posix(), sha256=digest(path))


def observation(frame):
    """Project player-visible descriptions only, excluding diagnostic actual kinds."""
    inventory = frame.get('inventory')
    equipment = None
    if isinstance(inventory, dict):
        equipment = {key: ([{k: item[k] for k in ('slot', 'description', 'weight') if k in item}
                           for item in inventory[key]] if key in inventory else None)
                     for key in ('equipment', 'pack', 'quiver')}
    spells = frame.get('spells')
    spells = spells if isinstance(spells, dict) else None
    result = {key: frame.get(key) for key in
              ('turn', 'level', 'depth', 'hp', 'max_hp', 'sp', 'max_sp')}
    result.update(inventory=equipment, spells=spells)
    hp, maximum = result['hp'], result['max_hp']
    result['low_hp_candidate'] = (type(hp) is int and type(maximum) is int
                                  and maximum > 0 and 0 < hp <= maximum / 4)
    result['missing'] = [key for key in ('inventory', 'spells') if result[key] is None]
    return result


def collect(root):
    root = root.resolve()
    cases, saved, excluded = [], [], []
    for path in sorted((root / 'deaths').glob('*/record.json')):
        record = read(path)
        frames = (record.get('recording') or {}).get('selected_original_frames', [])
        observations, variants = [], {}
        for entry in frames:
            # Published per-frame hashes are mandatory: a mismatch is not skipped.
            if 'json_sha256' not in entry:
                excluded.append(dict(record=reference(root, path), frame=entry.get('json'),
                                     reason='no_published_frame_digest'))
                continue
            source = local_file(path.parent, entry['json'], entry['json_sha256'])
            frame = read(source)
            spells = frame.get('spells') or {}
            if not isinstance(spells, dict) or spells.get('class') not in CASTERS:
                continue
            if type(frame.get('level')) is not int or not 1 <= frame['level'] <= 10:
                continue
            item = observation(frame)
            item['source'] = reference(root, source)
            item['class'] = spells['class']
            if item['inventory'] is not None:
                signature = hashlib.sha256(canonical(item['inventory'])).hexdigest()
                item['loadout_id'] = signature
                variants.setdefault(signature, dict(id=signature, inventory=item['inventory'],
                                                    first_observed_turn=item['turn']))
                variants[signature]['first_observed_turn'] = min(
                    variants[signature]['first_observed_turn'], item['turn'])
            observations.append(item)
        if observations:
            cases.append(dict(case=path.parent.name, record=reference(root, path),
                              identity=record.get('identity'), character=record.get('character'),
                              observations=sorted(observations, key=lambda item: (item['turn'], item['source']['path'])),
                              observed_loadouts=sorted(variants.values(), key=lambda item: item['id']),
                              execution_status='requires_caster_build_adapter',
                              original_continuation_verified=False))
    for path in sorted((root / 'scenarios').glob('*/scenario.json')):
        scenario = read(path)
        if scenario.get('class_idx') not in (1, 2, 3, 4):
            continue
        # Save metadata without a level is retained as unknown, never called low level.
        level = scenario.get('level', (scenario.get('checkpoint') or {}).get('clevel'))
        if level is not None and (type(level) is not int or not 1 <= level <= 10):
            continue
        save = None
        if scenario.get('save'):
            packed = local_file(path.parent, scenario['save'], scenario['compressed_sha256'])
            save = reference(root, packed)
        saved.append(dict(scenario=path.parent.name, source=reference(root, path), save=save,
                          level=level, class_idx=scenario['class_idx'], race_idx=scenario.get('race_idx'),
                          event_kind=scenario.get('event_kind'), origin=scenario.get('origin'),
                          startup_contract=scenario.get('startup_contract'),
                          original_continuation_verified=scenario.get('original_continuation_verified', False),
                          execution_status='requires_original_build_qualification' if save else 'missing_checkpoint',
                          independent_life=False))
    return dict(schema='borg-cemetery/caster-candidates@1',
                selection=dict(classes=sorted(CASTERS), level_min=1, level_max=10,
                               low_hp_screen='living HP <= 25% maximum; candidate only',
                               scope='Published selected frames and existing saved scenarios; not full-run coverage'),
                limitations=['Observed loadouts are descriptions, not executable character-build records.',
                             'No equipment effect, spell legality or causal explanation is inferred.',
                             'Save restarts do not restore private Borg memory.',
                             'Multiple frames, loadouts and checkpoints of one life are correlated.'],
                cases=cases, saved_scenarios=saved, excluded_frames=excluded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output already exists; use a new file to preserve prior evidence')
    subprocess.run(['git', '-C', str(args.root), 'diff', '--exit-code', 'HEAD', '--',
                    'deaths', 'scenarios'], check=True, stdout=subprocess.DEVNULL)
    result = collect(args.root)
    result['input_commit'] = subprocess.check_output(
        ['git', '-C', str(args.root), 'rev-parse', 'HEAD'], text=True).strip()
    write(args.out, result)


if __name__ == '__main__':
    main()
