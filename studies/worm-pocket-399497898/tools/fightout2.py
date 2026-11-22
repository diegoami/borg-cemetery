"""Interactive fight-out counterfactual (diagnostic). The Borg plays the recorded game to
key K in the original process; then this script plays, planning on the player's KNOWN map
and visible monsters only. Usage: fightout2.py K OUTDIR [maxsteps] [heal_hp] [policy]
policy: fight = cheapest known path to the exit corridor (33,141), attacking the worm on the path;
        none  = stand and attack the nearest adjacent worm (no movement) -- a control."""
import sys,subprocess,heapq,json,os
S=os.environ['SCRATCH']
B=open(f'{S}/env.sh').read().split('B=')[1].strip()
K=int(sys.argv[1]); OUT=sys.argv[2]; MAXS=int(sys.argv[3]) if len(sys.argv)>3 else 300
HEAL=int(sys.argv[4]) if len(sys.argv)>4 else 25
POL=sys.argv[5] if len(sys.argv)>5 else 'fight'
EXIT=(33,141); STAIR=(17,98)
DIRK={(-1,-1):55,(-1,0):56,(-1,1):57,(0,-1):52,(0,1):54,(1,-1):49,(1,0):50,(1,1):51}
run=f'{OUT}/run'; subprocess.run(['rm','-rf',OUT]); os.makedirs(run)
for d in 'user save archive panic scores'.split(): os.makedirs(f'{run}/{d}')
for f in ('borg.txt','scary_monsters.txt'): subprocess.run(['cp',f'{B}/user/{f}',f'{run}/user/'])
fi,fo=f'{OUT}/in.fifo',f'{OUT}/out.fifo'; os.mkfifo(fi); os.mkfifo(fo)
open(f'{OUT}/empty','w').close()
G=f'{S}/diag/build/rust/game'
env=dict(BORGH_HANDOVER=str(K),BORGH_HANDOVER_KEYS=f'{OUT}/empty',BORGH_MAPDUMP=f'{OUT}/map.txt',BORGH_IN=fi,BORGH_OUT=fo,
         PATH='/usr/bin:/bin',HOME='/tmp',TZ='UTC',LANG='C.UTF-8',LC_ALL='C.UTF-8',BORG_RUN_DIR=run)
cmd=[f'{G}/angband','-mborgh','-n','-uBorg']+[f'-d{d}={run}/{d}' for d in 'user save archive panic scores'.split()]+['--',
 '-seed','399497898','-race','8','-class','3','-turns','100000','-keylog',f'{run}/keys.log','-summary',f'{run}/summary.json',
 '-menu-letters','-exact-turns','-statelog',f'{run}/state.log','-msglog',f'{run}/messages.log']
proc=subprocess.Popen(cmd,cwd=G,env=env,stdout=subprocess.DEVNULL,stderr=open(f'{run}/stderr.log','w'))
rd=open(fo,'r'); wr=None
def state():
    L=open(f'{OUT}/map.txt').read().split('\n')
    h=L[0].split(); st=dict(turn=int(h[1]),depth=int(h[3]),pos=tuple(map(int,h[5].split(','))),
        hp=int(h[7].split('/')[0]),poison=int(h[13]),sp=int(h[15]),dead=int(h[17]))
    i=L.index('TRUTH'); j=L.index('KNOWN'); T=L[i+1:j]; Kn=L[j+1:j+1+len(T)]
    gear=[l for l in L if l.startswith('GEAR')]
    worms=sum(1 for l in L if l.startswith('MON') and 'worm' in l)
    st['worms']=worms
    return st,Kn,gear
def label(gear,kind):
    for g in gear:
        p=g.split(' ',2)
        if p[1]!='=' and g.endswith('['+kind+']'): return ord(p[1])
    return None
def plan(Kn,src,dst):
    H,W=len(Kn),len(Kn[0]); D={src:0};P={};pq=[(0,src)]
    while pq:
        d,u=heapq.heappop(pq)
        if u==dst: break
        if d>D[u]: continue
        for (dy,dx) in DIRK:
            v=(u[0]+dy,u[1]+dx)
            if not(0<=v[0]<H and 0<=v[1]<W): continue
            c=Kn[v[0]][v[1]]
            if c in ' #': continue
            w=1+(3 if c=='w' else 0)+(50 if c=='M' else 0)
            if d+w<D.get(v,1e9): D[v]=d+w;P[v]=u;heapq.heappush(pq,(d+w,v))
    if dst not in D: return None
    p=[dst]
    while p[-1]!=src: p.append(P[p[-1]])
    return p[::-1]
log=[];used=[];phase='exit';start=None;st=None;minhp=99;outturn=None
def send(k):
    global wr
    if wr is None: wr=open(fi,'w')
    wr.write(f'{k}\n'); wr.flush()
pending=[]
for step in range(MAXS*3):
    line=rd.readline()
    if not line: break
    st,Kn,gear=state()
    if start is None: start=dict(st); start['gear']=[g for g in gear if 'Potion' in g]
    minhp=min(minhp,st['hp'])
    if st['dead'] or st['depth']!=1: send(-1); break
    if pending: send(pending.pop(0)); continue
    if len(log)>=MAXS: send(-1); break
    y,x=st['pos']
    if phase=='exit' and y<=33 and x==141: phase='stair'; outturn=st['turn']
    if phase=='stair' and (y,x)==STAIR: log.append((st['turn'],'>')); send(ord('>')); continue
    k=None
    if st['hp']<HEAL:
        for kind in ('Cure Serious Wounds','Cure Light Wounds'):
            l=label(gear,kind)
            if l: k=[ord('q'),l]; used.append((st['turn'],kind)); break
    if k is None and st['poison']>0 and st['hp']<HEAL+15:
        l=label(gear,'Neutralize Poison')
        if l: k=[ord('q'),l]; used.append((st['turn'],'Neutralize Poison'))
    if k is None:
        if POL=='none':
            adj=[(dy,dx) for (dy,dx) in DIRK if Kn[y+dy][x+dx]=='w']
            k=[DIRK[adj[0]]] if adj else [ord('s')]   # 's' = steal/hold? use hold below
            if not adj: k=[ord(',')]  # ',' = stay still (pickup/hold) in 4.2 original keys
        else:
            p=plan(Kn,(y,x),EXIT if phase=='exit' else STAIR)
            if not p or len(p)<2: log.append((st['turn'],'no path')); send(-1); break
            n=p[1]; k=[DIRK[(n[0]-y,n[1]-x)]]
    log.append((st['turn'],phase,st['pos'],st['hp'],st['poison'],st['worms'],k))
    send(k[0]); pending=k[1:]
proc.wait(timeout=60)
try: st,Kn,gear=state()
except Exception: pass
summ=json.load(open(f'{run}/summary.json')) if os.path.exists(f'{run}/summary.json') else {}
res=dict(K=K,policy=POL,heal=HEAL,start=start,end=st,min_hp=minhp,out_of_room_turn=outturn,steps=len(log),used=used,
         escaped=bool(st and st['depth']!=1 and not st['dead']),dead=summ.get('dead'),death_cause=summ.get('death_cause'),
         stop=summ.get('stop_reason'),final_turn=summ.get('game_turns'),gear_end=[g for g in gear if 'Potion' in g],log=log)
json.dump(res,open(f'{OUT}/result.json','w'),indent=1)
print(K,POL,'start t',start['turn'],'hp',start['hp'],'| out',outturn,'| end',summ.get('stop_reason'),summ.get('game_turns'),'dead',summ.get('dead'),
      'depth',st['depth'],'hp',st['hp'],'minhp',minhp,'| used',[u[1] for u in used])
