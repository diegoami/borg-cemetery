# Where and when the Borg rests (borg-reborn-rs#615, step 1)

borg-reborn-rs#615 asks for an analysis before any rule: for every rest,
its kind and grid, whether and how soon it was interrupted, and the deaths
soon after an interrupted rest. This is that analysis, on one build and 108
games. It is a lead, not a measurement (no zoo run).

## The run
- **Build:** borg-reborn-rs main `6370643d` (borg-rs core, the shipped
  `harness/borg.txt`), plus a local diagnostic that was never committed
  ([rest-diag.patch](rest-diag.patch)). Whenever the Borg starts a rest (an
  `R` key at the head of the key queue or after Escape), it appends one line
  to a side file: the game turn, the feature under the Borg, its 8
  neighbours (passable, unknown, doors), HP and SP, depth, the scary and
  fleeing flags, and the youngest awake known monster (Borg-time age and
  distance). It writes to a file only, not to the game's message list, so it
  changes no decision.
- **Starts:** 108 ([starts.txt](starts.txt)), 100,000 game turns each:
  - borg-zoo's classes-18 (18 starts);
  - classes-1800-small (90 starts: starts 1-90, 10 per class).
- **What happened after each rest:** read from the next think in
  `trace-core.jsonl` (HP, SP, danger, depth) and the game messages between
  the two thinks:
  - **attacked:** an attack message, or HP lower than when it started;
  - **monster:** danger above 0 at the next think, without full HP and SP;
  - **complete:** HP and SP full;
  - **stopped short:** none of these; mostly a one-turn rest, see below;
  - **level change:** Recall or stairs.

  [analyze_rests.py](analyze_rests.py) builds the per-rest table
  ([rests.csv.gz](rests.csv.gz)) and [tables.py](tables.py) the tables
  ([tables.md](tables.md)).

## Findings

**13,425 rests in 108 games, 7,433 of them in town.** 4 games died: CL1-4,
none in town.

### 1. Most rests are one turn long: an awake monster is in view
**The pattern:** the game stops a rest at once when a monster comes into
view. The Borg's rest check (`borg_check_rest`) looks at fear and danger, not
at awake monsters in view, so it rests, is disturbed after one player turn
(10 game turns), thinks again, and rests again.

| where | rests | one-turn rests | with an awake monster seen within 5 Borg-time units | in runs of one-turn rests | games |
|---|---:|---:|---:|---:|---:|
| town | 7,433 | 4,708 (63%) | 4,459 | 4,222 (844 runs, longest 30) | 85 |
| dungeon | 5,992 | 783 (13%) | 692 | 617 (146 runs, longest 32) | 80 |

These rests cost little game time, but each one is a think spent standing
next to an awake monster.
- **In town** it is the townsfolk (#604, #618, #619).
- **In the dungeon** an awake monster 3 grids away is typical.

### 2. Interruptions follow the monsters, not the grid
Dungeon rests (depth > 0), by the grid the Borg rests on:

| grid | rests | interrupted | attacked |
|---|---:|---:|---:|
| staircase | 1,185 | 146 (12%) | 75 (6%) |
| dead end | 27 | 3 (11%) | 0 |
| corridor (2 passable neighbours) | 1,629 | 258 (16%) | 100 (6%) |
| room edge or junction (3-4) | 1,574 | 236 (15%) | 109 (7%) |
| open room (5-8) | 1,577 | 272 (17%) | 96 (6%) |
| *next to a door* | 597 | 88 (15%) | 41 |
| *on a scary level* | 395 | 120 (**30%**) | 32 |
| *fleeing* | 808 | 204 (**25%**) | 66 |

By the youngest awake known monster:

| awake monster last seen | rests | interrupted | attacked |
|---|---:|---:|---:|
| 0-5 Borg-time units ago | 1,444 | 339 (**23%**) | 92 |
| 6-20 | 165 | 40 (24%) | 19 |
| 21-50 | 160 | 26 (16%) | 12 |
| 51-200 | 161 | 17 (11%) | 6 |
| longer ago, or none | 4,062 | 493 (12%) | 251 |

- **The grid matters little:** the attacked share is 6-7% on every kind of
  grid. A staircase is interrupted least (12%) and is an escape when it is.
- **What doubles the interruption rate:**
  - an awake monster seen in the last 20 Borg-time units (23-24% against
    12%);
  - a scary level (30%);
  - a flight (25%).
- **Unknown grids:** the Borg almost never rests next to them (3 rests),
  because rests happen on mapped ground.

By kind of rest (all depths):

| kind | rests | interrupted | attacked |
|---|---:|---:|---:|
| HP (`# Resting to recover HP/SP`) | 9,454 | 984 (10%) | 389 |
| mana (`# Resting to gain Mana`) | 3,748 | 428 (11%) | 214 |
| Recall (`# Resting for Recall`, `# Waiting for Recall`) | 217 | 56 (**26%**) | 29 |

Interrupted rests are interrupted early: the median is 10 game turns.

### 3. Rests are not what killed these 4 games
| game | class | died at | last rest | kind | grid | outcome | game turns before the death |
|---|---|---:|---:|---|---|---|---:|
| 1199401383 | Necromancer | 88,127 | 83,682 | mana | open room, scary level | complete | 4,445 |
| 1516096046 | Druid | 3,400 | 2,931 | HP | room edge | complete | 469 |
| 1569794094 | Priest | 8,158 | 8,062 | HP | room edge | complete | 96 |
| 300461652 | Mage | 3,211 | 1,131 | HP | staircase | complete | 2,080 |

- **Their last rests:** every one completed.
- **Interrupted rests before a death:** only the Priest had one within 2,000
  game turns (game turn 7,001, on a staircase, a monster), 1,157 turns
  before it died.
- **What this means:** in this sample, interrupted rests cost thinks and HP
  but kill nobody directly. The rest deaths behind #615 (Druid 1678765969,
  priest-809881907) are rarer than 1 in 108.

## The candidate rules, ranked by what they would touch
Dungeon rests only; window 2,000 game turns.

| rule | rests touched | of them interrupted | attacked | deaths after a touched rest |
|---|---:|---:|---:|---:|
| **when:** no rest with an awake monster seen within 20 Borg-time units (#567's rule, generalized) | 1,609 | 379 (24%) | 111 | 1 |
| **when:** no rest on a scary level unless on a staircase | 377 | 112 (30%) | 28 | 0 |
| **when:** after two interruptions on one grid, move first | 468 | 100 (21%) | 35 | 0 |
| **where:** not in a room (walk to a staircase or corridor first) | 3,151 | 508 (16%) | 205 | 2 |
| **where:** not next to unknown grids | 3 | 0 | 0 | 0 |
| (all dungeon rests) | 5,992 | 915 (15%) | 380 | 2 |

1. **Awake monster seen recently: the strongest lead.**
   - In the dungeon it targets the rests interrupted twice as often (24%
     against 12%).
   - In town it would remove most of the 4,459 one-turn rests.
   - It is #567's ask (Recall rests), applied to every rest. The parameter
     would be a Borg-time age; the data put the step between 20 and 50
     (interruptions fall from 24% to 16%).
   - What the Borg does instead matters: keep exploring or fighting, walk
     away, or wait on a staircase.
2. **Scary level, not on a staircase:** the highest interruption rate (30%),
   on few rests (377). It generalizes #614, which only covers a committed
   flight.
3. **Move after two interruptions:** 468 rests, 21%; this mostly overlaps
   rule 1 (the same monsters).
4. **Where:** a corridor is no safer than a room here (16% against 17%),
   and the attacked share is the same. Walking to a corridor is not
   supported. A staircase is a little safer (12%), and it is also an escape,
   which #614's `caution_stairs_leave_on_monster` uses.
5. **How long:** not measurable here. The interruptions come at once
   (median 10 game turns), so shorter rests would not change them.

## Not checked
- **No zoo run:** 108 games on one build are direction, not a measurement
  (RULES 14 there).
- **The diagnostic build's keys against main:** not compared. The
  diagnostic only appends to a side file.
- **The 4 deaths have no Cemetery dossiers.** They were played on a
  diagnostic build, and none is a rest death.
- **"Awake" and its age** are the Borg's memory of monsters
  (`kill.awake`, `kill.when`), not the engine's.
- **The Recall-wait rests** (217) are the subject of #582/#583; they are
  counted here, not analysed.
