#!/usr/bin/env python3
"""Run a pinned Rust Borg, keeping seed receipts before any external work."""
import argparse
import hashlib
import gzip
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timezone
from death_pages import run_page

PROGRAMS = ('borg-rs', 'borg-reborn-rs')


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def command(argv, cwd=None, env=None, log=None, timeout=1200):
    """Bound the entire process group, including build/game grandchildren."""
    with log.open('w') if log else open(os.devnull, 'w') as output:
        child = subprocess.Popen(argv, cwd=cwd, env=env, stdout=output,
                                 stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            return 124


def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()


def kv(path):
    return dict(line.split('=', 1) for line in path.read_text().splitlines() if '=' in line)


def outcome(summary, process, rc, seed, race, cls):
    if rc == 124 or process.get('status') == 'timeout':
        return 'timeout'
    if process.get('status') in ('stall', 'stalled', 'stall_timeout'):
        return 'stalled'
    if rc or not summary:
        return 'harness_failure'
    # Older borg-rs summaries omit loaded. This launcher always supplies -n
    # with no load/save flags; a reported loaded=true is still rejected.
    if (summary.get('seed') != seed or summary.get('loaded', False) is not False
            or summary.get('race_idx') != race or summary.get('class_idx') != cls
            or summary.get('menu_letters') is not True):
        return 'identity_mismatch'
    options = summary.get('game_options', {})
    if any(value for key, value in options.items() if key.startswith('cheat_')):
        return 'config_error'
    if summary.get('effective_settings', {}).get('borg_cheat_death'):
        return 'config_error'
    if summary.get('dead') is True and summary.get('stop_reason') == 'death':
        return 'death'
    if summary.get('dead') is False and summary.get('stop_reason') == 'turns':
        return 'turn_cap'
    return 'stopped'


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def run_batch(a):
    root = a.out.resolve()
    # Never replace an earlier attempt, including one interrupted during setup.
    root.mkdir(parents=True, exist_ok=False)
    records = root / 'records'
    evidence = root / 'evidence'
    records.mkdir()
    evidence.mkdir()
    manifest = dict(schema='borg-cemetery/batch@1', program=a.program,
                    repository=f'diegoami/{a.program}', requested_ref=a.ref,
                    seeds=a.seeds, race_idx=a.race, class_idx=a.cls,
                    turns=a.turns, wall_seconds=a.wall_seconds, flags='menu',
                    checkpoint_every=a.checkpoint_every,
                    started_utc=datetime.now(timezone.utc).isoformat(),
                    runner=platform.platform(), status='preparing',
                    cemetery_commit=os.environ.get('GITHUB_SHA'),
                    workflow_run=os.environ.get('GITHUB_RUN_ID'),
                    workflow_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'))
    write_json(records / 'batch.json', manifest)
    for seed in a.seeds:
        write_json(records / f'seed-{seed}' / 'run.json',
                   dict(seed=seed, program=a.program, requested_ref=a.ref, status='not_started'))
    source = root / 'source'
    try:
        if a.profile:
            if a.program != 'borg-reborn-rs':
                raise ValueError('parameter profiles currently supported only for borg-reborn-rs')
            shutil.copy2(a.profile, records / 'profile.txt')
            manifest['profile_sha256'] = digest(records / 'profile.txt')
        command(['git', 'init', '-q', str(source)])
        rc = command(['git', '-C', str(source), 'fetch', '--depth', '1',
                      f'https://github.com/diegoami/{a.program}.git', a.ref],
                     log=evidence / 'fetch.log')
        if rc:
            raise RuntimeError(f'source fetch failed ({rc}); see fetch.log')
        git(source, 'checkout', '--detach', 'FETCH_HEAD')
        manifest['source_commit'] = git(source, 'rev-parse', 'HEAD')
        manifest['status'] = 'building'
        write_json(records / 'batch.json', manifest)
        env = dict(os.environ, BORG_IMPL='rust', BORG_X11='OFF',
                   BORG_DEATH_RECORDS_DIR=str(evidence / 'native-deaths'),
                   TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8',
                   RUN_TIMEOUT_SECONDS=str(a.wall_seconds))
        # Do not inherit local test features, profiles or binary overrides.
        for name in ('ANGBAND_BIN', 'BORG_TEST_FEATURES', 'BORG_PROFILE',
                     'BORGH_DATA_ROOT', 'SAVE_ROOT', 'CHECKPOINT_EVERY', 'STALL_TIMEOUT_SECONDS'):
            env.pop(name, None)
        if a.profile:
            env['BORG_PROFILE'] = str(records / 'profile.txt')
        env['CHECKPOINT_EVERY'] = str(a.checkpoint_every)
        rc = command(['bash', 'harness/build.sh'], cwd=source, env=env,
                     log=evidence / 'build.log')
        if rc:
            raise RuntimeError(f'build failed ({rc}); see build.log')
        build_id = source / 'build/rust/BUILD_ID'
        build = kv(build_id)
        binary = source / 'build/rust/game/angband'
        if (build.get('git_rev') != manifest['source_commit'] or
                build.get('impl') != 'rust' or build.get('inputs_dirty') != 'no' or
                build.get('binary_sha256') != digest(binary)):
            raise RuntimeError('BUILD_ID does not match the pinned source and binary')
        shutil.copy2(build_id, records / 'BUILD_ID')
        manifest['build'] = build
        manifest['status'] = 'running'
        write_json(records / 'batch.json', manifest)
        failed = False
        for seed in a.seeds:
            dest = records / f'seed-{seed}'
            raw = evidence / f'seed-{seed}'
            rec = dict(seed=seed, program=a.program, source_commit=manifest['source_commit'],
                       binary_sha256=build['binary_sha256'], race_idx=a.race,
                       class_idx=a.cls, turns=a.turns, flags='menu', status='running',
                       checkpoint_every=a.checkpoint_every)
            write_json(dest / 'run.json', rec)
            # These are observation-only interfaces already provided by the
            # pinned projects. Unsupported logs remain explicitly unavailable.
            env['BORG_OBSERVATION_LOG'] = str(raw / 'observations.jsonl')
            frontend = source / 'angband/src/main-borgh.c'
            extra = (['--', '-frames', str(raw / 'frames.jsonl')]
                     if frontend.is_file() and 'opt_frames' in frontend.read_text() else [])
            rc = command(['bash', 'harness/run.sh', str(raw), str(seed),
                          str(a.race), str(a.cls), str(a.turns), 'menu', *extra],
                         cwd=source, env=env, log=evidence / f'seed-{seed}-launcher.log',
                         timeout=a.wall_seconds + 30)
            summary = read_json(raw / 'summary.json')
            process = read_json(raw / 'process.json')
            rec.update(status=outcome(summary, process, rc, seed, a.race, a.cls),
                       exit_code=rc, summary=summary, process=process, hashes={})
            observations = raw / 'observations.jsonl'
            if observations.is_file():
                # Retain the full stream losslessly without accumulating all
                # uncompressed observation logs over a multi-seed batch.
                rec['observations_sha256'] = digest(observations)
                with observations.open('rb') as src, gzip.open(str(observations) + '.gz', 'wb') as dst:
                    shutil.copyfileobj(src, dst)
                observations.unlink()
            # Whitelist compact originals; raw logs and saves stay out of Git.
            for name in ('summary.json', 'process.json', 'config.txt', 'params.json'):
                if (raw / name).is_file():
                    shutil.copy2(raw / name, dest / name)
            for path in raw.rglob('*') if raw.exists() else []:
                if path.is_file():
                    rec['hashes'][str(path.relative_to(raw))] = digest(path)
            if rec['status'] == 'death':
                # Unassessed report from the original run, never a diagnostic rerun.
                (dest / 'death-report.md').write_text(
                    f"# {a.program}: seed {seed}\n\n"
                    f"Source: `{manifest['source_commit']}`\n\n"
                    f"Binary SHA-256: `{build['binary_sha256']}`\n\n"
                    f"Race/class indices: {a.race}/{a.cls}; birth menu letters; fresh birth.\n\n"
                    f"Cause (raw): {json.dumps(summary.get('death_cause'))}\n\n"
                    f"Game turn: {summary.get('game_turns')}; depth: {summary.get('depth')}; "
                    f"maximum depth: {summary.get('max_depth')}.\n\n"
                    "Assessment: unassessed. A death does not establish a defect.\n")
            write_json(dest / 'run.json', rec)
            failed |= rec['status'] not in ('death', 'turn_cap', 'stopped')
            run_page(dest)
        manifest['status'] = 'failed' if failed else 'complete'
        return int(failed)
    except Exception as exc:
        manifest.update(status='failed', error=str(exc))
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write_json(records / 'batch.json', manifest)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--program', required=True, choices=PROGRAMS)
    p.add_argument('--ref', required=True, help='commit, tag or branch; resolved once to a full SHA')
    p.add_argument('--seeds', required=True, help='comma or space separated uint32 seeds')
    p.add_argument('--race', type=int, default=0)
    p.add_argument('--class', type=int, dest='cls', default=0)
    p.add_argument('--turns', type=int, default=100000)
    p.add_argument('--wall-seconds', type=int, default=120)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--profile', type=Path, help='reborn-only parameter profile; original copied into records')
    p.add_argument('--checkpoint-every', type=int, default=100,
                   help='engine-turn save cadence; only selected scenario saves are archived (0 disables)')
    a = p.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/+-]{0,199}', a.ref):
        p.error('invalid ref')
    try:
        a.seeds = [int(s) for s in re.split(r'[\s,]+', a.seeds.strip())]
    except ValueError:
        p.error('seeds must be integers')
    if not 1 <= len(a.seeds) <= 20 or len(set(a.seeds)) != len(a.seeds):
        p.error('supply 1..20 distinct seeds')
    if any(not 0 <= s <= 4294967295 for s in a.seeds):
        p.error('seeds must be 0..4294967295')
    if not (0 <= a.race <= 10 and 0 <= a.cls <= 8 and
            1 <= a.turns <= 1000000000 and 1 <= a.wall_seconds <= 120):
        p.error('race 0..10, class 0..8, turns 1..1000000000, wall-seconds 1..120 required')
    if not 0 <= a.checkpoint_every <= 1000000000:
        p.error('checkpoint-every must be 0..1000000000')
    return a


if __name__ == '__main__':
    sys.exit(run_batch(parse_args()))
