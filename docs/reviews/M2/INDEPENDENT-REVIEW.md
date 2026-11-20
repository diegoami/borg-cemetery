# Independent review: M2 / synthetic P1

Reviewer: MiniMax-M3 (independent of the GPT/Codex implementer family).
Review date: 2026-11-20. This is a review, **not** owner acceptance. The owner
chooses acceptance, merges the review PR and advances the boundary.

## Pins reviewed

| Item | Value |
|---|---|
| Cemetery review pin | `ec332c62c82aea3a0a562a59683ec1936f6fff99` |
| Paired reborn implementation | `2faaadb1a8c9aee07fddcae905eee46699e99005` |
| Measured runtime built and executed | `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d` |
| Runtime source digest (reproduced) | `bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a` |

Cemetery PR #7 (`0360b72c`) is merged into `main`. Its tree is byte-identical to
the review pin (empty `git diff`), so the reviewed scope is exactly what was
merged. `reviewed` is still at the pre-M1 baseline `44d97669`; no acceptance tag
exists; `PLAN.md` and the M2 packet still record the milestone as not accepted.

## Recommendation

**Conditional accept**, subject to the owner deciding on Finding 1 (a wording
inaccuracy in the evidence packet) and noting that every substantive check in
the review scope passed.

Every executable claim in the packet was reproduced independently: the six-cell
suite was rebuilt from the pinned runtime and re-executed, and all six outcomes
and all 18 key/state/message streams matched the frozen reference.

## What was reproduced

### Runtime and identity

- Built `99473510` in an isolated checkout with `BORG_IMPL=rust flock
  /tmp/angband-validation.lock harness/build.sh`.
- Reproduced the source digest `bf9a451c...` exactly via
  `harness/identity.sh source-hash rust`; `BUILD_ID` reports
  `git_rev=99473510...`, `git_dirty=no`, `inputs_dirty=no`.
- The local binary (`68ed3ed7...`) differs from the retained `8336a9ca...`
  because it was built with a different rustc/CC in a different directory. This
  is the already-declared, *non*-established same-toolchain reproducibility
  situation, and it did not affect gameplay: all 18 streams matched.

### Six-cell suite

Ran the pinned workflow's commands verbatim:

```sh
python3 scripts/synthetic_suite.py run --manifest synthetic/p1-warrior/suite.json \
  --source <exact-built-reborn> --out <fresh-dir>
python3 scripts/synthetic_suite.py verify --actual <out>/results.json \
  --expected docs/reviews/M2/results.json
```

Result: **4 deaths, 2 cap survivals, 0 harness/identity/timeout/unsupported
failures**, and `6 scenarios and 18 gameplay streams match retained evidence`.

Scope confirmed from the run's own `state.log` first rows: three generated
caves at depths 5/10/15 (`50,15` / `28,36` / `159,16`), each with a birth and
an observed-tier cell sharing the identical cave hash and coordinates, all from
seed 101. The tier source also used seed 101.

Near-death invariants hold in every cell: `coverage='unavailable'`, `count=null`,
`reason='P1 has no null-move evaluator'`.

### Repository and native checks

| Check | Result |
|---|---|
| Cemetery repo tests | 58 passed |
| Cemetery native-tool tests | 50 passed |
| Cemetery statistics `--check` | 129 reports |
| Reborn `cargo fmt --check -p borg-reborn-rs` | clean |
| Reborn `cargo clippy --workspace --all-targets -- -D warnings` | clean |
| Reborn workspace tests | 156 + 4 + 5 passed, 0 failed |
| Reborn `cargo test --release -p borg-core` | 328 passed, 4 ignored |
| Reborn engine native tests | 81 tests, 16 skips, **0 failures** |
| Reborn tool tests (paired head `2faaadb1`) | 94 passed |
| Reborn script tests | 19 passed |
| Ordinary smoke parity | 3/3 runs identical (messages + state compared) |
| Exact smoke parity | 3/3 runs identical (messages + state compared) |
| `import-deaths.py --check` on the qualified registry | 79 dossiers verified |

The 7 errors seen on a first engine-test run were an artifact of my isolated
layout (the death-tools pointer expects a `borg-cemetery` sibling checkout and
the test subprocesses do not inherit `BORG_CEMETERY_DIR`). With the sibling
checkout in place the suite is `OK (skipped=16)`, matching the packet.

### Identity validation

- Preflight refuses any checkout that is not clean at the exact manifest
  commit. Observed directly: pointing the runner at the paired head
  `2faaadb1` (a descendant of the pinned runtime) produced six
  `identity_mismatch` rows with **zero** games attempted and the full
  denominator preserved. This is the behaviour the packet describes for the
  rejected scratch-build preflight.
- A harness advertising only `synthetic-start@1` is refused with
  `unsupported`; `@1` is not advertised in `harness/capabilities.json` and the
  only `@1` mention in the runtime is a historical HANDOVER entry.
- `classify` requires the executed binary digest to match the verified
  build before and after the run, and rejects a missing/falsy expected digest.
- The catalog's observed tier keeps its own, different source pin
  (`401597ca...`) and the suite keeps the execution pin (`99473510...`); both
  identities are retained separately, as required.

### Failure classification

Each terminal category was exercised through the fake adapter and behaves
independently:

| Mode | Status |
|---|---|
| death | `death` |
| survived to cap | `survived_to_cap` |
| early stop with `turns` | `stopped` (not a survival) |
| `borg_stopped` | `stopped` |
| timeout | `timeout` |
| launcher/child failure | `harness_failure` |
| wrong start depth | `identity_mismatch` |
| malformed state row | `identity_mismatch` |
| missing evidence | `harness_failure` |
| malformed summary | `harness_failure` |
| contradictory terminal receipt | `harness_failure` |
| registry pollution | `harness_failure` |
| unsupported preflight | `unsupported`, 0 attempted, denominators intact |

A run claiming `turns` but stopping before `turn_cap` is classified `stopped`,
not `survived_to_cap`.

### Required stream receipts

`keys.log`, `state.log` and `messages.log` are mandatory; missing any is a
failure. Key-line count must equal both the state-row count and
`summary.keys`. The terminal turn must fall in `[last_state_turn, 2**31-1]`,
rejecting an impossible int32 overflow. The native message counter matches
whole messages only (`'Nothing happens.'` embedded in a longer line is not
counted).

### Process cleanup

Verified independently of the repo's own tests: a real launcher/child/grandchild
tree under `run_bounded` left **no** surviving process after the outer wall
limit (grandchild `/proc` entry gone, not merely a zombie). The interruption
path (`SIGTERM` converted to an exception so the `finally` block runs) and the
real parent/child regression in `tests/test_synthetic_suite.py` both pass.

### Immutable evidence preservation

- `docs/reviews/M2/results.json` is byte-identical to
  `checkpoints/p1-results-52dff9f.json` (`7c5bea2d...`), and that file is
  byte-identical to the `results.json` at commit `52dff9f` — verified with
  `git show`.
- `checkpoints/p1-results-b55b07a.json` is byte-identical to the `results.json`
  at commit `b55b07a` (`005d44e8...`).
- `git diff 52dff9f ec332c62 -- docs/reviews/M2/results.json` is empty: the
  frozen reference has not been edited since the freeze.
- The two historical packets remain distinct and honestly labelled: `000d8d6f`
  (b55b07a), `ba06d6fa` (#15 pilot) and `8336a9ca` (52dff9f / latest). All three
  report `rustc 1.100.0` and `GCC 14.2.0` but were built in different
  directories. The packet now explicitly withdraws the earlier
  cross-toolchain-only explanation and states that same-toolchain bit
  reproducibility is **not** established and the cause of the byte differences
  was not isolated. This correction is accurate.
- The follow-up attempt in `reproductions/20261116-followup/` is a genuine
  separate execution, not a relabelled copy: different `runner_sha256`, and
  `config.txt` / `process.json` / `summary.json` differ (path/timing receipts),
  while all 18 gameplay streams and every deterministic field match. Only
  those three attempt-specific files differ across all six cells.
- Both merge-integrity receipts were independently reconstructed from Git
  objects. `74cb8ff`: 73 packages / 803 files, **0** parent blobs changed or
  missing. `9408927`: 79 packages / 869 files, **0** parent blobs changed or
  missing.
- The six migrated task-control packages are byte-identical (all files, by Git
  blob) to their origin at `68522fdc`.

### Exclusion of synthetic deaths from natural registries

- `not_natural` rejects a synthetic birth and a synthetic record death
  ("not natural: synthetic start") and accepts a genuinely natural death.
- Exporting a **real** synthetic death from my own run through the pinned
  native tools printed `export-death: not natural: synthetic start; no dossier`
  and created **no** dossier; the pinned checkout's `deaths/` tree was
  unchanged afterwards.
- Reconciling my real six-cell run output against an empty registry reported
  six visible `SKIPPED: ... not natural: synthetic start` lines and
  `0 natural deaths in the runs`.
- The retained ordinary controls are clean: of 79 qualified packages, **0** are
  synthetic-marked and **0** carry the one-way option pair.
- The pinned native subtree is enforced before any tool code executes
  (`death-tools-pin.txt`). I confirmed the pinned `1afd9423` subtree verifies,
  and that modified, missing and extra native files are each refused with
  "refusing to execute" before running.

### Retained-stream CI gate

I mutated the retained packets adversarially. **Every meaningful mutation was
detected**: changed stream digests, deleted stream receipts, changed byte
counts, flipped outcomes, flipped terminals, changed death cause, minimum HP,
observed turns, progress, candidate counts, refusal counts, spec digest,
manifest digest, suite spec digest, runtime commit, build commit, source
digest, `git_dirty`, capabilities digest, removed/duplicated cases, changed
schema, changed scenario count, and a failure status in the attempt.

The hard near-death invariant survives **joint editing of both packets**:
`count` set, `coverage` set to `qualified`, the key removed and an empty dict
are all rejected. This is a genuine hard invariant, not a comparison against a
reference that could be weakened in step.

The one gap is the documented one: a jointly edited runner *and* reference can
pass, because the gate is a regression check rather than an approval
mechanism. `docs/synthetic-suite.md` states this explicitly. The CI workflow
pins every action to a commit SHA, triggers on changes to
`scripts/synthetic_suite.py`, `synthetic/**`, the workflow itself and
`docs/reviews/M2/results.json`, runs with `contents: read` only, and performs
no archive to the natural registry.

## Findings

### Finding 1 — Packet wording misstates the observed kit's inventory (Low, documentation)

**Location:** `docs/synthetic-suite.md:122` ("the observed record contains no
wands/staves and all pvals are zero"); `synthetic/p1-warrior/README.md:33` ("The
fixed observed kit has no wands/staves and every recorded pval is zero");
`docs/reviews/M2/README.md:116` and `docs/reviews/M2/MILESTONE-REVIEW-RESPONSE.md:40`
("no charged devices ... all pvals are zero").

**Trigger:** The observed tier's record contains three devices that natively
carry a charge count: `item:9:1:1:0:0:0:0:0:0:1` (a wand, tval 9) and
`item:19:1:1:5:0:0:0:0:3231:1` and `item:19:1:2:-1:0:0:0:0:5000:1` (two staves,
tval 19). The packet states "The fixed observed kit has no wands/staves and
every recorded pval is zero" and "The observed tier contains no charged
devices".

**Consequence:** The literal statement "no wands/staves" is false: the kit does
contain one wand and two staves. The *substantive* claim is nevertheless
correct. In the pinned engine (`engine/angband/src/obj-make.c:848-849`) a
wand/staff's `pval` holds its charge count, and every pval in this record is
`0`; the nonzero values 3231 and 5000 are the `timeout` field, i.e. remaining
fuel for the light source, not charges. The devices therefore cannot be used,
so "no charged devices" and "all pvals are zero" hold, and the bank's decision
not to qualify charged/recharged builds is unaffected.

**Reproduction:** `python3 -c "import sys;sys.path.insert(0,'scripts');import synthetic_suite as s;print(s.build_record('synthetic/p1-warrior/warrior-level5.build')['items'])"`
on the pinned record shows tval 9 and two tval 19 entries with `pval=0` and
`timeout` 3231 / 5000.

**Why this matters despite being cosmetic:** the sentence sits directly next to
the statement that the current parser's numeric pval ceiling is not a
kind-specific charge bound. A reviewer or future maintainer who reads "no
wands/staves" and later finds a wand and two staves in the record has to
re-derive that the safety margin comes from `pval == 0`, not from the absence
of device kinds. The accurate phrasing would be "contains no *charged* devices:
every wand/staff pval is zero, and the two staves carry only residual fuel
timeouts". This is a wording correction to the evidence packet, not a change to
the bank, the runtime or any reviewed stream.

Note that the three locations that say only "no charged devices" / "all pvals
are zero" are themselves accurate; only the two locations that additionally say
"no wands/staves" overstate it.

### Finding 2 — The "no charged devices" guarantee is enforced by data, not by a rule (Informational)

**Location:** `scripts/synthetic_suite.py:128` (pval bound `0..32767`),
`engine/frontend/synthetic-build.c` (the same numeric ceiling).

The native record parser bounds `pval` numerically but not per kind, so a
record with a charged wand would be accepted. The bank is safe only because
*this* record has zero pvals. The packet declares this accurately and tracks
the per-kind cap as source-side follow-up #411, which is the correct handling
for a milestone that does not claim charged-tier qualification. Recorded here
so it is not lost, not as a defect of this milestone.

## Accepted scope limitations (not defects)

- One class, one seed, three depths, two conditions; denominator one per cell.
  Birth and observed cells at a depth share the same generated cave, so the six
  cells are paired conditions on three caves, not six independent lives. The
  report and `docs/synthetic-suite.md` state this; the observed tier also came
  from seed 101.
- The birth cells keep the **ordinary** Warrior birth kit and then apply the
  one-way options. At the pinned engine `class.txt:157` conditions the Word of
  Recall scroll on `birth_no_recall`, so a native one-way birth would omit it.
  The P1 birth cells retain it and each consume it at turn 3 with "Nothing
  happens." This was confirmed in the real run output of all three birth cells
  and is disclosed in `synthetic/p1-warrior/README.md`,
  `docs/synthetic-suite.md` and `MILESTONE-REVIEW-RESPONSE.md`. It is a
  declared construction difference, not a native one-way kit, and it means the
  bank is not an experiment isolating character level alone.
- Qualified near-death measurement is unavailable by design and stays null.
- No population, Borg-improvement, average-kit or same-toolchain binary
  reproducibility claim is made, and the packet explicitly withdraws the
  earlier cross-toolchain-only explanation.
- Low-HP candidate screens and the generic refusal counters are provisional
  diagnostics; the packet says so and the notes field says so in the data.
- One-way starvation remains unmeasured; the six cells cannot establish
  long-horizon policy competence.
- P2 (wider catalogs, qualified null-move evaluation) and P3 (paired
  two-executable comparison) are unimplemented and out of scope.

## Checks not performed

- The cloud `synthetic-suite` workflow was not dispatched; all suite execution
  was local on an independently built runtime. Current-head CI status is
  authoritative and was not asserted here.
- The upstream engine Git object, bindgen regeneration and the incident/fixture
  dependencies that CI supplies were not fetched; the 16 engine-test skips are
  the documented dependency/fixture skips.
- The `full` reference suite was not re-run; only the ordinary and exact smoke
  suites (3 cases each) were compared against their stored references.
- The vendor audit was not re-run independently.
- Recorder-driven capture/GIF pipelines, the `run-borg`/`try-scenario` cloud
  pipelines and the M1 collection/replay scope were not reviewed.
- The #15 external pilot was not re-executed; it was verified only as the
  immutable external reproduction recorded in `results-lineage.json`.
- The M2 packet's claim that raw logs exist outside Git in the task workspace
  (`p1-real-suite`, `p1-real-suite-repeat`, `p1-final-suite-executed`,
  `p1-review-suite`, `p1-milestone-suite`) could not be checked: those
  directories are not in the repository and were not available to this review.
  The packet's own account of a rejected final-runner preflight and its
  retained six identity-mismatch rows was therefore taken as reported.
- No owner acceptance, merge, `reviewed` advance, acceptance tag, or P2/P3
  work was performed. The `reviewed` branch remains at the pre-M1 baseline.
