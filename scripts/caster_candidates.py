#!/usr/bin/env python3
"""Index preserved low-level caster observations; never synthesize engine state."""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path

from synthetic_suite import canonical, local_file, read, write

CASTERS = {'Mage', 'Priest', 'Druid', 'Necromancer'}
CLASS_NAMES = {0: 'Warrior', 1: 'Mage', 2: 'Druid', 3: 'Priest', 4: 'Necromancer',
               5: 'Paladin', 6: 'Rogue', 7: 'Ranger', 8: 'Blackguard'}


def record_class(record):
    terminal = record.get('terminal') or {}
    if terminal.get('class_idx') in CLASS_NAMES:
        return CLASS_NAMES[terminal['class_idx']]
    words = re.findall(r'[A-Za-z]+', record.get('character', ''))
    return next((name for name in sorted(CLASS_NAMES.values()) if name in words), None)


def normalized_items(items, equipped=False):
    """Compare observed item types/bonuses, ignoring stack size and light fuel.

    These are description signatures, not engine kind IDs. Only known English
    inventory plural forms are folded; no hidden kind or unrecorded stat is used.
    """
    if items is None:
        return None
    plurals = dict(Books='Book', Tomes='Tome', Potions='Potion', Scrolls='Scroll',
                   Rations='Ration', Flasks='Flask', Torches='Torch', Staves='Staff',
                   Mushrooms='Mushroom', Apples='Apple', Handfuls='Handful')
    result = []
    for item in items:
        description = re.sub(r'^(?:an? |[0-9]+ )', '', item.get('description', ''))
        description = re.sub(r' \([0-9]+ turns\)', '', description)
        description = re.sub(r'\b(' + '|'.join(plurals) + r')\b',
                             lambda match: plurals[match[0]], description)
        value = dict(description=description)
        if equipped:
            value['slot'] = item.get('slot')
        result.append(value)
    # Pack order/duplicate stacks do not create another type set.
    unique = {canonical(value): value for value in result}
    return [unique[key] for key in sorted(unique)]


def normalized_sets(observations, key):
    result = {}
    for item in observations:
        inventory = item['inventory']
        if inventory is None or inventory.get(key) is None:
            continue
        items = normalized_items(inventory[key], equipped=key == 'equipment')
        signature = hashlib.sha256(canonical(items)).hexdigest()
        result[signature] = dict(id=signature, items=items)
    return [result[key] for key in sorted(result)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(root, path):
    return dict(path=path.relative_to(root).as_posix(), sha256=digest(path))


def death_identity(root, record):
    sidecar = record.parent / 'death-id.json'
    if not sidecar.exists():
        return None
    value = read(sidecar)
    local_file(record.parent, record.name, value['record_sha256'])
    return dict(id=value['id'], source=reference(root, sidecar))


def observation(frame):
    """Project player-visible descriptions only, excluding diagnostic actual kinds."""
    inventory = frame.get('inventory')
    equipment = None
    if isinstance(inventory, dict):
        equipment = {key: ([{k: item[k] for k in ('slot', 'description', 'weight') if k in item}
                           for item in inventory[key]] if key in inventory else None)
                     for key in ('equipment', 'pack', 'quiver')}
    spells = frame.get('spells')
    if isinstance(spells, dict):
        projected = {key: spells[key] for key in ('caster', 'class', 'mana', 'max_mana')
                     if key in spells}
        if isinstance(spells.get('learned'), list):
            projected['learned'] = [{key: spell[key] for key in
                                    ('book', 'book_label', 'castable', 'fail', 'label',
                                     'level', 'mana', 'name', 'status') if key in spell}
                                    for spell in spells['learned']]
        spells = projected
    else:
        spells = None
    result = {key: frame.get(key) for key in
              ('turn', 'level', 'depth', 'hp', 'max_hp', 'sp', 'max_sp')}
    result.update(inventory=equipment, spells=spells)
    flag = frame.get('dead')
    result['dead'] = bool(flag) if type(flag) in (bool, int) and flag in (0, 1) else None
    hp, maximum = result['hp'], result['max_hp']
    result['low_hp_candidate'] = (type(hp) is int and type(maximum) is int
                                  and maximum > 0 and 0 <= hp <= maximum / 4
                                  and result['dead'] is False)
    result['missing'] = [key for key in ('inventory', 'spells', 'dead') if result[key] is None]
    return result


def collect(root):
    root = root.resolve()
    cases, saved, excluded, unobserved, skipped = [], [], [], [], []
    for path in sorted((root / 'deaths').glob('*/record.json')):
        record = read(path)
        canonical_identity = death_identity(root, path)
        frames = (record.get('recording') or {}).get('selected_original_frames', [])
        known_class = record_class(record)
        terminal = record.get('terminal') or {}
        terminal_level = terminal.get('level')
        if (not frames and known_class in CASTERS and type(terminal_level) is int
                and 1 <= terminal_level <= 10):
            unobserved.append(dict(case=path.parent.name, record=reference(root, path),
                                   canonical_identity=canonical_identity,
                                   character=record.get('character'), terminal_level=terminal_level,
                                   class_name=known_class, status='no_recorded_frames',
                                   inventory=None, spells=None))
        observations, variants = [], {}
        for entry in frames:
            # Published per-frame hashes are mandatory: a mismatch is not skipped.
            if 'json_sha256' not in entry:
                excluded.append(dict(record=reference(root, path), frame=entry.get('json'),
                                     reason='no_published_frame_digest'))
                continue
            source = local_file(path.parent, entry['json'], entry['json_sha256'])
            frame = read(source)
            spells = frame.get('spells')
            frame_class = spells.get('class') if isinstance(spells, dict) else None
            if known_class and frame_class and frame_class != known_class:
                excluded.append(dict(record=reference(root, path), frame=entry['json'],
                                     reason='class_metadata_conflict'))
                continue
            selected_class = frame_class or known_class
            if selected_class is None:
                excluded.append(dict(record=reference(root, path), frame=entry['json'],
                                     reason='class_unavailable'))
                continue
            if selected_class not in CASTERS:
                continue
            if type(frame.get('level')) is not int or not 1 <= frame['level'] <= 10:
                continue
            item = observation(frame)
            item['source'] = reference(root, source)
            item['class'] = selected_class
            item['class_basis'] = 'frame_spells' if frame_class else 'record_metadata'
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
                              canonical_identity=canonical_identity,
                              identity=record.get('identity'), character=record.get('character'),
                              observations=sorted(observations, key=lambda item: (item['turn'], item['source']['path'])),
                              observed_loadouts=sorted(variants.values(), key=lambda item: item['id']),
                              normalized_equipment_sets=normalized_sets(observations, 'equipment'),
                              normalized_pack_sets=normalized_sets(observations, 'pack'),
                              execution_status='requires_caster_build_adapter',
                              original_continuation_verified=False))
        elif frames and known_class in CASTERS and type(terminal_level) is int and 1 <= terminal_level <= 10:
            status = ('frames_without_published_digest' if
                      all('json_sha256' not in entry for entry in frames) else 'no_eligible_frames')
            unobserved.append(dict(case=path.parent.name, record=reference(root, path),
                                   canonical_identity=canonical_identity,
                                   character=record.get('character'), terminal_level=terminal_level,
                                   class_name=known_class, status=status,
                                   inventory=None, spells=None))
        elif known_class is None or (known_class in CASTERS and type(terminal_level) is not int):
            skipped.append(dict(case=path.parent.name, record=reference(root, path),
                                canonical_identity=canonical_identity, schema=record.get('schema'),
                                class_name=known_class, terminal_level=terminal_level,
                                reason='class_unavailable' if known_class is None else 'level_unavailable'))
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
                cases=cases, saved_scenarios=saved, excluded_frames=excluded,
                unobserved_cases=unobserved, skipped_records=skipped)


def require_clean_inputs(root):
    status = subprocess.check_output(
        ['git', '-C', str(root), 'status', '--porcelain=v1', '--untracked-files=all',
         '--', 'deaths', 'scenarios'], text=True)
    if status:
        raise ValueError('tracked or untracked changes in deaths/ or scenarios/')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output already exists; use a new file to preserve prior evidence')
    require_clean_inputs(args.root)
    result = collect(args.root)
    result['input_commit'] = subprocess.check_output(
        ['git', '-C', str(args.root), 'rev-parse', 'HEAD'], text=True).strip()
    write(args.out, result)


if __name__ == '__main__':
    main()
