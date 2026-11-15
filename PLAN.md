# Milestones

| Milestone | Scope | State |
| --- | --- | --- |
| M1. Recorded runs, replay and human alternatives | Pinned seeded CI; human-readable death and scenario reports; recordings and saved-position trials; case-local launchers; alternative human-play attachment; shared version caches; statistics by build | Prepared for owner-run review; **not accepted** |

The owner requested the first milestone review on 2026-11-15 and will choose
or run its reviewer. No next milestone is selected. Automated causal discovery,
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

This is planning requested by the owner, not a selected next milestone or an
implementation commitment. M1 remains unaccepted; its implementation pin and
existing evidence are unchanged. The proposal includes delivery slices and
acceptance criteria for a later owner decision.
