# Zoo deaths: reborn-p8-exploration-medium, run 45456422005

The natural deaths of borg-zoo run [45456422005](https://github.com/diegoami/borg-zoo/actions/runs/45456422005), imported by `scripts/import_zoo_deaths.py` (borg-zoo#176). 2 of 2 deaths have a dossier. Every dossier was replayed in the zoo with full logs, and its key stream matched the cell's. A repeat is a death the cemetery already had.

| Dossier | Profile | Seed | Character | Cause | Turn | Level | Depth (max) | Import |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| [D-6285ed1d8a9b](../../deaths/D-6285ed1d8a9b9e4d08463a924343ff7e24f451bef8c4d1603e824012008c0b74/README.md) | reborn-p8-exploration-bfs0 | 480049625 | Dunadan Warrior | a giant white mouse | 12925 | 2 | 1 (2) | exported |
| [D-1452ffaf78df](../../deaths/D-1452ffaf78df734b2b396153fc528f5f5935667514a28ac3bf2f51a5af9332ba/README.md) | reborn-p8-exploration-bfs0 | 1125613689 | High-Elf Ranger | a soldier | 10108 | 2 | 1 (1) | exported |

Each dossier's REPLAY.md has the build, watch and rerun commands. A replay and its original are one life, not two samples.

## Diagnosis

The investigation covers the normal-world medium tier on [`c5501d3c`](https://github.com/diegoami/borg-reborn-rs/commit/c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894). The [interactive report](bfs0-medium.html) contains the last 50 changed screens for each death. Download the HTML and open it in a browser to use the viewer. [Zoo run](https://diegoami.github.io/borg-zoo/runs/reborn-p8-exploration-medium/45456422005-1/index.html)

### The first split was in the General Store

At turn 421 for the Ranger (key 101) and turn 441 for the Warrior (key 96), the breadth-first-off arm left after buying three torches. Both breadth-first-on arms bought two more. The breadth-first flag also controls the early food and light multiplier. The first divergence therefore predates a dungeon routing decision. Both Borgs still had light when they died, and these pairs cannot isolate the effects of shopping, exploration order or the encounters those changes created. [Supply gate and fuel goal](https://github.com/diegoami/borg-reborn-rs/blob/c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894/borg-core/src/borg_flow_dark.rs#L875-L898)

### Warrior 480049625

At turn 12,857 an apprentice confused the Warrior at 8/30 HP beside mice. The combat gate estimated danger 2 without regional fear and declined Phase Door at 8 HP, 6 HP and 4 HP. At 2 HP the combat gate allowed it, but the emergency landing check rated 100/100 samples scary, above its 75/100 limit. The later vetoes also reported 100/100, without the never-seen-grid flag in the messages. The Warrior had 16 Phase Door scrolls and no cure at death.

Neither stair search found a usable exit. The last seven decisions selected `boost_bravery_2`, with the notes showing repeated attempts to move through the mouse or a closed grid. While confused, some attacks or movements hit a wall or spun in place. The last action was a move at 0 HP, followed by a fatal bite. The immediate chain was confusion, failed escapes and an increasingly desperate movement fallback. [Bravery decision](https://github.com/diegoami/borg-reborn-rs/blob/c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894/borg-core/src/borg_think_dungeon.rs#L1747-L1780)

Both paired controls survived and reached CL6. The shipped arm reached CL5 at turn 71,529 and mixed-off at 53,854.

### Ranger 1125613689

The Ranger met a soldier while routing to the up stairs. At turn 9,834, the combat gate allowed Phase Door at full HP, 25/25. The landing check rejected it because 92/100 samples were scary against a 75/100 limit, with 91 never seen. The emergency and critical checks continued to refuse it through 13/25 HP. Four melee attempts, three hits and a miss, preceded the first accepted Phase Door at 6/25 HP on turn 9,858.

The Ranger used its three scrolls at 9,858, 10,008 and 10,069. After the last jump at 5 HP, it took one exploration step and switched back to the any-stair flow. At turn 10,099 it saw a soldier two steps away, estimated current danger as zero and stepped south. Two blows killed it at 10,108. The final pack held two Cure Light Wounds and 25 arrows. No cure was quaffed in the run. The final move had no healing action in the trace, and the trace does not expose every earlier heal rejection. Earlier unknown-grid refusal is directly evidenced. The final step used a stair flow at low HP after escape stock ran out. [Phase landing assessment](https://github.com/diegoami/borg-reborn-rs/blob/c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894/borg-core/src/borg_escape.rs#L1431-L1467) · [Any-stair flow](https://github.com/diegoami/borg-reborn-rs/blob/c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894/borg-core/src/borg_think_dungeon.rs#L1288-L1301)

Both Ranger controls survived to the cap with identical keys and reached CL4.

## Replay verification

All six paths replayed from birth with the original Actions binary (SHA-256 `58780f2a4e89eb35fed77f2e792394a54ead5383005449700e23f0d1c262126d`) and each arm's hash-checked archived configuration. All six key hashes matched the Zoo cells. The two exact deaths also matched the downloaded bundles' message and state hashes. The recordings and X11 play pack independently matched the two death key hashes.

| Seed | Arm | Outcome | Key SHA-256 |
| --- | --- | --- | --- |
| 480049625 | shipped | turn_cap | `97fde550301b131d28d5880d9053f7b18592bd77182520cb06e3979c70b1d115` |
| 1125613689 | shipped | turn_cap | `46b101de811a68fb91f3cb5a3572a17dc482e4197eaa1603c4ed0939aa99bf2a` |
| 480049625 | bfs0 | death | `7dcf9d22771dd19e2be89dcad8ef5382e83fca17089a7f4d39d609758a353d64` |
| 1125613689 | bfs0 | death | `511bd6ce18c4337e8fc333e71971d25aa1048e4025b37c7956ea4d3eb66fd8d1` |
| 480049625 | nomixed | turn_cap | `37766e5a84b158c89c9c63bc1c6ddde343a6e80ee821b05a34f4ed93c77dc397` |
| 1125613689 | nomixed | turn_cap | `46b101de811a68fb91f3cb5a3572a17dc482e4197eaa1603c4ed0939aa99bf2a` |
