#!/usr/bin/env python3
"""arm.py NAME 'k=v,k=v' [seeds...]  -> replay the death seeds from birth with borg.txt overrides, 100k turns."""
import sys,os,json,re,shutil,subprocess,hashlib
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user/2add62db-0818-573c-8b91-ab7e03086156/scratchpad'
GAME=sys.argv[4] if len(sys.argv)>4 and os.path.isdir(sys.argv[4]) else f'{S}/W/src/build/recorder/game'
name=sys.argv[1]; ov=dict(kv.split('=',1) for kv in sys.argv[2].split(',') if kv)
seeds=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] else sorted(os.listdir(f'{S}/W/d'))
env={k:v for k,v in os.environ.items() if not k.startswith('BORG_')}|{'TZ':'UTC','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
def run(seed):
    b=f'{S}/W/d/{seed}'; z=json.load(open(f'{b}/zoo-death.json'))
    cfg=dict(l.split('=',1) for l in open(f'{b}/config.txt').read().split() if '=' in l)
    w=f'{S}/arms/{name}/{seed}'; shutil.rmtree(w,ignore_errors=True)
    for d in ('user','save','archive','panic','scores'): os.makedirs(f'{w}/{d}')
    for f in os.listdir(f'{b}/user'):
        if f.endswith('.txt') and f not in ('CharOutput.txt','lore.txt'): shutil.copy2(f'{b}/user/{f}',f'{w}/user/{f}')
    src=os.environ.get('HARNESS')
    if src:
        shutil.copy2(f'{src}/scary_monsters.txt',f'{w}/user/scary_monsters.txt')
        txt=open(f'{src}/borg.txt').read()
        txt=re.sub(r'^borg_respawn_race = .*$',f"borg_respawn_race = {cfg['race_idx']}",txt,flags=re.M)
        txt=re.sub(r'^borg_respawn_class = .*$',f"borg_respawn_class = {cfg['class_idx']}",txt,flags=re.M)
    else:
        txt=open(f'{w}/user/borg.txt').read()
    for k,v in ov.items():
        key=k if k.startswith('borg_') else 'borg_param_'+k
        pat=re.compile(rf'^{re.escape(key)}\s*=.*$',re.M)
        txt=pat.sub(f'{key} = {v}',txt) if pat.search(txt) else txt+f'\n{key} = {v}\n'
    open(f'{w}/user/borg.txt','w').write(txt)
    subprocess.run(['./angband','-mborgh','-n','-uPlayer',f'-duser={w}/user',f'-dsave={w}/save',f'-darchive={w}/archive',f'-dpanic={w}/panic',f'-dscores={w}/scores','--',
        '-seed',seed,'-race',cfg['race_idx'],'-class',cfg['class_idx'],'-turns',cfg.get('turns','100000'),'-keylog',f'{w}/keys.log','-summary',f'{w}/summary.json','-menu-letters','-exact-turns','-msglog',f'{w}/messages.log'],
        cwd=GAME,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=3000)
    s=json.load(open(f'{w}/summary.json'))
    same=hashlib.sha256(open(f'{w}/keys.log','rb').read()).hexdigest()==z['play_sha256']
    return dict(seed=int(seed),dead=s['dead'],cause=s.get('death_cause'),turn=s['game_turns'],cl=s['max_clevel'],dl=s['max_depth'],same=same,char=z['character'])
with ThreadPoolExecutor(4) as ex: res=list(ex.map(run,seeds))
json.dump(res,open(f'{S}/arms/{name}.json','w'))
for r in res: print(f"{name} {r['seed']:>10} {r['char']:<22} {'DEAD '+str(r['cause'])[:28] if r['dead'] else 'alive':<34} t{r['turn']:<6} CL{r['cl']} DL{r['dl']} {'IDENTICAL' if r['same'] else ''}")
print(name,'deaths',sum(r['dead'] for r in res),'of',len(res))
