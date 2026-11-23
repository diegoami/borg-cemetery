import json,re,sys,glob,os
from collections import deque
S='/tmp/claude-0/-home-user/2add62db-0818-573c-8b91-ab7e03086156/scratchpad'
cells={str(json.loads(l)['seed']):json.loads(l) for l in open(f'{S}/cells-206.jsonl')}
PASS=set(".:<>'+^,_-|\\/=\"!?$*&(){}[]~`%0123456789")
def analyse(rec, bundle):
    seed=bundle.rstrip('/').split('/')[-1]; c=cells[seed]; cause=c['cause']
    fr=[json.loads(l) for l in open(f'{rec}/record/frames.jsonl')]
    grid=[' ']*1920
    # level segments: change when depth changes or big position jump with stairs msg; use depth+turn from messages entries
    msgs=[l.rstrip('\n').split(' ',3) for l in open(f'{bundle}/messages.log',errors='replace')]
    msgs=[m for m in msgs if len(m)==4]
    entries=[int(m[1]) for m in msgs if 'You enter a maze' in m[3]]
    t0=entries[-1]
    known={}  # (x,y)->glyph
    stairs={}
    traj=[]
    for f in fr:
        for i,ch,at in f['cells']:
            if 0<=i<1920: grid[i]=chr(ch) if ch>=32 else ' '
        if f['turn']<t0 or f.get('depth',0)!=c['final']['depth']: continue
        # locate @ in map area
        pos=None
        for r in range(1,22):
            row=grid[r*80+13:r*80+80]
            if '@' in row:
                pos=(r,13+row.index('@')); break
        if not pos: continue
        ox=pos[1]-f['x']; oy=pos[0]-f['y']
        for r in range(1,22):
            for col in range(13,80):
                g=grid[r*80+col]
                wx,wy=col-ox,r-oy
                if g in '<>': stairs[(wx,wy)]=(g,f['turn'])
                if g!=' ': known[(wx,wy)]=g
        traj.append((f['turn'],f['x'],f['y'],f['hp'],f['max_hp'],dict(stairs)))
    return c,traj,known,msgs,t0
def bfs(known,src,targets):
    if not targets: return None
    q=deque([(src,0)]); seen={src}
    while q:
        p,d=q.popleft()
        if p in targets: return d
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                n=(p[0]+dx,p[1]+dy)
                if n in seen: continue
                g=known.get(n)
                if g is None or g in '#% ': continue
                seen.add(n); q.append((n,d+1))
    return None
cheb=lambda p,q:max(abs(p[0]-q[0]),abs(p[1]-q[1]))
for rec in sorted(glob.glob(f'{S}/W/rec/*')):
    seed=rec.split('-')[-1]
    b=f'{S}/W/d/{seed}'
    if not os.path.exists(f'{rec}/record/frames.jsonl'): continue
    try:
        c,traj,known,msgs,t0=analyse(rec,b)
    except Exception as e:
        print(seed,'ERR',e); continue
    cause=re.sub(r'^(a|an|the) ','',c['cause'])
    kt=None
    for m in msgs:
        if int(m[1])>=t0:
            mm=re.search(r"# Creating a monster '(.+)' at \((\d+),(\d+)\)",m[3])
            if mm and mm.group(1)==cause: kt=(int(m[1]),int(mm.group(3)),int(mm.group(2))); break
    def at(t):
        r=None
        for x in traj:
            if x[0]<=t: r=x
        return r
    def sd(x):
        st=[k for k in x[5]]
        if not st: return (None,None)
        p=(x[1],x[2])
        return (min(cheb(p,s) for s in st), bfs(known,p,set(st)))
    mx=max((sd(x)[0] or 0) for x in traj)
    line=f"{seed:>10} {c['character']:<22} CL{c['final']['max_level']} enter t{t0} stairs_seen={len(traj[-1][5])} maxCheb={mx} death(cheb,walk)={sd(traj[-1])}"
    if kt:
        x=at(kt[0]); line+=f" | killer t{kt[0]} borg@stairs(cheb,walk)={sd(x)} killer-dist={cheb((x[1],x[2]),(kt[1],kt[2]))} hp={x[3]}/{x[4]} turns-to-death={(c['final']['turn']-kt[0])/10:.1f}"
    st=traj[-1][5]
    line+=" glyphs="+''.join(sorted(g for g,_ in st.values()))
    ups=[k for k,(g,_) in st.items() if g=='<']
    p=(traj[-1][1],traj[-1][2])
    line+=f" nearest_up(cheb)={min([cheb(p,u) for u in ups]) if ups else None} farthest_up={max([cheb(p,u) for u in ups]) if ups else None}"
    print(line)
