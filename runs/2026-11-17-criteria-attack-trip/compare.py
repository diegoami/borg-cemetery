#!/usr/bin/env python3
"""Pair two suite outputs start by start; print JSON + markdown tables."""
import json, sys, collections, pathlib

crit, ctl = map(pathlib.Path, sys.argv[1:3])


def load(root):
    out = {}
    for d in sorted(root.iterdir()):
        s = d / 'summary.json'
        if not s.is_file():
            continue
        j = json.loads(s.read_text())
        ex = int((d / 'run_exit').read_text().strip()) if (d / 'run_exit').is_file() else None
        out[d.name] = dict(
            race=j.get('race'), cls=j.get('class'), seed=j['seed'], stop=j['stop_reason'],
            dead=j['dead'], cause=j.get('death_cause'), turns=j['game_turns'],
            clevel=j.get('max_clevel', j.get('clevel')), maxdepth=j['max_depth'],
            depth=j.get('depth'), exit=ex, wall=j.get('wall_seconds'))
    return out


A, B = load(crit), load(ctl)
names = sorted(set(A) & set(B), key=lambda n: (int(n.split('-')[1]), int(n.split('-')[-1])))
classes = collections.OrderedDict()
for n in names:
    classes.setdefault(A[n]['cls'], []).append(n)


def tally(R, ns):
    d = [n for n in ns if R[n]['dead']]
    return dict(n=len(ns), dead=len(d), alive=len(ns) - len(d),
                med_turns=sorted(R[n]['turns'] for n in ns)[len(ns) // 2],
                med_clevel=sorted(R[n]['clevel'] for n in ns)[len(ns) // 2],
                max_depth=max(R[n]['maxdepth'] for n in ns),
                mean_clevel=sum(R[n]['clevel'] for n in ns) / len(ns))


res = dict(per_class={}, all={}, pairs=collections.Counter())
for c, ns in classes.items():
    res['per_class'][c] = dict(crit=tally(A, ns), ctl=tally(B, ns))
res['all'] = dict(crit=tally(A, names), ctl=tally(B, names))
for n in names:
    res['pairs'][('dies' if A[n]['dead'] else 'lives') + '/' + ('dies' if B[n]['dead'] else 'lives')] += 1
res['pairs'] = dict(res['pairs'])
res['same_keys_outcome'] = sum(1 for n in names if (A[n]['turns'], A[n]['dead'], A[n]['clevel']) == (B[n]['turns'], B[n]['dead'], B[n]['clevel']))
res['bad_exit'] = {arm: [n for n, r in R.items() if r['exit'] not in (0, None) and not r['dead']] for arm, R in (('crit', A), ('ctl', B))}
res['causes'] = {arm: collections.Counter(R[n]['cause'] for n in names if R[n]['dead']).most_common()
                 for arm, R in (('crit', A), ('ctl', B))}
res['deepest'] = {arm: sorted(((R[n]['maxdepth'], n, R[n]['dead'], R[n]['cause']) for n in names), reverse=True)[:8]
                  for arm, R in (('crit', A), ('ctl', B))}
res['rows'] = {n: dict(crit=A[n], ctl=B[n]) for n in names}
json.dump(res, sys.stdout, indent=1, default=list)
