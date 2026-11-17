#!/usr/bin/env python3
"""Prepare a bounded natural caster harvest; this is outside fast suite timing."""
import argparse
import fcntl
import gzip
import os
from pathlib import Path
import shutil
import subprocess
import time

from run_batch import kv
from synthetic_suite import COMMIT, integer, read, sha, write


def validate(spec):
    if spec.get('schema') != 'borg-cemetery/encounter-harvest-spec@1' or spec.get('core') != 'reborn':
        raise ValueError('unsupported harvest')
    if not COMMIT.fullmatch(spec.get('source_commit', '')):
        raise ValueError('exact source required')
    integer(spec['turn_cap'], 100, 30000)
    integer(spec['checkpoint_every'], 10, 1000)
    integer(spec['wall_seconds'], 1, 60)
    if not 1 <= len(spec['cells']) <= 16:
        raise ValueError('harvest requires 1..16 prespecified attempts')
    seen = set()
    for c in spec['cells']:
        name = c['id']
        if not name or any(x not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for x in name) or name in seen:
            raise ValueError('invalid/duplicate cell ID')
        seen.add(name)
        integer(c['seed'], 1, 2147483647)
        integer(c['race'], 0, 10)
        integer(c['cls'], 1, 4)


def archive(path):
    """Lossless compression; receipts record the uncompressed and stored hashes."""
    receipt = dict(file=path.name, sha256=sha(path), bytes=path.stat().st_size)
    packed = path.with_name(path.name + '.gz')
    with path.open('rb') as src, packed.open('xb') as dest:
        with gzip.GzipFile(fileobj=dest, mode='wb', filename='', mtime=0, compresslevel=6) as out:
            shutil.copyfileobj(src, out)
    receipt.update(archive=packed.name, archive_sha256=sha(packed))
    path.unlink()
    return receipt


def harvest(spec_path, source, out):
    spec = read(spec_path)
    validate(spec)
    if out.exists():
        raise ValueError('use a fresh harvest directory')
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    build = kv(source / 'build/rust/BUILD_ID')
    binary = source / 'build/rust/game/angband'
    current = subprocess.check_output(['bash', str(source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
    if (head != spec['source_commit'] or build.get('git_rev') != head or build.get('inputs_dirty') != 'no'
            or build.get('git_dirty') != 'no' or build.get('impl') != 'rust'
            or build.get('source_sha256') != current or build.get('binary_sha256') != sha(binary)):
        raise ValueError('harvest source/build identity differs')
    out.mkdir(parents=True)
    write(out / 'spec.json', spec)
    document = dict(schema='borg-cemetery/encounter-harvest@1', spec_sha256=sha(spec_path),
                    build=build, expected_attempts=len(spec['cells']), attempts=[])
    start = time.monotonic()
    with open('/tmp/angband-validation.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for cell in spec['cells']:
            run = out / cell['id']
            env = {k: v for k, v in os.environ.items() if not k.startswith(('BORG_', 'ANGBAND_'))
                   and k not in ('BORGH_DATA_ROOT', 'SAVE_ROOT', 'STALL_TIMEOUT_SECONDS')}
            if 'BORG_CEMETERY_DIR' in os.environ:
                env['BORG_CEMETERY_DIR'] = os.environ['BORG_CEMETERY_DIR']
            env.update(BORG_IMPL='rust', BORG_CORE='reborn', TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8',
                       BORG_PROFILE=str(source / 'harness/profiles/reborn-default.txt'),
                       BORG_DEATH_RECORDS_DIR=str(out / 'deaths'), RUN_TIMEOUT_SECONDS=str(spec['wall_seconds']),
                       CHECKPOINT_EVERY=str(spec['checkpoint_every']),
                       BORG_OBSERVATION_LOG=str(run / 'observations.jsonl'), BORG_KNOWLEDGE_LOG=str(run / 'knowledge.json'))
            row = dict(**cell, status='harness_failure')
            try:
                result = subprocess.run(['bash', str(source / 'harness/run.sh'), str(run), str(cell['seed']),
                    str(cell['race']), str(cell['cls']), str(spec['turn_cap']), 'menu'], env=env,
                    capture_output=True, text=True, timeout=spec['wall_seconds'] + 30)
                (out / (cell['id'] + '.launcher.log')).write_text(result.stdout + result.stderr)
                summary = read(run / 'summary.json') if (run / 'summary.json').exists() else {}
                row.update(returncode=result.returncode, summary=summary)
                process = read(run / 'process.json') if (run / 'process.json').exists() else {}
                identity_matches = (summary.get('loaded') is False and summary.get('seed') == cell['seed']
                    and summary.get('race_idx') == cell['race'] and summary.get('class_idx') == cell['cls']
                    and process.get('executable_sha256_before') == build['binary_sha256']
                    and process.get('executable_sha256_after') == build['binary_sha256'])
                if result.returncode == 0 and identity_matches:
                    row['status'] = 'death' if summary.get('dead') else 'survived_cap' if summary.get('stop_reason') == 'turns' else 'stopped'
                if summary.get('dead'):
                    packages = [read(p) for p in (out / 'deaths').glob('*/summary.json')]
                    if not any(p.get('seed') == cell['seed'] and p.get('race_idx') == cell['race']
                               and p.get('class_idx') == cell['cls'] and p.get('game_turns') == summary.get('game_turns')
                               and p.get('dead') is True for p in packages):
                        raise ValueError('death exporter produced no matching retained package')
            except Exception as error:
                row.update(status='harness_failure', reason=str(error))
            finally:
                retained = []
                for name in ('observations.jsonl', 'trace.jsonl', 'keys.log', 'state.log', 'messages.log'):
                    if (run / name).exists():
                        retained.append(archive(run / name))
                # Keep every intermediate checkpoint, compressed separately.
                if (run / 'checkpoints').exists():
                    for checkpoint in sorted((run / 'checkpoints').glob('*.save')):
                        archive(checkpoint)
                row['retention'] = retained
                document['attempts'].append(row)
                write(out / 'harvest.json', document)
                print(cell['id'], row['status'], flush=True)
    document['elapsed_seconds'] = time.monotonic() - start
    write(out / 'harvest.json', document)
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = harvest(args.spec.resolve(), args.source.resolve(), args.out.resolve())
    raise SystemExit(int(any(r['status'] == 'harness_failure' for r in result['attempts'])))
