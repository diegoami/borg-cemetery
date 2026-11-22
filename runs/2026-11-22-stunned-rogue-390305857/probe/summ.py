import sys,re,os
for d in sys.argv[1:]:
    msgs=[l.rstrip('\n').split(' ',3) for l in open(os.path.join(d,'messages.log')) if l.count(' ')>=3]
    probe=[l.split() for l in open(os.path.join(d,'stderr.log')) if l.startswith('PROBE')]
    cf=[l for l in open(os.path.join(d,'stderr.log')) if l.startswith('CF ')]
    t0=int(cf[0].split()[4]) if cf else 78746
    kill=None; stunend=None
    for k,t,ty,m in msgs:
        t=int(t)
        if t<78700: continue
        if kill is None and re.search(r'(slain|killed|destroyed) the blue yeek',m): kill=(t,m)
        if stunend is None and t>=78756 and 'no longer stunned' in m: stunend=t
    hp=[(int(p[1]),int(p[2][3:])) for p in probe if 78746<=int(p[1])<=(kill[0] if kill else 79500)]
    mn=min(hp,key=lambda x:x[1]) if hp else None
    end=[p for p in probe][-1]
    print(f"{os.path.basename(d)}: action turn {t0}; yeek killed {kill}; stun ends {stunend}; min HP over the encounter {mn}; last probe {end[1]} hp {end[2]}")
