#!/usr/bin/env python3
"""Rerun a recorded death with its logs (task TE.6, #76; docs/SPEC.md §8, §11).

  tools/rerun-death.py docs/deaths/D0664-rust-seed102 OUTDIR [--checkpoint-every N] [--any-build]

A run is deterministic: the same build, seed, character and flags play the
same game. This reruns a dossier's game through harness/run.sh with the
Borg's logs on: the observation of every think, the world model's digest
after each, the knowledge (docs/ENGINE.md), and, with --checkpoint-every,
an engine save every N game turns. It then checks that the key stream
equals the recorded one (record.json's result_sha256), which shows the
rerun is the same game.

The build must be the death's: build/rust/BUILD_ID's source_sha256 equals
the dossier's, else the tool says which commit to check out and build.
--any-build reruns anyway; the result is then not a reproduction.

A Zoo cell (config.txt has zoo_profile) did not go through harness/run.sh:
Zoo wrote user/borg.txt from the source's harness/borg.txt with the
profile's settings and started the game directly. Its rerun rebuilds that
borg.txt from config.txt's borg_* settings, refuses it unless its sha256 is
the recorded borg_txt_sha256, and starts the game with Zoo's arguments.

The run's recorded settings are restored too, including an errands plan:
the dossier's own copy when export-death.py kept one, else the file
config.txt names in the source checkout. A ladders or plan file whose
bytes differ from the recorded sha256 is refused.

OUTDIR gets the run directory (OUTDIR/run: keys, messages, state, summary,
trace, params, checkpoints) and the logs (OUTDIR/observations.jsonl,
worlds.txt, knowledge.json). The rerun's death is not exported to the
registry again (it would be a repeat).
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


def settings(config, case_dir=None):
    """The environment a dossier's run had, from its config.txt. A ladders
    file or errands plan must still be the one the run read."""
    # Empty values too: set but empty is not unset (re-review #227, 6).
    env = {v: config[v.lower()] for v in SETTINGS if v.lower() in config}
    if env.get('BORG_LADDERS'):
        path = Path(env['BORG_LADDERS'])
        want = config.get('borg_ladders_sha256')
        have = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if have != want:
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
        if have != want:
            raise SystemExit(f'rerun-death: the run read errands plan {path} ({str(want)[:12]}); '
                             f'here it is {"missing" if have is None else have[:12]}')
    return env


# borg-zoo's runner (zoo/borgrs.py config_text/command): the settings it
# forces before the profile's, and the argument form of a value.
ZOO_FORCED = ('borg_respawn_race', 'borg_respawn_class', 'borg_cheat_death', 'borg_respawn_winners')


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
    settings, plan_file = {}, None
    for name, value in config.items():
        if not name.startswith('borg_') or name.endswith('_sha256'):
            continue
        if name == 'borg_errands_plan':
            # Zoo's profile names it borg_plan; the cell got it as user/NAME.
            plan_file = case_dir / 'errands_plan.txt'
            want = config.get('errands_plan_sha256') or config.get('borg_errands_plan_sha256')
            have = hashlib.sha256(plan_file.read_bytes()).hexdigest() if plan_file.exists() else None
            if have != want:
                raise SystemExit(f'rerun-death: the Zoo cell read errands plan {str(want)[:12]}; '
                                 f'the dossier copy is {"missing" if have is None else have[:12]}')
            settings['borg_plan'] = Path(value).name
        else:
            settings[name] = value
    forced = dict(zip(ZOO_FORCED, (str(race), str(cls), 'FALSE', 'FALSE')))
    return {'forced': forced, 'settings': settings, 'plan_file': plan_file,
            'borg_txt_sha256': config.get('borg_txt_sha256'),
            'turns': int(config['turns']), 'exact': config.get('exact_turns') == '1'}


def zoo_borg_txt(zoo, source):
    text = (source / 'harness/borg.txt').read_text()
    for name, value in list(zoo['forced'].items()) + sorted(zoo['settings'].items()):
        text = zoo_override(text, name, value)
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
    return {
        'seed': ident['seed'] if ident.get('seed') is not None else summary.get('seed'),
        'race': race,
        'class': cls,
        'zoo': zoo,
        # The death came before this cap: the rerun stops there or earlier.
        'cap': int(term.get('turn') or summary.get('game_turns')) + 1,
        'flags': flags.replace('exact', '').replace(',,', ',').strip(',') or '-',
        'profile': config.get('profile'),
        'keys_sha256': record['attempts'][0]['result_sha256'],
        'env': {} if zoo else settings(config, case_dir),
        'source_sha256': ident.get('source_sha256'),
        'git_rev': ident.get('git_rev'),
    }


def run_zoo(p, out, logs_env, checkpoint_every):
    """Start the game as borg-zoo's runner did (zoo/borgrs.py run_cell/command)."""
    zoo, run = p['zoo'], out / 'run'
    text = zoo_borg_txt(zoo, ROOT)
    for d in ('user', 'save', 'archive', 'panic', 'scores'):
        (run / d).mkdir(parents=True)
    (run / 'user/borg.txt').write_text(text)
    if zoo['plan_file']:
        shutil.copy(zoo['plan_file'], run / 'user' / zoo['settings']['borg_plan'])
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
    # Zoo cleared every ambient BORG_* variable; only this tool's logs are set.
    env = {k: v for k, v in os.environ.items() if not k.startswith('BORG_')}
    env.update({k: v for k, v in logs_env.items() if k in ('BORG_OBSERVATION_LOG', 'BORG_WORLD_LOG', 'BORG_KNOWLEDGE_LOG')})
    env.update(TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
    with (run / 'stderr.log').open('w') as err:
        return subprocess.run(cmd, cwd=game, env=env, stdout=subprocess.DEVNULL, stderr=err, text=True)


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
    if build.get('source_sha256') != p['source_sha256'] and not a.any_build:
        raise SystemExit(f"rerun-death: build/rust is source {str(build.get('source_sha256'))[:12]}, the death's is "
                         f"{str(p['source_sha256'])[:12]}: check out {p['git_rev']} and run harness/build.sh "
                         '(or pass --any-build: then the rerun is not a reproduction)')
    if a.out.exists():
        raise SystemExit(f'rerun-death: {a.out} exists')
    a.out.mkdir(parents=True)
    # The build checked above, never an inherited ANGBAND_BIN.
    env = {k: v for k, v in os.environ.items() if k != 'ANGBAND_BIN' and k not in SETTINGS}
    # The run's own settings, never inherited ones.
    env.update(p['env'])
    env.update(BORG_IMPL='rust',
               BORG_OBSERVATION_LOG=str(a.out / 'observations.jsonl'),
               BORG_WORLD_LOG=str(a.out / 'worlds.txt'),
               BORG_KNOWLEDGE_LOG=str(a.out / 'knowledge.json'),
               BORG_DEATH_RECORDS_DIR=str(a.out / 'not-exported'),
               CHECKPOINT_EVERY=str(a.checkpoint_every))
    if p['zoo']:
        r = run_zoo(p, a.out, env, a.checkpoint_every)
    else:
        if p['profile']:
            env['BORG_PROFILE'] = str(ROOT / p['profile'])
        cmd = [str(ROOT / 'harness/run.sh'), str(a.out / 'run'), str(p['seed']), str(p['race']), str(p['class']),
               str(p['cap']), p['flags']]
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    keys = a.out / 'run/keys.log'
    got = hashlib.sha256(keys.read_bytes()).hexdigest() if keys.exists() else None
    same = got == p['keys_sha256']
    summary = json.loads((a.out / 'run/summary.json').read_text()) if (a.out / 'run/summary.json').exists() else {}
    print(f"{a.case.name}: rerun {'reproduces' if same else 'DOES NOT reproduce'} the recorded keys "
          f"({str(got)[:12]} vs {p['keys_sha256'][:12]}); {summary.get('stop_reason')} at turn {summary.get('game_turns')}"
          f"{' (' + summary['death_cause'] + ')' if summary.get('death_cause') else ''}")
    missing = [n for n in ('observations.jsonl', 'worlds.txt', 'knowledge.json')
               if not (a.out / n).exists() or not (a.out / n).stat().st_size]
    if missing and p['zoo'] and p['zoo']['settings'].get('borg_reborn_core') == 'borg-rs':
        # Those logs are the reborn Borg's; the borg-rs core writes none.
        print('rerun-death: the borg-rs core played this run; it writes no observation/world/knowledge logs')
        missing = []
    if missing:
        print(f"rerun-death: no logs written: {', '.join(missing)}", file=sys.stderr)
    print(f'logs in {a.out}')
    if r.returncode and not same:
        log = a.out / 'run/stderr.log'
        sys.stderr.write((r.stderr or (log.read_text(errors='replace') if log.exists() else ''))[-2000:])
    return 0 if (same or a.any_build) and not missing else 1


if __name__ == '__main__':
    sys.exit(main())
