# Fang at CL1: the oil's hit chance against the engine's (borg-reborn-rs#986)

What was asked (borg-reborn-rs [#986](https://github.com/diegoami/borg-reborn-rs/issues/986)):
two deaths against Fang, Farmer Maggot's Dog (speed +20) at CL1, from zoo run
[45028029063](https://github.com/diegoami/borg-zoo/actions/runs/45028029063). In both the
fight race said "winning" while the oil missed. Is the hit chance the race uses for thrown oil
the engine's? Does "2.000 turns to kill" assume every throw hits? Does #929's guessed wall on
the Borg's own grid change these fights?

**Two starts, one game each.** These are anecdotes, not rates (borg-reborn-rs RULES 14, 20).

## Answer

1. **No gap.** The Borg's hit chance for thrown oil is the engine's, to the permyriad, on every
   throw the fight race rated (7 of 7). Measured under gdb in the engine's own roll.
2. **"2.000 turns to kill" does not assume hits.** It is the expected damage: a throw's damage,
   capped at the HP the target still needs, times the engine's hit chance. The number of turns
   is rounded up to whole commands.
3. **#929's wall write does not change these fights.** With the write on the Borg's own grid
   removed, both key streams stay byte-identical, although the guard fired 5 times (Paladin)
   and 2 times (Druid).
4. **What happened instead:**
   - **Paladin:** five misses in a row at the engine's 67.70%, which has a probability of
     0.323^5 = 0.35%.
   - **Druid:** no "winning" verdict against Fang at all. Its death is the flight and the
     Recall refusal (#758), not this race.

## Builds and reproduction (verified)

- **Build:** borg-reborn-rs track-p `4b2c2fcf913e352ebd7bef5f16a531e8fc50d92a`,
  `BORG_IMPL=rust harness/build.sh`, borg-rs core.
- **Settings:** the shipped `harness/borg.txt` with the zoo arm `reborn-head-shipped`
  (`borg_reborn_core = borg-rs`, `borg_reborn_errand = none`). The zoo's `config_text`
  overrides are applied: respawn race and class, `borg_cheat_death = FALSE`,
  `borg_respawn_winners = FALSE`, and the `borg_world` line removed. Each case's
  `data/*/borg.txt` is the file the game read.
- **Command line:** the zoo's `borgrs.command`, with `-exact-turns`, `-statelog` and
  `-msglog`. The script is [`tools/replay.py`](tools/replay.py).

| Seed | Character | `sha256 keys.log` | End |
|---|---|---|---|
| 1194051723 | Elf Paladin (`-race 2 -class 5`) | `7fb11d46a041a04a…` | dead at game turn 1700, CL1 |
| 1024822556 | Dunadan Druid (`-race 8 -class 2`) | `3687ca84c5cdeb34…` | dead at game turn 3086, CL1 |

Both play hashes are the zoo's (borg-zoo#668), so these are the same games. Full hashes are in
[`data/SHA256SUMS`](data/SHA256SUMS).

## 1. The hit chance: engine against Borg

**The engine.** A thrown object's hit is one roll (`engine/angband/src/player-attack.c` at
`574b618c`):

- `make_ranged_throw` rolls `test_hit(chance_of_missile_hit(...), mon->race->ac)` (`:1279`).
- `chance_of_missile_hit_base` (`:121-145`) gives skill + bonus × `BTH_PLUS_ADJ`. For a
  `THROWING` object the bonus includes `p->state.to_h`; the flask of oil is
  `EXPLODE | THROWING` (`lib/gamedata/object.txt:254-265`).
- `chance_of_missile_hit` (`:156-165`) subtracts the distance and halves the chance for a target
  that is not obvious.
- `hit_chance` (`:196-219`): 12% always hit, 5% always miss, the rest scaled by
  (to-hit − 2/3 AC) / to-hit.
- Fang's AC is 36 (`lib/gamedata/monster.txt:1087`).

**The Borg.** The fight race (`winning_fight`, `borg-core/src/borg_caution.rs`) rates each foe
with `focused_attack`. For a throw, that goes to `focused_launch_damage`
(`borg-core/src/borg_fight_attack.rs:5290-5322`):

- the same chance: `BI_THT + 3 × (BI_TOHIT + to_h) − dist` for a `THROWING` object;
- the damage capped at the HP still needed;
- then `× hit_permyriad(chance, ac)` (`:5318`), which is `hit_chance` transcribed (`:5261`).

**Measurement.** [`tools/hit.py`](tools/hit.py) is a gdb script. The C engine has no debug
information and `test_hit` and `hit_chance` are inlined, so it breaks on `make_ranged_throw` and
on `random_chance_check`, which receives the engine's numerator and denominator. It then reads
the result's `success` and `dmg` on return. Under gdb the key streams are unchanged (same
hashes). Output: `data/*/engine-throws.txt`.

| Seed | Game turn | Target | Engine chance | Borg's rating (`Fight race targets`) | Implied Borg chance | Hit |
|---|---|---|---|---|---|---|
| 1194051723 | 1551 | Fang (needs 26) | 6770/10000 | 14.894 HP/turn (22 × p) | 67.70% | yes, 9 |
| 1194051723 | 1571 | Fang (needs 17) | 6770 | 11.509 (17 × p) | 67.70% | no |
| 1194051723 | 1591 | Fang (needs 17) | 6770 | 11.509 | 67.70% | no |
| 1194051723 | 1611 | Fang (needs 18) | 6770 | 12.186 (18 × p) | 67.70% | no |
| 1194051723 | 1621 | Fang (needs 18) | 6770 | 12.186 | 67.70% | no |
| 1194051723 | 1662 | Fang (needs 18) | 6770 | 12.186 | 67.70% | no |
| 1024822556 | 2342 | Fang (needs 26) | 5668 | 12.469 (22 × p) | 56.68% | no |
| 1024822556 | 2392 | white icky thing (needs 5) | 8701 | 4.350 (5 × p) | 87.00% | yes |

**Gap: 0 permyriad on every rated throw.** The issue's counts ("1 hit in 6", "3 hits in 6")
are right, but for the Druid only one throw was at Fang. The others were at a white icky thing
(87.01%) and a grey mushroom patch (95.00%).

## 2. What "2.000 turns to kill" means

- `race_turns` (`borg_caution.rs:2163-2176`) divides the HP still needed by the expected damage
  per command, from §1, and rounds up to whole commands.
  - At 1551: 26 / 14.894 = 1.75, which rounds up to 2.
  - Later: 17 / 11.509 = 1.48, which rounds up to 2.
- `wins_race` (`:2178-2181`) then asks whether turns × incoming < HP: 2 × 4.750 = 9.5 against
  HP 10 or 11. **That is a comparison of means, with a margin of 0.5 to 1.5 HP.**
- [`tools/race_sim.py`](tools/race_sim.py) fights the race to the end: no cures, no retreat,
  criticals and Fang's RAND_25 ignored. With the engine's 67.7% the Paladin wins **81%** at HP 11
  against Fang at 25, and **about 90%** against Fang at 16 or 17. So "winning" was a fair
  estimate of a fight fought to the end. It was not a sure one.
- **The Paladin did not fight it to the end.** The verdict flipped with its HP:
  - "winning" at HP 10–11, and it threw;
  - "not winning" at HP 6–9, and it drank a CLW (1561, 1581, 1601, 1641, 1651).
  - All 5 CLW went that way. At HP 2 the emergency Phase Door fired (1672). It died bleeding
    at 1700 with 5 Phase Door left.
  - Fang lost 9 HP to the one hit and regenerated about 1 HP.
- **The Druid** logged 16 fight-race lines against Fang, all "not winning" (3.000 turns at
  HP 9–13). Its one throw at Fang came from another planner. The rest of that fight is the
  flight and `Refusing flight Recall` (51 times, borg-reborn-rs#758).

## 3. borg-reborn-rs#929: the guessed wall on the Borg's own grid

- After each miss, `borg_target_unknown_wall` (`borg-core/src/borg_projection.rs`) logged
  `Guessing wall (50,87) near target (51,88)`, with the Borg at (50,87). That is 5 times for the
  Paladin, and 2 for the Druid at (39,112).
- Its "pathway found the target" branch steps back from the adjacent target onto the Borg's grid
  and writes `FEAT_GRANITE` there.
- **Counterfactual.** [`tools/cf929.patch`](tools/cf929.patch) is an environment-gated patch,
  built and never committed. With it, no wall is written on the Borg's grid and the function
  returns false, so `successful_target` stays negative.
- **Result.** The guard fired 5 times and 2 times (`# CF929` notes), and both key streams are
  **byte-identical** to the deaths (`data/*/keys-cf929.log`, same sha256).
- **So the write does not change these two fights.** That says nothing about other games;
  #929 stays open on its own evidence.

## What this cannot show

- Whether a margin on the race, such as a kill probability instead of means, or no flip-flop
  between throw and CLW, would have saved the Paladin. That is a policy change. It would need a
  parameter and a borg-zoo measurement.
- Criticals are not in the simulation. `critical_shot` can add damage. The measured damages
  (9, 27, 36) show none here.
