import json,sys,re,os
S=sys.argv[1]
for name in sorted(os.listdir(S)):
    d=S+'/'+name
    if not os.path.isdir(d) or name.endswith('none'): continue
    sm=json.load(open(d+'/summary.json'))
    err=open(d+'/stderr.log').read().splitlines()
    inj=[l for l in err if l.startswith('inject:')]
    armed=[l for l in inj if 'armed' in l]
    back=[l for l in inj if 'handing back' in l]
    t0=int(re.search(r'turn (\d+)',armed[0]).group(1)) if armed else None
    foe='crow' if name.startswith('N') else 'white jelly'
    msgs=[l.rstrip('\n').split(' ',3) for l in open(d+'/messages.log')]
    msgs=[m for m in msgs if len(m)==4]
    after=[m for m in msgs if t0 is not None and int(m[1])>=t0]
    end=next((m for m in after if re.search(foe+' (dies|flees)|destroyed the '+foe+'|slain the '+foe,m[3])),None)
    hits=[m for m in after if re.search(r'^(You hit|Your Flask of oil hits|You miss) the '+foe,m[3])]
    # HP over the fight window from state.log
    st=[l.split() for l in open(d+'/state.log')]
    hp=[(int(x[0]),int(x[3][2:].split('/')[0])) for x in st if t0 and t0<=int(x[0])<=t0+400]
    mn=min(hp,key=lambda z:z[1]) if hp else None
    out=f"{name:22s} armed:{t0} handback:{re.search(r'turn (\d+) hp (-?\d+)',back[0]).groups() if back else None} foe_end:{(end[1],end[3]) if end else None} min_hp_400t:{mn} dead:{sm['dead']} turn:{sm['game_turns']} cause:{sm.get('death_cause')} clev:{sm['clevel']} maxdl:{sm['max_depth']}"
    print(out)
