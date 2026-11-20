# Borg dive gates, seeds 1–18

This local comparison measures main's shipped character-level depth cap
and the C Borg dive gates in the #768 candidate. Both builds used their own
shipped settings, the default borg-rs core, the same Angband engine
`574b618c3bfec595f3503a58f8e488b1c4ae3a46`, and harness menu births.
Seeds 1–9 are Human. Seeds 10–18 are Half-Elf. Each race plays all nine
classes in game order. Both turn caps were run independently from birth.

| Build | Source revision | Binary SHA-256 |
|---|---|---|
| main | `fec0f89dde74fb0b669ed8c0c8a1d1b55051a680` | `b6fc7fe301dfb79ccf9a11d8167886412bd9a9b9b81fff5f711b320838233a7f` |
| candidate | `103b50a4b7f6f8623b9c525478770e1cbb7d9193` | `b2a469fbcd1700259a9305748362b3098b40a93aeaf0308eb6f77ec2f2651e2a` |

| Turn cap | Build | Deaths | Highest max CL | Sum of max CL | Highest max DL | Sum of max DL |
|---:|---|---:|---:|---:|---:|---:|
| 100,000 | main | 0 | 8 | 115 | 4 | 41 |
| 100,000 | candidate | 2 | 9 | 117 | 5 | 47 |
| 200,000 | main | 0 | 12 | 153 | 6 | 59 |
| 200,000 | candidate | 2 | 12 | 150 | 7 | 61 |

The candidate changed 13 of 18 key streams at each cap. Main's final
timing report stopped at the missing `bc` command. All 36 baseline run
receipts exited zero, reported the requested start and reached the turn
cap. The executable digest matched the initial suite manifest.

## Natural deaths

- Human Priest, seed 4, was killed by an acolyte at turn 58,147 on DL2 at
  CL7. [Dossier](../../deaths/D-348b5e144f8463a089d02e8c6c07112b5d66b07e6b18ae976fc92e4a8bb0cc3f/)
- Human Blackguard, seed 9, was killed by a giant green frog at turn
  9,896 on DL2 at CL4. [Dossier](../../deaths/D-7cbb003e62e82491028c11cec6d12726fd6257c69ddae655005ed2f828039e20/)

Both deaths repeated with the same endpoint and identical keys, messages
and state streams at the two caps. Each pair represents one distinct start.

## Per-seed maxima

† marks a death.

| Seed | Race | Class | 100k main CL/DL | 100k PR CL/DL | 200k main CL/DL | 200k PR CL/DL |
|---:|---|---|---:|---:|---:|---:|
| 1 | Human | Warrior | 5/2 | 9/5 | 8/4 | 12/7 |
| 2 | Human | Mage | 6/2 | 6/2 | 7/2 | 7/2 |
| 3 | Human | Druid | 8/2 | 8/2 | 9/3 | 10/3 |
| 4 | Human | Priest | 7/2 | 7/2 † | 8/2 | 7/2 † |
| 5 | Human | Necromancer | 7/2 | 6/2 | 8/2 | 8/2 |
| 6 | Human | Paladin | 7/3 | 6/2 | 9/4 | 9/4 |
| 7 | Human | Rogue | 8/2 | 8/2 | 9/3 | 9/3 |
| 8 | Human | Ranger | 4/2 | 7/3 | 9/4 | 9/5 |
| 9 | Human | Blackguard | 7/2 | 4/2 † | 9/4 | 4/2 † |
| 10 | Half-Elf | Warrior | 8/4 | 8/4 | 12/6 | 12/6 |
| 11 | Half-Elf | Mage | 6/2 | 6/2 | 7/2 | 7/2 |
| 12 | Half-Elf | Druid | 6/2 | 7/2 | 8/3 | 9/3 |
| 13 | Half-Elf | Priest | 7/2 | 6/2 | 9/3 | 8/3 |
| 14 | Half-Elf | Necromancer | 7/3 | 6/3 | 8/3 | 7/3 |
| 15 | Half-Elf | Paladin | 5/2 | 6/3 | 9/5 | 8/3 |
| 16 | Half-Elf | Rogue | 6/3 | 6/3 | 8/3 | 8/3 |
| 17 | Half-Elf | Ranger | 6/2 | 6/3 | 7/2 | 7/3 |
| 18 | Half-Elf | Blackguard | 5/2 | 5/3 | 9/4 | 9/5 |

[Source PR](https://github.com/diegoami/borg-reborn-rs/pull/772)
