#!/usr/bin/env python3
"""Natural death and observed critical-HP recovery starts, with explicit evidence."""
import bisect
import gzip
import json
from pathlib import Path
import re

LOW = 0.25
RECOVERED = 0.50


def text_open(path):
    return gzip.open(path, 'rt') if path.suffix == '.gz' else path.open()


def load_frames(path):
    frames, episodes, active, critical, recoveries = [], [], {}, None, []
    previous_hp = None
    with text_open(path) as stream:
        for number, raw in enumerate(stream, 1):
            o = json.loads(raw)
            s = o['status']
            row = dict(line=number, turn=o['turn'], hp=s['hp'], max_hp=s['max_hp'], sp=s['sp'], max_sp=s['max_sp'],
                       level=s['level'], depth=s['depth'], monsters=[dict(index=m['index'], race=m['race']) for m in o['monsters']])
            frames.append(row)
            present = {(s['depth'], m['index'], m['race']) for m in o['monsters']}
            for key in list(active):
                if key not in present:
                    episodes.append(active.pop(key))
            for m in o['monsters']:
                key = (s['depth'], m['index'], m['race'])
                if key not in active:
                    active[key] = dict(depth=s['depth'], index=m['index'], race=m['race'], first=o['turn'], last=o['turn'], line=number)
                active[key]['last'] = o['turn']
            if s['hp'] >= 0 and s['max_hp'] > 0:
                if critical is None and s['hp'] / s['max_hp'] <= LOW and previous_hp is not None and s['hp'] < previous_hp:
                    critical = dict(first=row, minimum=row)
                elif critical is not None:
                    if s['hp'] / s['max_hp'] < critical['minimum']['hp'] / critical['minimum']['max_hp']:
                        critical['minimum'] = row
                    if s['hp'] / s['max_hp'] >= RECOVERED:
                        recoveries.append(dict(**critical, recovery=row))
                        critical = None
            previous_hp = s['hp']
    episodes.extend(active.values())
    return frames, episodes, recoveries


def messages(path):
    result = []
    with text_open(path) as stream:
        for raw in stream:
            p = raw.rstrip('\n').split(' ', 3)
            if len(p) == 4:
                result.append(dict(turn=int(p[1]), type=int(p[2]), text=p[3]))
    return result


def attacker(message_rows, races, cutoff):
    verbs = ('hits you', 'bites you', 'touches you', 'claws you', 'stings you', 'crushes you', 'kicks you',
             'punches you', 'butts you', 'gazes at you', 'spits at you', 'releases spores at you', 'casts', 'breathes')
    for m in reversed(message_rows):
        if not cutoff - 500 <= m['turn'] <= cutoff or not any(v in m['text'].lower() for v in verbs):
            continue
        text = m['text'].lower()
        match = [r for r in races if text.startswith(('the ' + r['name'].lower() + ' ', r['name'].lower() + ' '))]
        if match:
            return max(match, key=lambda r: len(r['name']))
    return None


def onset(episodes, message_rows, races, cutoff, cause=None):
    kind = next((r for r in races if cause in (r['name'], 'a ' + r['name'], 'an ' + r['name'], 'the ' + r['name'])), None) if cause else None
    if cause and kind is None and cause != 'poison':
        raise ValueError('environmental death needs a separate observable-trigger adapter')
    if kind is None:
        kind = attacker(message_rows, races, cutoff)
    choices = [e for e in episodes if kind and e['race'] == kind['index'] and e['first'] <= cutoff and e['last'] >= cutoff - 500]
    if choices:
        selected = max(choices, key=lambda e: e['last'])
        contacts = [m for m in message_rows if selected['first'] - 10 <= m['turn'] <= selected['last'] + 10 and
                    m['text'].lower().startswith('the ' + kind['name'].lower() + ' ') and ' you' in m['text']]
        return dict(trigger_turn=min([selected['first']] + [m['turn'] for m in contacts]), first_visible_turn=selected['first'],
                    monster_kind=kind['name'], monster_index=selected['index'], observation_line=selected['line'],
                    kind='first_visible_kind_in_incident_episode', terminal_individual_identity='unavailable; kind association only',
                    no_omniscient_trigger=True)
    contacts = [m for m in message_rows if cutoff - 1000 <= m['turn'] <= cutoff and m['text'].startswith('Something ') and ' you' in m['text']]
    if contacts:
        episode = [contacts[-1]]
        for m in reversed(contacts[:-1]):
            if episode[-1]['turn'] - m['turn'] > 200:
                break
            episode.append(m)
        return dict(trigger_turn=episode[-1]['turn'], monster_kind='unseen attacker', monster_index=None, observation_line=None,
                    kind='first_observable_unseen_contact', terminal_individual_identity='unavailable', no_omniscient_trigger=True)
    raise ValueError('no observable incident threat association')


def candidates(run, summary):
    compact = run / 'encounters.jsonl'
    if not compact.exists():
        compact = run / 'encounters.jsonl.gz'
    frames, episodes, recoveries = load_frames(compact)
    log = run / 'messages.log'
    if not log.exists():
        log = run / 'messages.log.gz'
    message_rows = messages(log)
    races = json.loads((run / 'knowledge.json').read_text())['races']
    checkpoints = [json.loads(line) for line in (run / 'checkpoints/index.jsonl').read_text().splitlines()]
    result = []
    incidents = [dict(type='observed_critical_recovery', turn=r['minimum']['turn'], witness=r) for r in recoveries]
    if summary.get('dead'):
        incidents.append(dict(type='death', turn=summary['game_turns'], witness=dict(cause=summary['death_cause'])))
    for incident in incidents:
        row = dict(**incident, status='excluded')
        try:
            trigger = onset(episodes, message_rows, races, incident['turn'], summary['death_cause'] if incident['type'] == 'death' else None)
            eligible = [c for c in checkpoints if c['game_turn'] <= trigger['trigger_turn']]
            if not eligible:
                raise ValueError('no saved state before first observable threat')
            checkpoint = eligible[-1]
            if incident['turn'] - checkpoint['game_turn'] > 2000:
                raise ValueError('incident exceeds fast 2000-engine-turn horizon from onset')
            row.update(status='candidate', selection=trigger, checkpoint=checkpoint)
        except ValueError as error:
            row['reason'] = str(error)
        result.append(row)
    return result
