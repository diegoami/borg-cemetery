import json,glob,os,collections,sys
res=[]
for f in glob.glob('**/trace-core-tail.jsonl', recursive=True):
    d=os.path.dirname(f)
    try: L=[json.loads(l) for l in open(f)]
    except Exception: continue
    seq=[(e.get('check'),e.get('danger',0)) for e in L[-120:]]
    alt=sum(1 for a,b in zip(seq,seq[1:]) if a[0]=='borg_caution' and a[1]>0 and b[0] and 'flow' in b[0] and b[1]==0)
    if alt>=10:
        try: r=json.load(open(d+'/record.json'))
        except Exception: r={}
        t=r.get('terminal',{}); i=r.get('identity',{})
        res.append((alt, d, r.get('character'), t.get('cause') or r.get('raw_cause'), t.get('level'), t.get('depth'), i.get('seed'), (i.get('git_rev') or '')[:8], r.get('encounter_family','')[:18], collections.Counter(s[0] for s in seq).most_common(3)))
for x in sorted(res, key=lambda x:-x[0]): print(x)
print(len(res))
