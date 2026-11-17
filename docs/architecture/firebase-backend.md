# Backend decision proposal: Firebase

Status: proposed replacement for the PostgreSQL/S3 choice in architecture PR #2.
This is a design update, not a deployment or a claim of working Firebase code.
The [scenario contract](scenario-contract.md) remains the domain model; backend
choice does not change cemetery's boundary with borg-zoo or introduce tuning.

## Choice and tradeoffs

Use **Cloud Firestore, Standard edition**, as the managed document database.
Use **Cloud Storage for Firebase** for artifacts, **Firebase Authentication** for
users, **Firebase Hosting** for human pages, and one **Cloud Run API/coordinator**.
Native capture/replay/analysis workers remain in CI or local isolated processes.
No database trigger runs a game or determines an investigation's truth.

Firestore's collections/documents and indexed compound queries fit source runs,
immutable evidence checks and independent study assessments. This selects
Firestore rather than Realtime Database's single JSON tree; presence/chat-style
synchronization is not the main requirement.
([Firebase database comparison](https://firebase.google.com/docs/firestore/rtdb-vs-firestore).)
Cloud Storage supplies a Google Cloud Storage bucket for file artifacts, and
Hosting can route API requests to Cloud Run.
([Storage](https://firebase.google.com/docs/storage),
[Hosting integration](https://firebase.google.com/docs/hosting/cloud-run).)

The benefit is managed shared documents, identity and web delivery without
operating a PostgreSQL server. The cost is provider dependence and application
ownership of referential integrity, uniqueness, materialized views and access
checks. No SQL foreign keys, arbitrary joins, cross-store transaction or unlimited
ad-hoc query surface is assumed. Portable scenario packages remain independent
of Firebase; a second production backend is future work, not a hidden prerequisite.

## Collections and bounded documents

All authoritative project records live under
`workspaces/{workspaceId}/projects/{projectId}/...`. Membership is at workspace
scope; every document also carries checked workspace/project IDs for queries.
Owner-specific repository names, filesystem paths and Firebase project IDs are
configuration, not keys built into the tools.

| Collection | Contents |
| --- | --- |
| `sourceCases` | Frozen source suite/case provenance and initialization recipe |
| `sourceAttempts` | Fully qualified original execution key, payload digest and local run reference |
| `builds`, `configurations` | Exact runtime/source and complete effective-configuration identities |
| `runs`, `checks` | Original/diagnostic attempts and immutable executed seed/local checks |
| `episodes`, `scenarioRevisions` | Observed battles and runnable scenario definitions |
| `qualificationContracts`, `qualifications` | Versioned danger/recovery definition and evidence-specific results |
| `studies`, `assessments` | Independent objective/revision and target-specific priority projections |
| `artifacts`, `pins` | Object generations, digests, byte ownership and dependency protection |
| `jobs` | Bounded work requests, leases, fencing generation and immutable input references |
| `views`, `reportCache` | Regenerable human-facing summaries, not authoritative evidence |

Use a deterministic digest of each canonical identity tuple as its document ID;
store and compare the original tuple as well. Transactionally create/check that
document to enforce application uniqueness. Never derive an original attempt
from a zoo cell key alone or treat a fresh random Firestore ID as deduplication.
Validate referenced workspace/project/record IDs during writes. The coordinator
is the only authoritative writer, including imports and administrative repairs.

Keep one document per bounded record, not one growing document per seed or build.
Do not embed all a run's thoughts, episodes, trials or assessments in arrays.
Firestore documents have a 1 MiB limit; adopt a lower application document limit
before implementation. Large configuration receipts/observations/manifests become
chunked objects with digests and bounded database summaries.
([Firestore limits](https://firebase.google.com/docs/firestore/quotas).)
Complete effective settings remain retrievable even when the indexed document
only contains their digest and selected searchable fields.

## Queries and indexes

Version the required indexes with deployment configuration. Denormalize small
identity/filter fields into projections and validate/rebuild them from immutable
inputs. Exempt bulky free-form observations/maps and report text from indexing.
Do not promise arbitrary combinations of filters without an index/query plan.
([Index management](https://firebase.google.com/docs/firestore/query-data/indexing).)

| Human/tool query | Planned bounded query shape |
| --- | --- |
| Runs for one build/configuration/seed | `runs` filtered by build/config/case IDs, ordered by execution time and document ID |
| Active death studies for current target | `assessments` filtered by target build/config, objective and priority, with paginated update order |
| Current qualified hazardous recoveries | `assessments` filtered by target, objective, active qualification contract and priority |
| Scenario's alternative attempts | `checks` filtered by scenario revision and target/role, ordered by execution time |
| Fatal/surviving encounters of one mechanism | `episodes` filtered by build/config, encounter family and outcome, ordered by episode time |
| Work ready for lease | `jobs` filtered by state and due time; bounded candidates acquired transactionally |

Each query is workspace/project-scoped and cursor-paginated. Job/assessment
projections contain references to underlying checks and their version/digests.
Reports fetch that bounded evidence manifest, not an unconstrained database scan.
Cross-project administrative queries use authorized server code with explicit
workspace filters. Broad exploratory analysis exports selected metadata to a
bounded analysis job; no second population statistics service is introduced.

## Transactions, workers and pins

Firestore transactions can retry, and they do not include Cloud Storage writes.
Therefore transaction callbacks only validate/update documents; they never launch
games, send work or delete/upload artifacts.
([Transactions](https://firebase.google.com/docs/firestore/manage-data/transactions).)

1. Register an idempotent job with immutable target, study/qualification versions
   and input IDs. Lease acquisition transactionally advances a fencing generation.
2. Trusted publication uploads immutable objects under an isolated staging path.
   Verify size/digest and record the exact Storage object generation. Candidate
   game processes get no database or deletion credentials.
3. Finalization validates job generation, deployment epoch, target freshness and
   verified dependency state, then commits check/manifest documents and a request
   to update affected projections. Object upload and database commit are separate;
   failed finalization leaves a collectable orphan, not a fabricated result.
4. Retried delivery/projection updates use deterministic IDs/input versions. Late
   workers cannot replace new evidence, and stale projections are visibly pending.

An artifact control document records live/deleting/deleted state and a bounded
pin/lease count backed by separate pin records. Acquiring a pin transactionally
checks live state and records ownership. GC's transaction requires no protected
owners, then marks deleting and fences new pin acquisition. Actual generation-
specific deletion happens outside the transaction and is retried idempotently;
only then is the deletion receipt finalized. A deleting generation cannot be
silently reused. Large dependency sets use a retention barrier while staging
bounded pin batches, so partial pin installation is never advertised as a fully
protected replay package. Backup roots participate in the same protection.

Use Firestore TTL only for already detached, independently disposable cache or
completed-receipt documents. TTL is asynchronous, nontransactional and does not
delete subcollections. Authoritative studies, checks, artifact controls, live
leases and dependency pins have no automatic TTL. The API enforces logical
expiry immediately and the coordinator performs controlled retirement/cascade
cleanup; TTL is not the quota or garbage-collection algorithm.
([TTL behavior](https://firebase.google.com/docs/firestore/ttl).)

## Users, permissions and portable execution

Firebase Auth identifies a person; workspace membership defines owner, contributor
or reader permissions. The API verifies identity, membership and project/job
scope on every operation. Only bounded presentation documents may be read through
client SDKs under matching read rules; client writes to authoritative collections
are denied. Public publication creates an explicit sanitized view/package rather
than exposing private evidence by changing a broad collection rule.

Server/Admin SDKs bypass Firestore Security Rules and use IAM. Thus browser rules
alone do not enforce multi-user isolation: API checks, limited service identities
and server-path tests are required. Worker access is job-scoped, with expiring
artifact grants; workers cannot self-assign another workspace or target.
([Firebase authorization](https://firebase.google.com/docs/firestore/security/rules-conditions).)
Private artifact downloads are authorized through the API with short-lived
access, not public bucket listing. Sharing preserves explicit dependency access.

A maintainer may join a shared installation or deploy the documented project into
their own Firebase account. Local API development uses Auth/Firestore/Storage
emulators with isolated test data; downloaded native bundles play offline without
Firebase. Emulators are not a production self-hosted backend.
([Emulator scope](https://firebase.google.com/docs/emulator-suite).)
Rules, index requirements, IAM, collection isolation, transaction contention and
real object generations must also be checked in bounded staging qualification;
emulator checks alone are not deployment evidence.

## Coordinated recovery across documents and artifacts

Invariant: **every completed recovery snapshot retains the actual immutable
artifact generations required by its core metadata until that snapshot expires**.
Keeping an object hash or an independently scheduled database backup does not
meet this invariant. Storage soft delete/versioning may add protection but is
not a substitute for an explicit recoverable dependency set.

Initially support bounded application recovery snapshots with a short workspace
maintenance window, rather than claiming an arbitrary coordinated PITR horizon:

1. Fence new workspace core writes/GC, drain in-flight finalizations and hold a
   retention barrier. All authoritative writers honor this maintenance epoch.
   Core documents have no automatic TTL; report caches are outside the snapshot.
2. Export the stable core documents and enumerate their required artifact
   generations. Install recovery pins, verify actual bytes/digests, and retain
   those generations or verified recovery copies in the protected namespace.
3. Publish a complete immutable recovery manifest outside the live database,
   naming metadata export, required objects, epoch and expiry. Incomplete
   snapshots are never advertised as restorable. Release the maintenance window.
4. Keep recovery roots discoverable independently of restored metadata; GC honors
   every unexpired completed root. Count exports/copies/pinned generations against
   the recovery budget and retire roots explicitly before releasing their pins.
   An initial seven-day daily-snapshot window is a proposal to cost/qualify, not
   a current recovery guarantee. Do not exceed quotas by silently adding snapshots.
5. Restore with serving/jobs/GC paused into a new deployment/restore epoch stored
   outside the restored workspace snapshot. Old leases, grants and queued job
   generations are fenced. Rebuild pins/projections from the selected manifest
   and still-live external recovery roots, then reconcile referenced object
   generations and bytes before declaring availability or running dependent jobs.
   Missing bytes produce unavailable/incomplete state and blocked/retryable work.

Workspace membership and current publication/access policy belong to the control
plane, not the rolled-back project evidence snapshot. Restored views remain
private until rebuilt under current authorization. A data restore cannot restore
an old membership grant or public sharing decision by itself.

Firestore's managed export can include changes made during export, so an ordinary
live export is not treated as a frozen coordinated snapshot. A later PITR design
would need an equally explicit artifact-retention invariant.
([Export semantics](https://firebase.google.com/docs/firestore/manage-data/export-import).)

Required restore exercise: snapshot a runnable scenario, release its ordinary
study pin, and run GC. Its backup root must preserve recoverable bytes. Restore
the older metadata and prove reconciliation and new-epoch fencing before work
resumes. Also deliberately remove a dependency in an isolated recovery test and
prove it becomes unavailable, never runnable from its digest alone.

## Cost and implementation boundary

Budget document reads/writes and listener refreshes, indexes, artifact bytes and
egress, runtime caches and recovery generations. Use paginated bounded views,
coalesced state updates and per-workspace/job admission limits; never stream game
ticks into a live Firestore document. Provider billing is metered, and production
Cloud Storage for Firebase requires a billing-enabled Blaze project. No free-tier
or hard provider-spend cap is assumed.
([Firestore billing](https://firebase.google.com/docs/firestore/pricing),
[Storage billing requirements](https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024).)

Implementation must first qualify representative queries/indexes, authorization,
transaction races, large-document boundaries, artifact finalization and coordinated
restore using synthetic fixtures, then retained real scenarios. No Firebase
project, billing account, rule, index, cloud job or deployed application is created
by this PR. The owner still decides architecture acceptance and implementation.
