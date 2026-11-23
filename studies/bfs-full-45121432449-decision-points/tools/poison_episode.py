import re,sys
def parse(path):
    out=[]
    for l in open(path):
        p=l.split()
        if len(p)<5 or p[1]=='-': continue
        t=int(p[0]); m=re.match(r'd(\d+)/(\d+)',p[2]); h=re.match(r'hp(-?\d+)/(\d+)',p[3])
        tm={}
        tf=[x for x in p if x.startswith('t') and (x=='t-' or ':' in x)][0]
        if tf!='t-':
            for kv in tf[1:].split(','):
                k,v=kv.split(':'); tm[int(k)]=int(v)
        au=int([x for x in p if x.startswith('au')][0][2:])
        out.append((t,int(m.group(1)),int(h.group(1)),int(h.group(2)),tm.get(7,0),au,tm))
    return out
d=sys.argv[1]
s=parse(f'D/{d}/state.log')
# find start of the last poison episode (last time poison went from 0 to >0 ... but treat gaps <200 turns as same)
i=len(s)-1
while i>0 and s[i][4]==0: i-=1
start=i
while start>0:
    j=start-1
    while j>0 and s[j][4]==0: j-=1
    if s[j][4]>0 and s[start][0]-s[j][0] < 300 and s[start-1][4]==0: start=j; continue
    if s[start-1][4]>0: start-=1; continue
    break
print(d,'episode start turn',s[start][0],'death turn',s[-1][0])
last=None
for r in s[start:]:
    key=(r[1],r[2],r[4],r[5])
    if key!=last and (r[0]%50==0 or last is None or r[1]!=last[0] or r==s[-1] or abs(r[4]-last[2])>3):
        print(f"t{r[0]} DL{r[1]} hp{r[2]}/{r[3]} pois{r[4]} au{r[5]} margin{r[2]-r[4]} other{ {k:v for k,v in r[6].items() if k!=7} }")
    last=key
