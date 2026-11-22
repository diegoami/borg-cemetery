# A white jelly, a ghost soldier and a two-rule loop: Half-Troll Ranger 829474344

Investigation of one death of the `reborn-fastfrag-stats-ban` arm of borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466)
(experiment `reborn-fast-fragile-big`, [borg-zoo#596](https://github.com/diegoami/borg-zoo/issues/596),
specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`, borg-reborn-rs
[`7f8c6b80`](https://github.com/diegoami/borg-reborn-rs/commit/7f8c6b80a617eba3a6f2b83e4ba9d45b7b552b73)).
Dossier: [D-87e4851831ce](../../deaths/D-87e4851831ce1b7c8ac10bf7f6714bf48a1487eda3f1e042c9ad5da080fb799f/README.md);
run page: [runs/2026-11-22-fastfrag-stats-ban](../../runs/2026-11-22-fastfrag-stats-ban/README.md)
(both arrive with borg-cemetery#109, on which this study is stacked).

Half-Troll Ranger (race 7, class 7), seed 829474344, CL8, killed by poison on DL2 (max DL4)
at game turn 96,820, max HP 96, 16,652 keys. The core is borg-rs's (`borg_reborn_core =
borg-rs`, `borg-core/` at `7f8c6b80`). Arm settings on top of the shipped `harness/borg.txt`:
`fast_fragile_policy = 1`, `fast_fragile_by_stats = 1`, `fast_fragile_no_heal = 1`. The
control arm (`reborn-fastfrag-ctl`) lives to the 100,000-turn cap.

**One life, one start.** Every counterfactual below continues the same game. It shows what
this game needed, not a rate (RULES 12/14 of borg-reborn-rs). Thresholds named below are
hypotheses until borg-zoo measures them.

## In short

- From 95,170 to 96,820 two rules alternate every player turn: the strategic **retreat**
  (`borg_caution`) steps out of the jelly's reach, and the **stair flight**
  (`borg_flow_stair_both`) steps back next to it. 74 retreats, 77 flight steps, 132 touches,
  45 misses. The poison counter climbs to 534 and the Borg dies at HP 0, still in the loop.
- **The level is "scary" because of a ghost.** The only scary monster in the Borg's memory
  is a soldier "asleep at (11,86)". In the engine that soldier woke, walked to the Borg and was
  killed by it at 94,379. The Borg had opened a second record for it and never dropped the
  first one (`evidence/monster-records.txt`).
- **The ghost also prices the real way out.** The true route to the only known staircase
  (33 steps, north-west along row 11) passes the ghost's square, where the danger map reads
  79–172. The weighted flight instead takes a 36-step route east past the jelly and on through
  squares it has never seen. In the true map they are granite (borg-reborn-rs#881's phantom route).
- **The jelly was never attacked.** Next to it, `borg_caution` retreats before `borg_attack`
  runs. Two squares away, nothing reaches: no arrows (spent at 79,741), and the Magic Missile
  wand is unidentified, and unknown wands are never aimed (`BF_WAND_UNKNOWN => 0`). Melee kills
  the 25-HP jelly in two player turns (D1). One zap of the wand teaches the Borg the wand, and
  then it kills the jelly itself (B1).
- **Poison is a flag, not a quantity.** The Borg drank 3 Neutralize Poison while still in the
  loop and 12 Cure Light Wounds (no poison cure in 4.2). It never read its 2 Phase Doors,
  because the retreat always comes first. A Phase Door saves the game up to 96,100, not from
  96,200.
- The arm parts from the control at keys.log line 239 (game turn 1,246, CL1). The death is
  95,000 game turns downstream of the policy's only decision, in an unrelated level.

## Reproduction

- **Bundle:** zoo artifact `deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-1`, cell
  `classes-1800-big/4.2.6-reborn-rust-fast-fragile-7f8c6b80/reborn-fastfrag-stats-ban/829474344`
  (keys, messages and state logs, the full `trace-core.jsonl` of 9,402 thinks, `user/borg.txt`).
  Its log hashes equal the dossier's `record.json`.
- **Build:** borg-reborn-rs `7f8c6b80`, `BORG_IMPL=rust harness/build.sh` (engine
  `574b618c`), with the zoo's own binary from artifact `build-4.2.6-reborn-rust-fast-fragile-7f8c6b80`
  (sha256 `6098359c…`, the dossier's) put in `build/rust/game/angband`. A local rustc 1.97
  build (`a13e411c…`) plays the same three streams.
- **borg.txt:** the cell's own `user/borg.txt`, kept here as `borg-stats-ban.txt` (sha256
  `51b1004a3680…`, the cell's `borg_txt_sha256`). The control's is `borg-ctl.txt`
  (`a5cfee0cf3a2…`, the control cell's `config_sha256`): the same file with the three
  fast-fragile switches at 0. Scary list: the dossier's `scary_list.txt` (`9766d882…`).
- **Command:** `tools/zoorun.sh` starts the game as borg-zoo does (`-mborgh -n`, `-seed
  829474344 -race 7 -class 7 -turns 100000 -menu-letters -exact-turns`, message and state logs
  on, `TZ=UTC`, every ambient variable cleared). The keys are played from birth: no save is
  loaded and the Borg is never restarted. `scripts/native/rerun-death.py` refused this cell:
  its borg.txt rebuilt from `config.txt` hashes `02949423a683`, not `51b1004a3680` (the
  respawn lines and `borg_world = none` differ), so the cell's own file was used.
- **Result**, played from birth: death by poison at 96,820, 16,652 keys, byte for byte equal
  to the zoo cell:

  | log | sha256 (replay = zoo cell = dossier) |
  |---|---|
  | keys.log | `798335ae2821113ed4fac2726bb3acfb34e1e12f0426aeb60e6391bfcbd639dc` |
  | messages.log | `24bb3cc598e8e067b847d5129e141f9900fd2c4ce54cb5a3420a0766560428a5` |
  | state.log | `3bd31975a7ddd058cfc5544c98eed40db48fa79a7a9333df9b3610e6c2b46993` |

- **Control** from birth, the same way: the cap (100,000 turns, CL7, DL3), 19,450 keys,
  keys.log `689e1ca56038…`, the control cell's `play_sha256`.
- **Counterfactual build:** `tools/cf-hook.patch` on `7f8c6b80` (scratch only, never
  committed to borg-reborn-rs). With `BORG_CF="TURN:hex keys;…"` it queues the given keys at
  the first think at or after TURN, in place of that think, then lets the Borg go on with its
  memory intact. With `DUMP` it writes the Borg's map, pack, stair lists, flow costs, danger map,
  monster records and, for this analysis only, the engine's true map and monsters. With
  `BORG_CF` unset it plays the original game (the three hashes above); with a `DUMP` entry
  alone it plays the same keys.

Coordinates are (y,x), as in the Borg's notes. `state.log` prints x,y. A "keys.log line" is
1-based; the first column of `messages.log` is the number of keys sent before it (line − 1).

## What the engine says (574b618c)

| fact | where |
|---|---|
| White jelly: speed 120, 36 HP average, `TOUCH:POISON:1d2`, `NEVER_MOVE`, `HURT_LIGHT \| IM_POIS \| HURT_COLD`, depth 2 | `lib/gamedata/monster.txt:959-974` |
| A monster's HP is `Rand_normal(avg_hp, std_dev)`: this one had 25/25 (engine dump at 95,190; the Borg estimated 25) | `src/mon-make.c:956-972`, `1150` |
| Energy per game turn: speed 110 → 10, 120 → 20, 122 → 22 (the Borg's record says speed 122): the jelly acts 2.2 times per player turn | `src/game-world.c:81-82`, `136`; `src/mon-move.c:1938` |
| A monster's move or attack is the one grid next to it (`loc_sum(mon->grid, ddgrid[d])`). It attacks only when that grid holds the player; a `NEVER_MOVE` monster otherwise ends its turn | `src/mon-move.c:1586`, `1621-1633`, `1637-1644` |
| So the jelly at (14,96) reaches (13,95), (14,95), (13,96) and the other neighbours, never (13,94) or (12,93) (two columns away) | (from the line above) |
| POISON blow: elemental damage (1d2 here, `PROJ_POIS`), then `TMD_POISONED` += 5 + 1d(monster level) = 6–7 per poisoning touch | `src/mon-blows.c:674-690` |
| Poison: 1 HP per `process_world`, which runs every 10 game turns (one player turn at normal speed) | `src/game-world.c:512-519`, `1080-1081` |
| Poison falls by `adj_con_fix[CON] + 1` per 10 game turns: CON 16 → 1 + 1 = 2 | `src/game-world.c:280-282`, `317-320`; `src/player-calcs.c:686-702` |
| No HP regeneration while poisoned | `src/player-util.c:468` |
| One grade only, "Poisoned": the amount is not on screen | `lib/gamedata/player_timed.txt:253-262` |
| Cure Light Wounds: heal 20, cure blindness, reduce cuts and confusion; **no poison cure**. Cure Serious Wounds neither | `lib/gamedata/object.txt:3156-3173`, `3175-3190` |
| What cures poison: Neutralize Poison, Cure Critical Wounds, Healing, *Healing*, Life, Resist Poison, Salt Water, Curing staff/rod, Waybread, Fast Recovery, Purging | `lib/gamedata/object.txt:3278-3287` (Neutralize), `3192-3205` (CCW) and the other `CURE:POISONED` lines |
| Ranger Herbal Curing (cures poison) is a level-9 spell; the ranger was CL8 | `lib/gamedata/class.txt:1532-1534` |
| Wand of Magic Missile: `BOLT_OR_BEAM:MISSILE` 3d4, 6+d10 charges | `lib/gamedata/object.txt:3696-3708` |
| Phase Door: `TELEPORT` 10 | `lib/gamedata/object.txt:2571-2581` |

## The level at 95,190

`evidence/maps-95190.txt` holds the true map and the Borg's map (x 40–129). The level's
staircases (true map): down at (2,64), (28,122) and (33,48), up at (29,56). The Borg knew only
the down staircase at (2,64) (`evidence/pack-95170.txt`). From (13,94), avoiding the eight
squares around the jelly (`evidence/routes-95190.txt`):

| staircase | steps (true map, never next to the jelly) | known to the Borg |
|---|---:|---|
| `>` (2,64) | 33, via (12,93), (11,92) … west along row 11, then north | yes |
| `<` (29,56) | 58 | no |
| `>` (33,48) | 62 | no |
| `>` (28,122) | 95 | no |

On the Borg's own map the route to (2,64) over known squares only is 98 steps (south and
round). With unknown squares counted as floor, as the flight counts them, it is 30 steps,
north-west, the true route. The route the flight committed (`evidence/flow-costs-95190.txt`)
is neither: (13,94) 36 → (13,95) 35 → (13,96) 34 → (12,97) 33 → (11,96) → (10,95) →
(9,94…89) → (8,88…74) → … → (2,64) 0. It runs next to the jelly at (13,95) and (13,96), then
through (12,97), (11,96), (10,95) and (9,89–94), all granite in the true map.

**Why not north-west: the ghost soldier.** The Borg's danger map at 95,190
(`evidence/danger-95190.txt`, `borg_danger(y,x,1)`) is 36 on the eight squares around the
jelly and 0 elsewhere near it: the jelly's reach is modelled right. Around (11,86) it is
79–172, from a soldier record "asleep at (11,86), last seen think 9061". The engine has no
monster there (`evidence/monster-records.txt`). There is one soldier near (midx 30). It was
asleep at (11,86) at 93,439, awake at (15,96) at 93,859, where the Borg opened a second record
("Creating a monster 'soldier' at (15,96)", keys.log line 16,104), and it was killed at (20,113)
at 94,379 ("You have slain the soldier", line 16,187). The first record stayed, asleep, until
the death: it is forgotten only when its square comes into view empty, and the Borg never
looked there again.

The ghost does two things. It is the level's only scary monster at the time (`soldier |
8-11` in the scary list; the cutpurses were forgotten at 95,080 and 95,090), so "Scary guy on
level" and the flight to "any stair" (`borg_think_dungeon.rs:1085-1101`) hold for the whole
loop. And the weighted flight pays `100 + 100 × 5 × danger / HP` hundredths of a step per
square entered (`borg_flow.rs:590-616`, `629`, `caution_stairs_flight_threat_weight` 5). At HP
96 a square at danger 158 costs about 9 steps and a jelly-adjacent square (36) about 2.9. So
two jelly squares and a run through unseen rock beat a corridor past the ghost. At HP 3 the
jelly squares cost 61 steps each, and the flight finally switched to the 95-step southern route,
one turn before death (keys.log line 16,647: "Flowing toward stairs at cost 95").

## The loop, turn by turn

The first cycles and the last. Position and HP are `state.log`'s row for the think's key,
before it is played. "Poison" is `TMD_POISONED` (the `t7:` field). The rule is the core
trace's `check`. The full loop is in `evidence/loop-95170-96820.md` (`tools/loop_table.py`).

| keys.log line | game turn | position | HP | poison | rule (danger) | key | note | engine, until the next think |
|---:|---:|---|---:|---:|---|---|---|---|
| 16282 | 95160 | 14,94 | 96 | 0 | `borg_flow_stair_both` (0) | `9` | Flowing toward stairs at cost 35 | |
| 16283 | 95170 | 13,95 | 96 | 0 | `borg_caution` (72) | `4` | Retreating to 12,93 (distance 2) via 13,94 (72 > 0) | The white jelly wakes up. |
| 16285 | 95180 | 13,94 | 96 | 0 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches you; You are poisoned!; misses |
| 16288 | 95190 | 13,95 | 95 | 6 | `borg_caution` (36) | `1` | Retreating to 15,93 (distance 2) via 14,94 (36 > 0) | |
| 16289 | 95200 | 14,94 | 94 | 4 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches; more poisoned; misses |
| 16292 | 95210 | 14,95 | 91 | 8 | `borg_caution` (36) | `4` | Retreating to 15,93 (distance 2) via 14,94 (36 > 0) | |
| 16293 | 95220 | 14,94 | 90 | 6 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches; more poisoned; misses |
| 16296 | 95230 | 14,95 | 88 | 11 | `borg_caution` (36) | `7` | Retreating to 12,93 (distance 2) via 13,94 (36 > 0) | |
| 16297 | 95240 | 13,94 | 87 | 9 | `borg_recover` (0) | `qc` | Quaffing Potions of Neutralize Poison. | You are no longer poisoned. |
| 16300 | 95250 | 13,94 | 87 | 0 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches; You are poisoned!; misses |
| … | | | | | | | (the same two steps; Neutralize Poison at 95,270 and 95,320, the last) | |
| 16334 | 95400 | 13,95 | 64 | 28 | `borg_caution` (36) | `qb` | Quaffing Potions of Cure Light Wounds (11 left) | You feel much better. |
| … | | | | | | | (CLW at 95,490 … 96,410, the 12th and last) | |
| 16617 | 96640 | 13,95 | 38 | 468 | `borg_caution` (36) | `4` | Retreating to 13,94 (distance 1) via 13,94 (36 > 0) | |
| 16618 | 96650 | 13,94 | 37 | 466 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches ×2; more poisoned ×2 |
| 16621 | 96660 | 13,95 | 33 | 477 | `borg_caution` (36) | `4` | Retreating to 13,94 (distance 1) via 13,94 (36 > 0) | |
| … | | | | | | | | |
| 16642 | 96760 | 13,95 | 9 | 524 | `borg_caution` (36) | `4` | Retreating to 13,94 (distance 1) via 13,94 (36 > 0) | |
| 16643 | 96770 | 13,94 | 8 | 522 | `borg_flow_stair_both` (0) | `6` | Flowing toward stairs at cost 36 | touches ×2; more poisoned ×2 |
| 16646 | 96780 | 13,95 | 4 | 534 | `borg_caution` (36) | `4` | Retreating to 13,94 (distance 1) via 13,94 (36 > 0) | |
| 16647 | 96790 | 13,94 | 3 | 532 | `borg_flow_stair_both` (0) | `1` | Flowing toward stairs at cost 95 | |
| 16648–16650 | 96800–96820 | 14,93 → 16,93 | 2 → 0 | 530 → 526 | `borg_flow_stair_both` (0) | `2` | cost 94, 93, 92 | You die. (poison) |

Totals from 95,170: 86 `borg_caution` thinks (74 retreats, 12 CLW), 77 `borg_flow_stair_both`,
3 `borg_recover` (Neutralize Poison). 132 touches, 45 misses. No attack, no Phase Door, no
"Phase rule" note at all after 95,170.

## Answers

### 1. The white jelly and its reach

`monster.txt:959-974`: speed 120 (this one 122), 36 HP average (this one 25), one blow
`TOUCH:POISON:1d2`, `NEVER_MOVE`. It can only hit a player on one of its eight neighbours
(`mon-move.c:1586`, `1621-1633`). On every other turn it ends its move without moving
(`:1637-1644`). From (14,96) it touches (13,95), (14,95) and (13,96); (13,94), (14,94),
(12,93) and (15,93) are two columns away, out of reach. At energy 22 against 10 it acts about
twice per player turn: two touches a turn, as the log shows.

### 2. The loop: the two rules, the path, no breaker

- **The retreat** is `retreat()` (`borg_caution.rs:1131-1342`, note `:1327`), reached from
  `borg_caution` (`borg_think_dungeon.rs:796`) at `borg_caution.rs:2904-2912`. It fires
  because the danger here (36) is above HP / 3 (`caution_retreat_danger_divisor` 3: 36 > 32
  at full HP). `may_move_away` (`:1799-1818`) allows it: poison is not "nasty" (only weak,
  blind, confused and hallucinating are, `:2426-2438`) and the one-blow exemption needs a
  kill in one blow. It picks the nearest in-view "happy" square of lower danger, (13,94) or
  (14,94), and clears the flow goal (`goal.type_0 = 0`, `:1336`).
- **The stair flight** is `borg_flow_stair_both(GOAL_FLEE)` at `borg_think_dungeon.rs:1101`,
  under "Fleeing and leaving the level (Looking for any stair)", because the ghost keeps the
  level scary. From (13,94) its route (above) starts east.
- **Why through the square next to an immobile monster.** The weighted route does count the
  jelly's reach: every square entered costs its `borg_danger`. But that is only about 2.9
  steps at HP 96, cheaper than the north-west corridor priced by the ghost and cheaper than the
  98-step known detour. Unknown squares count as floor in a flight (`spread_blocked`, borg-reborn-rs#881),
  so the route east "through" rock is only 36. The clean-path check (borg-reborn-rs#743/borg-reborn-rs#751, mode 3,
  `weighted_route`, `borg_flow_stairs.rs:181-232`) does not refuse it. A blocker's danger is
  measured **at the Borg's own square** (`dangerous_path_blocker`, `borg_flow_stairs.rs:620-624`).
  The Borg flows only from (13,94) or (14,94), where a `NEVER_MOVE` monster two columns away
  has danger 0. Even measured from the path square, 36 would block only below HP 72
  (`caution_stairs_block_danger_percent` 50).
- **Why it never breaks.** Each rule decides afresh; nothing remembers the other. The retreat
  resets the flow goal, and the flow re-plans the same route next think. `bouncing()`
  (`borg_caution.rs:104-113`) looks at the last two flow steps and only at ≥ 70% HP
  (`caution_bounce_healthy_tenths` 7). The anti-loop counter `antibounce_count` is bumped only
  by equipment swaps (`borg_io.rs:150-153`). `caution_immobile_step_to_exit` (`:1749-1752`)
  belongs to `immobile_step_away`, off here (`caution_ranged_vs_immobile` 0). The retreat
  always finds its safe square, so `borg_escape` (`:2920`) is never reached. Nothing in the
  loop changes the inputs: the ghost stays, the danger stays 36, and HP only grows its weight.

### 3. Why no attack, and could it have won

- **Next to it** (13,95), `borg_caution` (`borg_think_dungeon.rs:796`) acts before `borg_attack`
  (`:889`): the retreat takes every one of those turns.
- **Two squares away** (13,94), `borg_attack` runs and keeps the jelly as a target (at distance
  2 and faster than the Borg, it counts as "adjacent" on a scary level, `borg_fight_attack.rs:4893-4899`,
  `attack_fast_monster_distance` 2). But every attack scores 0 (trace at 96,650, all 129
  candidates `nonpositive_return`): melee needs a neighbour, `BF_LAUNCH` has no arrows (the last
  of 289 shots went at 79,741), and the three wands are unidentified (Rusty, Steel, Gold).
  `BF_ROD_UNKNOWN | BF_WAND_UNKNOWN => 0` (`borg_fight_attack.rs:4511`); since borg-reborn-rs#470 an unaware
  device is never used (borg-reborn-rs#918). The ranger casts nothing at range at CL8.
- **Why scary.** The jelly is not scary. A `NEVER_MOVE` monster never is with
  `caution_scary_stand` 1, and it is not on the list. Danger 36 makes it worth stepping away
  from (> HP/3). The flight that brings the Borg back belongs to the ghost soldier.
- **What the pack held** (95,170, the Borg's item list, `evidence/pack-95170.txt`): 12 CLW,
  3 Neutralize Poison, 2 Phase Door, three unknown scroll stacks, five unknown potion stacks,
  the three wands, a Dagger (1d4) (+2,+2) wielded, two Main Gauches, two Short Bows, no arrows.
  The wands' kinds, from the Borg's own "Creating an object" notes at pickup: Rusty = Magic
  Missile (44,512), Steel = Heal Monster (48,731), Gold = Haste Monster (80,855). The game's
  letters were q, r, s (screen dump at 95,190).
- **It could have won, three ways** (counterfactuals below). Melee: two player turns, four
  hits, jelly destroyed at 95,200 (D1). The Magic Missile wand: one aim at 95,190 identifies it
  ("You have a Wand of Magic Missile (8 charges)"), and the Borg then aims it three more times
  by itself (`BF_WAND_MAGIC_MISSILE`, "Targeting white jelly who has 20 Hit Points") and
  destroys the jelly at 95,230 (B1). Walking around it: the true route north-west, 33 steps,
  never next to it, reaches the down staircase at 95,510 (A1).

### 4. Poison

1 HP per player turn (`game-world.c:512-519`), no regeneration (`player-util.c:468`); each
poisoning touch adds 6–7 (`mon-blows.c:683-684`), and the counter falls by 2 a turn (CON 16).
At two touches a turn the counter grew from 0 to 534. CLW heals 20 but does not cure poison
(`object.txt:3156-3173`); Neutralize Poison does (`:3278-3287`).

The Borg reads poison only as a flag (`BI_ISPOISONED`; the screen shows one grade,
`player_timed.txt:255`). It drank its 3 Neutralize Poison at 95,240, 95,270 and 95,320, each one
turn before stepping back into the jelly's reach, and then 12 CLW from 95,400 to 96,410. No
decision counted the poison still to come. The danger stays 36 to the end, and the retreat runs
before every escape. By `state.log`, poison alone outweighed the HP (counter / 2 ≥ HP) from
95,670 (HP 64, poison 134). With CLW left the Borg could still outlast it (C1, C4). After the
last CLW (96,410: HP 65, poison 388) nothing in the pack could. The flee rule for poison
("Fleeing (bleeding/poison)", `borg_caution.rs:3023-3031`) adds nothing: the Borg is already
fleeing.

### 5. Where the arm parts from the control

The first differing key is keys.log line 239, game turn 1,246, CL1 on DL1. The arm's "Fast-fragile
(stats): metallic red centipede (speed +12 vs +0, 13 HP vs 10.7 per turn …)" leads to "Attack on
sight" and a Main Gauche blow (`+`). The control reads Phase Door (`e000`, a menu key). From
there the games are different games. The control is on DL2 at 1,456, the arm at 3,678. The
control meets white jellies on other levels (45,399, 45,759, 55,720). At 55,720 (CL5) it starts
the same retreat/flight pattern. There the retreat sometimes declines, "Phase rule: attacked
instead of a Phase Door" fires, the jelly drops to 17 HP, and the Borg walks on (11 touches in that encounter, 17 in the whole game). So the loop is not the policy's; the control is exposed to it too.

### 6. Counterfactuals (exact game, scratch hook, shared lock)

`cf-summary.tsv` has the exact `BORG_CF` strings. The "first differing" column is the first
keys.log line that differs from the factual game.

| name | at | intervention | first differing line | outcome |
|---|---:|---|---:|---|
| factual | | none | | dies of poison, 96,820 |
| A1 | 95,170 | walk the true route north-west (34 steps, never next to the jelly), take `>` at (2,64) | 16,285 | DL3 at 95,510; **alive at the cap** (CL8) |
| A2 | 95,170 | two steps out of reach to (12,93), then the Borg resumes | 16,285 | the flight walks straight back east (cost 37, 36); the same loop; **dies of poison, 96,870** |
| B1 | 95,190 | aim the Rusty Wand once (`a q 3`), then the Borg resumes | 16,288 | wand learnt; the Borg zaps 3 more times itself; jelly destroyed 95,230; poison cured 95,250; **alive at the cap** |
| D1 | 95,190–95,300 | melee (`3`, into the jelly) at each think | 16,288 | jelly destroyed 95,200 (4 hits, 2 turns); **alive at the cap** |
| C1 | 96,000 | read Phase Door (HP 76, poison 239, 5 CLW) | 16,472 | lands at (11,85), lives on CLW until the poison ends (~97,200); **alive at the cap** |
| C4 | 96,100 | read Phase Door | 16,496 | **alive at the cap** |
| C3 | 96,200 | read Phase Door (HP 72, poison 313, 3 CLW) | 16,518 | **dies of poison, 97,240** |
| C2 | 96,500 | read Phase Door (HP 66, poison 424, no CLW) | 16,588 | **dies of poison, 97,180** |

Stepping out of reach alone (A2) does not save it: the Borg already does that every other
turn. What saves it is ending the alternation: kill the jelly (D1, B1), take the true route
(A1), or leave the area while the CLW can still outlast the poison (C1, C4). After the Phase
Door at 96,200 the Borg also notes the ghost at last ("There was a monster 'soldier' at
(11,86)"), but too late.

### 7. A pattern?

`tools/osc.py` scans every `trace-core-tail.jsonl` in this repository (396 files on this
branch) for a `borg_caution` think with danger > 0 followed by a flow think with danger 0,
at least 10 times in the last 120 thinks. Beyond worm and kobold cases, the hits next to a
`NEVER_MOVE` monster:

| case | character | killer | the alternation | note |
|---|---|---|---|---|
| this one | Half-Troll Ranger 829474344, `7f8c6b80` | poison (white jelly) | `borg_caution` `4` / `borg_flow_stair_both` `6`, 51 in 120 | |
| [D-5a494c5be113](../../deaths/D-5a494c5be11353382590b2d0af92832c0a8c1bb14175de602d418952b5398fa7/README.md) (and its repeats D-96f16297bf24, D-ecd3c22b08b0) | Half-Troll Ranger 214960633, `e8b3acfd`/`fde8025a` | a grey mold | `borg_caution` `2`/`1` / `borg_flow_dark` `8`/`9`, 51 in 120, at HP 0–3 next to a down staircase | borg-reborn-rs#753 (closed): the rising hold on a down staircase |
| [validation D0007-rust-seed1050](../../validation/borg-reborn-rs/native-controls/deaths/D0000-q13eeaebe421d34585c93b498421b554fc6c8b973281fea66a0c1f5c0cd3e8fdd/report.md) (and its repeats) | Dwarf Paladin 1050, harness full suite | a grey mold | `borg_caution` `9` (danger 16) / `borg_flow_stair_both` `1`, HP 6 | raw logs not retained |
| [validation D0010-rust-seed1074](../../validation/borg-reborn-rs/native-controls/deaths/D0000-qee65e8edbd3bf8644d1fcfb458398ce992a214938cee66b5bb482b5e24b17fe9/report.md) (and its repeats) | Human Ranger 1074, harness full suite | poison | `borg_caution` `4` (danger 32) / `borg_flow_stair_both` `6`, HP 7 → 0 | the same signature as this case; the monster is not known (raw logs not retained) |

The nearest non-immobile case: Human Ranger 526144893
([D-48dad39005b6](../../deaths/D-48dad39005b695e64239bf8f67c748f49e3174628292cb0a576a7b41dd2f4cac/README.md),
`e8b3acfd`, zoo run 44738419997) dies of poison in a `borg_caution` `4` / `borg_flow_dark` `6`
loop against white worm masses (breeders that move; compare borg-reborn-rs#876, borg-reborn-rs#882). These
are leads from trace signatures, not a count: repeats of one start are not independent, and
the seed 1050/1074 monsters are not confirmed.

## Defects filed in borg-reborn-rs

Each issue links back here. The track is left to the owner, and every threshold is a
hypothesis (RULES 14).

- borg-reborn-rs#930 — a monster that wakes out of view and is seen elsewhere gets a second
  record; the first stays asleep forever (the ghost soldier: scary level and a priced corridor).
- borg-reborn-rs#931 — the stair flight passes next to an immobile monster: the clean-path
  check measures a blocker's danger at the Borg's square, not at the path's (see also borg-reborn-rs#881 for
  the route through unknown rock).
- borg-reborn-rs#932 — retreat and stair flight undo each other every turn with no breaker
  (132 touches).
- borg-reborn-rs#933 — no attack on an immobile monster that blocks the route: the retreat
  pre-empts melee, and an unknown wand is never aimed (see borg-reborn-rs#918).
- borg-reborn-rs#934 — accumulated poison is never weighed: cures are spent inside the loop,
  CLW is drunk against poison, and Phase Door is never considered (see borg-reborn-rs#916).
- borg-reborn-rs#935 — a ranger out of arrows for 17,000 game turns with 2,516 gold, no Recall
  and no way up.

## Files

| file | what |
|---|---|
| `borg-stats-ban.txt`, `borg-ctl.txt` | the arm's and the control's `user/borg.txt` (sha256 above) |
| `cf-summary.tsv` | the counterfactuals: `BORG_CF`, first differing line, outcome |
| `tools/zoorun.sh` | start the game as borg-zoo does (`GAME` = the build's `game/` directory) |
| `tools/cf.sh` | one counterfactual (`CF_WORK` holds the cell bundle in `d/` and the factual replay in `replay/`) |
| `tools/cf-hook.patch` | the scratch `BORG_CF` hook on `borg-core/src/borg.rs` at `7f8c6b80` (not for borg-reborn-rs) |
| `tools/route.py`, `tools/maps.py` | routes on the dumped maps; the A1 key script |
| `tools/loop_table.py` | the loop table from a run directory with `trace-core.jsonl` |
| `tools/osc.py` | the pattern scan of question 7 (run from the repository root) |
| `evidence/loop-95170-96820.md` | every think of the loop |
| `evidence/maps-95190.txt`, `evidence/routes-95190.txt` | the true and the Borg's map at 95,190; routes and staircase distances |
| `evidence/flow-costs-95190.txt` | the committed flight's route, from the Borg's flow costs |
| `evidence/danger-95190.txt`, `evidence/danger-96780.txt` | the Borg's danger map around the jelly and the ghost |
| `evidence/monster-records.txt` | the Borg's records and the engine's monsters at 93,439, 93,859, 94,369 and 95,190 |
| `evidence/pack-95170.txt` | the Borg's pack and stair lists at 95,170 |

Not checked: the five unknown potion flavours were never tried. From the Borg's pickup notes,
Metallic Red is Berserk Strength and Oily Yellow is Slime Mold Juice; the others are not
determined. The `danger 72` at 95,170, while the jelly was still asleep, is reported, not
explained. The ascent that never happened (borg-reborn-rs#935) is described from the notes, not diagnosed.
