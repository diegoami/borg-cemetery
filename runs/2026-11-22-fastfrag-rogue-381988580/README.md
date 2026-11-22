# Dunadan Rogue 381988580: two hasted soldiers, a walk to the stairs, borg-reborn-rs 7f8c6b80

- **Dossier:** [D-d97a18672a49](../../deaths/D-d97a18672a492587c9acbfede7f83106d2dbf6bca390faa93200127d89e4f46d/README.md). It is imported by #109 (`runs/2026-11-22-fastfrag-stats-ban`), so the link works once #109 is merged.
- **Source:** borg-zoo run [44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466), experiment `reborn-fast-fragile-big` (borg-zoo#596), specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`, suite `classes-1800-big`, arm `reborn-fastfrag-stats-ban`.
- **Character:** Dunadan Rogue, race 8, class 6, seed 381988580.
- **Outcome:** killed by a soldier at game turn 62,965, CL4, DL2, after 8,497 keys.
- **One life, not two samples:** the `reborn-fastfrag-ctl` arm plays the same key stream. The fast-fragile policy is not involved: at HP 23–28 the soldier is not "fast-fragile by stats" (`fast_fragile_kill_turns` 2 × 9.8 HP per turn = 19.6 HP, see the CLW branch below). So the heal ban never applied.
- **Engine:** upstream Angband `574b618c`. Every game rule below cites `engine/angband` at that commit (borg-reborn-rs RULES 16).

## Reproduction (verified)

The zoo artifact host was not reachable from this session. Instead, the game was rebuilt from birth and replayed.

- **Build:** borg-reborn-rs `7f8c6b80`, source sha256 `4ef15001…` (equal to the dossier's), rustc 1.100.0, built at the zoo's path.
- **Binary:** the bytes differ from the zoo's (`6098359c…`) because of the build environment. The game streams do not differ.
- **How it ran:** through borg-zoo's own adapter (`zoo.borgrs.build` and `run_cell` with logs kept; [probe/zoo_cell.py](probe/zoo_cell.py)). It wrote the same `borg.txt` (sha256 `a98d1bb5…`).
- **Result:** every stream equals the dossier's recorded hash:

| stream | sha256 | equals the dossier |
|---|---|---|
| keys.log | `1e1abd52b9dda3b2d92f26dc9817e06b6f697f8ae0bd676ccaa7f4f5e9fae3ff` | yes |
| messages.log | `2ee52cfa54c96ab36cb92d313a73f78a2cdc122e258c07692ddb3b20a92ccad4` | yes |
| state.log | `e45b6541aae77ea4c86376276a51bfa49225eca492df2712f545b362f50c4046` | yes |

These three logs and the run's `user/borg.txt` and `scary_monsters.txt` are retained in [replay/](replay/), because the zoo artifact expires after 90 days.

The engine-state evidence below comes from a **probe build**: 7f8c6b80 plus [probe/probe.patch](probe/probe.patch), a scratch change to the headless frontend and to the key-log hook. It does three things, all read-only for the game:

- dumps the monsters near the player at each key, with speed, haste timer, energy, visibility and view;
- dumps the screen, the inventory and the Black Market/Alchemist stock on arrival in town;
- optionally injects keys at a given key count.

Without injection the probe replays the same three hashes, so it does not change the game. The probe is not proposed for borg-reborn-rs.

## The chase, turn by turn

- **Positions** are engine (x, y). The Borg's own notes print (y, x).
- **Soldiers:** m26 is the soldier that kills the rogue (28 HP); m27 is a second soldier (22 HP). Both have base speed 109 (`monster.txt:844-847` says speed 110, randomised at birth by `mon-make.c:1158-1164`).
- **`fast`** is the monster's `MON_TMD_FAST` timer. A hasted monster gets +10 speed (`mon-move.c:1929-1931`), so 119.
- **Data:** [evidence/monsters-62830-62965.txt](evidence/monsters-62830-62965.txt) and [evidence/screens.txt](evidence/screens.txt) hold the probe's data. The Borg's lines come from `messages.log` and its decision trace (`trace-core.jsonl`).

| key | turn | rogue | HP | m26 soldier | m27 soldier | what the Borg did and why |
|---:|---:|---|---:|---|---|---|
| 8463 | 62,837 | (55,40) | 35 | (62,41), not visible, **fast 25** | (62,42), not visible, fast 25 | The shrieker at (54,47) shrieks. The messages name only the visible mouse and small kobold "(offscreen)" (Q1). |
| 8466 | 62,841 | (55,40) | 35 | (61,41), fast 24 | (61,42) | "Fearing region (40,55) … non-LOS shrieker", danger 14. "Fleeing and leaving the level (Looking for any stair)": flows to the up stairs, cost 17. |
| 8470 | 62,867 | (55,37) | 35 | (56,42), **fast 44** | (57,42), fast 44 | Second shriek: "The small kobold looks even faster!" The soldiers are hasted again, still unseen. |
| 8471 | 62,871 | (55,37) | 35 | (56,41) | (56,42) | Small kobold seen: "Scary guy on level" (`scary_monsters.txt:53`, small kobold scary to CL5–8). "Desperate for Stairs (three)", key `7`. |
| 8473 | 62,881 | (54,36) | 35 | (55,39), 3 away, not visible | (56,41) | Fight race "1 attackers … winning" on the kobold: `fight_before_flight` attacks (`+3`). |
| 8477 | 62,889 | (54,36) | 31 | (55,38), 2 away, not visible | (55,39) | Kills the small kobold. |
| 8480 | 62,892 | (54,36) | 31 | **(55,37), adjacent, 28/28, visible, fast 39** | (55,38), 2 away, **not visible** | The soldier steps into the kobold's square. Fight race "3.000 turns to kill, 9.502 damage/turn, HP 31: winning". Attacks with the Dagger (`+3`): one hit for 5, one miss. Danger 41. |
| 8483 | 62,899 | (54,36) | 23 | (55,37), 23/28, fast 38 | (55,38), not visible | It took two hits (8 HP). Fight race "not winning". `borg_caution`: "Scary guy on level", "Fleeing and leaving the level (scaryguy)", "Desperate for Stairs (three)", up stairs at cost 13. Walks west (`4`). Danger 41. No CLW (Q2). |
| 8485 | 62,909 | (53,36) | 17 | (54,36), 24/28, fast 36 | (55,36), now visible | One soldier turn moved, the next one attacked: miss, hit. Same walk, cost 12. Danger 49. |
| 8487 | 62,919 | (52,36) | 10 | (53,36), fast 34 | (54,36) | Miss, hit. Same walk, cost 11. Danger 45. |
| 8489 | 62,929 | (51,36) | 7 | (52,36), fast 32 | (53,36) | Hit, hit. Same walk, cost 10. |
| 8491 | 62,939 | (50,36) | 2 | (51,36), fast 30 | (52,36) | Miss, hit. Same walk, cost 9. |
| 8493 | 62,949 | (49,36) | 2 | (50,36), fast 28 | (51,36) | Miss, miss. Same walk, cost 8. |
| 8495 | 62,959 | (48,36) | 3 | (49,36), fast 27 | (50,36) | Same walk, cost 7. |
| 8496 | 62,965 | (47,36) | −3 | (48,36), fast 25 | (49,36) | "The soldier hits you. You die." The `<` is at (41,36), 6 squares on. |

On the screen at 62,892 ([evidence/screens.txt](evidence/screens.txt), K8479), the rogue stands where a 1-wide east-west corridor meets the corridor the soldiers come up. The `<` is in plain view 13 squares west, so only one soldier can reach the rogue at a time.

From 62,899 to 62,959 the Borg ran the same rule every turn: `borg_caution` → "Desperate for Stairs (three)" → one step west. It read no scroll and drank no potion. At death it carried 21 Cure Light Wounds (`c`) and 14 Phase Door (`e`).

## 1. Was the soldier hasted?

**Yes. Both soldiers were hasted, twice, while out of the rogue's sight, and the game could not have announced it.**

**What the shriek does.**
- `SHRIEK` is `effect:WAKE` then `effect:PROJECT_LOS:MON_SPEED` with `dice:25` (`monster_spell.txt:139-148`).
- `effect_handler_PROJECT_LOS` hastes every monster in line of sight **of the shrieker**, not of the player (`effect-handler-attack.c:1088-1116`: `los(cave, origin, mon->grid)`).
- `MON_SPEED` sets the timer to the damage, 25 (`project-mon.c:943-947`), applied through `mon_inc_timed` (`project-mon.c:1256-1260`).
- `WAKE` wakes sleepers within twice the sight range of the shrieker (`effect-handler-general.c:2223-2251`). That is "You hear a sudden stirring in the distance!".

**Why no message.**
- `mon_inc_timed` prints "starts moving faster" only when `monster_is_obvious(mon)` (`mon-timed.c:209-216`), that is visible and not camouflaged (`mon-predicate.c:307-310`).
- " (offscreen)" is added for a *visible* monster outside the map panel (`mon-msg.c:171-172, 352-353`). That is the mouse and the small kobold.
- The soldiers were not visible (probe: `vis0 view0` at K8463, K8470), so the haste of an unseen monster gives no message at all.

**Monster recall.** Recall (lore) says nothing about a temporary haste. Only the look/target description adds ", hasted" (`target.c:94`), and only for a monster in view.

**Moves per rogue turn.**
- Energy per game turn is `extract_energy[speed]` (`game-world.c:136-139`; table at `game-world.c:80-81`): speed 110 gets 10, speed 109 gets 9, speed 119 gets 19.
- So the hasted soldier gets **1.9 turns per rogue turn**, against 0.9 at its base speed.
- The chase shows exactly that. Every rogue step west, the soldier spends one turn closing the gap and the next attacking (two `HIT:HURT:1d7` blows, `monster.txt:856-857`). It attacked after 6 of the 7 steps (all but 62,949 → 62,959).
- An unhasted soldier (0.9 turns per rogue turn) could only have followed.
- The haste lasted the whole fight: the timer drops by 1 per monster turn (`mon-move.c:1800-1801`), from 44 at 62,867 to 25 at the death.

## 2. Why no Phase Door and no Cure Light Wounds from HP 23 to 2

**The order of the think.**
- `fight_before_flight` (`borg_think_dungeon.rs:735-744`) runs first. At 62,892 its fight race said "winning", so the Borg attacked.
- From 62,899 the race said "not winning", and `borg_caution` (`borg_think_dungeon.rs:797`) decided. Inside `borg_caution`, in order:
  1. **Scary guy.** `st.borg.mon.scary` is set by the named list: the soldier is `soldier | 8-11` (`scary_monsters.txt:56`), and the rogue is CL4. That starts leaving and fleeing (`borg_caution.rs:2491-2508`).
  2. **The healing rule** runs while fleeing (`borg_caution.rs:2630-2639`, `borg_heal`).
  3. **`choose_stairs`** sets `stair_less` and notes "Fleeing and leaving the level. (scaryguy)" (`borg_caution.rs:4979-4984`).
  4. **"Flee on foot"**: `desperate_for_stairs` (`borg_caution.rs:2860-2868`). Its branch (three) applies when the up stairs are within `caution_desperate_scary_distance − 1` = 19, the level is scary and CL < 20 (`borg_caution.rs:1063-1102`). It flowed toward the stairs and **returned true every turn**.
  5. `retreat`, **`borg_escape` (Phase Door, `borg_caution.rs:2920`)**, the Phase rule (#584), back-away, and at the very end **#457's outmatched heal** (`borg_caution.rs:3095`). None of these were reached.

**Why the walk went ahead: the faster-neighbour test (#747).**
- Branch (three) must not walk when an adjacent monster is faster than the Borg (`borg_caution.rs:1066-1092`). The test is `kills[kill].speed > BI_SPEED`.
- `kills[].speed` is `m.mspeed` (`borg_flow_kill.rs:461, 504`). That is the monster's base speed, **without** the +10 of `MON_TMD_FAST`.
- So the test compared 109 with the rogue's 110 and found the soldier slower. With the haste it is 119 > 110, and `fast_neighbour_counts` would hold: its danger 41 is above 50% of HP 23 (`caution_desperate_fast_danger_percent` 50). The walk would have been refused.
- The core already reads the haste: `kill.observed_fast` (`borg_flow_kill.rs:360`), used by `forecast_monster_speed` (`borg_caution.rs:2183-2185`) in the fight race and the Recall forecast. It is not used here.

**Phase Door was never asked.** `borg_escape` sits after the walk, and the walk acted. No "Phase rule" or "Considering Phase" note appears from 62,899 on.

**Cure Light Wounds.** `borg_heal` (`borg_caution.rs:261-567`) uses CLW estimated at 20 HP (`caution_clw_estimate_min` 20; the potion heals 20, `object.txt:3165-3166`). CLW needs all of these:
- `pct_down ≥ 30`;
- `pct_down ≤ 40`, or CL < 10;
- `danger < HP + 20`;
- `20 > danger / 3`.

Before that test, a random skip by wound band (`borg_caution.rs:513-554`) can refuse the heal. Turn by turn:

| turn | HP | % down | danger | band skip | CLW test |
|---:|---:|---:|---:|---|---|
| 62,899 | 23 | 34 | 41 | band 3 skips when chance < 80. chance = randint0(100) − 25 (non-priest). No +75 "lethal" bonus, because that needs danger < **max** HP (41 ≥ 35, `borg_caution.rs:521`). Chance ≤ 74, so **the skip is certain**. | would pass: 41 < 43 and 20 > 13 |
| 62,909 | 17 | 51 | 49 | band 4: skips when randint0 < 75 | fails: 49 ≥ 37 |
| 62,919 | 10 | 71 | 45 | band 5: skips when randint0 < 50 | fails: 45 ≥ 30 |
| 62,929 | 7 | 80 | 45 | band 6: skips when randint0 < 26 | fails: 45 ≥ 27 |
| 62,939–62,959 | 2–3 | 91–94 | 45 | band 6 | fails |

So the one turn where the CLW rule would have healed, its random skip could not let it through. From then on, the "covers the danger" test refused because the danger was above HP + 20. #457's outmatched heal (`caution_heal_when_outmatched` 1) is the remedy for that lockout, but it lies behind the walk.

**Did the danger count the soldier's real speed? No.**
- `borg_danger` takes `monster_speed = kill.speed` (`borg_danger.rs:2097`). Its moves are `extract_energy` of that speed against the player's (`borg_danger.rs:2161-2171`).
- With 109 against 110 that is 0.9 moves per rogue turn, against the real 1.9. The danger numbers 41–49 count the soldier at about half its real rate of attack.
- The fight race did count the haste: 9.502 damage per turn is 2 blows × 4 average × 0.625 to-hit × 1.9 (see question 5).

## 3. Speed: could it have had a Potion of Speed?

**Shops.**
- No store lists Potions of Speed in `always:` or `normal:` (`store.txt:21-222`). The General Store sells oil (`store.txt:31`). The Alchemist sells CLW, Phase Door and Recall always (`store.txt:160-163`).
- Only the Black Market's random stock can hold one, at 75 gold (`object.txt:3429-3439`) × 2 × 150% = **225 gold** (`store.c:616-617, 646-653`).
- Stock is re-rolled from the game RNG on arrival in town (`player-util.c:149`, `store.c:1422-1435`). So the probe read the real stock at every arrival ([evidence/stores-at-town-arrivals.txt](evidence/stores-at-town-arrivals.txt)):
  - **From turn 30,299 the Black Market held 3 Potions of Speed, and from 42,058 it held 6, through the last visit at 53,466.**
  - At those visits the rogue carried 0–106 gold; from 34,845 it carried 0.

**The floor.**
- **At 36,256 a Potion of Speed lay two squares from the rogue**, on DL1 at (168,53), in view (probe: `Speed x1 [tval26 sv24] seen1`; `TV_POTION` is 26, `list-tvals.h:6,32`). The Borg logged "Creating an object 'Speed' at (168,53)".
- In the same think a small kobold came into view: asleep, 4 squares away (probe: `sleep103`). It is a named scare up to CL5–8, and the rogue was CL3.
- So: "Scary guy on level", "Fleeing (Scary guy on level)", "Desperate for Stairs (three)", at danger 0. It left the level by the up stairs and never took the potion ([evidence/speed-potion-36256.txt](evidence/speed-potion-36256.txt)).
- That is the only Speed potion the game ever showed it.

**So:** it never had a Potion of Speed, and it could not have drunk one in this fight. It had two chances to own one: the floor potion at 36,256, and the Black Market, which it could not afford on any visit.

**Other escapes it had at 62,899:**
- **14 Phase Door** (`object.txt:2571-2581`: `TELEPORT` 10).
- **21 CLW.**
- **The up stairs**, 13 squares down the corridor. At 1.9 soldier turns per step, that is about 13 attack rounds of 5.8 HP expected each. An approximate simulation with the engine's rules gives **0.2%** for reaching them from HP 23, and 1.6% from HP 31 ([evidence/race-simulation.txt](evidence/race-simulation.txt)).
- **The other scrolls** were Blessing ×2, Summon Monster and Blindness potions ×3. None of them is an escape.
- **No Word of Recall** and no Flask of oil.

## 4. Gold and oil: why no trip to town

**Oil and gold.**
- The last Flask of oil was thrown at 40,463 ("You have no more Flasks of oil").
- Gold went to 0 at 34,845, not about 38,000. It stayed 0 until 56,379, then rose to 375 by 58,408.
- Flasks cost 3 gold each (native receipts in `town-transactions.jsonl`, "12 Flasks of oil … 36 gold").

**Why no trip.**
- The last town visit was at 53,466, with 0 gold ("Nothing to sell in town (leaving)").
- After 58,408 no rule asked for town:
  - At DL2, `borg_restock` (`borg_prepared.rs:886-916`) asks only for light, fuel and food: "Assume happy at level 3". It has nothing for oil, missiles, armour or Speed.
  - `borg_prepared` for DL3 failed on "50 hp", so the rogue stayed on DL2. No rule spends a grown purse.
- `kit_restock` (#840 remedy a: a trip when the kit score is low and the purse has grown) is not in 7f8c6b80. It came with `0327fa97`, and it ships 0 on main today (`harness/borg.txt:1330`).
- This is #840's case: no ranged option, money, no trip. It is also #810's (surplus gold). No new issue is filed for it.

With 375 gold the rogue could have bought, for example, 25 flasks (75 gold) and a Speed potion (225), if the re-rolled Black Market still held one.

## 5. "Winning" at HP 31 with a 1d4 dagger

**Both rates in the race are right on average.**
- **Outgoing, 9.772 HP per turn:**
  - The probe reads skill 68, to-hit +4, to-dam +2 and 2.77 blows (`S thn68 toh4 tod2 blows277`).
  - To-hit is 68 + 3×4 = 80 against AC 24 (`player-attack.c:88-94`). That hits 0.12 + 0.83 × 64/80 = 0.784 of the time (`player-attack.c:174-219`).
  - Damage is 2.5 + 2 = 4.5 per hit. Blows are limited by energy, at most two per command (`player-attack.c:988-1020`), so 2.77 per 100 energy.
  - 2.77 × 0.784 × 4.5 = 9.77.
- **Incoming, 9.502 HP per turn:**
  - HURT has power 40 (`blow_effects.txt:21-22`). To-hit is 40 + 3×2 = 46 against AC 28, which hits 0.625 of the time.
  - 2 blows × 4 × 0.625 = 5.0 per monster turn, × 1.9 for the haste = 9.50.
  - AC damage reduction (`mon-attack.c:540-543`) is 0 for 1d7 at AC 28.

**Why it was still wrong.**
- **It is a coin flip with no margin.** The race wins when turns × incoming < HP: 3 × 9.502 = 28.5 < 31, a 2.5 HP margin on expected values (`borg_caution.rs:1932-1935, 2352`). An engine-rule simulation of this one-on-one fight from HP 31 wins 82%.
- **It counted one soldier. There were two.**
  - The race counts "every awake visible attacker" (`borg_caution.rs:2277-2300`). The second hasted soldier was 2 squares behind, in the dark corridor, not visible.
  - Soldiers come in groups (`monster.txt:861-864`, `friends:50:1d2:Same`).
  - Fighting both, one at a time at the corridor mouth, the simulation wins **1.4%** from HP 31.
  - The Borg could not see the second soldier (fair information), but the race takes no account of group members it has not seen.
- **Simulation scope:** an estimate from the engine's rules, no cures or escapes, criticals ignored ([probe/race_mc.py](probe/race_mc.py)). It is a hypothesis-level number, not a measurement (RULES 14).

## 6. Counterfactuals on the exact game

**Method.**
- One named case, under the shared lock (borg-reborn-rs RULES 17, 20).
- The probe replays the original keys from birth. When the key count reaches the think's boundary, it feeds one action instead of the Borg's. Then the unchanged Borg plays on to the 100,000-turn cap.
- The actions are `ESC ESC r e` (read Phase Door), `ESC ESC q c` (quaff CLW) and `ESC ESC + <dir>` (melee). `ESC ESC r e` is the Borg's own key sequence for Phase Door at 36,185.
- Each branch's keys equal the original up to the injection.
- Each is **one branch of one life**: the injected action moves the game RNG, so the landing of a Phase Door is a single draw, not a probability.

**Results** ([counterfactuals/results.json](counterfactuals/results.json) with each branch's hashes; [counterfactuals/encounters.txt](counterfactuals/encounters.txt)):

| action at turn (HP) | 62,892 (31) | 62,899 (23) | 62,909 (17) | 62,919 (10) | 62,929 (7) | 62,939 (2) | 62,949 (2) | 62,959 (3) |
|---|---|---|---|---|---|---|---|---|
| Phase Door | **lives** | dies 63,054 | **lives** | **lives** | dies 63,055 | dies 63,075 | dies 62,987 | dies 63,233 |
| Cure Light Wounds | – | **lives** | dies 63,007 | dies 62,986 | dies 63,017 | dies 63,017 | dies 63,028 | dies 62,990 |
| melee instead of the walk | (original) | dies 62,944 | dies 63,134 | | | | | |

**What happened in each.**
- **Phase Door at 62,892** (instead of the "winning" attack): it lands out of reach and walks to a staircase, chased. HP falls to 14; it leaves the level at 63,062 and reaches the cap at CL6.
- **CLW at 62,899** (HP 23 → 31): the race says "winning" again, and it fights on.
  - Later rules act in order: the fast-fragile Phase at HP 9 (the soldier is now at 14 HP), a CLW, the Phase rule.
  - It kills a soldier at 63,100, leaves at 63,167 and reaches the cap.
- **Phase Door at 62,899:** it lands near the shrieker. The second soldier finds it, and it reads another Phase Door at 62,937. Then it walks "Desperate for Stairs (three)" again for 11 turns with a soldier behind it, HP 21 → 16 → 5 → 0, and dies at 63,054. This is the same walk as the original death, after a different landing.
- **Phase Door at 62,909 or 62,919** (HP 17, 10): it lives. It leaves the level at 63,013 and 63,215.
- **From 62,929 (HP 7)** no single Phase Door and no single CLW saves it.

**The last escape that works** in these branches is the Phase Door at **62,919, HP 10**, the third step of the walk. The last cure that works is the CLW at **62,899**, the first.

Every death after an escape in these branches comes back to the walk to the stairs, or to the fight, with a hasted soldier behind it.

## Defects (filed in borg-reborn-rs; thresholds are hypotheses, RULES 14)

- borg-reborn-rs#907: monster haste is not counted by `borg_danger` or by "Desperate for Stairs (three)"'s faster-neighbour test.
- borg-reborn-rs#908: "Desperate for Stairs (three)" keeps walking while it is hit every step, ahead of Phase Door and #457's outmatched heal.
- borg-reborn-rs#909: CLW's random band skip is certain when danger ≥ max HP (non-priest), so the one turn a CLW was allowed it could not fire.
- borg-reborn-rs#910: the fight race declares "winning" on a 2.5 HP expected margin and ignores unseen group members.
- borg-reborn-rs#911: a sleeping named scare at danger 0 makes the Borg leave a Potion of Speed two squares away.
- Gold and oil: existing borg-reborn-rs#840 (kit restock, remedy a) and #810 (surplus gold). No new issue.

## The new switches on the exact game (borg-reborn-rs#907–#911)

**Setup.**
- The code of the five task branches (`task/T907-haste-speed` … `task/T911-scary-pickup`, track P) was ported onto 7f8c6b80 in a scratch tree: [counterfactuals/switches-port-7f8c6b80.patch](counterfactuals/switches-port-7f8c6b80.patch).
- Each arm sets its switches through `BORG_PARAM_*` on the zoo cell's `borg.txt`, and plays from birth ([probe/port-arm.sh](probe/port-arm.sh)).
- With every switch at 0 the port replays the death's keys exactly (`1e1abd52…`).
- With a switch on, the game is the death's game until that rule first acts.
- One life per arm, not a measurement ([counterfactuals/switches-on-7f8c6b80.json](counterfactuals/switches-on-7f8c6b80.json)).

| arm | settings | splits from the death at | outcome |
|---|---|---|---|
| off | all 0 | – | dies 62,965 (the original) |
| 907a | `caution_desperate_fast_haste` 1 | 62,929 | lives to the 100,000-turn cap |
| 907b | `danger_observed_haste` 1 | – | dies 62,965 |
| 908 | `caution_desperate_walk_cost_percent` 100 | 62,929 | lives to the cap |
| 908+907b | both | 62,899 | lives to the cap |
| 909a | `caution_heal_lethal_over_max` 1 | 62,899 (drinks CLW) | lives to the cap |
| 909b | `caution_heal_outmatched_before_walk` 1 | 62,909 | lives to the cap |
| 910a | `caution_winning_fight_margin_percent` 20 | 62,892 (no attack) | dies 62,991 |
| 910b | `caution_winning_fight_group_percent` 100 | 62,892 | dies 62,991 |
| 910+908 | margin 20, walk cost 100 | 62,892 | lives to the cap |
| 911 | `caution_scary_take_distance` 5 | 13,982 (an earlier scare) | lives to the cap at CL7, and later drinks a Potion of Speed |
| all but 911 | every switch above except 911 | 62,892 | lives to the cap |
| all | every switch | 13,982 | lives to the cap (the same game as 911) |

**What the arms show.**
- **908 alone.** The walk is refused from 62,899 ("13 steps x 4.50 HP/step = 58.5 >= 100% of HP 23 (#908)"). But "Strategic retreat" steps away instead for three turns, because `borg_danger` prices the next grid at the soldier's base speed ("41 > 0"). The Phase Door comes at HP 7.
- **908 with 907b.** The danger is 84 at 62,899: no retreat, a Phase Door at once at HP 23, then a CLW.
- **910 alone** does not attack at 62,892. It then walks to the stairs and dies, as the original did one turn later. With 908 as well, it lives.

## The same switches on track-p (borg-reborn-rs 608d9fed)

The arms above ran on 7f8c6b80, the death's build: a main commit, 242 commits behind `track-p` on 2026-11-22. So this section repeats the check on the stack's top, `608d9fed` (`track-p` `9085c266` plus borg-reborn-rs#920–#924).

**Setup.**
- **The seeds.** The 9 deaths of #596's `reborn-fastfrag-stats-ban` arm.
- **The arms.** #596's `ctl` and `stats-ban` profiles, each with and without every new switch. That is 36 named-case games, 100,000 turns, on `classes-1800-big`'s characters.
- **How they ran.** Built and played by borg-zoo's own adapter ([probe/trackp_arms.py](probe/trackp_arms.py); the specimen pins `track-p`'s own `scary_monsters.txt`, `ff831d0a…`). Results: [counterfactuals/trackp-608d9fed-named-cases.jsonl](counterfactuals/trackp-608d9fed-named-cases.jsonl).

**Results.**
- **No deaths.** None of the 9 starts dies on `track-p`, with or without the switches. All 36 games reach the cap. On `track-p`, 381988580 is a CL7 Rogue that reached DL3, and CL6/DL4 with the switches.
- **The switches act.** Every "+all" game splits from its control. #911's take acted 263 times and #908's walk refusal 10 times. The outmatched heal (#909) never acted. #907's and #910's switches leave no note of their own.
- **Levels.** The total character level is 60 in both `ctl` arms.

These games show that the switches act on `track-p`, with no new death in 18 games. They cannot show a rescue, because nothing died. That is borg-zoo#643's measurement, which runs on `608d9fed`.

## Limits

- The zoo bundle itself was not downloaded: the artifact host is blocked here. The logs were regenerated, and their hashes equal the dossier's.
- The binary bytes differ from the zoo's (build environment); the streams match.
- The probe patch is a diagnostic only, applied to a copy of the generated engine. Without injection it replays the same hashes.
- The counterfactuals are single branches: one action and then the unchanged Borg, or one setting per arm. They show what one action does in this life, not how often it works.
- The simulations are approximate (no cures, escapes or criticals) and are hypotheses.
