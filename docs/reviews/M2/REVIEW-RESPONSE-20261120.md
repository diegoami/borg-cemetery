# Response to the independent M2 review (2026-11-20)

Subsequent disposition: the owner [accepted the frozen M2 milestone](../ACCEPTANCE-20261120.md)
on 2026-11-20, keeping `reviewed` unchanged. The response below retains the
finding dispositions as presented before that decision.

Status: [PR #83](https://github.com/diegoami/borg-cemetery/pull/83) records the
owner-selected MiniMax-M3 review and a conditional acceptance recommendation.
Owner acceptance remains pending. The reviewer independently reproduced the
six outcomes and all 18 gameplay streams on the pinned runtime. This response
changes no runtime, build record, scenario, frozen result or historical review.

## Finding 1: item types were decoded against the wrong mapping

The proposed wording correction is not applicable to the pinned engine.
The observed record's first item field is an engine `tval`. At runtime
`99473510940b8a7bd6e77ad61e3a2b00c72a6e6d`, the enum in
[obj-properties.h](https://github.com/diegoami/borg-reborn-rs/blob/99473510940b8a7bd6e77ad61e3a2b00c72a6e6d/engine/angband/src/obj-properties.h)
expands
[list-tvals.h](https://github.com/diegoami/borg-reborn-rs/blob/99473510940b8a7bd6e77ad61e3a2b00c72a6e6d/engine/angband/src/list-tvals.h)
in order, starting at zero:

| tval | Pinned engine type | Review's interpretation |
| --- | --- | --- |
| 9 | SWORD | wand |
| 19 | LIGHT | staff |
| 22 | STAFF | not identified |
| 23 | WAND | not identified |

Thus `item:9:1:...` is a sword, and both `item:19:1:...` rows are lights.
Their timeouts of 3231 and 5000 are light fuel. They are not uncharged staves.
No observed item has type 22 or 23, and all recorded pvals are zero. The
existing statement that this kit has no wands/staves is accurate. Replacing
it with the proposed account of a wand and two staves would introduce an error.

Run this from Cemetery with a local reborn clone containing the runtime commit
(change only the clone path). It reads the exact Git object, not the clone's
working-tree version:

```sh
python3 - /path/to/borg-reborn-rs <<'PY'
from pathlib import Path
import re
import subprocess
import sys

runtime = '99473510940b8a7bd6e77ad61e3a2b00c72a6e6d'
source = subprocess.check_output([
    'git', '-C', sys.argv[1], 'show',
    runtime + ':engine/angband/src/list-tvals.h',
], text=True)
types = re.findall(r'^TV\((\w+),', source, re.M)
assert {n: types[n] for n in (9, 19, 22, 23)} == {
    9: 'SWORD', 19: 'LIGHT', 22: 'STAFF', 23: 'WAND',
}
record = Path('synthetic/p1-warrior/warrior-level5.build').read_text()
items = [line.split(':')[1:] for line in record.splitlines()
         if line.startswith('item:')]
for item in items:
    print(item[0], types[int(item[0])], 'pval=' + item[7],
          'timeout=' + item[8])
assert not any(types[int(item[0])] in {'STAFF', 'WAND'} for item in items)
assert all(int(item[7]) == 0 for item in items)
PY
```

## Finding 2 and declared limits

Acknowledged. This fixed bank does not qualify charged/recharged devices or
kind-specific charge caps; source follow-up reborn #411 remains separate.
The absence of wands/staves in this data is not a general parser restriction.
The reviewer reproduced the execution and preservation claims, with the
cloud/vendor/full-reference/fixture gaps stated in the review. No additional
coverage is inferred. The paired three-cave/two-condition/one-seed scope,
ordinary-before-one-way birth normalization, unavailable qualified near-death
measurement and unestablished binary reproducibility remain unchanged.

The review is retained as submitted on its own branch. This response records
the implementer's evidence-based disposition; it does not rewrite the review,
merge its PR, advance `reviewed`, tag acceptance or start P2/P3.
PR #83 also targets the pre-M1 `reviewed` baseline, so its merge would include
the preceding M1 history. A decision on the M2 finding does not independently
authorize that broader boundary advance. Both frozen milestones can receive
scoped owner decisions while the shared branch boundary remains unchanged.
