# The poison deaths of breadth-first on and off (trackp 1c071812)

Source: borg-zoo#730, run [45121432449](https://github.com/diegoami/borg-zoo/actions/runs/45121432449): borg-reborn-rs trackp `1c071812`, arms `ctl` (shipped, `explore_breadth_first 1`) and `bfs0` (`explore_breadth_first 0`), classes-1800 full slice, 900 starts each, 100,000 turns. All 25 deaths were replayed from birth (keys match the zoo cells'); the dossiers are in [zoo-reborn-bfs-full-45121432449](../zoo-reborn-bfs-full-45121432449/README.md). This page lists the 7 poison deaths, the leading killer.

Report with each death's last recorded screens: https://claude.ai/artifact/VWWQhyKLZZbvoBxuHUStGm
Play pack: `~/borg-play/bfs-full` (`./play.sh`).

| character | arm | seed | CL | DL | turn | dossier |
|---|---|---:|---:|---:|---:|---|
| Half-Elf Rogue | ctl | 626789725 | 3 | 1 | 27480 | [D-f083a7ec7262](../../deaths/D-f083a7ec7262f16659812e93c3244c2fbf003692a1534257c4a1f4f3ef9adb28/README.md) |
| Dunadan Druid | bfs0 | 727698927 | 7 | 2 | 62100 | [D-99b8f510ae77](../../deaths/D-99b8f510ae778b2f00afd83ab8c6e0a4aaf8a8957eedab21decfc1c64523e671/README.md) |
| Elf Druid | ctl | 799968561 | 4 | 0 | 22600 | [D-b6fe508ca729](../../deaths/D-b6fe508ca7292964767801be5242caa48b73e1fd1704cf325642e0ad18e69452/README.md) |
| Elf Ranger | ctl | 956247604 | 5 | 1 | 88060 | [D-d6ef4a57e25c](../../deaths/D-d6ef4a57e25cb18d0680d581c8ad2c0f57dfb4b91222a5eaf7cc0405c188ef5b/README.md) |
| Half-Elf Paladin | bfs0 | 1200156945 | 6 | 2 | 92070 | [D-4f6abb6a2c4e](../../deaths/D-4f6abb6a2c4e1e330002b1fe2bd7f506b519979c09580cfff376f0c9624d1823/README.md) |
| Elf Druid | ctl | 1575381233 | 7 | 1 | 92040 | [D-16f76a5925f5](../../deaths/D-16f76a5925f56292559a3fe58cda1670c6c28b9b133c482c5b4a03ce695059bb/README.md) |
| Human Druid | bfs0 | 1902932078 | 7 | 1 | 53110 | [D-5b75993e7f46](../../deaths/D-5b75993e7f467ea4f695e6bd87bea72728e146157557a877e00deb50653ec751/README.md) |
## Observations

- In this engine only Cure Critical Wounds, Neutralize Poison, Healing and better cure poison (`object.txt`); Cure Light and Cure Serious Wounds heal HP only. None of the 7 drank a poison cure. While poisoned, four drank Cure Light Wounds instead (the Elf Druid 11, the Elf Ranger 6, the Dunadan Druid 5, the Rogue 3 and one Cure Serious Wounds).
- 5 of the 7 were poisoned while meleeing a white jelly (3) or a white worm mass (2); the scary list has white jelly as `ranged | poison-touch`. The other 2 were crawled on by a blubbering icky thing.
- In 4 of the 7, Word of Recall was refused with the poison in the forecast (`Flight Recall forecast: 34 poison HP included (#880)`, then `Refusing flight Recall ... (#758)`), and the Borg walked to the stairs.
- The Elf Druid 799968561 died of poison in town, while its town plan sold and dropped items.
- Six of the 7 died with no healing or curing potion left; the Half-Elf Paladin 1200156945 died with 2 Neutralize Poison and 10 Cure Light Wounds, unused.
- Deaths per arm: ctl 13, bfs0 12, one start dying in both (exact McNemar p = 1.0).
