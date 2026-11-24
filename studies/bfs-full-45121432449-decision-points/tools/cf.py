"""Counterfactual replays: play a seed from birth with edited borg.txt params.
cf.py ARMS_JSON JOBS_JSON OUT_JSONL --game DIR --work DIR [-j N]
ARMS_JSON: {"arm": {"param": value, ...}}; JOBS_JSON: [{"seed","race","cls","profile","template","play_sha256"}]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from div2 import CAP, replay_outcome

def play(job, arm, params, game, work):
    w = Path(work).resolve() / arm / f"{job['profile']}-{job['seed']}"
    shutil.rmtree(w, ignore_errors=True)
    for d in ('user', 'save', 'archive', 'panic', 'scores', 'record'):
        (w / d).mkdir(parents=True)
    t = Path(job['template'])
    for f in t.iterdir():
        if f.suffix in ('.txt', '.prf') and f.name not in ('CharOutput.txt', 'lore.txt'):
            shutil.copy2(f, w / 'user' / f.name)
    txt = (w / 'user/borg.txt').read_text()
    txt = re.sub(r'(?m)^borg_respawn_race = .*$', f"borg_respawn_race = {job['race']}", txt)
    txt = re.sub(r'(?m)^borg_respawn_class = .*$', f"borg_respawn_class = {job['cls']}", txt)
    for k, v in params.items():
        line = f'borg_param_{k} = {v}'
        txt, n = re.subn(rf'(?m)^borg_param_{k} = .*$', line, txt)
        if n == 0:
            txt += f'\n{line}\n'
    (w / 'user/borg.txt').write_text(txt)
    env = {k: v for k, v in os.environ.items() if not k.startswith('BORG_')} | {'TZ': 'UTC', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
    command = [
        './angband', '-mborgh', '-n', '-uPlayer', f'-duser={w}/user',
        f'-dsave={w}/save', f'-darchive={w}/archive', f'-dpanic={w}/panic',
        f'-dscores={w}/scores', '--', '-seed', str(job['seed']), '-race', str(job['race']),
        '-class', str(job['cls']), '-turns', str(CAP), '-keylog', f'{w}/keys.log',
        '-summary', f'{w}/summary.json', '-menu-letters', '-exact-turns',
        '-msglog', f'{w}/messages.log', '-statelog', f'{w}/state.log',
    ]
    with (w / 'stderr.log').open('wb') as stderr:
        subprocess.run(command, cwd=game, env=env, stdout=subprocess.DEVNULL,
                       stderr=stderr, timeout=3600, check=True)
    summary = json.loads((w / 'summary.json').read_text())
    if not isinstance(summary, dict) or replay_outcome(summary) == 'failed':
        raise ValueError(f'unexpected replay endpoint: {summary}')
    stream_hashes = {}
    for stream in ('keys.log', 'messages.log', 'state.log'):
        stream_path = w / stream
        stream_hashes[stream] = hashlib.sha256(stream_path.read_bytes()).hexdigest()
    return {
        'same_play': stream_hashes['keys.log'] == job['play_sha256'],
        'summary': summary,
        'stream_sha256': stream_hashes,
        'borg_txt_sha256': hashlib.sha256((w / 'user/borg.txt').read_bytes()).hexdigest(),
    }


def run(job, arm, params, game, work):
    row = {key: job[key] for key in ('seed', 'profile', 'race', 'cls')}
    row['arm'] = arm
    try:
        row.update(play(job, arm, params, game, work))
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        row.update(same_play=False, summary={}, error=str(error))
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arms', type=Path)
    parser.add_argument('jobs', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--game', required=True)
    parser.add_argument('--work', required=True)
    parser.add_argument('-j', type=int, default=4)
    args = parser.parse_args()
    arms = json.loads(args.arms.read_text())
    jobs = json.loads(args.jobs.read_text())
    done = set()
    failed = False
    if args.out.exists():
        for line in args.out.read_text().splitlines():
            row = json.loads(line)
            done.add((row['arm'], row['profile'], row['seed']))
            failed |= bool(row.get('error')) or replay_outcome(row['summary']) == 'failed'
    todo = [(job, arm, params) for arm, params in arms.items() for job in jobs
            if (arm, job['profile'], job['seed']) not in done]
    with ThreadPoolExecutor(args.j) as pool, args.out.open('a') as output:
        for row in pool.map(lambda item: run(*item, args.game, args.work), todo):
            output.write(json.dumps(row) + '\n')
            output.flush()
            outcome = row.get('error') or replay_outcome(row['summary'])
            print(row['arm'], row['profile'], row['seed'], outcome, flush=True)
            failed |= 'error' in row
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
