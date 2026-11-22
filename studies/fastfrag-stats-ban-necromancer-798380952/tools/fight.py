"""Turn-by-turn table of a fight from a run's messages.log, state.log and trace-core.jsonl.
usage: fight.py RUNDIR T0 T1 [FOE]"""
import json, re, sys
run, t0, t1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
foe = sys.argv[4] if len(sys.argv) > 4 else None
thinks = [json.loads(l) for l in open(run + '/trace-core.jsonl')]
thinks = [d for d in thinks if t0 <= d['turn'] <= t1]
msgs = [l.rstrip('\n').split(' ', 3) for l in open(run + '/messages.log')]
msgs = [(int(m[0]), int(m[1]), m[3]) for m in msgs if len(m) == 4]
state = [l.split() for l in open(run + '/state.log')]
def st_at(turn):
    rows = [s for s in state if int(s[0]) <= turn]
    s = rows[-1]
    t = s[9]
    cut = re.search(r'8:(\d+)', t); poi = re.search(r'7:(\d+)', t)
    return s[1], s[3], s[4], cut.group(1) if cut else '-', poi.group(1) if poi else '-'
print('| think | turn | keys | Borg x,y | HP | SP | cut | poison | check | Borg notes (choice) | game messages until the next think |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for i, d in enumerate(thinks):
    nxt = thinks[i + 1]['turn'] if i + 1 < len(thinks) else t1 + 1
    pos, hp, sp, cut, poi = st_at(d['turn'])
    notes = [m[2][2:] for m in msgs if m[1] == d['turn'] and m[2].startswith('# ') and not re.match(r'# (HIT_BY|MISS_BY|PAIN|QUAKE|MISS|HIT|KILL):', m[2])]
    notes = [n for n in notes if not n.startswith(('Scary guy', 'Fleeing and leaving the level. (scaryguy)', 'There was', 'Forgetting', 'Removing Regional'))]
    game = [m[2] for m in msgs if d['turn'] <= m[1] < nxt and not m[2].startswith('#') and m[2].strip() not in ('', 'Target Selected.')]
    keys = ''.join(chr(k) if 32 < k < 127 else ('ESC' if k == 57344 else f'<{k}>') for k in d['keys'])
    kidx = [m[0] for m in msgs if m[1] == d['turn']]
    print(f"| {d['think']} | {d['turn']} | `{keys}` (after key {min(kidx) if kidx else '?'}) | {pos} | {hp[2:]} | {sp[2:]} | {cut} | {poi} | {d['check']} | {'; '.join(notes)[:420]} | {' '.join(game)[:300]} |")
