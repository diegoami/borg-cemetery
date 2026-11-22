import sys,re
from collections import deque
maps={'true':{},'borg':{}}
for l in open(sys.argv[1]):
    m=re.search(r'# CF (true|borg) y(\d+) (.*)$',l.rstrip('\n'))
    if m:
        for k,c in enumerate(m.group(3)): maps[m.group(1)][(int(m.group(2)),40+k)]=c
JELLY=(14,96)
def adj(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=1
def bfs(mp, start, goals, passable, avoid_jelly):
    prev={start:None}; q=deque([start])
    while q:
        c=q.popleft()
        if c in goals:
            p=[];
            while c: p.append(c); c=prev[c]
            return p[::-1]
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                n=(c[0]+dy,c[1]+dx)
                if n in prev or n==JELLY: continue
                ch=mp.get(n,'#')
                if not passable(ch): continue
                if avoid_jelly and adj(n,JELLY): continue
                prev[n]=c; q.append(n)
    return None
known=lambda ch: ch in ".'<>+:M"
withunknown=lambda ch: ch in ".'<>+:M "
start=(13,94)
for name,mp in maps.items():
    st=[k for k,v in mp.items() if v in '<>']
    for desc,pas in (('known-only',known),('unknown-passable',withunknown)):
        if name=='true' and desc=='unknown-passable': continue
        for aj in (False,True):
            p=bfs(mp,start,set(st),pas,aj)
            print(f'{name:5s} {desc:16s} avoid-jelly={aj!s:5s}:', 'none' if not p else f'{len(p)-1} steps to {p[-1]} via {p[1:6]}...')
    for s in st:
        p=bfs(mp,start,{s},known,True)
        print(f'  {name} stair {s} {mp[s]}: {"unreachable" if not p else str(len(p)-1)+" steps avoiding the jelly"}')
if len(sys.argv)>2:
    out=open(sys.argv[2],'w')
    for name,mp in maps.items():
        out.write(f'== {name} map (y rows, x columns 40-129; M monster)\n')
        out.write('    '+''.join(str((x//10)%10) for x in range(40,130))+'\n')
        out.write('    '+''.join(str(x%10) for x in range(40,130))+'\n')
        for y in range(0,40):
            out.write(f'{y:3d} '+''.join(mp.get((y,x),' ') for x in range(40,130))+'\n')
