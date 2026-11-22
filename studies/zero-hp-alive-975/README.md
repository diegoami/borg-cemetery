# A monster at 0 HP is alive: grey mold (Hobbit Ranger 282602274) and grey mushroom patch (Kobold Ranger 1723941400)

Study for [borg-reborn-rs#975](https://github.com/diegoami/borg-reborn-rs/issues/975), with the fix in
[borg-reborn-rs#994](https://github.com/diegoami/borg-reborn-rs/pull/994) (`kill_live_zero_hp`, compiled 0, not
shipped). Both deaths come from zoo run [45028029063](https://github.com/diegoami/borg-zoo/actions/runs/45028029063)
on the borg-rs core, on track-p `9085c266`. They replay on `4b2c2fcf`
([borg-zoo report](https://github.com/diegoami/borg-zoo/blob/claude/dazzling-hamilton-ejjpi4/reports/reborn-trackp-9085c266-full-other-deaths/README.md)).
The zoo measurement is requested in [borg-zoo#670](https://github.com/diegoami/borg-zoo/issues/670).

Dossiers (branch `runs/2026-11-22-trackp-9085c266-full-deaths`):
- **Grey mold:** [D-dd6cbab2a37e](https://github.com/diegoami/borg-cemetery/blob/runs/2026-11-22-trackp-9085c266-full-deaths/deaths/D-dd6cbab2a37e0eba82088bb1ef5ada66f1e97213b5214a1e1cd5974f2b7761ed/README.md), Hobbit Ranger 282602274.
- **Grey mushroom patch:** [D-c2d9dcbfcfa4](https://github.com/diegoami/borg-cemetery/blob/runs/2026-11-22-trackp-9085c266-full-deaths/deaths/D-c2d9dcbfcfa4d172a20d648260cdc42d24d39599220a2c7ff25cb06a86eab544/README.md), Kobold Ranger 1723941400.

**One start each, so these are leads, not measurements** (borg-reborn-rs RULES 14). The flag-1 arms are
alternative continuations of the same lives, not independent games.

## Summary

- **Cause.** The engine kills a monster only when its hp falls below 0 (`mon_take_hit`,
  `src/mon-util.c:1300` at Angband `574b618c`), so a monster hit down to exactly 0 lives. The Borg reads hp
  from the engine (`set_health`, `borg_flow_kill.rs:375`). The #546 floor (`kill_live_min_power`, shipped 1)
  applies only when hp is above 0, so such a monster is estimated at **0 HP**.
- **What the 0 does.** The overkill caps (`borg_fight_attack.rs:694`, `:1629`) limit every attack's damage to
  the estimate times a multiplier, so every attack scores 0 and `borg_attack` passes ("nonpositive_return" in
  the trace). The danger code does not read the estimate for a mold: danger 0 at turn 5454 is the danger on
  the Borg's own square before the step.
- **Grey mold, 282602274** (2 HP; an arrow hits for 2, "jerks limply"):
  - **Flag 0** (`13e34b27193b2e8c`, the zoo's game). At 3584 the first mold is not shot again. At 5454 a
    second mold is not shot again either, and `borg_flow_old` steps next to it. Spores take HP 12 → 5, a melee
    swing misses, and the Ranger dies at 5467 with 6 CLW and 10 Phase Door.
  - **Flag 1** (`f23e697a38a01ae2`). The game diverges at 3584, where a second arrow destroys the first mold.
    The Ranger is alive at the 100,000-turn cap: CL7, max DL3, 18,229 keys.
- **Grey mushroom patch, 1723941400** (3 HP; a Main Gauche hit for 3): flag 0 and flag 1 play the same keys
  (`eca7a249ca7c64b4`), dying at 1314. The estimate reads "0 HP" with the flag off and "1 HP" with it on.
  Kill-on-sight melees the patch either way while the Ranger is confused, so this death belongs to
  borg-reborn-rs#969, not to this fix.

## Arms

| arm | seed, race, class | `kill_live_zero_hp` | keys sha256 | end |
|---|---|---|---|---|
| `mold-0` | 282602274, 3 Hobbit, 7 Ranger | 0 | `13e34b27193b2e8c…` | dies at 5467 to a grey mold, CL1 DL1 |
| `mold-1` | same | 1 | `f23e697a38a01ae2…` | alive at 100,000, CL7, max DL3 |
| `mush-0` | 1723941400, 10 Kobold, 7 Ranger | 0 | `eca7a249ca7c64b4…` | dies at 1314 to a grey mushroom patch, CL1 DL1 |
| `mush-1` | same | 1 | `eca7a249ca7c64b4…` | the same game |

Each `arms/<arm>/` holds:
- `borg.txt`: the shipped `harness/borg.txt` with the zoo report's overrides and `borg_param_kill_live_zero_hp`. The `mold-0` and `mold-1` files differ in that one line.
- `keys.log.gz` and `keys.sha256`: the key stream and its full hash.
- `summary.json`: the run's summary.

## Reproduction

| what | value |
|---|---|
| build | borg-reborn-rs `1f4e9e89` (track-p `4b2c2fcf` plus the parameter), `BORG_IMPL=rust harness/build.sh`. With the flag at 0 it plays as `4b2c2fcf`: smoke-borg-rs is 3/3 identical, and `mold-0` matches the zoo's hash |
| configuration | `arms/<arm>/borg.txt`, built by [`tools/replay.sh`](tools/replay.sh) from the shipped `harness/borg.txt` |
| command | the zoo report's: `angband -mborgh … -- -seed S -race R -class C -turns 100000 -menu-letters -exact-turns`, BORG_* cleared, from birth, no save loaded |
| check | `sha256sum keys.log` equals `arms/<arm>/keys.sha256` |

`attack_kill_on_sight_min_hp_percent` (#969's setting) is not on track-p, so 1723941400 was replayed at
shipped settings. The issue's run, which died at 1323 with that setting, was not repeated.

## Evidence

The `evidence/` excerpts, with the message-log turn in the second column:
- `mold-0-messages-3574-3594.log`, `mold-1-messages-3574-3594.log`: the first mold, the divergence.
- `mold-0-messages-5434-5467.log`: the death.
- `mold-0-trace-core-*.jsonl`, `mold-1-trace-core-3574-3594.jsonl`: the decision trace.
  - At think 384 (turn 3584) and think 579 (turn 5454), every `borg_attack` candidate in `mold-0` has raw utility 0.
  - At think 384, `mold-1` fires.
- `mush-0-messages-1259-1314.log`, `mush-1-messages-1259-1314.log`: the patch case, "0 HP" against "1 HP" with the same messages otherwise.
