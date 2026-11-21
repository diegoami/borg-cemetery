# Fast-fragile monsters: the 8 crow cases of 3b4924ba, replayed with the #842 switches

Local replays for [borg-reborn-rs#842](https://github.com/diegoami/borg-reborn-rs/issues/842)
(owner, 2026-11-21: attack fast, fragile monsters with everything, Phase Door or a
staircase as the only alternative, no cure against them). The 8 deaths are the
`runs/2026-11-21-reborn-head-3b4924ba/replay/<SEED>` cases of borg-zoo#566.

**Direction only.** Eight chosen cases, one start each, no confidence interval;
borg-zoo measures (borg-reborn-rs RULES 14, 20). A case that survives here is a
rescued game on this start, not a rate.

## Build and method

- borg-reborn-rs commit **`ca89e738`** (branch `task/842-fast-fragile`: main `12c4ce7c`
  plus the policy). Engine built as the zoo builds it (`harness/build.sh`, rust, recorder off).
- Replay: `runs/replay-zoo-death.sh <case> <workdir> <that checkout>`, 100,000 game turns
  (the zoo's cap), the case's own `user/borg.txt` with the arm's lines appended. `arms.sh`
  and `summ.py` in this folder do exactly that.
- Control: with the switches at their shipped 0 the 8 games are the zoo's key for key
  ("same game as the zoo" for all eight), and the smoke suite is 3/3 identical to
  `smoke-borg-rs`.

## Arms (lines appended to the case's `borg.txt`)

| arm | lines |
|---|---|
| shipped | none |
| attack-only | `borg_param_fast_fragile_policy = 1`, `borg_param_fast_fragile_escape_percent = 0` |
| named | `borg_param_fast_fragile_policy = 1` |
| named-ban | policy 1, `borg_param_fast_fragile_no_heal = 1` |
| named-ban-exc | policy 1, `no_heal = 2` (cured when cornered) |
| named-esc75 | policy 1, `borg_param_fast_fragile_escape_percent = 75` |
| stats | policy 1, `borg_param_fast_fragile_by_stats = 1` |
| stats-ban | policy 1, by_stats 1, `no_heal = 1` |
| ban-only | `no_heal = 1` |

## Result (`heals` = cure quaffs, `oil` = flasks thrown, `phase` = Phase Door read by the new rule, over the whole game)

| case | shipped | attack-only | named | named-ban | named-ban-exc | named-esc75 | stats | stats-ban | ban-only |
|---|---|---|---|---|---|---|---|---|---|
| Dwarf Mage 896890415 | died (a crow) CL1 DL1 t782; heals 4, oil 1, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 35, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL7 maxDL2 t100000; heals 2, oil 37, phase 3, stairs 0 | alive CL6 maxDL2 t100000; heals 5, oil 77, phase 0, stairs 0 |
| Human Ranger 526144893 | died (a crow) CL1 DL1 t2231; heals 3, oil 0, phase 0, stairs 0 | died (a crow) CL1 DL1 t1326; heals 0, oil 0, phase 0, stairs 0 | alive CL6 maxDL3 t100000; heals 5, oil 6, phase 2, stairs 0 | alive CL6 maxDL3 t100000; heals 5, oil 6, phase 2, stairs 0 | died (a crow) CL1 DL1 t2231; heals 3, oil 0, phase 2, stairs 0 | alive CL6 maxDL3 t100000; heals 5, oil 6, phase 2, stairs 0 | alive CL6 maxDL3 t100000; heals 5, oil 6, phase 2, stairs 0 | alive CL6 maxDL3 t100000; heals 5, oil 6, phase 2, stairs 0 | died (a crow) CL1 DL1 t2195; heals 0, oil 0, phase 0, stairs 0 |
| Gnome Druid 1311931798 | died (a crow) CL1 DL1 t2618; heals 8, oil 4, phase 0, stairs 0 | died (a crow) CL1 DL1 t2728; heals 0, oil 5, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 60, phase 4, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 48, phase 0, stairs 0 |
| Kobold Priest 994753489 | died (a crow) CL1 DL1 t2810; heals 0, oil 3, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 0, oil 69, phase 0, stairs 0 | alive CL6 maxDL2 t100000; heals 0, oil 72, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 0, oil 72, phase 1, stairs 0 | died (a crow) CL1 DL1 t2810; heals 0, oil 3, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 66, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 0, oil 72, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 0, oil 72, phase 1, stairs 0 | died (a crow) CL1 DL1 t2810; heals 0, oil 3, phase 0, stairs 0 |
| Dunadan Priest 1309976551 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 37, phase 1, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 | died (a fatal wound) CL1 DL1 t4430; heals 0, oil 1, phase 0, stairs 0 |
| H-Troll Necro 1705507033 | died (a crow) CL1 DL1 t4501; heals 3, oil 8, phase 0, stairs 0 | died (a crow) CL1 DL1 t4781; heals 1, oil 10, phase 0, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL6 maxDL2 t100000; heals 1, oil 117, phase 1, stairs 0 | alive CL7 maxDL3 t100000; heals 1, oil 102, phase 0, stairs 0 |
| Half-Elf Druid 733550937 | died (a crow) CL1 DL1 t5082; heals 3, oil 4, phase 0, stairs 0 | died (a crow) CL1 DL1 t5040; heals 0, oil 5, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 6, oil 76, phase 1, stairs 0 | alive CL7 maxDL2 t100000; heals 6, oil 76, phase 1, stairs 0 | alive CL7 maxDL2 t100000; heals 6, oil 76, phase 1, stairs 0 | alive CL7 maxDL2 t100000; heals 1, oil 81, phase 1, stairs 0 | alive CL8 maxDL3 t100000; heals 2, oil 48, phase 2, stairs 0 | alive CL8 maxDL3 t100000; heals 2, oil 48, phase 2, stairs 0 | died (a crow) CL1 DL1 t5051; heals 0, oil 4, phase 0, stairs 0 |
| Dwarf Necro 258108142 | died (a crow) CL1 DL1 t11359; heals 1, oil 7, phase 0, stairs 0 | died (a wild cat) CL4 DL2 t37534; heals 0, oil 28, phase 0, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | alive CL7 maxDL2 t100000; heals 5, oil 68, phase 2, stairs 0 | died (a crow) CL1 DL1 t11348; heals 0, oil 6, phase 0, stairs 0 |

shipped: dead 8/8, to crow/cat 7, heals 22, oil 28, phase 0, stairs 0, ff-notes 0
attack-only: dead 6/8, to crow/cat 5, heals 2, oil 153, phase 0, stairs 0, ff-notes 31
named: dead 1/8, to crow/cat 0, heals 20, oil 437, phase 14, stairs 0, ff-notes 80
named-ban: dead 1/8, to crow/cat 0, heals 20, oil 437, phase 14, stairs 0, ff-notes 80
named-ban-exc: dead 3/8, to crow/cat 2, heals 18, oil 362, phase 14, stairs 0, ff-notes 49
named-esc75: dead 0/8, to crow/cat 0, heals 17, oil 472, phase 15, stairs 0, ff-notes 78
stats: dead 1/8, to crow/cat 0, heals 16, oil 409, phase 15, stairs 0, ff-notes 87
stats-ban: dead 1/8, to crow/cat 0, heals 16, oil 409, phase 15, stairs 0, ff-notes 87
ban-only: dead 5/8, to crow/cat 4, heals 7, oil 241, phase 0, stairs 0, ff-notes 0

## Reading it

1. **Policy alone: 8 dead → 1 dead.** The Dunadan Priest 1309976551 is the one left, in every arm but `named-esc75`.
2. **The attack without the Phase Door / stairs alternative is not enough** (`attack-only`: 6 of 8 die, at HP 3 with the crow adjacent). Phase Door is what saves the games: the Gnome Druid 1311931798 reads it four times (it carried eight) and lives.
3. **The heal ban never binds once the policy is on** (`named-ban` = `named`): attack-on-sight acts before the healing code. Alone (`ban-only`), it leaves 5 of 8 dead.
4. **The cornered exception is worse** (`named-ban-exc`): Ranger 526144893 and Kobold Priest 994753489 die again in the cure loop (cure, four bites, cure).
5. **The Dunadan Priest** dies identically in all arms at the default: 7.2 damage a turn against 8 HP is under "the next turn kills" at the mean, so it throws one flask (missed) and the four bites kill it with a Phase Door unread. At `escape_percent=75` it reads Phase and all 8 live.
6. **Necromancer 1705507033, 34 flasks, melee**: not a bug. Its throwing skill is 20 − 10 = 10 (`class.txt:966`, `p_race.txt:227`) against melee 35 + 20 = 55; against a crow (AC 14) a flask hits 20.3% (1.83 HP a turn) and the Main Gauche about 4.09. The planner's expected-damage ranking is right on these numbers.
7. **By stats** the rule also marked cave spiders (6 notes, when a group had thinned to one). Its first version marked a small kobold at "speed +1": monsters spread about one speed point around the race's (`mon-make.c:1158-1164`), so the rule has `fast_fragile_speed_margin` (5).
