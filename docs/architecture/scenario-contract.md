# Proposed scenario and integration contract

Companion to the [architecture proposal](../cemetery-redesign.md). All operations
and schemas here are proposed, not existing service endpoints. The contract is
portable across projects; native game formats stay adapter-specific.

## Identities and invariants

Every record carries a schema name/version, workspace, project, immutable ID,
creation time and provenance. Local display names such as D0007 or S0003 are
aliases; they never collide with another registry's IDs or establish equivalence.
Unknown fields may be retained, but an unsupported major schema cannot execute.

| Document | Minimum contents |
| --- | --- |
| Source reference | Producer namespace/repository, immutable origin dataset/result revision and path, suite/cell, source execution/attempt coordinates, record digest, retrieval revision/URL and import tool version |
| Starting case | Original seed as represented by its engine, requested/reported seed, engine/RNG family, race/class and birth settings, calendar/options/other randomness, declared clock and stop contract |
| Build | Source and dirty-input digests, exact runtime/data package digests, engine/save ABI, Borg implementation, toolchain/build flags, instrumentation/recorder identities |
| Configuration | Requested profile/overrides, effective resolved settings including defaults, schema/types, core/environment/options and verification status |
| Attempt | Source/start/build/config references, original or diagnostic role, outcome, requested/actual horizons, seed/birth verification, observed progress and evidence manifest |
| Episode | Original attempt, observed start/end/recovery, checkpoint start, event anchors, known context, encounter outcome, independent danger grade and qualifier version |
| Scenario revision | Origin episode, save/checkpoint/runtime dependencies, continuation mode, observation/encounter contract, runnable endpoint/follow-up and compatibility requirements |
| Qualification contract/result | Immutable evaluator/mechanics/threshold/recovery definition; separate result over an episode/input digest under that definition |
| Evidence check | Immutable executed check, execution contract, terminal outcome, encounter result, scope, death relation, validity and evidence references |
| Study revision | Stable study ID/revision, scenario revision, one objective and admissible evidence contracts; objective-specific priority policy |
| Assessment | Study revision + target build/config + hazard qualification contract where applicable; shared-check references, freshness, independent priority and reasons |
| Investigation/trial | Immutable inputs/target, tool/model version if used, actor, hypothesis, execution contract and outcome qualification |

Effective configuration is canonicalized by declared key/type/value semantics,
then hashed. Hash the original bytes separately. Do not collapse missing defaults
into presumed defaults or treat a profile name as identity. Unknown provenance
allows a qualified written investigation, not an exact comparison claim.

The logical source cell identifies suite revision, specimen/profile and starting
case. It is not an execution. Original attempt uniqueness is the canonical tuple:

```text
workspace + project + producer namespace/repository
  + immutable origin dataset/result revision and result path
  + suite/cell + source execution key + source attempt key
```

For zoo, include its result run directory/workflow execution and attempt, not
only its cell key. Two producer repositories or two measured executions of the
same cell remain distinct. The origin revision belongs to that execution's
immutable published result/version; a newer commit used to retrieve unchanged
results is recorded separately and does not create another execution. An adapter
must resolve this origin consistently; missing execution identity stays explicitly
unqualified rather than inventing unrelated IDs on each import.

Reimport of identical bytes under that qualified key is a no-op; altered bytes
are a conflict requiring an explicit new source correction identity and a link
to the superseded record. Source-declared repeated primary runs and retries keep
their execution/attempt coordinates and roles. Diagnostic reconstruction and
human/alternative branches get separate local attempt IDs linked to the original.
None of these becomes another independent seed case. Firestore transactionally
creates a document keyed by a digest of the canonical tuple and checks the full
stored tuple/payload; backend-generated random IDs alone cannot enforce this.

## Episode and replay package

A package contains a manifest with schema/version, provenance, byte sizes,
digests, dependency graph and licenses/redistribution status; a readable README;
original save and required runtime/data or verified resolvable dependency pins;
configuration and initialization receipts; available input/state streams; and
the scenario's observation/encounter contract. A metadata-only export declares
missing dependencies and cannot advertise standalone replay. Public export must
include or arrange authorized access to every dependency it promises.

An observation names its native tick, player-decision and engine-event indices,
plus energy/scheduling information where available. A trace records what the Borg
knew separately from diagnostic engine truth. No lossy universal turn conversion
is used to qualify equality between C and Neo or different harness frontends.

An encounter anchor uses supported game facts: actors/positions relative to the
verified checkpoint, first interaction event, relevant terrain/resources and
trace-prefix digests. Anchor version, tolerances and unavailable observations
are explicit. A killer name, minimum HP or nearby turn number is insufficient.
Changed encounter predicates create a new scenario revision and require new
assessments; reports never silently broaden a battle to manufacture a match.

Both continuation modes declare which private Borg state is restored or reset.
For a shared-save trial, baseline and candidate use the same bytes/RNG, equal
memory-reset semantics, ordinary-play options and follow-up rules. First verify
the baseline under that mode. If a fresh-Borg control does not reproduce the
original death, it remains a position benchmark; an alternative survivor is not
a demonstrated rescue of the original uninterrupted failure.

Each result distinguishes loaded start, anchor reached, battle engaged/avoided,
alive at horizon, sustained recovery and terminal death. Later death remains
visible. Survival ends at a declared horizon; it is not indefinite survival.
Missing observations cannot establish that an encounter was avoided.

## Danger qualification

Encounter outcome and danger are independent fields. A surviving normal fight
is eligible for study; it need not pass a near-death threshold. Danger grades
are death, qualified near-death, hazard candidate, rejected candidate or unknown.
Only engine-confirmed death counts as death; Borg fear cannot qualify a near-death.

A near-death certificate names the exposure event/window, qualifying mechanic,
actual attack/status/energy facts, evaluated legal outcome distribution and
independent calculation/version, calibrated probability criterion and observed
recovery interval. Calculation cannot reuse a Borg fear value as ground truth.
Full-HP lethal exposure can qualify; safe low HP and impossible attacks must not.
Where a mechanic cannot be independently checked, retain a candidate label.

Forked diagnostic outcomes, if an engine supports them, identify exactly what
randomness changed and the common state. They estimate only that conditional
local experiment; changing the seed and world is not another roll of the same
battle. No invented probability is inferred from a single surviving trace.

A qualification contract has an immutable ID/digest covering evaluator version,
supported mechanics/scheduling, probability threshold, exposure boundaries and
sustained-recovery semantics. Qualification results are keyed by episode/input
digest + contract, with qualified/rejected/unknown/pending status and reasons.
They are separate from observed run outcome and from immutable runnable saves.

When the project's active qualification contract changes, affected hazard-study
projections become pending requalification. Reuse retained observations or verify
reconstruction; missing inputs stay unknown. Preserve old-contract results as
historical, and do not mix them into the current hazard queue or regression
comparison. A lost qualification deactivates that hazard objective under the new
contract; a gained qualification activates an existing hazard study or creates
one linked to the same episode. This is a definition change, not a Borg regression.

Changing only diagnostic evaluator/threshold/recovery semantics creates new
qualification results/projections, not a scenario revision. Changing the runnable
start, encounter anchor, save/continuation semantics or execution endpoint/window
does create a new scenario revision. If a new qualifier needs observations beyond
the retained window, request more evidence or report unknown; do not silently
extend a package's advertised execution contract.

## Relevance and investigation lifecycle

The original scenario revision and every executed evidence check are immutable.
Each check owns its actual execution contract; studies may share it without
duplicating execution or giving the check an investigation priority.

Check fields are genuinely orthogonal:

| Field | Closed values/meaning |
| --- | --- |
| Terminal outcome | alive_at_horizon, win, death, stall, policy_stop, timeout, failure, unknown |
| Observation scope | full_source_horizon, episode_follow_up, saved_position_trial |
| Encounter result | matched_death, matched_recovery, engaged_unresolved, avoided, unknown |
| Death relation | matched_original_manifestation, different_later_failure, unknown, not_applicable |
| Contract validity | verified, incomplete, mismatch, unsupported, diverged |

Record requested/actual horizons, ordinary-play/seed/config verification and
continuation mode alongside these fields. Full-seed survival is the derived
predicate verified + full_source_horizon + alive_at_horizon (or win under the
source completion contract). Encounter result may independently be unknown.
Missing encounter traces forbid avoided/matched_recovery, but do not invalidate
a separately verified full-horizon terminal receipt. Missing terminal/config
evidence does invalidate the corresponding seed-survival claim. Check scheduling
state such as not-yet-executed belongs to its job, not a synthetic gameplay result.

A study revision names one closed objective: **death_manifestation**,
**hazardous_recovery**, **ordinary_battle**, or **local_tactical_regression**.
Separate studies may share a scenario and its checks. Their relevance identity is:

```text
workspace/project + study revision + target build + effective configuration
  + qualification contract (hazardous_recovery only; otherwise not_applicable)
```

The study revision specifies its original manifestation/encounter predicate and
which execution contracts/scopes are admissible. Changing that policy versions
the study, rather than changing a check's historical contract. Each assessment
has its own pending_revalidation, active, inactive_for_target or regression_watch
priority, evidence dependencies and reasons. An explicit maintainer pin is an
independent override. Thus death=inactive and hazard=active can coexist for the
same build/configuration and same qualified recovery check.

Default transitions below require verified checks admissible to that study:

| Objective and evidence | Projection/transition |
| --- | --- |
| Death: full-source alive_at_horizon/win, encounter unknown or avoided | inactive_for_target; no claim of direct battle success |
| Death: matched_recovery in original-seed encounter, followed by a different later death | Original death study inactive; link a separate later-failure episode |
| Death: full-source death with matched_original_manifestation | active; if the compatible prior target was inactive, link a death regression |
| Death: full-source survival plus death only in saved_position_trial | Death study stays inactive; local result belongs to a separate tactical study |
| Death: only a short episode follow-up without encounter, or invalid/incomplete check | pending_revalidation or explicitly provisional lower priority; no full-seed-survival claim |
| Hazard: qualified exposure/recovery under the active qualification contract | Hazard study active regardless of seed survival; death study can independently be inactive |
| Hazard: requalification rejected under a new contract | New-contract hazard projection inactive; preserve old-contract evidence without a Borg-regression label |
| Ordinary battle | Explicit study objective/pin determines relevance; seed survival alone does not close it |
| Local tactical regression: compatible pinned position fails after a verified prior local recovery | Reopen only the local study; no automatic reopening of the seed-death study |

Regression links name prior and new target assessments, objective, compatible
execution/qualification contracts and actual check IDs. A different killer name
or local-only death cannot substitute for a matched seed-death manifestation.
If two later builds both avoid the encounter in their surviving full seed and
both die in the old checkpoint, the seed-death study stays inactive: neither a
new seed regression nor a newly introduced local regression is demonstrated.
Unknown matches stay pending or create separate observed episodes. Preserve
conflicting verified evidence explicitly instead of selecting a favorable retry.

A new tracked build/config makes old-target priorities stale and queues missing
checks. A qualification-contract change invalidates hazard projections only;
death/ordinary studies do not inherit its semantic change. Deep-analysis jobs
check target and qualification freshness before dispatch and publication. If the
target changes mid-job, retain an old-target report and revalidate the current
queue. Evidence leases and restore/deployment epochs fence late workers. A user's
study never changes another workspace/configuration's priority.

## Adapter and service surface

Adapters advertise versions and capability levels independently: metadata import,
chronology, independent danger evidence, reconstruction, save trials, recorder
rendering and private continuation. Unavailable capabilities degrade explicitly;
they never substitute another Borg or create fake saves/screens.

Proposed adapter operations: describe capabilities; normalize a source run;
resolve/prepare an exact runtime; capture/reconstruct an attempt; verify an
encounter anchor; execute a supported scenario; and render actual recorded frames.
Native harnesses remain the execution authority. Candidate code runs isolated;
parsing/importing a bundle never executes it.

Proposed coordinator operations: register projects/builds/configurations; ingest
source manifests; list runs/episodes; promote a scenario; track a build; request
revalidation, investigation or local trial; fetch a readable report/bundle; and
plan/apply retention under workspace policy. All writes are workspace-authorized
and idempotent. Uploads use expiring job-scoped grants; finalization checks the
lease generation, immutable target and complete verified artifact manifest.

Links to zoo are read/import contracts. Suggested future producer hooks export
run identity plus an evidence inventory and an optional short-lived artifact
locator. Cemetery can copy/pin selected evidence before expiry. No zoo write
permission, new population scheduler, automatic parameter search or mandatory
cemetery server is added to a Borg's normal game execution.

## Review acceptance examples

| Situation | Required result |
| --- | --- |
| Latest build survives seed 102 by avoiding Fang, but dies when loaded into the old position | Full-seed avoidance and local death both recorded; old failure deprioritized for latest build; no direct-fight success claim |
| Latest build recovers from Fang, then dies to a different enemy later | Local recovery retained; later death linked as a new episode; seed not labelled a surviving run |
| Latest build survives only to a point before the old death/follow-up | Inconclusive relevance check; no automatic resolution |
| Latest build survives the complete seed horizon but encounter traces are missing | verified + alive_at_horizon + full_source_horizon + encounter unknown; death study inactive and no tactical fix claim |
| Source of a near-death study survives again with the same qualified exposure | Hazard study stays active; seed survival does not dismiss a study of surviving danger |
| Same matched encounter recovers with qualified exposure on one build/configuration | Separate death and hazard assessments share the check: death inactive, hazard active; neither overwrites the other |
| Borg is frightened at safe low HP, and another full-HP Borg survives a potentially lethal burst | First is not a near-death; second can qualify with independent distribution and recovery evidence |
| Ordinary fight is won without lethal exposure | Surviving battle/control scenario; no invented near-death |
| New build arrives during analysis | Old-target report remains labelled; current queue revalidation required |
| A later compatible full-seed check reproduces the original death after prior seed survival | Reopen only that death study, linking old/new target assessments and check IDs |
| Two later builds both survive by avoiding the encounter but both die in the old save | Seed-death study remains inactive; no newly introduced local regression is inferred from an unchanged local failure |
| A pinned local position fails after a compatible previous local recovery | Reopen only the local-tactical study; seed-death relevance still follows seed evidence |
| Two producer repositories or two zoo result executions reuse one cell key | Distinct fully qualified source attempt identities; unchanged reimport is a no-op and altered bytes under one qualified key conflict |
| Qualifier v2 rejects v1 exposure, or newly qualifies an earlier unverified exposure | Hazard projection pending then inactive/active under v2; preserve v1 results; no Borg-regression label or unnecessary scenario rewrite |
| Qualifier needs a different runnable endpoint or encounter anchor | New scenario revision plus compatible checks; no silent endpoint/predicate mutation |
| Two projects/users both import S0003, or use seed 102 in different engines | Namespaced records and isolated priorities; no implicit save/seed equivalence |
| Artifact hash exists but bytes expired or rebuild diverges | Explicit unavailable/diverged status; no replay or survival claim |
| Imported confirmation/sealed case is requested for exploratory analysis | Reject unless its source owner's policy explicitly authorizes that use |
| Deletion races a new investigation pin | Serialized state transition prevents a successful pin to deleted bytes; job fails/retries visibly if collection already committed |
| Restore a metadata snapshot taken before a later ordinary unpin/GC | Recovery root preserves required generations; reconciliation/new worker epoch precede availability and job dispatch |
| Recovery dependency is deliberately missing in an isolated restore test | Mark unavailable/incomplete and fence affected jobs; a restored pin/digest alone is not runnable evidence |
| Invalid archive paths, unauthorized workspace download or unsupported bundle major version | Reject before extraction/execution or data disclosure |
