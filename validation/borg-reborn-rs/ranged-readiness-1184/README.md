# Ranged supply in the watched Human Paladin

This case supports [borg-reborn-rs #1184](https://github.com/diegoami/borg-reborn-rs/issues/1184). The two snapshots and the final recording cover one watched life, `Borg261124132707`, on Track P build `3c46575d`. The receipt and game-turn steps below come from the owner's [recording release](https://github.com/diegoami/angband-workspace/releases/tag/borg-1184-paladin-recording). Access to the original recordings requires the workspace repository. The final death has its own [incident record](../../../incidents/2026-11-24-watch-human-paladin-wormtongue-645892/README.md).

## Watched life

| Game turn | Observation |
| --- | --- |
| 2,069 | Bought 24 oil flasks for 72 gold. |
| 22,741 | Reached town with 417 gold and 3 flasks. A torch was equipped, the launcher slot and quiver were empty, and the pack used 13 of 23 slots. The observed learned prayers, Bless and Detect Evil, offered no ranged attack. |
| 23,031 | Bought four Detect Invisible scrolls for 60 gold, leaving 357. The planner then headed toward the General Store. Scary-monster flight interrupted the approach at 23,259 and the second approach at 23,609. The visit gives no General Store shelf snapshot, oil quote or oil score. The earlier 3-gold receipt establishes only the price at the original purchase. |
| 24,687–24,707 | Used the last two flasks against Fang. The last was spent at 24,707. |
| 57,300–58,641 | Picked up and later used one flask. First-snapshot traces through 156,423 contained no town-return or rising goal after 24,707. |
| 177,633–178,447 | Reached town and then bought 17 flasks for 51 gold. |
| 201,492 | Threw the last flask. |
| 204,994 | Picked up and equipped a Short Bow on DL3, with zero arrows. |
| 336,602–336,603 | First recorded arrows arrived from the dungeon, 27 enchanted arrows on DL4. The first shot hit a giant white ant. |
| 354,811 | First town arrival after equipping the bow. The Borg already had arrows. The final archive contains no arrow purchase. |

The first gap had two parts. The return to town produced one consumable purchase before scary-monster flight interrupted general shopping. After oil ran out, the Borg continued in the dungeon with no oil-specific town-return goal. In the second gap the launcher sat empty until the Borg found arrows, 131,608 game turns after equipping it. There was no town visit during that gap.

The initial archive SHA-256 is `cd4ba52e21463ff14396b2e5db74c0994d98f4e430df787dd4cbf245a7df9d05`. The final archive SHA-256 is `984e7df3b70934ca4b5d62ad979b463941dbddc1cb9a1a3d61094d010e8ba4ca`.

## Baseline mechanism checks

These checks were run at `3c46575d` and use independent or constructed starts. The natural torch Paladin ran out of oil at 17,025. At 17,113 the last observed shop had 40 flasks at 3 gold each, while the Borg held 2 gold. The trip trace marked `restock=false`. It later selected known up stairs at 23,178 on the existing unknown-depth condition, with zero Recall scrolls. With 262 gold in town and a remaining pack budget of 15 slots and 60.1 lb, it selected 22 flasks for 66 gold and departed with 22. When those ran out at 151,388, the remaining DL1–2 decisions had no rising goal. The funded three-flask torch start also selected 19 more flasks and left with 22.

The naturally born Ranger had another ranged source and bought 14 matching arrows for 14 gold, leaving the oil offer alone on the first trip. The low-purse constructed lantern start bought five flasks and left with three allocated to fuel and two available to throw. The funded constructed empty-bow Paladin saw 1-gold arrows and bought 26 oil flasks for 78 gold. It bought no arrows. These town checks isolate the mechanism and do not reconstruct the watched shop's unseen stock.

## Revised candidate and deterministic starts

The tested source commit is [ddc1c35aeb95d1e20809eb2ffb8f5a64d4a12b1c](https://github.com/diegoami/borg-reborn-rs/commit/ddc1c35aeb95d1e20809eb2ffb8f5a64d4a12b1c). Its Rust source SHA-256 is `74c613a2c34df56b0dc3e7d6daec0f5e565b0dcdc63b1a46a58c7b3a9e48b83e`. The engine is Angband `574b618c3bfec595f3503a58f8e488b1c4ae3a46` with the pinned repository integration. The build uses GCC's shipped right-to-left profile and the vendored borg-rs core.

- **Funded Short Bow Paladin.** Constructed Human Paladin birth at seed 1184. [The data patch](bow.patch) adds the empty bow and raises starting gold. Shopping bought six arrows for six gold at turn 91, before oil.
- **Lantern Paladin.** Constructed Human Paladin birth at seed 1184. [The data patch](lantern.patch) substitutes a lantern and raises starting gold. Shopping bought 8 and 25 flasks for 24 and 75 gold. At first dungeon entry the Borg carried 33 flasks, with 3 reserved for fuel and 30 counted for throwing. There were no arrow purchases.
- **Ranger.** Ordinary Human Ranger birth at seed 1184 using shipped game data. With both switches on, it bought 14 arrows for 14 gold at turn 809 and kept usable launcher ammo throughout the observed dungeon time.

The arms below start the same Human Paladin seed 302 and set the readiness trace in every arm. Elapsed game turns are weighted between readiness transitions at depths above zero, with the last state carried to the recorded endpoint. All four survived their 100,000-turn caps. This is one start.

| Arm | Dungeon turns without coverage | Dungeon turns | Share |
| --- | --- | --- | --- |
| Control | 46,145 | 92,591 | 49.8% |
| Shopping | 49,362 | 87,534 | 56.4% |
| Recovery | 38,309 | 92,645 | 41.4% |
| Both | 170 | 82,548 | 0.2% |

The shopping rule no longer makes the first cure or Phase Door urgent. Shopping and control both bought 22 oil on their first visit on seed 302. Buying the reserve in two transactions changed the timing of later decisions. The local comparison does not isolate which downstream decisions caused the difference in coverage. The population comparison is tracked at [borg-zoo #778](https://github.com/diegoami/borg-zoo/issues/778).

## Reproduction

Build the pinned repository with `BORG_IMPL=rust harness/build.sh`. From that source checkout, run [reproduce.sh](reproduce.sh) with a new output directory. The script uses the shipped profile and scary list, records the explicit parameter overrides, and stages the two data patches in isolated directories. These deterministic birth definitions supply the start state. The [trial manifest](manifest.json) and [purchase receipts](receipts.json) contain build and setting identities, endpoints, stream digests, and purchase receipts.

### Verified Track P merge

The [merged-candidate manifest](manifest-fa3f8590.json) records the runs at
`fa3f859041674028c0415b849577154e4f1fc9a9`, the commit pinned in the
Zoo request. The seven seeded cases and both Mage continuations reproduced
keys, messages, state, and readiness traces. The original manifest remains
the receipt for `ddc1c35a` and the new manifest records the new binary and
resolved parameter digests. For each Mage continuation it also gives the
exact save artifact, uncompressed hash, load mode, and turn cap.

Use a clean Git checkout of the candidate to verify its source hash with
`harness/identity.sh source-hash rust`. An archive initialized as a new
repository with an empty index skips the tracked
`engine/angband/lib/user/save/Makefile` because its directory is ignored
for untracked files. With that file indexed, the archive reproduces the
checkout hash.

### Candidate with the enabled settings

The [enabled-profile manifest](manifest-2daac373.json) records the four
Paladin arms, both Mage continuations, and the Druid regression at PR
head `2daac373`. This build includes the same-turn stair-scumming guard
triggered by the enabled profile. The original Druid run reached 1,290
queued keys on turn 5,981. The guarded run reached its 100,000-turn cap
alive and peaked at 30 keys on one turn.

| Paladin arm | Turns without range | Dungeon turns | Share |
| --- | ---: | ---: | ---: |
| Control | 47,015 | 91,568 | 51.3% |
| Shopping | 12,312 | 89,433 | 13.8% |
| Recovery | 19,132 | 87,922 | 21.8% |
| Both | 9,335 | 85,474 | 10.9% |

All four lived. The guard changed the seed's path and hence the local
comparison. The four runs still represent one Human Paladin start.
