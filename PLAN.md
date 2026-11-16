# Milestones

## Owner-directed caster bank (2026-11-16)

The owner requested continued scenario work, prioritizing low-level casters,
different equipment combinations, and extraction from deaths/near deaths.
`synthetic/low-level-casters/` adds a provenance-checked incident candidate index
and a bounded four-class birth matrix. This instruction authorizes that scoped
bank work without changing the frozen M2 Warrior review packet or accepting M1/M2.
Caster equipment application remains reborn #382; unsupported records are
explicitly untested. No P2/P3 population experiment or acceptance tag is implied.

| Milestone | Scope | State |
| --- | --- | --- |
| M1. Recorded runs, replay and human alternatives | Pinned seeded CI; human-readable death and scenario reports; recordings and saved-position trials; case-local launchers; alternative human-play attachment; shared version caches; statistics by build | Prepared for owner-run review; **not accepted** |
| M2 / synthetic P1. Small generated-depth suite | One class, depths 5/10/15, one seed, birth kit plus one observed level tier; deterministic manifests, bounded execution, independent outcome/failure fields, candidate danger screens and reports; pinned cemetery CI | Prepared for owner-run milestone review; not accepted |

The owner instructed continued implementation with review at the milestone.
This selects the bounded synthetic P1 work under #5 and reborn #371. It does
not accept M1, move its review pin, or authorize expansion into synthetic P2/P3.
The existing synthetic-start PRs are integration checkpoints, not a task-level
review stop. The milestone packet will pin both repositories and the real suite.

### M2 / synthetic P1 exit

- Human Warrior, depths 5/10/15, seed 101; birth kit and one level tier derived
  from a real observed run. Record observation provenance and sampling limits;
  do not call a single observed kit a population average.
- A strict declarative build contract applied by reborn without an input save;
  unsupported native item/state features fail visibly rather than disappearing.
- Stable scenario identity independent of the executable under test; explicit
  harness capability, profile/build-catalog digests and exact runtime pins.
- Bounded suite runner and human/machine reports with complete denominators,
  death/survival/stopped separated from failure/mismatch/timeout. Low HP is only
  a candidate screen; qualified null-move coverage/count is unavailable in P1.
- Fake-adapter regression cases, a real six-cell pinned suite and a read-only
  game-execution CI workflow. Synthetic outcomes never enter natural registries.
- Freeze for owner-run milestone review with exact pins, evidence and limitations.
  Qualified null-move diagnostics and wider catalogs belong to P2; paired
  two-build impact comparison belongs to P3.

The owner requested the first milestone review on 2026-11-15 and will choose
or run its reviewer. M2 is separately selected above. Automated causal discovery,
tuning proposals, exact uninterrupted Borg-memory continuation and wider
recorder-version qualification remain future work, not M1 completion claims.

[Milestone M1](https://github.com/diegoami/borg-cemetery/milestone/1) ·
[Review PR #1: main → reviewed](https://github.com/diegoami/borg-cemetery/pull/1).

## M1 boundary

- Baseline: `44d97669ebdf7390b384656c61365b0ca30f3266`, the last commit before
  this implementation session's collection/replay work.
- Implementation head: `cd562eabc40267a15be3eb7d2036d65e6f0c4a5a`.
- [Review packet and evidence](docs/reviews/M1/README.md).
- [Independent reviewer prompt](docs/reviews/M1/PROMPT.md).

`reviewed` is bootstrapped at the pre-M1 baseline so `main` → `reviewed` shows
the milestone's diff. That bootstrap is **not** a claim that the imported
historical data or baseline passed a review. The review PR's body pins the
publication head, which also contains the review/process documents added after
the implementation head. Those documentation-only additions belong to the PR.

The owner decides acceptance and merges the review PR. Only then should the
reviewed boundary advance and an acceptance tag such as `m1` be recorded.
Review findings become explicit follow-up work; unresolved blockers do not
disappear because tests pass.

## Owner-requested redesign proposal

The [controlled-experiment design](docs/cemetery-redesign.md) proposes replacing
routine permanent Git report collection with fixed seed cohorts, exact
build/configuration identities, database-backed attempts, bounded external
evidence and on-demand analysis/reconstruction. Near-deaths require independent
engine evidence; findings feed scenario trials and cohort validation.

The broader database/service redesign remains planning, not an implementation
commitment. Only the bounded synthetic P1 subset selected above is authorized. M1 remains unaccepted; its implementation pin and
existing evidence are unchanged. The proposal includes delivery slices and
acceptance criteria for a later owner decision.


## Owner-selected execution/storage direction (2026-11-16)

[Cemetery #32](https://github.com/diegoami/borg-cemetery/issues/32) records a
Cemetery-first database/artifact design followed by an alternate saved-scenario
executor: local CLI or optional Cemetery CI retains runs and intermediate
checkpoints, while Zoo ingests pinned result snapshots, aggregates them and
owns report presentation. Zoo-executed pinned Cemetery inputs remain supported.
Both modes share one scenario/save/run identity and storage contract.

Joint architecture coordination remains in
[Zoo #114](https://github.com/diegoami/borg-zoo/issues/114); both executor modes
feed [Zoo #144](https://github.com/diegoami/borg-zoo/issues/144).
[Cemetery #31](https://github.com/diegoami/borg-cemetery/issues/31) supplies
living 100k checkpoint/continuation requirements. The
[updated design](docs/cemetery-redesign.md) records the ownership and sequence.
This selects the architecture direction and planning task; the database and
alternate executor are not implemented. M1/M2 acceptance and review pins are
unchanged; no new implementation milestone has started.
