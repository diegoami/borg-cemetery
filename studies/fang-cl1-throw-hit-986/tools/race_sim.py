"""Rough Monte Carlo of the Paladin's race against Fang, fought to the end with no cures.
Engine numbers: oil hits at 67.70% (measured), 1d4 x 9 a hit (seen: 9, 27, 36; criticals
ignored); Fang 2 bites per player turn (speed +20), 1d4 each at ~95%. Fang moves RAND_25
in the engine; this ignores that. A death is HP below zero (both sides)."""
import random
def sim(hp, fang, p=0.677, bite=0.95, n=200000):
    win = 0
    for _ in range(n):
        h, f = hp, fang
        while True:
            if random.random() < p: f -= 9 * random.randint(1, 4)
            if f < 0: win += 1; break
            for _ in range(2):
                if random.random() < bite: h -= random.randint(1, 4)
            if h < 0: break
    return win / n
random.seed(1)
for hp, fang in [(11, 25), (11, 16), (10, 16), (11, 17)]:
    print(hp, fang, round(sim(hp, fang), 3))
