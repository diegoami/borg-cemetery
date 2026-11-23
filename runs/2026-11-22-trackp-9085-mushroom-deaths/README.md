# The 11 grey mushroom patch deaths of trackp 9085c266

Source: borg-zoo#645 (baseline of borg-reborn-rs trackp `9085c266`, shipped settings, classes-1800 full slice, 900 starts, 100,000 turns), run [45028029063](https://github.com/diegoami/borg-zoo/actions/runs/45028029063). All 28 deaths of the run were replayed from birth (keys match the zoo cell's) and are dossiers in [zoo-reborn-trackp-9085c266-full-45028029063](../zoo-reborn-trackp-9085c266-full-45028029063/README.md); this page lists the 11 whose killer is a grey mushroom patch.

Report with each death's last recorded screens: https://claude.ai/artifact/9guW56gLU9BBnncyo2ShMq
Play pack: `~/borg-play/trackp9085-full` (`./play.sh`).

| character | seed | CL | DL | turn | dossier |
|---|---:|---:|---:|---:|---|
| Kobold Druid | 1062599390 | 1 | 1 | 160 | [D-907b0f6c4b76](../../deaths/D-907b0f6c4b76779140eb61e23319395ec09a74121ef4140ab670cf96ab34695f) |
| Kobold Ranger | 1723941400 | 1 | 1 | 1314 | [D-c2d9dcbfcfa4](../../deaths/D-c2d9dcbfcfa4d172a20d648260cdc42d24d39599220a2c7ff25cb06a86eab544) |
| Half-Troll Priest | 1896645817 | 1 | 1 | 2270 | [D-82942e96ea50](../../deaths/D-82942e96ea50b41e1ab38c331c1f416f68a3edc61fbff236690cba1f4aa8e5d9) |
| Dunadan Necromancer | 1928291203 | 2 | 1 | 2544 | [D-2e7f15b5c70c](../../deaths/D-2e7f15b5c70cce02b88bb5a6bdcc593607fc6e6d716c0a3c9302f2b70ea50604) |
| Gnome Druid | 1917818854 | 1 | 1 | 3113 | [D-50b92f1de753](../../deaths/D-50b92f1de75344493c126d9beee536990feaddb37d138c3e95fd2fcea922eb39) |
| Gnome Priest | 327746368 | 1 | 1 | 4712 | [D-9cbd3a86c931](../../deaths/D-9cbd3a86c931760f52151912dae87c6964f506032b7287eae9e76849c75386b0) |
| Elf Druid | 1143689460 | 3 | 1 | 10825 | [D-86d4d814d008](../../deaths/D-86d4d814d0088db4d54dfceff3aca9788b841e7b145721daaba89b6e54ff7c27) |
| Elf Blackguard | 1965910635 | 2 | 1 | 11871 | [D-43950a07124e](../../deaths/D-43950a07124e5c770c66b94389ab8664363aec672c3b93f20877084de8fa237f) |
| Kobold Druid | 653243095 | 2 | 1 | 13069 | [D-2246038bdaf9](../../deaths/D-2246038bdaf92584ddc36cb66a383b50a5171924557473faeb39d768a6c12742) |
| Dunadan Ranger | 284201809 | 2 | 1 | 16357 | [D-5f8796702ac1](../../deaths/D-5f8796702ac1cd5b378935c97cdd0a0ba32052c399bee34c82fc53648d0d66b6) |
| High-Elf Necromancer | 215443413 | 5 | 1 | 59574 | [D-a5ab59206c60](../../deaths/D-a5ab59206c60ba582de37b49d2dbb3161bd7b86a6e0ab073989b3835746e493d) |

## Observations (counted from the replays)

- On the same 900 starts, main `f57499d0` (run 44976971265) had 14 deaths and main `ab775d48` (run 44944083365) 16, none by a mushroom patch. Here 11 of 28.
- Every death is the same loop: a spore confuses the Borg, then each think notes `Attack on sight: grey mushroom patch (kill-on-sight)` and swings. No cure was drunk and no stairs were taken in any final encounter. Contact to death was 45 to 162 game turns (median 59).
- 86 melee swings in the final encounters of ten deaths; 11 reached the patch (9 hits, 2 misses), 42 chipped at a wall, 32 spun around an empty grid, 1 unclassified. The engine's confusion rule predicts 11/32 (34%) going the right way; 11 or fewer of 86 has a chance of about 5e-6 at that rate. Not explained.
- 8 of 11 met the patch unseen (the first patch line in the log is its spore message). Kobold Druid 1062599390 arrived on DL1 with the patch beside the staircase and died on the `Up staircase` without moving.
- Carried at death: Cure Light Wounds in 8 of 11, Cure Serious Wounds in both Priests and the CL5 Necromancer, flasks of oil in 4, a bow with arrows in both Rangers. Ten of 11 final encounters chose melee.
- On f57499d0 the scary list had the patch as `ranged`; on 9085c266 it is `attack | kill-on-sight | melee, missiles, throws, devices` (#869), with `attack_confused_by_direction` 1 (#901). 102 commits separate the builds; which adds the deaths is not known.
- Same-start pairs: seeds 1965910635, 653243095 and 1928291203 died on other causes on the older builds (zoo-reborn-tonight-full-44944083365 lists them).
