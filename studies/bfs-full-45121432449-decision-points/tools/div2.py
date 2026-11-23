import sys,json,collections
# div2.py RESULTS.jsonl... : per arm, changed death games with divergence turn, base death turn, class near/early
NEAR=2000
rows=[]
for f in sys.argv[1:]:
    for l in open(f): rows.append(json.loads(l))
summ=collections.defaultdict(lambda: collections.Counter())
for r in rows:
    tag='ctl' if r['profile'].endswith('ctl') else 'bfs0'
    try: bk=open(f"D/{r['seed']}_{tag}/keys.log").read().splitlines()
    except FileNotFoundError: continue
    s=r['summary']; arm=r['arm']
    if r['same_play']:
        summ[arm]['identical']+=1; continue
    ck=open(f"cfw/{arm}/{r['profile']}-{r['seed']}/keys.log").read().splitlines()
    i=next((k for k,(a,b) in enumerate(zip(bk,ck)) if a!=b),min(len(bk),len(ck)))
    dt=int(bk[min(i,len(bk)-1)].split()[0]); death=int(bk[-1].split()[0])
    near=death-dt<=NEAR
    out='lives' if s.get('stop_reason')!='death' else f"dies t{s.get('game_turns')} ({s.get('death_cause')})"
    summ[arm][('near ' if near else 'early ')+('lives' if out=='lives' else 'dies')]+=1
    print(f"{arm:9} {r['seed']:>10} {tag:4} diverge t{dt:>6} death t{death:>6} {'NEAR ' if near else 'early'} -> {out}")
print()
for a,c in summ.items(): print(a, dict(c))
