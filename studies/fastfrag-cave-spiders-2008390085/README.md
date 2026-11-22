# Cave spiders, a Potion of Speed and the fast-fragile ban: High-Elf Rogue 2008390085

Investigation of one death of the `reborn-fastfrag-stats-ban` arm of borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466)
(experiment `reborn-fast-fragile-big`, [borg-zoo#596](https://github.com/diegoami/borg-zoo/issues/596),
specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`, borg-reborn-rs
[`7f8c6b80`](https://github.com/diegoami/borg-reborn-rs/commit/7f8c6b80a617eba3a6f2b83e4ba9d45b7b552b73),
PR [#847](https://github.com/diegoami/borg-reborn-rs/pull/847), issue
[#842](https://github.com/diegoami/borg-reborn-rs/issues/842)). Dossier:
[D-af342fe11101](../../deaths/D-af342fe111018d78cd4dca016ffce4069371996a691ee9e598981e25dc15a1e7/README.md);
run page: [runs/2026-11-22-fastfrag-stats-ban](../../runs/2026-11-22-fastfrag-stats-ban/README.md).

High-Elf Rogue (race 9, class 6), seed 2008390085, CL6, DL2, max HP 39, killed by a cave
spider at game turn 64,483. Arm settings on top of the shipped `harness/borg.txt`:
`fast_fragile_policy = 1`, `fast_fragile_by_stats = 1`, `fast_fragile_no_heal = 1`.
The control arm (`reborn-fastfrag-ctl`) lives to the 100,000-turn cap.

The owner's view: quaffing a Potion of Speed would have saved him. **It would have, at any
Borg turn up to 64,454** (table below). The Borg never considered it: it believed it was still
hasted from a potion drunk at 56,229 (see the correction below, #941). The fast-fragile policy also took the turn
at 64,454 that the control spent on the Phase Door that saved it.

**One life, one start.** Every row of the counterfactual table is a continuation of the same
game, not an independent sample (RULES 12/14 of borg-reborn-rs). It shows what this game
needed, not a rate. Thresholds named below are hypotheses until borg-zoo measures them.

## Reproduction

- The zoo's raw bundle (artifact `deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-8`) could not
  be downloaded from this session: the artifact storage host is outside its network policy.
  The game was rebuilt from birth instead. Deterministic play (seed, build, borg.txt) gives the same
  key stream. The hashes below prove it.
- Build: borg-reborn-rs `7f8c6b80`, `BORG_IMPL=rust harness/build.sh` (engine `574b618c`,
  recorder off). The binary's sha256 differs from the CI binary's (`6098359c…`), as any local
  compiler's does. The play is identical.
- borg.txt: rebuilt with borg-zoo's own `zoo.borgrs.config_text` from the catalogue at borg-zoo
  `97e54f9`. `borg-stats-ban.txt` here has sha256 `58b6d86c55df…`, the cell's
  `borg_txt_sha256` in the dossier's `config.txt`. `borg-ctl.txt` (`fbf2663eb101…`) is the control's.
  Scary list: the build's `harness/scary_monsters.txt`, sha256 `9766d882…` (the dossier's).
- Command: `runcell.sh` is the zoo's `zoo/borgrs.py:command()` with the message and state
  logs on (`-menu-letters -exact-turns`, 100,000 turns, `TZ=UTC`, ambient settings cleared).
  `scripts/native/rerun-death.py` refused this zoo cell (its rebuilt borg.txt hashed
  `7e4c006a000f`, not `58b6d86c55df`), so the zoo's own builder was used.
- Result, played from birth: death by a cave spider at 64,483, 9,280 keys. Byte for byte equal
  to the dossier's raw hashes:

  | log | sha256 (rerun = zoo cell) |
  |---|---|
  | keys.log | `1ef124668f172b7a692e78310bc41fc332302c992ec893c18e429c5ab7f6088a` |
  | messages.log | `8410b8083e6fddfe75c160ae89bab207c95ed47226807707cb14642fbfeb3238` |
  | state.log | `064f346ca049984edf6b9ac419dd8960c79632a01090416c4cfd31879a56f27e` |

- Control from birth, the same way: reaches the cap (100,000 turns, CL6, max DL2, HP 39/39).

## What the engine says (574b618c)

| fact | where |
|---|---|
| Cave spider: speed 120 (+10), 7 HP, `BITE:HURT:1d4`, `friends:100:2d8:Same` (comes with 2d8 others) | `lib/gamedata/monster.txt:1116-1131` |
| Each non-unique monster gets `rand_spread(0, turn_energy(speed)/10)` = ±2 speed: a cave spider is 118-122 | `src/mon-make.c:1158-1164` |
| Shrieker's SHRIEK: `WAKE` then `PROJECT_LOS:MON_SPEED`, dice 25 | `lib/gamedata/monster_spell.txt:139-148` |
| MON_SPEED sets the monster's FAST timer to the damage (25) | `src/project-mon.c:943-947` |
| A FAST monster moves at +10 more; the timer falls by 1 each monster turn | `src/mon-move.c:1928-1938`, `1800-1801` |
| Grouped message: "3 cave spiders start moving faster." (`"%d %s"` with the plural) | `src/list-mon-message.h:44`, `src/mon-msg.c:333-345` |
| Potion of Speed: `TIMED_INC:FAST`, 20+2d10 turns, cost 75 | `lib/gamedata/object.txt:3429-3439` |
| Player FAST: +10 speed | `src/player-calcs.c:2176-2177` |
| Energy per game turn: `extract_energy[speed]`; 110 → 10, 120 → 20, 122 → 22, 130 → 30, 132 → 32 | `src/game-world.c:68-89`, `136-139` |
| Cure Light Wounds heals 20 (HEAL_HP minimum), Phase Door teleports 10 | `lib/gamedata/object.txt:3156-3170`, `2571-2581`; `src/effect-handler-attack.c:201-230` |

So a cave spider acts 1.8–2.2 times per turn of the unhasted rogue (energy 18–22 against
10). After the shriek's haste it acts 2.8–3.2 times (28–32 against 10). With a Potion of Speed
(120, energy 20), the rogue is level with an unhasted spider (0.9–1.1) and the hasted spiders
act only 1.4–1.6 times per rogue turn: the bites per rogue turn halve, and an unhasted spider
can no longer both follow and bite while the rogue walks. The haste lasts 25 monster turns, about 8–9 turns of the
unhasted rogue.

## The fight, turn by turn

Positions are (y,x). The up-stairs the Borg flows to is 19 steps away at 64,414. Key numbers
are lines of `keys.log`; the "check" is the core trace's chosen rung
(`trace-core-tail.jsonl` in the dossier).

| turn | keys | Borg | HP | danger | spiders (y,x) | decision and why |
|---|---|---|---:|---:|---|---|
| 64,384 | 9226-9235 | (3,113) | 39 | 21 | asleep at (2,114) | Cave spider seen: it is on the named scary list up to CL20-23 (`harness/scary_monsters.txt:74`): "Scary guy on level", **goal fleeing set**. Phase rule: no awake enemy adjacent, so attack at range: throws a Flask of oil, kills it. (check `borg_caution`) |
| 64,394 | 9236-9245 | (3,113) | 39 | 21 | none (a stale memory of the dead one at (2,114)) | "There was a monster 'cave spider' at (2,114)": throws the **last** Flask of oil at the empty square ("Guessing wall"). |
| 64,404 | 9246-9247 | (3,113)→(4,113) | 39 | 21 | none known | "Retreating to 8,113" (strategic retreat from the stale danger). |
| 64,406 | | | | | | The shrieker at (7,125) shrieks: "a sudden stirring": the level wakes. |
| 64,414 | 9249-9250 | (4,113)→(5,112) | 39 | 30 | (3,113) | "Desperate for Stairs (three)", flow cost 19. The adjacent spider is faster, but its danger alone is under 50% of HP (`caution_desperate_fast_danger_percent = 50`, #747), so the walk is allowed. |
| 64,421 | | | 38 | | | bitten |
| 64,424 | 9251-9252 | (5,112)→(6,111) | 38 | 31 | (4,112), (3,113) | stairs, cost 18 |
| 64,430-64,434 | | | 32 | | | bitten twice. The shrieker shrieks again: "3 cave spiders start moving faster." The Borg logs "PAIN:3 cave spiders" and three times "Assuming player ghost (3 cave spiders)" (Q4). |
| 64,434 | 9255-9256 | (6,111)→(7,112) | 32 | 34 | (5,112), (5,113), (4,112) | stairs, cost 17 |
| 64,438-64,444 | | | 23 | | | 6 bites, 4 hit |
| 64,444 | 9258-9260 | (7,112)→(8,113) | 23 | 63 | (6,113), (6,112), (6,111), (4,113) | "Possibility of being surrounded (4/3)". "Retreating to 8,113 (63 > 18)": one step. |
| 64,450-64,454 | | | 18 | | | 2 bites hit |
| **64,454** | 9262-9264 | (8,113) | 18 | 55 | (7,113), (7,112), (6,114) | **Fork with the control.** "Fast-fragile (stats): cave spider (speed +22 vs +0, 8 HP vs 10.4 per turn, 5.0 damage/turn = 28% of HP 18, 2 others in view)". Attack on sight with the Dagger kills the spider at (7,112). (check `fight_before_flight`, before `borg_caution`). **The control reads Phase Door here** ("escape 1 emergency"). |
| 64,457-64,461 | | | 7 | | | 4 bites hit |
| 64,462 | 9268-9269 | (8,113)→(9,112) | 7 | 53 | 3 in contact | No attack on sight this think (no "Attack on sight" note): the other spiders' danger is above 2 × HP = 14, so `category_attack_safe_with` skips the target. "Fight race: 3 attackers, 3.000 turns to kill, 13.127 damage/turn, HP 7: not winning (#759)". "**No healing potion in contact with a fast-fragile attacker (#842)**": the cure is banned. Strategic retreat one step, "53 > 14", which comes before `borg_escape` (Phase Door) in `borg_caution`. |
| 64,466-64,469 | | | 6 | | | bitten, missed |
| 64,472 | 9270-9272 | (9,112) | 6 | 12 | (8,113) | Attack on sight (fast-fragile, "1 others in view"), 1 hit, 1 miss; the spider flees in terror. |
| 64,479 | 9274-9276 | (9,112) | 6 | 11 | (8,113) | Attack on sight, two hits, not killed (8 HP, Dagger 1d4). |
| 64,480-64,483 | | | -3 | | | bitten, grazed, bitten: dead. 3 Potions of Speed, 22 CLW, 4 CSW and 14 Phase Door in the pack. |

## Correction (2026-11-22, later the same day): the speed flag was stuck

Checking the #913 fix on this game found the deeper cause. At 56,229 the rogue
drank a Potion of Speed. At 56,550 the engine ended it: "You feel yourself slow down."
(`player_timed.txt:194-198`). The Borg parsed that line as **monster pain**
("PAIN:You feel yourself", then three "Assuming player ghost (You feel yourself)"),
because the pain suffix "slow[s] down." (`borg_messages.rs:215`) is tried
(`borg_messages.rs:818`) before the temporary-effect table (`:967`). The timer
fallback in `borg_trait.rs` only ever sets `temp.fast`. **From 56,229 to its death the
Borg believed it was hasted.** All three rules below start with "already fast →
no", and the danger counted the rogue at +10. The reasons given in Q1 (fleeing,
the thresholds, Phase Door in the pack) are real, but they were never reached.
Filed as [borg-reborn-rs#941](https://github.com/diegoami/borg-reborn-rs/issues/941).

Replays of the zoo's game on `7f8c6b80` plus the fix commits (a local branch,
never pushed). With every switch off it plays the zoo game key for key (keys `1ef12466…`):

| switches on (borg.txt lines added to `borg-stats-ban.txt`) | outcome |
|---|---|
| none | dies at 64,483 (the zoo game) |
| `trait_timed_sync = 1` (#941) | lives to the cap: `borg_defend_aux_speed` drinks Speed at 64,344 (danger 20 at HP 39, against the shrieker) |
| `caution_emergency_speed_danger_percent = 50` (#913) | same keys as the zoo game: the stuck flag stops it |
| #941 + #913 | lives to the cap; #913's rule fires later in that game (76,970) |
| `caution_retreat_from_faster = 1` (#916) | lives to the cap (CL7, max DL3) |
| `fast_fragile_contact_max = 1` (#914) | lives to the cap |
| `kill_grouped_names = 1` (#915) | same keys as the zoo game |
| all five | lives to the cap |

On `track-p` (`86843a79`) this seed no longer dies, switches off or on. The #941 bug
is there too: in `track-p`'s game the haste of 37,688 ends at 37,930 and is again
parsed as pain. PRs, all into `track-p` and shipped 0: #943 (#915), #944 (#916),
#945 (#913), #946 (#914), #947 (#941). Zoo request:
[borg-zoo#652](https://github.com/diegoami/borg-zoo/issues/652).

## Q1. Which rule drinks Speed, and why it never fired

borg-core at `7f8c6b80` has three ways to drink a Potion of Speed. All three are out of
reach in this fight:

1. **`borg_defend_aux_speed`** (`borg-core/src/borg_fight_defend.rs:378-514`, via
   `borg_defend`). It drinks when `p1 > p2`, `p2 <= avoidance / 3` and `p1 > avoidance / 7`.
   `p1` is the danger here and `p2` the danger with the Borg assumed fast
   (`defend_speed_divisor = 3`, `defend_speed_min_danger_divisor = 7`,
   `borg-core/src/params.rs:1127-1128`; with a rod, staff, spell or activation of speed `/2` and
   `/5`). `avoidance` is the current HP (`borg-core/src/borg_update.rs:1941`). **It is only
   called when the Borg is not fleeing** (`borg_caution.rs:2594-2626`: `if !st.borg.goal.fleeing { ... borg_heal ... borg_defend ... }`;
   fleeing, only `borg_heal`). The first cave spider sets
   the fleeing goal at 64,384 ("Fleeing (Scary guy on level)"), and the trace shows `fleeing:
   True` at every think to the end. Had it been called, it would still have refused. Fast, the
   Borg's own danger is 17-19 at HP 38-39 (counterfactual `speed-64414`: "Danger:p=19" at
   64,419, against 30 unhasted at 64,414), above HP/3 = 13. After the haste it is 42-47
   (counterfactual `speed-64434`).
2. **`borg_fight_speed`** (#469, `borg-core/src/borg_fight_attack.rs:5514-5552`), inside
   `borg_attack` once it has picked an attack. It drinks when the danger of the monsters that
   can move exceeds `avoidance × attack_speed_fight_danger_tenths / 10` = 3 × HP
   (`harness/borg.txt:528`). It was reached at 64,384 and 64,394, through the Phase rule's
   `borg_attack` (`borg-core/src/borg_escape.rs:1179`): danger about 21 against 117. Later
   turns never reach `borg_attack`. The Desperate stair walk and the strategic retreat
   come first. The fast-fragile attack calls `perform_focused_attack` directly
   (`borg_fight_attack.rs:5466-5482`) and skips the speed check.
3. **`cornered_boost`** (#504, `borg-core/src/borg_caution.rs:4774-4815`, Speed first). It runs
   when `fight_cornered` holds, and that needs no Phase Door in the pack (`BI_APHASE <= 0`,
   `borg_caution.rs:4666-4679`). The rogue carried 14. The Phase rule's boost
   (`borg_escape.rs:1186`) runs only when `borg_attack` finds no attack, and the rogue had one.

The "last resort" Speed of the closed #452 (`borg_speed_last_resort`) is not in this build.
Nothing in the core drinks Speed because the monsters in contact are faster than the Borg.

## Q2. Does the fast-fragile policy pre-empt the boost?

The order in `borg_think_dungeon` (`borg-core/src/borg_think_dungeon.rs`):

1. `fight_before_flight` (`:734-744`) = `attack_on_sight || winning_fight`
   (`borg_caution.rs:2416-2418`), before the out-of-light wait and before `borg_caution`;
2. `borg_caution` (`:796`). Inside it, while fleeing: `borg_heal` (the ban applies), the Desperate stair
   walks (`borg_caution.rs:2859-2868`), the cornered boost (`:2889`), the strategic retreat
   (`:2897-2914`), then `borg_escape` with Phase Door (`:2920`);
3. `borg_attack` with its `borg_fight_speed` (`:889`), never reached while caution acts.

The fast-fragile branch of `attack_on_sight` (`borg_fight_attack.rs:5466-5482`) runs these
steps: `classify`; `category_attack_safe_with(.., false)`, which drops the
target's own damage gate and keeps only "other danger ≤ 2 × HP"; `escape_instead`, Phase or
stairs only when the summed bites of marked monsters within 2 grids reach the HP; then the
attack. It has no boost. When it attacks, it takes the turn before any caution, so neither
Speed nor the emergency Phase Door is considered.

**`stats-ban` blocks only healing.** `heal_banned` is checked in `borg_heal_outmatched` and
`borg_heal` (`borg_caution.rs:239`, `508`). It never touches Speed. In this game no speed rule
could fire anyway (Q1).

**The control meets the same spiders.** The two arms send identical keys up to key 9,262
(turn 64,454): the same four spiders, the same HP 18, the same danger 55. At key 9,263 the
stats-ban arm sends `+7`, the attack. The control instead reads Phase Door ("Phase rule (from
escape 1 emergency): enemy adjacent and the fight looks lost (danger 55, HP 18)"), lands at
(7,123), quaffs Cure Light Wounds at danger 5, kills a spider, and reads Phase Door again. Its
HP falls to 19 at 64,592. It cures at a distance and reaches the cap. In the stats-ban arm, the
attack at 64,454 killed one spider but left the rogue in contact at HP 7. At 64,462 the cure
was banned. The ban did not decide the game (Q6: lifted, the same keys), but the one-grid
retreat that took the turn did. It comes before both the Phase Door and the outmatched
cure.

## Q3. A group of cave spiders as fast-fragile

`fast_fragile_group_max = 2` counts **others of the race in view** (`viewed`: `BORG_VIEW`,
`borg_fast_fragile.rs:97-102`). Three spiders in contact read "2 others in view", so they pass. The
unit test `the_cave_spider_swarm_is_not_fast_fragile_in_the_open` covers 8 in view, not 3.
`FRIENDS 100:2d8:Same` (monster.txt:1130) says more are coming: four were known at 64,444.
Each spider alone does 4.8-5.0 a Borg turn (25-28% of HP 18, the marking threshold 25%). Three
together do 13.1, against a kill rate of 10.4 HP a turn on 8-9 HP spiders: 3 turns to kill
them all (the Borg's own fight race). The premise of the policy (fragile, dies in one or two
of our attacks, so attack and do not heal) holds for one crow. It does not hold for three
hasted spiders.

The ban held with three in contact, though in this game it changed no key (Q6). `heal_banned` marks the case through any one adjacent
monster's `classify`. It never compares the cure with the summed incoming damage. Cure Light
Wounds heals 20 (`object.txt:3165-3166`), more than the 13.1 a turn three hasted spiders do.
Candidates, all hypotheses for the zoo: count a race with `friends` by its expected group, or
by the marked monsters in contact, not by those in view; and lift the ban when two or more
marked attackers are in contact, or when the summed incoming damage exceeds the kill rate.

## Q4. "Assuming player ghost (3 cave spiders)"

Confirmed as a message-parsing error. The engine groups the haste message for three monsters
as "3 cave spiders start moving faster." (`src/mon-msg.c:333-345`). The Borg's monster-message
table lists "start[s] moving faster." among the pain suffixes
(`borg-core/src/borg_messages.rs:214`), hence the "PAIN:3 cave spiders" tag
(`borg_messages.rs:1228-1231`). `borg_locate_kill` → `guess_race_name`
(`borg-core/src/borg_flow_kill.rs:1314-1320`) accepts only names starting with "The " or "the ".
Any other name is taken as the player ghost, race `r_max - 1`. In 4.2 there are no player ghosts, and that index is the
last entry of monster.txt, **Morgoth, Lord of Darkness** (`src/mon-init.c:1792-1810`,
`lib/gamedata/monster.txt:14762`).

What it did here: it raised `race_count` for Morgoth (`borg_flow_kill.rs:1420`) and found no
object or monster with Morgoth's glyph near the spot, so no kill was converted or created (no
"Converting" note). The message stayed unused. **The monster list and the danger did not
change.** The Borg still saw the haste through its own speed reading ("speed +22" at 64,454).
The error matters elsewhere. Every grouped monster message is lost the same way: the control
logs "4 cave spiders look even faster!" and "3 cave spiders start moving faster." at 64,478,
and six more "Assuming player ghost" notes. A grouped message that should locate monsters,
mark them afraid or record a death does nothing. Near a known 'P' monster of Morgoth's colour, the
"similar monster" pass of `borg_locate_kill` (`borg_flow_kill.rs:1525-1610`) could convert it
into Morgoth.

## Q5. The stair walk

At 64,414 the stairs were 19 steps away. The spiders had twice the rogue's speed (+10 to +12
against +0), and after 64,433 three times (+20 to +22). Each step gives every adjacent spider
about one bite: it spends one move following and one biting. Three spiders at the
Borg's own 4.4-5 a turn each is about 13 a step. The walk lost 16 HP in two steps (64,434 →
64,444) and reached cost 17 of 19. **It was not reasonable** at danger 30 with fast monsters
waking around. The walk was allowed because #747's refusal tests one neighbour at a time (each
under 50% of HP), not their sum. Issue [#849](https://github.com/diegoami/borg-reborn-rs/issues/849)
already asks to refuse it from a fast-fragile monster.

Speed first changes the walk. With the rogue level with the unhasted spiders, they cannot bite
and keep up. Quaffed at 64,414 (danger 30), the rogue walks the 19 steps, is bitten twice
(lowest HP 38) and takes the up-stairs at 64,525. Phase Door first: see the table. Phase
Door alone moves the rogue up to 10 grids among awake spiders twice its speed. The control's
Phase Doors worked because cures followed at a distance.

## Q6. Counterfactuals on the exact game

Method: a build of `7f8c6b80` with `cf-hook.patch` (local only, never committed to
borg-reborn-rs). With `BORG_CF=T:action`, at the first dungeon think at or after game turn
T, after `borg_notice`, the Borg drinks or reads the named item through its own
`borg_quaff_potion` / `borg_read_scroll`, and then plays on. With `BORG_CF_UNBAN=T`,
`heal_banned` is false from turn T on. Nothing else changes. With neither set, this build
plays the zoo game key for key (keys.log `1ef12466…`). Each row is the game from birth, played
under the shared lock (`cf-batch.sh`, summarized by `cfsum.py`). "Fight ends" is the first
level change or death after 64,380. "Lowest HP" is the lowest `# Loc:` HP until then.

| run | at the first think ≥ | HP then | outcome | fight ends | lowest HP from then | cures / Phase Door in the fight | at 100,000 |
|---|---|---:|---|---|---:|---|---|
| zoo game (no change) | | | **dies** 64,483 | death | -3 | 0 / 0 | |
| control arm (`borg-ctl.txt`) | (Phase Door at 64,454) | 18 | lives | up-stairs 65,342 | 18 | 3 / 7 | CL6 |
| `speed-64384` | 64,384 Speed | 39 | lives | up-stairs 64,499 | 39 | 0 / 0 | CL7 |
| `speed-64394` | 64,394 Speed | 39 | lives | up-stairs 64,499 | 39 | 0 / 0 | CL6 |
| `speed-64404` | 64,404 Speed | 39 | lives | up-stairs 64,509 | 39 | 0 / 0 | CL7 |
| `speed-64414` | 64,414 Speed | 39 | lives | up-stairs 64,525 | 38 | 0 / 0 | CL6 |
| `speed-64424` | 64,424 Speed | 38 | lives | up-stairs 64,530 | 31 | 0 / 0 | CL7 |
| `speed-64434` | 64,434 Speed (just after the haste) | 32 | lives | up-stairs 64,529 | 19 | 1 / 0 | CL6 |
| `speed-64444` | 64,444 Speed | 23 | lives | up-stairs 64,539 | 21 | 2 / 0 | CL6 |
| `speed-64454` | 64,454 Speed (instead of the attack) | 18 | lives | up-stairs 64,539 | 13 | 1 / 0 | CL6 |
| `speed-64462` | 64,462 Speed | 7 | **dies** 64,466 | death | | 0 / 0 | |
| `speed-64472` | 64,472 Speed | 6 | **dies** 64,483 | death | 1 | 0 / 0 | |
| `speed-64479` | 64,479 Speed | 6 | lives | up-stairs 64,561 | 6 | 1 / 0 | CL6 |
| `clw-64462` | 64,462 Cure Light Wounds (forced) | 7 | lives | up-stairs 64,650 | 4 | 2 / 0 | CL6 |
| `unban-64462` | heal ban lifted from 64,462 | 7 | **dies** 64,483: same keys as the zoo game | death | | 0 / 0 | |
| `unban-64384` | heal ban lifted from 64,384 | 39 | **dies** 64,483: same keys as the zoo game | death | | 0 / 0 | |
| `phase-64414` | 64,414 Phase Door | 39 | lives | up-stairs 64,722 | 17 | 1 / 2 | CL6 |
| `phase-64444` | 64,444 Phase Door | 23 | **dies** 64,922 | death | 7 | 3 / 5 | |
| `phase-64454` | 64,454 Phase Door (instead of the attack) | 18 | lives | up-stairs 64,890 | 6 | 3 / 9 | CL7 |

(`cf-summary.tsv` holds the raw summary lines; the HP columns read the Borg's `# Loc:` and
fast-fragile notes.)

What the table says, for this game only:

- **Speed saves the rogue at every think from 64,384 to 64,454**: before the shriek, after the
  haste, and at the fork with the control. The cost falls as it is drunk earlier: no bite
  before 64,414, 38 HP at 64,414, 13 at 64,454. **The last turn speed saves it in a row is
  64,454.** At 64,462 (HP 7) and 64,472 (HP 6) it is too late. At 64,479 it lives again
  (lowest HP 6, one cure), because by then one of the two spiders left had fled in terror at
  64,472. That is luck, not a window.
- Once the rogue is fast, no spider is marked fast-fragile any more (no "# Fast-fragile" note
  after the quaff: the bites per Borg turn halve below 25% of the HP). The heal ban lifts by
  itself and the Borg cures normally (CSW at 64,459 in `speed-64454`).
- **The heal ban decided nothing here.** Lifted from 64,384 or 64,462, the Borg plays the same
  keys and dies the same way. At HP 7 and danger 53, `borg_heal`'s own tests already skip
  Cure Light Wounds (danger must be under HP + 20 = 27) and Cure Serious Wounds (under HP +
  40 = 47). The outmatched cure of #457 comes last in `borg_caution`
  (`borg_caution.rs:3095`), after the one-grid strategic retreat that took the turn. A **forced**
  Cure Light Wounds at 64,462 does save it: HP 27, then the fast-fragile attacks kill three
  spiders and it leaves at 64,650 with 4 HP at its lowest.
- Phase Door is the weaker first move: it saves at 64,414 (lowest 17) and, narrowly, at 64,454
  (lowest 6, nine Phase Doors). At 64,444 it only delays the death to 64,922. Speed is better
  at every turn where both were tried.

## Defects filed in borg-reborn-rs

- [#913](https://github.com/diegoami/borg-reborn-rs/issues/913): Speed is never drunk while fleeing from monsters faster than the Borg (Q1, Q5, Q6).
- [#914](https://github.com/diegoami/borg-reborn-rs/issues/914): the fast-fragile policy pre-empts the emergency Phase Door against a group. Three spiders pass `group_max` 2 because it counts those "in view", and the heal ban holds with three in contact (Q2, Q3).
- [#915](https://github.com/diegoami/borg-reborn-rs/issues/915): grouped monster messages are parsed as the player ghost, i.e. Morgoth's race (Q4).
- [#916](https://github.com/diegoami/borg-reborn-rs/issues/916): the one-grid strategic retreat from faster monsters comes before Phase Door and the outmatched cure (64,444 and 64,462).
- [#941](https://github.com/diegoami/borg-reborn-rs/issues/941): "You feel yourself slow down." is parsed as monster pain, so the Borg believes it is hasted for the rest of the game (see the correction above). The root cause of Q1.
- The stair walk from faster monsters (Q5) is already [#849](https://github.com/diegoami/borg-reborn-rs/issues/849); this case is evidence for it.
- Observation only, not filed: at 64,394 the last Flask of oil was thrown at the remembered square of the spider killed at 64,384.

All thresholds above are hypotheses (borg-reborn-rs RULES 14). The track is the owner's choice.

## Files

- `runcell.sh`: plays the cell from birth as the zoo does (GAME_ROOT = the build).
- `borg-stats-ban.txt`, `borg-ctl.txt`: the two arms' borg.txt, as the zoo wrote them.
- `cf-hook.patch`: the local counterfactual hook (against `7f8c6b80`).
- `cf-batch.sh`, `cfsum.py`: the counterfactual matrix and its summary.
