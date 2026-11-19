"""#615 analysis: every rest (R keypress at a rest site), its kind, grid, outcome."""
import json, glob, os, re, sys, collections
D = sys.argv[1]
ATTACK = re.compile(r'(hits|bites|claws|stings|touches|kicks|butts|crushes|engulfs|crawls on|drools on|spits on|gazes at|wails at|releases spores at|begs you|insults you|moans|casts|breathes|fires|shoots|throws|You are hit|You feel|grabs|squeezes) ')
KIND = [('# Resting to recover HP/SP', 'hp'), ('# Resting to gain Mana', 'mana'), ('# Resting to recharge a rod', 'rod'),
        ('# Resting for Recall', 'recall'), ('# Waiting for Recall', 'recall'), ('# Resting on stair to gain Mana', 'stair-mana'),
        ('# Resting on town stair', 'stair-mana'), ('# Resting on this Glowing Grid', 'glow'), ('# Waiting for towns people', 'town-scum'),
        ('# Resting on grid', 'morgoth')]
FEAT_LESS, FEAT_MORE = 5, 6
rows = []
games = {}
for rests in sorted(glob.glob(f'{D}/*.rests')):
    seed = os.path.basename(rests)[:-6]
    g = f'{D}/{seed}'
    try:
        sm = json.load(open(f'{g}/summary.json'))
    except Exception:
        continue
    games[seed] = sm
    tr = [json.loads(l) for l in open(f'{g}/trace-core.jsonl')]
    by_turn = collections.defaultdict(list)
    for i, t in enumerate(tr):
        if 82 in t['keys']:
            by_turn[t['turn']].append(i)
    msgs = []
    for l in open(f'{g}/messages.log', errors='replace'):
        p = l.rstrip('\n').split(' ', 3)
        if len(p) == 4 and p[1].isdigit():
            msgs.append((int(p[0]), int(p[1]), p[3]))
    notes_at = collections.defaultdict(list)
    for k, t, m in msgs:
        if m.startswith('# '):
            notes_at[t].append(m)
    # state.log: key count -> pos, depth
    st = []
    for l in open(f'{g}/state.log'):
        p = l.split()
        st.append((int(p[0]), p[1], p[2]))
    used = collections.Counter()
    for line in open(rests):
        p = line.split()
        T = int(p[0])
        kv = dict(x.split('=') for x in p[1:])
        kind = 'other'
        for m in reversed(notes_at.get(T, [])):
            hit = [k for pre, k in KIND if m.startswith(pre)]
            if hit:
                kind = hit[0]
                break
        idx = by_turn.get(T, [])
        j = used[T]; used[T] += 1
        i = idx[min(j, len(idx) - 1)] if idx else None
        nxt = tr[i + 1] if i is not None and i + 1 < len(tr) else None
        cur = tr[i] if i is not None else None
        feat = int(kv['feat']); passn = int(kv['pass'])
        if feat in (FEAT_LESS, FEAT_MORE): grid = 'stairs'
        elif passn <= 1: grid = 'dead end'
        elif passn == 2: grid = 'corridor'
        elif passn <= 4: grid = 'room edge/junction'
        else: grid = 'open room'
        out = 'unknown'; why = ''
        dur = None
        if nxt:
            dur = nxt['turn'] - T
            between = [m for k, t, m in msgs if T < t <= nxt['turn'] and not m.startswith('#')]
            attacked = any(ATTACK.search(m) and 'you' in m.lower() for m in between) or nxt['hp'] < cur['hp']
            full = nxt['hp'] >= nxt['max_hp'] and nxt['sp'] >= nxt['max_sp']
            if nxt['depth'] != cur['depth']:
                out, why = 'level change', ''
            elif attacked:
                out, why = 'interrupted', 'attacked'
            elif nxt['danger'] > 0 and not full:
                out, why = 'interrupted', 'monster'
            elif full:
                out = 'complete'
            elif kind in ('recall', 'town-scum', 'glow', 'other', 'morgoth'):
                out = 'complete' if nxt['danger'] <= 0 else 'interrupted'
                why = 'monster' if out == 'interrupted' else ''
            else:
                out, why = 'stopped short', 'other'
        # state at this key count
        key = None
        for k, t, m in msgs:
            if t == T:
                key = k; break
        pos = None
        if key is not None:
            for k, ps, dep in st:
                if k <= key: pos = (ps, dep)
                else: break
        rows.append(dict(seed=seed, cls=sm['class'], T=T, kind=kind, grid=grid, unknown=int(kv['unknown']), doors=int(kv['closed']) + int(kv['open']),
                         scary=kv['scary'] == 'true', fleeing=kv['fleeing'] == 'true', depth=int(kv['depth']), age_awake=int(kv['age_awake']),
                         near_awake=int(kv['near_awake']), hp=kv['hp'], sp=kv['sp'], out=out, why=why, dur=dur, pos=pos,
                         danger_next=nxt['danger'] if nxt else None))
json.dump(dict(rows=rows, games={s: dict(cls=g['class'], race=g['race'], stop=g['stop_reason'], turns=g['game_turns'], cl=g['clevel']) for s, g in games.items()}),
          open(f'{D}/rests.json', 'w'))
print(len(games), 'games', len(rows), 'rests')
