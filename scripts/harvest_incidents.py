#!/usr/bin/env python3
"""Bounded natural incident harvest, balanced by class; all attempts survive selection."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import gzip
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time

from mine_incidents import candidates
from synthetic_suite import read, sha, write
from run_batch import kv


def compress(path):
    dest = path.with_name(path.name + '.gz')
    with path.open('rb') as a, dest.open('xb') as b, gzip.GzipFile(fileobj=b, mode='wb', filename='', mtime=0) as z:
        shutil.copyfileobj(a, z)
    info = dict(path=path.name, sha256=sha(path), archive=dest.name, archive_sha256=sha(dest))
    path.unlink()
    return info


def archive_checkpoints(directory):
    dest = directory.with_name('checkpoints.tar.gz')
    inventory = []
    with dest.open('xb') as out, gzip.GzipFile(fileobj=out, mode='wb', filename='', mtime=0) as z, tarfile.open(fileobj=z, mode='w|') as archive:
        for path in sorted(directory.iterdir()):
            if not path.is_file():
                continue
            info = archive.gettarinfo(str(path), arcname=path.name)
            info.mtime = info.uid = info.gid = 0
            info.uname = info.gname = ''
            with path.open('rb') as stream:
                archive.addfile(info, stream)
            inventory.append(dict(name=path.name, sha256=sha(path)))
    write(directory.with_name('checkpoint-archive.json'), dict(path=dest.name, sha256=sha(dest), files=inventory))
    shutil.rmtree(directory)


def execute(source, out, seed, race, cls, spec, save=None, turns=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith(('BORG_', 'ANGBAND_', 'BORGH_'))
           and k not in ('SAVE_ROOT', 'STALL_TIMEOUT_SECONDS', 'CHECKPOINT_EVERY')}
    env.update(BORG_CORE=spec.get('core', 'reborn'), BORG_CEMETERY_DIR=spec['tools_directory'],
               BORG_ENCOUNTER_LOG=str(out / 'encounters.jsonl'), BORG_KNOWLEDGE_LOG=str(out / 'knowledge.json'),
               BORG_DEATH_RECORDS_DIR=str(out / 'native-deaths'), RUN_TIMEOUT_SECONDS=str(spec['wall_seconds']),
               CHECKPOINT_EVERY='0' if save else str(spec['checkpoint_every']))
    if save:
        env.pop('BORG_KNOWLEDGE_LOG', None)
    flags = 'menu'
    if save:
        env['SAVE_ROOT'] = str(save.parent)
        flags += ',keep-load-rng,save=' + save.name
    result = subprocess.run(['bash', str(source / 'harness/run.sh'), str(out), str(seed), str(race), str(cls),
                             str(turns or spec['turn_cap']), flags], env=env, capture_output=True, text=True,
                            timeout=spec['wall_seconds'] + 45)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'launcher.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise ValueError('native harness failed: ' + str(result.returncode))
    summary = read(out / 'summary.json')
    if summary.get('seed') != seed or summary.get('race_idx') != race or summary.get('class_idx') != cls:
        raise ValueError('native birth identity differs')
    return summary


def one(source, root, cls, ordinal, spec):
    seed = spec['seed_base'] + cls * 10000 + ordinal
    race = spec['races'][ordinal % len(spec['races'])]
    name = f'c{cls}-r{race}-s{seed}'
    run = root / 'attempts' / name
    row = dict(id=name, ordinal=ordinal, seed=seed, race=race, cls=cls, status='harness_failure', cases=[])
    tick = time.monotonic()
    try:
        summary = execute(source, run, seed, race, cls, spec)
        row.update(summary=summary, status='death' if summary['dead'] else 'survived_cap' if summary['stop_reason'] == 'turns' else 'stopped')
        if summary['dead'] and not list((run / 'native-deaths').glob('*/record.json')):
            raise ValueError('natural death package absent')
        incidents = candidates(run, summary)
        seen = set()
        for number, incident in enumerate(incidents):
            if incident['status'] != 'candidate':
                continue
            try:
                checkpoint = incident['checkpoint']
                saved = run / 'checkpoints' / checkpoint['file']
                digest = sha(saved)
                if digest in seen:
                    incident.update(status='duplicate_saved_start')
                    continue
                seen.add(digest)
                case_id = name + f'-i{number:03d}'
                dest = root / 'cases' / case_id
                dest.mkdir(parents=True)
                with saved.open('rb') as a, (dest / 'start.save.gz').open('xb') as b, gzip.GzipFile(fileobj=b, mode='wb', filename='', mtime=0) as z:
                    shutil.copyfileobj(a, z)
                # A short native load obtains exact initial gear/status; no guessed
                # relation between queued-key and think logs is used.
                probe = dest / 'probe'
                probe_summary = execute(source, probe, seed, race, cls, spec, save=saved, turns=checkpoint['game_turn'] + 1)
                with (probe / 'encounters.jsonl').open() as stream:
                    initial = json.loads(next(stream))
                if initial['turn'] != checkpoint['game_turn'] or not probe_summary.get('loaded'):
                    raise ValueError('native initial inspection differs from saved start')
                write(dest / 'initial-observation.json', initial)
                shutil.copyfile(source / 'harness/profiles/reborn-default.txt', dest / 'profile.txt')
                write(dest / 'incident.json', incident)
                row['cases'].append(dict(id=case_id, directory=case_id, save_sha256=digest, incident_type=incident['type'],
                                         incident_turn=incident['turn'], initial_turn=initial['turn'],
                                         initial_state=(probe / 'state.log').read_text().splitlines()[0]))
            except Exception as error:
                incident.update(status='unusable_initial_state', reason=str(error))
        write(run / 'selection.json', dict(incidents=incidents))
        for info in row['cases']:
            probe = root / 'cases' / info['directory'] / 'probe'
            for filename in ('encounters.jsonl', 'trace.jsonl', 'keys.log', 'messages.log', 'state.log'):
                if (probe / filename).exists():
                    compress(probe / filename)
    except Exception as error:
        row.update(status='harness_failure', reason=str(error))
    finally:
        if run.exists():
            retention = []
            for filename in ('encounters.jsonl', 'trace.jsonl', 'keys.log', 'messages.log', 'state.log'):
                if (run / filename).exists():
                    retention.append(compress(run / filename))
            if (run / 'checkpoints').exists():
                archive_checkpoints(run / 'checkpoints')
            row['retention'] = retention
        row['elapsed_seconds'] = time.monotonic() - tick
        write(root / 'completed' / (name + '.json'), row)
    return row


def run(spec_path, source, root, cls, tools, smoke=False):
    spec = read(spec_path)
    original_spec_sha256 = sha(spec_path)
    excluded = set()
    if 'exclusion' in spec:
        exclusion = spec_path.parent / spec['exclusion']['path']
        if sha(exclusion) != spec['exclusion']['sha256']:
            raise ValueError('exclusion inventory changed')
        inventory = read(exclusion)
        excluded = set(inventory['save_sha256'])
        seeds = {spec['seed_base'] + c * 10000 + i for c in range(9) for i in range(spec['max_attempts_per_class'])}
        if seeds.intersection(inventory['source_seeds']):
            raise ValueError('source seeds overlap earlier suite')
    if 'configuration' in spec:
        if (sha(source / 'harness/borg.txt') != spec['configuration']['borg_txt_sha256'] or
                sha(source / 'harness/profiles/reborn-default.txt') != spec['configuration']['profile_sha256']):
            raise ValueError('preparation configuration changed')
    goal = spec['smoke']['target_per_class'] if smoke else spec['target_per_class']
    if smoke:
        spec.update(seed_base=spec['smoke_seed_base'], max_attempts_per_class=spec['smoke']['max_attempts_per_class'])
    tools_head = subprocess.check_output(['git', '-C', str(tools), 'rev-parse', 'HEAD'], text=True).strip()
    if tools_head != spec['native_tools_commit']:
        raise ValueError('native tools differ from pin')
    spec['tools_directory'] = str(tools)
    if root.exists() or cls not in range(9) or spec['target_per_class'] != 111:
        raise ValueError('fresh directory and declared balanced999 quota required')
    build = kv(source / 'build/rust/BUILD_ID')
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    inputs = subprocess.check_output(['bash', str(source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
    if head != spec['source_commit'] or build['git_rev'] != head or inputs != build['source_sha256'] or sha(source / 'build/rust/game/angband') != build['binary_sha256']:
        raise ValueError('source/build mismatch')
    root.mkdir(parents=True)
    write(root / 'spec.json', spec)
    write(root / 'build.json', build)
    document = dict(schema='borg-cemetery/balanced-incident-harvest@1', spec_sha256=original_spec_sha256,
                    class_idx=cls, target=goal, stage='smoke' if smoke else 'harvest', attempts=[], selected=[], rejected=[], independent_life=False)
    seen, selected = set(excluded), []
    with open('/tmp/angband-validation.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        with ThreadPoolExecutor(max_workers=spec['workers']) as pool:
            for offset in range(0, spec['max_attempts_per_class'], spec['workers']):
                # Selection uses prespecified seed order, never completion speed.
                futures = [pool.submit(one, source, root, cls, ordinal, spec) for ordinal in range(offset, min(offset + spec['workers'], spec['max_attempts_per_class']))]
                batch = [future.result() for future in futures]
                for row in batch:
                    document['attempts'].append(row)
                    for case in row['cases']:
                        if case['save_sha256'] in seen:
                            document['rejected'].append(dict(case, reason='duplicate_suite1' if case['save_sha256'] in excluded else 'duplicate_in_suite'))
                            continue
                        seen.add(case['save_sha256'])
                        if len(selected) < goal:
                            selected.append(dict(**case, source_attempt=row['id']))
                document['selected'] = selected
                # Completed attempt journals are immutable; the replaceable
                # progress pointer is bounded instead of quadratic snapshots.
                progress = root / 'harvest-progress.json.tmp'
                progress.write_text(json.dumps(document, indent=2, sort_keys=True) + '\n')
                os.replace(progress, root / 'harvest-progress.json')
                print('class', cls, 'attempts', len(document['attempts']), 'usable', len(selected), '/' + str(goal), flush=True)
                if len(selected) == goal:
                    break
    write(root / 'harvest.json', document)
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--class-index', type=int, required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    result = run(args.spec.resolve(), args.source.resolve(), args.out.resolve(), args.class_index, args.tools.resolve(), args.smoke)
    raise SystemExit(int(len(result['selected']) != result['target']))
