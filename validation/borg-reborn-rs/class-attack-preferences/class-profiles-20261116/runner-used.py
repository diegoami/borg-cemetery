#!/usr/bin/env python3
"""Run the frozen paired class-preference smoke, preserving every attempt."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def trace_stats(path, expected_class):
    result = dict(rankings=0, positive_rankings=0, reranked_winners=0,
                  selected_families={}, first_reranked=None)
    with path.open() as stream:
        for line in stream:
            row = json.loads(line)
            assert row['schema'] == 'borg-reborn-rs/core-trace@2'
            for ranking in row['attacks']:
                result['rankings'] += 1
                raw_best = weighted_best = None
                for c in ranking['candidates']:
                    assert c['class_id'] == expected_class
                    raw, weight = c['raw_utility'], c['effective_weight']
                    expected = max(1, min(2147483647, raw * weight // 1000)) if raw > 0 else raw
                    assert c['adjusted_utility'] == expected
                    if raw > (raw_best['raw_utility'] if raw_best else 0):
                        raw_best = c
                    if c['adjusted_utility'] > (weighted_best['adjusted_utility'] if weighted_best else 0):
                        weighted_best = c
                assert ranking['winner'] == (weighted_best['attack_id'] if weighted_best else None)
                if weighted_best:
                    result['positive_rankings'] += 1
                    family = weighted_best['family']
                    result['selected_families'][family] = result['selected_families'].get(family, 0) + 1
                if raw_best and weighted_best and raw_best['attack_id'] != weighted_best['attack_id']:
                    result['reranked_winners'] += 1
                    if result['first_reranked'] is None:
                        result['first_reranked'] = dict(turn=row['turn'], raw_best=raw_best,
                                                       weighted_best=weighted_best)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--zoo', type=Path, required=True, help='Read-only pinned borg-zoo checkout')
    args = parser.parse_args()
    assert 1 <= args.jobs <= 3
    source, output = args.source.resolve(), args.output.resolve()
    plan_path = Path(__file__).with_name('plan.json')
    plan = json.loads(plan_path.read_text())
    output.mkdir(parents=True, exist_ok=False)
    write(output / 'plan.json', plan)
    binary = source / 'build/rust/game/angband'
    identity = source / 'harness/identity.sh'
    build_id = source / 'build/rust/BUILD_ID'
    build = dict(line.split('=', 1) for line in build_id.read_text().splitlines() if '=' in line)
    (output / 'BUILD_ID').write_bytes(build_id.read_bytes())
    parameter_prefix = 'attack_preference_'
    checker_spec = importlib.util.spec_from_file_location('zoo_check', source / 'harness/zoo-check.py')
    checker = importlib.util.module_from_spec(checker_spec)
    checker_spec.loader.exec_module(checker)
    zoo_tree = output / 'pinned-zoo'
    zoo_tree.mkdir()
    checker.pinned_tree(args.zoo.resolve(), plan['zoo_pin'], zoo_tree)
    checker.import_zoo(zoo_tree)
    adapter = importlib.import_module('zoo.borgrs')
    profile_build = output / 'profile-build'
    profile_build.mkdir()
    (profile_build / 'borg.txt').write_bytes((source / 'harness/borg.txt').read_bytes())

    def source_hash():
        return subprocess.check_output([str(identity), 'source-hash', 'rust'], text=True).strip()

    def run_case(case, arm):
        name = case['class'] + '-' + arm
        directory = output / name
        profile_path = plan_path.parent / (case['profile'] if arm == 'boosted' else plan['neutral_profile'])
        profile = json.loads(profile_path.read_text())
        expected_settings = {key.removeprefix('borg_param_'): value
                             for key, value in profile['settings'].items() if key.startswith('borg_param_')}
        for name in ['user', 'save', 'archive', 'panic', 'scores']:
            (directory / name).mkdir(parents=True)
        (directory / 'profile.json').write_bytes(profile_path.read_bytes())
        config = adapter.config_text(profile_build, profile, case['race_id'], case['class_id'])
        assert adapter.check_config(config, profile) is None
        (directory / 'user/borg.txt').write_text(config)
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(('BORG_', 'ANGBAND_', 'CHECKPOINT_', 'RUN_TIMEOUT_', 'SAVE_ROOT'))}
        env.update(BORG_CORE_TRACE='on', BORG_RUN_DIR=str(directory),
                   BORG_CEMETERY_DIR=str((source / 'vendor/borg-cemetery').resolve()),
                   BORG_DEATH_RECORDS_DIR=str(output / 'deaths'),
                   TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
        game_command = adapter.command(binary, directory, {'seed': case['seed']},
                                       case['race_id'], case['class_id'], {'cap': plan['game_turn_cap']},
                                       {'exact_turns': True, 'depth_stream': True})
        game_command += ['-msglog', str(directory / 'messages.log'), '-screen']
        command = [sys.executable, str(source / 'harness/supervise.py'), '--receipt',
                   str(directory / 'process.json'), '--diagnostics', str(directory),
                   '--timeout', '180', '--', *game_command]
        config_rows = [f"flags={plan['flags']}", f"borg_txt_sha256={sha(directory / 'user/borg.txt')}",
                       f"profile={profile_path.name}", f"profile_sha256={sha(profile_path)}"]
        (directory / 'config.txt').write_text('\n'.join(config_rows) + '\n')
        attempt = dict(name=name, arm=arm, case=case, command=command,
                       profile=profile_path.name, profile_sha256=sha(profile_path),
                       expected_settings=expected_settings)
        started = time.monotonic()
        with (output / (name + '.supervisor.log')).open('wb') as log:
            process = subprocess.Popen(command, cwd=binary.parent, env=env, stdout=log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            try:
                attempt['returncode'] = process.wait(timeout=240)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                attempt.update(returncode=process.returncode, supervisor_timeout=True)
        attempt['wall_seconds'] = round(time.monotonic() - started, 3)
        try:
            assert attempt['returncode'] == 0, 'harness failed; retain process diagnostics'
            attempt['summary'] = json.loads((directory / 'summary.json').read_text())
            settings = json.loads((directory / 'params-core.json').read_text())
            with (directory / 'config.txt').open('a') as config_file:
                config_file.write('params_core_sha256=' + sha(directory / 'params-core.json') + '\n')
            with (output / (name + '.supervisor.log')).open('ab') as log:
                subprocess.run([sys.executable, str(source / 'tools/depth-stream.py'), str(directory),
                                '--cap', str(plan['game_turn_cap'])], cwd=source, env=env,
                               stdout=log, stderr=subprocess.STDOUT, check=True)
                subprocess.run([sys.executable, str(source / 'tools/export-death.py'), str(directory),
                                '--impl', 'rust', '--build-id', str(build_id), '--flags', plan['flags']],
                               cwd=source, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
            preferences = [p for p in settings if p['name'].startswith(parameter_prefix)]
            assert len(preferences) == 54
            changed = [p for p in settings if p['value'] != p['default']]
            assert {p['name']: p['value'] for p in changed} == {
                key: value for key, value in expected_settings.items() if value != 1000}
            assert all(p['origin'] == 'borg.txt' for p in changed)
            assert attempt['summary']['race_idx'] == case['race_id']
            assert attempt['summary']['class_idx'] == case['class_id']
            assert attempt['summary']['stop_reason'] in ['death', 'turns']
            if not attempt['summary']['dead']:
                assert attempt['summary']['game_turns'] == plan['game_turn_cap']
            attempt['configuration_verified'] = True
            attempt['hashes'] = {n: sha(directory / n) for n in
                                 ['keys.log', 'messages.log', 'state.log', 'config.txt',
                                  'params-core.json', 'trace-core.jsonl']}
            attempt['trace'] = trace_stats(directory / 'trace-core.jsonl', case['class_id'])
            if arm == 'neutral':
                assert attempt['trace']['reranked_winners'] == 0
        except Exception as error:
            attempt['validation_error'] = repr(error)
        write(output / (name + '.attempt.json'), attempt)
        print(name, 'complete' if 'validation_error' not in attempt else attempt['validation_error'], flush=True)
        return attempt

    def run_pair(case):
        neutral = run_case(case, 'neutral')
        boosted = run_case(case, 'boosted')
        return dict(class_name=case['class'], profile=case['profile'], neutral=neutral, boosted=boosted)

    with Path('/tmp/angband-validation.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        assert source_hash() == build['source_sha256'] == plan['runtime_source_sha256']
        assert sha(binary) == build['binary_sha256'] == plan['binary_sha256']
        assert build['git_rev'] == plan['actual_build_commit'] and build['inputs_dirty'] == 'no'
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(run_pair, plan['classes']))
        assert source_hash() == plan['runtime_source_sha256']
        assert sha(binary) == plan['binary_sha256']
    write(output / 'results.json', dict(plan_sha256=sha(plan_path), results=results))
    errors = [a['name'] for p in results for a in [p['neutral'], p['boosted']] if 'validation_error' in a]
    if errors:
        raise SystemExit('Retained failed attempts: ' + ', '.join(errors))


if __name__ == '__main__':
    main()
