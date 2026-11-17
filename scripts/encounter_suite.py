#!/usr/bin/env python3
"""Fast encounter smoke: load curated starts into an already-built Borg."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time

from run_scenario import run_scenario
from curate_encounters import coverage
from synthetic_suite import COMMIT, STATE, integer, local_file, read, sha, write

ROOT = Path(__file__).resolve().parents[1]
VALID = {'death', 'survived_horizon', 'stopped'}


def prepare(path, root=ROOT):
    manifest = read(path)
    if manifest.get('schema') != 'borg-cemetery/saved-encounter-suite@1' or manifest.get('core') != 'reborn':
        raise ValueError('unsupported encounter suite')
    for key in ('baseline_source_commit', 'engine_commit'):
        if not COMMIT.fullmatch(manifest.get(key, '')):
            raise ValueError('exact commit required: ' + key)
    integer(manifest['horizon_engine_turns'], 10, 2000)
    integer(manifest['wall_seconds'], 1, 10)
    entries = manifest['scenarios']
    if not isinstance(entries, list) or not 1 <= len(entries) <= 8:
        raise ValueError('fast suite requires 1..8 cases')
    result, seen = [], set()
    for entry in entries:
        name = entry['id']
        if not isinstance(name, str) or not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in name) or name in seen:
            raise ValueError('invalid or duplicate scenario ID')
        seen.add(name)
        scenario_file = local_file(root, entry['scenario'], entry['sha256'])
        scenario = read(scenario_file)
        if (scenario.get('id') != name or scenario.get('schema') != 'borg-cemetery/save-scenario@1' or
                scenario.get('status') != 'ready_for_restart_trials' or
                scenario.get('startup_contract') != 'fresh_borg_saved_engine_rng' or
                scenario.get('borg_memory_restored') is not False or
                scenario.get('independent_life') is not False):
            raise ValueError('scenario lacks qualified fresh-Borg startup identity')
        local_file(scenario_file.parent, scenario['save'], scenario['compressed_sha256'])
        profile = local_file(scenario_file.parent, scenario['baseline_profile'], scenario['baseline_profile_sha256'])
        selection = scenario['selection']
        integer(scenario['start_turn'], 0, 1000000000)
        if not scenario['start_turn'] <= selection['trigger_turn'] < scenario['original_endpoint_turn']:
            raise ValueError('scenario must begin at/before encounter onset, before original death')
        result.append((name, scenario_file.parent, profile))
    return manifest, result


def run_suite(path, source, output, target_commit=None, adapter=run_scenario, root=ROOT):
    manifest, cases = prepare(path, root)
    if output.exists():
        raise ValueError('use a fresh output directory; never overwrite attempts')
    expected = target_commit or manifest['baseline_source_commit']
    if not COMMIT.fullmatch(expected):
        raise ValueError('target must be an exact commit')
    actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != expected:
        raise ValueError('target source commit differs')
    upstream = dict(line.split('=', 1) for line in (source / 'engine/UPSTREAM').read_text().splitlines() if '=' in line)
    if upstream.get('commit') != manifest['engine_commit']:
        raise ValueError('saved encounter engine pin is incompatible')
    output.mkdir(parents=True)
    start = time.monotonic()
    document = dict(schema='borg-cemetery/encounter-suite-results@1', suite_id=manifest['suite_id'],
                    manifest_sha256=sha(path), source_commit=actual, core='reborn',
                    expected_count=len(cases), results=[], borg_memory_restored=False)
    environment = {'BORG_CORE': 'reborn', 'BORG_CORE_OVERRIDES': None,
                   'ANGBAND_RECORD_DIR': None, 'ANGBAND_REPLAY_DIR': None,
                   'BORG_RECORD_DIR': None, 'BORG_REPLAY_DIR': None}
    for key in os.environ:
        if (key.startswith('BORG_') and key != 'BORG_CEMETERY_DIR') or key.startswith('ANGBAND_'):
            environment.setdefault(key, None)
    previous = {key: os.environ.get(key) for key in environment}
    try:
        for key, value in environment.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        with open('/tmp/angband-validation.lock', 'a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            for name, scenario, profile in cases:
                case_start = time.monotonic()
                dest = output / name
                try:
                    rc = adapter(source, scenario, dest, turns=manifest['horizon_engine_turns'],
                                 wall_seconds=manifest['wall_seconds'], profile=profile)
                    trial = read(dest / 'trial.json')
                    status = trial['status']
                    if rc and status in VALID:
                        status = 'harness_failure'
                    row = dict(id=name, status=status, trial_sha256=sha(dest / 'trial.json'),
                               summary=trial.get('summary'), source_build=trial.get('build'))
                    row['streams'] = {f: sha(dest / 'run' / f) for f in
                                      ('keys.log', 'state.log', 'messages.log') if (dest / 'run' / f).exists()}
                    if status in VALID:
                        if len(row['streams']) != 3:
                            raise ValueError('missing gameplay stream')
                        first = (dest / 'run/state.log').read_text().splitlines()[0]
                        state = STATE.match(first)
                        expected_start = read(scenario / 'scenario.json')['initial_observed']
                        values = [expected_start[k] for k in ('hp', 'max_hp', 'sp', 'max_sp')]
                        if not state or list(map(int, state.groups()[3:])) != values:
                            raise ValueError('loaded resource state differs from scenario')
                        expected_coverage = read(scenario / 'scenario.json').get('coverage')
                        if expected_coverage:
                            with (dest / 'run/observations.jsonl').open() as stream:
                                actual_coverage = coverage(json.loads(next(stream)))
                            row['loaded_coverage'] = actual_coverage
                            for field in ('level', 'depth', 'equipment_kind_signature', 'inventory'):
                                if actual_coverage[field] != expected_coverage[field]:
                                    raise ValueError('loaded coverage differs: ' + field)
                except Exception as error:
                    row = dict(id=name, status='harness_failure', reason=str(error))
                row['elapsed_seconds'] = time.monotonic() - case_start
                document['results'].append(row)
                write(output / 'results.json', document)
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    document['elapsed_seconds'] = time.monotonic() - start
    document['invalid_count'] = sum(r['status'] not in VALID for r in document['results'])
    write(output / 'results.json', document)
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--target-commit')
    args = parser.parse_args()
    result = run_suite(args.manifest, args.source, args.out, args.target_commit)
    print(f"{len(result['results'])}/{result['expected_count']} cases, {result['invalid_count']} invalid, {result['elapsed_seconds']:.2f}s")
    return int(bool(result['invalid_count']))


if __name__ == '__main__':
    raise SystemExit(main())
