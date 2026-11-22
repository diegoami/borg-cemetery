import sys,re
from collections import deque
true={}
for l in open(sys.argv[1]):
    m=re.search(r'# CF true y(\d+) (.*)$',l.rstrip('\n'))
    if m:
        for k,c in enumerate(m.group(2)): true[(int(m.group(1)),40+k)]=c
start=tuple(map(int,sys.argv[2].split(','))); goal=tuple(map(int,sys.argv[3].split(',')))
J=(14,96)
prev={start:None};q=deque([start])
order=[(-1,0),(0,-1),(0,1),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
while q:
    c=q.popleft()
    if c==goal: break
    for dy,dx in order:
        n=(c[0]+dy,c[1]+dx)
        if n in prev: continue
        if true.get(n,'#') not in ".'<>:": continue
        if max(abs(n[0]-J[0]),abs(n[1]-J[1]))<=1: continue
        prev[n]=c;q.append(n)
p=[];c=goal
while c: p.append(c);c=prev[c]
p=p[::-1]
key={(-1,-1):'7',(-1,0):'8',(-1,1):'9',(0,-1):'4',(0,1):'6',(1,-1):'1',(1,0):'2',(1,1):'3'}
ks=[key[(b[0]-a[0],b[1]-a[1])] for a,b in zip(p,p[1:])]
print(len(ks),'steps:',''.join(ks),file=sys.stderr)
print(' '.join(format(ord(k),'x') for k in ks))
