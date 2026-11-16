#!/usr/bin/env python3
"""Bounded generated-dungeon suites. Definitions contain no recorded game/save.

Terminal gameplay, infrastructure validity and hazard coverage are independent.
Executable identity belongs to an attempt, never to a scenario's stable spec.
"""
import argparse
import fcntl
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

SCHEMA = 'borg-cemetery/synthetic-suite@1'
RESULT_SCHEMA = 'borg-cemetery/synthetic-results@1'
CONTRACT = 'borg-reborn-rs/synthetic-start@'
FAILURES = {'harness_failure', 'identity_mismatch', 'timeout', 'unsupported'}
STATE = re.compile(r'^(\d+) -?\d+,-?\d+ d(\d+)/(\d+) hp(-?\d+)/(\d+) sp(-?\d+)/(\d+)(?: |$)')
HEX = re.compile(r'[0-9a-f]{64}')
COMMIT = re.compile(r'[0-9a-f]{40}')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hashed(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def read(path):
    # Duplicate JSON keys would hide conflicting identities or stop rules.
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def kv(path):
    result = {}
    for line in Path(path).read_text().splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            if key in result:
                raise ValueError(f'duplicate receipt field: {key}')
            result[key] = value
    return result


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'integer outside {low}..{high}: {value!r}')
    return value


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or value.keys() - set(required) - set(optional):
        raise ValueError(f'expected fields {required}; got {list(value) if isinstance(value, dict) else type(value).__name__}')


def local_file(root, name, digest):
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError('dependency must be a relative file')
    path = root / name
    if path.is_symlink() or '..' in Path(name).parts or not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'invalid dependency path: {name}')
    if not isinstance(digest, str) or not HEX.fullmatch(digest) or sha(path) != digest:
        raise ValueError(f'dependency hash mismatch: {name}')
    return path


def build_record(path):
    """Validate the portable JSON projection of the deliberately small native adapter."""
    data = Path(path).read_bytes()
    if not 0 < len(data) <= 16384 or not data.endswith(b'\n') or b'\x00' in data or b'\r' in data:
        raise ValueError('invalid native build record bytes')
    lines = data.decode('ascii').splitlines()
    if len(lines) < 10 or any(not line for line in lines) or lines[0] != 'schema:borg-reborn-rs/character-build@1' or lines[-1] != 'end':
        raise ValueError('unsupported native build record')
    if lines[1] != 'engine:42cd156ac9f95ddf4311e88dd7ad462292d6d1d6':
        raise ValueError('native build engine mismatch')
    result = {}
    for index, (label, count) in enumerate((('identity', 3), ('observed', 3), ('vitals', 4), ('stats', 5), ('hp-rolls', 50), ('knowledge', 3)), 2):
        parts = lines[index].split(':')
        if parts[0] != label or len(parts) != count + 1 or any(not re.fullmatch(r'-?[0-9]+', p) for p in parts[1:]):
            raise ValueError(f'invalid build {label}')
        result[label] = [int(p) for p in parts[1:]]
    if result['identity'][:2] != [0, 0]:
        raise ValueError('P1 native adapter supports Human Warrior only')
    integer(result['identity'][2], 1, 15)
    for value in result['stats']:
        integer(value, 3, 118)
    for value in result['vitals'][:2]:
        integer(value, 0, 100000000)
    integer(result['vitals'][2], 1, 10000)
    if result['vitals'][3] != 0 or result['observed'][0] < 0 or not 0 <= result['observed'][1] <= result['vitals'][2] or result['observed'][2] != 0:
        raise ValueError('invalid warrior vitals')
    if any(v not in (0, 1) for v in result['knowledge']) or any(a >= b for a, b in zip([0] + result['hp-rolls'], result['hp-rolls'])):
        raise ValueError('invalid HP progression/combat knowledge')
    items = []
    for line in lines[8:-1]:
        parts = line.split(':')
        if parts[0] != 'item' or len(parts) != 11 or any(not re.fullmatch(r'-?[0-9]+', p) for p in parts[1:]):
            raise ValueError('invalid or unsupported build item')
        items.append(dict(zip(('tval', 'sval', 'quantity', 'slot', 'to_h', 'to_d', 'to_a', 'pval', 'timeout', 'aware'), map(int, parts[1:]))))
        item = items[-1]
        for name, low, high in (('tval', 1, 255), ('sval', 0, 255), ('quantity', 1, 40), ('slot', -1, 11),
                                ('to_h', -20, 20), ('to_d', -20, 20), ('to_a', -20, 20), ('pval', 0, 32767), ('timeout', 0, 32767), ('aware', 0, 1)):
            integer(item[name], low, high)
    if not 1 <= len(items) <= 48:
        raise ValueError('invalid build item count')
    equipped = [item['slot'] for item in items if item['slot'] >= 0]
    if len(set(equipped)) != len(equipped) or any(item['quantity'] != 1 for item in items if item['slot'] >= 0):
        raise ValueError('duplicate/stacked equipment slots')
    result['items'] = items
    return result


def catalog(record_path, run_path, source, output):
    record_path, run_path, source = map(Path, (record_path, run_path, source))
    projection = build_record(record_path)
    summary, identity = read(run_path / 'summary.json'), kv(source / 'build/rust/BUILD_ID')
    process = read(run_path / 'process.json')
    if (summary.get('synthetic') or summary.get('loaded') is not False or
            summary.get('race_idx') != projection['identity'][0] or summary.get('class_idx') != projection['identity'][1] or
            type(summary.get('game_turns')) is not int or summary['game_turns'] < projection['observed'][0] or
            summary.get('build_capture_sha256') != sha(record_path) or
            summary.get('build_capture_level') != projection['identity'][2] or
            summary.get('build_capture_turn') != projection['observed'][0]):
        raise ValueError('record lacks matching ordinary-run capture receipt')
    if identity.get('inputs_dirty') != 'no' or identity.get('git_dirty') != 'no':
        raise ValueError('catalog provenance requires a clean measured build')
    try:
        RebornAdapter(source).describe(identity.get('git_rev'), set())
    except ExecutionError as error:
        raise ValueError(f'catalog source verification failed: {error}') from error
    if (process.get('status') != 'success' or process.get('exit_code') != 0 or
            process.get('executable_sha256_before') != identity.get('binary_sha256') or
            process.get('executable_sha256_after') != identity.get('binary_sha256')):
        raise ValueError('catalog source binary/process identity mismatch')
    value = dict(schema='borg-cemetery/character-catalog@1', selection='single_observed_tier',
                 sample_count=1, independent_run_count=1, projection=projection,
                 record_sha256=sha(record_path),
                 provenance=dict(build=identity, seed=summary['seed'], summary_sha256=sha(run_path / 'summary.json'),
                                 config_sha256=sha(run_path / 'config.txt'), keys_sha256=sha(run_path / 'keys.log'),
                                 state_sha256=sha(run_path / 'state.log'), capture_turn=summary['build_capture_turn']),
                 normalization=['full HP/SP at synthetic start', 'no timed status effects', 'fresh Borg memory',
                                'fresh-birth hunger and other nonprojected character state',
                                'native mundane-kind projection; recorded combat knowledge and carried-kind awareness',
                                'other historical knowledge, quest history and dungeon state are not restored'],
                 limitations=['one observation, not a population average or typical-kit claim',
                              'Human Warrior only; no artifacts, egos, curses or nondefault item properties'],
                 missing_data=['historical monster/object knowledge beyond the recorded projection', 'Borg private memory and source dungeon/quest history'])
    check_catalog(value, projection, sha(record_path))
    write(output, value)
    return value


def check_catalog(value, projection, record_digest):
    fields(value, ('schema', 'selection', 'sample_count', 'independent_run_count', 'projection', 'record_sha256',
                   'provenance', 'normalization', 'limitations', 'missing_data'))
    if (value['schema'] != 'borg-cemetery/character-catalog@1' or value['selection'] != 'single_observed_tier' or
            type(value['sample_count']) is not int or value['sample_count'] != 1 or
            type(value['independent_run_count']) is not int or value['independent_run_count'] != 1 or
            value['record_sha256'] != record_digest or value['projection'] != projection):
        raise ValueError('catalog/build identity or selection mismatch')
    for key in ('normalization', 'limitations', 'missing_data'):
        if not isinstance(value[key], list) or not value[key] or any(not isinstance(v, str) or not v for v in value[key]):
            raise ValueError('catalog must declare normalization, limitations and missing data')
    provenance = value['provenance']
    fields(provenance, ('build', 'seed', 'summary_sha256', 'config_sha256', 'keys_sha256', 'state_sha256', 'capture_turn'))
    integer(provenance['seed'], 0, 2**32 - 1)
    if provenance['capture_turn'] != projection['observed'][0]:
        raise ValueError('catalog capture anchor mismatch')
    for key in ('summary_sha256', 'config_sha256', 'keys_sha256', 'state_sha256'):
        if not isinstance(provenance[key], str) or not HEX.fullmatch(provenance[key]):
            raise ValueError('catalog evidence digest missing')
    build = provenance['build']
    if (not isinstance(build, dict) or build.get('impl') != 'rust' or build.get('inputs_dirty') != 'no' or build.get('git_dirty') != 'no' or
            not COMMIT.fullmatch(build.get('git_rev', '')) or
            not HEX.fullmatch(build.get('source_sha256', '')) or not HEX.fullmatch(build.get('binary_sha256', ''))):
        raise ValueError('catalog requires exact clean source and binary identities')


def generate(path):
    path = Path(path)
    root = path.parent.resolve()
    manifest = read(path)
    fields(manifest, ('schema', 'suite_id', 'revision', 'seeds', 'depths', 'turn_cap', 'wall_seconds', 'candidate_screen', 'character_builds', 'runtime'))
    if manifest['schema'] != SCHEMA or not isinstance(manifest['suite_id'], str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', manifest['suite_id']):
        raise ValueError('unsupported suite identity/schema')
    integer(manifest['revision'], 1, 1000000)
    integer(manifest['turn_cap'], 100, 100000)
    integer(manifest['wall_seconds'], 1, 120)
    screen = manifest['candidate_screen']
    fields(screen, ('kind', 'hp_threshold'))
    if screen['kind'] != 'low_hp_candidate':
        raise ValueError('P1 supports only an explicitly provisional low-HP screen')
    integer(screen['hp_threshold'], 0, 100)
    runtime = manifest['runtime']
    fields(runtime, ('repository', 'commit'))
    if runtime['repository'] != 'diegoami/borg-reborn-rs' or not isinstance(runtime['commit'], str) or not COMMIT.fullmatch(runtime['commit']):
        raise ValueError('runtime must name an exact supported repository commit')
    for label, maximum in (('seeds', 2**32 - 1), ('depths', 127)):
        values = manifest[label]
        if not isinstance(values, list) or not values or len(values) > 32:
            raise ValueError(f'invalid {label}')
        for value in values:
            integer(value, 0 if label == 'seeds' else 1, maximum)
        if len(set(values)) != len(values):
            raise ValueError(f'duplicate {label}')
    builds = manifest['character_builds']
    if not isinstance(builds, list) or not builds or len(builds) > 8:
        raise ValueError('missing/bounded character builds required')
    if len(builds) * len(manifest['seeds']) * len(manifest['depths']) > 64:
        raise ValueError('suite exceeds 64-cell work budget')
    identifiers = set()
    for build in builds:
        fields(build, ('id', 'race_idx', 'class_idx', 'core', 'profile', 'profile_sha256', 'start'),
               ('record', 'record_sha256', 'catalog', 'catalog_sha256'))
        if not isinstance(build['id'], str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', build['id']) or build['id'] in identifiers:
            raise ValueError('invalid/duplicate character-build ID')
        identifiers.add(build['id'])
        integer(build['race_idx'], 0, 10)
        integer(build['class_idx'], 0, 8)
        if build['core'] not in ('reborn', 'borg-rs'):
            raise ValueError('unsupported explicit Borg core')
        local_file(root, build['profile'], build['profile_sha256'])
        if build['start'] == 'record':
            if not all(k in build for k in ('record', 'record_sha256', 'catalog', 'catalog_sha256')):
                raise ValueError('record build needs exact catalog provenance')
            native = build_record(local_file(root, build['record'], build['record_sha256']))
            cat = read(local_file(root, build['catalog'], build['catalog_sha256']))
            check_catalog(cat, native, build['record_sha256'])
            if native['identity'][:2] != [build['race_idx'], build['class_idx']]:
                raise ValueError('catalog character mismatch')
        elif build['start'] != 'birth' or any(k in build for k in ('record', 'record_sha256', 'catalog', 'catalog_sha256')):
            raise ValueError('unsupported/ambiguous character build')
    # Runtime is intentionally excluded: selecting a different executable does
    # not create different starting cases. Requested manifest bytes are retained separately.
    spec = {key: value for key, value in manifest.items() if key != 'runtime'}
    spec.update(seeds=sorted(manifest['seeds']), depths=sorted(manifest['depths']), character_builds=sorted(builds, key=lambda build: build['id']))
    suite_hash = hashed(spec)
    cases = []
    for seed in sorted(manifest['seeds']):
        for depth in sorted(manifest['depths']):
            for build in sorted(builds, key=lambda value: value['id']):
                expected_start = dict(level=1)
                if build['start'] == 'record':
                    native = build_record(local_file(root, build['record'], build['record_sha256']))
                    expected_start = dict(level=native['identity'][2], max_hp=native['vitals'][2], max_sp=native['vitals'][3])
                case = dict(schema='borg-cemetery/synthetic-scenario@1', suite_id=manifest['suite_id'],
                            revision=manifest['revision'], seed=seed, depth=depth, character_build=build,
                            turn_cap=manifest['turn_cap'], wall_seconds=manifest['wall_seconds'], candidate_screen=screen,
                            expected_start=expected_start, harness_contract=CONTRACT + '2')
                digest = hashed(case)
                cases.append(dict(case, id=manifest['suite_id'] + '-' + digest[:24], spec_sha256=digest))
    if len({c['id'] for c in cases}) != len(cases):
        raise ValueError('scenario ID collision')
    return dict(manifest=manifest, manifest_sha256=sha(path), suite_spec_sha256=suite_hash,
                cases=cases, root=root)


class ExecutionError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class RebornAdapter:
    def __init__(self, source):
        self.source = Path(source).resolve()

    def describe(self, expected_commit, contracts, cores=()):
        def git(*args):
            return subprocess.check_output(['git', '-C', str(self.source), *args], text=True).strip()
        head = git('rev-parse', 'HEAD')
        if head != expected_commit or git('status', '--porcelain'):
            raise ExecutionError('identity_mismatch', 'target checkout must be clean at the exact requested commit')
        capabilities_path = self.source / 'harness/capabilities.json'
        if not capabilities_path.is_file():
            raise ExecutionError('unsupported', 'pinned harness has no capability declaration')
        capabilities = read(capabilities_path)
        if (not isinstance(capabilities, dict) or capabilities.get('schema') != 'borg-reborn-rs/harness-capabilities@1' or
                not isinstance(capabilities.get('contracts'), list) or not all(isinstance(c, str) for c in capabilities['contracts']) or
                not contracts <= set(capabilities.get('contracts', [])) or not set(cores) <= set(capabilities.get('cores', []))):
            raise ExecutionError('unsupported', 'pinned harness lacks a required start capability')
        build = kv(self.source / 'build/rust/BUILD_ID')
        binary = self.source / 'build/rust/game/angband'
        current = subprocess.check_output(['bash', str(self.source / 'harness/identity.sh'), 'source-hash', 'rust'], text=True).strip()
        if (build.get('git_rev') != head or build.get('impl') != 'rust' or build.get('inputs_dirty') != 'no' or
                build.get('git_dirty') != 'no' or build.get('source_sha256') != current or
                build.get('binary_sha256') != sha(binary)):
            raise ExecutionError('identity_mismatch', 'source inputs or binary do not match the pinned clean build')
        return dict(repository='diegoami/borg-reborn-rs', commit=head, build=build,
                    capabilities_sha256=sha(capabilities_path))

    def run(self, case, root, output):
        build = case['character_build']
        profile = local_file(root, build['profile'], build['profile_sha256'])
        profile_copy = output.parent / 'profile.txt'
        profile_copy.write_bytes(profile.read_bytes())
        profile_copy.chmod(0o400)
        if sha(profile_copy) != build['profile_sha256']:
            raise ExecutionError('identity_mismatch', 'profile changed during preparation')
        # Construct a small child environment. No account token, secret, inherited
        # Borg policy, arbitrary binary/data path, or save root reaches gameplay.
        env = {key: os.environ[key] for key in ('PATH', 'TMPDIR', 'LD_LIBRARY_PATH') if key in os.environ}
        env.update(TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8', BORG_IMPL='rust', BORG_PROFILE=str(profile_copy),
                   BORG_CORE=build['core'],
                   BORG_DEATH_RECORDS_DIR=str(output.parent / 'natural-registry-guard'),
                   RUN_TIMEOUT_SECONDS=str(case['wall_seconds']), CHECKPOINT_EVERY='0')
        argv = ['bash', str(self.source / 'harness/run.sh'), str(output), str(case['seed']), str(build['race_idx']),
                str(build['class_idx']), str(case['turn_cap']), f"menu,start-depth={case['depth']}"]
        if build['start'] == 'record':
            argv += ['--', '-start-build', str(local_file(root, build['record'], build['record_sha256']))]
        with Path('/tmp/angband-validation.lock').open('a') as lock, (output.parent / 'launcher.log').open('wb') as log:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                result = subprocess.run(argv, cwd=self.source, env=env, stdout=log, stderr=subprocess.STDOUT,
                                        timeout=case['wall_seconds'] + 15)
                return result.returncode
            except subprocess.TimeoutExpired:
                return 124


def classify(case, output, returncode, expected_binary=None):
    result = dict(status='harness_failure', reason='', terminal=None, death_cause=None,
                  launcher_returncode=returncode,
                  minimum_observed_living_hp=None, candidate_screen=dict(kind='low_hp_candidate', count=None),
                  refusal_messages=dict(coverage='unavailable', nothing_happens_dot=None, nothing_happens_bang=None),
                  qualified_near_death=dict(coverage='unavailable', count=None, reason='P1 has no null-move evaluator'),
                  evidence={})
    receipts = {}
    for name in ('summary.json', 'process.json', 'config.txt', 'state.log', 'messages.log'):
        path = output / name
        if path.is_file():
            result['evidence'][name] = dict(sha256=sha(path), bytes=path.stat().st_size)
            if name not in ('state.log', 'messages.log'):
                try:
                    value = kv(path) if name == 'config.txt' else read(path)
                    if not isinstance(value, dict):
                        raise ValueError('receipt must be an object')
                    receipts[name] = value
                except (ValueError, UnicodeError):
                    result['reason'] = f'malformed {name}'
    summary, process, config = (receipts.get(name, {}) for name in ('summary.json', 'process.json', 'config.txt'))
    if (output / 'messages.log').is_file():
        try:
            messages = [parts[3].strip() for line in (output / 'messages.log').read_text().splitlines()
                        if len(parts := line.split(' ', 3)) == 4]
            result['refusal_messages'] = dict(coverage='recorded_native_messages',
                nothing_happens_dot=messages.count('Nothing happens.'), nothing_happens_bang=messages.count('Nothing happens!'),
                note='generic engine messages, not a unique action/cost classifier; inspect adjacent messages for attribution')
        except UnicodeError:
            pass
    if returncode == 124 or process.get('status') == 'timeout' or process.get('timed_out') is True:
        result.update(status='timeout', reason='wall limit; partial evidence retained')
        return result
    if type(returncode) is not int or returncode or process.get('status') != 'success' or type(process.get('exit_code')) is not int or process.get('exit_code') != 0:
        result['reason'] = 'launcher/child failure or missing successful process receipt'
        return result
    if result['reason'] or set(receipts) != {'summary.json', 'process.json', 'config.txt'} or 'state.log' not in result['evidence']:
        result['reason'] = result['reason'] or 'missing required evidence'
        return result
    build = case['character_build']
    if (not isinstance(summary.get('game_options'), dict) or type(summary.get('dead')) is not bool or
            not isinstance(summary.get('stop_reason'), str) or
            summary.get('death_cause') is not None and not isinstance(summary.get('death_cause'), str)):
        result['reason'] = 'malformed typed terminal/options receipt'
        return result
    expected = dict(synthetic=True, loaded=False, seed=case['seed'], race_idx=build['race_idx'], class_idx=build['class_idx'],
                    start_depth=case['depth'], initial_depth=case['depth'], initial_cave_depth=case['depth'],
                    initial_generation_pending=False, start_build=build['start'],
                    synthetic_contract=case['harness_contract'], dungeon_mode='one_way')
    mismatch = [key for key, value in expected.items() if type(summary.get(key)) is not type(value) or summary.get(key) != value]
    if expected_binary and (process.get('executable_sha256_before') != expected_binary or process.get('executable_sha256_after') != expected_binary):
        mismatch.append('executed binary digest')
    for key, summary_key in (('level', 'initial_clevel'), ('max_hp', 'initial_max_hp'), ('max_sp', 'initial_max_sp')):
        if key in case['expected_start'] and (type(summary.get(summary_key)) is not int or summary[summary_key] != case['expected_start'][key]):
            mismatch.append(summary_key)
    if build['start'] == 'record' and summary.get('start_build_sha256') != build['record_sha256']:
        mismatch.append('start_build_sha256')
    options = summary.get('game_options', {})
    if options.get('birth_force_descend') is not True or options.get('birth_no_recall') is not True:
        mismatch.append('native one-way options')
    if (config.get('synthetic') != '1' or config.get('start_depth') != str(case['depth']) or
            config.get('profile_sha256') != build['profile_sha256'] or config.get('start_build') != build['start'] or
            config.get('borg_core') != build['core'] or
            config.get('synthetic_contract') != case['harness_contract'] or config.get('dungeon_mode') != 'one_way'):
        mismatch.append('configuration receipt')
    if build['start'] == 'record' and config.get('start_build_sha256') != build['record_sha256']:
        mismatch.append('configuration build digest')
    if mismatch:
        result.update(status='identity_mismatch', reason=', '.join(mismatch))
        return result
    rows = []
    previous = -1
    try:
        for line in (output / 'state.log').read_text().splitlines():
            match = STATE.match(line)
            if not match:
                raise ValueError('malformed state row')
            turn, depth, maximum, hp, max_hp, sp, max_sp = map(int, match.groups())
            if turn < previous or depth < case['depth'] or maximum < depth or max_hp < 1:
                raise ValueError('state chronology/depth mismatch')
            rows.append((turn, depth, maximum, hp))
            previous = turn
    except (ValueError, UnicodeError) as error:
        result.update(status='identity_mismatch', reason=str(error))
        return result
    if not rows or rows[0][1:3] != (case['depth'], case['depth']):
        result.update(status='identity_mismatch', reason='missing or incorrect first state')
        return result
    terminal_turn = summary.get('game_turns')
    if type(terminal_turn) is not int or terminal_turn < previous or type(summary.get('keys')) is not int or summary.get('keys') != len(rows):
        result.update(status='identity_mismatch', reason='terminal/log boundary mismatch')
        return result
    alive = [(turn, hp) for turn, _, _, hp in rows if hp >= 0]
    result['minimum_observed_living_hp'] = min((hp for _, hp in alive), default=None)
    result['candidate_screen']['count'] = len({turn for turn, hp in alive if hp <= case['candidate_screen']['hp_threshold']})
    result['candidate_screen']['hp_threshold'] = case['candidate_screen']['hp_threshold']
    result['candidate_screen']['sampling'] = 'distinct engine turns in pre-key state log; provisional, not qualified exposure'
    if summary.get('dead') is True and summary.get('stop_reason') == 'death':
        result.update(status='death', terminal='dead', death_cause=summary.get('death_cause') or 'unknown')
    elif summary.get('dead') is False and summary.get('stop_reason') == 'turns' and terminal_turn >= case['turn_cap']:
        result.update(status='survived_to_cap', terminal='alive_at_horizon')
    elif summary.get('dead') is False and summary.get('stop_reason') != 'death' and isinstance(summary.get('stop_reason'), str):
        result.update(status='stopped', terminal='stopped', reason=summary['stop_reason'])
    else:
        result['reason'] = 'missing/contradictory terminal evidence'
    result['observed_turns'] = terminal_turn
    result['progress'] = {key: summary.get(key) for key in ('game_turns', 'player_turns', 'borg_decisions', 'keys', 'stop_reason')}
    return result


def report(document):
    rows = document['results']
    counts = Counter(row['status'] for row in rows)
    lines = [f"# Synthetic suite {document['suite_id']} revision {document['revision']}", '',
             f"Attempted {sum(row['attempted'] for row in rows)} / {document['scenario_count']} scenarios. "
             f"Deaths: {counts['death']}; survived to cap: {counts['survived_to_cap']}; stopped: {counts['stopped']}; "
             f"failures/mismatches/timeouts/unsupported: {sum(counts[s] for s in FAILURES)}.", '',
             'Qualified near-death coverage is unavailable; count is unknown. Low-HP screens are provisional.', '',
             '| Scenario | Depth | Character tier | Outcome | Min living HP observed | Candidate sampled turns | Nothing happens messages | Death cause / reason |',
             '|---|---:|---|---|---:|---:|---:|---|']
    groups = defaultdict(Counter)
    for row in rows:
        groups[(row['depth'], row['character_build_id'])][row['status']] += 1
        clean = lambda value: str(value).replace('|', '/').replace('\n', ' ') if value is not None else 'unavailable'
        refused = row['refusal_messages']
        refusal_count = (refused['nothing_happens_dot'] + refused['nothing_happens_bang']) if refused['coverage'] != 'unavailable' else None
        lines.append('| ' + ' | '.join(map(clean, (row['scenario_id'], row['depth'], row['character_build_id'], row['status'],
                     row['minimum_observed_living_hp'], row['candidate_screen']['count'], refusal_count, row['death_cause'] or row['reason']))) + ' |')
    lines += ['', '| Depth | Character tier | Total denominator | Death | Survived | Stopped | Invalid |', '|---:|---|---:|---:|---:|---:|---:|']
    aggregates = []
    for (depth, build), group in sorted(groups.items()):
        total, invalid = sum(group.values()), sum(group[status] for status in FAILURES)
        lines.append(f"| {depth} | {build} | {total} | {group['death']} | {group['survived_to_cap']} | {group['stopped']} | {invalid} |")
        aggregates.append(dict(depth=depth, character_build_id=build, denominator=total, counts=dict(group)))
    lines += ['', 'These are synthetic starting-condition experiments, not historical replays or population improvement evidence.',
              'Character catalog provenance and sampling/normalization limits are part of each scenario definition.',
              'Minimum HP describes sampled pre-key states; it is not a complete decision-state distribution.', '']
    document['aggregates'] = aggregates
    document['counts'] = dict(counts)
    document['attempted_count'] = sum(row['attempted'] for row in rows)
    document['minimum_living_hp_distribution'] = dict(Counter(str(row['minimum_observed_living_hp']) for row in rows))
    document['death_causes'] = dict(Counter(row['death_cause'] for row in rows if row['status'] == 'death'))
    document['missing_evidence'] = [dict(scenario_id=row['scenario_id'], files=sorted({'summary.json', 'process.json', 'config.txt', 'state.log'} - row['evidence'].keys()))
                                    for row in rows if {'summary.json', 'process.json', 'config.txt', 'state.log'} - row['evidence'].keys()]
    lines += ['Death causes: ' + json.dumps(document['death_causes'], sort_keys=True),
              'Sampled minimum living HP distribution: ' + json.dumps(document['minimum_living_hp_distribution'], sort_keys=True),
              f"Scenarios with missing evidence: {len(document['missing_evidence'])}.", '']
    return '\n'.join(lines)


def run_suite(path, source, output, target_commit=None, adapter=None):
    generated = generate(path)
    manifest, cases, root = generated['manifest'], generated['cases'], generated['root']
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    target = target_commit or manifest['runtime']['commit']
    if not isinstance(target, str) or not COMMIT.fullmatch(target):
        raise ValueError('target override must be an exact commit')
    adapter = adapter or RebornAdapter(source)
    identity, preflight = None, None
    try:
        identity = adapter.describe(target, {case['harness_contract'] for case in cases}, {case['character_build']['core'] for case in cases})
    except ExecutionError as error:
        preflight = error
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as error:
        preflight = ExecutionError('harness_failure', f'preflight failed: {error}')
    document = dict(schema=RESULT_SCHEMA, suite_id=manifest['suite_id'], revision=manifest['revision'],
                    producer=dict(runner_sha256=sha(Path(__file__)), workflow_run_id=os.environ.get('GITHUB_RUN_ID'),
                                  workflow_attempt=os.environ.get('GITHUB_RUN_ATTEMPT')),
                    manifest_sha256=generated['manifest_sha256'], suite_spec_sha256=generated['suite_spec_sha256'],
                    requested_runtime=dict(repository=manifest['runtime']['repository'], commit=target),
                    build_identity=identity, scenario_count=len(cases), results=[])
    write(output / 'scenarios.json', cases)
    for case in cases:
        case_dir = output / 'attempts' / case['id']
        case_dir.mkdir(parents=True)
        write(case_dir / 'scenario.json', case)
        if preflight:
            result = dict(status=preflight.status, reason=str(preflight), terminal=None, death_cause=None,
                          minimum_observed_living_hp=None, candidate_screen=dict(kind='low_hp_candidate', count=None),
                          refusal_messages=dict(coverage='unavailable', nothing_happens_dot=None, nothing_happens_bang=None),
                          qualified_near_death=dict(coverage='unavailable', count=None), evidence={})
        else:
            try:
                rc = adapter.run(case, root, case_dir / 'run')
                result = classify(case, case_dir / 'run', rc, (identity.get('build') or {}).get('binary_sha256'))
                if (case_dir / 'profile.txt').exists() and sha(case_dir / 'profile.txt') != case['character_build']['profile_sha256']:
                    result.update(status='identity_mismatch', terminal=None, reason='profile changed during execution')
                if (case_dir / 'natural-registry-guard').exists():
                    result.update(status='harness_failure', terminal=None, reason='synthetic run wrote a natural registry')
            except (OSError, ValueError, ExecutionError, subprocess.SubprocessError) as error:
                result = classify(case, case_dir / 'run', 1)
                if isinstance(error, ExecutionError):
                    result['status'] = error.status
                result['reason'] = str(error)
        result.update(attempted=preflight is None, scenario_id=case['id'], spec_sha256=case['spec_sha256'], depth=case['depth'],
                      character_build_id=case['character_build']['id'])
        document['results'].append(result)
        write(case_dir / 'result.json', result)
    (output / 'report.md').write_text(report(document))
    write(output / 'results.json', document)
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('generate', 'run'):
        child = sub.add_parser(command)
        child.add_argument('--manifest', required=True, type=Path)
        child.add_argument('--out', required=True, type=Path)
        if command == 'run':
            child.add_argument('--source', required=True, type=Path)
            child.add_argument('--target-commit')
    child = sub.add_parser('catalog')
    for name in ('record', 'run', 'source', 'out'):
        child.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'generate':
            value = generate(args.manifest)
            write(args.out, dict(schema='borg-cemetery/synthetic-scenarios@1', suite_spec_sha256=value['suite_spec_sha256'], scenarios=value['cases']))
        elif args.command == 'catalog':
            catalog(args.record, args.run, args.source, args.out)
        else:
            document = run_suite(args.manifest, args.source, args.out, args.target_commit)
            return int(any(row['status'] in FAILURES for row in document['results']))
    except (OSError, ValueError, KeyError, ExecutionError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
