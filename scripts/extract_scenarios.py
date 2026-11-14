#!/usr/bin/env python3
"""Reconstruct adverse episodes and curate actual engine saves for Borg trials."""
import argparse
import gzip
import json
from pathlib import Path
import re
import shutil

from run_batch import digest, read_json, write_json
from episode_inventory import extract_inventory
from death_pages import episode_page, analysis_page, run_page
from human_readable import action, threat

STATE = re.compile(r'^(\d+) (-?\d+),(-?\d+) d(\d+)/(\d+) hp(-?\d+)/(\d+)(?: sp(-?\d+)/(\d+))?')


def states(path):
    found = []
    if path.exists():
        with path.open() as stream:
            for number, line in enumerate(stream, 1):
                match = STATE.match(line)
                if match:
                    values = [int(v) if v is not None else None for v in match.groups()]
                    found.append(dict(zip(('turn', 'x', 'y', 'depth', 'max_depth',
                                           'hp', 'max_hp', 'sp', 'max_sp'), values),
                                      line=number, raw=line.rstrip()))
    return found


def jsonlines(path):
    if path.exists():
        with path.open() as stream:
            for number, line in enumerate(stream, 1):
                try:
                    value = json.loads(line)
                    if isinstance(value, dict):
                        yield dict(line=number, value=value)
                except ValueError:
                    continue


def events(rows, summary, decisions=(), stable_hp=0.7, stable_samples=3, low_hp=0.25):
    """Follow decline from sustained stability through recovery/death.

    Stability is an inference, never proof of safety. Repeated keys at the same
    engine turn cannot by themselves establish sustained stability.
    """
    found, active, last_stable = [], None, None
    streak, last_turn, index, latest = 0, None, 0, None
    traces = sorted((d['value'] for d in decisions if isinstance(d['value'].get('turn'), int)),
                    key=lambda d: d['turn'])
    for row in rows:
        while index < len(traces) and traces[index]['turn'] <= row['turn']:
            latest = traces[index]
            index += 1
        threat = (latest or {}).get('threat') or {}
        healthy = row['max_hp'] > 0 and row['hp'] / row['max_hp'] >= stable_hp
        safe_estimate = (not threat or
                         (threat.get('p_death', 0) == 0 and threat.get('worst', 0) < row['hp']
                          and threat.get('disabling', 0) <= 0.05))
        stable = healthy and safe_estimate
        if stable:
            if row['turn'] != last_turn:
                streak += 1
            if streak >= stable_samples:
                last_stable = dict(row, threat_evidence='available' if threat else 'missing')
        else:
            streak = 0
        last_turn = row['turn']
        low_health = 0 < row['hp'] <= low_hp * row['max_hp']
        estimated_lethal_risk = (row['hp'] > 0 and bool(threat) and
                                (threat.get('p_death', 0) >= 0.1 or threat.get('worst', 0) >= row['hp']))
        if low_health or estimated_lethal_risk:
            if active is None:
                active = dict(kind='near_death_candidate', start=last_stable or rows[0],
                              start_basis='stable_observation' if last_stable else 'no_stable_boundary_observed',
                              trigger=row, trigger_reason='low_hp' if low_health else 'estimated_lethal_risk',
                              trigger_threat=threat, worst=row, end=row, resolution='unresolved')
            if row['hp'] / row['max_hp'] < active['worst']['hp'] / active['worst']['max_hp']:
                active['worst'] = row
        if active:
            active['end'] = row
            if stable and streak >= stable_samples:
                active['resolution'] = 'recovered_to_stable'
                found.append(active)
                active = None
    if summary.get('dead') is True and summary.get('stop_reason') == 'death':
        if active is None:
            active = dict(start=last_stable or (rows[0] if rows else None),
                          start_basis='stable_observation' if last_stable else 'no_stable_boundary_observed',
                          trigger=None, worst=None, end=rows[-1] if rows else None)
        active.update(kind='death', turn=summary['game_turns'], cause=summary.get('death_cause'),
                      resolution='death')
        found.append(active)
    elif active:
        found.append(active)
    for event in found:
        if 'turn' not in event:
            event['turn'] = event['worst']['turn']
    return found


def sequence(raw, rows, decisions, start, end, end_line):
    timeline = [dict(stream='state.log', line=r['line'], turn=r['turn'], state=r)
                for r in rows if start <= r['turn'] <= end and r['line'] <= end_line]
    timeline += [dict(stream='trace.jsonl', line=d['line'], turn=d['value']['turn'], decision=d['value'])
                 for d in decisions if isinstance(d['value'].get('turn'), int)
                 and start <= d['value']['turn'] <= end]
    if (raw / 'messages.log').exists():
        with (raw / 'messages.log').open() as stream:
            for number, line in enumerate(stream, 1):
                parts = line.rstrip().split(' ', 3)
                if len(parts) == 4 and parts[0].isdigit() and parts[1].isdigit():
                    turn = int(parts[1])
                    if start <= turn <= end:
                        timeline.append(dict(stream='messages.log', line=number, turn=turn,
                                             key_position=int(parts[0]), message=parts[3]))
    # Cross-stream ordering at one turn is unresolved.
    return sorted(timeline, key=lambda item: (item['turn'], item['stream'], item['line']))


def curate_save(raw, identity, event, dest):
    start = event['start']
    result = dict(schema='borg-cemetery/save-scenario@1', status='missing_checkpoint',
                  origin={key: identity.get(key) for key in ('seed', 'program', 'source_commit', 'binary_sha256')},
                  race_idx=identity.get('race_idx'), class_idx=identity.get('class_idx'),
                  birth_seed=identity.get('seed'), event_kind=event['kind'],
                  original_endpoint_turn=event['turn'],
                  startup_contract='fresh_borg_saved_engine_rng', borg_memory_restored=False,
                  original_continuation_verified=False)
    if start:
        eligible = [d['value'] for d in jsonlines(raw / 'checkpoints/index.jsonl')
                    if isinstance(d['value'].get('game_turn'), int)
                    and d['value']['game_turn'] <= start['turn']
                    and d['value'].get('keys', 0) <= start['line']]
        for checkpoint in sorted(eligible, key=lambda c: (c['game_turn'], c.get('keys', 0)), reverse=True):
            name = checkpoint.get('file', '')
            if not name or Path(name).name != name:
                continue
            save = raw / 'checkpoints' / name
            if not save.is_file() or save.is_symlink():
                continue
            if any(checkpoint.get(k) != identity.get(k) for k in ('seed', 'race_idx', 'class_idx')):
                continue
            dest.mkdir(parents=True, exist_ok=True)
            packed = dest / 'start.save.gz'
            with save.open('rb') as source, packed.open('wb') as target:
                with gzip.GzipFile(fileobj=target, mode='wb', mtime=0) as compressed:
                    shutil.copyfileobj(source, compressed)
            result.update(status='ready_for_restart_trials', save='start.save.gz',
                          save_sha256=digest(save), compressed_sha256=digest(packed),
                          checkpoint=checkpoint, start_turn=checkpoint['game_turn'],
                          report_start_turn=start['turn'],
                          checkpoint_lead_turns=start['turn'] - checkpoint['game_turn'])
            break
    write_json(dest / 'scenario.json', result)
    return result


def escaped(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def report_event(path, event, timeline, scenario):
    start = event['start']
    observations = [entry['state'] for entry in timeline if 'state' in entry]
    decisions = [entry['decision'] for entry in timeline if 'decision' in entry]
    summary = []
    if observations:
        first = observations[0]
        lowest = min(observations, key=lambda r: r['hp'] / max(1, r['max_hp']))
        summary.append(f"At the saved/report starting point (turn {first['turn']}), the character had "
                       f"{first['hp']}/{first['max_hp']} HP at depth {first['depth']}. "
                       f"The lowest logged HP was {lowest['hp']}/{lowest['max_hp']} at turn {lowest['turn']}.")
    if decisions:
        modes = []
        for decision in decisions:
            mode = decision.get('mode', 'unreported')
            if not modes or modes[-1] != mode:
                modes.append(mode)
        summary.append('Observed Borg mode sequence: ' + ' → '.join(modes) + '.')
    title = 'Death' if event['kind'] == 'death' else 'Near-death candidate'
    resolution = {'death': 'The character died.', 'recovered_to_stable': 'The character returned to sustained stability.',
                  'unresolved': 'The run ended before sustained recovery was established.'}.get(event['resolution'], 'Outcome not established.')
    text = [f"# {title}: observed sequence", '',
            f"The inferred reasonably stable starting point is turn {start['turn'] if start else 'unknown'}. "
            f"The {'death' if event['kind'] == 'death' else 'worst recorded risk point'} is at turn {event['turn']}. "
            f"The account follows observations through turn {(event['end'] or {}).get('turn', event['turn'])}. {resolution}", '',
            'The start is inferred from sustained HP and available Borg threat estimates, '
            'not proof of safety. Missing threat, inventory or perception evidence stays unknown. '
            'Follow earlier causes beyond this boundary when needed.', '',
            ('A playable starting save is retained. ' if scenario.get('save') else 'No playable starting save was retained. ') +
            'Saved-position trials start a fresh Borg with the saved engine RNG; original private Borg memory is not restored.', '',
            f"Retained save turn: {scenario.get('start_turn', 'unavailable')}; "
            f"inferred stable boundary: {start['turn'] if start else 'unknown'}.", '',
            ' '.join(summary), '',
            'Chronology is ordered by engine turn. Ordering between different evidence streams at the same turn '
            'is unresolved. The table shows state changes, game messages and recorded Borg decisions.', '',
            '| Turn | Evidence | Observation |', '| --- | --- | --- |']
    previous = None
    for entry in timeline:
        if 'state' in entry:
            r = entry['state']
            signature = (r['hp'], r['max_hp'], r['sp'], r['max_sp'], r['depth'])
            if signature == previous:
                continue
            previous = signature
            observation = f"HP {r['hp']}/{r['max_hp']}; SP {r['sp']}/{r['max_sp']}; depth {r['depth']}; position {r['x']},{r['y']}"
        elif 'decision' in entry:
            d = entry['decision']
            observation = (f"Strategy: {d.get('mode', 'not recorded')}; goal: {d.get('goal', 'not recorded')}. "
                           f"{action(d.get('choice'))}. {threat(d.get('threat'))}.")
        else:
            observation = entry['message']
        label = {'state.log': 'State observation', 'trace.jsonl': 'Borg decision', 'messages.log': 'Game message'}.get(entry['stream'], 'Observation')
        text.append(f"| {entry['turn']} | {label} {entry['line']} | {escaped(observation)} |")
    text += ['', f"Terminal observation: {escaped(event.get('cause', event['resolution']))}.", '',
             'Investigate any evidence-backed survival improvement. Separate facts, hypotheses '
             'and missing observations; propose a mechanism, intervention, prediction and experiment. '
             'No predefined behavior checklist limits the investigation.', '']
    path.write_text('\n'.join(text))


def extract(raw, record, out, stable_hp=0.7, stable_samples=3):
    rows = states(raw / 'state.log')
    identity = read_json(record / 'run.json')
    terminal = read_json(raw / 'summary.json')
    decisions = list(jsonlines(raw / 'trace.jsonl'))
    if identity.get('status') != 'death':
        terminal['dead'] = False
    selected = events(rows, terminal, decisions, stable_hp, stable_samples)
    for number, event in enumerate(selected, 1):
        event['id'] = f'event-{number}'
        dest = out / event['id']
        scenario = curate_save(raw, identity, event, dest)
        profile = record.parent / 'profile.txt'
        if profile.is_file():
            shutil.copy2(profile, dest / 'baseline-profile.txt')
            scenario.update(baseline_profile='baseline-profile.txt', baseline_profile_sha256=digest(profile))
            write_json(dest / 'scenario.json', scenario)
        start = scenario.get('start_turn', (event['start'] or {}).get('turn', 0))
        end = max(event['turn'], (event['end'] or {}).get('turn', event['turn']))
        timeline = sequence(raw, rows, decisions, start, end, (event['end'] or {}).get('line', 0))
        write_json(dest / 'sequence.json', timeline)
        report_event(dest / 'report.md', event, timeline, scenario)
        inventory = extract_inventory(raw, dest, start, end)
        with (dest / 'report.md').open('a') as report:
            report.write(f"\n[Inventory, equipment and spells](inventory.md): {inventory['status']}.\n")
            media = raw / 'media' / event['id']
            if media.is_dir():
                shutil.copytree(media, dest / 'media', dirs_exist_ok=False)
                status = read_json(media / 'media.json')
                if status.get('gif') and (dest / 'media' / status['gif']).is_file():
                    report.write('\n![Episode: actual terminal screenshots](media/episode.gif)\n')
                report.write(f"\nAnimation capture: {status.get('status', 'unavailable')}; provenance in media/media.json.\n")
        event.update(scenario=scenario, sequence=f"{event['id']}/sequence.json", report=f"{event['id']}/report.md")
        episode_page(dest, event, identity)
    result = dict(schema='borg-cemetery/scenarios@2', identity=identity, events=selected,
                  boundary_rule=dict(stable_hp_ratio=stable_hp, stable_distinct_turns=stable_samples,
                                     threat='zero estimated death chance; worst damage below HP; disabling <=5% when available'),
                  near_death_rule='living HP <=25%, estimated death chance >=10%, or worst estimated damage >=HP; ends at sustained stability or run termination',
                  limitations=['Boundary is heuristic and may need extending earlier.',
                               'Low HP misses some dangerous situations.',
                               'Save scenarios start a fresh Borg with saved engine RNG.',
                               'Original Borg memory and uninterrupted continuation are not restored.'])
    write_json(out / 'scenarios.json', result)
    (out / 'analysis.md').write_text(
        '# Adverse episode reports\n\n'
        f"Seed {identity.get('seed')}; source `{identity.get('source_commit')}`.\n\n"
        'Episodes follow the observed sequence from the last inferred stable state through '
        'deterioration, death or recovery. They do not use fixed-duration windows.\n\n' +
        ''.join(f"- [{e['id']}: {e['kind']}]({e['report']}); save: {e['scenario']['status']}.\n" for e in selected))
    analysis_page(out)
    run_page(record)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('batch', type=Path)
    p.add_argument('--stable-hp', type=float, default=0.7)
    p.add_argument('--stable-samples', type=int, default=3)
    a = p.parse_args()
    if not 0.25 < a.stable_hp <= 1 or a.stable_samples < 1:
        p.error('stable-hp must be >0.25 and <=1; stable-samples must be positive')
    for record in sorted((a.batch / 'records').glob('seed-*')):
        extract(a.batch / 'evidence' / record.name, record, record / 'analysis', a.stable_hp, a.stable_samples)


if __name__ == '__main__':
    main()
