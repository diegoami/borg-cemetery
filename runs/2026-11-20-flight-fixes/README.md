# Every death of the flight-fixes runs (borg-zoo#501)

- **Source:** borg-zoo#501, four runs of borg-reborn-rs `e8b3acfd` (the flight fixes) against its control, engine 574b618c, 100,000 turns:
  - `reborn-flight-fixes-pilot` run [44737523620](https://github.com/diegoami/borg-zoo/actions/runs/44737523620): ctl 1, flight 0 deaths;
  - `reborn-flight-fixes-rangers` run [44738419997](https://github.com/diegoami/borg-zoo/actions/runs/44738419997) (the 200 classes-1800 Ranger starts): ctl 9, flight 10;
  - `reborn-flight-fixes-small` run [44738432656](https://github.com/diegoami/borg-zoo/actions/runs/44738432656): ctl 0, flight 2;
  - `reborn-flight-fixes-medium` run [44738444831](https://github.com/diegoami/borg-zoo/actions/runs/44738444831): ctl 5, flight 4.
- **Selection:** every death in every arm, at the owner's request ("I would want to see all deaths in this run"). The 31 dossiers below come from 22 distinct games:
  - 7 games are byte-identical in both arms (the same keys), so the fixes never acted in them;
  - seed 1439525086 (a Ranger, killed by Sméagol) is in both the Ranger and the medium suite, and is the same game in all four cells.
  - Every dossier was replayed in the zoo with full logs, and its key stream matches the cell's.
- **Report with the last 50 recorded screens of each of the 22 games:** https://claude.ai/artifact/SnqujSa3vHiJUebG9hLu87

| dossier | run | arm | seed | character | killed by | CL | game turn | arrows at death | last attack |
|---|---|---|---:|---|---|---:|---:|---:|---|
| [D-e74bce649ff4](../../deaths/D-e74bce649ff4e7ffa1df68f1c5d10f4185542f23b3eb443ef9a4aede1b6d4dd4/README.md) | rangers | ctl | 807683971 | Human Ranger | a black naga | 1 | 1,534 | 74 | melee |
| [D-699216fe94cf](../../deaths/D-699216fe94cfe9f2964604f15f68e3ce40fc6bc96f497cd32692240e2ff03a43/README.md) | medium | flight | 93034700 | Elf Necromancer | an apprentice | 1 | 2,147 | – | melee |
| [D-9170afbd5468](../../deaths/D-9170afbd546818293fe7e8038b67a371885afd44e0faa1c724d852adfb6ac25b/README.md) | rangers | flight | 2095979189 | Half-Orc Ranger | a wild cat | 1 | 3,326 | 80 | shot |
| [D-5cb784c6ad20](../../deaths/D-5cb784c6ad20e5a158f78913be73bb4df46e2e966971bcc6e84d4b0eece90f08/README.md) | rangers | ctl | 2095979189 | Half-Orc Ranger | a wild cat | 1 | 3,345 | 80 | melee |
| [D-5ceb347a93e9](../../deaths/D-5ceb347a93e900b15d79a1b3883da6efc29c682a2657d5265716124e24671663/README.md) | rangers | ctl | 425904011 | Elf Ranger | a wild cat | 1 | 3,660 | 72 | melee |
| [D-e98ac4d9c565](../../deaths/D-e98ac4d9c56582b53f119875cae932b217877d732e2e5b554758e160f49a4c26/README.md) | rangers | flight | 425904011 | Elf Ranger | a wild cat | 1 | 3,660 | 72 | melee |
| [D-8f67a91ceadd](../../deaths/D-8f67a91ceadddd2328e35e62f8dad2ac490cf92560a6ecdf9fce2a67312ebaa3/README.md) | rangers | ctl | 1976035382 | Dunadan Ranger | a wild cat | 1 | 4,248 | 73 | melee |
| [D-4547c20ea2ef](../../deaths/D-4547c20ea2ef65ef88ceb1cdc2f4a80b6d9cabe6cd562e977f46846a8b73d436/README.md) | rangers | flight | 1976035382 | Dunadan Ranger | a wild cat | 1 | 4,248 | 73 | melee |
| [D-e0377024753c](../../deaths/D-e0377024753cf0efe981830a0f4b481f3b2d4d25b5e84598858dbde9aa698f53/README.md) | rangers | ctl | 2049259432 | Gnome Ranger | Fang, Farmer Maggot's Dog | 1 | 4,429 | 70 | shot |
| [D-4225067b3ed3](../../deaths/D-4225067b3ed3d3ec77c901b629f3064c94c0ac7c62b534fd206ab176f5d0722f/README.md) | rangers | flight | 2049259432 | Gnome Ranger | Fang, Farmer Maggot's Dog | 1 | 4,429 | 70 | shot |
| [D-ec213c6be10e](../../deaths/D-ec213c6be10e7ca4cb48d033d6fcccf8cd0c63dcf02f1e1053252d97c5bc59ed/README.md) | rangers | ctl | 225452245 | Half-Orc Ranger | a kobold shaman | 4 | 5,647 | 64 | melee |
| [D-b4089d61abea](../../deaths/D-b4089d61abea685dd3badc939cbde14db973d6322b0258d441671cd6ba50f5fc/README.md) | rangers | ctl | 1517990203 | Gnome Ranger | a small kobold | 1 | 6,338 | 58 | melee |
| [D-2abb98b72353](../../deaths/D-2abb98b723539deb468ee5c679d0c43e79b4734d926ca9d5dfc5a34ac4315bed/README.md) | rangers | flight | 1517990203 | Gnome Ranger | a small kobold | 1 | 6,338 | 58 | melee |
| [D-7782f9a20ec6](../../deaths/D-7782f9a20ec69cb2087d5ffc3d897b71051828b6cd9399dfe0dbe90bdcb4aef7/README.md) | rangers | flight | 807683971 | Human Ranger | a large kobold | 1 | 6,911 | 62 | melee |
| [D-4427f8d5e1bb](../../deaths/D-4427f8d5e1bb9c7adaf5327d62f1f32717e537b9625ec6c5015a37a242728de1/README.md) | rangers | ctl | 1439525086 | Half-Orc Ranger | Sméagol | 2 | 12,281 | 24 | melee |
| [D-4427f8d5e1bb](../../deaths/D-4427f8d5e1bb9c7adaf5327d62f1f32717e537b9625ec6c5015a37a242728de1/README.md) | medium | ctl | 1439525086 | Half-Orc Ranger | Sméagol | 2 | 12,281 | 24 | melee |
| [D-ed2689a734c2](../../deaths/D-ed2689a734c2df78fd6978421ad5574cc13b9d4678cf2e8f29debb015e957d50/README.md) | rangers | flight | 1439525086 | Half-Orc Ranger | Sméagol | 2 | 12,281 | 24 | melee |
| [D-ed2689a734c2](../../deaths/D-ed2689a734c2df78fd6978421ad5574cc13b9d4678cf2e8f29debb015e957d50/README.md) | medium | flight | 1439525086 | Half-Orc Ranger | Sméagol | 2 | 12,281 | 24 | melee |
| [D-d257b2a47157](../../deaths/D-d257b2a47157c9578ac22db8910ed06d014e741a0b91b833db7e47173731d9f9/README.md) | small | flight | 247597266 | Half-Elf Mage | a cutpurse | 2 | 15,076 | – | spell |
| [D-b5de2cd5da1f](../../deaths/D-b5de2cd5da1f523fdcbaf61b022b0cc13ae7282cd1c4601128f3ac513d9adb7a/README.md) | medium | ctl | 1870400446 | Hobbit Priest | Fang, Farmer Maggot's Dog | 3 | 15,135 | – | melee |
| [D-48dad39005b6](../../deaths/D-48dad39005b695e64239bf8f67c748f49e3174628292cb0a576a7b41dd2f4cac/README.md) | rangers | flight | 526144893 | Human Ranger | poison | 3 | 15,810 | 99 | shot |
| [D-aef5c3e05a94](../../deaths/D-aef5c3e05a9447e366f23f2136af72adc96ece5f00cec14a56e6d513793aca4e/README.md) | medium | ctl | 912444426 | Elf Mage | a fatal wound | 3 | 19,360 | – | spell |
| [D-5ca6470a0c43](../../deaths/D-5ca6470a0c43b838d55e207b38c2312d592436b22c0e15d904526688e95ca1a7/README.md) | medium | flight | 912444426 | Elf Mage | a fatal wound | 3 | 19,360 | – | spell |
| [D-f74e3c4476af](../../deaths/D-f74e3c4476afb6174df9c5f660d206e5864aa1f46d7ec6a8b2a9fe34df195a62/README.md) | pilot | ctl | 102023799 | Human Druid | a clear icky thing | 4 | 37,759 | – | throw |
| [D-95b5e0084cc0](../../deaths/D-95b5e0084cc0beecfcd71bbdd2694e025005d94e2db4dd10aea3404e7e8cafba/README.md) | small | flight | 1584060551 | Half-Elf Paladin | poison | 3 | 44,090 | – | throw |
| [D-ad1bde345ed0](../../deaths/D-ad1bde345ed08014c61025dfeaaa95c45c2503fba612adbb51d88670537002d9/README.md) | medium | ctl | 1777269782 | Hobbit Paladin | a wild cat | 4 | 45,585 | – | melee |
| [D-5a494c5be113](../../deaths/D-5a494c5be11353382590b2d0af92832c0a8c1bb14175de602d418952b5398fa7/README.md) | rangers | ctl | 214960633 | Half-Troll Ranger | a grey mold | 5 | 61,850 | 24 | shot |
| [D-96f16297bf24](../../deaths/D-96f16297bf2491bfcc2f0a4fb3afb2b0f770e075edd65cc94a86d32e30948ff9/README.md) | rangers | flight | 214960633 | Half-Troll Ranger | a grey mold | 5 | 61,850 | 24 | shot |
| [D-7a8b9fc3a689](../../deaths/D-7a8b9fc3a68994b3efc5571c1d6a8b3caa8458da1de5c4e031873f13cc6dcf75/README.md) | medium | flight | 1653223723 | Half-Orc Warrior | a yellow jelly | 6 | 68,399 | – | throw |
| [D-4c54abc98478](../../deaths/D-4c54abc98478fbad0d6dd68fa0ac98bade09d5152452b824e0465d7b88f48d73/README.md) | medium | ctl | 809881907 | Human Priest | a white worm mass | 6 | 72,283 | – | melee |
| [D-5def5b1735ec](../../deaths/D-5def5b1735ec23b39d973fea82ddaf60ac10a19cda705214df4999b6c8195911/README.md) | rangers | flight | 956247604 | Elf Ranger | a giant white louse | 9 | 99,599 | 0 | melee |

## What the deaths show (from messages.log and the recordings; observations, not a diagnosis)
- **Rangers are 13 of the 22 games** (11 seeds). 8 of the 13 die at CL1 on DL1 before game turn 7,000. Their killers are wild cats (4), a black naga, a large kobold, a small kobold and Fang.
- **The same deaths as main fde8025a:** 8 of the 11 Ranger seeds died on [main fde8025a](../2026-11-20-reborn-fde8-rangers/README.md) to the same killer at the same game turn. In these games the flight fixes changed nothing.
- **None ran out of arrows.** The CL1 Rangers had 58-80 arrows at death. They shoot at range, then switch to the Main Gauche once the monster is adjacent. The last attack was melee in 6 of the 8 CL1 deaths.
  - "Fleeing and leaving the level (scaryguy)" is followed in the same game turn by "Performing attack type 1" (melee), e.g. 425904011 and 1976035382.
  - In 425904011, the Ranger read its last Word of Recall with the wild cat adjacent and 3 cure potions in the pack, and died 10 game turns later.
  - Arrows at point-blank range are halved for Rangers (`attack_arrow_point_blank_divisor_ranger = 2`), but borg-zoo#379 found divisor 1 worse.
- **The other 9 games:**
  - two Priests: Fang at CL3, a white worm mass at CL6;
  - two Paladins: a wild cat, poison;
  - two Mages: a cutpurse, a fatal wound;
  - a Druid: a clear icky thing;
  - a Necromancer: an apprentice, at CL1;
  - a Warrior: a yellow jelly, at CL6 on DL3.

## Playing them
`~/borg-play/flight-501` on the owner's machine holds these 22 games. That folder isn't part of this repository. It was built from these bundles:
- an X11 build of e8b3acfd (`BORG_X11=ON`);
- per death, the arm's borg.txt and scary list, plus the zoo's keys, messages and state logs;
- saves at about 3,000, 1,000 and 300 game turns before the death, and one just before it.

Every save was cut after a full replay with that build matched the zoo run's play hash. `./play.sh NAME --to TURN` replays the exact game.
