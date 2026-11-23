import json,collections
NEAR=2000
arms=['p934','flee100','flee1','osc','bundle','conf','phase50','phasefear','recall0']
cells=[json.loads(l) for l in open('cells.jsonl')]
deaths=[r for r in cells if r['outcome']=='death']
deaths.sort(key=lambda r:(r['cause']!='poison',r['profile'],r['seed']))
res={}
for f in ['cf-deaths.jsonl','cf-deaths2.jsonl']:
    for l in open(f):
        r=json.loads(l); res.setdefault((r['arm'],r['profile'],r['seed']),r)
def code(arm,d):
    r=res.get((arm,d['profile'],d['seed']))
    if r is None: return '?'
    if r['same_play']: return '='
    tag='ctl' if d['profile'].endswith('ctl') else 'bfs0'
    bk=open(f"D/{d['seed']}_{tag}/keys.log").read().splitlines()
    ck=open(f"cfw/{arm}/{d['profile']}-{d['seed']}/keys.log").read().splitlines()
    i=next((k for k,(a,b) in enumerate(zip(bk,ck)) if a!=b),min(len(bk),len(ck)))
    dt=int(bk[min(i,len(bk)-1)].split()[0]); death=int(bk[-1].split()[0])
    near=death-dt<=NEAR; lives=r['summary'].get('stop_reason')!='death'
    return ('**L**' if lives else 'D') if near else ('l' if lives else 'd')
print('| seed | arm | killer | '+' | '.join(arms)+' |')
print('|---:|---|---|'+'|'.join(':-:' for _ in arms)+'|')
tot=collections.Counter()
for d in deaths:
    cs=[code(a,d) for a in arms]
    for a,c in zip(arms,cs): tot[(a,c)]+=1
    print(f"| {d['seed']} | {d['profile'][11:]} | {d['cause']} | "+' | '.join(cs)+' |')
for c,name in [('**L**','lives, diverged ≤ 2,000 game turns before the death'),('D','still dies, diverged near'),('l','lives, diverged earlier'),('d','dies, diverged earlier'),('=','identical play')]:
    print(f"| {c} | | {name} | "+' | '.join(str(tot[(a,c)]) for a in arms)+' |')
