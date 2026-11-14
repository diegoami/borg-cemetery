# Saved scenarios

Every scenario has a written account, a screenshot animation, inventory and
learned-spell tables, and copyable instructions for testing another Borg from
its saved position. The original birth seed is **102**, an Elf Mage; the
original program is borg-reborn-rs commit `e9a6a521f3ac`.

| Scenario | Situation | Saved turn | Original outcome |
| --- | --- | --- | --- |
| [S0001](S0001/README.md) | Estimated-danger candidate | 3202 | Reached sustained stability again at 3302 |
| [S0002](S0002/README.md) | Estimated-danger candidate | 3302 | Reached sustained stability again at 3382 |
| [S0003](S0003/README.md) | Sequence leading to the Fang death | 3402 | Died at 3640; alternative borg-rs survived its tested horizon |

The first two are detector candidates, not proof that death was imminent.
All three positions came from one birth and belong to [death D0007](../deaths/D0007/README.md).
Trials preserve the saved engine RNG and start a fresh Borg in each arm.
These saved positions are playable; this birth has no standalone-recorder
input recording. Each replay page explains that distinction and the exact
commands that are available.
