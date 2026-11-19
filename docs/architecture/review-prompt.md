# Architecture review prompt

The owner selects and runs the reviewer. This is a design review of the proposed
battle-scenario laboratory, not an M1 implementation review, an acceptance tag or
authorization to implement/deploy. Implementer: Codex/OpenAI GPT family; if a
model reviews, the repository asks for a different family. No reviewer is launched
as part of preparing this PR.

## Scope and exact pins

Use the **baseline and proposal head in the architecture PR body**. Fetch those
commits and inspect only that exact diff in an isolated checkout. The proposed
branch targets main; the separate M1 review targets reviewed. Do not merge either
PR, select another milestone, run games, alter evidence or change another repo.

Read AGENTS.md, PLAN.md, [the proposal](../cemetery-redesign.md) and
[the scenario contract](scenario-contract.md), the
[Firebase backend decision](firebase-backend.md), and the
[response to the first review](review-response.md). Read README navigation changes and
the earlier-pipeline scope correction. Distinguish implemented M1 capabilities
from proposed service capabilities; this PR contains documentation only.

Reference inspected integration sources at borg-zoo
`912ecb13bb08e99f6d57b381a10b794e22e3423c`: docs/DESIGN.md, zoo/evidence.py and
zoo/borgrs.py. The architecture links those exact sources. Do not assume producer
hooks, surviving traces, exact configuration introspection or private-state
restoration exist merely because the proposal requires them.

## Questions to audit

1. Does the scope actually center on studying and reproducing surviving/fatal
   battles? Does any component accidentally recreate zoo's population scheduler,
   performance dashboard, sealed-suite exploration or parameter optimization?
2. Can thousands of fixed source cases yield useful, diverse battle scenarios
   without permanently archiving every trace/report? Are the discovery target,
   deep-game coverage and detailed-storage quota treated separately?
3. Are seed, source run, diagnostic rerun, episode, immutable scenario and
   target-build assessment distinct? Can duplicate imports, colliding IDs or
   different effective defaults corrupt identity or outcomes?
4. Trace every acceptance example in scenario-contract.md. In particular, does
   unexpected seed survival stop wasted investigation without fabricating direct
   battle success? Can later death, avoidance, an unknown encounter and a failing
   old checkpoint all coexist honestly? Does a later regression reopen correctly?
5. Is near-death qualification independent of Borg fear, with adequate calibration
   and unavailable states? Can it handle scheduling/multiple attacks? Are ordinary
   surviving encounters retained without falsely calling them near-deaths?
6. Can packages reproduce their advertised continuation mode? Audit hidden Borg
   memory, baseline reproduction, engine/save compatibility, nondeterminism,
   calendar/random inputs, runtime dependencies and actual versus inferred starts.
7. Does a second maintainer/project have a workable adapter/export path without
   Diego's directory layout or account? Audit namespaces, permissions, offline
   bundles, untrusted execution and explicit sharing of replay dependencies.
8. Walk runner loss, duplicate/altered imports, stale publication, new-build arrival,
   source artifact expiry, quota exhaustion, garbage-collection/pinning races and
   backup recovery. Are availability and missing evidence honest in the UI?
9. Are components and delivery slices proportionate? Assess Firestore document/
   index/query boundaries, application-enforced uniqueness/references, Auth/rules
   versus server IAM, TTL limitations, transaction side effects and cross-store
   recovery. Can the shared installation stay bounded without pretending the
   emulators are a self-hosted production backend?
10. Are the human report, replay commands, inventory/thoughts/animation and
    maintainer feedback useful? Is the proposed investigation broad enough to
    discover behavior/code defects, without automatic tuning or causal overclaim?

For the follow-up revision, re-audit all six findings from review
`5911244495` at `d084f13f09e4af8bdf989ad2bdb774db05625d22` against the new head
pinned in the PR body. Especially check independent outcome/scope/encounter axes,
per-study priorities, dimension-specific regressions, fully qualified source
executions, restore after artifact collection and qualifier invalidation. Treat
the review response as proposed corrections, not as reviewer acceptance.

## Deliverable

For each finding give severity, document/section, a concrete failure scenario,
consequence and recommended architecture correction. Separate design defects,
implementation prerequisites, unresolved owner choices and optional extensions.
List assumptions and what you did not inspect. Finish with **accept direction**,
**accept with specified changes**, or **redesign required**; this is not milestone
acceptance. The owner decides next work and merging.

No code tests can prove an unimplemented architecture. Review state/identity and
failure cases as design arguments; do not invent operational validation receipts.
