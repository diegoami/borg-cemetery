import sys
f,y0,y1,x0,x1=sys.argv[1],*map(int,sys.argv[2:6])
mode=sys.argv[6] if len(sys.argv)>6 else 'both'
L=open(f).read().split('\n')
i=L.index('TRUTH'); j=L.index('KNOWN')
T=L[i+1:j]; K=L[j+1:j+1+len(T)]
print(L[0])
hdr='    '+''.join(str(x//100) if x%10==0 else ' ' for x in range(x0,x1))
hdr2='    '+''.join(str((x//10)%10) if x%10==0 else ' ' for x in range(x0,x1))
hdr3='    '+''.join(str(x%10) for x in range(x0,x1))
w=x1-x0
print(hdr2+'   '+hdr2[4:]); print(hdr3+'   '+hdr3[4:])
for y in range(y0,y1):
  a=T[y][x0:x1]; b=K[y][x0:x1]
  print(f'{y:3d} '+(a if mode!='known' else '')+('   '+b if mode!='truth' else ''))
mons=[l for l in L if l.startswith('MON')]
import collections
c=collections.Counter(' '.join(l.split()[2:-2]) for l in mons)
print('monsters:',dict(c))
