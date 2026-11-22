# Dunadan Priest 399497898: trapped in a worm lattice on DL1, and the "fight your way out" policy

One named case, one life. Every replay below is a branch of the same game, not a sample
(borg-reborn-rs RULES 12, 14). The owner watched the replay from game turn 65000 and judged:
"its only chance was to go southwest and fight its way out through the worms; instead it went
north and stayed trapped there until it died". This study checks that reading against the map,
the Borg's own decisions and the engine, plays the alternative on the exact game, and states
the owner's policy as a rule.

**Verdict, in short.**
1. The owner's reading of the map is right. The pocket is a 62-square checkerboard room whose
   **only exit is its southwest corner (37,142)**; north (29,148) is a dead-end tip.
2. The Borg went north because its **flight to the stairs planned routes through unseen
   rock**: 58 of the 68 stair-flight paths it committed inside the room crossed grids its map
   holds as unknown, north of the room. Retreat and back-up have no notion of exits or dead
   ends, and every lattice square counts as a "happy" grid for them.
3. **Fighting out works on the exact game** from every valid start between turns 62992 and
   66262 (two failures, at 66112 and 66172), with no potion needed before 63442. Shipped
   borg-core already holds this rule: `caution_breeder_policy 4` (avoid plus "fight through
   the breeders to the stairs") plays the same game to turn 63372, then walks out southwest and
   lives to the 100,000-turn cap.
4. The owner's "only chance" is too strong. **Standing still and hitting whatever is adjacent
   also survives**, even later (to turn 66402), with 3 bites in 400 player turns. What killed
   the priest was **moving**: 214 moves (retreat, back-up, flight steps) in 359 player turns,
   81 bites. The policy should therefore be "against slow erratic breeders, never retreat:
   hold, or cut the real path out".
5. The #758 Recall refusal was moot: the priest **had no Word of Recall** after turn 45022.
   The forecast does mis-model slow poison-biting breeders (borg-reborn-rs #876, #880).

**Issues.** borg-reborn-rs [#882](https://github.com/diegoami/borg-reborn-rs/issues/882)
(the policy, below), [#881](https://github.com/diegoami/borg-reborn-rs/issues/881) (the flight
plans through unknown grids), [#883](https://github.com/diegoami/borg-reborn-rs/issues/883)
(Heroism recast below CL20). The Recall forecast is already
[#876](https://github.com/diegoami/borg-reborn-rs/issues/876) and
[#880](https://github.com/diegoami/borg-reborn-rs/issues/880).

## The case

| | |
|---|---|
| zoo run | [44924461733](https://github.com/diegoami/borg-zoo/actions/runs/44924461733), experiment `reborn-confusion-837-small` (borg-zoo#581), suite `classes-1800-small`, start 76 of `toolkit/originals-20261108/starts.json`. **Not** run 44936494812: that is the medium tier (starts 91–360) and has no seed 399497898 (it holds the CL3 Mage 461220874 cited in question 7). |
| specimen | `4.2.6-reborn-rust-confusion-da097a76`: borg-reborn-rs `da097a764239c64cdcdd0fb469d5a05577a6823e` (main `12c4ce7c` plus #837's confusion settings), shipped `harness/borg.txt`, scary list `9766d882…` |
| core | **borg-rs** (`borg-core/`): the profiles set `borg_reborn_core = borg-rs` (borg-zoo `catalogue/profiles.json`, `reborn-confusion-*`); cell `harness_kind: borg-rs`. Not `BORG_CORE=reborn`. |
| arms that died | `reborn-confusion-clw_walk` and `reborn-confusion-csw`, with the same play hash `dde95ceb…`: one game. `ctl` (`f9374a2b…`) and `stuck` (`a9c8f917…`) reached the cap alive. |
| character | Dunadan Priest (race 8, class 3), seed 399497898, cap 100,000 game turns, exact turns, menu letters |
| death | game turn 66588, key 6212, CL6, HP 1/59 before the last bite, DL1 (max 2), "a white worm mass" |
| dossier | [`deaths/D-3b3bfb975c2d…`](../../deaths/D-3b3bfb975c2d4a54df938a40fb243446467febad7c205154d3648d81cadae96f/README.md) (csw arm, imported by cemetery PR #104). The clw_walk bundle is the same life and gets no separate analysis here. |

**Why the arms split.** Replaying `ctl` locally from birth reproduces the zoo's `ctl` cell key for
key (`f9374a2b…`, [evidence/hashes.txt](evidence/hashes.txt)). The first difference is at key
4243, turn 50702, two keys after a grey mushroom patch confused the priest: the arm quaffs a potion
for the confusion where `ctl` attacks. The death comes 16,000 turns and several dungeon visits
later. The confusion settings changed which game was played; they are not part of how this one ended.

**Reproduction (verified).** borg-reborn-rs `da097a76` was built here (`harness/build.sh`, clean,
source hash `cba81bd0…` = the zoo's). The zoo cell's invocation, from birth, gives `keys.log`,
`messages.log` and `state.log` byte-identical to the zoo artifact `deaths-…-5` (hashes in
[evidence/hashes.txt](evidence/hashes.txt)). The binary hash differs (rustc 1.97 here, 1.100 in the zoo).

## How the map was read: a diagnostic build

The harness terminal is a fixed 80×24 screen, so a copy of the source got a diagnostic-only patch,
[tools/diagnostic.patch](tools/diagnostic.patch). It was never committed to borg-reborn-rs and is
never a measured build. It:
- at the stop (`-keys N`), writes the whole level from the engine (truth) and from the player's
  knowledge (`player->cave`), every monster, the pack with true item kinds, HP, SP and the poison
  timer (`BORGH_MAPDUMP`);
- prints each stair-flight path the Borg commits, marking grids its own map holds as unknown
  (`BORG_DIAG_PATH`, `borg-core/src/borg_flow.rs` `commit_weighted_stair_path`);
- after N Borg keys, stops consulting the Borg **in the same process** and takes keys from a pipe
  (`BORGH_HANDOVER`, `BORGH_IN`/`BORGH_OUT`), so a counterfactual continues the exact game.

Every diagnostic run reproduced the original key stream before it was used. Truth maps are what
the engine held, not what the Borg saw; the counterfactual player below plans only on the
player's knowledge and visible monsters.

## 1. The map

[maps/level-overview-66572.txt](maps/level-overview-66572.txt) shows the level around the pocket at
the death; [maps/pocket-at-key-turns.txt](maps/pocket-at-key-turns.txt) shows the pocket at seven
key turns. Excerpt at turn 63592: `*` is the least-worm route to the corridor, `w` a worm.

```
game turn 63592, key 5526: priest @ 33,148, HP 43/59, white worm masses on level 13;
least-worm route to the corridor (33,141): 10 steps through 1 worm
         4    4    5    5
      789012345678901234567
   28 ##.##########.......#
   29 ##...######,##....#.#     29,148: the north tip, walled on five sides (a dead end)
   30 ####.#####,#,##.....#
   31 ####.####,#,#,###.###
   32 ####.###,#,#,#,##.###
   33 ####*##,#w#@#,#,#.###     column 141: the corridor out (rows 29-37, then 29,139 west)
   34 ####*###,#*#,#,##..##
   35 ####*##,#*#,#,#w#..##
   36 ####*###w#w#,#w##..##
   37 ####.***#,#,#w#,#....     37,142: the room's only exit
   38 ########w#,#w#,##.###
   ...
   45 ###########,#########     45,148: the south tip, also a dead end
```

- **The room.** 62 floor squares, rows 29–45, columns 143–152, in a checkerboard: every
  floor square touches its neighbours only diagonally, the orthogonal ones are pillars.
  A flood fill from the priest that never enters column ≤142 reaches all 62 and touches the
  outside at **one square, 37,142** (`tools/paths.py`). North is a dead end: 29,148's
  five neighbours to the north and sides are granite. The south tip 45,148 is a dead end too.
- **The way out.** 37,142 → 36,141 → the column-141 corridor (rows 29–37) → 29,139 → west along
  rows 23/22 → the down stair at **17,98**, the staircase the priest arrived on and the only
  one it ever knew. That is 62–69 steps from the pocket. The level's other stairs, all unseen:
  `>` 20,173, `>` 45,171, `>` 39,57, `<` 42,52, `<` 42,74. No up stair was ever known.
- **How it got there.** It walked, one square per player turn (`state.log`, 62002–63012); no
  Phase Door or teleport. At 62132 its trip plan started a walking return to town
  ("Trip: return via search (plan 2)", "no up stairs found, exploring for them (rising)").
  It had no Word of Recall (below), so it explored for an up stair and entered the lattice from
  the corridor at 37,142 at 62852.

**Worms between the priest and the exit** ([evidence/exit-series.tsv](evidence/exit-series.tsv),
every 100 game turns; least-worm path to 33,141 on the truth map):

| game turn | priest | HP | worms on level | in the room | worms on the least-worm path | steps |
|---:|---|---:|---:|---:|---:|---:|
| 62992 | 40,149 | 59 | 4 | 2 | **0** | 11 |
| 63192 | 30,147 (north tip area) | 57 | 7 | 5 | **0** | 15 |
| 63492 | 37,150 | 48 | 13 | 11 | **0** | 14 |
| 63592 | 33,148 | 43 | 13 | 11 | 1 | 10 |
| 63692 | 33,148 | 39 | 14 | 12 | **0** | 12 |
| 63892 | 32,145 | 44 | 22 | 20 | 4 | 11 |
| 64392 | 33,152 | 50 | 30 | 28 | 4 | 14 |
| 64992 | 33,144 | 57 | 39 | 35 | 5 | 10 |
| 65992 | 35,144 | 33 | 37 | 32 | 4 | 8 |
| 66392 | 29,148 (north tip) | 34 | 42 | 37 | 8 | 14 |
| 66572 | 34,147 | 2 | 39 | 34 | 4 | 11 |

The path was **free of worms until about 63692**, and cheapest around 62992–63692. From 63892 it
crossed 3–8 worms. The population levelled off at 35–44 (`num_repro` peaked at 45, far below the
engine's cap of 100): the room is small, and a breeder with 3 or more neighbours never breeds
(mon-move.c:1043).

## 2. Why it went north

Each move after 62900 is paired with the note that decided it in
[evidence/moves-after-62900.tsv](evidence/moves-after-62900.tsv). Of 223 moves: 58 stair-flight
steps, 47 retreats, 27 back-ups, 13 exploration steps, 12 right after a Heroism cast, and 56
"attack" keys that moved because the target had staggered away.

**The stair flight planned through unseen rock.** Flights to the stairs
(`borg_flow_stair_more` / `stair_both`, borg_think_dungeon.rs:1102 and :1283) use the
threat-weighted route `weighted_stair_path` (borg-core/src/borg_flow.rs:590). It refuses awake
monster grids (:608) and grids that `spread_blocked` blocks. `spread_blocked` blocks an unknown
grid (`FEAT_NONE`) only `if (avoid || b.status.desperate)` (borg_flow.rs:442), and the flight
passes `avoid: false` (borg_flow_stairs.rs:742ff). The diagnostic path print shows what that does
([evidence/flight-paths-in-pocket.tsv](evidence/flight-paths-in-pocket.tsv)):
- **58 of 68** committed flight paths that started inside the room went through grids the
  Borg's map held as unknown. All 58 were granite.
- **10** used the real exit at 37,142.
- Example, think 3688 (turn 63182), from 30,147: `29,148 28,147? 28,146? 28,145? 28,144?
  28,143? 27,142? 26,141? 25,140 …`. This is the north tip and then a straight line through the
  rock to the corridor. The real route is 66 steps southwest.

  The `~` marks of the 63192 map in
  [maps/pocket-at-key-turns.txt](maps/pocket-at-key-turns.txt) draw it.
- 28,147 was a **known wall in the player's own map**, yet unknown in the Borg's. This
  perception gap is a second, smaller problem.

With worms moving every other turn, the planner switched between such phantom routes
(north via 28,143, northeast via 27,149) each think. So the priest went up into the tip, down,
and up again: after turn 60000 it arrived at 29,148 25 times.

**Retreat and back-up know nothing of exits.**
- `retreat` (borg_caution.rs:1137, note at :1333) takes the nearest viewable "happy" floor grid
  whose danger, over `caution_retreat_danger_horizon`, is lower than here.
- `back_away` (:1358, note at :1533) takes the adjacent grid with the lowest danger.
- In a lattice every square is "happy": the pillar cases of `borg_happy_grid_bold`
  (borg_flow_misc.rs:311ff) match each square, the dead-end tip included.
- Neither rule counts breeding or dead ends. The worms' slowness enters only through `borg_danger`.
- Typical notes are "(46 > 36)" or "(83 > 6)". The step was always to a square the worms
  reached a turn later.

**Exploring for an up stair** ("no up stairs found, exploring for them (rising)",
borg_think_dungeon_util.rs:1074) is what took it into the room, at 62132–62852. It is a
dark-flow toward unexplored grids. Inside the pocket, it took 13 more steps.

**Heroism spent the mana.** At 63012–63072 it cast Heroism five times in a row ("Hard breeder
fight: Heroism", `cornered_boost` borg_caution.rs:4850, from `breeder_fight_hard` :4780 because
danger 32 ≥ HP 59 × 5/10). This happened at full HP. A priest's Heroism below CL20 only heals 10
and cures fear: the HERO duration is `PLAYER_LEVEL − 19 + d(PLAYER_LEVEL − 19)`, negative at CL6
(lib/gamedata/class.txt:767–776). So the status never appeared, and `cornered_boost` kept
recasting while `!temp.hero`. SP went 11 → 1 and stayed there. Those 10 SP were five Minor
Healings, 16 HP each at CL6 (class.txt:742–746).

## 3. Leave the level, Recall, no up stair, a down stair at cost 55–73

- **The goals.** At 63072 "Fleeing (failed to teleport)" set fleeing and leaving (no Phase, no
  teleport item). At 63312 "Breeders: 5 known, more than the 4 this class clears: the level is
  lost" (borg_caution.rs:4101; `caution_breeder_hunt_max_count 4`, harness/borg.txt:1102;
  `caution_breeder_policy 3`, :1190). From then "Scary guy on level" fired every think. White and
  green worm masses are scary at CL ≤ 15 once the known breeder count reaches the character level
  (borg_flow_kill.rs:2827–2835, lifted from the C Borg's borg-flow-kill.c:2740–2754); at CL6
  that means 6 worms.
- **Why the down stair was never taken.** It was the only known stair and the flight did aim at
  it ("Flowing toward down-stairs at cost 53–69"). But 85% of the routes it chose went through
  rock (above). At 64262 the clean-path check refused once: "Stairs not reachable: white worm mass
  in the way (flight to the stairs)" (`caution_stairs_clean_path_flee 1`). Fighting through to
  the stairs (`fight_through_plain`, borg_flow_stairs.rs:1081ff) needs `breeder_block` marks,
  which only `caution_breeder_avoid` makes. That is layer 4 of the breeder policy, off at the
  shipped policy 3 (borg-core/src/params.rs:342, :2429). So the real route through 1–8 worms was
  never deliberately taken, and retreat and back-up undid the flight's progress, as in the mouse
  colony of `runs/2026-11-19-reborn-614-leave-priest-592068863`.
- **Is "scary guy" reasonable here?** Wanting to leave is right. The manual says to leave a
  large colony (docs/strategy/10-exploration.md:509–514) and to leave when breeders outpace kills
  (:663), preferring known stairs (:665–668). The C Borg leaves at `MIN(clevel+2, 5)` breeders
  (borg-think-dungeon.c:1185–1225).

  What failed is the execution, not the goal. Scary and "level lost" hand the movement to a flight
  that cannot find the one real path. The flight shares it with retreat and back-up, which move
  away from the worms into the room. Being scared of white worms is also out of scale with the
  measured threat: 0.51–0.86 HP per player turn (below).

## 4. The #758 Recall refusal

The refusal note appears 146 times. Each time it is "unmodelled spell/status risk from N reachable
monsters; modelled contact exposure 21–442 HP during 34 world ticks".

- **The priest had no scroll to read.** It read its last Word of Recall at 45022 ("You have no
  more Scrolls of Word of Recall"). The pack dump at 62892 and 66572 has none: true kinds,
  `GEAR` lines of the map dump. The forecast `flight_recall_survivable` runs inside
  `borg_recall_for_flight` before `borg_recall` looks for a scroll (borg_escape.rs:101–107), so
  every refusal was moot. The parallel study for borg-reborn-rs #876
  (`studies/recall-breeders-876` on branch `claude/borg-flight-recall-breeder-r5b73d`) found the
  same: forcing the check open replays the same game key for key. The unread scrolls in the pack
  were Light and Treasure Detection, and the unknown potion was Sleep. There was no escape item
  at all.
- **The model is still wrong for slow, erratic melee breeders.**
  - *Right:* the 34 ticks are the engine's longest delay, `randint0(20) + 15` world ticks
    (src/effect-handler-general.c:1145), counted down once per 10 game turns
    (src/game-world.c:709–711). The energy ratio is applied correctly: the worm gets 5 energy per
    game turn against the priest's 10 (game-world.c:80–81, 136–138; monster.txt:680), so it acts
    every second player turn.
  - *Wrong: POISON makes every worm an "unmodelled" risk,* and any unmodelled risk refuses
    outright. `modelled_blow` accepts only HURT, ACID, ELEC, FIRE, COLD and NONE
    (borg_caution.rs:2285). The engine models poison simply: element damage plus
    `TMD_POISONED + 5 + randint1(rlev)` (src/mon-blows.c:684), then 1 HP per world tick
    (game-world.c:513–515), with one timer whatever the number of worms.
  - *Wrong: every reachable worm is summed* for the whole delay. In the lattice at most 4 can
    stand next to the priest (diagonals only), and 75% of a white worm's moves are random
    (`RAND_25 | RAND_50`, monster.txt:690; mon-move.c:1087–1102).
  - *Measured:* the priest lost 0.51 HP per player turn in 63000–64000, 0.77 in 64000–65000 and
    0.86 in 65000–66000 (`state.log`). Over 34 player turns that is 17–29 HP. The model said
    193–442 HP.
- **Would Recall have saved it?** Only with a scroll, which it lacked. At the measured rates, a
  priest at HP ≥ 35 with cures survives a 34-turn wait, and the stand control below shows near-zero
  damage when it does not move. That holds as a hypothesis from about 63000 to 65900. This belongs
  to #876 and #880, which already cover the change; this study adds that no scroll was carried, so
  the forecast's log line is misleading on its own.

## 5. Counterfactual on the exact game: cut southwest

Method ([tools/fightout2.py](tools/fightout2.py), [tools/hand.sh](tools/hand.sh)): the Borg plays
the recorded game to key K, in the same process, and then a scripted player takes over. Its
inputs are the **player's known map and visible monsters** and nothing else. Its rules:
- each turn, walk the cheapest known path to the corridor square 33,141, where a worm on the
  path costs 3 extra steps, and attack by moving into the worm on that path, not the nearest one;
- quaff Cure Serious, then Cure Light Wounds, at HP < 25, and Neutralize Poison if poisoned and
  HP < 40;
- once out, walk to the known down stair 17,98 and take it.

An exactness check: handing over at key 5418 and feeding the Borg's own next 300 keys reproduces
all 1,074 game messages of the original.

Results for every 10th key from 5430 to 6206
([evidence/counterfactual-fight-out.tsv](evidence/counterfactual-fight-out.tsv)). Four handovers
fell inside a prompt (a spell menu after `m a`, a direction prompt after `+`) and are excluded.

| starts (game turn) | start HP | outcome | min HP | consumables |
|---|---|---|---|---|
| 62992–63372 (5 starts) | 54–59 | out of the room in 11–14 player turns, DL2 alive | 53–59 | none |
| 63442–63952 (10) | 38–55 | DL2 alive | 24–51 | 0–1 Neutralize Poison, once CSW + CLW |
| 64012–65982 (49) | 30–58 | DL2 alive | 3–51 | Neutralize Poison; often CSW, 1–4 CLW |
| 66032 | 33 | DL2 alive | **2** | Neutralize Poison |
| 66112, 66172 | 29, 26 | **dead** | 0 | Neutralize Poison (the Borg had already drunk all its CLW, the last at 65352, and its CSW at 65622) |
| 66212, 66262 | 37, 38 | DL2 alive | 14, 19 | Neutralize Poison |
| 66332 and later (6) | ≤ 40 | **dead** | 0 | |

Representative run, handover at key 5526 (turn 63602, HP 43): out of the room at 63762 (16 player turns), on DL2
at 64292 with HP 52, minimum 39, nothing drunk.

**The latest working start is turn 66262** (key 6130, HP 38), 33 player turns before the death,
and it is marginal from about 66000. The policy was safe with no consumables until about 63442,
and safe with the pack's own potions until about 65900.

**The control: stand and fight**
([evidence/counterfactual-stand.tsv](evidence/counterfactual-stand.tsv)). Same handover, but the
player never moves: it attacks an adjacent visible worm or holds still.
- From 63082, 63642, 64242, 64682, 65132, 65522, 65892, 66262, 66112, 66172, 66332 and 66402 it
  is alive after 400 player turns, all at HP 59 or more at the end. Some gained a level.
- From 64242 it took **3 bites in 400 player turns** and destroyed 45 worms.
- It dies from 66452 (HP 24) and later.

The original game took 81 bites in 359 player turns, with 214 moves and 128 swings. An adjacent
worm acts every second player turn and staggers on 75% of its moves, so a priest who stays put
gets about two blows in before most worms can bite.

**The shipped switch that already does it.** Replaying the start from birth with
`borg_param_caution_breeder_policy = 4`, a single named case:
- the game is identical to the death until **key 5491, turn 63372**;
- then it notes "Fighting through the breeders to the stairs", walks 33,148 → 37,142 → the
  column-141 corridor → 17,98 at full HP (63362–64202), and lives to the 100,000-turn cap;
- it did hover on the stair for 1,000 game turns ("Standing on dn-stairs" / "No rest: breeders
  known" / exploring) before descending at 65222.

Policy 5 (`caution_breeder_exit` too) diverges at turn 36698, so it plays a different game, which
also lives.

## 6. The policy, stated as a rule (hypotheses, RULES 14)

**SLOW-BREEDER: hold or cut out; never retreat into the colony.**

*Fires* when all of these hold:
- every awake monster within `R_SCAN` (8) grids that can reach the Borg is a breeder
  (`RF_MULTIPLY`);
- each of them is slower than the Borg or erratic (RAND_25/RAND_50), and none has spells or
  ranged attacks;
- either the colony is growing (known breeders ≥ `N_BREEDERS` (5), or up by ≥ `N_GROWTH` (2) in
  the last 100 game turns), or the level is "lost" or scary because of breeders.

*Does*, in this order:
1. **No retreat and no back-up** into a square with no known exit route. In this mode,
   `retreat` and `back_away` only accept a step that lowers the known-path distance to an exit.
2. **Exit**: the nearest known grid outside the room's breeders. That is a corridor or doorway at
   least `D_CLEAR` (6) grids from every known breeder, or a stair. Plan on **known grids only**:
   unknown counts as wall for this route. The cost is steps plus `W_WORM` (3) per breeder on the
   path. If the route crosses at most `MAX_ON_PATH` (8) breeders and the "HP and cure margin"
   below holds, walk it: attack the breeder **on the path**, not the nearest one, and let no other
   movement rule undo a step until the exit is reached (#556's "the exit owns the movement").
3. **Otherwise hold**: stand still on the current square and attack adjacent breeders, nearest
   first. Do not move except to the exit route.
4. On reaching the exit, go on to the stair if one is known. Otherwise keep the corridor:
   breeders come one at a time there and stop breeding at 4 neighbours (mon-move.c:1043).

*HP and cure margin*: cut out while HP ≥ `HP_GO` (40%) of max, or while HP ≥ 25% with at least
one cure (CLW/CSW) left. Otherwise hold, heal at `HP_HEAL` (40%), and quaff Neutralize Poison or
Cure Light Wounds while poisoned. Note that CLW and Minor Healing do not cure poison in 4.2
(object.txt:3156–3173, class.txt:742–746).

*Yields* to the existing escapes when any of these holds:
- a non-breeder, a breeder with ranged attacks, or a breeder faster than the Borg comes within
  `R_SCAN`;
- HP < `HP_FLOOR` (25%) with no cure left;
- a free stair is within `caution_breeder_easy_escape_steps`.

*Also*:
- no Heroism or Berserk from `cornered_boost` when the class's spell grants no timed effect at
  this level (Heroism below CL20, class.txt:767–776);
- and #876/#880 for the Recall forecast.

Every number above is a hypothesis.
- `D_CLEAR` 6 comes from `caution_breeder_exit_distance` (harness/borg.txt:1140).
- `W_WORM` 3 reflects that a 2d4 mace needs about two blows for a 10-HP worm (monster.txt:681).
- `HP_GO` 40% and `MAX_ON_PATH` 8 cover the sweep: starts at HP ≥ 30 with 3–8 worms on the
  route survived, the 66032 start (HP 33/59) only just, at 2 HP.

Against the evidence:
- *Strategy manual.* It agrees with "fight them in a corridor" and "leave a large colony"
  (10-exploration.md:509–514, 663), with FIGHT-03, "prefer corridors against groups", within
  `K_CORRIDOR_STEPS` = 3 (15-notes-for-the-borg.md:222–224), and with "always know your exit"
  (10:597–615). The manual says nothing on *how* to leave through a colony; this rule fills that gap.
- *C Borg.* It flees at `MIN(clevel+2, 5)` breeders (borg-think-dungeon.c:1185–1225), and its
  `borg_surrounded` comment warns: "The borg can get trapped by continuing to flee into a
  dead-end" (borg-escape.c:250–260). That is exactly this death.
- *borg-core.* It already has the pieces, all off at shipped policy 3:
  - `caution_breeder_avoid` with `caution_breeder_avoid_fight_through` (layer 4,
    harness/borg.txt:1159, 1168), which played the way out here;
  - `caution_breeder_exit` (layer 5, borg_caution.rs:3779), written for the dead-end worm room of
    borg-reborn-rs #544;
  - `caution_slow_crowd_exit`.

  What they lack: unknown grids are passable in the flight route, retreat and back-up stay
  active, and there is no "hold" fallback.
- *Zoo.* #482 measured policies 4 and 5 against 3 in the breeders-×4 world: 8, 6 and 8 deaths over
  360 starts, neutral at that size (borg-zoo docs/FINDINGS.md:662–666). #530, in the normal world:
  no deaths in any arm (:700).

## 7. A pattern?

**In this specimen's runs:**
- the CL3 Human Mage 461220874 (run 44936494812, csw arm) died to white worm masses' poison at
  turn 18520, after 58 retreats or back-ups and 23 Recall refusals for the same POISON reason.
  See borg-reborn-rs #878 and #880 and the case on cemetery branch `claude/trusting-turing-puk2no`;
- the Human Ranger 129607500's "poison" (small tier, `stuck` arm) was a **white jelly**, not a
  breeder.

**In the cemetery:**
- 14 curated dossiers were killed by breeders: giant white louse 6, giant white mouse 5, blue worm
  mass 2, white worm mass 1. They cluster at CL2–12 on DL1–4.
- Three older dossiers with messages (D0012, D0020, D0022) died to white worm masses after 9–38
  "Retreating to" and 204–478 "Scary guy" notes.
- `runs/2026-11-19-reborn-614-leave-priest-592068863` (D-5153ba00…) is the same mechanism with
  mice: 172 back-ups undid a 162-round flight.
- In the historical borg-reborn-rs archive, 177 of 2,378 deaths (7.4%) were breeders: mice 132,
  white worms 30, lice 12. 166 of them were on DL1
  (`statistics/sources/reborn-historical.snapshot.json`).

**In zoo death tails:** 9 breeder kills and 4 "poison" deaths with a white worm mass as the last
attacker, most with 10–24 "Retreating to"/"Backing up" notes.

**What a borg-zoo measurement of the rule needs** (RULES 20, once a commit implements it):
- arms over the shipped `harness/borg.txt`: control (policy 3), the new rule on, and policy 4 as
  the existing comparator;
- a **breeder-rich suite**: the breeders-×4 world of #482 and a slice of classes-1800, since
  breeder deaths are ~4–7% of all deaths and normal-world pilots see none (#530);
- pre-specified endpoints: deaths with a breeder as killer or last attacker (including "poison"
  where the last attacker was a breeder), total deaths, CL and max depth at the cap, and the
  number of "Retreating/Backing up" decisions on breeder levels;
- paired rescued and newly-killed counts against control (exact McNemar), and a confirmation tier;
- Priests, Mages, Necromancers and Druids reported separately: low melee, low CL, DL1.

## Repeated on track-p (e2d8919e, 2026-11-22)

Everything above ran on the specimen's own commit, da097a76 (main `12c4ce7c` plus #837). It ran
on neither main nor `track-p`. `track-p` at `e2d8919e` contains da097a76 and is 260 commits ahead
(main `b34196c5` is 155 ahead). It was built here (`harness/build.sh`, clean) and checked three ways.

1. **From birth, the same start.** Track-p's shipped `harness/borg.txt` was used with the zoo's
   changes (respawn race 8, class 3; `borg_world` line dropped) and its own scary list
   (`ff831d0a…`).
   - The shipped settings, `clw_walk` and `csw` all reach the 100,000-turn cap alive (CL 7, 6, 7;
     max depth 3, 2, 3).
   - All three split from the zoo's death at **key 29, turn 261**, in town. Track-p therefore plays
     a different game from the start; this says nothing about the pocket.
2. **The same pocket, a fresh Borg.** The da097a76 game's own checkpoints (62502…66502, every 500
   turns) were loaded with the saved game RNG kept, each into a fresh Borg of da097a76 and of
   track-p ([evidence/fresh-borg-loads-da097a76-vs-track-p.txt](evidence/fresh-borg-loads-da097a76-vs-track-p.txt)).
   - **Track-p's shipped Borg plays the same keys as da097a76's from 7 of the 9 saves**, with the
     same deaths from every save from 64002 on (death turns 66560–67400).
   - It survives from 63002 and 63502 like da097a76. Its keys differ only at 66093 and 66943,
     after it had left the room.
   - Both die from 62502: the priest is still in the corridor there and walks into the room.
   - `caution_breeder_policy 4` on track-p also dies from every save from 64002 on. But a loaded
     Borg starts with empty memory and never learned the down stair at 17,98 (no "Flowing toward
     down-stairs" note; "no up stairs found, exploring"), so "fight through to the stairs" had no
     target.

     This is the stair-forgetting caveat of #544. These loads understate policy 4; the
     from-birth policy-4 run of section 5 is the fair test of it.
3. **The code.** Compared function by function, da097a76 to track-p:
   - unchanged: `retreat`, `back_away`, `borg_happy_grid_bold`, `cornered_boost`,
     `breeder_fight_hard`, `weighted_stair_path`, and `stair_more`'s `avoid: false`;
   - `spread_blocked` changed only in an unrelated #837 clause (immobile reach); its unknown-grid
     rule is the same, now at borg_flow.rs:445;
   - `borg_recall_for_flight` still forecasts before it looks for a scroll (borg_escape.rs:106).
   - **Changed: #880 landed.** `caution_recall_blow_model 1` (shipped) prices poison as HP, caps
     the adjacent attackers, models erratic movers and drops the breeder veto. The section 4
     critique of the model is fixed on track-p. The refusal was moot here anyway: no scroll.

   Line numbers on track-p: `weighted_stair_path` borg_flow.rs:598; `retreat`
   borg_caution.rs:1154; `back_away` :1375; `flight_recall_survivable` :2335; `modelled_blow`
   :2501; `breeder_fight_hard` :5153; `cornered_boost` :5223 (Heroism :5253).

The scripted counterfactuals of section 5 do not use the Borg after the handover, and the engine
is 574b618c on both commits. Their results are a property of this game state, not of a Borg
build. **Every finding except the #758 model holds on track-p**: the flight's route through unknown
grids (#881), exit-blind retreat and back-up (#881, #882), and the Heroism recast (#883).

## Files

| path | what |
|---|---|
| [maps/pocket-at-key-turns.txt](maps/pocket-at-key-turns.txt) | the pocket at turns 62992, 63192 (with the Borg's planned flight), 63592, 63992, 64992, 66292, 66572 |
| [maps/level-overview-66572.txt](maps/level-overview-66572.txt) | rows 8–50, columns 90–179 at the death, with every stair |
| [evidence/exit-series.tsv](evidence/exit-series.tsv) | every 100 game turns: position, HP, worms, least-worm route to the exit |
| [evidence/flight-paths-in-pocket.tsv](evidence/flight-paths-in-pocket.tsv) | the 68 stair-flight paths committed in the room, `?` = unknown in the Borg's map |
| [evidence/moves-after-62900.tsv](evidence/moves-after-62900.tsv) | every move and the note that decided it |
| [evidence/counterfactual-fight-out.tsv](evidence/counterfactual-fight-out.tsv), [evidence/counterfactual-stand.tsv](evidence/counterfactual-stand.tsv) | the two counterfactual sweeps |
| [evidence/fresh-borg-loads-da097a76-vs-track-p.txt](evidence/fresh-borg-loads-da097a76-vs-track-p.txt) | fresh-Borg loads of the pocket saves into da097a76, track-p and track-p policy 4 |
| [evidence/hashes.txt](evidence/hashes.txt) | stream hashes of the zoo cell, the local reproduction, the diagnostic runs and the `ctl` replay; both BUILD_IDs |
| [tools/](tools/) | `diagnostic.patch` (applies to da097a76), `play.sh` (the zoo invocation), `hand.sh`, `fightout2.py`, `paths.py`, `showmap.py`. The scripts expect `SCRATCH` (a work directory holding `env.sh` with `B=<zoo bundle dir>` and the diagnostic build under `diag/`). |

Raw logs stay in the zoo artifact `deaths-4.2.6-reborn-rust-confusion-da097a76-5` of run
44924461733 (90 days). Every counterfactual is a branch of this one life, not an independent sample.
