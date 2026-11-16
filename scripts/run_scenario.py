#!/usr/bin/env python3
"""Load a curated game save into a pinned, already-built alternative Borg."""
import argparse
import gzip
import os
from pathlib import Path
import shutil
import subprocess
import sys

from run_batch import command, digest, git, kv, read_json, write_json


def run_scenario(source, scenario_dir, out, turns=1000, wall_seconds=120, profile=None):
    source, scenario_dir, out = source.resolve(), scenario_dir.resolve(), out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    scenario_file = scenario_dir / 'scenario.json'
    scenario = read_json(scenario_file)
    receipt = dict(schema='borg-cemetery/scenario-trial@1', status='preparing',
                   scenario_sha256=digest(scenario_file),
                   save_sha256=scenario.get('save_sha256'),
                   startup_contract='fresh_borg_saved_engine_rng',
                   borg_memory_restored=False, origin=scenario.get('origin'),
                   horizon_engine_turns=turns)
    write_json(out / 'trial.json', receipt)
    try:
        if scenario.get('status') != 'ready_for_restart_trials':
            raise ValueError('scenario has no usable checkpoint')
        if scenario.get('startup_contract') != receipt['startup_contract']:
            raise ValueError('unsupported scenario startup contract')
        name = scenario['save']
        if Path(name).name != name:
            raise ValueError('scenario save must be a local filename')
        packed = scenario_dir / name
        if digest(packed) != scenario['compressed_sha256']:
            raise ValueError('compressed scenario save hash mismatch')
        save = out / 'input.save'
        with gzip.open(packed, 'rb') as src, save.open('wb') as dest:
            shutil.copyfileobj(src, dest)
        if digest(save) != scenario['save_sha256']:
            raise ValueError('scenario save hash mismatch')
        build = kv(source / 'build/rust/BUILD_ID')
        binary = source / 'build/rust/game/angband'
        head = git(source, 'rev-parse', 'HEAD')
        if (build.get('git_rev') != head or build.get('impl') != 'rust' or
                build.get('inputs_dirty') != 'no' or digest(binary) != build.get('binary_sha256')):
            raise ValueError('target build does not match its pinned source/binary')
        current_inputs = subprocess.check_output(
            ['bash', str(source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
        if current_inputs != build.get('source_sha256'):
            raise ValueError('target build inputs have changed')
        env = dict(os.environ, BORG_IMPL='rust', TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8',
                   RUN_TIMEOUT_SECONDS=str(wall_seconds), CHECKPOINT_EVERY='0',
                   BORG_CEMETERY_DIR=os.environ.get('BORG_CEMETERY_DIR', str(Path(__file__).resolve().parents[1])),
                   BORG_DEATH_RECORDS_DIR=str(out / 'native-deaths'))
        for key in ('ANGBAND_BIN', 'BORG_PROFILE', 'BORGH_DATA_ROOT', 'BORG_TEST_FEATURES',
                    'STALL_TIMEOUT_SECONDS', 'SAVE_ROOT'):
            env.pop(key, None)
        env['SAVE_ROOT'] = str(out)
        env['BORG_OBSERVATION_LOG'] = str(out / 'run/observations.jsonl')
        if profile is None and head == scenario.get('origin', {}).get('source_commit') and scenario.get('baseline_profile'):
            name = scenario['baseline_profile']
            if Path(name).name != name:
                raise ValueError('baseline profile must be a local filename')
            profile = scenario_dir / name
            if digest(profile) != scenario['baseline_profile_sha256']:
                raise ValueError('baseline profile hash mismatch')
        if profile:
            shutil.copy2(profile, out / 'profile.txt')
            env['BORG_PROFILE'] = str(out / 'profile.txt')
            receipt['profile_sha256'] = digest(out / 'profile.txt')
        start = scenario['start_turn']
        cap = start + turns
        receipt.update(status='running', source_commit=head, build=build,
                       start_turn=start, cap_turn=cap)
        write_json(out / 'trial.json', receipt)
        raw = out / 'run'
        rc = command(['bash', 'harness/run.sh', str(raw), str(scenario['birth_seed']),
                      str(scenario['race_idx']), str(scenario['class_idx']), str(cap),
                      'menu,keep-load-rng,save=input.save'],
                     cwd=source, env=env, log=out / 'launcher.log', timeout=wall_seconds + 30)
        summary, process = read_json(raw / 'summary.json'), read_json(raw / 'process.json')
        status = 'harness_failure'
        if rc == 124 or process.get('status') == 'timeout':
            status = 'timeout'
        elif (not rc and summary.get('loaded_turn') == start and
              summary.get('loaded', True) is True and summary.get('seed') == scenario['birth_seed'] and
              summary.get('race_idx') == scenario['race_idx'] and
              summary.get('class_idx') == scenario['class_idx']):
            if summary.get('dead') is True and summary.get('stop_reason') == 'death':
                status = 'death'
            elif (summary.get('dead') is False and summary.get('stop_reason') == 'turns'
                  and summary.get('game_turns', 0) >= cap):
                status = 'survived_horizon'
            else:
                status = 'stopped'
        elif not rc:
            status = 'load_identity_mismatch'
        options = summary.get('game_options', {})
        if (any(value for key, value in options.items() if key.startswith('cheat_')) or
                summary.get('effective_settings', {}).get('borg_cheat_death')):
            status = 'config_error'
        if profile and not rc and kv(raw / 'config.txt').get('profile_sha256') != receipt['profile_sha256']:
            status = 'config_error'
        receipt.update(status=status, exit_code=rc, summary=summary, process=process)
        return int(status not in ('death', 'survived_horizon'))
    except Exception as exc:
        receipt.update(status='failed', error=str(exc))
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        write_json(out / 'trial.json', receipt)


def compare_trials(baseline, candidate):
    for key in ('scenario_sha256', 'save_sha256', 'startup_contract', 'horizon_engine_turns'):
        if baseline.get(key) is None or baseline[key] != candidate.get(key):
            raise ValueError(f'trials differ or lack {key}')
    a, b = baseline['status'], candidate['status']
    result = 'inconclusive'
    if all(s in ('death', 'survived_horizon') for s in (a, b)):
        result = ('rescued' if a == 'death' and b == 'survived_horizon'
                  else 'newly_killed' if a == 'survived_horizon' and b == 'death'
                  else 'same_survival_outcome')
    return dict(schema='borg-cemetery/scenario-comparison@1', result=result,
                baseline=baseline, candidate=candidate,
                interpretation='Shared saved game with fresh Borg memory in both arms; survival to a finite horizon.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    run = sub.add_parser('run')
    run.add_argument('--source', type=Path, required=True)
    run.add_argument('--scenario', type=Path, required=True)
    run.add_argument('--out', type=Path, required=True)
    run.add_argument('--turns', type=int, default=1000)
    run.add_argument('--wall-seconds', type=int, default=120)
    run.add_argument('--profile', type=Path)
    compare = sub.add_parser('compare')
    compare.add_argument('baseline', type=Path)
    compare.add_argument('candidate', type=Path)
    compare.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if a.action == 'compare':
        write_json(a.out, compare_trials(read_json(a.baseline), read_json(a.candidate)))
    else:
        if not 1 <= a.turns <= 1000000000 or not 1 <= a.wall_seconds <= 120:
            p.error('turns must be 1..1000000000; wall-seconds 1..120')
        sys.exit(run_scenario(a.source, a.scenario, a.out, a.turns, a.wall_seconds, a.profile))
