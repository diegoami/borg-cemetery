# A floating eye's paralysis lock — Half-Elf Necromancer 453254028

Analysis pass: 2026-11-23.
- **Run.** A local replay from birth of one of the 20 level-1 death starts of [#138](https://github.com/diegoami/borg-cemetery/pull/138). Harness run, 100,000 turns, borg-rs core, shipped settings.
- **Build.** borg-reborn-rs [`d8b55d64`](https://github.com/diegoami/borg-reborn-rs/commit/d8b55d647ec941676ac2449ad97a786ecf8f235f), PR [borg-reborn-rs#1117](https://github.com/diegoami/borg-reborn-rs/pull/1117), clean source.
- **Reproduction.** Verified with `scripts/native/rerun-death.py`: keys, messages, states and the endpoint match.

**One death, one game.** The same key stream also died in that study's `explore_mixed = 1` arm (same start), which is not a separate death. The game split from the `explore_bfs_leave_when_done = 0` arm at turn 2,082; that arm lived to the cap.

## What happened
1. **Turns 77,029–77,419, a loop.** For about 400 game turns the Borg alternated between `Flowing toward dark-bfs (ring 3)` and `Flowing toward targetable position`, next to a floating eye at (43,88).
2. **Turns 77,419–77,449, the eye forgotten.** It was forgotten and re-created at the same grid every think (`Forgetting a monster 'floating eye' at (43,88)`), although it never moves. The breadth-first flow then stepped to (42,89), next to it.
3. **Turn 77,453, the lock.** First gaze, at 29/29 HP: `You are paralysed!`.
   - The eye has the Borg's speed (110). It gazes as each paralysis ends, so the Borg was paralysed almost all the time.
   - It acted only when a saving throw succeeded ("You resist the effects!").
   - A gaze on a paralysed player does at least 1 damage, so HP fell 1–2 a gaze: 29 → 7 by turn 77,789.
4. **Turn 77,789, the one decision, at 7/29 HP.**
   - `Danger:p=200`, then `Phase rule: danger 0 without fear (with fear 200)`.
   - `enemy adjacent but the fight is not lost (danger 0, HP 7): no Phase Door; other escapes, else fight`.
   - It attacked with a Main Gauche (1d5). Paralysed again, it died at 77,923.

**One step to a grid not next to the eye would have ended it.** The eye has `NEVER_MOVE`.

## The engine (574b618c)
- `monster.txt:694`: floating eye, `speed:110`, `blow:GAZE:PARALYZE` (no dice), `NEVER_MOVE`, depth 1.
- `mon-blows.c:1017-1025`: paralysis for 3 + 1d(rlev) turns, resisted by Free Action, and at least 1 damage per blow while paralysed.
- `player_timed.txt:216-222`: `PARALYZED` is `NONSTACKING`.

Without Free Action, standing next to a paralyser of equal speed is a lost fight at any HP.

## Why the Borg stayed
- **The danger model counts the gaze as 0** (`borg_danger.rs:479`, `MONBLOW_PARALYZE`: dice 0, plus a fear term). The Phase rule reads the danger without fear, so "the fight is not lost".
- **The step-away is shipped off.** `caution_ranged_vs_immobile` mode 2 (borg-reborn-rs#713) would keep it at range and step away, but ships 0 (owner, 2026-11-20).
- **The scary list's entry is not enforced.** `floating eye | 50 | | ranged | paralysing-gaze`, but `caution_ranged_only` ships 0 (borg-reborn-rs#838, #852).
- **A never-moving monster out of view is forgotten,** so no path cost kept the flow out of its reach.

## Proposed work
- [borg-reborn-rs#1125](https://github.com/diegoami/borg-reborn-rs/issues/1125) (owner: "from paralyzing monsters it is necessary to walk away"):
  - next to a paralyser without Free Action, the fight is lost;
  - step out of a never-moving one's reach first;
  - no flow into its reach;
  - remember never-moving monsters.
- [borg-reborn-rs#852](https://github.com/diegoami/borg-reborn-rs/issues/852): the ranged-only scary entries.
- **Replay check:** this seed from birth, each switch on against off. A single replay is one start, not a rate (borg-reborn-rs RULES 14).
