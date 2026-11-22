# Half-Elf Necromancer 798380952: four missed flasks, a graze and a Phase Door at HP 0 (stats-ban arm)

The death [D-32621a9cd11c](../../deaths/D-32621a9cd11c6723f94706b2936a8745441f1889b901db6d67bd686d6dd7d9ea/README.md)
(imported by borg-cemetery#109) of borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466), experiment
`reborn-fast-fragile-big` ([borg-zoo#596](https://github.com/diegoami/borg-zoo/issues/596)), specimen
`4.2.6-reborn-rust-fast-fragile-7f8c6b80` (borg-reborn-rs `7f8c6b80`), arm `reborn-fastfrag-stats-ban`
(`fast_fragile_policy = 1`, `fast_fragile_by_stats = 1`, `fast_fragile_no_heal = 1`). Half-Elf
Necromancer (race 1, class 4), seed 798380952, killed by "a fatal wound" (a cut) at game turn 93,910,
CL6, DL2, max HP 41, 10,294 keys. The control arm `reborn-fastfrag-ctl` lives to the 100,000-turn cap.

**One life, one start.** Everything here is a direction, not a rate (borg-reborn-rs RULES 14). The
counterfactuals are branches of this one life, not independent games.

## Summary

- **Where it parts from the control.** The two arms play the same 10,288 keys. They part at key
  10,289, game turn 93,906, at HP 0, still bleeding from a graze. The control quaffs Cure Light
  Wounds (HP 20, "You are no longer bleeding") and lives. The stats-ban arm reads Phase Door and dies
  of the cut at the next world tick (93,910). The four missed flasks and the five turns without a cure
  happen in the control too.
- **Either #842 switch alone gives the same death, key for key.**
  - `fast_fragile_policy = 1` alone: `escape_instead` reads Phase Door ("the next turn kills").
  - `fast_fragile_no_heal = 1` alone (policy 0): the heal ban stops the cure, and `borg_caution` reads
    a "critical Phase" next.

  `fast_fragile_by_stats` plays no part, because the crow is a named entry.
- **The throws were the right square and the right attack.** The crow was visible and adjacent. The
  target was its square, a one-grid path. The engine rolled the hit at 79.43% four times and missed
  four times (joint chance 0.18%). A thrown flask has no miss message; it breaks where it lands.
  - "Guessing wall (49,120)" is the Borg's own square. That inherited C rule marks the first unknown
    grid of the path as granite, and here the first grid is the one the Borg stands on. It does not
    move the target.
- **No cure from HP 33 to 10, in both arms.** Attack on sight runs before `borg_caution`, where the
  cures are. Its #760 gate only asks whether the crow's mean damage (4.2 per turn) is below the HP.
  The control was saved only because that gate fails at HP 0.
- **The cut is in no estimate.** Neither "the next turn kills", the #760 gate nor the danger counts
  the cut's 1 HP per world tick. At HP 0 that tick alone kills, so only a cure could save the Borg.
  Phase Door could not.
- **Counterfactuals.** Every alternative tried from 93,866 to 93,896 saves this life: melee, Cure Light
  or Serious Wounds, or Phase Door. At 93,906 (HP 0) only a cure saves it; Phase Door and melee die at
  93,910.

## Reproduction

| what | value |
|---|---|
| zoo cell | `classes-1800-big/4.2.6-reborn-rust-fast-fragile-7f8c6b80/reborn-fastfrag-stats-ban/798380952`, artifact `deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-4` |
| build | the zoo's build artifact `build-4.2.6-reborn-rust-fast-fragile-7f8c6b80` (binary sha256 `6098359c7072…`), and a local build of `7f8c6b80` from source (`harness/build.sh`, binary `66562921…`, rustc 1.97): both give the cell's key stream |
| configuration | the cell's written `user/borg.txt`, `configurations/1b009024c2b8….txt` (sha256 `1b009024c2b84c3c…`); control `9ae69896a3aa….txt` (differs only in the three switches) |
| command | [`tools/run-cell.sh`](tools/run-cell.sh): the zoo's `zoo/borgrs.py` `command()` (borg-zoo `a98b013`), BORG_* cleared, `-exact-turns`, 100,000 turns, from birth. No save is loaded |
| stats-ban | keys.log `0133c6646de79ba4…` = the cell's `play_sha256`; messages.log `5f6a9491…` and state.log `08bbe46d…` byte-equal to the bundle |
| control | keys.log `80f7a7b49bb9cfff…` = its cell's `play_sha256`; alive at 100,000 |
| first differing key | 10,289 (game turn 93,906); keys 1–10,288 identical |

Heavy runs took `flock /tmp/angband-validation.lock`.

## The fight, think by think

Coordinates are x,y as in `state.log`; the Borg's notes print them y,x (`(49,121)` is x121,y49). The
Borg stands at x120,y49 throughout. The screen after key 10,240 shows `#@B.`, the crow (`B`) on
x121,y49, beside it ([screen](data/screen-after-key-10240.txt)). The cut column is `TMD_CUT` from
`state.log` (`t8:N`). The full trace extract is in [data/fight-trace.md](data/fight-trace.md).

| think | game turn | first key | HP | SP | cut | Borg's choice (check `fight_before_flight` every time) | engine result until the next think |
|---|---|---|---|---|---|---|---|
| 6744 | 93,846 | 10,219 | 33 | 2 | – | Nether Bolt at a cave spider (attack 38) | spider dies |
| 6745 | 93,856 | 10,230 | 33 | 1 | – | crow created at (49,122). "Fast-fragile (named): crow (speed +8 vs +0, 10 HP vs 9.5 per turn, 4.2 damage/turn …)", "Attack on sight: crow (fast-fragile), 9 HP, attack 38 (#842)": Nether Bolt | "You failed to concentrate hard enough!" (SP 1 → 0); the crow moves to x121,y49; 2 misses |
| 6746 | 93,866 | 10,242 | 33 | 0 | – | "Attack on sight … attack 2 (#842)", "Targeting crow who has 9 Hit Points (49,121)", throws a Flask of oil | "The Flask of oil breaks." (no hit); 3 bites, 1 miss |
| 6747 | 93,876 | 10,254 | 24 | 0 | – | "Perhaps wall near targetted location (49,121)", "Guessing wall (49,120) near target (49,121)"; attack 2, flask | breaks, no hit; 2 bites, **"You have been given a graze."** (93,880) |
| 6748 | 93,886 | 10,266 | 15 | 0 | 9 | same notes; flask | breaks, no hit; 3 bites, 1 miss; cut tick at 93,890 |
| 6749 | 93,896 | 10,277 | 10 | 0 | 8 | same notes ("4.2 damage/turn = 42% of HP 10"); flask | breaks, no hit; 4 bites; cut tick at 93,900 |
| 6750 | 93,906 | 10,289 | 0 | 0 | 7 | "Fast-fragile (named): … 0% of HP 0", "Fast-fragile: the next turn kills (4.2 damage/turn, HP 0), the kill needs 1.3 turns: Phase Door (#842)": `ESC ESC r n` | Phase Door; the cut tick at 93,910 takes HP 0 → −1: "You die." |

The graze of 93,701 is not the fatal cut. It ended at 93,710 ("You are no longer bleeding"). The fatal
cut is the second graze, at 93,880.

The pack at 93,866 ([throw prompt after key 10,249](data/screen-after-key-10249.txt)): 17 Flasks of
oil (`f`), 18 Cure Light Wounds (`g`), 3 Cure Serious Wounds (`i`), 3 Berserk Strength (`m`), 11
Phase Door (`n`), a Word of Recall (`o`). At death: 13 flasks and 10 Phase Door, the potions untouched.
The targeting screen after key 10,244 reads "You are on an open floor, 0 N, 0 E": the cursor starts on
the Borg's own square ([screen](data/screen-after-key-10244.txt)).

## Q1. Why did four flasks at an adjacent crow all miss?

**The square was right.** At 93,866 the keys are `* p 6 5` (targeting mode, cursor to the player,
one step east, select: "Target Selected."), then `v / f 5`: throw, item list, the flasks, and `5`, "use
the target" (`engine/angband/src/ui-input.c:1661-1663`). The screen shows the crow on that square.

Under gdb on the zoo binary ([tools/hit-roll.gdb](tools/hit-roll.gdb),
[data/hit-rolls-gdb.txt](data/hit-rolls-gdb.txt); the key stream is unchanged under gdb), each throw:
- runs `project_path` with range 10 from (x120,y49) to (x121,y49);
- calls `make_ranged_throw` on the crow's square (`src/player-attack.c:1123-1131`, `1270-1279`);
- checks `monster_is_obvious` (visible);
- rolls `random_chance_check` at **7943/10000**.

That is the engine's hit chance:
- `chance_of_missile_hit_base` for a THROWING object is the throw skill plus 3 per to-hit point
  (`src/player-attack.c:121-145`; the flask has `THROWING`, `lib/gamedata/object.txt:254-264`);
- one point is lost for the distance, and there is no halving because the crow is visible
  (`:156-164`);
- `hit_chance` gives a 12% sure hit, a 5% sure miss, and `(to_hit − AC×2/3) / to_hit` otherwise
  (`:196-220`);
- the crow's AC is 14 (`lib/gamedata/monster.txt:1151-1162`);
- 7943 is a to-hit of 48: 10000 × 39/48 = 8125, × 0.83 = 6743, + 1200.

Four misses at 20.57% each is a 0.18% event. Over the whole game this character hit with 49 of 61
flask throws.

**"Breaks" with no hit message is a miss.** `ranged_helper` prints only on success (`src/player-attack.c:1123-1179`).
Then it drops the missile with its breakage chance (`:1209-1213`), and a flask always breaks
(`lib/gamedata/object_base.txt:159-161`, `break:100`).

**"Guessing wall (49,120)" is the Borg's own square.** A ranged attack sets
`successful_target < 0`. When no hit message clears it, `borg_update` calls
`borg_target_unknown_wall` (`borg-core/src/borg_update.rs:1729-1739`). That function walks the path
from the Borg's own grid. The first grid whose `feat` is `FEAT_NONE` becomes `FEAT_GRANITE`
(`borg-core/src/borg_projection.rs:746-835`). The C function does the same
(`engine/angband/src/borg/borg-projection.c:753-754`, `809-813`).

The note shows that the Necromancer's own grid was unknown in its map ("Light 0" on the status line).
So the Borg wrote a wall under itself after every miss, and then set `successful_target = 2`. That
skips the one round without a ranged attack that `missed_before` would have imposed
(`borg-core/src/borg_fight_attack.rs:1803-1813`). The engine's target was not affected: the Borg did
not target the wrong square. Whether the skipped round would have led to melee is not established
here.

## Q2. Why the throw (attack 2) every turn, not Nether Bolt (38) or melee?

- **Nether Bolt.** The failed cast at 93,856 spent the last SP ("You failed to concentrate hard
  enough!"; `state.log` SP 1 → 0 from 93,864). With SP 0 the spell is not an option.
- **Throw over melee.** The focused attack ranks the candidates by expected damage per turn, then by
  family priority (`borg-core/src/borg_fight_attack.rs:5257-5265`, `5289-5291`, `5363`). The flask's
  "7.9 per turn" is 0.7943 × the 10 HP it needs. A hit does 1d4 × (2 + 20/12) for a THROWING object,
  × 3 for EXPLODE (`src/player-attack.c:569-578`, `1296-1297`): 9 to 36, mean 22.5. So every hit
  nearly always kills. The estimate already includes the miss rate, and the rolls are independent, so
  repeating the throw after a miss is what the estimate says to do. The melee estimate is not in the
  core trace (the focused-attack candidates are not traced), so the margin is not known.
- **Where a miss is recorded.** Only in `successful_target`, the C Borg's "shot into darkness" logic
  (Q1). That logic took the misses for walls. Nothing in attack on sight counts misses, and for
  independent 79% rolls nothing needs to.

**No defect found in the attack choice.** Melee would also have saved this life (counterfactuals N01,
N04, N08): one hit and "The crow flees in terror!". That is a consequence, not evidence that melee
was rated better.

## Q3. Why no cure from HP 33 to 10, while cut and bitten?

The order is `borg_think_dungeon`: `fight_before_flight` (attack on sight, then `winning_fight`) at
`borg-core/src/borg_think_dungeon.rs:736-745`, before `borg_caution` at `:797`. The cures, and the
heal ban, are inside `borg_caution` (`borg-core/src/borg_caution.rs:239`, `486-560`, `815-830`).

`attack_on_sight` (`borg-core/src/borg_fight_attack.rs:5458-5491`) tries the #842 branch first, then
the #760 branch:

- **#842 branch** (`policy = 1`): `classify` (named crow), then `category_attack_safe_with(…,
  gate_target = false)`. That passes at `hp >= 0`, "HP 0 is alive" (`borg_caution.rs:2387-2400`).
  Then `escape_instead`, then `yield_to_cure` (only when `no_heal = 2`), then the attack.
- **#760 branch** (the control, `policy = 0`): `category_attack_safe`, whose gate is
  `hp > 0 && target_damage < hp` with the crow's **mean** damage, 4.2 per Borg turn
  (`borg_caution.rs:2371-2373`, `2380-2382`).

So in both arms the attack takes every turn from HP 33 to 10. The cure is never considered, and the
heal ban never fires in this fight (no "No healing potion" note). The real losses per Borg turn were
9, 9, 5 and 10: up to four 1d3 bites, plus the cut from 93,880. The control survives only because its
gate fails at HP 0 (`hp > 0`), which hands the turn to `borg_caution` and its Cure Light Wounds. With
the policy on, the gate has no HP test left but `hp >= 0`, and `escape_instead` acts first.

## Q4. The cut: engine damage, cure, and the Borg's estimates

- A graze is `TMD_CUT` up to 10 (`lib/gamedata/player_timed.txt:264-276`). Every world tick (every 10
  game turns at normal speed, `src/game-world.c:1080-1081`), a cut below Severe deals 1 HP, a Severe
  Cut 2, and a Deep Gash or Mortal Wound 3 (`src/game-world.c:522-538`).
- The counter falls by `adj_con_fix + 1` per tick (`src/game-world.c:282`, `300-312`), and a cut
  stops HP regeneration (`src/player-util.c:470`). A player below 0 HP dies (`src/player-util.c:228`).
- Cure Light Wounds: `HEAL_HP` 20 and `TIMED_DEC:CUT` 20 (`lib/gamedata/object.txt:3156-3172`), so it
  ends a graze. Cure Serious Wounds: `HEAL_HP` 40 and `CURE:CUT` (`object.txt:3175-3190`).
- **The Borg counts the cut nowhere in this decision:**
  - "the next turn kills" (`escape_wanted`, `borg-core/src/borg_fast_fragile.rs:84-90`) compares only
    `incoming_total` (`:194-207`), the monsters' blows from `fight_incoming_with`
    (`borg_caution.rs:2221-2251`);
  - the #760 gate uses the same blow estimate;
  - `borg_danger.rs` reads no `BI_ISCUT`.

  At 93,906 the Borg had 4 game turns before a tick that kills it at HP 0, whatever the crow does.

## Q5. The Phase Door at HP 0: the threshold

`escape_wanted` fires when `incoming × 100 ≥ fast_fragile_escape_percent × HP` and the kill needs
more than one more turn. The threshold is `fast_fragile_escape_percent = 100`, a hypothesis
(`params.rs:49`, "no measurement chose 100").

- At HP 10: 420 < 1000, so the Borg attacks. That turn cost it 10 HP.
- At HP 0: 420 ≥ 0, so it escapes, but by then a cure was the only move that could live.

What the threshold should count (all hypotheses, RULES 14):
- the Borg's own damage before its next action (the cut's tick here, poison elsewhere);
- the spread of the blows (four 1d3 bites are up to 12 a turn, against a mean of 4.2), rather than
  the mean;
- when that damage alone reaches HP + 1, a cure that stops it (CLW or CSW for a graze), ahead of
  Phase Door and ahead of the heal ban.

The miss rate is already in `per_turn` (0.794 × 10). The "kill needs 1.3 turns" is right as an
expectation; the chance of no kill in two throws is 4.2%.

## Q6. Where this game parts from the control

At key 10,289, game turn 93,906:
- **Control** (all switches 0): no attack-on-sight note (the #760 gate fails at HP 0), then
  "Quaffing Potions of Cure Light Wounds", "You are no longer bleeding". Its next flask hits at
  93,916 and the crow flees. It quaffs Cure Serious Wounds at 93,926 and lives to the cap.
- **stats-ban**: `escape_instead` reads Phase Door. The point is the #842 policy, or the heal ban on
  its own:

| policy | by_stats | no_heal | keys.log | end |
|---|---|---|---|---|
| 0 | 0 | 0 | `80f7a7b49bb9…` | alive, 100,000 (control cell) |
| 0 | 0 | 1 | `0133c6646de7…` | died 93,910: heal ban ("No healing potion in contact with a fast-fragile attacker (#842)"), then "Phase (escape 1.2 critical)" |
| 0 | 1 | 1 | `0133c6646de7…` | died 93,910 |
| 1 | 0 | 0 | `0133c6646de7…` | died 93,910: `escape_instead` |
| 1 | 0 | 1 | `0133c6646de7…` | died 93,910 |
| 1 | 1 | 0 | `0133c6646de7…` | died 93,910 |
| 1 | 1 | 1 | `0133c6646de7…` | died 93,910 (stats-ban cell) |

([data/variants.tsv](data/variants.tsv), full hashes.)

## Q7. Counterfactuals on the exact game

**Method.** The scratch frontend hook [tools/inject-frontend.patch](tools/inject-frontend.patch) is
applied to `engine/frontend/main-borgh.c` of a `7f8c6b80` checkout, never committed (RULES 9: the
engine tree is untouched).
- The game is played from birth by the same Borg. After key N, `inkey_hack` answers with the
  injected keys, then hands control back to the same Borg, its memory intact. No save is loaded and no
  new Borg is started.
- With no injection set, the patched build plays the death key for key (`0133c6646de7…`).
- `melee:crow` attacks an adjacent crow every turn until none is adjacent (ESC ×3 between attacks for
  `-more-` prompts).
- `q i` / `q g` / `r n` = quaff Cure Serious Wounds, quaff Cure Light Wounds, read Phase Door, each
  after two ESC.

Run with [tools/counterfactuals.sh](tools/counterfactuals.sh) and [tools/cases.txt](tools/cases.txt);
summarised by [tools/summarize.py](tools/summarize.py) into
[data/counterfactuals.tsv](data/counterfactuals.tsv), which also holds the key hashes.

| case | after key (turn, HP) | instead of the Borg's choice | HP when the Borg takes over | the crow | end |
|---|---|---|---|---|---|
| N01 | 10,241 (93,866, 33) | melee | 33 | flees in terror after the first hit (93,866) | alive, cap |
| N02 | 10,241 | Cure Serious Wounds | 41 | flees 93,886 | alive, cap |
| N03 | 10,241 | Phase Door | 33 | out of contact | alive, cap |
| N04 | 10,253 (93,876, 24) | melee | 24 | flees 93,876 | alive, cap |
| N05 | 10,253 | Cure Serious Wounds | 41 | flees 93,886 | alive, cap |
| N06 | 10,253 | Phase Door | 24 | out of contact | alive, cap (CL7) |
| N07 | 10,253 | Cure Light Wounds | 41 | flees 93,886 | alive, cap |
| N08 | 10,265 (93,886, 15) | melee | 14 | flees 93,886 | alive, cap (lowest HP 13) |
| N09 | 10,265 | Cure Serious Wounds (cures the graze) | 41 | dies 93,896 | alive, cap |
| N10 | 10,265 | Phase Door | 14 | dies 93,926 | alive, cap (CL7) |
| N11 | 10,276 (93,896, 10) | Cure Serious Wounds | 41 | dies 93,906 | alive, cap |
| N12 | 10,276 | Phase Door | 9 | dies 93,936 | alive, cap (CL7) |
| N13 | 10,276 | Cure Light Wounds | 30 | dies 93,906 | alive, cap |
| N14 | 10,288 (93,906, 0) | Cure Light Wounds (the control's move) | 20 | flees 93,916 | alive, cap |
| N15 | 10,288 | Cure Serious Wounds | 40 | flees 93,916 | alive, cap |
| N16 | 10,288 | melee | −1 | flees 93,906 | **died 93,910, a fatal wound** |

Every alternative saves this life from 93,866 to 93,896. At HP 0 only a cure does: Cure Light Wounds
is enough, and the arm's own Borg then plays on to the cap (N14). After N14 the policy Borg is the
same Borg that died. So the death is the single choice at 93,906, made by either #842 switch.

## Defects (borg-reborn-rs; each a lead until the zoo measures it)

- [borg-reborn-rs#926](https://github.com/diegoami/borg-reborn-rs/issues/926): at HP 0 and bleeding,
  Phase Door (`escape_instead`) or the heal ban replaces the cure that saves; "the next turn kills"
  counts neither the cut nor poison. Decisive here.
- [borg-reborn-rs#927](https://github.com/diegoami/borg-reborn-rs/issues/927): attack on sight
  comes before every cure; the #760 gate uses the mean target damage. Both arms.
- [borg-reborn-rs#929](https://github.com/diegoami/borg-reborn-rs/issues/929): a missed throw is
  read as a shot into an unknown wall, and the guessed wall is the Borg's own grid (as in C). No effect
  on this death established.

Not confirmed: "thrown oil targets the wrong square" (it did not: the engine rolled and missed),
and "attack on sight repeats a failing attack" (the throw is a 79% kill each turn; its estimate
includes the miss rate). Compare borg-reborn-rs#870, which concerns how point-blank throws are rated.
