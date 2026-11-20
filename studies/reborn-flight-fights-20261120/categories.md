# Category evidence by class

Snapshot: borg-zoo results commit `a31a57e985517b6b46e1aeea9e8a29c7b5fb6119`. Filter and
deduplication are in [zoo-candidate-deaths.json](zoo-candidate-deaths.json).
There are 8953 distinct recorded reborn death outcomes.
Builds/profiles/engine versions are pooled as investigative leads. These are
direct-killer counts, not mortality rates or independent causal evidence;
poison deaths are not attributed back to worm masses.

| Class | wild cat | crow | cave spider | crow of Durthang | wood spider | giant white mouse | giant white louse | giant fruit fly | white worm mass | green worm mass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Warrior | 9 | 11 | 11 | 0 | 0 | 29 | 21 | 0 | 4 | 3 |
| Mage | 73 | 63 | 28 | 0 | 0 | 42 | 1 | 0 | 10 | 2 |
| Druid | 112 | 87 | 27 | 1 | 0 | 56 | 4 | 0 | 32 | 8 |
| Priest | 56 | 41 | 46 | 0 | 0 | 71 | 11 | 0 | 28 | 4 |
| Necromancer | 79 | 54 | 27 | 0 | 0 | 50 | 5 | 0 | 23 | 4 |
| Paladin | 26 | 32 | 26 | 0 | 0 | 31 | 8 | 0 | 13 | 1 |
| Rogue | 44 | 36 | 19 | 1 | 0 | 38 | 4 | 0 | 10 | 2 |
| Ranger | 94 | 67 | 42 | 0 | 0 | 25 | 12 | 0 | 8 | 7 |
| Blackguard | 28 | 36 | 35 | 0 | 0 | 37 | 7 | 1 | 19 | 8 |

Initial entries are wild cat/crow (`fast-fragile`) and mouse/louse/fly/white
and green worm masses (`breeder`). The initial all-class CL50 range is
unmeasured. Existing breeder stand/stoppable/lost-colony rules still decide
whether a breeder attack entry applies. Cave and wood spiders are deferred
because of groups/poison; crow of Durthang adds WOUND. No third reason is
justified by this analysis.

Mechanics were checked against borg-reborn-rs engine `574b618c`:
`monster.txt:627-642,677-691,1099-1113,1116-1163,1239-1253,2088-2106,2131-2146,3101-3114`
and `monster_base.txt:211-216` (insect MULTIPLY inheritance).
The game data, not these frequencies, establish speed/fragility/breeding.
