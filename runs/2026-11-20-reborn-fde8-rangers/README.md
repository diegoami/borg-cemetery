# The Ranger deaths of borg-reborn-rs main fde8025a's full run

- **Source:** borg-zoo `reborn-main-fde8-full`, run [44681930409](https://github.com/diegoami/borg-zoo/actions/runs/44681930409) (borg-zoo#488).
  - borg-reborn-rs main `fde8025a` with its shipped harness/borg.txt, engine 574b618c, classes-1800, 100,000 turns.
- **Selection:** at the owner's request (2026-11-20), only the run's 12 Ranger deaths are imported here, not all 33. The run page lists just these.
  - Each dossier was replayed in the zoo with full logs, and its key stream matches the cell's.
- **Why Rangers:** between main 94032140 and fde8025a, on the same 200 starts, Ranger deaths rose from 5 to 12, the largest change of any class (Priests 3 to 5, Warriors 0 to 1; the others fell). 11 of these 12 survive on 94032140 (borg-zoo#488).
- **Report with the last recorded screens of each death:** https://claude.ai/artifact/9mNNHzbGBFsjUyqaULpzHt
  - Merged in between: borg-reborn-rs #725 (#716, the Ranger arrow cap), #739 (#736, `caution_stairs_clean_path`, `caution_immobile_step_to_exit`) and #738.

| dossier | seed | character | killed by | CL | DL | game turn | arrows at death | last attack |
|---|---|---|---|---:|---:|---:|---:|---|
| [D-14f4ce452597](../../deaths/D-14f4ce4525975a357d623e1048d8ea21676bf89e57af9d57749b8b1c15146faa/README.md) | 432972050 | Half-Elf Ranger | a cutpurse | 1 | 1 | 1,528 | 65 | melee |
| [D-7e07cc9e67b6](../../deaths/D-7e07cc9e67b6a60f60af54b0b2d449c322d05e6d5f58a855c8972afa8973d29f/README.md) | 807683971 | Human Ranger | a black naga | 1 | 1 | 1,534 | 74 | melee |
| [D-d09b9d357988](../../deaths/D-d09b9d357988e5fe2fbcb60d5691ec15d2e9d00a2ceaadf5868c72d4ee2a9124/README.md) | 2095979189 | Half-Orc Ranger | a wild cat | 1 | 1 | 3,345 | 80 | melee |
| [D-3299fd20a324](../../deaths/D-3299fd20a324cddeb556d39707e3b22e0735fa9666224a1a22fe26b587060911/README.md) | 425904011 | Elf Ranger | a wild cat | 1 | 1 | 3,660 | 72 | melee |
| [D-4d01e23a3d52](../../deaths/D-4d01e23a3d529c82e67301b17fbaacf8d6dae8d2265709ff0f255e8a0b241f8a/README.md) | 1976035382 | Dunadan Ranger | a wild cat | 1 | 1 | 4,248 | 73 | melee |
| [D-9e526055f043](../../deaths/D-9e526055f043e11781d5ecb1d97e66385be2acd3a5590f775b6145d4fe0720e8/README.md) | 2049259432 | Gnome Ranger | Fang, Farmer Maggot's Dog | 1 | 1 | 4,429 | 70 | shot |
| [D-b2999995995d](../../deaths/D-b2999995995dc0cee34ce8ecf8133ef74a8684a88ad2e7cdb44340aebf8b0073/README.md) | 154156985 | High-Elf Ranger | a crow | 1 | 1 | 5,563 | 53 | melee |
| [D-57bc76470000](../../deaths/D-57bc76470000bab3f203ffb0085c3ffe48901c0a6e7162a713f2d0a5b0965bec/README.md) | 225452245 | Half-Orc Ranger | a kobold shaman | 4 | 1 | 5,647 | 64 | melee |
| [D-e1ba89db1a1e](../../deaths/D-e1ba89db1a1e0e03ce014e04f1d2e2ab2cc14228048ee34ff9a5aef98c648010/README.md) | 1517990203 | Gnome Ranger | a small kobold | 1 | 1 | 6,338 | 58 | melee |
| [D-df12b1b7e3a9](../../deaths/D-df12b1b7e3a94be38e36f2a45e5fddf69ddab9fd00fd6a66b396c7550b62ab77/README.md) | 1222599014 | Half-Elf Ranger | a wild cat | 2 | 1 | 11,016 | 86 | melee |
| [D-b83cd0de21e0](../../deaths/D-b83cd0de21e0ef12b029584a2b33912a059eb75a07bb344333b80be39c6e4c40/README.md) | 1583605217 | Kobold Ranger | a crow | 4 | 2 | 27,297 | 67 | melee |
| [D-ecd3c22b08b0](../../deaths/D-ecd3c22b08b0c94a9c5285143428c2dc1ef56b9afab0d8d28f0cc41ce689c116/README.md) | 214960633 | Half-Troll Ranger | a grey mold | 5 | 1 | 61,850 | 24 | shot |

## What the deaths show (from messages.log; observations, not a diagnosis)
- **Early:** 9 of the 12 die on DL1 before game turn 6,400, 8 of them at CL1. Across all 12, the killers are wild cats (4), crows (2), a cutpurse, a black naga, Fang and a small kobold.
- **Ammunition:** none ran out of arrows. Each had 24-86 at death, most 53 or more; the first town visit bought 45-60 arrows and 3 unknown potions, no armour.
- **Melee at the end:** the Rangers shoot at range (446 shots against 94 melee over these 12 games). Once the monster is adjacent they switch to the Main Gauche (1d5): the last attack was melee in 10 of the 12.
  - Arrows at point-blank are halved for Rangers (`attack_arrow_point_blank_divisor_ranger = 2`). borg-zoo#379 found divisor 1 worse, so this alone isn't the fix.
- **Flight:** the scary rule flags the killer every time ("Scary by damage: wild cat, 7 of max HP 14"), and they flee constantly: 15-57 "Fleeing" or "Looking for stairs" notes per CL1 death.

## Playing them
`~/borg-play/fde8-rangers` on the owner's machine holds these 12 deaths. That folder isn't part of this repository; it was built from these bundles:
- an X11 build of fde8025a (`BORG_X11=ON harness/build.sh`);
- per death, the arm's borg.txt and scary list, the zoo's keys, messages and state logs;
- saves at about 3,000, 1,000 and 300 game turns before the death and just before it.

Every save was cut after a full replay with that build matched the zoo run's play hash. `./play.sh` there works as in `~/borg-play`.
