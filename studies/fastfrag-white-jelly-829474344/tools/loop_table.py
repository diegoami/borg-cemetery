import sys,json,re,collections
run=sys.argv[1]; ranges=[tuple(map(int,r.split('-'))) for r in sys.argv[2:]]
# state rows by key line: state.log has one row per key, same order as keys.log
keys=[l.split() for l in open(run+'/keys.log') if l.strip()]
state=[l.split() for l in open(run+'/state.log') if l.strip()]
trace={}
for l in open(run+'/trace-core.jsonl'):
    e=json.loads(l); trace.setdefault(e['turn'],e)
notes=collections.defaultdict(list); game=collections.defaultdict(list)
for l in open(run+'/messages.log'):
    p=l.rstrip('\n').split(' ',3)
    if len(p)<4: continue
    t=int(p[1]); m=p[3]
    if m.startswith('# Retreating') or m.startswith('# Flowing toward') or m.startswith('# Quaffing') : notes[t].append(m[2:])
    elif not m.startswith('#') and ('jelly' in m or 'poison' in m or 'feel' in m): game[t].append(m)
print('| key (keys.log line) | game turn | position (y,x) | HP | poison (TMD_POISONED) | rule (core trace `check`) | key | note | engine messages until the next think |')
print('|---:|---:|---|---:|---:|---|---|---|---|')
for lo,hi in ranges:
    turns=sorted(t for t in trace if lo<=t<=hi)
    for i,t in enumerate(turns):
        e=trace[t]
        # first key line at this turn whose key is the think's key
        idx=next((n for n,k in enumerate(keys) if int(k[0])==t and int(k[2],16) in (e.get('keys') or [0])), None)
        s=state[idx] if idx is not None else None
        pos=s[1].split(',') if s else ['?','?']
        hp=re.match(r'hp(-?\d+)',s[3]).group(1) if s else '?'
        m=re.match(r't7:(\d+)',s[9]) if s else None
        pois=m.group(1) if m else '0'
        nxt=turns[i+1] if i+1<len(turns) else t+10
        gm='; '.join(x for tt in range(t+1,nxt+1) for x in game.get(tt,[]))
        k=''.join(chr(c) for c in (e.get('keys') or []))
        print(f"| {idx+1 if idx is not None else '?'} | {t} | {pos[1]},{pos[0]} | {hp} | {pois} | `{e['check'].split('::')[-1]}` (danger {e['danger']}) | `{k}` | {'; '.join(notes.get(t,[]))} | {gm} |")
    print('| … | | | | | | | | |')
