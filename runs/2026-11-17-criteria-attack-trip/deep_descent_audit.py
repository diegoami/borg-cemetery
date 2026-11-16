import json,glob,re,collections,sys
plan={};sec=None
for l in open('crit/harness/plans/errands_plan.txt'):
    l=l.split('#')[0].rstrip()
    m=re.match(r'\[(\w+)\]',l)
    if m: sec=m.group(1); plan[sec]=[]; continue
    m=re.match(r'\s*(?:(\d+)\s*<\s*level\s*<=\s*(\d+)|level\s*<=\s*(\d+)|level\s*==\s*(\d+))',l)
    if m: cur=m.groups()
    m2=re.match(r'\s*max-depth\s+(\d+)',l)
    if m2 and sec:
        a,b,c,d=cur
        lo,hi=(int(a)+1,int(b)) if a else (1,int(c)) if c else (int(d),int(d))
        plan[sec].append((lo,hi,int(m2.group(1))))
def cap(cls,l):
    for lo,hi,mx in plan.get(cls,plan['default']):
        if lo<=l<=hi: return mx
out={}
for arm in ('crit','reborn'):
    rows=[]
    for d in sorted(glob.glob(f'out-{arm}/crit-*/summary.json')):
        p=d.rsplit('/',1)[0]; j=json.load(open(d))
        msgs=open(p+'/messages.log',errors='replace').read()
        reads=len(re.findall(r'# Reading Scrolls? of Deep Descent',msgs))
        floors=len(re.findall(r'The floor opens beneath you',msgs))
        c=cap(j['class'].lower(),j.get('max_clevel') or j['clevel'])
        rows.append(dict(name=p.split('/')[1],cls=j['class'],dead=j['dead'],cause=j['death_cause'],maxd=j['max_depth'],depth=j['depth'],lvl=j['max_clevel'],cap=c,over=j['max_depth']>c,dd_reads=reads,dd_falls=floors))
    out[arm]=rows
    n=len(rows); dd=[r for r in rows if r['dd_falls']>0]; over=[r for r in rows if r['over']]
    print(arm,'runs',n,'with a Deep Descent fall',len(dd),'over cap',len(over),'over cap without DD',len([r for r in over if not r['dd_falls']]),'DD but not over cap',len([r for r in dd if not r['over']]))
    print('  deaths with DD:',sum(r['dead'] for r in dd),'/',len(dd),' deaths without DD:',sum(r['dead'] for r in rows if not r['dd_falls']),'/',n-len(dd))
    print('  deaths deeper than cap for level at death:',len([r for r in rows if r['dead'] and r['depth'] is not None and r['cap'] and r['depth']>r['cap']]))
    print('  median dd falls among DD runs', sorted(r['dd_falls'] for r in dd)[len(dd)//2] if dd else 0, 'max', max(r['dd_falls'] for r in rows))
json.dump(out,open('dd.json','w'))
