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
| Source reference | Producer/repository, immutable catalogue/result revision, suite/cell/attempt key, source record digest, original URL and import tool version |
| Starting case | Original seed as represented by its engine, requested/reported seed, engine/RNG family, race/class and birth settings, calendar/options/other randomness, declared clock and stop contract |
| Build | Source and dirty-input digests, exact runtime/data package digests, engine/save ABI, Borg implementation, toolchain/build flags, instrumentation/recorder identities |
| Configuration | Requested profile/overrides, effective resolved settings including defaults, schema/types, core/environment/options and verification status |
| Attempt | Source/start/build/config references, original or diagnostic role, outcome, requested/actual horizons, seed/birth verification, observed progress and evidence manifest |
| Episode | Original attempt, observed start/end/recovery, checkpoint start, event anchors, known context, encounter outcome, independent danger grade and qualifier version |
| Scenario revision | Origin episode, save/checkpoint/runtime dependencies, continuation mode, observation contract, encounter/recovery predicates, follow-up horizon and compatibility requirements |
| Assessment | Scenario revision and target build/config, separate seed/local checks, observation freshness, priority state and reasons/evidence |
| Investigation/trial | Immutable inputs/target, tool/model version if used, actor, hypothesis, execution contract and outcome qualification |

Effective configuration is canonicalized by declared key/type/value semantics,
then hashed. Hash the original bytes separately. Do not collapse missing defaults
into presumed defaults or treat a profile name as identity. Unknown provenance
allows a qualified written investigation, not an exact comparison claim.

Original import uniqueness is scoped to workspace/project/source attempt ID.
Reimport of identical bytes is a no-op; a different digest under that ID is a
conflict requiring a new source correction identity. Diagnostic reconstruction
and human/alternative branches always get new attempt IDs linked to the original.
Neither duplicate imports nor alternative play create new independent lives.

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

## Relevance and investigation lifecycle

The original scenario revision is immutable. Current relevance is a projection
of versioned assessment evidence, keyed by scenario revision + build + effective
configuration + execution contract. A tracked alias such as current resolves to
an immutable target before scheduling. A user's assessment does not alter another
workspace or configuration's queue.

Assessment records its study objective (death manifestation, hazardous recovery
or ordinary battle) and keeps three independent dimensions:

- Seed check: pending, same failure, recovered matched encounter, avoided,
  different later failure, or inconclusive. Terminal run outcome, encounter
  known/unknown and scope (episode follow-up versus full source horizon) are
  separate fields. Seed survival requires a verified living endpoint at the full
  source horizon or an engine-confirmed win under the same ordinary-play contract.
- Local trial: untested, died, survived to horizon, recovered, diverged,
  incompatible or failed. Encounter engagement and continuation mode are explicit.
- Investigation priority: pending revalidation, active, inactive for target,
  regression watch or explicitly pinned study. Reason and supporting checks
  identify who/what changed this priority.

Default transition rules:

1. A new tracked build/config makes prior-target conclusions stale. Import an
   equivalent qualified source result or schedule a missing relevance check.
2. The same death keeps its death investigation active. Verified survival to the
   full seed horizon makes that old death manifestation inactive for the target,
   even if encounter evidence is unknown; preserve that uncertainty and do not
   claim a battle victory. Matched encounter recovery can also close that death
   manifestation, with a later death treated separately.
3. A shorter bounded continuation without the encounter permits only a provisional
   lower priority, not a full-seed survival or resolved-battle claim. Timeout,
   config mismatch and missing seed evidence remain pending/inconclusive. Near-
   death and ordinary-battle studies use their hazard/encounter objective; their
   source surviving is expected and cannot deactivate them by itself. A qualified
   near-death may remain active after the death manifestation is inactive. An
   explicit maintainer pin overrides default priority.
4. Seed survival and local-trial failure can coexist. Prefer investigating current
   observed failures; retain the old tactical fixture only if pinned or selected
   for regression. A new later death becomes a separate episode.
5. A subsequent build's reproduced failure reopens its assessment as a regression.
   Never edit the original run, transfer a fix globally or claim a causal fix
   merely because a newer build survives.
6. Deep-analysis jobs verify the target assessment before dispatch and before
   publication. Mid-job target changes preserve an old-target report, not a
   current-failure claim. Leases/pins protect its inputs until finalization.

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
| Latest build survives the complete seed horizon but encounter traces are missing | Old death investigation inactive for this target; encounter outcome unknown and no tactical fix claim |
| Source of a near-death study survives again with the same qualified exposure | Hazard study stays active; seed survival does not dismiss a study of surviving danger |
| Borg is frightened at safe low HP, and another full-HP Borg survives a potentially lethal burst | First is not a near-death; second can qualify with independent distribution and recovery evidence |
| Ordinary fight is won without lethal exposure | Surviving battle/control scenario; no invented near-death |
| New build arrives during analysis | Old-target report remains labelled; current queue revalidation required |
| Scenario later fails again | New-target regression assessment reopens without rewriting old outcomes |
| Two projects/users both import S0003, or use seed 102 in different engines | Namespaced records and isolated priorities; no implicit save/seed equivalence |
| Artifact hash exists but bytes expired or rebuild diverges | Explicit unavailable/diverged status; no replay or survival claim |
| Imported confirmation/sealed case is requested for exploratory analysis | Reject unless its source owner's policy explicitly authorizes that use |
| Deletion races a new investigation pin | Serialized state transition prevents a successful pin to deleted bytes; job fails/retries visibly if collection already committed |
| Invalid archive paths, unauthorized workspace download or unsupported bundle major version | Reject before extraction/execution or data disclosure |
