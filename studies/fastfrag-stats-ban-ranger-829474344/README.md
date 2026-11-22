# Half-Troll Ranger 829474344: 132 touches of a white jelly in a retreat / stair-flight loop (stats-ban arm)

The death [D-87e4851831ce](../../deaths/D-87e4851831ce1b7c8ac10bf7f6714bf48a1487eda3f1e042c9ad5da080fb799f/README.md)
(imported by borg-cemetery#109) of borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466), experiment
`reborn-fast-fragile-big` ([borg-zoo#596](https://github.com/diegoami/borg-zoo/issues/596)), specimen
`4.2.6-reborn-rust-fast-fragile-7f8c6b80` (borg-reborn-rs `7f8c6b80`), arm `reborn-fastfrag-stats-ban`
(`fast_fragile_policy = 1`, `fast_fragile_by_stats = 1`, `fast_fragile_no_heal = 1`). Half-Troll
Ranger (race 7, class 7), seed 829474344, killed by poison at game turn 96,820, CL8, DL2 (max DL4),
max HP 96, 16,652 keys. The control arm `reborn-fastfrag-ctl` lives to the 100,000-turn cap.

**One life, one start.** A direction, not a rate (borg-reborn-rs RULES 14). Tools, method and the
engine rules shared with the other case of this run are in
[fastfrag-stats-ban-necromancer-798380952](../fastfrag-stats-ban-necromancer-798380952/README.md).

## Summary

- **The game parts from the control at key 239** (game turn 1,246, CL1). The stats rule marks a
  metallic red centipede fast-fragile ("speed +12 vs +0, 13 HP vs 10.7 per turn"), and the Borg melees
  it where the control reads Phase Door. From there on it is another game. 95,000 turns later the
  death is not the policy acting: no fast-fragile note appears in the fatal loop, and a white jelly
  cannot be marked (`NEVER_MOVE`).
- **The death is a two-step loop between two rules that exist in the control too.** The Borg is
  fleeing (a cutpurse on the level keeps it "scary") and is down to melee only (no arrows since turn
  79,741).
  - On the square next to the jelly, `borg_caution`'s strategic retreat steps away (danger 36 >
    avoidance/3).
  - On the square one step away (danger 0), the threat-weighted stair flight of #765 steps back next
    to the jelly. The jelly sits by the route, and the weight prices its touch at under 2 extra steps.

  This repeats from 95,170 to 96,780: 164 thinks (74 retreats, 77 stair steps), 132 touches, 12 Cure
  Light Wounds and 3 Neutralize Poison. The poison counter climbs to 534.
- **Cure Light Wounds does not cure poison** in this game. After the third and last Neutralize Poison
  (95,320) each touch adds 5 + 1d2 turns of poison, and poison stops regeneration. The death is the
  accumulated poison, not one touch.
- **Counterfactuals.** Two melee rounds destroy the jelly (36 HP, AC 1). Meleeing it from any of eight
  thinks between 95,170 and 96,050 saves this life (alive at the cap). From 96,150 on (poison 303)
  the Ranger dies of the poison it already carries, even after killing the jelly.

## Reproduction

| what | value |
|---|---|
| zoo cell | `classes-1800-big/4.2.6-reborn-rust-fast-fragile-7f8c6b80/reborn-fastfrag-stats-ban/829474344`, artifact `deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-1` |
| build | the zoo's build artifact (binary `6098359c7072…`) |
| configuration | the cell's written `user/borg.txt`, `configurations/51b1004a3680….txt`; control `a5cfee0cf3a2….txt` (the three switches differ) |
| command | [`../fastfrag-stats-ban-necromancer-798380952/tools/run-cell.sh`](../fastfrag-stats-ban-necromancer-798380952/tools/run-cell.sh) (the zoo's `command()`), from birth, no save |
| stats-ban | keys.log `798335ae2821113e…` = the cell's `play_sha256`; messages.log `24bb3cc5…` and state.log `3bd31975…` byte-equal to the bundle |
| control | keys.log `689e1ca56038f6a7…` = its cell's `play_sha256`; alive at 100,000, CL7, max DL4 |
| first differing key | 239 (game turn 1,246) |

## The white jelly (engine)

`lib/gamedata/monster.txt:959-974`:
- speed 120, HP 36, AC 1, sleepiness 99, depth 2;
- `TOUCH:POISON:1d2`;
- `NEVER_MOVE`, `HURT_LIGHT | IM_POIS | HURT_COLD | NO_CONF | NO_SLEEP`.

A touch:
- cannot cut or stun (`lib/gamedata/blow_methods.txt:23-30`);
- deals poison damage reduced by `adjust_dam` (`src/mon-blows.c:417-470`, `674-690`);
- adds **5 + 1d(monster level = 2) turns** of `TMD_POISONED` (`src/mon-blows.c:682-686`).

Poison:
- costs 1 HP per world tick, every 10 game turns (`src/game-world.c:513-519`, `1080-1081`);
- stops HP regeneration (`src/player-util.c:467`);
- falls by `adj_con_fix + 1` per tick (`src/game-world.c:282`).

What cures it:
- Neutralize Poison (`lib/gamedata/object.txt:3278-3287`) and Cure Critical Wounds
  (`object.txt:3192-3206`) cure poison;
- Cure Light Wounds (`object.txt:3156-3172`) and Cure Serious Wounds (`object.txt:3175-3190`) do not.

## Where and how the loop runs

Coordinates x,y as in `state.log`; the Borg's notes print y,x. Two screens: before the jelly wakes
([after key 16,282](data/screen-after-key-16282.txt)) and at HP 4
([after key 16,646](data/screen-after-key-16646.txt)). The map around it:

```
x:   92 93 94 95 96 97
y12   #  .  #  #  #         <- the corridor north (the retreat's target 12,93)
y13   #  .  .  @  .         <- the Borg alternates x94 / x95
y14   #  .  .  .  j  #      <- the jelly at x96,y14
y15   #  .  #  #  .  #      <- two corridors south, x93 and x96
```

The jelly touches x95,y13 and x95,y14. The whole loop is in [data/loop.tsv](data/loop.tsv), one line
per think: position, HP, poison, danger, check, keys and note.

| think | turn | Borg x,y | HP | poison | danger | check | choice |
|---|---|---|---|---|---|---|---|
| 9236 | 95,160 | 94,14 | 96 | 0 | 0 | `borg_flow_stair_both` | "Flowing toward stairs at cost 35" (key `9`) |
| 9237 | 95,170 | 95,13 | 96 | 0 | 72 | `borg_caution` | "Retreating to 12,93 (distance 2) via 13,94 (72 > 0)"; "The white jelly wakes up." |
| 9238 | 95,180 | 94,13 | 96 | 0 | 0 | `borg_flow_stair_both` | "Flowing toward stairs at cost 36"; touch, "You are poisoned!" |
| 9239 | 95,190 | 95,13 | 95 | 6 | 36 | `borg_caution` | "Retreating to 15,93 (distance 2) via 14,94 (36 > 0)" |
| 9240 | 95,200 | 94,14 | 94 | 4 | 0 | `borg_flow_stair_both` | stair step back; touch |
| … | | | | | | | the same pair, about every 20 game turns |
| 9244 | 95,240 | 94,13 | 87 | 9 | 0 | `borg_recover` | Neutralize Poison (also 95,270; the last at 95,320) |
| 9361 | 96,410 | 95,13 | 65 | 388 | 36 | `borg_caution` | the last Cure Light Wounds (12 in the loop, from 95,400) |
| 9380 | 96,600 | 95,13 | 45 | 463 | 36 | `borg_caution` | "Retreating to 13,94 (distance 1) via 13,94 (36 > 0)" |
| 9398 | 96,780 | 95,13 | 4 | 534 | 36 | `borg_caution` | retreat |
| 9399 | 96,790 | 94,13 | 3 | 532 | 0 | `borg_flow_stair_both` | "Flowing toward stairs at cost 95": at HP 3 the weight sends it to another staircase |
| | 96,820 | | −1 | | | | "You die." (poison) |

Counts from 95,170 to death: 74 "Retreating", 77 "Flowing toward stairs", 132 touches, 12 Cure
Light Wounds, 3 Neutralize Poison (the last one; "You have no more Potions of Neutralize Poison" at
95,320).

At HP 4 ([inventory](data/inventory-after-key-16645.txt)) the Ranger still carried:
- 2 Phase Door;
- three unknown wands (Rusty, Steel, Gold), never aimed;
- 11 unknown potions and 11 unknown scrolls;
- no arrows, no flasks, no cure for poison.

### The two rules

1. **The strategic retreat** (`borg-core/src/borg_caution.rs:2896-2913`, `retreat` at `:1131-1340`).
   - It moves when `danger_test` holds: `pos_danger > avoidance / caution_retreat_danger_divisor (3)`,
     36 > 32 at full HP, and more as HP falls. `may_move_away` must allow it (`:1799-1818`).
   - It picks a grid of lower danger (0) within reach. "Retreating to 15,93 … via 14,94" even aims at
     the x93 corridor south, but it is a one-step move, and the next think is the stair flight's.
   - Its one exemption is a lone adjacent monster that **one blow** kills
     (`borg_adjacent_kill_in_one_blow`, `:1817`, `:1820-1840`). The comment there describes this very
     case: "retreating hands the initiative back and lets a flee route walk straight back into
     reach". The jelly takes two rounds, so the exemption does not apply.
2. **The threat-weighted stair flight** (#765; `borg-core/src/borg_caution.rs:5271-5275`,
   `caution_stairs_flight_threat_weight = 5`, `params.rs:206`).
   - Each entered grid costs one step plus weight × danger / current HP. At HP 96 the jelly's touch
     grid costs 1 + 5 × 36 / 96 ≈ 2.9 steps, so the route past the jelly stays the cheapest.
   - Awake monster grids are blocked, but the grids next to a monster that never moves are only
     priced.
   - At HP 3 the same weight makes that grid cost 61 steps, and the Borg turns to a staircase at cost
     95, too late.

Neither rule sees the other. No anti-bounce check covers a cycle between `borg_caution` and the stair
flow (`bouncing` only filters retreat targets).

### Why it never attacked the jelly

- The level stays scary for the whole loop: "Scary guy on level." on every think.
  - A cutpurse is on the scary list at `8-11` (`scary_monsters.txt`). For a Ranger (fragility 33) that
    means scary up to CL 9; this Ranger is CL8.
  - The cutpurse was last seen at 95,090 ("Forgetting a monster 'cutpurse'"), but the flag lasts the
    level (`borg_update.rs:1919` clears it on a new level).
- In flight there is no hunting.
- On the touch square, `borg_caution` (`borg_think_dungeon.rs:797`) retreats before anything else.
- One step away, no attack reaches: every candidate in the core trace is `nonpositive_return`. There
  are no arrows ("You have no more Arrows" at 79,741) and no flasks (none since 67,437). The wands are
  unknown.

The fast-fragile code cannot mark the jelly (`NEVER_MOVE`, `borg_fast_fragile.rs:118-123`), and
`caution_ranged_vs_immobile` is 0 in this arm (#646, #713, #838).

## Healing

All 12 Cure Light Wounds went to HP (+20 each); none can touch the poison (above). The Borg's
contact decisions do not count the poison it carries:
- the retreat's and the flight's danger price the jelly's next touches, not the 300–530 turns of
  poison already running;
- at 96,150 (HP 82, poison 303) that poison alone is fatal without a cure for poison, as R02 shows.

## Where the game parts from the control (Q6)

Key 239, game turn 1,246, CL1, DL1, HP 17/17:
- **stats-ban**: "Fast-fragile (stats): metallic red centipede (speed +12 vs +0, 13 HP vs 10.7 per
  turn, 6.3 damage/turn = 37% of HP 17, 0 others in view) (#842)", "Attack on sight: … attack 1",
  melee with the Main Gauche.
- **control**: "Phase rule (from escape 3.1 danger): enemy adjacent and the fight looks lost (danger
  18, HP 17)", Phase Door.

| policy | by_stats | no_heal | keys.log | end |
|---|---|---|---|---|
| 0 | 0 | 0 | `689e1ca56038…` | alive (control cell) |
| 0 | 0 | 1 | `689e1ca56038…` | alive |
| 0 | 1 | 1 | `689e1ca56038…` | alive |
| 1 | 0 | 0 | `689e1ca56038…` | alive |
| 1 | 0 | 1 | `689e1ca56038…` | alive |
| 1 | 1 | 0 | `798335ae2821…` | died 96,820, poison |
| 1 | 1 | 1 | `798335ae2821…` | died 96,820 (stats-ban cell) |

([data/variants.tsv](data/variants.tsv).) Only `policy = 1` with `by_stats = 1` gives this game; the
heal ban plays no part. The split is the policy acting at CL1; the death is the loop above, which the
control's code has as well.

## Counterfactuals on the exact game

Same method as the other case: the same Borg plays from birth. After the given key, the hook attacks
the adjacent jelly every turn until none is adjacent (`melee:white jelly`), then hands back to the
same Borg. ([data/counterfactuals.tsv](data/counterfactuals.tsv).)

| case | after key (turn) | HP, poison at the start | jelly | HP when the Borg takes over | end |
|---|---|---|---|---|---|
| R01 | 16,282 (95,170) | 96, 0 | destroyed 95,180 (two rounds) | 91 | **alive**, cap |
| R06 | 16,313 (95,310) | 79, 22 | destroyed 95,320 | 73 | alive, cap |
| R07 | 16,342 (95,430) | 79, 35 | destroyed 95,440 | 77 | alive, cap |
| R08 | 16,369 (95,540) | 71, 85 | destroyed 95,550 | 67 | alive, cap |
| R09 | 16,397 (95,670) | 64, 134 | destroyed 95,680 | 60 | alive, cap |
| R10 | 16,427 (95,790) | 77, 174 | destroyed 95,800 | 73 | alive, cap |
| R11 | 16,454 (95,920) | 71, 215 | destroyed 95,930 | 66 | alive, cap |
| R12 | 16,482 (96,050) | 66, 261 | destroyed 96,060 | 62 | alive, cap |
| R02 | 16,508 (96,150) | 82, 303 | destroyed 96,160 | 80 | died 97,600, poison |
| R03 | 16,608 (96,600) | 45, 463 | destroyed 96,620 | 37 | died 97,010, poison |
| R04 | 16,633 (96,720) | 18, 505 | destroyed 96,730 | 13 | died 96,870, poison |
| R05 | 16,641 (96,760) | 9, 524 | destroyed 96,770 | 5 | died 96,830, poison |

The jelly dies in two melee rounds from any start. The Ranger lives when it kills it before about
turn 96,100, while the poison counter is below about 260 (261 at 96,050 lives, 303 at 96,150 dies). After that the carried poison outlasts its
cures.

## Defects (borg-reborn-rs; each a lead until the zoo measures it)

- [borg-reborn-rs#928](https://github.com/diegoami/borg-reborn-rs/issues/928): the strategic
  retreat and the threat-weighted stair flight (#765) undo each other beside a monster that never
  moves. Decisive here, and in the control's code.
- [borg-reborn-rs#926](https://github.com/diegoami/borg-reborn-rs/issues/926): the Borg's own damage
  over time (the cut there, the poison here) is not in its escape and contact decisions.

## Repeat on borg-reborn-rs `track-p` (`e2d8919e`, 2026-11-22)

The analysis above is of the zoo specimen `7f8c6b80`. `track-p` head `e2d8919e` is 242 commits ahead
of it (main `b34196c5` is 137 ahead), and it ships `fast_fragile_policy = 1`,
`fast_fragile_no_heal = 1` and `fast_fragile_by_stats = 0`.

I built `e2d8919e` (`harness/build.sh`) and played the same start from birth, as the zoo writes the
cell: `track-p`'s `harness/borg.txt` with `borg_respawn_race`/`_class` set. I played it at three
settings ([data/track-p-e2d8919e.tsv](data/track-p-e2d8919e.tsv)):
- shipped (1, 0, 1);
- ctl (0, 0, 0);
- stats-ban (1, 1, 1).

**Every run lives to the 100,000 cap.** On `track-p` this start plays another game from early on,
and the fatal situation of this case never arises. In none of the runs is there a "the next turn
kills" note, a heal-ban note or a white jelly touch.

That is not evidence that the defects are fixed. The code behind them is unchanged on `track-p`:
- `escape_wanted` counts only the monsters' blows (`borg_fast_fragile.rs:89-91`);
- the #842 gate is still `hp >= 0` (`borg_caution.rs:2830-2831`);
- the #760 gate is still the mean damage against HP (`borg_caution.rs:2804-2806`);
- `fight_before_flight` still comes before `borg_caution` (`borg_think_dungeon.rs:755`, `815`);
- the wall walk still starts at the Borg's grid (`borg_projection.rs:789`);
- the stair-flight threat weight is still 5.

The fast-fragile Phase Door now goes through the shared `phase_door` decision, with the landing test
off by default (`fast_fragile_phase_landing = 0`), so at HP 0 it is still read. With the policy and
the ban now shipped, borg-reborn-rs#926's path is in the default play of `track-p`.
