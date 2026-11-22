import sys,collections,heapq
def load(f):
    L=open(f).read().split('\n')
    i=L.index('TRUTH'); j=L.index('KNOWN')
    T=L[i+1:j]; K=L[j+1:j+1+len(T)]
    h=L[0].split(); py,px=map(int,h[5].split(','))
    mons=[(tuple(map(int,l.split()[1].split(','))),' '.join(l.split()[2:-2])) for l in L if l.startswith('MON')]
    return L[0],T,K,(py,px),mons
PASS=set(".,'+<>:@wM")
def dij(T,src,mons,worm_cost=None,known=None):
    H,W=len(T),len(T[0])
    wpos={p for p,n in mons if 'worm' in n}
    opos={p for p,n in mons if 'worm' not in n}
    D={src:0};P={};pq=[(0,src)]
    while pq:
        d,u=heapq.heappop(pq)
        if d>D[u]: continue
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                if not dy and not dx: continue
                v=(u[0]+dy,u[1]+dx)
                if not(0<=v[0]<H and 0<=v[1]<W): continue
                c=T[v[0]][v[1]]
                if c not in PASS: continue
                if known is not None and known[v[0]][v[1]]==' ': continue
                w=1
                if v in wpos: w+= worm_cost if worm_cost is not None else 10**6
                if c==':': w+=5
                nd=d+w
                if nd<D.get(v,1e18): D[v]=nd;P[v]=u;heapq.heappush(pq,(nd,v))
    return D,P
def path(P,src,dst):
    p=[dst]
    while p[-1]!=src: p.append(P[p[-1]])
    return p[::-1]
if __name__=='__main__':
    hdr,T,K,src,mons=load(sys.argv[1])
    print(hdr)
    stairs=[(y,x,c) for y,r in enumerate(T) for x,c in enumerate(r) if c in '<>']
    wpos={p for p,n in mons if 'worm' in n}
    for wc in (None,3):
        D,P=dij(T,src,mons,wc)
        for y,x,c in stairs:
            if (y,x) in D:
                p=path(P,src,(y,x)); nw=sum(1 for q in p if q in wpos)
                print(f"worm_cost={wc} stair {c} {y},{x}: steps {len(p)-1} worms_on_path {nw} first: {p[1:8]}")
            else: print(f"worm_cost={wc} stair {c} {y},{x}: unreachable")
