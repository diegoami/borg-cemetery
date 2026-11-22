import json,re,sys
B=sys.argv[1]
trace=[json.loads(l) for l in open(B+'/trace-core.jsonl')]
msgs=[]
for l in open(B+'/messages.log'):
    p=l.rstrip('\n').split(' ',3)
    if len(p)==4: msgs.append((int(p[0]),int(p[1]),p[3]))
state={}
for i,l in enumerate(open(B+'/state.log'),1):
    f=l.split(); state[i]=f
keys=[l.split() for l in open(B+'/keys.log')]
# key index -> state line: state line i corresponds to key i
rows=[]
probe={}; borg={}
for l in open(sys.argv[2]):
    f=l.split()
    if f[0]=='PROBE' and int(f[1]) not in probe: probe[int(f[1])]=dict(x.split('=') for x in f[2:])
    if f[0]=='BORG' and int(f[1]) not in borg: borg[int(f[1])]=dict(x.split('=') for x in f[2:])
th=[t for t in trace if t['turn']>=78684]
for n,t in enumerate(th):
    turn=t['turn']; nxt=th[n+1]['turn'] if n+1<len(th) else 10**9
    # messages logged at this think: notes with game turn == turn and key count between
    notes=[m for m in msgs if m[1]==turn and m[2].startswith('# ')]
    race=[m[2] for m in notes if m[2].startswith('# Fight race')]
    standing=any('Standing on dn-stairs' in m[2] for m in notes)
    scary=any('Scary guy on level' in m[2] for m in notes)
    # game messages from this think until next think
    k=[i for i,kk in enumerate(keys,1) if int(kk[0])==turn]
    kn=[i for i,kk in enumerate(keys,1) if int(kk[0])==nxt]
    K=k[0]; KN=kn[0] if kn else 10**9
    game=[m[2] for m in msgs if K<=m[0]<KN and not m[2].startswith('#') and m[2]]
    st=state[k[0]] if k else None
    pos=st[1] if st else '?'; hp=st[3] if st else '?'; tm=st[9] if st else '?'
    stun=re.search(r'9:(\d+)',tm); stun=stun.group(1) if stun else '0'
    rr=''
    if race:
        m=re.search(r'([\d.]+) turns to kill, ([\d.]+) damage/turn, HP (-?\d+): (\w+(?: \w+)?)',race[0]); t2=re.search(r'needs (\d+) HP, attack \d+ ([\d.]+)',race[1]) if len(race)>1 else None
        rr=f"{m.group(4)}: {m.group(1)} turns, in {m.group(2)}/turn" + (f"; needs {t2.group(1)}, out {t2.group(2)}/turn" if t2 else '')
    gm='; '.join(x.replace('the blue yeek','yeek').replace("Grip, Farmer Maggot's Dog",'Grip').replace('The blue yeek','Yeek') for x in game)
    kb=bytes(t['keys']).decode('latin1').replace('\x1b','ESC')
    pr=probe.get(turn,{}); bo=borg.get(turn,{})
    rows.append(f"| {t['think']} | {k[0] if k else ''} | {turn} | {pos} | {hp[2:]} | {stun} | {pr.get('to_d','')} | {bo.get('todam','')} / {bo.get('isstun','')} | {t['check']} (`:{t['check_source'].split(':')[-1]}`) | `{kb}` | {'yes' if standing else ''} | {rr} | {gm} |")
print("| think | key # | game turn | x,y | HP | stun timer | engine to_d | Borg BI_TODAM / BI_ISSTUN | check | keys | on `>` note | fight race | game messages to next think |")
print("|---:|---:|---:|---|---|---:|---:|---|---|---|---|---|---|")
print('\n'.join(rows))
