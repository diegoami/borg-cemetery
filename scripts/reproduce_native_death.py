#!/usr/bin/env python3
"""Reproduce a natural death from pinned birth inputs, without a recording."""
import argparse
import fcntl
import os
from pathlib import Path
import subprocess

from synthetic_suite import COMMIT, HEX, integer, kv, local_file, read, sha, write

ROOT = Path(__file__).resolve().parents[1]


def inputs(recipe, root):
    if recipe.get('schema') != 'borg-cemetery/native-death-recipe@1' or recipe.get('start') != 'birth':
        raise ValueError('only explicit native birth recipes are supported')
    if recipe.get('repository') != 'diegoami/borg-reborn-rs':
        raise ValueError('unsupported source repository')
    if not COMMIT.fullmatch(recipe.get('source_commit', '')):
        raise ValueError('exact source commit required')
    for key in ('source_sha256', 'binary_sha256'):
        if not HEX.fullmatch(recipe.get(key, '')):
            raise ValueError('missing build digest: ' + key)
    for key, low, high in [('seed', 0, 2**32 - 1), ('race_idx', 0, 10),
                           ('class_idx', 0, 8), ('turn_cap', 1, 10000000)]:
        integer(recipe[key], low, high)
    if recipe.get('flags') != 'menu':
        raise ValueError('this adapter qualifies menu birth only; no ignored flags')
    environment = recipe.get('environment', {})
    if set(environment) - {'BORG_CORE', 'BORG_CORE_OVERRIDES'}:
        raise ValueError('unsupported configuration override')
    if environment.get('BORG_CORE', 'reborn') not in ('reborn', 'borg-rs'):
        raise ValueError('unsupported core')
    if environment.get('BORG_CORE_OVERRIDES', 'on') not in ('on', 'off'):
        raise ValueError('unsupported core override mode')
    result = {}
    for key in ('record', 'borg_txt', 'profile', 'runtime'):
        ref = recipe[key]
        result[key] = local_file(root, ref['path'], ref['sha256'])
    original = read(result['record'])
    identity, terminal = original['identity'], original['terminal']
    if (original.get('schema') != 'borg-reborn-rs/death-record@1' or terminal.get('dead') is not True or
            original.get('run_kind') == 'synthetic' or
            identity.get('git_rev') != recipe['source_commit'] or
            identity.get('source_sha256') != recipe['source_sha256'] or
            identity.get('binary_sha256') != recipe['binary_sha256'] or
            identity.get('seed') != recipe['seed'] or terminal.get('race_idx') != recipe['race_idx'] or
            terminal.get('class_idx') != recipe['class_idx']):
        raise ValueError('recipe differs from original natural death identity')
    summary_path = local_file(result['record'].parent, 'summary.json', original['files_sha256']['summary.json'])
    summary = read(summary_path)
    if summary.get('loaded') is not False or summary.get('synthetic'):
        raise ValueError('original was not an ordinary birth run')
    if sha(result['borg_txt']) != identity['borg_txt_sha256'] or sha(result['profile']) != identity['profile_sha256']:
        raise ValueError('recipe configuration differs from original death')
    result['runtime_manifest'] = read(result['runtime'])
    if result['runtime_manifest']['binary_sha256'] != recipe['binary_sha256']:
        raise ValueError('runtime manifest differs from original binary')
    result['original'] = original
    return result


def verify_run(recipe, original, output):
    summary = read(output / 'summary.json')
    terminal = original['terminal']
    expected = dict(seed=recipe['seed'], race_idx=recipe['race_idx'], class_idx=recipe['class_idx'],
                    loaded=False, dead=True, stop_reason='death', game_turns=terminal['turn'],
                    death_cause=terminal['cause'], clevel=terminal['level'], depth=terminal['depth'])
    if any(type(summary.get(k)) is not type(v) or summary.get(k) != v for k, v in expected.items()):
        raise ValueError('rerun death endpoint differs')
    if summary.get('synthetic'):
        raise ValueError('synthetic result cannot reproduce a natural death')
    config = kv(output / 'config.txt')
    for key in ('borg_txt_sha256', 'profile_sha256', 'params_core_sha256'):
        if config.get(key) != original['identity'].get(key):
            raise ValueError('effective configuration differs: ' + key)
    hashes = original['attempts'][0]['raw_sha256']
    for name in ('keys.log', 'state.log', 'messages.log'):
        if sha(output / name) != hashes[name]:
            raise ValueError('rerun stream differs: ' + name)
    return {name: hashes[name] for name in ('keys.log', 'state.log', 'messages.log')}


def reproduce(recipe_path, source, output, binary=None, allow_rebuilt=False):
    recipe = read(recipe_path)
    data = inputs(recipe, ROOT)
    source, output = source.resolve(), output.resolve()
    if output.exists():
        raise ValueError('output already exists; preserve every attempt in a fresh directory')
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != recipe['source_commit']:
        raise ValueError('source checkout is not the pinned commit')
    if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip():
        raise ValueError('source checkout is dirty')
    digest = subprocess.check_output([str(source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
    if digest != recipe['source_sha256']:
        raise ValueError('source inputs differ')
    binary = (binary or source / 'build/rust/game/angband').resolve()
    binary_hash = sha(binary)
    if binary_hash != recipe['binary_sha256'] and not allow_rebuilt:
        raise ValueError('binary differs; use original binary or explicitly qualify --allow-rebuilt-binary')
    build = kv(binary.parent.parent / 'BUILD_ID')
    if (build.get('git_rev') != revision or build.get('source_sha256') != digest or
            build.get('binary_sha256') != binary_hash or build.get('git_dirty') != 'no' or
            build.get('inputs_dirty') != 'no'):
        raise ValueError('build receipt is not exact and clean')
    data_root = binary.parent / 'lib'
    actual_data = {'lib/' + p.relative_to(data_root).as_posix(): sha(p)
                   for p in data_root.rglob('*') if p.is_file()}
    if actual_data != data['runtime_manifest']['game_data_files']:
        raise ValueError('game data differs from original runtime')
    env = {key: os.environ[key] for key in ('PATH', 'PYTHONPATH', 'LD_LIBRARY_PATH', 'BORG_CEMETERY_DIR')
           if key in os.environ}
    env.update(recipe['environment'], ANGBAND_BIN=str(binary), BORG_PROFILE=str(data['profile']),
               BORG_DEATH_RECORDS_DIR=str(output / 'death-registry'), RUN_TIMEOUT_SECONDS='120')
    command = ['bash', str(source / 'harness/run.sh'), str(output), str(recipe['seed']),
               str(recipe['race_idx']), str(recipe['class_idx']), str(recipe['turn_cap']), recipe['flags']]
    receipt = dict(schema='borg-cemetery/native-death-reproduction@1', recipe_sha256=sha(recipe_path),
                   source_commit=revision, source_sha256=digest, binary_sha256=binary_hash,
                   original_binary_match=binary_hash == recipe['binary_sha256'], command=command,
                   status='failed', independent_life=False)
    # Lock is held only by this runner; harness/run.sh does not acquire it.
    try:
        with open('/tmp/angband-validation.lock', 'a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if output.exists():
                raise ValueError('output appeared while waiting for lock')
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=150)
    except (OSError, subprocess.TimeoutExpired) as error:
        receipt['reason'] = str(error)
        write(output / 'reproduction.json', receipt)
        return receipt
    receipt['returncode'] = result.returncode
    try:
        if result.returncode:
            raise ValueError('native harness failed')
        process = read(output / 'process.json')
        if (process.get('executable_sha256_before') != binary_hash or
                process.get('executable_sha256_after') != binary_hash):
            raise ValueError('actual executable differs from requested binary')
        receipt['streams'] = verify_run(recipe, data['original'], output)
        receipt['status'] = 'reproduced'
    except (OSError, ValueError, KeyError) as error:
        receipt['reason'] = str(error)
    write(output / 'reproduction.json', receipt)
    (output / 'reproduction-launcher.log').write_text(result.stdout + result.stderr)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', required=True, type=Path)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--binary', type=Path)
    parser.add_argument('--allow-rebuilt-binary', action='store_true')
    args = parser.parse_args()
    receipt = reproduce(args.recipe, args.source, args.out, args.binary, args.allow_rebuilt_binary)
    print(receipt['status'])
    return int(receipt['status'] != 'reproduced')


if __name__ == '__main__':
    raise SystemExit(main())
