Latest review correction: [review-cases.md](review-cases.md) and
[review-comparisons.json](review-comparisons.json), specimen `394f2aea`.
The earlier matrix below is retained history. New all-switch outcomes are
five of seven alive; Fang425 and rock-lizard151 remain deaths. Both
reviewer-named oil/pebble starts reach100k, with actual spell/oil choices
recorded. No population improvement is claimed.

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


## Owner decision: measurement belongs to borg-zoo

Owner, 2026-11-20: local validation is limited to builds, smoke and named
case replays. No new local population comparison is authorized. The local
parent script has only 24 replays of the six named starts across four
configurations; control-retention work has three games. No 600-start
candidate cohort has started. The Rogue 390305857 is an additional named
local case.

The normalized [600-start manifest](starts-600.tsv) has columns seed,
race_idx, class_idx and turn_cap (100000). It contains exactly the original
200 Rangers and 50 of every other class, without resampling. The original
lists and their hashes remain retained. `controls.json` records supplied
observations, not a newly played local population arm.

The [named before/after checks](local-cases.md) are complete, including the
owner-approved possible-wake follow-up. After the damage-first selector correction on `5acb8104`, six of seven
all-switch named lives reach 100k; 1976035382 dies to a large white snake
at engine turn 17873. Earlier outcomes remain in the ledger. The Rogue
control was already alive. These
selected cases are not population evidence. Population measurement is [borg-zoo #511](https://github.com/diegoami/borg-zoo/issues/511),
with a pinned specimen, shipped control, individual-switch arms and all
switches together. Only the owner schedules
that request; this session must not dispatch it. This report currently
contains completed baseline/category analysis and must not be read as an
enabled measurement result.

The initial Zoo pilot ran on `78b8f297` and found no survival-leading arm.
See the [recorded-death investigation](zoo-pilot-investigation.md) for the
selector defect and the boundary between observed evidence and unmeasured
corrections. No additional pilot starts were replayed locally.
