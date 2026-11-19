# Architecture review response and Firebase revision

Status: **proposed corrections, awaiting owner/reviewer confirmation**. No merge,
milestone acceptance or platform implementation is implied.

The [first architecture review](https://github.com/diegoami/borg-cemetery/pull/2#pullrequestreview-5911244495)
reviewed `7d5d1422d4429db932c5f3d3b6279a837ec9123b` →
`d084f13f09e4af8bdf989ad2bdb774db05625d22` and returned **accept with specified
changes**. The PR body pins the new proposal head and its documentation checks.
Existing M1 implementation/evidence remain unchanged.

The owner subsequently proposed a Firebase-like database. The
[backend decision](firebase-backend.md) now recommends Cloud Firestore, Cloud
Storage and Firebase Auth with Hosting/Cloud Run, replacing PostgreSQL/S3 in this
proposal. That is an additional architecture change requiring review, not merely
a database name substitution: query/index plans, application uniqueness, server
authorization, transaction boundaries, TTL and recovery are specified explicitly.

| Finding | Proposed correction | Acceptance reasoning/example |
| --- | --- | --- |
| R1 High: seed-check enum cannot encode verified full-seed survival with missing encounter traces | Replace combined seed states with independent terminal outcome, observation scope, encounter result, death relation and contract validity | verified + alive_at_horizon + full_source_horizon + unknown encounter deactivates the death study without claiming avoidance/recovery |
| R2 High: one priority cannot represent death inactive and hazard active | Introduce immutable study revisions with one objective each; key assessments by study revision, target build/config and applicable hazard qualification contract; share executed check records | One recovery check supports separate death-inactive and hazard-active assessments; execution contracts remain on checks |
| R3 Medium: generic failure reopens the wrong regression | Specify per-objective, compatible-dimension regression triggers and prior/new assessment links | Two successive surviving/avoiding seed runs with unchanged local deaths do not reopen seed-death study; only a pinned local study can have a local regression |
| R4 Medium: source attempt identity collides across zoo runs/producers | Canonical source tuple includes producer/repository, immutable origin result revision/path, suite/cell and execution/attempt coordinates, within workspace/project | Repeated source executions have distinct identities; same-source reimport is idempotent; altered bytes under one qualified identity conflict; retrieval revision is separate |
| R5 Medium: database restore can resurrect dangling replay references | Completed recovery roots preserve metadata plus actual artifact generations; restore fences old jobs and reconciles bytes before availability | Snapshot before unpin/GC remains recoverable through backup-root protection; isolated missing-byte injection yields unavailable/incomplete, never runnable |
| R6 Medium: qualifier changes do not invalidate hazard priorities | Immutable qualification contracts/results; contract change makes hazard projections pending requalification while preserving history | v2 rejecting/recognizing an exposure produces new inactive/active hazard projections, not a Borg-regression claim; only runnable-definition changes require a new scenario revision |

The [scenario contract](scenario-contract.md) supplies the corrected identities,
orthogonal evidence fields, objective-specific transition table and positive/
negative acceptance cases. The [main proposal](../cemetery-redesign.md) mirrors
those rules; the Firebase decision specifies their storage/coordination mapping.

## Boundaries and unresolved work

Keep the review's supported direction: encounter analysis, zoo ownership,
ordinary survivors as controls, explicit restart/continuation modes, namespace
isolation and dependency-aware retention. Database selection does not supply
missing effective-config export, survivor capture, native danger calculations,
encounter anchors, recorder compatibility or private Borg-state restoration.

No Firebase project/rules/indexes, service, games, new fixtures or data migrations
are created by this revision. Local checks validate documentation consistency,
links and whitespace only; existing repository CI exercises existing tools.
Firestore emulators, staging permissions/indexes and recovery fault injection
are implementation acceptance requirements, not tests reported as already run.

The owner chooses whether to obtain another reviewer pass, accept architecture
direction or request more design changes. No reviewer is selected/launched and
neither architecture PR #2 nor milestone PR #1 is merged by this work.
