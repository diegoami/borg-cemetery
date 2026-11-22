# branch.py DIR TURN: min HP, level change, soldiers slain and death after TURN in one branch.
import sys, re
d = sys.argv[1]; t0 = int(sys.argv[2])
st = [l.split() for l in open(d + '/state.log') if not l.split()[1] == '-']
minhp = 999; dep0 = None; left = None; end = None
for f in st:
    t = int(f[0])
    if t < t0: continue
    hp = int(f[3][2:].split('/')[0]); dep = int(f[2][1:].split('/')[0])
    if dep0 is None: dep0 = dep
    if t <= t0 + 1500: minhp = min(minhp, hp)
    if left is None and dep != dep0: left = (t, dep)
msgs = [l.rstrip('\n') for l in open(d + '/messages.log')]
kills = [m for m in msgs if 'slain the soldier' in m and int(m.split()[1]) >= t0]
dead = [m for m in msgs if 'You die' in m]
print(f"{d.split('/')[-1]}: min HP in 1500 turns {minhp}; level left at {left}; soldiers slain {len(kills)} {[k.split()[1] for k in kills][:3]}; death {dead[0].split()[1] if dead else '-'}")
