#!/usr/bin/env python3
"""Rerun a recorded death with its logs (task TE.6, #76; docs/SPEC.md §8, §11).

  tools/rerun-death.py docs/deaths/D0664-rust-seed102 OUTDIR [--checkpoint-every N] [--any-build]

A run is deterministic: the same build, seed, character and flags play the
same game. This reruns a dossier's game through harness/run.sh with the
Borg's logs on: the observation of every think, the world model's digest
after each, the knowledge (docs/ENGINE.md), and, with --checkpoint-every,
an engine save every N game turns. A verified reproduction requires the
recorded binary, effective configuration/parameter receipts, death endpoint
and complete key/state/message streams to match. Missing evidence fails closed.

The build must be the death's: build/rust/BUILD_ID's source_sha256 equals
the dossier's, else the tool says which commit to check out and build.
--any-build reruns anyway; the result is then not a reproduction.

A Zoo cell (config.txt has zoo_profile) did not go through harness/run.sh:
Zoo applied the profile's settings to the source's harness/borg.txt and
started the game directly. Its rerun rebuilds that text from config.txt's
borg_* settings, strips Zoo's adapter-only world setting and checks the
recorded borg_txt_sha256. For PBorg it converts the text and checks
pborg_yaml_sha256 before starting the game with Zoo's arguments.

The run's recorded settings are restored too, including an errands plan:
the dossier's own copy when export-death.py kept one, else the file
config.txt names in the source checkout. A ladders or plan file whose
bytes differ from the recorded sha256 is refused.

OUTDIR gets reproduction.json and the run directory. The reborn core requires
observations.jsonl, worlds.txt and knowledge.json; borg-rs instead requires
run/params-core.json and run/trace-core.jsonl. Ambient policy is cleared and
only environment-origin parameters are restored from the retained receipt.
Historical harness dossiers without borg_core explicitly select reborn.
The rerun's exported dossier stays under OUTDIR, never in the canonical registry.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CEMETERY_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(globals().get('SOURCE_ROOT', os.environ.get('BORG_DEATH_SOURCE_ROOT', str(CEMETERY_ROOT.parent / 'borg-reborn-rs'))))


def read_kv(path):
    if not path.exists():
        return {}
    return dict(l.split('=', 1) for l in path.read_text().splitlines() if '=' in l)


# The settings harness/run.sh records when the environment gives them
# (review #227, finding 8): the core, the errand and its options, the plan.
SETTINGS = ('BORG_CORE', 'BORG_CORE_OVERRIDES', 'BORG_ERRAND', 'BORG_STOPSCARED', 'BORG_ERRAND_BUDGET',
            'BORG_LADDERS', 'BORG_ERRANDS_PLAN')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_hash(case_dir, record, config, name, identity_key=None):
    """All retained identity receipts must agree, including a missing payload."""
    expected = [record.get('files_sha256', {}).get(name)]
    if identity_key:
        expected += [record['identity'].get(identity_key), config.get(identity_key)]
    expected = [value for value in expected if value]
    if expected and (len(set(expected)) != 1 or not (case_dir / name).is_file()
                     or sha(case_dir / name) != expected[0]):
        raise SystemExit(f'rerun-death: retained {name} differs from its recorded hash or is missing')
    return expected[0] if expected else None


def controller(config, zoo=False, native_receipt=False):
    """The core that played, from the recorded controller.

    Before borg-reborn-rs #606/#607, an unset harness BORG_CORE played reborn,
    so a historical harness record without borg_core names the reborn core.
    Zoo selects through borg.txt instead, and must not use that fallback.

    A native parameter receipt settles it either way: only the native core
    writes params-core.json (the reborn core writes params.json), and
    harness/run.sh records params_core_sha256 only when that file exists. A
    record with such a receipt and no borg_core is a native run, not a
    historical reborn one, and must not be replayed on the wrong core.
    """
    if zoo:
        core = config.get('borg_reborn_core', 'borg-rs')
    elif 'borg_core' in config:
        core = config['borg_core']
    elif native_receipt:
        core = 'borg-rs'
    else:
        core = 'reborn'
    if core not in ('reborn', 'borg-rs'):
        raise SystemExit(f'rerun-death: unsupported recorded core {core!r}')
    if zoo and 'borg_core' in config and config['borg_core'] != core:
        raise SystemExit('rerun-death: contradictory recorded controller settings')
    if not zoo and native_receipt and core != 'borg-rs':
        raise SystemExit('rerun-death: native parameter receipt contradicts the recorded reborn core')
    return core


def parameter_environment(case_dir, record, config):
    """Restore environment origins only; file origins stay in borg.txt.

    Exact post-run parameter bytes check values, origins, class overrides and
    defaults together. An unrecoverable custom borg.txt must fail that check,
    not silently become an environment override with different provenance.
    """
    digest = checked_hash(case_dir, record, config, 'params-core.json', 'params_core_sha256')
    path = case_dir / 'params-core.json'
    if not path.exists():
        return {}, None
    if not digest:
        raise SystemExit('rerun-death: params-core.json has no recorded hash')
    try:
        values = json.loads(path.read_text())
        if not isinstance(values, list) or not values:
            raise ValueError('expected a nonempty parameter list')
        env, seen = {}, set()
        for row in values:
            name = row['name']
            if not isinstance(name, str) or not re.fullmatch(r'[a-z][a-z0-9_]*', name) or name in seen:
                raise ValueError('invalid or duplicate parameter name')
            seen.add(name)
            entries = [(name, row)]
            classes = row.get('class_values', {})
            if not isinstance(classes, dict):
                raise ValueError('invalid class_values')
            for cls, value in classes.items():
                if cls not in ('warrior', 'mage', 'druid', 'priest', 'necromancer',
                               'paladin', 'rogue', 'ranger', 'blackguard'):
                    raise ValueError('unknown parameter class')
                entries.append((name + '__' + cls, value))
            for key, entry in entries:
                if entry['origin'] not in ('default', 'borg.txt', 'environment') or type(entry['value']) is not int:
                    raise ValueError('invalid parameter value or origin')
                if entry['origin'] == 'environment':
                    env['BORG_PARAM_' + key.upper()] = str(entry['value'])
        return env, digest
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'rerun-death: invalid params-core.json: {error}') from error


def clean_environment():
    # Native policy has many BORG_* settings outside SETTINGS; none may leak
    # into a replay. Keep the explicit toolkit location, which changes code
    # lookup, not gameplay. Runtime paths and instrumentation are set below.
    return {k: v for k, v in os.environ.items()
            if (not k.startswith(('BORG_', 'ANGBAND_', 'BORGH_')) or k == 'BORG_CEMETERY_DIR')
            and k not in ('SAVE_ROOT', 'CHECKPOINT_EVERY', 'STALL_TIMEOUT_SECONDS')}


def settings(config, case_dir=None):
    """The environment a dossier's run had, from its config.txt. A ladders
    file or errands plan must still be the one the run read."""
    # Empty values too: set but empty is not unset (re-review #227, 6).
    env = {v: config[v.lower()] for v in SETTINGS if v.lower() in config}
    if env.get('BORG_LADDERS'):
        path = Path(env['BORG_LADDERS'])
        if not path.is_absolute():
            path = ROOT / path
        env['BORG_LADDERS'] = str(path)
        want = config.get('borg_ladders_sha256')
        have = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if not want or have != want:
            raise SystemExit(f'rerun-death: the run read ladders {path} ({str(want)[:12]}); '
                             f'here it is {"missing" if have is None else have[:12]}')
    if env.get('BORG_ERRANDS_PLAN'):
        # A dossier keeps the plan a run read, so a later edit in the source
        # checkout does not change what the rerun plays. Without the copy,
        # config.txt names it relative to the source checkout (absolute when
        # outside it); run.sh runs in its own directory.
        recorded = Path(env['BORG_ERRANDS_PLAN'])
        copy = case_dir / 'errands_plan.txt' if case_dir else None
        path = copy if copy and copy.exists() else (recorded if recorded.is_absolute() else ROOT / recorded)
        env['BORG_ERRANDS_PLAN'] = str(path)
        want = config.get('borg_errands_plan_sha256')
        have = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if not want or have != want:
            raise SystemExit(f'rerun-death: the run read errands plan {path} ({str(want)[:12]}); '
                             f'here it is {"missing" if have is None else have[:12]}')
    return env


# borg-zoo's runner (zoo/borgrs.py config_text/command): the settings it
# forces before the profile's, and the argument form of a value.
ZOO_FORCED = ('borg_respawn_race', 'borg_respawn_class', 'borg_cheat_death', 'borg_respawn_winners')
# Match borg-zoo's WORLD_LINE. The Zoo adapter consumes this setting.
ZOO_WORLD_LINE = re.compile(r'^[ \t]*borg_world[ \t]*=[ \t]*\S*[ \t]*\n?', re.M)
# Observation-only record paths a retained-evidence or town-shadow Zoo cell
# set (zoo/borgrs.py run_cell); config.txt names them in zoo_record_streams.
ZOO_RECORD_STREAMS = {'BORG_TOWN_PLAN_RECORD': 'town-plan.jsonl', 'BORG_TRIP_RECORD': 'trip.jsonl'}


def zoo_override(text, name, value):
    """borg-zoo catalogue._override: replace the setting's line, else add it."""
    line = f'{name} = {value}'
    pattern = re.compile(rf'^[ \t]*{re.escape(name)}[ \t]*=.*$', re.M)
    if pattern.search(text):
        return pattern.sub(lambda _: line, text)
    marker = '[BEGIN FORMULA SECTION]'
    if marker in text:
        return text.replace(marker, line + '\n\n' + marker, 1)
    return text.rstrip('\n') + '\n' + line + '\n'


def zoo_plan(config, case_dir, race, cls):
    """A Zoo cell's borg.txt settings and plan, from its config.txt."""
    if config.get('borg_world') not in (None, '', 'none'):
        raise SystemExit('rerun-death: Zoo replay cannot restore the recorded custom world '
                         f'{config["borg_world"]}')
    settings, plan_file, scary_file = {}, None, None
    for name, value in config.items():
        if not name.startswith('borg_') or name.endswith('_sha256') or name == 'borg_world':
            continue
        if name == 'borg_scary_list' and value in ('', 'none'):
            settings[name] = value  # the compiled C list: no file (borg-zoo#228)
            continue
        if name == 'borg_scary_list':
            # borg-zoo#228: the named scary list the cell read as user/NAME.
            scary_file = case_dir / 'scary_list.txt'
            want = config.get('scary_list_sha256')
            if not want:
                raise SystemExit('rerun-death: the Zoo cell read a scary list, but config.txt records no '
                                 'scary_list_sha256: the list cannot be verified')
            have = hashlib.sha256(scary_file.read_bytes()).hexdigest() if scary_file.exists() else None
            if have != want:
                raise SystemExit(f'rerun-death: the Zoo cell read scary list {want[:12]} (expected); '
                                 f'the dossier copy is {"missing" if have is None else have[:12]} (actual)')
            settings[name] = value
            continue
        if name == 'borg_errands_plan':
            # Zoo's profile names it borg_plan; the cell got it as user/NAME.
            plan_file = case_dir / 'errands_plan.txt'
            # Zoo dossiers record the hash as errands_plan_sha256 (borg-zoo
            # zoo/deaths.py, and the 58 hand-made Zoo dossiers); the harness
            # path's key, borg_errands_plan_sha256, is accepted too.
            want = config.get('errands_plan_sha256') or config.get('borg_errands_plan_sha256')
            if not want:
                raise SystemExit('rerun-death: the Zoo cell read an errands plan, but config.txt records '
                                 'no plan hash (errands_plan_sha256): the plan cannot be verified')
            have = hashlib.sha256(plan_file.read_bytes()).hexdigest() if plan_file.exists() else None
            if have != want:
                raise SystemExit(f'rerun-death: the Zoo cell read errands plan {want[:12]} (expected); '
                                 f'the dossier copy is {"missing" if have is None else have[:12]} (actual)')
            settings['borg_plan'] = Path(value).name
        else:
            settings[name] = value
    forced = dict(zip(ZOO_FORCED, (str(race), str(cls), 'FALSE', 'FALSE')))
    streams = [name for name in config.get('zoo_record_streams', '').split(',') if name]
    unknown = sorted(set(streams) - set(ZOO_RECORD_STREAMS))
    if unknown:
        raise SystemExit(f'rerun-death: unknown Zoo record streams {", ".join(unknown)}')
    return {'forced': forced, 'settings': settings, 'plan_file': plan_file, 'scary_file': scary_file, 'streams': streams,
            'borg_txt_sha256': config.get('borg_txt_sha256'),
            'turns': int(config['turns']), 'exact': config.get('exact_turns') == '1'}


def zoo_borg_txt(zoo, source):
    text = (source / 'harness/borg.txt').read_text()
    for name, value in list(zoo['forced'].items()) + sorted(zoo['settings'].items()):
        text = zoo_override(text, name, value)
    text = ZOO_WORLD_LINE.sub('', text)
    have = hashlib.sha256(text.encode()).hexdigest()
    if have != zoo['borg_txt_sha256']:
        raise SystemExit(f"rerun-death: rebuilt borg.txt is {have[:12]}, the Zoo cell's was "
                         f"{str(zoo['borg_txt_sha256'])[:12]}: its settings cannot be restored from config.txt")
    return text


def plan(case_dir):
    """What to run for a dossier: (seed, race, class, cap, flags, profile, expected keys hash, source)."""
    record = json.loads((case_dir / 'record.json').read_text())
    if record.get('schema') != 'borg-reborn-rs/death-record@1':
        raise SystemExit(f'rerun-death: {case_dir.name} is not a harness dossier ({record.get("schema")}); '
                         'only tools/export-death.py dossiers can be rerun')
    ident, term = record['identity'], record['terminal']
    if ident.get('impl') != 'rust':
        raise SystemExit(f'rerun-death: {case_dir.name} is a {ident.get("impl")} death; only the Rust Borg is built here')
    config = read_kv(case_dir / 'config.txt')
    for name in ('config.txt', 'summary.json', 'params.json'):
        checked_hash(case_dir, record, config, name)
    flags = config.get('flags', ident.get('flags') or '-')
    # Requested indices: the run's own (summary.json), not the played ones.
    summary = json.loads((case_dir / 'summary.json').read_text())
    # A loaded save (save=NAME, or -load among the extra options) starts
    # another game than the seed's: the dossier alone cannot replay it.
    if 'save=' in flags or 'save_sha256' in config or summary.get('loaded'):
        raise SystemExit(f'rerun-death: {case_dir.name} loaded a save; it cannot be rerun from the dossier alone')
    race = summary.get('race_idx', term.get('race_idx'))
    cls = summary.get('class_idx', term.get('class_idx'))
    zoo = zoo_plan(config, case_dir, race, cls) if 'zoo_profile' in config else None
    overrides, params_hash = parameter_environment(case_dir, record, config)
    # The native receipt decides a record that names no controller: it is a
    # native run even when the harness that made it predates #607.
    core = controller(config, zoo is not None, bool(params_hash))
    original = [attempt for attempt in record['attempts'] if attempt.get('role') == 'original']
    if not original:  # oldest records predate the explicit role field
        original = record['attempts'][:1]
    if len(original) != 1:
        raise SystemExit('rerun-death: expected one original attempt')
    expected_streams = dict(original[0].get('raw_sha256', {}))
    expected_streams.setdefault('keys.log', original[0]['result_sha256'])
    if expected_streams['keys.log'] != original[0]['result_sha256']:
        raise SystemExit('rerun-death: contradictory original key hashes')
    return {
        'seed': ident['seed'] if ident.get('seed') is not None else summary.get('seed'),
        'race': race,
        'class': cls,
        'zoo': zoo,
        # The death came before this cap: the rerun stops there or earlier.
        'cap': int(term.get('turn') or summary.get('game_turns')) + 1,
        'flags': flags.replace('exact', '').replace(',,', ',').strip(',') or '-',
        'profile': config.get('profile'),
        'keys_sha256': original[0]['result_sha256'],
        'streams': expected_streams,
        'core': core,
        'params_core_sha256': params_hash,
        'config': config,
        'terminal': term,
        'record': record,
        'env': overrides if zoo else dict(settings(config, case_dir), BORG_CORE=core, **overrides),
        'source_sha256': ident.get('source_sha256'),
        'git_rev': ident.get('git_rev'),
        'binary_sha256': ident.get('binary_sha256'),
    }


def stage_zoo_config(run, text, yaml_sha, revision=None):
    if not yaml_sha:
        (run / 'user/borg.txt').write_text(text)
        return
    converter = ROOT / 'harness/pborg-config.py'
    repair = f"check out {revision or 'the death’s revision'} in {ROOT} and run harness/build.sh"
    if not converter.is_file():
        raise SystemExit(f'rerun-death: missing {converter}. {repair}.')
    try:
        yaml = subprocess.check_output([sys.executable, str(converter), '-'], input=text.encode('utf-8'))
    except (OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f'rerun-death: failed to convert PBorg settings. {repair}.') from error
    if hashlib.sha256(yaml).hexdigest() != yaml_sha:
        raise SystemExit(f'rerun-death: rebuilt pborg.yaml differs from the recorded configuration. {repair}.')
    (run / 'pborg-legacy.txt').write_bytes(text.encode('utf-8'))
    (run / 'user/pborg.yaml').write_bytes(yaml)


def run_zoo(p, out, logs_env, checkpoint_every, extra=()):
    """Start the game as borg-zoo's runner did (zoo/borgrs.py run_cell/command).
    EXTRA borgh options (e.g. -keys N -screen, scripts/animate_death.py) are
    appended; the caller checks that they leave the key stream unchanged."""
    zoo, run = p['zoo'], out / 'run'
    text = zoo_borg_txt(zoo, ROOT)
    for d in ('user', 'save', 'archive', 'panic', 'scores'):
        (run / d).mkdir(parents=True)
    stage_zoo_config(run, text, p['config'].get('pborg_yaml_sha256'), p.get('git_rev'))
    # Input configuration is retained; effective parameters are independently
    # checked from the controller's newly written params-core.json below.
    (run / 'config.txt').write_text(''.join(f'{k}={v}\n' for k, v in p['config'].items()))
    if zoo['plan_file']:
        shutil.copy(zoo['plan_file'], run / 'user' / zoo['settings']['borg_plan'])
    if zoo.get('scary_file'):
        shutil.copy(zoo['scary_file'], run / 'user' / zoo['settings']['borg_scary_list'])
    game = ROOT / 'build/rust/game'
    cmd = [str(game / 'angband'), '-mborgh', '-n', '-uBorg'] + \
        [f'-d{d}={run / d}' for d in ('user', 'save', 'archive', 'panic', 'scores')] + \
        ['--', '-seed', str(p['seed']), '-race', str(p['race']), '-class', str(p['class']), '-turns', str(zoo['turns']),
         '-keylog', str(run / 'keys.log'), '-summary', str(run / 'summary.json'), '-menu-letters']
    if zoo['exact']:
        cmd.append('-exact-turns')
    cmd += ['-statelog', str(run / 'state.log'), '-msglog', str(run / 'messages.log')]
    if checkpoint_every:
        cmd += ['-checkpoint-every', str(checkpoint_every), '-checkpoint-dir', str(run / 'checkpoints')]
    cmd += [str(x) for x in extra]
    # Zoo cleared every ambient BORG_* variable; only this tool's logs are set.
    env = clean_environment()
    env.update(p['env'])
    env['BORG_RUN_DIR'] = str(run)
    env.update({k: v for k, v in logs_env.items() if k in ('BORG_OBSERVATION_LOG', 'BORG_WORLD_LOG', 'BORG_KNOWLEDGE_LOG')})
    # The cell's own record streams, if it set any, so the rerun is the cell's
    # process configuration and not only its key stream.
    for name in zoo.get('streams', ()):
        env[name] = str(run / ZOO_RECORD_STREAMS[name])
        (run / ZOO_RECORD_STREAMS[name]).touch()
    env.update(TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
    with (run / 'stderr.log').open('w') as err:
        return subprocess.run(cmd, cwd=game, env=env, stdout=subprocess.DEVNULL, stderr=err, text=True)


def configuration_hash(p, name):
    values = [p['config'].get(name), p['record']['identity'].get(name)]
    values = [value for value in values if value]
    if len(set(values)) > 1:
        raise SystemExit(f'rerun-death: contradictory recorded {name}')
    return values[0] if values else None


def verify(p, out):
    """Keys alone cannot qualify a death reproduction (including --any-build)."""
    run = out / 'run'
    errors, streams = [], {}
    for name in ('keys.log', 'state.log', 'messages.log'):
        actual = sha(run / name) if (run / name).is_file() else None
        streams[name] = actual
        if not p['streams'].get(name):
            errors.append(f'no original {name} hash; complete reproduction cannot be verified')
        elif actual != p['streams'][name]:
            errors.append(f'{name} differs or is missing')
    try:
        summary = json.loads((run / 'summary.json').read_text())
        if not isinstance(summary, dict):
            raise ValueError('expected summary object')
        term = p['terminal']
        expected = dict(seed=p['seed'], dead=True, stop_reason='death', loaded=False,
                        game_turns=term['turn'])
        expected.update({key: term[value] for key, value in (
            ('death_cause', 'cause'), ('depth', 'depth'), ('max_depth', 'max_depth'), ('clevel', 'level'))
                         if term.get(value) is not None})
        for key, value in expected.items():
            if type(summary.get(key)) is not type(value) or summary.get(key) != value:
                errors.append(f'death endpoint differs: {key}')
        for key in ('race_idx', 'class_idx'):
            if summary.get('played_' + key, summary.get(key)) != term.get(key):
                errors.append(f'death endpoint differs: {key}')
    except (OSError, ValueError, KeyError, TypeError):
        summary = {}
        errors.append('missing or invalid terminal summary')
    actual_config = read_kv(run / 'config.txt')
    if not actual_config:
        errors.append('missing run/config.txt')
    legacy_path = 'pborg-legacy.txt' if actual_config.get('pborg_yaml_sha256') else 'user/borg.txt'
    for key, filename in (('borg_txt_sha256', legacy_path), ('pborg_yaml_sha256', 'user/pborg.yaml'),
                          ('profile_sha256', None)):
        expected = configuration_hash(p, key)
        if expected:
            if actual_config.get(key) != expected:
                errors.append(f'effective configuration differs: {key}')
            if filename and (not (run / filename).is_file() or sha(run / filename) != expected):
                errors.append(f'actual {filename} differs or is missing')
    # The effective controller of the replay: the run's own config names it,
    # and the run's own native receipt settles a config that names none.
    ran_native = (run / 'params-core.json').is_file()
    if controller(actual_config, p['zoo'] is not None, ran_native) != p['core']:
        errors.append('effective controller differs')
    if p['core'] == 'borg-rs':
        required = [run / 'params-core.json', run / 'trace-core.jsonl']
        if not p['params_core_sha256']:
            errors.append('no original native parameter receipt; native replay cannot be qualified')
        elif not required[0].is_file() or sha(required[0]) != p['params_core_sha256']:
            errors.append('effective native parameter values/origins differ')
    else:
        required = [out / name for name in ('observations.jsonl', 'worlds.txt', 'knowledge.json')]
        expected = p['record'].get('files_sha256', {}).get('params.json')
        if expected and (not (run / 'params.json').is_file() or sha(run / 'params.json') != expected):
            errors.append('effective reborn parameters differ')
    for path in required:
        if not path.is_file() or not path.stat().st_size:
            errors.append(f'missing {p["core"]} log: {path.name}')
    return errors, streams, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case', type=Path)
    ap.add_argument('out', type=Path)
    ap.add_argument('--checkpoint-every', type=int, default=0)
    ap.add_argument('--any-build', action='store_true')
    ap.add_argument('--source-root', type=Path, help='exact source checkout that owns the build/harness')
    a = ap.parse_args(argv)
    global ROOT
    if a.source_root:
        ROOT = a.source_root.resolve()
    # run.sh runs in its own directory: relative paths would land elsewhere.
    a.case, a.out = a.case.resolve(), a.out.resolve()
    p = plan(a.case)
    build = read_kv(ROOT / 'build/rust/BUILD_ID')
    if (not p['source_sha256'] or build.get('source_sha256') != p['source_sha256']) and not a.any_build:
        raise SystemExit(f"rerun-death: build/rust is source {str(build.get('source_sha256'))[:12]}, the death's is "
                         f"{str(p['source_sha256'])[:12]}: check out {p['git_rev']} and run harness/build.sh "
                         '(or pass --any-build: then the rerun is not a reproduction)')
    binary = ROOT / 'build/rust/game/angband'
    before = sha(binary) if binary.is_file() else None
    if p['binary_sha256'] and before != p['binary_sha256'] and not a.any_build:
        raise SystemExit('rerun-death: executable differs from the recorded binary; rebuild the exact source '
                         'or use --any-build for a diagnostic only')
    for key in ('borg_txt_sha256', 'profile_sha256'):
        expected = configuration_hash(p, key)
        if key == 'profile_sha256' and expected:
            profile = ROOT / p['profile'] if p['profile'] else None
            if not profile or not profile.is_file() or sha(profile) != expected:
                raise SystemExit('rerun-death: recorded profile differs or is missing')
    if a.out.exists():
        raise SystemExit(f'rerun-death: {a.out} exists')
    a.out.mkdir(parents=True)
    # The build checked above, never an inherited ANGBAND_BIN.
    env = clean_environment()
    # The run's own settings, never inherited ones.
    env.update(p['env'])
    env.update(BORG_IMPL='rust', BORG_DEATH_RECORDS_DIR=str(a.out / 'not-exported'),
               CHECKPOINT_EVERY=str(a.checkpoint_every))
    if p['core'] == 'reborn':
        env.update(BORG_OBSERVATION_LOG=str(a.out / 'observations.jsonl'),
                   BORG_WORLD_LOG=str(a.out / 'worlds.txt'),
                   BORG_KNOWLEDGE_LOG=str(a.out / 'knowledge.json'))
    receipt = dict(schema='borg-cemetery/death-rerun@1', core=p['core'], independent_life=False,
                   record_sha256=sha(a.case / 'record.json'), source_sha256=build.get('source_sha256'),
                   binary_sha256_before=before, status='failed', reproduction_verified=False,
                   diagnostic=a.any_build)
    try:
        if p['zoo']:
            r = run_zoo(p, a.out, env, a.checkpoint_every)
        else:
            if p['profile']:
                env['BORG_PROFILE'] = str(ROOT / p['profile'])
            cmd = [str(ROOT / 'harness/run.sh'), str(a.out / 'run'), str(p['seed']), str(p['race']), str(p['class']),
                   str(p['cap']), p['flags']]
            r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        errors, streams, summary = verify(p, a.out)
        if not p['binary_sha256'] or not before:
            errors.append('missing original or actual executable identity; reproduction cannot be verified')
        after = sha(binary) if binary.is_file() else None
        if after != before:
            errors.append('executable changed during the rerun')
        if r.returncode:
            errors.append(f'launcher failed with return code {r.returncode}')
        receipt.update(returncode=r.returncode, streams=streams, terminal=summary,
                       binary_sha256_after=after, errors=errors)
        receipt['reproduction_verified'] = not errors and not a.any_build
        receipt['status'] = 'diagnostic' if a.any_build else ('reproduced' if not errors else 'mismatch')
    except (OSError, ValueError, SystemExit) as error:
        receipt['errors'] = [str(error)]
    (a.out / 'reproduction.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(f"{a.case.name}: {receipt['status']}; core={p['core']}; reproduction_verified="
          f"{receipt['reproduction_verified']}; logs in {a.out}")
    for error in receipt.get('errors', []):
        print('rerun-death: ' + error, file=sys.stderr)
    return 0 if not receipt.get('errors') else 1


if __name__ == '__main__':
    sys.exit(main())
