# Review: PR #92 "Retain unseen stair-blocker investigation and trials (reborn #781)"

- Repository: `diegoami/borg-cemetery`
- Branch: `evidence/reborn-781-unseen-bump`
- Head reviewed: `adf585125e1d1b1b525d1e5424797c4e938e990f` (PR evidence head)
- Base: `6ebb6e34` — 24 commits behind current `origin/main` (`126cf1f7`)
- Reviewer model family: MiniMax (M3). This is a **review of a retained-evidence
  PR**, not of the upstream implementation; the upstream implementation
  (borg-reborn-rs PR #782) was authored by the same author and is not
  re-reviewed here beyond what the retained evidence asserts.
- Upstream references checked locally: `borg-reborn-rs` commits
  `09a70906`, `4e9af99e`, `155943c0`, `f1d3c576`, PR #782, and
  `docs/handover/2026-11-20-781-unseen-blocker.md`.

## Verdict

**Approve with two minor documentation fixes.** The evidence is complete,
custody is verifiable byte-for-byte, every quantitative claim in the case
README that I could check reproduces exactly, and the scope is correct: nothing
outside the new validation case and three additive `deaths/ALIASES.json`
entries changes.

This is the strongest evidence PR I have reviewed in this repository. The
custody chain (receipts → per-file SHA-256 → embedded dossier hashes →
`verify.py`) is complete with no gaps, the investigation separates the
surviving enabled runs from the single reproducing control without
overclaiming, and the three retained death dossiers correctly declare
themselves repeats of one life rather than independent samples.

Two things should be corrected before merge. Neither blocks the evidence.

| # | Finding | Severity |
|---|---|---|
| F1 | The reproduction instructions point at the wrong commit for the "shipped identity" check | minor |
| F2 | The PR body's dossier count (847) is stale against current `main` (1733) | minor |

## What I verified

### 1. Evidence custody — complete and self-consistent

`validation/borg-reborn-rs/unseen-bump-781/verify.py` re-hashes every retained
file against `receipts.json`:

```
$ python3 validation/borg-reborn-rs/unseen-bump-781/verify.py
Verified 22 attempts; repeats are not independent lives
```

Beyond that check I verified the receipts are *complete* rather than merely
passing their own assertions:

- **264 receipt-stored files, 264 files on disk** — exact 1:1. Nothing
  referenced is missing; nothing present is unreferenced. No orphan evidence,
  no gap in the custody chain.
- The receipts' `sha256`/`bytes` fields are checked against **decompressed**
  bytes for `.gz` files, and the `process.json` `executable_sha256_before`/
  `_after` fields equal the recorded `binary_sha256` for every attempt
  (`verify.py:14-20`). No attempt has a binary that changed under it.
- All 22 attempts record `process_status: success`; no attempt was silently
  dropped.

### 2. The central reproduction claim — confirmed exactly

README:16-19 claims the historical control matches the reported key SHA-256
`8b21c6b94e80e9692c45c4dcf88352d351c3f88db19bc11c189a2330cf613124` and dies
at turn 37,759, CL4/DL1, to "a clear icky thing".

Verified across **all three** historical builds:

| Run | `keys.log` SHA-256 | Turns | Dead | Cause | max_clevel / max_depth |
|---|---|---|---|---|---|
| `historical-off` | `8b21c6b9…13124` | 37,759 | yes | a clear icky thing | 4 / 1 |
| `historical-patch-off` | `8b21c6b9…13124` | 37,759 | yes | a clear icky thing | 4 / 1 |
| `historical-final-off` | `8b21c6b9…13124` | 37,759 | yes | a clear icky thing | 4 / 1 |

The three builds differ in `source_sha256` / `binary_sha256` /
`borg_txt_sha256` (i.e. the patched and unpatched sources), yet produce a
**byte-identical key stream**. This is exactly the "disabled changes still
reproduce the original death" property the upstream PR body claims, and it is
the strongest single piece of evidence in the case: the behaviour under test
is provably inert when switched off.

### 3. The quantitative investigation — every figure reproduces

README:26-33 describes the stuck phase. All of it checks out against
`runs/historical-off/trace-core.jsonl.gz` and `state.log.gz`:

- **110 caution decisions from turn 36,669** — counted exactly
  (`check == "borg_caution"`, `turn >= 36669` → 110 events).
- First decision **HP 41/44, danger 24**; at turn **37,189 → HP 21/44, danger
  99**; at turn **37,709 → HP 3/44, danger 162**; final danger **170**.
- The player **never moves**: across all 248 state rows for turns 36,669 →
  37,759 the position is `(x35,y40)` without exception. README:20-21's
  "(y40,x35)" is correct (the state log records `x,y`).
- **219** "You fail to harm something." messages, and **48** "Something touches
  you." messages — matching README:21-22 and :35-36.
- Danger is **not zero**, confirming README:28 ("the problem is not zero
  reported danger").

The causal reading (README:28-33) — that CLW's three gates (wound percentage
≥30, `danger < HP + 20`, `20 > danger/3`) never all hold across those 110
decisions — is a claim about the engine's gate arithmetic that I did not
re-derive from the borg-core source; the *observables* it rests on (HP/danger
series, decision count) all reproduce, so the conclusion is at least
consistent with the recorded data.

### 4. The preliminary wasted-throw trial — preserved and correctly explained

README:59-63 claims the preliminary build kept the grid occupied after
"It dies." and wasted two further throws plus a Phase Door, and that the final
build associates the throw's death feedback with its grid and clears it.

Verified from the message logs:

- **Preliminary (`historical-on`, turns 10,703–10,733):** oil throw →
  "It dies." → *another* oil throw at 10,713 → *another* oil throw at
  10,723 → Phase Door at 10,733. Three throws and a Phase Door for one
  already-dead target.
- **Final (`historical-final-on`, same turns):** oil throw → "It dies." →
  the Borg then *walks into* (30,78) at 10,723 and proceeds to (30,79),
  (31,79). No further throw, no Phase Door.

This is the clearest example in the case of a negative result being retained
rather than discarded: the preliminary attempt is the evidence that motivated
the kill-confirmation fix, and it is preserved with the same rigour as the
delivery.

The divergence point in README:56-58 is exact: `# Unseen bump: (30,78)
occupied for 100 game turns` and the oil throw occur at **turn 10,703** in
every enabled run.

### 5. Per-run parameter claims — confirmed from the retained `borg.txt`

README:65-72 describes each run's configuration. The retained
`runs/*/user/borg.txt` files confirm each one exactly:

| Run | `turns` | `response` | `heal_hp_percent` | `throw_tries` | README claim | ✓ |
|---|---|---|---|---|---|---|
| `historical-on`, `historical-final-on` | 100 | 1 | 50 | 3 | "100-turn memory, response1, cure threshold50, three throws" (:65-66) | ✓ |
| `historical-heal` | 100 | 0 | 50 | 3 | "Occupancy/cure-only (response0)" (:66-67) | ✓ |
| `historical-phase` | 100 | 1 | 50 | **0** | "Zero throws exercises five Phase Doors" (:67-68) | ✓ |
| `historical-cure-probe` | 100 | 0 | **100** | 3 | "The explicit cure-threshold100 probe" (:68-69) | ✓ |

The event counts corroborate each description independently: `historical-phase`
logs exactly 5 `# Phase (unseen bump): done` and 0 oil throws;
`historical-cure-probe` logs exactly 16 `# Healing before stairs:` and 0 oil
throws; `historical-heal` logs 0 oil throws and 0 heals, matching "survives,
without needing the new cure" (:66-67).

The Detect Invisible caveat (:70-72) holds: **every one of the 22 attempts
records `# Detect Invisible: an unseen monster` = 0**. The new call site is
genuinely unexercised, exactly as claimed.

### 6. Endpoint and key-hash claims — confirmed

| README claim | Verified |
|---|---|
| Current main `4e9af99e` survives, key `4cb7bb43…9cc74` (:74-75) | `base` and `current-off` both `4cb7bb4376932733cbf11100e7a3c60f8694392e43c88c30fb93f1781699cc74` ✓ |
| "The disabled patched run is identical" (:75-76) | `current-off` ≡ `base` byte-for-byte ✓ |
| Final delivery enabled keys `94930733…f355` (:140-142) | `clean-on`, `current-on`, `delivery-on` all `949307338b60b03e6df33e25a0a314eeeb8d498a69407b3694d23637bcabf355` ✓ |
| Enabled survival to 100,000 (:65-79) | all 10 non-death Druid runs reach `game_turns=100000`, `stop_reason=turns` ✓ |
| CL7/maxDL2 for historical enabled (:66) | `historical-final-on`: clevel 7, max_depth 2 ✓ |
| CL6/maxDL1 for zero-throws (:67) | `historical-phase`: clevel 6, max_depth 1 ✓ |
| CL5/maxDL2 for threshold100 (:68-69) | `historical-cure-probe`: clevel 5, max_depth 2 ✓ |
| Clean delivery head CL8/maxDL3 (:77-78) | `delivery-on`: clevel 8, max_depth 3 ✓ |

### 7. Smoke identity checks — 3/3, consistent receipts

`smoke-diff.txt`, `clean-smoke-diff.txt` and `delivery-smoke-diff.txt` each
report `3/3 runs identical (expected 3)` with `messages.log` and `state.log`
compared in 3 runs. The manifests are internally consistent: each records
`binary_sha256` == `binary_sha256_end` (the binary did not change during the
suite) and the build identity (`git_rev`, `source_sha256`, compiler versions)
matches the corresponding `builds.json` entry and the `receipts.json` attempt
it backs.

The three smoke seeds are each repeated three times (9 smoke attempts), which
the receipts' `same_life_group` field records explicitly
(`smoke-mage-2`: 3, `smoke-priest-3`: 3, `smoke-warrior-1`: 3).

### 8. Count discipline — the independence framing is correct

- `receipts.json` carries `independent_druid_seeds: 1` and an explicit
  `warning`: "Replays and alternative plays of one seeded life, not independent
  samples. Three smoke seeds repeated three times are identity checks."
- `same_life_group` gives exactly **13 plays of `human-druid-102023799`** and
  **9 smoke identity checks** = 22, matching README:143-144 and the PR body.
- Each dossier's `record.json` carries `independence_note`: "One independent
  death per encounter family; repeats of the same run are not new cases."

This is the correct treatment under AGENTS.md ("never count replay or
alternative continuations of one life as independent samples").

### 9. Death identity contract — compliant

The three dossiers get three distinct canonical IDs, and that is correct, not
ID inflation. `docs/death-identity.md` states the ID hashes
`{encounter_family, result_sha256}` and that "Build/configuration and
starting-position distinctions are already represented by the encounter
family". The three deaths share `result_sha256` (`8b21c6b9…13124`) but have
three distinct `encounter_family` values, because their source/binary/config
differ:

| Dossier | `encounter_family` | `source_sha256` | `binary_sha256` |
|---|---|---|---|
| `D-41faa5e2…` | `start-5ab78da6…` | `0d6f9daa…` | `cfc67e7f…` |
| `D-18705b44…` | `start-91c4ff55…` | `b16e86f8…` | `6741f73b…` |
| `D-30366e42…` | `start-1102a8a2…` | `2e28b05f…` | `ab0b1c46…` |

The `encounter_family` is derived in `scripts/native/death_registry.py:57-59`
from seed/race/class/config/origin, so different source builds legitimately
produce different families. The README states the consequence plainly
(:88-90): "All three deaths have the same original start/key stream, so they
are repeats of one life despite the configuration/provenance-specific
exporter IDs. They do not count as three distinct deaths."

### 10. Repository checks — all green, on the branch and merged onto current `main`

On the branch head `adf58512`:

```
python3 validation/borg-reborn-rs/unseen-bump-781/verify.py → Verified 22 attempts
python3 scripts/death_ids.py --check                          → Verified canonical IDs for 847 retained dossiers
python3 -m unittest discover -s tests                          → Ran 130 tests … OK
python3 -m unittest discover -s scripts/native/tests           → Ran 69 tests … OK
python3 scripts/build_statistics.py --check                    → Statistics: 134 reports checked/generated
```

Merged onto current `origin/main` (`126cf1f7`) — **clean auto-merge, no
conflict** (only `deaths/ALIASES.json` is touched by both sides, at different
offsets):

```
python3 scripts/death_ids.py --check                          → Verified canonical IDs for 1736 retained dossiers
python3 -m unittest discover -s tests                          → Ran 130 tests … OK
python3 -m unittest discover -s scripts/native/tests           → Ran 69 tests … OK
python3 scripts/build_statistics.py --check                    → Statistics: 139 reports checked/generated
```

### 11. Scope discipline — correct

The diff outside `validation/borg-reborn-rs/unseen-bump-781/` is **exactly one
file**: `deaths/ALIASES.json`, +18 lines, three additive entries. No change to
`deaths/CATALOG.md`, `statistics/`, `incidents/`, `docs/`, `PLAN.md`,
`README.md` or `AGENTS.md`. The three validation dossiers are correctly *not*
added to `deaths/CATALOG.md` (which indexes only `deaths/`), and
`build_statistics.py` does not pick up `validation/` evidence, so no population
or statistics series is inflated by three repeats of one life.

### 12. Upstream consistency

Checked against the local `borg-reborn-rs` clone:

- All four referenced commits exist: `09a70906`, `4e9af99e`, `155943c0`,
  `f1d3c576`. `155943c0` is the parent of `f1d3c576`.
- `f1d3c576` "Recognize every pinned melee verb when observing unseen bumps"
  touches `borg-core/src/borg_caution.rs`, `params.rs`, `docs/CALIBRATION.md`
  and the handover — consistent with README:134-140.
- `borg-core/src/params.rs` at `f1d3c576` defines the four parameters with
  defaults `turns=0`, `response=0`, `heal_hp_percent=0`, `throw_tries=3` —
  identical to the defaults in the retained `borg.txt` files. **All behaviour
  ships off**, confirmed in the retained smoke runs
  (`borg_param_caution_unseen_bump_*` all 0).
- The upstream handover
  `docs/handover/2026-11-20-781-unseen-blocker.md` states the same findings
  (37,759 death, `8b21c6b94e80e969`, 110 caution decisions, danger 24→170,
  CLW gates non-overlapping, Detect Invisible unexercised, no population
  claim). The two documents agree.

## Findings

### F1 (minor) — the reproduction instructions point at the wrong commit for the "shipped identity" check

README:124-126 reads:

> To check the shipped identity, build clean delivery commit`155943c0` and run
> `harness/suite.sh smoke`, then `harness/diff --suite smoke --expect-impl rust
> OUT harness/reference/smoke-borg-rs`: retained clean-build result is3/3 exact
> keys/messages/states.

`155943c0` is the **initial** head, not the final delivery — README:5-6 and
the PR body both name `f1d3c576` as the final delivery. The retained receipt
this instruction points at, `clean-smoke-manifest.txt`, is indeed built at
`155943c0`:

```
clean-smoke-manifest.txt:    build_id_git_rev=155943c0…  git_rev=155943c0…
delivery-smoke-manifest.txt: build_id_git_rev=f1d3c576…  git_rev=f1d3c576…
```

So the sentence is internally consistent — it names a commit and names the
matching receipt — but the wording is wrong in a way that matters: the
paragraph's subject is "the shipped identity", and the shipped identity is
`f1d3c576`, whose own 3/3 receipt is `delivery-smoke-manifest.txt`
(described separately at README:140 as "The clean final smoke again
matches3/3"). The upstream PR body puts it correctly: "Clean commit
`f1d3c576` matches shipped default-core smoke 3/3".

A reader following README:124 literally would build the wrong commit and
believe they had checked the shipped identity.

**Suggested resolution:** change `155943c0` to `f1d3c576` and point at
`delivery-smoke-manifest.txt` / `delivery-smoke-diff.txt`, or reword to make
clear that `155943c0` is the initial-head clean build and `f1d3c576` is the
final-delivery clean build, both retained and both 3/3. Both receipts are
present in the case, so either framing is fully supported by the evidence.

### F2 (minor) — the PR body's dossier count is stale against current `main`

The PR body says "scripts/death_ids.py --check verifies 847 retained
dossiers". That is true at the branch's base (`6ebb6e34`), but current
`origin/main` has **1733** retained dossiers, and the merged tree has 1736
(counted independently: `1733` on `origin/main` alone, `1736` after merging
the PR's three).

The number in the body is not wrong for the base it was measured on, but it
does not describe the repository's current state, and a reader checking the
claim against `main` today will see a different figure. This is the same
class of issue as F2 in the PR #62 review.

**Suggested resolution:** refresh the PR body against current `main` (or state
the base commit alongside the count).

### F3 (nit) — the receipts do not carry the parameter configuration

`receipts.json` records, per attempt: the build, `same_life_group`, the
outcome, `process_status`, `binary_sha256`, event counts, and the per-file
custody hashes. It does **not** record the `borg_param_caution_unseen_bump_*`
settings used for that attempt.

The configuration is recoverable — it is in the retained
`runs/*/user/borg.txt` files, and I confirmed all four values for every run
from there (table in §5 above). But the receipt is the file a consumer would
plausibly treat as the authoritative per-attempt summary, and the settings
that distinguish `historical-phase` (zero throws) from `historical-heal`
(response 0) from `historical-cure-probe` (threshold 100) live only in a
second file that the receipt does not reference by hash.

Note this is a strict improvement on the common pattern, not a regression:
`borg.txt` *is* retained per attempt and *is* inside the custody chain, so
nothing is unverified. It only means the receipt does not carry the
distinguishing knob on its own.

**Suggested resolution (optional):** add the four parameter values to each
receipt entry, or record a `borg_txt_sha256` pointer to the retained
`user/borg.txt` in the receipt entry so the link is explicit. This is a
convenience nit, not a correctness issue.

### F4 (nit) — `deaths/index.json` reports 3 "distinct starting conditions"

The generated `validation/…/deaths/index.json` reports
`"distinct_starting_conditions": 3` and `"death_process_attempts": 3`,
because `scripts/native/death_registry.py:97` keys attempts on
`(encounter_family, result_sha256)` and the three deaths have three distinct
families (§9 above). The index also carries its own limit line
("Selected cases; repeats/reference variants and backup branches are not
independent lives or a mortality-rate estimate"), and the case README and
`receipts.json` both state the one-life qualification explicitly.

So the file is not wrong — it is the standard generator output, and the
qualification is disclosed in three places. But a reader who opens
`index.json` alone sees "3 distinct starting conditions" for what the README
says is one life. The three deaths are correctly excluded from
`deaths/CATALOG.md` and from the statistics series, so nothing downstream
consumes this count as population.

**Suggested resolution (optional):** the case README already carries the
qualification at :88-90; no change is strictly needed. If the owner wants the
generated index to be self-qualifying for a validation-local registry, that
is a change to `death_registry.py` affecting every registry, not this PR.

## Notes on scope

- The three retained dossiers carry `assessment.json` with
  `"classification": "unassessed"`. That is the exporter's default and is
  consistent with the sibling validation cases (`native-controls`,
  `fast-encounter-trials`, `class-attack-preferences` are all `unassessed`
  too). The investigation narrative lives in the case README, which is the
  right place for it. Not a defect.
- `deaths/README.md` and `deaths/index.json` under the case are the
  generator's own output for the validation-local registry and regenerate
  consistently with the three dossiers.
- The `510` vs `511` release-test counts (README:127 vs :139) are not a
  contradiction: 510 was the preliminary build, 511 after the final delivery
  added the melee-verb corpus test.

## Recommended disposition

1. **F1** — correct the commit named in the shipped-identity reproduction
   instruction (`155943c0` → `f1d3c576`, or reword to distinguish the two
   clean builds). This is the only change I would ask for before merge.
2. **F2** — refresh the PR body's dossier count against current `main`, or
   state the base commit.
3. **F3** / **F4** — optional conveniences; neither affects correctness.

This review does **not** merge the PR, mark any milestone accepted, advance
the `reviewed` boundary, or dispatch a reviewer for the upstream
implementation PR #782. Those remain the owner's decisions.

## Reproduction (review)

```bash
cd /home/diego/projects/angband/borg-cemetery
git fetch origin evidence/reborn-781-unseen-bump origin/main
git worktree add /tmp/opencode/pr92-review origin/evidence/reborn-781-unseen-bump
cd /tmp/opencode/pr92-review
python3 validation/borg-reborn-rs/unseen-bump-781/verify.py   # Verified 22 attempts
python3 scripts/death_ids.py --check                            # 847 retained dossiers
python3 -m unittest discover -s tests                           # Ran 130 tests … OK
python3 -m unittest discover -s scripts/native/tests            # Ran 69 tests … OK
python3 scripts/build_statistics.py --check                     # 134 reports

# merged onto current main
git worktree add /tmp/opencode/pr92-merged origin/main
cd /tmp/opencode/pr92-merged && git merge --no-commit --no-ff adf58512   # clean
python3 scripts/death_ids.py --check                            # 1736 retained dossiers
python3 -m unittest discover -s tests                           # Ran 130 tests … OK
python3 -m unittest discover -s scripts/native/tests            # Ran 69 tests … OK
python3 scripts/build_statistics.py --check                     # 139 reports
```

Key-stream and endpoint figures were recomputed from the retained
`runs/*/keys.log[.gz]`, `summary.json`, `state.log.gz`,
`messages.log.gz` and `trace-core.jsonl.gz`; dossier hashes from
`record.json` `files_sha256`; upstream commit identities from the local
`borg-reborn-rs` clone.
