# borg-zoo #501: flight fixes on e8b3acfd, every death

**Report with each death's last recorded screens:** https://claude.ai/artifact/UrppDb4v4u7n7XV8m1Exzn

## Source
- **Specimen:** `4.2.6-reborn-rust-flight-e8b3acfd` (borg-reborn-rs `scratch/T751-with-755`).
- **Arms:** `ctl` (shipped flight) and `flight` (six switches: #743, #747, #749, #750, #751, #753).
- **Runs:**
  - [44738419997](https://github.com/diegoami/borg-zoo/actions/runs/44738419997): the 200 classes-1800 Ranger starts, 400 games;
  - [44738432656](https://github.com/diegoami/borg-zoo/actions/runs/44738432656): classes-1800-small;
  - [44738444831](https://github.com/diegoami/borg-zoo/actions/runs/44738444831): classes-1800-medium.
- **Run pages:** `runs/zoo-reborn-flight-fixes-*`.
- **The pilot** ([44737523620](https://github.com/diegoami/borg-zoo/actions/runs/44737523620), 18 starts) has one death, in ctl only: Human Druid 102023799, CL4 DL1, a clear icky thing at game turn 37,759 ([D-f74e3c4476](../../deaths/D-f74e3c4476afb6174df9c5f660d206e5864aa1f46d7ec6a8b2a9fe34df195a62/)). It is in the second report below, with all four runs: https://claude.ai/artifact/SnqujSa3vHiJUebG9hLu87

## Deaths
14 in ctl and 16 in flight. That is 21 different games: 7 the same in both arms, 4 in ctl only, 6 in flight only, and 2 starts that die differently in each arm. Every replay's keys match the zoo cell's.

| dossier | character | killed by | game turn | arm |
|---|---|---|---:|---|
| [D-e74bce649f](../../deaths/D-e74bce649ff4e7ffa1df68f1c5d10f4185542f23b3eb443ef9a4aede1b6d4dd4/) | Human Ranger, CL1 DL1 | a black naga | 1,534 | ctl, other arm dies differently |
| [D-699216fe94](../../deaths/D-699216fe94cfe9f2964604f15f68e3ce40fc6bc96f497cd32692240e2ff03a43/) | Elf Necromancer, CL1 DL1 | an apprentice | 2,147 | flight only |
| [D-9170afbd54](../../deaths/D-9170afbd546818293fe7e8038b67a371885afd44e0faa1c724d852adfb6ac25b/) | Half-Orc Ranger, CL1 DL1 | a wild cat | 3,326 | flight, other arm dies differently |
| [D-5cb784c6ad](../../deaths/D-5cb784c6ad20e5a158f78913be73bb4df46e2e966971bcc6e84d4b0eece90f08/) | Half-Orc Ranger, CL1 DL1 | a wild cat | 3,345 | ctl, other arm dies differently |
| [D-5ceb347a93](../../deaths/D-5ceb347a93e900b15d79a1b3883da6efc29c682a2657d5265716124e24671663/) | Elf Ranger, CL1 DL1 | a wild cat | 3,660 | same in both |
| [D-8f67a91cea](../../deaths/D-8f67a91ceadddd2328e35e62f8dad2ac490cf92560a6ecdf9fce2a67312ebaa3/) | Dunadan Ranger, CL1 DL1 | a wild cat | 4,248 | same in both |
| [D-e037702475](../../deaths/D-e0377024753cf0efe981830a0f4b481f3b2d4d25b5e84598858dbde9aa698f53/) | Gnome Ranger, CL1 DL1 | Fang, Farmer Maggot's Dog | 4,429 | same in both |
| [D-ec213c6be1](../../deaths/D-ec213c6be10e7ca4cb48d033d6fcccf8cd0c63dcf02f1e1053252d97c5bc59ed/) | Half-Orc Ranger, CL4 DL1 | a kobold shaman | 5,647 | ctl only |
| [D-b4089d61ab](../../deaths/D-b4089d61abea685dd3badc939cbde14db973d6322b0258d441671cd6ba50f5fc/) | Gnome Ranger, CL1 DL1 | a small kobold | 6,338 | same in both |
| [D-7782f9a20e](../../deaths/D-7782f9a20ec69cb2087d5ffc3d897b71051828b6cd9399dfe0dbe90bdcb4aef7/) | Human Ranger, CL1 DL1 | a large kobold | 6,911 | flight, other arm dies differently |
| [D-4427f8d5e1](../../deaths/D-4427f8d5e1bb9c7adaf5327d62f1f32717e537b9625ec6c5015a37a242728de1/) | Half-Orc Ranger, CL2 DL1 | Sméagol | 12,281 | same in both |
| [D-d257b2a471](../../deaths/D-d257b2a47157c9578ac22db8910ed06d014e741a0b91b833db7e47173731d9f9/) | Half-Elf Mage, CL2 DL1 | a cutpurse | 15,076 | flight only |
| [D-b5de2cd5da](../../deaths/D-b5de2cd5da1f523fdcbaf61b022b0cc13ae7282cd1c4601128f3ac513d9adb7a/) | Hobbit Priest, CL3 DL1 | Fang, Farmer Maggot's Dog | 15,135 | ctl only |
| [D-48dad39005](../../deaths/D-48dad39005b695e64239bf8f67c748f49e3174628292cb0a576a7b41dd2f4cac/) | Human Ranger, CL3 DL1 | poison | 15,810 | flight only |
| [D-aef5c3e05a](../../deaths/D-aef5c3e05a9447e366f23f2136af72adc96ece5f00cec14a56e6d513793aca4e/) | Elf Mage, CL3 DL1 | a fatal wound | 19,360 | same in both |
| [D-95b5e0084c](../../deaths/D-95b5e0084cc0beecfcd71bbdd2694e025005d94e2db4dd10aea3404e7e8cafba/) | Half-Elf Paladin, CL3 DL0 | poison | 44,090 | flight only |
| [D-ad1bde345e](../../deaths/D-ad1bde345ed08014c61025dfeaaa95c45c2503fba612adbb51d88670537002d9/) | Hobbit Paladin, CL4 DL2 | a wild cat | 45,585 | ctl only |
| [D-5a494c5be1](../../deaths/D-5a494c5be11353382590b2d0af92832c0a8c1bb14175de602d418952b5398fa7/) | Half-Troll Ranger, CL5 DL1 | a grey mold | 61,850 | same in both |
| [D-7a8b9fc3a6](../../deaths/D-7a8b9fc3a68994b3efc5571c1d6a8b3caa8458da1de5c4e031873f13cc6dcf75/) | Half-Orc Warrior, CL6 DL3 | a yellow jelly | 68,399 | flight only |
| [D-4c54abc984](../../deaths/D-4c54abc98478fbad0d6dd68fa0ac98bade09d5152452b824e0465d7b88f48d73/) | Human Priest, CL6 DL1 | a white worm mass | 72,283 | ctl only |
| [D-5def5b1735](../../deaths/D-5def5b1735ec23b39d973fea82ddaf60ac10a19cda705214df4999b6c8195911/) | Elf Ranger, CL9 DL3 | a giant white louse | 99,599 | flight only |

## Observations
- **Two of the six flight-only deaths** are "Desperate for Stairs (three)" walks with the killer next to the Borg: Necromancer 93034700 and Mage 247597266.
- **The other four flight-only deaths:**
  - Warrior 1653223723: Phase Door is forbidden, and it has 24 Cure Light Wounds in the pack.
  - Paladin 1584060551: dies of poison in town with no cures left.
  - Ranger 526144893: dies of poison on DL1 with no cures left, looking for an up-stair.
  - Ranger 956247604: killed by breeding lice at CL9.
- **Verdict:** neutral (4 rescued, 6 newly killed). Details on borg-zoo#501.

Play them: `~/borg-play/flight-fixes` (`./play.sh NAME --to TURN` is the exact game).


## Replay inputs

`replay/1653223723/` (the Warrior with the anti-teleportation robe, borg-reborn-rs#829) replays exactly without the zoo artifacts: `runs/replay-zoo-death.sh runs/2026-11-20-reborn-flight-fixes/replay/1653223723`.
