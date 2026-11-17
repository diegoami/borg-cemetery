#!/usr/bin/env python3
"""Curate one observable encounter per harvest life, preserving all exclusions."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from synthetic_suite import STATE, hashed, kv, read, sha, write
from native.death_identity import death_id


def require_source(source, document):
    expected = document['build']
    actual = kv(source / 'build/rust/BUILD_ID')
    for key in ('git_rev', 'source_sha256', 'binary_sha256', 'engine_upstream'):
        if actual.get(key) != expected.get(key):
            raise ValueError('preparation source/build differs: ' + key)
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    inputs = subprocess.check_output(['bash', str(source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
    if head != expected['git_rev'] or inputs != expected['source_sha256'] or sha(source / 'build/rust/game/angband') != expected['binary_sha256']:
        raise ValueError('preparation build inputs changed')


def rows(path):
    with gzip.open(path, 'rt') as stream:
        for number, line in enumerate(stream, 1):
            yield number, json.loads(line)


def coverage(observation):
    status = observation['status']
    equipment = [dict(slot=e['slot_type'], kind=e['item']['kind'], description=e['item']['desc'])
                 for e in observation['equipment'] if e['item']]
    pack = [dict(kind=i['kind'], description=i['desc'], count=i['number']) for i in observation['inventory']]
    # Item kind/slot combinations, without torch fuel or stack counts, describe
    # gear diversity; exact observable details remain in initial-observation.json.
    signature = hashed([(e['slot'], e['kind']) for e in equipment])
    return dict(level=status['level'], depth=status['depth'], hp=status['hp'], max_hp=status['max_hp'],
                sp=status['sp'], max_sp=status['max_sp'],
                mana_state='empty' if status['max_sp'] > 0 and status['sp'] == 0 else
                           'partial' if status['sp'] < status['max_sp'] else 'full',
                equipment=equipment, inventory=pack, equipment_kind_signature=signature)


def select(observations, messages, races, summary):
    def named_contact(message):
        text = message['text'].lower()
        return (' you' in text and text.startswith('the ')
                and any(text.startswith('the ' + r['name'].lower() + ' ') for r in races))
    eligible = [o for o in observations if (summary.get('dead') or o['s']['depth'] > 0)
                and 1 <= o['s']['level'] <= 5 and o['s']['hp'] >= 0]
    if not eligible:
        raise ValueError('no living level1..5 observation')
    worst = min(eligible, key=lambda o: (o['s']['hp'] / o['s']['max_hp'], o['turn']))
    basis = 'observable kind episode before terminal death' if summary.get('dead') else 'observable attacker near observed HP minimum'
    if summary.get('dead'):
        cause = summary['death_cause']
        kinds = [r for r in races if cause in (r['name'], 'a ' + r['name'], 'an ' + r['name'], 'the ' + r['name'])]
        if not kinds:
            if cause != 'poison':
                raise ValueError('death cause cannot be linked to a monster kind')
            poison = [m for m in messages if m['text'] == 'You are poisoned!']
            if not poison:
                raise ValueError('poison death has no observable onset')
            poison_turn = poison[-1]['turn']
            incoming = [m for m in messages if poison_turn - 20 <= m['turn'] <= poison_turn
                        and m['text'].startswith('The ') and ' you' in m['text']]
            if not incoming:
                raise ValueError('poison onset has no named incoming contact')
            kinds = [r for r in races if incoming[-1]['text'].lower().startswith('the ' + r['name'].lower() + ' ')]
            if not kinds:
                raise ValueError('poison contact kind unavailable')
            basis = 'named incoming contact immediately before final observed poisoning; terminal cause poison'
        kind = kinds[0]
        cutoff = summary['game_turns']
    else:
        cutoff = worst['turn']
        attacks = [m for m in messages if cutoff - 500 <= m['turn'] <= cutoff and named_contact(m)]
        if not attacks:
            contacts = [m for m in messages if cutoff - 500 <= m['turn'] <= cutoff
                        and m['text'].startswith('Something ') and ' you' in m['text']]
            if contacts:
                return dict(trigger_turn=contacts[0]['turn'], kind='first_observable_unseen_contact',
                    monster_kind='unseen attacker; identity unavailable', terminal_individual_identity='unavailable',
                    observation_line=None, worst=worst, contacts=contacts, no_omniscient_trigger=True)
            # A level-up can lower HP/maxHP without damage. Keep a surviving
            # fight control from this life, without pretending it was a near death.
            candidates = [m for m in messages if named_contact(m)]
            for attack in candidates:
                prior = next((o for o in reversed(observations) if o['turn'] <= attack['turn']), None)
                if prior and prior['s']['depth'] > 0 and 1 <= prior['s']['level'] <= 5:
                    attacks = [attack]
                    cutoff = attack['turn']
                    basis = 'first named incoming dungeon contact; HP-minimum association unavailable'
                    break
            if not attacks:
                raise ValueError('no incoming dungeon encounter')
        attack = attacks[-1]
        kinds = [r for r in races if attack['text'].lower().startswith('the ' + r['name'].lower() + ' ')]
        if not kinds:
            raise ValueError('incoming attack has no known monster kind')
        kind = max(kinds, key=lambda r: len(r['name']))
    visible = [(i, o) for i, o in enumerate(observations) if o['turn'] <= cutoff and
               any(m['race'] == kind['index'] for m in o['monsters'])]
    if not visible:
        contacts = [m for m in messages if cutoff - 1000 <= m['turn'] <= cutoff and m['text'].startswith('Something ') and ' you' in m['text']]
        if not contacts:
            raise ValueError('killer has neither observed visibility nor recent unseen contact')
        trigger = contacts[0]['turn']
        return dict(trigger_turn=trigger, kind='first_observable_unseen_contact', monster_kind=kind['name'],
                    terminal_individual_identity='unavailable', observation_line=None, worst=worst,
                    contacts=contacts, no_omniscient_trigger=True)
    last_i, last = visible[-1]
    candidates = [m for m in last['monsters'] if m['race'] == kind['index']]
    monster = min(candidates, key=lambda m: abs(m['x'] - last['s']['x']) + abs(m['y'] - last['s']['y']))
    first = last_i
    while first > 0:
        previous = observations[first - 1]
        if previous['s']['depth'] != last['s']['depth'] or not any(m['index'] == monster['index'] and m['race'] == kind['index'] for m in previous['monsters']):
            break
        first -= 1
    onset = observations[first]
    # A message can precede the next think/visibility receipt by several ticks.
    contacts = [m for m in messages if onset['turn'] - 100 <= m['turn'] <= cutoff and
                m['text'].lower().startswith('the ' + kind['name'].lower() + ' ') and ' you' in m['text']]
    trigger = min([onset['turn']] + [m['turn'] for m in contacts])
    return dict(trigger_turn=trigger, kind='first_visible_kind_in_selected_episode', monster_kind=kind['name'],
                monster_index=monster['index'], terminal_individual_identity='unavailable; kind association only',
                observation_line=onset['line'], first_visible_turn=onset['turn'], worst=worst,
                contacts=contacts, no_omniscient_trigger=True, selection_basis=basis)


def curate(harvest, source, bank, root, only=None):
    if bank.exists():
        raise ValueError('use a fresh bank path')
    document = read(harvest / 'harvest.json')
    require_source(source, document)
    bank.mkdir(parents=True)
    # Use the exact pinned exporter's family function, not a local redefinition.
    exporter_path = Path(os.environ['BORG_CEMETERY_DIR']) / 'scripts/native/export-death.py'
    module = importlib.util.spec_from_file_location('pinned_exporter', exporter_path)
    exporter = importlib.util.module_from_spec(module)
    module.loader.exec_module(exporter)
    packages = [read(p) for p in (harvest / 'deaths').glob('*/record.json')]
    results = []
    for attempt in document['attempts']:
        if only and attempt['id'] not in only:
            continue
        run = harvest / attempt['id']
        result = dict(id=attempt['id'], natural_status=attempt['status'], status='excluded')
        try:
            if attempt['status'] not in ('death', 'survived_cap'):
                raise ValueError('natural run did not finish validly')
            compact = []
            for number, observation in rows(run / 'observations.jsonl.gz'):
                compact.append(dict(line=number, turn=observation['turn'], s=observation['status'], monsters=observation['monsters']))
            messages = []
            with gzip.open(run / 'messages.log.gz', 'rt') as stream:
                for line in stream:
                    parts = line.rstrip('\n').split(' ', 3)
                    if len(parts) == 4:
                        messages.append(dict(turn=int(parts[1]), text=parts[3]))
            selection = select(compact, messages, read(run / 'knowledge.json')['races'], attempt['summary'])
            checkpoints = [json.loads(line) for line in (run / 'checkpoints/index.jsonl').read_text().splitlines()]
            eligible = [c for c in checkpoints if c['game_turn'] <= selection['trigger_turn'] and c['clevel'] <= 5]
            if not eligible:
                raise ValueError('no checkpoint before observable trigger')
            checkpoint = eligible[-1]
            start = checkpoint['game_turn']
            initial_compact = next(o for o in compact if o['turn'] == start)
            wanted = {initial_compact['line'], selection['observation_line']}
            witnesses = {n: o for n, o in rows(run / 'observations.jsonl.gz') if n in wanted}
            initial = witnesses[initial_compact['line']]
            with gzip.open(run / 'state.log.gz', 'rt') as stream:
                state_line = list(stream)[checkpoint['keys'] - 1]
            state = STATE.match(state_line)
            resources = list(map(int, state.groups()[3:]))
            if resources != [initial['status'][k] for k in ('hp', 'max_hp', 'sp', 'max_sp')]:
                raise ValueError('checkpoint observation/resource witness differs')
            name = attempt['id']
            dest = bank / name
            dest.mkdir()
            saved = run / 'checkpoints' / (checkpoint['file'] + '.gz')
            shutil.copyfile(saved, dest / 'start.save.gz')
            with gzip.open(saved, 'rb') as stream:
                save_sha = hashlib.sha256(stream.read()).hexdigest()
            shutil.copyfile(source / 'harness/profiles/reborn-default.txt', dest / 'profile.txt')
            write(dest / 'initial-observation.json', initial)
            if selection['observation_line'] is not None:
                write(dest / 'first-observation.json', witnesses[selection['observation_line']])
            config = kv(run / 'config.txt')
            if sha(dest / 'profile.txt') != config['profile_sha256']:
                raise ValueError('preparation profile differs from original run')
            family = exporter.run_family(attempt['summary'], config, 'rust', document['build']['source_sha256'], flags=config['flags'])
            parent = next((p for p in packages if p['encounter_family'] == family), None)
            parent_id = death_id(family, next(a['result_sha256'] for a in parent['attempts'] if a['role'] == 'original')) if parent else None
            if attempt['status'] == 'death' and parent_id is None:
                raise ValueError('original death package missing')
            selection.update(lead_engine_turns=selection['trigger_turn'] - start,
                             observation_sha256=next(r['sha256'] for r in attempt['retention'] if r['file'] == 'observations.jsonl'))
            write(dest / 'trigger-witness.json', selection)
            # Keep large observation-only material out of the scenario contract.
            brief = {k: v for k, v in selection.items() if k not in ('worst', 'contacts')}
            value = dict(schema='borg-cemetery/save-scenario@1', id=name, status='ready_for_restart_trials',
                save='start.save.gz', save_sha256=save_sha, compressed_sha256=sha(dest / 'start.save.gz'),
                birth_seed=attempt['seed'], race_idx=attempt['race'], class_idx=attempt['cls'], start_turn=start,
                original_endpoint_turn=attempt['summary']['game_turns'],
                event_kind='death_encounter' if parent else 'surviving_encounter',
                startup_contract='fresh_borg_saved_engine_rng', borg_memory_restored=False,
                original_continuation_verified=False, independent_life=False,
                baseline_profile='profile.txt', baseline_profile_sha256=sha(dest / 'profile.txt'),
                origin=dict(program='borg-reborn-rs', seed=attempt['seed'], source_commit=document['build']['git_rev'],
                    source_sha256=document['build']['source_sha256'], binary_sha256=document['build']['binary_sha256'],
                    parent_death_id=parent_id, encounter_family=family), checkpoint=checkpoint, selection=brief,
                initial_observed=dict(zip(('hp', 'max_hp', 'sp', 'max_sp'), resources)), coverage=coverage(initial))
            write(dest / 'scenario.json', value)
            result.update(status='selected', scenario=(dest / 'scenario.json').relative_to(root).as_posix(),
                          sha256=sha(dest / 'scenario.json'), coverage=value['coverage'], parent_death_id=parent_id)
        except Exception as error:
            result['reason'] = str(error)
        results.append(result)
        write(bank / 'selection-results.json', dict(schema='borg-cemetery/encounter-selection@1', attempts=results))
        print(attempt['id'], result['status'], result.get('reason', ''), flush=True)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('harvest', 'source', 'bank', 'root'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--only', nargs='+', help='explicit subset for a fresh preparation attempt')
    args = parser.parse_args()
    curate(args.harvest.resolve(), args.source.resolve(), args.bank.resolve(), args.root.resolve(), args.only)
