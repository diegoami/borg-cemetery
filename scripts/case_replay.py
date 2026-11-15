#!/usr/bin/env python3
"""Build, watch and record human alternatives using case-local launchers."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
# Optional recording integration, separate from the original recorder-off build.
RECORDER_SOURCE = '2e648118eedc31904dcaed056db52e14acda2a07'
QUALIFIED_ORIGINS = {'e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71', RECORDER_SOURCE}
RELEASE = 'https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15'
ARCHIVES = {'D0005': 'b103d0c0fea96135eccf348d93198264cc6074b670bc8b77da8d4c860a9a0ad5',
            'D0006': '99891c034f1271bcbd122a16c532f63482447ce67d893ee5e177d434c4b4703f'}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def default_cache(root=ROOT):
    explicit = os.environ.get('BORG_CEMETERY_CACHE')
    if explicit:
        return Path(explicit).expanduser()
    local = root / '.cache/borg-cemetery'
    legacy = Path(os.environ.get('XDG_CACHE_HOME') or str(Path.home() / '.cache')) / 'borg-cemetery'
    if not local.exists() and not local.is_symlink() and legacy.is_dir():
        # Preserve existing runtimes and absolute recording bindings. The
        # checkout-local entry points at the old cache rather than rebuilding.
        local.parent.mkdir(parents=True, exist_ok=True)
        try:
            local.symlink_to(legacy.resolve(), target_is_directory=True)
        except FileExistsError:
            pass
    return local


def cached_executable(receipt, key='binary'):
    if not receipt.exists():
        return None
    result = read(receipt)
    binary = Path(result[key])
    if not binary.is_file() or sha(binary) != result[key + '_sha256']:
        raise ValueError(f'Cached executable changed: {binary}. Preserve that cache and use a fresh --cache.')
    return result


def run(args, **kwargs):
    argv = [str(a) for a in args]
    timeout = kwargs.pop('timeout', None)
    if timeout is None:
        subprocess.run(argv, check=True, **kwargs)
        return
    child = subprocess.Popen(argv, start_new_session=True, **kwargs)
    try:
        code = child.wait(timeout=timeout)
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        raise
    if code:
        raise subprocess.CalledProcessError(code, argv)


@contextmanager
def native_lock():
    with open('/tmp/angband-validation.lock', 'a') as held:
        try:
            fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Another native build/run is active. Retry when it finishes.')
        yield


def plan(case):
    if (case / 'scenario.json').exists():
        return dict(kind='scenario', case=case.name, scenario=case)
    path = case / 'record.json'
    if not path.exists():
        path = case / 'run.json'
    record = read(path)
    case_id = record.get('id', case.name)
    if case_id in ARCHIVES:
        return dict(kind='legacy', case=case_id)
    for name in record.get('scenarios', []):
        candidate = ROOT / 'scenarios' / name
        if read(candidate / 'scenario.json').get('event_kind') == 'death':
            return dict(kind='scenario', case=case_id, scenario=candidate)
    for candidate in sorted(case.glob('analysis/event-*/scenario.json')):
        if read(candidate).get('event_kind') == 'death':
            return dict(kind='scenario', case=case_id, scenario=candidate.parent)
    identity = record.get('identity', record)
    return dict(kind='seed', case=case_id, source=identity.get('source', identity.get('git_rev', identity.get('source_commit'))),
                program=record.get('program', 'borg-rs'))


def checkout(cache, program, commit):
    if program not in ('borg-rs', 'borg-reborn-rs') or not re.fullmatch(r'[0-9a-f]{40}', str(commit)):
        raise ValueError('The case must identify an allowed Borg project and a full immutable source commit.')
    dest = cache / 'sources' / program / commit
    initialized = (dest / '.git').exists()
    has_head = initialized and subprocess.run(['git', '-C', str(dest), 'rev-parse', '--verify', 'HEAD'],
                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    if not has_head:
        if initialized and any(p.name != '.git' for p in dest.iterdir()):
            raise ValueError('Incomplete source cache contains other files; preserve it and choose a new cache.')
        dest.mkdir(parents=True, exist_ok=True)
        if not initialized:
            run(['git', 'init', '-q', dest])
        run(['git', '-C', dest, 'fetch', '--depth', '1', f'https://github.com/diegoami/{program}.git', commit])
        run(['git', '-C', dest, 'checkout', '--detach', 'FETCH_HEAD'])
    head = subprocess.check_output(['git', '-C', str(dest), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(dest), 'status', '--porcelain'], text=True).strip()
    if head != commit or dirty:
        raise ValueError(f'Pinned source cache changed; preserve it and choose another --cache: {dest}')
    return dest


def cached_recorder(cache):
    folder = cache / 'recorder-runtime' / RECORDER_SOURCE
    receipt = folder / 'runtime.json'
    if receipt.exists():
        result = read(receipt)
        if result.get('source_commit') == RECORDER_SOURCE and all(Path(result[k]).is_file() and sha(Path(result[k])) == result[k + '_sha256']
               for k in ('binary', 'recorder')):
            print(f'Using cached recorder-enabled Borg version {RECORDER_SOURCE[:12]}.', flush=True)
            return result
        raise ValueError('Cached recorder executable changed; preserve the cache and choose a fresh --cache.')
    return None


def recorder_build(cache, jobs):
    existing = cached_recorder(cache)
    if existing is not None:
        return existing
    folder = cache / 'recorder-runtime' / RECORDER_SOURCE
    receipt = folder / 'runtime.json'
    source = checkout(cache, 'borg-reborn-rs', RECORDER_SOURCE)
    build = folder / 'engine'
    game_receipt = folder / 'game-ready.json'
    game = cached_executable(game_receipt)
    if game is not None and game.get('source_commit') != RECORDER_SOURCE:
        raise ValueError('The cached recorder game phase belongs to a different version.')
    if game is None:
        config = (build / 'CMakeCache.txt').read_text() if (build / 'CMakeCache.txt').exists() else ''
        required = ('SUPPORT_BORG_RECORDING:BOOL=ON', 'SUPPORT_X11:BOOL=ON', 'CMAKE_BUILD_TYPE:STRING=Release',
                    f'CMAKE_HOME_DIRECTORY:INTERNAL={source / "engine"}')
        if not all(line in config.splitlines() for line in required):
            run(['cmake', '-S', source / 'engine', '-B', build, '-DCMAKE_BUILD_TYPE=Release',
                 '-DSUPPORT_BORG_RECORDING=ON', '-DSUPPORT_X11=ON'])
        run(['cmake', '--build', build, '--parallel', jobs])
        game_binary = build / 'game/angband'
        write(game_receipt, dict(source_commit=RECORDER_SOURCE, binary=str(game_binary), binary_sha256=sha(game_binary)))
    tools = folder / 'tools'
    run(['cargo', 'build', '--locked', '--release', '--manifest-path',
         source / 'vendor/angband-recorder/Cargo.toml', '--target-dir', tools])
    binary, recorder = build / 'game/angband', tools / 'release/angband-recorder'
    result = dict(source_commit=RECORDER_SOURCE, binary=str(binary), recorder=str(recorder),
                  binary_sha256=sha(binary), recorder_sha256=sha(recorder),
                  profile=str(source / 'harness/profiles/reborn-default.txt'))
    write(receipt, result)
    return result


def original_build(cache, selected):
    program, commit = selected['program'], selected['source']
    folder = cache / 'original-runtime' / program / commit
    receipt = folder / 'runtime.json'
    existing = cached_executable(receipt)
    if existing is not None:
        if existing.get('source_commit') != commit or existing.get('program') != program:
            raise ValueError('The cached original runtime identifies a different program/version.')
        print(f'Using cached {program} version {commit[:12]}: {existing["binary"]}', flush=True)
        return existing
    source = checkout(cache, program, commit)
    binary = source / 'build/rust/game/angband'
    build_id = source / 'build/rust/BUILD_ID'
    identity = {}
    if build_id.exists():
        identity = dict(line.split('=', 1) for line in build_id.read_text().splitlines() if '=' in line)
    reusable = (binary.is_file() and identity.get('git_rev') == commit and identity.get('impl') == 'rust'
                and identity.get('inputs_dirty') == 'no' and identity.get('binary_sha256') == sha(binary))
    if not reusable:
        env = dict(os.environ, BORG_IMPL='rust')
        for name in ('BORG_TEST_FEATURES', 'ANGBAND_BIN'):
            env.pop(name, None)
        run(['bash', source / 'harness/build.sh'], env=env)
    if not binary.is_file():
        raise ValueError('The original build did not produce its expected executable.')
    result = dict(program=program, source_commit=commit, binary=str(binary), binary_sha256=sha(binary))
    write(receipt, result)
    print(f'Cached {program} version {commit[:12]}: {binary}', flush=True)
    return result


def legacy_bundle(cache, case_id, archive=None):
    folder = cache / 'recordings' / (case_id + '-recorded')
    if folder.exists():
        return folder
    packed = Path(archive).resolve() if archive else cache / (case_id + '.tar.xz')
    if not packed.exists():
        cache.mkdir(parents=True, exist_ok=True)
        partial = packed.with_suffix('.partial')
        print(f'Downloading the verified original {case_id} recording…', flush=True)
        with urllib.request.urlopen(f'{RELEASE}/{case_id}.tar.xz', timeout=60) as src, partial.open('wb') as dst:
            shutil.copyfileobj(src, dst)
        partial.replace(packed)
    if sha(packed) != ARCHIVES[case_id]:
        raise ValueError('Original recording archive checksum mismatch; refusing to extract or execute it.')
    folder.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=folder.parent) as temporary:
        with tarfile.open(packed) as stream:
            stream.extractall(temporary, filter='data')
        shutil.move(str(Path(temporary) / folder.name), folder)
    return folder


def prepare_profile(folder, save):
    run_dir = folder / 'run'
    for name in ('user', 'save', 'archive', 'panic', 'scores'):
        (run_dir / name).mkdir(parents=True, exist_ok=True)
    shutil.copy2(save, run_dir / 'save/Borg')
    return run_dir


def environment(runtime, run_dir, human=False):
    env = dict(os.environ, BORG_PROFILE=runtime['profile'], BORG_RUN_DIR=str(run_dir),
               TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
    for key in ('BORG_RECORD_DIR', 'BORG_REPLAY_DIR', 'ANGBAND_RECORD_DIR', 'ANGBAND_REPLAY_DIR',
                'BORG_OBSERVATION_LOG', 'BORG_KNOWLEDGE_LOG', 'BORG_TOOLKIT_HEADLESS'):
        env.pop(key, None)
    if not human:
        env['BORG_TOOLKIT_HEADLESS'] = '1'
    env.setdefault('ANGBAND_X11_FONT', 'fixed')
    return env


def unpack_save(scenario_dir, dest):
    scenario = read(scenario_dir / 'scenario.json')
    with gzip.open(scenario_dir / scenario['save'], 'rb') as src, dest.open('wb') as dst:
        shutil.copyfileobj(src, dst)
    if sha(dest) != scenario['save_sha256']:
        raise ValueError('Scenario save hash mismatch')
    return scenario


def frames(recording):
    with (recording / 'frames.jsonl').open() as stream:
        return [json.loads(line) for line in stream]


def capture_scenario(cache, selected, runtime):
    scenario_dir = selected['scenario']
    scenario = read(scenario_dir / 'scenario.json')
    folder = cache / 'sessions' / scenario_dir.name / RECORDER_SOURCE[:12]
    if (folder / 'verified.json').exists():
        prior = read(folder / 'verified.json')
        if prior.get('scenario_sha256') != sha(scenario_dir / 'scenario.json'):
            raise ValueError('The scenario changed since capture; choose a new cache.')
        if any(not (folder / 'record' / name).is_file() or sha(folder / 'record' / name) != value
               for name, value in prior.get('recording_hashes', {}).items()):
            raise ValueError('The recorded streams changed; preserve the cache and recapture in a new cache.')
        if not prior.get('recording_hashes'):
            raise ValueError('This recording has no retained integrity proof; use a fresh cache.')
        return folder
    if folder.exists():
        raise ValueError(f'An incomplete recorder session is retained at {folder}. Inspect its capture/verify logs or select a fresh --cache; no evidence was overwritten.')
    folder.mkdir(parents=True, exist_ok=False)
    save = folder / 'start.save'
    unpack_save(scenario_dir, save)
    run_dir = prepare_profile(folder, save)
    binary, recorder = Path(runtime['binary']), Path(runtime['recorder'])
    command = [binary, '-mborgh', '-uBorg',
               *[f'-d{k}={run_dir/k}' for k in ('user', 'save', 'archive', 'panic', 'scores')], '--',
               '-load', save, '-keep-load-rng', '-seed', str(scenario['birth_seed']),
               '-race', str(scenario['race_idx']), '-class', str(scenario['class_idx']),
               '-turns', str(scenario['start_turn'] + 1000), '-menu-letters',
               '-keylog', run_dir / 'keys.log', '-msglog', run_dir / 'messages.log',
               '-statelog', run_dir / 'state.log', '-summary', run_dir / 'summary.json', '-screen']
    env = environment(runtime, run_dir)
    for label, argv in (('capture', [recorder, 'record', folder / 'record', '--', *command]),
                        ('verify', [recorder, 'replay', '--verify', folder / 'record', folder / 'verified-replay'])):
        with (folder / (label + '.log')).open('w') as output:
            run(argv, cwd=binary.parent, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=120)
    summary = read(run_dir / 'summary.json')
    if summary.get('loaded_turn') != scenario['start_turn'] or summary.get('loaded') is not True:
        raise ValueError('The game did not load the expected scenario position.')
    if not ((summary.get('dead') is True and summary.get('stop_reason') == 'death') or
            (summary.get('dead') is False and summary.get('stop_reason') == 'turns' and
             summary.get('game_turns', 0) >= scenario['start_turn'] + 1000)):
        raise ValueError(f'The recorded game stopped early ({summary.get("stop_reason")}); retained streams are not a completed scenario trial.')
    write(folder / 'verified.json', dict(runtime=runtime, scenario_sha256=sha(scenario_dir / 'scenario.json'),
                                       summary=summary, independent_birth=False,
                                       recording_hashes={str(p.relative_to(folder / 'record')): sha(p)
                                                         for p in (folder / 'record').rglob('*') if p.is_file()}))
    return folder


def watch_frames(runtime, recording, start, delay, dump=False):
    selected = [f for f in frames(recording) if f.get('turn', 0) >= start]
    if not selected:
        raise ValueError('No recorded screen exists at or after that turn.')
    for frame in selected[:1] if dump else selected:
        if not dump:
            print('\033[H\033[2J', end='', flush=True)
        run([runtime['recorder'], 'view', recording, frame['index']])
        if not dump:
            print('Recorded screen playback — Ctrl-C stops.', flush=True)
            time.sleep(delay)


def alternative_summary(recording, scenario):
    observed = frames(recording)
    with (recording / 'inputs.jsonl').open() as stream:
        events = [json.loads(line) for line in stream]
    bot = any(e.get('kind') == 'bot' for e in events)
    manual = any(e.get('kind') == 'poll' and e.get('input', {}).get('event_type', 0) != 0 for e in events)
    actor = ('mixed human/Borg play' if bot and manual else 'Borg-only play' if bot
             else 'human play' if manual else 'no human gameplay input observed')
    matching = [f for f in observed if f.get('turn') == scenario['start_turn']
                and f.get('race_idx') == scenario['race_idx'] and f.get('class_idx') == scenario['class_idx']]
    if not matching:
        raise ValueError('The human recording has no observation of the expected starting turn; it cannot be attached as this scenario.')
    last = observed[-1]
    outcome = (f"Died: {last.get('cause') or 'cause not recorded'}" if last.get('dead')
               else 'Last observed alive; no survival-to-horizon claim')
    return dict(actor=actor, outcome=outcome, last_turn=last.get('turn'), hp=last.get('hp'))


def attach_human(case, scenario_dir, session, label, note):
    scenario = read(scenario_dir / 'scenario.json')
    summary = alternative_summary(session / 'record', scenario)
    verification = read(session / 'verification.json')
    dest = case / 'alternatives/human' / session.name
    dest.mkdir(parents=True, exist_ok=False)
    packed = dest / 'recording.tar.xz'
    with tarfile.open(packed, 'w:xz') as archive:
        archive.add(session / 'record', arcname='recording')
    if packed.stat().st_size > 50 * 1024 * 1024:
        packed.unlink()
        recording_link = f'Large recording retained locally at `{session / "record"}`; publish it separately before removing that cache.'
    else:
        recording_link = '[Recorder input recording](recording.tar.xz)'
    meta = dict(schema='borg-cemetery/human-alternative@1', label=label, note=note,
                scenario=str(scenario_dir.relative_to(ROOT)) if scenario_dir.is_relative_to(ROOT) else str(scenario_dir),
                scenario_manifest=scenario, save_sha256=scenario['save_sha256'],
                runtime=read(session / 'session.json')['runtime'],
                recording_sha256=sha(packed) if packed.exists() else None,
                session=str(session), verification=verification, independent_birth=False, **summary)
    write(dest / 'alternative.json', meta)
    (dest / 'README.md').write_text(
        f'# Alternative human play — {label}\n\n'
        f"Actor: {summary['actor']}. Started from the same saved game at turn {scenario['start_turn']}, with saved engine RNG and the Borg initially off.\n\n"
        f"Recorded game version: `{meta['runtime'].get('source_commit', 'not retained')}` (the separate recorder-enabled runtime).\n\n"
        f"Outcome: {summary['outcome']}; last recorded turn {summary['last_turn']}, HP {summary['hp']}.\n\n"
        f"Replay verification: {'passed' if verification['verified'] else 'failed; recording retained for investigation'}.\n\n"
        f'{note}\n\n{recording_link}\n\n'
        f'From the death directory, replay with `./watch.sh --alternative {session.name}`.\n\n'
        'This is a branch of the original life, not a new independent death or a proved improvement.\n')
    entries = sorted((case / 'alternatives/human').glob('*/README.md'))
    section = ['## Alternative human play', '']
    section += [f'- [{read(p.parent / "alternative.json")["label"]}]({p.relative_to(case)})' for p in entries]
    marker, end = '<!-- alternative-human-play:start -->', '<!-- alternative-human-play:end -->'
    report = case / ('report.md' if (case / 'report.md').exists() else 'death-report.md')
    original = report.read_text()
    block = marker + '\n' + '\n'.join(section) + '\n' + end
    if marker in original:
        before, remainder = original.split(marker, 1)
        if end not in remainder:
            raise ValueError('The report has an incomplete alternative-play section; the new recording is retained but the report was not overwritten.')
        _, after = remainder.split(end, 1)
        updated = before + block + after
    else:
        updated = original.rstrip() + '\n\n' + block + '\n'
    replacement = report.with_name(report.name + '.new')
    replacement.write_text(updated)
    replacement.replace(report)
    from death_pages import dossier_page, run_page
    if (case / 'record.json').exists():
        dossier_page(case)
    elif (case / 'run.json').exists():
        run_page(case)
    return dest


def legacy_scenario(cache, case, selected, archive=None, start=None):
    bundle = legacy_bundle(cache, selected['case'], archive)
    record = read(case / 'record.json')
    if sha(bundle / 'recording.json') != record['recording']['manifest_sha256']:
        raise ValueError('The legacy recording no longer matches its original case manifest.')
    desired = start if start is not None else (36184 if selected['case'] == 'D0005' else 22736)
    with (bundle / 'run/checkpoints/index.jsonl').open() as stream:
        checkpoints = [json.loads(line) for line in stream]
    eligible = [c for c in checkpoints if c['game_turn'] <= desired]
    if not eligible:
        raise ValueError('No retained living checkpoint is available before the requested turn.')
    checkpoint = max(eligible, key=lambda c: c['game_turn'])
    if Path(checkpoint['file']).name != checkpoint['file']:
        raise ValueError('Invalid checkpoint filename')
    save = bundle / 'run/checkpoints' / checkpoint['file']
    manifest = read(bundle / 'recording.json')
    expected = manifest['files_sha256'].get(str(save.relative_to(bundle)))
    if expected is None or sha(save) != expected:
        raise ValueError('The original checkpoint does not match its recording hash.')
    dest = cache / 'scenario-starts' / selected['case'] / str(checkpoint['game_turn'])
    dest.mkdir(parents=True, exist_ok=True)
    with save.open('rb') as src, gzip.open(dest / 'start.save.gz', 'wb') as dst:
        shutil.copyfileobj(src, dst)
    write(dest / 'scenario.json', dict(status='ready_for_restart_trials', save='start.save.gz',
          save_sha256=sha(save), start_turn=checkpoint['game_turn'], birth_seed=record['identity']['seed'],
          race_idx=record['terminal']['race_idx'], class_idx=record['terminal']['class_idx'],
          original_endpoint_turn=record['identity']['turn'], report_start_turn=desired))
    return dict(kind='scenario', case=selected['case'], scenario=dest)


def watch_alternative(args):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', args.alternative):
        raise ValueError('Use a session identifier, not a path.')
    entry = args.case / 'alternatives/human' / args.alternative
    meta = read(entry / 'alternative.json')
    with native_lock():
        runtime = recorder_build(args.cache, args.jobs)
    recording = Path(meta['session']) / 'record'
    packed = entry / 'recording.tar.xz'
    if packed.exists():
        if sha(packed) != meta['recording_sha256']:
            raise ValueError('Human recording archive hash mismatch')
        dest = args.cache / 'alternative-playback' / args.alternative
        if not dest.exists():
            dest.mkdir(parents=True)
            with tarfile.open(packed) as archive:
                archive.extractall(dest, filter='data')
        recording = dest / 'recording'
    if args.verify_only:
        launch = read(recording / 'launch.json')
        if sha(Path(runtime['binary'])) != launch['sha256']:
            raise ValueError('Exact recorded executable is unavailable. Recorded frames can still be watched; a different build cannot qualify verification.')
        # Relocate only a staging copy's launch paths; keep original inputs intact.
        with tempfile.TemporaryDirectory(dir=args.cache) as temporary:
            stage = Path(temporary) / 'record'
            shutil.copytree(recording, stage)
            launch.update(executable=runtime['binary'], cwd=str(Path(runtime['binary']).parent))
            write(stage / 'launch.json', launch)
            env = environment(runtime, Path(meta['session']) / 'run', human=True)
            with native_lock():
                run([runtime['recorder'], 'replay', '--verify', stage, Path(temporary) / 'replay'], env=env, timeout=300)
        return
    print('Viewing the retained human recording. Verification at attachment: ' + ('passed' if meta['verification']['verified'] else 'not passed'), flush=True)
    watch_frames(runtime, recording, args.dump_turn if args.dump_turn is not None else (args.from_turn or 0), args.delay, args.dump_turn is not None)
    if args.dump_turn is None:
        print(f"{meta['outcome']}; last recorded turn {meta['last_turn']}.", flush=True)


def human_play(args, selected, runtime):
    if selected['kind'] != 'scenario':
        raise ValueError('No retained scenario save is linked to this death. Original recording playback is available where retained; a human branch needs a curated starting save.')
    if not os.environ.get('DISPLAY'):
        raise ValueError('Human play requires an X11 display (for example WSLg). Set DISPLAY in your desktop terminal.')
    folder = args.cache / 'human' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + os.urandom(3).hex())
    folder.mkdir(parents=True)
    scenario = unpack_save(selected['scenario'], folder / 'start.save')
    run_dir = prepare_profile(folder, folder / 'start.save')
    recorder, binary = Path(runtime['recorder']), Path(runtime['binary'])
    env = environment(runtime, run_dir, human=True)
    # Select private directories before -u: Angband resolves the save name
    # while processing that option. Avoid its small filename buffer as well.
    command = [binary, '-mx11',
               *[f'-d{k}={run_dir/k}' for k in ('user', 'save', 'archive', 'panic', 'scores')], '-uBorg']
    write(folder / 'session.json', dict(runtime=runtime, env={k: env[k] for k in ('BORG_PROFILE', 'BORG_RUN_DIR', 'TZ', 'LANG', 'LC_ALL')}, scenario=str(selected['scenario'])))
    if args.prepare_only:
        print(f'Human starting save prepared and hash-checked: {run_dir / "save/Borg"}. No game has been played or attached.', flush=True)
        return
    print(f'Human continuation: saved turn {scenario["start_turn"]}; original report boundary '
          f'{scenario.get("report_start_turn", "not recorded")}; original endpoint '
          f'{scenario.get("original_endpoint_turn", "not recorded")}.', flush=True)
    print('You control the game; the Borg starts off. Your actions can change whether the original encounter happens. '
          'Use watch.sh to watch the recorded Borg sequence. Ctrl-X saves and exits; acknowledge Return/Escape if prompted. '
          'Your continuation will be attached to the death report.', flush=True)
    with (folder / 'capture.log').open('w') as log:
        captured = subprocess.run([str(a) for a in [recorder, 'record', folder / 'record', '--', *command]],
                                  cwd=binary.parent, env=env, stdout=log, stderr=subprocess.STDOUT)
    if not (folder / 'record/frames.jsonl').exists():
        raise ValueError(f'No continuation could be recorded; diagnostics are retained at {folder / "capture.log"}')
    verified = captured.returncode == 0
    with (folder / 'verify.log').open('w') as log:
        if verified:
            try:
                run([recorder, 'replay', '--verify', folder / 'record', folder / 'verified-replay'],
                    env=env, stdout=log, stderr=subprocess.STDOUT, timeout=300)
            except subprocess.SubprocessError:
                verified = False
        else:
            log.write('Capture did not finish cleanly; incomplete streams retained without a verification claim.\n')
    write(folder / 'verification.json', dict(verified=verified, log=str(folder / 'verify.log')))
    case = args.case
    if args.case.parent.name == 'scenarios':
        event = read(args.case / 'episode.json')['event']
        case = ROOT / 'deaths' / event['death_id']
    elif (args.case / 'scenario.json').exists():
        # CI episodes live beneath the original run's death report.
        for parent in args.case.parents:
            if (parent / 'run.json').exists() and (parent / 'death-report.md').exists():
                case = parent
                break
    attached = attach_human(case, selected['scenario'], folder, args.label, args.note)
    print(f'Alternative human play saved and linked: {attached / "README.md"}', flush=True)
    print('The recording and report are repository changes. Commit/push them when ready; unrelated work is not staged automatically.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build', 'watch', 'human'))
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--cache', type=Path, help='shared version cache (default: this checkout/.cache/borg-cemetery)')
    parser.add_argument('--jobs', type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument('--archive', type=Path, help='already downloaded legacy archive; checksum is still verified')
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--dump-turn', type=int)
    parser.add_argument('--from-turn', type=int)
    parser.add_argument('--delay', type=float, default=0.25)
    parser.add_argument('--alternative', help='recorded human-alternative session identifier')
    parser.add_argument('--label', default='Alternative human play')
    parser.add_argument('--note', default='')
    parser.add_argument('--prepare-only', action='store_true', help='prepare a private human starting save without launching or attaching play')
    args = parser.parse_args()
    if args.jobs < 1 or not 0 <= args.delay <= 10:
        parser.error('jobs must be positive; delay must be 0..10 seconds')
    args.case = args.case.resolve()
    args.cache = (args.cache if args.cache is not None else default_cache()).expanduser().resolve()
    try:
        selected = plan(args.case)
        if args.action == 'human' and selected['kind'] == 'scenario' and args.from_turn is not None:
            saved_turn = read(selected['scenario'] / 'scenario.json')['start_turn']
            if args.from_turn != saved_turn:
                raise ValueError(f'This retained human starting save is at turn {saved_turn}, not {args.from_turn}. '
                                 'watch.sh --from-turn seeks recorded screens; human play needs an actual save at the requested position.')
        if args.alternative:
            watch_alternative(args)
            return
        if selected['kind'] == 'legacy' and args.action != 'human':
            bundle = legacy_bundle(args.cache, selected['case'], args.archive)
            if args.action == 'build':
                print(f'Prepared original frozen runtime and player: {bundle}')
                return
            argv = [sys.executable, bundle / 'runtime/tool-source/replay-borg.py', bundle]
            if args.verify_only:
                argv += ['--verify-only', '--output', Path(tempfile.mkdtemp(prefix='cemetery-proof-', dir=args.cache)) / 'proof', '--timeout', '60']
            elif args.dump_turn is not None:
                argv += ['--dump-turn', str(args.dump_turn)]
            elif args.from_turn is not None:
                argv += ['--from-turn', str(args.from_turn)]
            run(argv)
            return
        if args.action == 'build' and selected['kind'] == 'scenario':
            origin = read(selected['scenario'] / 'scenario.json').get('origin', {})
            if origin.get('program') == 'borg-reborn-rs' and origin.get('source_commit') in QUALIFIED_ORIGINS:
                # A cache hit is read-only and should work even while another
                # native run owns the shared validation lock.
                if cached_recorder(args.cache) is not None:
                    return
        if args.action == 'build' and selected['kind'] == 'seed':
            cached = cached_executable(args.cache / 'original-runtime' / selected['program'] / selected['source'] / 'runtime.json')
            if cached is not None:
                if cached.get('source_commit') != selected['source'] or cached.get('program') != selected['program']:
                    raise ValueError('Cached original runtime belongs to another version.')
                print(f'Using cached {selected["program"]} version {selected["source"][:12]}: {cached["binary"]}', flush=True)
                return
        with native_lock():
            if selected['kind'] == 'legacy':
                selected = legacy_scenario(args.cache, args.case, selected, args.archive, args.from_turn)
            if selected['kind'] == 'seed':
                if args.action != 'build':
                    raise ValueError('This historical death has no retained recording/save. build.sh builds its original version; REPLAY.md describes its seed rerun. No original movie can be invented.')
                original_build(args.cache, selected)
                return
            if args.action != 'human':
                origin = read(selected['scenario'] / 'scenario.json').get('origin', {})
                if origin.get('program') != 'borg-reborn-rs' or origin.get('source_commit') not in QUALIFIED_ORIGINS:
                    raise ValueError('No recorder-enabled player has been qualified for this scenario version. Refusing to substitute a different Borg. Its saved-position trial remains available through REPLAY.md.')
            runtime = recorder_build(args.cache, args.jobs)
            if args.action == 'build':
                print(f'Prepared recorder-enabled runtime: {runtime["binary"]}')
            elif args.action == 'human':
                human_play(args, selected, runtime)
            else:
                session = capture_scenario(args.cache, selected, runtime)
                if args.verify_only:
                    print(f'VERIFIED saved-position recording: {session / "record"}')
                    return
        if args.action == 'watch':
            scenario = read(selected['scenario'] / 'scenario.json')
            start = args.dump_turn if args.dump_turn is not None else (args.from_turn if args.from_turn is not None else scenario.get('report_start_turn', scenario['start_turn']))
            watch_frames(runtime, session / 'record', start, args.delay, args.dump_turn is not None)
            if args.dump_turn is None:
                result = read(session / 'verified.json')['summary']
                print(f"Verified game result at turn {result.get('game_turns')}: " +
                      (f"died to {result.get('death_cause')}" if result.get('dead') else 'alive at the requested cap'), flush=True)
                print('The last rendered recorder frame may precede that final game result.', flush=True)
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
