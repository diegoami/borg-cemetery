"""Every executed attack in a harness run: decision note, target, distance,
utilities from trace-core.jsonl, HP from state.log, outcome messages."""
import re,sys,json,collections
def load(d):
    msgs=[l.rstrip('\n').split(' ',3) for l in open(f'{d}/messages.log',errors='replace')]
    msgs=[m for m in msgs if len(m)==4]
    state=[l.split() for l in open(f'{d}/state.log')]
    trace=collections.defaultdict(list)
    for l in open(f'{d}/trace-core.jsonl'):
        t=json.loads(l); trace[t['turn']].append(t)
    return msgs,state,trace
KIND={'Attacking with weapon':'melee','Firing missile':'shot','Throwing':'throw'}
def attacks(d):
    msgs,state,trace=load(d); out=[]
    for i,(key,turn,typ,text) in enumerate(msgs):
        kind=next((v for k,v in KIND.items() if text.startswith('# '+k)),None)
        if not kind: continue
        dec=tgt=None
        for j in range(i-1,max(0,i-40),-1):
            t=msgs[j][3]
            if tgt is None:
                m=re.search(r'# Facing (.+?) at \((\d+),(\d+)\) who has (\d+)',t) or None
                m2=re.search(r'# Targeting (.+?) who has (\d+) Hit Points \((\d+),(\d+)\)',t)
                if m: tgt=(m[1],int(m[2]),int(m[3]),int(m[4]))
                elif m2: tgt=(m2[1],int(m2[3]),int(m2[4]),int(m2[2]))
            if re.search(r'# (Performing attack type|Attack on sight)',t): dec=t[2:]; break
        k=int(key); s=state[k-1] if k-1<len(state) else None
        px,py=map(int,s[1].split(',')); hp=s[3]
        dist=max(abs(py-tgt[1]),abs(px-tgt[2])) if tgt else None
        # outcome: game messages until next Borg decision line
        res=[]
        for j in range(i+1,min(len(msgs),i+30)):
            t=msgs[j][3]
            if t.startswith('# ') and re.search(r'Performing attack|Attack on sight|Loc:',t): break
            if not t.startswith('#'): res.append(t)
        tr=[x for x in trace.get(int(turn),[]) if x.get('attacks')]
        util={}
        if tr:
            for c in tr[-1]['attacks'][-1]['candidates']:
                if c['attack_name'] in ('BF_THRUST','BF_OBJECT','BF_LAUNCH') : util[c['attack_name'][3:]]=(c['raw_utility'],c['adjusted_utility'])
        hp_after=None
        for s2 in state[k:k+60]:
            if int(s2[0])>int(turn): hp_after=s2[3]; break
        out.append(dict(key=k,turn=int(turn),depth=s[2],kind=kind,decision=dec,target=tgt and tgt[0],thp=tgt and tgt[3],dist=dist,hp=hp,hp_after=hp_after,util=util,res=res,text=text[2:]))
    return out
if __name__=='__main__':
    for a in attacks(sys.argv[1]): print(json.dumps(a))
