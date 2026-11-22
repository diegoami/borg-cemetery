#!/usr/bin/env python3
"""Summarise counterfactual runs: outcome, the fight's lowest HP (until the
rogue leaves DL2 or dies), when it left, cures/phases used in the fight."""
import json,re,glob,os,sys
root=sys.argv[1]
dirs=sorted(glob.glob(root+'/*'))
for d in dirs:
    if not os.path.exists(d+'/summary.json'): continue
    s=json.load(open(d+'/summary.json'))
    msgs=open(d+'/messages.log',errors='replace').read().splitlines()
    rows=[(int(l.split()[1]),l.split(' ',3)[3]) for l in msgs if len(l.split())>3 and l.split()[1].isdigit()]
    hook=next((m for t,m in rows if 'CF hook' in m),'-')
    end=next(((t,m) for t,m in rows if t>=64380 and (m.startswith('You enter') or m.startswith('You die'))),None)
    tend=end[0] if end else 10**9
    fight=[(t,m) for t,m in rows if 64380<=t<=tend]
    hps=[(t,int(re.search(r'HP:(-?\d+)/',m).group(1))) for t,m in fight if '# Loc:' in m]
    mn=min(hps,key=lambda x:x[1]) if hps else None
    cnt=lambda k: sum(1 for t,m in fight if m.startswith(k))
    print(f"{os.path.basename(d)}\t{s['stop_reason']}\tturn {s['game_turns']}\tCL{s['clevel']}\tmaxDL{s['max_depth']}\tfight ends {end[0] if end else '-'} ({(end[1][:22] if end else '')})\tmin HP {mn}\tcures {cnt('# Quaffing Potions of Cure')}\tphase {cnt('# Reading Scrolls of Phase')}\t{hook}")
