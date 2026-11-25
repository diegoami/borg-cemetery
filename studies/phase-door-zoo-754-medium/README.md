# Phase Door at two breadth-first-off deaths

[Zoo #754](https://github.com/diegoami/borg-zoo/issues/754) run
[45456422005](https://github.com/diegoami/borg-zoo/actions/runs/45456422005)
measured 270 paired starts in the normal world. This study varies the
unseen-grid veto on the two deaths in that run's breadth-first-off arm.
The [original death dossiers](https://github.com/diegoami/borg-cemetery/pull/155)
cover the comparison across exploration settings.

| Start | Unseen-grid veto on | Unseen-grid veto off |
| --- | --- | --- |
| High-Elf Ranger 1125613689 | Soldier death at turn 10,108, CL2 | Alive at 100,000 turns, CL7, deepest DL3 |
| Dunadan Warrior 480049625 | White mouse death at turn 12,925, CL2 | Same death and key stream |

Both control key streams match their archived Zoo SHA-256 on a clean
GCC right-to-left build. The diagnostic observer and the clean build
also agree on key hashes in both counterfactuals. The [replay
manifest](replays.tsv) records the exact keys and outcomes. These two
starts were selected for investigation after their deaths.

## Ranger

At turn 9,834, the adjacent soldier caused the emergency combat gate to
permit Phase Door at 25/25 HP. With the unseen-grid veto enabled, the
emergency check counted 92 of 100 samples as scary, including 91 unseen,
and refused. The Borg attacked. With the veto disabled, the check
counted 18 scary samples and the Borg read the scroll. That is the first
distinct key. The veto-off Ranger survived this named start.

The local observer retained the last mixed frame at turn 9,764 with
radius 10. In the accepted check, 87 samples had a ring at or inside
that radius, and 13 lacked a ring in the retained frame. The current
goal was already escape. These are distances in a prior frame. They
give no verified candidate beyond radius 10 and leave the semantics
for a missing or stale ring open. [Mixed landing issue](https://github.com/diegoami/borg-reborn-rs/issues/1116)

## Warrior

The two arms produced the same keys through death. The emergency landing
checks that the local mixed observer captured were already 100/100
scary in both arms. The veto toggle left this decision unchanged.
[Phase Door switch issue](https://github.com/diegoami/borg-reborn-rs/issues/1073)

## Reproduce

Build the default borg-rs core at
`c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894` with GCC right-to-left
argument order. Use the normal world and shipped settings with
`BORG_TXT_SET=borg_param_explore_breadth_first=0`. For the second arm,
append `;borg_param_escape_phase_unknown_scary=0` to that variable.
Newcomer wait stays on. Run
`harness/run.sh OUT SEED RACE_IDX CLASS_IDX 100000 menu,exact`.
The manifest includes the engine birth indices. This experiment
holds the exploration candidate fixed and does not estimate population
mortality or the interaction between breadth-first and the veto.
