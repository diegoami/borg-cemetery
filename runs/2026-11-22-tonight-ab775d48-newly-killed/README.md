# The 22 starts that died on main ab775d48 and not on ed52fec1

Source: borg-zoo#609 (tonight's test of borg-reborn-rs main `ab775d48`, shipped settings, classes-1800, 100,000 turns), runs 44944038357 (medium), 44944061084 (big), 44944083365 (full). Selection: the starts dead on `ab775d48` that reach the cap on `ed52fec1` (borg-zoo#601). Every death replays from birth with keys matching the zoo cell; dossiers exported with `scripts/import_zoo_deaths.py`.

Report with each death's last 50 screens: https://claude.ai/artifact/UEdmGqyAecu3M3qGtJR9Yi
Play pack: `~/borg-play/main-ab775d48-newly-killed` (`./play.sh`).

| character | seed | killer | CL | DL | turn | dossier | zoo run |
|---|---:|---|---:|---:|---:|---|---|
| Dunadan Blackguard | 2064233389 | a soldier | 5 | 1 | 90681 | [D-37aa5edfd2b3](../../deaths/D-37aa5edfd2b3861eb71bbf59475be9de0573138cfd2332ee87a6771b5eb93e23) | 44944061084 |
| Dunadan Mage | 2017596150 | a soldier | 5 | 2 | 95866 | [D-b259d40a7193](../../deaths/D-b259d40a71939f3ecc121928c40b91e5dcceba5a1b567ebe1f3ba661c9f26edc) | 44944038357 |
| Dunadan Necromancer | 1203232169 | a fatal wound | 2 | 1 | 2860 | [D-7c24ebf5da80](../../deaths/D-7c24ebf5da805948b48249749ca86b54587ce8178cfc9f52c225670c5f912392) | 44944061084 |
| Dunadan Necromancer | 1928291203 | Grip, Farmer Maggot's Dog | 1 | 1 | 3575 | [D-676d39d85a86](../../deaths/D-676d39d85a865320b22c8418897e03efdf53553c6516c669ab984bab915318c4) | 44944083365 |
| Elf Blackguard | 1965910635 | a scrawny cat | 3 | 0 | 64969 | [D-9d573f3b704f](../../deaths/D-9d573f3b704fb5405b4aa0d357e624d0737152b8ac6670985dc973ed4cc8c940) | 44944083365 |
| Elf Priest | 1986973337 | a giant white louse | 6 | 2 | 61732 | [D-0180b56fa3be](../../deaths/D-0180b56fa3be368f99b7e843ce84f5df596db90f1b55d7eceaccf3404b0510f2) | 44944083365 |
| Gnome Necromancer | 1570385859 | a small kobold | 1 | 1 | 2455 | [D-dcefeeb9106a](../../deaths/D-dcefeeb9106adfa738b0e6ccbef5b947f195fc440fccbb13fc47830151451543) | 44944083365 |
| Half-Elf Mage | 267877625 | a Quarterstaff | 2 | 1 | 12400 | [D-17c7ca04ca39](../../deaths/D-17c7ca04ca39b0bc9c4649fffb86ed7115a14441f37ff195f39bc122f6c693b1) | 44944083365 |
| Half-Orc Necromancer | 881186109 | a soldier | 2 | 1 | 4372 | [D-5f2e8f8af3e5](../../deaths/D-5f2e8f8af3e575d75d59daf8d3ce5c72ff7c1c80576db33b98512b211b5f9849) | 44944083365 |
| Half-Troll Druid | 1291190486 | a crow | 1 | 1 | 1909 | [D-684512063273](../../deaths/D-68451206327306a226f865b5ca742a30199b2273b2057cb617cac1453f6b4cbe) | 44944083365 |
| High-Elf Blackguard | 1987427386 | a giant white louse | 12 | 3 | 87152 | [D-e6951115fe49](../../deaths/D-e6951115fe4907b3d6781907a96d65cd3c81f2124595173026abc0a9cb63aa67) | 44944061084 |
| Hobbit Necromancer | 1425433569 | a soldier | 6 | 2 | 89922 | [D-3ce8d44c5d3f](../../deaths/D-3ce8d44c5d3fb1159918a45de33deea27e5f4be6ab0b483994bfed944c16d671) | 44944083365 |
| Hobbit Paladin | 832354864 | a crow | 5 | 2 | 74978 | [D-d8994727bb97](../../deaths/D-d8994727bb9706c4db6692fe541114287e1a4e7946c8ace2ce48034414eb9a2b) | 44944061084 |
| Hobbit Paladin | 2123511101 | a crow | 4 | 2 | 46842 | [D-61f148407fbf](../../deaths/D-61f148407fbfa561f5534ea6e69c6a41d384fc09d6baca6c7997fc27d6339658) | 44944083365 |
| Hobbit Warrior | 1972332898 | a crow | 4 | 2 | 6297 | [D-9c429943b153](../../deaths/D-9c429943b1530142b64716476b717c57dc929607c5e1ab75d2bce7ada89d2eba) | 44944061084 |
| Human Druid | 1674396030 | a crow | 2 | 1 | 10205 | [D-262d366ec8fd](../../deaths/D-262d366ec8fd14ec0eaf1193285f8fe49d28db3ab8ab45f1525223ca91734dac) | 44944061084 |
| Human Paladin | 864942296 | a giant white louse | 9 | 3 | 73179 | [D-367e4c36b93f](../../deaths/D-367e4c36b93f16dca3d60e6136a3f18ba00073cfaceb6be11d0a9524fda79b9d) | 44944061084 |
| Human Ranger | 2046073961 | a cave spider | 6 | 3 | 56300 | [D-33369edf63dc](../../deaths/D-33369edf63dc3e5ed2e15fe3beb171bf1f4d730cae6c1962b7f783864d2b204f) | 44944083365 |
| Human Rogue | 248464194 | a cave spider | 5 | 1 | 25350 | [D-07d910154ace](../../deaths/D-07d910154aced7f33d3493064acb942f764bd33c015b80d4b02f9ed0eeab1465) | 44944083365 |
| Kobold Druid | 653243095 | a scrawny cat | 6 | 0 | 77418 | [D-3734fe452121](../../deaths/D-3734fe4521214832e6fe58a21c07ffec76d9b72a79d999edb70156bb0a7fff1c) | 44944083365 |
| Kobold Druid | 2128748366 | a crow | 5 | 1 | 51029 | [D-45fecae48412](../../deaths/D-45fecae48412bd22faf6444c7cd017052dae12540acc4c79808884013bdf63df) | 44944083365 |
| Kobold Mage | 383215433 | a cave spider | 4 | 1 | 14124 | [D-26d4a841a1a5](../../deaths/D-26d4a841a1a5fa6cbd2cdcce6bec5bf439b2415773ad16d375f4beda8686fa17) | 44944061084 |

## Observations (counted from the replays)

- Two deaths are a curse-removal loop: Elf Blackguard 1965910635 (1,422 take-offs and re-wields of a paralysis-cursed Wooden Torch from turn 43,382) and Kobold Druid 653243095 (367 from turn 71,694), both killed in town by a scrawny cat. The code (`borg_cursed.rs`, #830/#832) is in `ab775d48`, not in `ed52fec1`.
- 13 of 22 died holding Cure potions (2 to 24), 14 holding Phase Door, 6 neither.
- Desperate walk to the stairs ("Desperate for Stairs (three)") with a soldier adjacent and a full pack: Necromancer 1425433569; the note also appears in the last lines of 2017596150 and 1570385859.
