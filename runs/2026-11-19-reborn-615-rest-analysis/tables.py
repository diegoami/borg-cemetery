"""Tables for #615 from rests.json."""
import json, sys, collections, statistics
d = json.load(open(sys.argv[1])); R = d['rows']; G = d['games']
W = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
def pct(a, b): return f'{100*a/b:.0f}%' if b else '-'
inter = lambda r: r['out'] == 'interrupted'
print(f"games {len(G)}, deaths {sum(g['stop']!='turns' for g in G.values())}, rests {len(R)}")
print('\n### By kind\n| kind | rests | interrupted | attacked | monster | stopped short | level change | median game turns to interruption |')
print('|---|---:|---:|---:|---:|---:|---:|---:|')
for k, rs in sorted(collections.Counter(r['kind'] for r in R).items(), key=lambda x: -x[1]):
    rr = [r for r in R if r['kind'] == k]; ii = [r for r in rr if inter(r)]
    md = statistics.median([r['dur'] for r in ii]) if ii else '-'
    print(f"| {k} | {len(rr)} | {len(ii)} ({pct(len(ii),len(rr))}) | {sum(r['why']=='attacked' for r in rr)} | {sum(r['why']=='monster' for r in rr)} | {sum(r['out']=='stopped short' for r in rr)} | {sum(r['out']=='level change' for r in rr)} | {md} |")
print('\n### By grid (dungeon rests only, depth > 0)\n| grid | rests | interrupted | attacked |')
print('|---|---:|---:|---:|')
DR = [r for r in R if r['depth'] > 0]
for k in ['stairs', 'dead end', 'corridor', 'room edge/junction', 'open room']:
    rr = [r for r in DR if r['grid'] == k]; ii = [r for r in rr if inter(r)]
    print(f"| {k} | {len(rr)} | {len(ii)} ({pct(len(ii),len(rr))}) | {sum(r['why']=='attacked' for r in rr)} ({pct(sum(r['why']=='attacked' for r in rr),len(rr))}) |")
for lab, f in [('next to unknown grids', lambda r: r['unknown'] > 0), ('next to a door', lambda r: r['doors'] > 0), ('on a scary level', lambda r: r['scary']), ('fleeing', lambda r: r['fleeing'])]:
    rr = [r for r in DR if f(r)]; ii = [r for r in rr if inter(r)]
    print(f"| *{lab}* | {len(rr)} | {len(ii)} ({pct(len(ii),len(rr))}) | {sum(r['why']=='attacked' for r in rr)} |")
print('\n### Awake monster seen recently (Borg-time age of the youngest awake known monster)\n| last seen | rests | interrupted | attacked |')
print('|---|---:|---:|---:|')
for lo, hi in [(0, 5), (6, 20), (21, 50), (51, 200), (201, 10**9)]:
    rr = [r for r in DR if lo <= r['age_awake'] <= hi]; ii = [r for r in rr if inter(r)]
    lab = f'{lo}-{hi}' if hi < 10**9 else f'>{lo-1} or none'
    print(f"| {lab} | {len(rr)} | {len(ii)} ({pct(len(ii),len(rr))}) | {sum(r['why']=='attacked' for r in rr)} |")
# deaths
print(f'\n### Deaths and their last rest (window {W} game turns)\n| game | class | died at | last rest | kind | grid | outcome | turns before death |')
print('|---|---|---:|---:|---|---|---|---:|')
near = 0
for s, g in sorted(G.items()):
    if g['stop'] == 'turns': continue
    rr = [r for r in R if r['seed'] == s and r['T'] <= g['turns']]
    if not rr: print(f"| {s} | {g['cls']} | {g['turns']} | none | | | | |"); continue
    r = rr[-1]
    li = [x for x in rr if inter(x) and g['turns'] - x['T'] <= W]
    near += bool(li)
    print(f"| {s} | {g['cls']} | {g['turns']} | {r['T']} | {r['kind']} | {r['grid']}{' (scary)' if r['scary'] else ''} | {r['out']} {r['why']} | {g['turns']-r['T']} |")
print(f'\ndeaths with an interrupted rest within {W} turns before: {near}')
# candidate rules
print('\n### Candidate rules: rests they would touch (dungeon)\n| rule | rests touched | of them interrupted | attacked | deaths within window after a touched rest |')
print('|---|---:|---:|---:|---:|')
def deaths_after(rs):
    n = set()
    for r in rs:
        g = G[r['seed']]
        if g['stop'] != 'turns' and 0 <= g['turns'] - r['T'] <= W: n.add(r['seed'])
    return len(n)
# rule 4 second interruption on same grid
same = []
seen = collections.Counter()
for r in DR:
    key = (r['seed'], tuple(r['pos']) if r['pos'] else None)
    if seen[key] >= 2: same.append(r)
    if inter(r): seen[key] += 1
rules = [
    ('where: not in an open room (walk to stairs/corridor)', [r for r in DR if r['grid'] in ('open room', 'room edge/junction')]),
    ('where: not next to unknown grids', [r for r in DR if r['unknown'] > 0]),
    ('when: scary level, not on stairs', [r for r in DR if r['scary'] and r['grid'] != 'stairs']),
    ('when: an awake monster seen within 20', [r for r in DR if r['age_awake'] <= 20]),
    ('when: an awake monster seen within 50', [r for r in DR if r['age_awake'] <= 50]),
    ('when: after two interruptions on one grid', same),
]
for lab, rs in rules:
    print(f"| {lab} | {len(rs)} | {sum(inter(r) for r in rs)} ({pct(sum(inter(r) for r in rs),len(rs))}) | {sum(r['why']=='attacked' for r in rs)} | {deaths_after(rs)} |")
base = DR
print(f"| (all dungeon rests) | {len(base)} | {sum(inter(r) for r in base)} ({pct(sum(inter(r) for r in base),len(base))}) | {sum(r['why']=='attacked' for r in base)} | {deaths_after(base)} |")
