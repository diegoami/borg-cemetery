# Ranger flight fights and Recall: #760, #759, #758

Owner-requested local development comparison. The 600 starts and 100,000
engine-turn cap were specified before implementation: 200 Rangers and 50
starts of every other class. These are paired by seed, race and class.
Replays of the six named starts do not increase the independent sample count.

Source changes: [borg-reborn-rs #763](https://github.com/diegoami/borg-reborn-rs/pull/763)
and the separate stacked [#764](https://github.com/diegoami/borg-reborn-rs/pull/764).
Compiled and shipped switches remain 0. No population improvement claim.

See [category evidence by class](categories.md) for the proposed entries,
engine citations, and pinned zoo counts.

## Baseline reproduction

Before any implementation, clean `08f94e1fed0b80fd854584d893209983079157ea`
reproduced all six deaths. Keys, states and messages match both the supplied
off-arm evidence and the canonical Cemetery records byte for byte. See
[baseline-six.json](baseline-six.json) for exact build and stream hashes.
No duplicate baseline deaths were exported.

| Seed | Race/class index | Cause | Game turn | Canonical case |
| --- | --- | --- | ---: | --- |
| 425904011 | 2/7 | a wild cat | 3660 | [D-3299fd20a324](../../deaths/D-3299fd20a324cddeb556d39707e3b22e0735fa9666224a1a22fe26b587060911/README.md) |
| 2095979189 | 6/7 | a wild cat | 3345 | [D-d09b9d357988](../../deaths/D-d09b9d357988e5fe2fbcb60d5691ec15d2e9d00a2ceaadf5868c72d4ee2a9124/README.md) |
| 1976035382 | 8/7 | a wild cat | 4248 | [D-4d01e23a3d52](../../deaths/D-4d01e23a3d529c82e67301b17fbaacf8d6dae8d2265709ff0f255e8a0b241f8a/README.md) |
| 2049259432 | 4/7 | Fang, Farmer Maggot's Dog | 4429 | [D-9e526055f043](../../deaths/D-9e526055f043e11781d5ecb1d97e66385be2acd3a5590f775b6145d4fe0720e8/README.md) |
| 807683971 | 0/7 | a black naga | 1534 | [D-7e07cc9e67b6](../../deaths/D-7e07cc9e67b6a60f60af54b0b2d449c322d05e6d5f58a855c8972afa8973d29f/README.md) |
| 1517990203 | 4/7 | a small kobold | 6338 | [D-e1ba89db1a1e](../../deaths/D-e1ba89db1a1e0e03ce014e04f1d2e2ab2cc14228048ee34ff9a5aef98c648010/README.md) |


## Validation in progress

Enabled cases, winning-fight checks and paired cohort results are still
pending the shared local validation lock. This file currently records only
the completed baseline reproduction; it must not be read as an enabled result.
