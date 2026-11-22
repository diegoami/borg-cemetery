import sys,re,collections
d=sys.argv[1]
msgs=[l.rstrip('\n').split(' ',3) for l in open(f'{d}/messages.log',errors='replace')]
msgs=[m for m in msgs if len(m)==4]
state=[l.split() for l in open(f'{d}/state.log')]
bykey=collections.OrderedDict()
for k,t,ty,x in msgs: bykey.setdefault(int(k),[]).append(x)
keys=[k for k,v in bykey.items() if any('crow' in x.lower() for x in v)]
for k in keys:
    v=bykey[k]
    act=[x for x in v if re.search(r'Attack on sight|Performing attack|Phase|Reading|Quaff|Fleeing|Retreat|Flowing|Fast-fragile|No healing|Cornered|Fight race:',x)]
    game=[x for x in v if not x.startswith('#') and 'crow' in x.lower()]
    s=state[k-1]
    print(k,s[0],s[2],s[3],'|',' ; '.join(a[2:90] for a in act[:3]),'|',' / '.join(game[:4]))
