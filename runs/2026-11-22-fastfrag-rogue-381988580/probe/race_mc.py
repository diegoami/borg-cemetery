# Approximate simulations for the case README, questions 3 and 5. Run: python3 -I race_mc.py
# Monte Carlo of the 62,892 melee using the engine's rules (574b618c):
# player-attack.c:174-219 hit_chance (12% auto hit, 5% auto miss, roll 0..to_hit-1 >= ac*2/3),
# player-attack.c:990-1020 blows limited by energy, game-world.c:80-81 extract_energy,
# mon-attack.c:540-543 adjust_dam_armor. Criticals ignored (dagger crit ~1%).
import random, sys
def hit(to_hit, ac, r):
    k = r.randrange(100)
    if k < 12: return True
    if k >= 95: return False
    return r.randrange(max(9, to_hit)) >= ac * 2 // 3
def fight(r, hp, foes, join_turn):
    pe = 102; mons = [[28, 27, 0], [22, 23, join_turn]]  # hp, energy, earliest game-turn offset to engage
    mons = mons[:foes]
    t = 0
    while t < 2000:
        t += 1
        pe += 10
        for m in mons: m[1] += 19
        if pe >= 100:
            alive = [m for m in mons if m[0] > 0 and t >= m[2]]
            if not alive: return True
            tgt = alive[0]; used = 0
            while 100 - used >= 36 and tgt[0] > 0:
                if hit(80, 24, r): tgt[0] -= r.randint(1, 4) + 2
                used += 36
            pe -= used
            if all(m[0] <= 0 for m in mons): return True
        for m in mons:
            if m[0] > 0 and m[1] >= 100 and t >= m[2]:
                m[1] -= 100
                for _ in range(2):
                    if hit(46, 28, r):
                        d = r.randint(1, 7); hp -= d - d * 28 // 400
                if hp <= 0: return False
    return True
r = random.Random(1)
N = 100000
for foes, join, label in ((1, 0, 'one soldier (the race as computed)'), (2, 10, 'both soldiers, the second joining after one rogue turn')):
    for hp in (31, 23):
        w = sum(fight(r, hp, foes, join) for _ in range(N))
        print(f"{label}, rogue HP {hp}: wins {100*w/N:.1f}%")

def seq(r, hp, s1, s2):
    # one soldier at a time at the corridor mouth; the second steps in after the first dies
    pe = 102; mons = [[s1, 27], [s2, 23]]; t = 0
    while t < 4000:
        t += 1; pe += 10
        for m in mons: m[1] += 19
        cur = [m for m in mons if m[0] > 0]
        if not cur: return True
        m = cur[0]
        if pe >= 100:
            used = 0
            while 100 - used >= 36 and m[0] > 0:
                if hit(80, 24, r): m[0] -= r.randint(1, 4) + 2
                used += 36
            pe -= used
            if m[0] <= 0: m[1] = 0; continue  # the next one has to step up
        if m[0] > 0 and m[1] >= 100:
            m[1] -= 100
            for _ in range(2):
                if hit(46, 28, r):
                    d = r.randint(1, 7); hp -= d
            if hp <= 0: return False
    return True
def walk(r, hp, steps):
    # rogue steps away each 10 game turns; the adjacent hasted soldier needs one move to re-close, then attacks
    pe = 100; me = 60; t = 0; adjacent = True; left = steps
    while left > 0:
        t += 1; pe += 10; me += 19
        if pe >= 100:
            pe -= 100; left -= 1; adjacent = False
            if left == 0: return True
        if me >= 100:
            me -= 100
            if not adjacent: adjacent = True
            else:
                for _ in range(2):
                    if hit(46, 28, r):
                        d = r.randint(1, 7); hp -= d
                if hp <= 0: return False
    return True
print("sequential (corridor), HP 31 vs 28 then 22:", f"{100*sum(seq(r,31,28,22) for _ in range(N))/N:.1f}%")
print("sequential (corridor), HP 23 vs 23 then 22:", f"{100*sum(seq(r,23,23,22) for _ in range(N))/N:.1f}%")
print("first soldier only, HP 23 vs 23:", f"{100*sum(seq(r,23,23,0) for _ in range(N))/N:.1f}%")
print("walk 13 steps to '<' from HP 23:", f"{100*sum(walk(r,23,13) for _ in range(N))/N:.1f}%")
print("walk 13 steps to '<' from HP 31:", f"{100*sum(walk(r,31,13) for _ in range(N))/N:.1f}%")
