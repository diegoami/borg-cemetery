# A stunned Gnome Rogue keeps "winning" against a 1-HP blue yeek (seed 390305857)

Investigation of one natural death from borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466)
(experiment `reborn-fast-fragile-big`, borg-zoo#596). The arm is `reborn-fastfrag-stats-ban`.
Specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`, borg-reborn-rs
[`7f8c6b80`](https://github.com/diegoami/borg-reborn-rs/commit/7f8c6b80a617eba3a6f2b83e4ba9d45b7b552b73),
core `borg-rs` (`borg-core/`). Dossier:
[D-85f1e458d8e9](../../deaths/D-85f1e458d8e94776e211db55dc21245ca194088014efe6f5734226c431fd9679/README.md)
(imported by borg-cemetery#109; the link resolves once that PR is merged).

**The game:** Gnome Rogue (race 4, class 6), killed by a blue yeek at game turn 78,878. CL5, DL1 (max DL2), 35 max HP, 10,095 keys. The control arm `reborn-fastfrag-ctl` plays the same key stream, and so does `main-ed52fec1 / reborn-alpha1-shipped`. The fast-fragile policy does not act here.

The engine is upstream Angband `574b618c`. Every game rule below is cited in `engine/angband/` at that commit. Every Borg rule is cited in borg-reborn-rs `borg-core/src/` at `7f8c6b80`, with the line at the track-p head `e2d8919e` where it moved.

## Reproduction

- **Build:** `7f8c6b80`, `BORG_IMPL=rust harness/build.sh`, recorder off. The local binary hash differs from the zoo's (`c1bd2467…` vs `6098359c…`, a different rustc). The play hash is what has to match.
- **Replay:** from birth, the bundle's own `user/` (`borg.txt` sha256 `677bfaea…` and `scary_monsters.txt` `9766d882…`, both as recorded). Command: [`probe/replay.sh`](probe/replay.sh).
- **Result:** keys.log `07c2fdcc053d6576…`, equal to the cell's `play_sha256`. messages.log `f452f55e…` and state.log `d4a323b9…` also equal the dossier's hashes. Death at 78,878 by a blue yeek.

No save was loaded at any point. Every counterfactual below is the same process replaying from birth (see *Method*).

## What happened

| game turn | event |
|---|---|
| 78,647 | Arrives on DL1 by an up staircase ("maze of up staircases", connected stairs). Goals: `rising` (walking home). |
| 78,684 | Grip, Farmer Maggot's Dog, is a scary guy. "Fleeing and leaving the level (scaryguy)". "Desperate for Stairs (four)" walks it onto the **down** staircase at (134,6). |
| 78,694–78,746 | Six thinks on the down staircase, each noting "Standing on dn-stairs" and "Fleeing and leaving the level". It fights Grip, then the blue yeek, in melee (`borg_attack`). It never presses `>`. The yeek drops to 0–1 HP. |
| 78,746 | Both monsters are out of view and forgotten. "Looking for any stair", then `borg_flow_old` (dark exploration) steps **off** the staircase, NW onto (133,5). |
| 78,756 | "The blue yeek hits you. You have been stunned." HP 33 → 28, stun timer 14. |
| 78,756–78,874 | 15 thinks, all `fight_before_flight`. The race says "1 turn to kill … winning" every time. 30 blows: **28 "You fail to harm the blue yeek"** and 2 misses. The yeek lands 10 more hits. |
| 78,878 | The yeek hits for 5 at HP 3. Dead, with stun timer 2: two more player turns and the stun would have worn off. |

The full turn-by-turn table is [`evidence/fight-table.md`](evidence/fight-table.md). It gives, per think: key number, game turn, position, HP, the engine's stun timer, the engine's real to_d, the Borg's `BI_TODAM` / `BI_ISSTUN`, the check that chose the action (trace `check_source`), the keys, the fight-race numbers and the game messages. The stun-phase rows:

| think | turn | HP | stun | engine to_d | Borg BI_TODAM / ISSTUN | check | race | result |
|---:|---:|---:|---:|---:|---|---|---|---|
| 7791 | 78,756 | 28 | 14 | −4 | 1 / 1 | fight_before_flight | winning, 1 turn, in 1.785, needs 1, out 1.918 | 2× fail to harm |
| 7792 | 78,765 | 28 | 13 | −4 | 1 / 1 | fight_before_flight | winning, same | 2× fail to harm |
| 7794 | 78,781 | 24 | 11 | −4 | 1 / 1 | fight_before_flight | winning, same | 2× fail to harm, hit |
| 7797 | 78,807 | 16 | 9 | −4 | 1 / 1 | fight_before_flight | winning, needs 2, out 3.838 | miss, fail to harm, hit |
| 7799 | 78,823 | 11 | 7 | −4 | 1 / 1 | fight_before_flight | winning | 2× fail to harm |
| 7801 | 78,840 | 9 | 6 | −4 | 1 / 1 | fight_before_flight | winning | 2× fail to harm, hit |
| 7802 | 78,849 | 5 | 5 | −4 | 1 / 1 | fight_before_flight | winning | miss, fail to harm, hit |
| 7805 | 78,874 | 3 | 2 | −4 | 1 / 1 | fight_before_flight | winning | 2× fail to harm, hit, **dies** |

The engine to_d / `BI_TODAM` columns come from a read-only probe in the scratch build, on a run whose keys are identical to the zoo's (see *Method*).

## 1. Why the stunned Dagger does no damage

**The stun penalty.** STUN has grades `Stun` up to 50, `Heavy Stun` up to 150, then `Knocked Out` (`lib/gamedata/player_timed.txt:278-286`).
- Stun: to_h −5, to_d −5 (`src/player-calcs.c:2144-2150`).
- Heavy Stun: to_h −20, to_d −20 (`:2137-2143`).
- Knocked Out: the player gets no turn (`src/game-world.c:895-897`).

The timer falls by `adj_con_fix[CON] + 1` per player turn (`src/game-world.c:282, 318-321`): 14 at 78,756, 2 at death, worn off at 78,890 in the runs that live. A stunned player gets no HP regeneration either (`src/player-util.c:469`).

**The blow that stunned.** A blue yeek has one blow, `HIT:HURT:1d5` (`lib/gamedata/monster.txt:1045-1057`), and the HIT method can stun (`blow_methods.txt:14-21`). The 5-damage hit at 78,756 was a perfect roll. `monster_critical` gives a sub-20 blow a `dam`% chance (`src/mon-attack.c:495-520`), and a cut/stun conflict is a coin flip (`:660-668`). It returned 2, so the stun was 11–20 (`:694-716`); here 14.

**The damage floor.**
1. `melee_damage` = 1d4 + the weapon's to_d, which is 0 (`src/player-attack.c:480-493`, called at `:804`).
2. `critical_melee` (`:807`) can add damage.
3. The player's to_d is added (`:827`).
4. `dmg <= 0` becomes 0, verb "fail to harm" (`:840-845`).

Read from the engine by the probe: before the stun, to_h +3 and to_d +1 (STR index 13, `adj_str_td` +1, `player-calcs.c:272-312, 2234`). Stunned: to_h −2 and to_d −4.

- **A normal blow:** 1d4 − 4 is −3 to 0, so it is always 0, "fail to harm".
- **A critical blow:** would be 2·d + 5 − 4 ≥ 3 (`constants.txt:261`). The crit chance is weight 12 + 5 × to_h + skill 49 − 60 (`player-attack.c:399-433`; `constants.txt:219-242`; Dagger weight `object.txt:701-709`). Stunned, that is 12 − 10 + 49 − 60 = **−9**, so no crit is possible.

**Every blow while stunned did exactly 0.** The 2 non-"fail to harm" blows were misses. The hit chance is to-hit 49 + 3 × (−2) = 43 against AC 16, giving **75.7 %** (`player-attack.c:88-94, 181-219`).

**Do Cure Light / Serious Wounds cure the stun? No.**
- CLW: `HEAL_HP` 20, `CURE:BLIND`, `TIMED_DEC:CUT`, `TIMED_DEC:CONFUSED` (`object.txt:3156-3173`).
- CSW: `HEAL_HP` 40, `CURE:BLIND/CUT/CONFUSED` (`object.txt:3175-3190`).
- The first potion with `CURE:STUN` is Cure Critical Wounds (`object.txt:3192-3209`), and the rogue carried none.
- HEAL_HP heals the larger of a percentage of the missing HP and the base (`effect-handler-attack.c:201-230`). At 28/35 either potion just tops the rogue up to 35.

## 2. Does the Borg know it is stunned?

**Yes, as a status:** `BI_ISSTUN` is set for a stun timer of 1–50 and `BI_ISHEAVYSTUN` above 50 (`borg_trait.rs:2852-2858`). The probe shows `BI_ISSTUN = 1` from 78,756.

**No, in its combat numbers:**
- `BI_TODAM` and `BI_TOHIT` are built only from equipment and the STR/DEX tables (`borg_trait.rs:1275-1276, 1374-1376`), with no stun term. They stay +1 / +3 throughout.
- The melee estimate `thrust_damage_with` adds `BI_TODAM` (`borg_fight_attack.rs:535`; track-p `:636`). Its hit chance uses `BI_THN + 3·(BI_TOHIT + to_h)` (`:542`).
- The fight race `winning_fight` gives up on confusion, blindness, hallucination, cuts and poison, but **not stun** (`borg_caution.rs:2282`; track-p `:2715`).
- The danger does use stun, but only to fear sound and force breath more (`borg_danger.rs:1031-1036` and siblings).

**Where 1.918 and 3.838 HP/turn come from.** `focused_blow_expectation` = min(blow damage, needed HP ÷ blows) × hit chance (`borg_fight_attack.rs:5270-5272`, track-p `:5414`). It is multiplied by the engine's `num_blows` 238 (`engine.rs:1408-1411`).
- Blow damage: 1d4 average 2.5 + `BI_TODAM` 1 = 3.5.
- Hit chance: `hit_permyriad(49 + 3·3, 16)` = 0.8068 (`:5117-5121`). The engine's stunned chance is 0.757.
- "Needs N HP" is the health-bar HP + 1 (`observed_kill_hp`, `:5132-5134`). The yeek showed 0, then 1.
- Needs 1: min(3.5, 1) × 0.8068 × 2.38 = **1.918**. Needs 2: min(3.5, 2) × 0.8068 × 2.38 = **3.838**.
- The real expectation while stunned is **0**.

**Why 28 harmless hits never changed it.** "You fail to harm …" is not parsed: `borg_messages.rs` reacts to "You hit " (`:764`) and "You miss " (`:793`) only. The trace shows no `HIT:`/`MISS:` reaction after any "fail to harm" line. Nothing feeds the blows' real result back. The estimate is recomputed every think from the same unstunned `BI_TODAM` and the same health bar.

## 3. Why it never cured the stun

- **Cures in the Borg:** `borg_recover` has the stun cures (`borg_recover.rs:268-299`, `:411-430`): activations or spells (cheap rung), or a Staff of Curing, Rod of Curing/Healing or CCW via `borg_quaff_crit` (costly rung). CLW and CSW are absent, which is **correct for this engine** (§1). The rogue had none of the listed items.
- **It was never reached anyway:** `borg_recover` runs at `borg_think_dungeon.rs:843/946`, after `fight_before_flight` (`:735-745`) has already returned. The same holds for `borg_caution` (`:797`), which holds `borg_heal` and the escapes.
- **Waiting would have worked:** the stun was 2 player turns from ending on its own. Stepping away, or simply not attacking, cures it.

## 4. Why it did not take the down staircase

On 78,694–78,746 `borg_caution` ran. It noted "Standing on dn-stairs" (`note_standing`, `borg_caution.rs:888-924`) and "Fleeing and leaving the level (scaryguy)" (`choose_stairs`, `:4978`). It then took neither staircase, then `borg_attack` (`borg_think_dungeon.rs:890`) chose the blow.

`choose_stairs` sets `stair_less` (there is no up staircase here) and sets `stair_more` because the Borg is fleeing and the guy is scary. Then `rising_holds_descent` (#483, `borg_caution.rs:4878-4884`; track-p `:5327`) clears `stair_more`, because all four of its conditions hold:
1. `goal.rising` is set.
2. The depth is > 0.
3. The Borg has spent fewer than `caution_rising_explore_ticks` = **500** ticks on the level (shipped).
4. The danger 4–5 is ≤ avoidance (HP 33) × `caution_rising_descend_danger_tenths` 10 / 10.

The `>` rule (`:2780-2802`) then has no `stair_more`.

#557's separate hold (`caution_rising_hold_flee_descent`) ships 0 and does not act. The #753 exception (`caution_rising_hold_min_hp_percent`) applies only to #557's hold, so #483's hold has no low-HP, scary-level or already-on-the-staircase exception.

At 78,746 "Looking for any stair" (`borg_think_dungeon.rs:1087-1098`) found no old flee flow. The dark-exploration flow (`:1327-1330`) then walked it off the staircase into the yeek.

With the race switched off from 78,756 (row I below), the same hold produces the #753 loop: "Desperate for Stairs (four)" onto the `>`, then "Standing on dn-stairs", then "Flowing toward dark-3" off it. That repeats 26 times in 550 game turns, and the Borg stays on the scary level until 83,625.

## 5. Why no Phase Door or retreat at HP 11, 9, 5

`fight_before_flight` = `attack_on_sight || winning_fight` (`borg_caution.rs:2416-2418`). It is called at `borg_think_dungeon.rs:735-745`, before the light rung, the depth return, `borg_caution` (all heals, escapes, stairs) and `borg_recover`. While it returns true, nothing else runs. So **"winning" suppresses every escape and heal.**

`wins_race` wins when turns × incoming < HP (`borg_caution.rs:1932-1935`). Here that is 1 × 1.785 < HP, true at every HP ≥ 2. The yeek's blow is up to 5 (1d5), so the race lets go only after HP is already in one-blow range. In row G, HP happened to land on exactly 0. The race said "not winning", and `borg_caution` drank a CLW at once ("Healing Level 1").

**Phase Door would not have helped.** The worn *Soft Leather Armour of Resist Lightning [8,+8] {??}* carries the unknown curse *anti-teleportation* (`NO_TELEPORT`, `curse.txt:318-330`). Every Phase Door read prints "Teleportation forbidden!" (`effect-handler-general.c:2573-2578`) and spends the turn. The Borg could not know this before the first read: the rune is learned by trying (see #829 for the repeat-read case).

## 6. Counterfactuals on the exact game

**Method.** This uses a scratch build of `7f8c6b80`, never committed. Its patch is [`probe/cf-scratch.patch`](probe/cf-scratch.patch):
- An environment-gated hook at the top of `borg_think` replaces **one** think, the first at or after `CF_TURN`, with the named action, using the Borg's own `borg_keypress` / `borg_quaff_potion` / `borg_read_scroll`.
- After that the same Borg, with its memory intact, plays on in the same process to the 100,000-turn cap. It is not a save and not a restart.
- A read-only stderr probe prints the engine's to_h/to_d/stun and the Borg's traits.

With the probe on and no action, the keys are `07c2fdcc…`, identical to the zoo's. Every variant's keys are identical to the zoo's up to the replaced think (`evidence/runs.json`, [`probe/cf-all.sh`](probe/cf-all.sh), [`probe/summ.py`](probe/summ.py)). One named case, run under `flock /tmp/angband-validation.lock`.

| | replaced think (turn, HP) | action | first different key | yeek fight | lowest HP after the action | game |
|---|---|---|---:|---|---:|---|
| — | none (zoo game) | — | — | dies at 78,878 | −2 | dies |
| A | 78,746 (HP 33, on `>`) | take the down staircase `>` | 10,037 | left behind on DL1 | 28 (Grip on DL2) | **lives** to 100,000, CL6 |
| B | 78,756 (HP 28, stun 14) | quaff CSW | 10,039 | stun ends 78,890, yeek slain 78,892 | **3** | lives, CL6 |
| C | 78,765 (HP 28, stun 13) | quaff CSW | 10,042 | stun ends 78,890, yeek slain 78,902 | **2** | lives, CL6 |
| D | 78,765 | quaff CLW | 10,042 | same as C (same game but the item letter) | **2** | lives, CL6 |
| E | 78,807 (HP 16) | read Phase Door | 10,061 | "Teleportation forbidden!", fights on | −1 | **dies** 78,878 |
| F | 78,823 (HP 11) | read Phase Door | 10,069 | "Teleportation forbidden!" | −3 | **dies** 78,878 |
| G | 78,849 (HP 5) | read Phase Door | 10,080 | "Teleportation forbidden!". HP reaches 0, race "not winning", CLW at 78,859, stun ends, yeek slain 78,894 | **0** | lives, CL6 (luck) |
| I | 78,756 | (diagnostic) the race switched off | 10,039 | stair loop (§4), yeek slain 79,043 | 23 | lives, CL6 |

**What saves it, and how well.**
- **Only the stairs save it with a margin:** HP 33, out of the fight.
- **CSW or CLW** do not cure the stun (§1). They only top HP up by 7 to 35. The rogue then survives the 12 more turns until the stun wears off by **2–3 HP**. That is a save on this roll sequence, not a robust one.
- **Phase Door saves nothing:** the armour bans teleport. G lives only because a blow left HP at exactly 0, which released the race into the ordinary heal.
- **I shows two things.** The race alone kept the rogue in the fight. Without the race, the stair hold keeps it on the level.

One start, one game: direction only (RULES 14). Nothing here is a rate.

## 7. Pattern

**Where I searched.**
- **The Cemetery:** "fail to harm" appears in only 4 retained cases: D0009 (mushroom patch), D0012 (large white snake), D0018 (fox form) and `validation/borg-reborn-rs/unseen-bump-781`. None is a stun. Most dossiers keep no message log.
- **The zoo:** its cells carry no message tails for reborn runs. Instead I downloaded the `deaths-*` bundles of the 56 most recent reborn runs with deaths (80 listed by `death-report/scripts/runs.py reborn --n 80`): **599 death bundles**.
- **The test:** "You fail to harm" or a stun message within the last 200 game turns ([`probe/pattern.py`](probe/pattern.py), hits in `evidence/pattern-hits.txt`). That gives 28 cells, 10 distinct games (seed and death turn).

**The same defect (stunned, the race says "winning", the blows do nothing), 2 games:**

| game | character | killer | stun → death | "fail to harm" | race while stunned | cells |
|---|---|---|---|---:|---|---|
| 390305857 (this case) | Gnome Rogue CL5, Dagger 1d4 | blue yeek | 78,756 → 78,878 | 28 | winning ×15 | `fast-fragile-7f8c6b80` ctl and stats-ban, `main-ed52fec1` alpha1-shipped |
| 722977062 | Human Rogue CL6, Dagger 1d4 | soldier | 43,809 → 43,929 | 16 | winning ×3 (HP 29, 24, 20), then not winning at 13, then 2 CLW, then attacks to death | `fast-fragile-7f8c6b80` stats and named (run 44936539730). **Not retained in the Cemetery.** |

**A related case, not analysed here:** Dunadan Mage 2017596150 (soldier, 10 cells of `main-ab775d48` / `f57499d0` / `throw-pb`). It was stunned at 95,839 and the race said "winning" twice with a spell attack. Stun raises spell failure rather than flooring damage, so it is not the same mechanism.

**Stunned with no "winning" race after the stun (6 games):** Blackguard 1474282934, Paladin 2123511101, Priest 1569794094, Paladin 766958386, Rogue 1496113358 and Blackguard 1981269294.

**Many harmless hits but no stun:** Druid 507571350, a Whip (1d3) against a yellow worm mass, 38 hits. That is a different cause, left for another case.

Two games in 599 bundles is a lead, not a rate (RULES 14).

## Same code at the track-p head

All four mechanisms read the same at track-p `e2d8919e` (242 commits after `7f8c6b80`):
- The race has no stun gate (`borg_caution.rs:2715`).
- `BI_TODAM` has no stun term (`borg_trait.rs:1276, 1374`).
- "fail to harm" is not parsed (`borg_messages.rs:799` handles "You miss " only).
- `fight_before_flight` is still ahead of `borg_caution` (`borg_think_dungeon.rs:763` vs `:816`).
- `rising_holds_descent` (`borg_caution.rs:5327`) ships `caution_rising_explore_ticks = 500`.

No line mentioning stun changed in those commits. Seed 390305857 on a track-p build (`harness/run.sh`, shipped settings, and with `fast_fragile_by_stats = 1`) plays a different game from key 84 (turn 411). It meets no stun and lives to the cap, so it is no evidence either way.

## Issues

ISSUES_PLACEHOLDER

## Files

- `evidence/fight-table.md`: the fight think by think, from the zoo bundle's own trace, messages and state logs, plus the probe columns.
- `evidence/runs.json`: keys sha256, length and outcome of the exact replay, the probe control and every counterfactual.
- `evidence/counterfactual-summary.txt`, `evidence/*.messages-78680-79050.log`: the variants' messages around the fight.
- `probe/`: `replay.sh` (exact replay from birth), `cf-all.sh`, `summ.py`, `table.py`, `pattern.py`, and `cf-scratch.patch` (scratch only, not a proposed change). Set `WORK` to a scratch directory holding the bundle as `yeek/b`.
- The raw bundle stays in the zoo artifact `deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-6` (90-day retention).
