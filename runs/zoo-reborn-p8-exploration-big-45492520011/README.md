# Zoo deaths: reborn-p8-exploration-big, run 45492520011

The natural deaths of borg-zoo run [45492520011](https://github.com/diegoami/borg-zoo/actions/runs/45492520011), imported by `scripts/import_zoo_deaths.py` (borg-zoo#176). 6 of 6 deaths have a dossier. Every dossier was replayed in the zoo with full logs, and its key stream matched the cell's. A repeat is a death the cemetery already had.

| Dossier | Profile | Seed | Character | Cause | Turn | Level | Depth (max) | Import |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| [D-9781f2081e7b](../../deaths/D-9781f2081e7bab24d44769cb29c4948dbfb760d66ea4d8d1efcfe425134a2b7f/README.md) | reborn-p8-exploration-bfs0 | 813826708 | Hobbit Ranger | a grey mushroom patch | 22933 | 3 | 1 (1) | exported |
| [D-159a5b611bc2](../../deaths/D-159a5b611bc2f2822a4852268424d4611e2f6d6c8373ea00934a98d007a55e01/README.md) | reborn-p8-exploration-bfs0 | 1386870371 | Half-Troll Necromancer | a scout | 11689 | 2 | 1 (1) | exported |
| [D-6668ca522502](../../deaths/D-6668ca5225024fc58a17dd1697f2b67a59e4c0365c8b0f57730d8a412d238966/README.md) | reborn-p8-exploration-nomixed | 1179277706 | Gnome Druid | a soldier | 51287 | 4 | 1 (1) | exported |
| [D-4493a7ffa646](../../deaths/D-4493a7ffa646a4e9d655b763dd03f428a04837528f7189e0b1268ad2b94dc838/README.md) | reborn-p8-exploration-nomixed | 1925085453 | Elf Rogue | a cutpurse | 25590 | 4 | 1 (2) | exported |
| [D-c517f4b4a156](../../deaths/D-c517f4b4a15614c8f22f7c98f02353f9d0ed243695c5d24739780f7b4b7fc8ab/README.md) | reborn-p8-exploration-shipped | 1179277706 | Gnome Druid | a soldier | 51287 | 4 | 1 (1) | exported |
| [D-249ee0097ba8](../../deaths/D-249ee0097ba8262a347ee54b69ab217667feafa07b4a32bd486321fa40aaa836/README.md) | reborn-p8-exploration-shipped | 1925085453 | Elf Rogue | a cutpurse | 25590 | 4 | 1 (2) | exported |

Each dossier's REPLAY.md has the build, watch and rerun commands. A replay and its original are one life, not two samples.

[The full P8 exploration death report](../2026-11-25-p8-exploration/README.md) covers both tiers and links the six interactive replays.

## Observations

- **Half-Troll Necromancer, 1386870371.** It began a five-step up-stair flow at turn 11,641. The scout hasted at 11,648. The Borg switched to one-step retreats while the scout closed and fired, losing 18 HP before reaching the stairs. Six Phase Door scrolls and six Cure Light Wounds remained.
- **Hobbit Ranger, 813826708.** It was confused three steps from the stairs. The grey mushroom patch reapplied confusion after both Cure Light Wounds, leaving the seven Phase Door scrolls unreadable. The Borg kept trying melee after it found no safe adjacent step.
- **Elf Rogue, 1925085453.** At 5 HP the landing check rejected Phase Door. A critical jump at 1 HP bought time. The next jump, at 2 HP, passed the check and the cutpurse hit on landing.
- **Gnome Druid, 1179277706.** The fight estimate favored a two-turn kill. The soldier’s tracked HP stayed at 23 after two oil throws, and the Druid’s HP fell from 26 to 8. It died to the soldier after casting Fox Form for a 17-step stair retreat, with 17 Phase Door scrolls and 12 Cure Light Wounds still in its pack.

The Rogue and Druid have separate dossiers for the shipped and mixed-off configurations. Their key hashes match across the two arms. Each distinct big-tier fatal key stream also matched a recorder replay from birth.
