#!/usr/bin/env python3
"""Discover combat-associated visible episodes and materialize distinct saved starts."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil

from curate_encounters import coverage, require_source
from native.death_identity import death_id
from synthetic_suite import STATE, kv, read, sha, write


def open_log(run, name):
    packed = run / (name + '.gz')
    return gzip.open(packed, 'rt') if packed.exists() else (run / name).open()


def discover(harvest, output):
    if output.exists():
        raise ValueError('use a fresh discovery path')
    results = []
    for attempt in read(harvest / 'harvest.json')['attempts']:
        run = harvest / attempt['id']
        row = dict(id=attempt['id'], status='failed', selected=[])
        try:
            if attempt['status'] not in ('death', 'survived_cap'):
                raise ValueError('invalid natural run')
            races = {r['index']: r['name'] for r in read(run / 'knowledge.json')['races']}
            episodes, active = [], {}
            with open_log(run, 'observations.jsonl') as stream:
                for number, raw in enumerate(stream, 1):
                    observation = json.loads(raw)
                    status = observation['status']
                    present = {(status['depth'], m['index'], m['race']) for m in observation['monsters']}
                    for key in list(active):
                        if key not in present:
                            episodes.append(active.pop(key))
                    if not 1 <= status['level'] <= 5 or status['hp'] < 0:
                        continue
                    for monster in observation['monsters']:
                        if status['depth'] == 0:
                            continue  # Town terminal incidents are curated separately.
                        key = (status['depth'], monster['index'], monster['race'])
                        if key not in active:
                            active[key] = dict(first=observation['turn'], last=observation['turn'], line=number,
                                depth=status['depth'], level=status['level'], race=monster['race'],
                                index=monster['index'], kind=races[monster['race']])
                        active[key]['last'] = observation['turn']
            episodes += list(active.values())
            messages = []
            with open_log(run, 'messages.log') as stream:
                for raw in stream:
                    parts = raw.rstrip('\n').split(' ', 3)
                    if len(parts) == 4:
                        messages.append(dict(turn=int(parts[1]), text=parts[3]))
            checkpoints = [json.loads(line) for line in (run / 'checkpoints/index.jsonl').read_text().splitlines()]
            selected, used = [], set()
            for episode in episodes:
                kind = episode['kind'].lower()
                contacts = [m for m in messages if episode['first'] <= m['turn'] <= episode['last'] + 10
                    and (m['text'].lower().startswith('the ' + kind + ' ')
                         and (' you' in m['text'] or 'targeted' in m['text'])
                         or m['text'].lower().startswith(('you hit the ' + kind + '.', 'you miss the ' + kind + '.')))]
                if not contacts:
                    continue
                trigger = episode['first']
                eligible = [c for c in checkpoints if c['game_turn'] <= trigger and c['clevel'] <= 5]
                if not eligible or trigger >= attempt['summary']['game_turns']:
                    continue
                checkpoint = eligible[-1]
                if checkpoint['file'] in used:
                    continue
                used.add(checkpoint['file'])
                selected.append(dict(**episode, trigger=trigger, checkpoint=checkpoint, contacts=contacts))
            row.update(status='discovered', episodes=len(episodes), selected=selected)
        except (ValueError, OSError, KeyError) as error:
            row['reason'] = str(error)
        results.append(row)
        write(output, dict(schema='borg-cemetery/encounter-discovery@1', attempts=results))
        print(attempt['id'], row['status'], len(row['selected']), flush=True)
    return results


def reduced(observation, number, raw):
    return dict(schema='borg-cemetery/selected-observation@1', original_line=number,
                original_line_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                retained_fields={k: observation[k] for k in ('turn', 'status', 'equipment', 'inventory', 'spells', 'monsters', 'messages')},
                omitted_fields='panel, quiver, objects, stores, store_header, message_line; full original stream hash in harvest receipt')


def materialize(harvest, discovery, source, bank, root, existing):
    if bank.exists():
        raise ValueError('use a fresh materialization directory')
    bank.mkdir(parents=True)
    document = read(harvest / 'harvest.json')
    require_source(source, document)
    expected = read(existing)['cases']
    used = {read(root / c['scenario'])['save_sha256'] for c in expected}
    exporter_path = Path(os.environ['BORG_CEMETERY_DIR']) / 'scripts/native/export-death.py'
    module = importlib.util.spec_from_file_location('pinned_exporter', exporter_path)
    exporter = importlib.util.module_from_spec(module)
    module.loader.exec_module(exporter)
    packages = [read(p) for p in (harvest / 'deaths').glob('*/record.json')]
    results = []
    for discovered in read(discovery)['attempts']:
        attempt = next(a for a in document['attempts'] if a['id'] == discovered['id'])
        run = harvest / attempt['id']
        episodes = discovered['selected']
        desired_lines = {e['line'] for e in episodes}
        desired_turns = {e['checkpoint']['game_turn'] for e in episodes}
        lines, starts = {}, {}
        with open_log(run, 'observations.jsonl') as stream:
            for number, raw in enumerate(stream, 1):
                observation = json.loads(raw)
                if number in desired_lines:
                    lines[number] = reduced(observation, number, raw)
                turn = observation['turn']
                if turn in desired_turns and turn not in starts:
                    starts[turn] = reduced(observation, number, raw)
        with open_log(run, 'state.log') as stream:
            states = list(stream)
        config = kv(run / 'config.txt')
        if sha(source / 'harness/profiles/reborn-default.txt') != config['profile_sha256']:
            raise ValueError('preparation profile differs from original run')
        family = exporter.run_family(attempt['summary'], config, 'rust', document['build']['source_sha256'], flags=config['flags'])
        parent = next((p for p in packages if p['encounter_family'] == family), None)
        parent_id = death_id(family, next(a['result_sha256'] for a in parent['attempts'] if a['role'] == 'original')) if parent else None
        for episode in episodes:
            name = attempt['id'] + f"-t{episode['trigger']:07d}-m{episode['index']}"
            row = dict(id=name, source_life=attempt['id'], status='failed')
            try:
                checkpoint = episode['checkpoint']
                start = checkpoint['game_turn']
                saved = run / 'checkpoints' / (checkpoint['file'] + '.gz')
                with gzip.open(saved, 'rb') as stream:
                    digest = hashlib.sha256(stream.read()).hexdigest()
                if digest in used:
                    row.update(status='duplicate_saved_start', save_sha256=digest)
                    results.append(row)
                    continue
                witness = starts[start]
                initial = witness['retained_fields']
                native = STATE.match(states[checkpoint['keys'] - 1])
                resources = list(map(int, native.groups()[3:]))
                if resources != [initial['status'][k] for k in ('hp', 'max_hp', 'sp', 'max_sp')]:
                    raise ValueError('checkpoint/observation resource witness differs')
                dest = bank / name
                dest.mkdir()
                shutil.copyfile(saved, dest / 'start.save.gz')
                shutil.copyfile(source / 'harness/profiles/reborn-default.txt', dest / 'profile.txt')
                write(dest / 'initial-witness.json', witness)
                write(dest / 'onset-witness.json', lines[episode['line']])
                write(dest / 'contact-witness.json', episode['contacts'])
                value = dict(schema='borg-cemetery/save-scenario@1', id=name, status='ready_for_restart_trials',
                    save='start.save.gz', save_sha256=digest, compressed_sha256=sha(dest / 'start.save.gz'),
                    birth_seed=attempt['seed'], race_idx=attempt['race'], class_idx=attempt['cls'], start_turn=start,
                    original_endpoint_turn=attempt['summary']['game_turns'], event_kind='observed_combat_encounter',
                    startup_contract='fresh_borg_saved_engine_rng', borg_memory_restored=False,
                    original_continuation_verified=False, independent_life=False,
                    baseline_profile='profile.txt', baseline_profile_sha256=sha(dest / 'profile.txt'),
                    origin=dict(program='borg-reborn-rs', seed=attempt['seed'], source_commit=document['build']['git_rev'],
                        source_sha256=document['build']['source_sha256'], binary_sha256=document['build']['binary_sha256'],
                        parent_death_id=parent_id, encounter_family=family), checkpoint=checkpoint,
                    selection=dict(kind='first_visible_kind_in_combat_associated_episode', monster_kind=episode['kind'],
                        monster_index=episode['index'], terminal_individual_identity='unavailable; kind association only',
                        trigger_turn=episode['trigger'], first_visible_turn=episode['first'],
                        lead_engine_turns=episode['trigger'] - start, no_omniscient_trigger=True,
                        first_contact_turn=episode['contacts'][0]['turn'],
                        observation_sha256=next(r['sha256'] for r in attempt['retention'] if r['file'] == 'observations.jsonl')),
                    initial_observed=dict(zip(('hp', 'max_hp', 'sp', 'max_sp'), resources)), coverage=coverage(initial))
                write(dest / 'scenario.json', value)
                used.add(digest)
                row.update(status='ready', scenario=(dest / 'scenario.json').relative_to(root).as_posix(),
                           sha256=sha(dest / 'scenario.json'), save_sha256=digest)
            except (ValueError, OSError, KeyError, IndexError, AttributeError) as error:
                row['reason'] = str(error)
            results.append(row)
        write(bank / 'materialization.json', dict(schema='borg-cemetery/encounter-materialization@1', results=results))
        print(attempt['id'], 'materialized', sum(r['status'] == 'ready' for r in results), flush=True)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    d = sub.add_parser('discover')
    d.add_argument('--harvest', type=Path, required=True)
    d.add_argument('--out', type=Path, required=True)
    m = sub.add_parser('materialize')
    for name in ('harvest', 'discovery', 'source', 'bank', 'root', 'existing'):
        m.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    if args.action == 'discover':
        discover(args.harvest.resolve(), args.out.resolve())
    else:
        materialize(args.harvest.resolve(), args.discovery.resolve(), args.source.resolve(),
                    args.bank.resolve(), args.root.resolve(), args.existing.resolve())
