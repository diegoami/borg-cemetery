# Zoo deaths: reborn-main-pbd-pilot, run 44098927907-local-replay

**Provenance.** These are the 11 natural deaths of borg-zoo run [44098927907](https://github.com/diegoami/borg-zoo/actions/runs/44098927907) (`reborn-main-pbd-pilot`, borg-zoo#186; borg-reborn-rs 4d83dd26, attack_arrow_point_blank_divisor 1, 2 and 5). That run's own death bundles failed because of a relative `--deaths` path (fixed in borg-zoo#189). Each death was therefore replayed locally with the fixed zoo code, on a local build of the same source hash (258ccc77…). Every replay played exactly the key stream the CI cell recorded (`play_sha256`), and its `params-core.json` reports the arm's divisor. The raw logs are not in the run's artifacts; rerun a dossier to regenerate them.

The natural deaths of borg-zoo run `44098927907-local-replay`, imported by `scripts/import_zoo_deaths.py` (borg-zoo#176). 11 of 11 deaths have a dossier. Every dossier was replayed in the zoo with full logs, and its key stream matched the cell's. A repeat is a death the cemetery already had.

| Dossier | Profile | Seed | Character | Cause | Turn | Level | Depth (max) | Import |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| [D-0a0f08dbd16f](../../deaths/D-0a0f08dbd16fc6b6f65a18bb06a213dee6223d8b98b929c423e8ed366c2870a2/README.md) | reborn-main-pbd1 | 102023799 | Human Druid | a small kobold | 45514 | 4 | 2 (2) | exported |
| [D-d0fb912491ea](../../deaths/D-d0fb912491ea722a7d9b04e1dad09608c14fac3e3e64e49f36872bc8506a56f4/README.md) | reborn-main-pbd1 | 300036923 | Human Necromancer | a wild cat | 12328 | 1 | 1 (1) | exported |
| [D-af257e0d0bd1](../../deaths/D-af257e0d0bd1b16d4b8cd1d682852405dc80853948eb1b870b2d9133e896bd5e/README.md) | reborn-main-pbd1 | 888896726 | Half-Elf Blackguard | a crow | 54455 | 3 | 2 (2) | exported |
| [D-3ad8f65c4aef](../../deaths/D-3ad8f65c4aef4c8ac9c0a58e868d4b961e002a41b58ed7b1f1b50ce00f93234f/README.md) | reborn-main-pbd1 | 1502695781 | Human Rogue | a giant white mouse | 9976 | 3 | 1 (1) | exported |
| [D-6f6f69cdc0d1](../../deaths/D-6f6f69cdc0d1f739ba8b9a64b09b7d743bd3042a521c8b639502f4ea2c51058c/README.md) | reborn-main-pbd2 | 102023799 | Human Druid | a rock lizard | 33735 | 2 | 1 (1) | exported |
| [D-37b257768410](../../deaths/D-37b25776841057313c8ec4f03c2121a1a1be2b24485ec25702207ae7328349ef/README.md) | reborn-main-pbd2 | 226104090 | Human Ranger | a soldier | 76788 | 5 | 1 (2) | exported |
| [D-a11c0a7a2abb](../../deaths/D-a11c0a7a2abb486dd41868b5f86eeda660ec44b5205b67d7179679b6e9520866/README.md) | reborn-main-pbd2 | 300036923 | Human Necromancer | a wild cat | 12328 | 1 | 1 (1) | exported |
| [D-2f582b9b2b1e](../../deaths/D-2f582b9b2b1ef1e480d235dc7e73f078dc27d9557cc827c5a2c43b5f4ca75cca/README.md) | reborn-main-pbd2 | 888896726 | Half-Elf Blackguard | a crow | 54455 | 3 | 2 (2) | exported |
| [D-c892630cb993](../../deaths/D-c892630cb993dec464750e1de5db731e8936c57611cf4e0ddf1b32100467ba30/README.md) | reborn-main-pbd5 | 102023799 | Human Druid | a rock lizard | 33735 | 2 | 1 (1) | exported |
| [D-74a83e6c2de3](../../deaths/D-74a83e6c2de317abcca72a298a226e4ff1ee8f56ec2af759f85994ae081ebe84/README.md) | reborn-main-pbd5 | 300036923 | Human Necromancer | a wild cat | 12328 | 1 | 1 (1) | exported |
| [D-bcb22b6e93ac](../../deaths/D-bcb22b6e93ac5017d7f670a3690bf861b81bcf866ac6abe0885c42d495039ba4/README.md) | reborn-main-pbd5 | 888896726 | Half-Elf Blackguard | a crow | 54455 | 3 | 2 (2) | exported |

Each dossier's REPLAY.md has the build, watch and rerun commands. A replay and its original are one life, not two samples.
