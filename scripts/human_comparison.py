"""Describe survival past the original death time without inventing a rescue."""
import hashlib
import json
import tarfile


def compare(observed, scenario, *, save_captured, verified, cause=None):
    start = scenario['start_turn']
    endpoint = scenario.get('original_endpoint_turn')
    matching = [i for i, row in enumerate(observed) if row.get('turn') == start
                and row.get('race_idx') == scenario['race_idx'] and row.get('class_idx') == scenario['class_idx']]
    rows = observed[matching[0]:] if matching else []
    beyond = next((i for i, row in enumerate(rows) if isinstance(endpoint, int)
                   and row.get('turn', 0) > endpoint and not row.get('dead') and row.get('hp', 0) > 0), None)
    checked = rows[:beyond + 1] if beyond is not None else rows
    monotonic = all(a.get('turn', 0) <= b.get('turn', 0) for a, b in zip(checked, checked[1:]))
    # player.h at the qualified e473720 engine: WIZARD=0x2, DEBUG=0x8.
    ordinary = bool(checked) and all(row.get('cheat_live') == 0 and isinstance(row.get('noscore'), int)
                                    and not row['noscore'] & 0xA for row in checked)
    continuous = bool(checked) and monotonic and all(not row.get('dead')
        and row.get('race_idx') == scenario['race_idx'] and row.get('class_idx') == scenario['class_idx'] for row in checked)
    qualified = bool(matching) and save_captured and verified and ordinary and continuous
    last = {}
    previous = start
    for row in rows:
        if row.get('turn', 0) < previous or row.get('dead') or row.get('hp', -1) < 0:
            break
        if row.get('race_idx') != scenario['race_idx'] or row.get('class_idx') != scenario['class_idx']:
            break
        last, previous = row, row.get('turn', 0)
    if not last:
        last = rows[-1] if rows else (observed[-1] if observed else {})
    target_present, target_visible = False, False
    details = None
    for row in rows:
        details = row.get('details') or details
        for monster in (details or {}).get('monsters', []):
            if cause and monster.get('name', '').casefold() == cause.casefold():
                target_present = True
                target_visible |= bool(monster.get('visible'))
    return dict(schema='borg-cemetery/human-survival-comparison@1', saved_turn=start,
                original_death_turn=endpoint, last_turn=last.get('turn'), hp=last.get('hp'),
                max_hp=last.get('max_hp'), level=last.get('level'),
                beyond_original_death=qualified and beyond is not None,
                engine_ticks_beyond_original=(last.get('turn', 0) - endpoint) if isinstance(endpoint, int) else None,
                observed_beyond_original=beyond is not None,
                original_save_captured=save_captured, start_observed=bool(matching),
                replay_verified=verified, ordinary_play_flags=ordinary, continuous=continuous,
                original_cause=cause, original_cause_visible=target_visible if target_present else None,
                scope='One recorded continuation from a retained save; not a direct-fight or population-survival claim.')


def recording_comparison(recording, scenario, verified, cause=None):
    with (recording / 'frames.jsonl').open() as stream:
        observed = [json.loads(line) for line in stream]
    captured = any(hashlib.sha256(p.read_bytes()).hexdigest() == scenario['save_sha256']
                   for p in recording.glob('file-input-*.bin'))
    return compare(observed, scenario, save_captured=captured, verified=verified, cause=cause)


def archive_comparison(entry, cause=None):
    meta = json.loads((entry / 'alternative.json').read_text())
    packed = entry / 'recording.tar.xz'
    if hashlib.sha256(packed.read_bytes()).hexdigest() != meta['recording_sha256']:
        raise ValueError('Human recording archive differs from the retained capture hash.')
    with tarfile.open(packed) as archive:
        observed = [json.loads(line) for line in archive.extractfile('recording/frames.jsonl')]
        captured = any(hashlib.sha256(archive.extractfile(member).read()).hexdigest() == meta['save_sha256']
                       for member in archive.getmembers() if member.isfile() and '/file-input-' in member.name)
    return compare(observed, meta['scenario_manifest'], save_captured=captured,
                   verified=meta['verification']['verified'], cause=cause)


def prose(result):
    if result['beyond_original_death']:
        return (f"Survived beyond the original death turn {result['original_death_turn']}: "
                f"the continuation was last observed alive at {result['last_turn']}, "
                f"{result['engine_ticks_beyond_original']} engine ticks later, "
                f"with {result['hp']}/{result['max_hp']} HP at level {result['level']}.")
    if result['observed_beyond_original']:
        return 'Observed alive beyond the original death time, but the starting-save, replay or continuity checks are incomplete; no qualified survival comparison is claimed.'
    return 'The recording does not establish survival beyond the original death time.'


def markdown(result):
    rows = ['## Comparison with the original death', '', '**' + prose(result) + '**', '',
            '| Observation | Result |', '| --- | --- |',
            f"| Retained starting save | Turn {result['saved_turn']} |",
            f"| Original Borg death | Turn {result['original_death_turn']} |",
            f"| Last recorded continuation | Turn {result['last_turn']}; HP {result['hp']}/{result['max_hp']}; level {result['level']} |",
            f"| Original save bytes captured | {'Yes' if result['original_save_captured'] else 'Not established'} |",
            f"| Recorder replay verification | {'Passed' if result['replay_verified'] else 'Not passed'} |",
            f"| Continuous ordinary-play observations through comparison | {'Yes' if result['ordinary_play_flags'] and result['continuous'] else 'Not established'} |", '']
    if result['original_cause_visible'] is False:
        rows += [f"{result['original_cause']} was never recorded as visible in this continuation. "
                 'This shows survival from the saved situation; it does not demonstrate defeating that enemy in a direct fight.', '']
    rows += ['The identified human-play runtime and chosen route may differ from the original Borg run. '
             'This is one alternative from the retained starting position, not a general policy improvement, '
             'an exact restoration of original private Borg memory, or an additional independent life.', '']
    return '\n'.join(rows)
