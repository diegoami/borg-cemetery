import json,sys
S='/tmp/claude-0/-home-user/2add62db-0818-573c-8b91-ab7e03086156/scratchpad'
ref=sys.argv[1]
R={r['seed']:r for r in json.load(open(f'{S}/arms/{ref}.json'))}
def div(a,b):
    la=open(a).read().splitlines(); lb=open(b).read().splitlines()
    for i,(x,y) in enumerate(zip(la,lb)):
        if x!=y: return int(la[i].split()[0])
    return None if len(la)==len(lb) else int(la[min(len(la),len(lb))-1].split()[0])
for arm in sys.argv[2:]:
    res=json.load(open(f'{S}/arms/{arm}.json'))
    out=[];c={'saved':0,'killed':0,'same':0,'both_dead_diff':0,'both_alive':0}
    for r in res:
        b=R[r['seed']]; t=div(f"{S}/arms/{ref}/{r['seed']}/keys.log",f"{S}/arms/{arm}/{r['seed']}/keys.log")
        if t is None: c['same']+=1; continue
        k='saved' if b['dead'] and not r['dead'] else 'killed' if r['dead'] and not b['dead'] else 'both_dead_diff' if r['dead'] else 'both_alive'
        c[k]+=1
        if k!='both_alive': out.append(f"   {r['seed']} {r['char']}: {k} (ref {'dead t'+str(b['turn']) if b['dead'] else 'alive'}; arm {('dead t'+str(r['turn'])+' '+str(r['cause'])) if r['dead'] else 'alive CL'+str(r['cl'])+' DL'+str(r['dl'])}; diverges t{t})")
    print(f"{arm} vs {ref}: deaths {sum(r['dead'] for r in res)} | same game {c['same']}, saved {c['saved']}, newly killed {c['killed']}, both dead differently {c['both_dead_diff']}, both alive differently {c['both_alive']}")
    print('\n'.join(out))
