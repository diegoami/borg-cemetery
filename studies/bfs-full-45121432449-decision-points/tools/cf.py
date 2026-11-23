"""Counterfactual replays: play a seed from birth with edited borg.txt params.
cf.py ARMS_JSON JOBS_JSON OUT_JSONL --game DIR --work DIR [-j N]
ARMS_JSON: {"arm": {"param": value, ...}}; JOBS_JSON: [{"seed","race","cls","profile","template","play_sha256"}]
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def run(job, arm, params, game, work):
    w = Path(work) / arm / f"{job['profile']}-{job['seed']}"
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
    subprocess.run(['./angband', '-mborgh', '-n', '-uPlayer', f'-duser={w}/user', f'-dsave={w}/save', f'-darchive={w}/archive',
                    f'-dpanic={w}/panic', f'-dscores={w}/scores', '--', '-seed', str(job['seed']), '-race', str(job['race']),
                    '-class', str(job['cls']), '-turns', '100000', '-keylog', f'{w}/keys.log', '-summary', f'{w}/summary.json',
                    '-menu-letters', '-exact-turns', '-msglog', f'{w}/messages.log', '-statelog', f'{w}/state.log'],
                   cwd=game, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
    s = json.loads((w / 'summary.json').read_text()) if (w / 'summary.json').exists() else {}
    sha = hashlib.sha256((w / 'keys.log').read_bytes()).hexdigest() if (w / 'keys.log').exists() else None
    return dict(arm=arm, seed=job['seed'], profile=job['profile'], race=job['race'], cls=job['cls'],
                same_play=(sha == job.get('play_sha256')), summary=s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arms'); ap.add_argument('jobs'); ap.add_argument('out')
    ap.add_argument('--game', required=True); ap.add_argument('--work', required=True); ap.add_argument('-j', type=int, default=4)
    a = ap.parse_args()
    arms = json.load(open(a.arms)); jobs = json.load(open(a.jobs))
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            r = json.loads(l); done.add((r['arm'], r['profile'], r['seed']))
    todo = [(j, arm, p) for arm, p in arms.items() for j in jobs if (arm, j['profile'], j['seed']) not in done]
    with ThreadPoolExecutor(a.j) as ex, open(a.out, 'a') as out:
        for r in ex.map(lambda x: run(x[0], x[1], x[2], a.game, a.work), todo):
            out.write(json.dumps(r) + '\n'); out.flush()
            print(r['arm'], r['profile'], r['seed'], r['same_play'], {k: r['summary'].get(k) for k in ('stop_reason', 'game_turns', 'death_cause', 'clevel', 'depth')}, flush=True)

main()
