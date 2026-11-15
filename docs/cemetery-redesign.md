# Architecture proposal: a shared laboratory for Borg battle scenarios

Status: **proposed for architecture review; no implementation authorized by this
document**. This revision incorporates the owner's clarification: cemetery studies
battle scenarios and how Borgs survive or die. Borg-zoo owns population comparisons.
Configuration is recorded as evidence; parameter search is outside this design.
The earlier 64-case evaluation proposal is superseded.

Read the [scenario and integration contract](architecture/scenario-contract.md)
for identities, state transitions, adapter operations and acceptance examples.
The [review prompt](architecture/review-prompt.md) defines this review. M1 remains
unaccepted and its implementation boundary is unchanged.

## 1. Purpose and ownership

The questions are: what happened in this encounter, what did the Borg know, why
did it die or recover, and can another implementation survive the same position?
Study surviving battles as well as deaths. Preserve executable situations with
their context, and stop spending analysis effort on an old failure once it no
longer affects a project's tracked build. A useful outcome is an explanation,
reproduction and focused regression case for the Borg maintainer.

| Owner | Responsibility |
| --- | --- |
| Borg-zoo | Seed suites, population experiments, broad build/configuration comparisons, performance statistics and any confirmation/sealed-suite policy |
| Cemetery | Encounter discovery, death/near-death qualification, scenario packages, reconstruction, local trials, human reports and current-build relevance |
| Borg/engine project | Gameplay, instrumentation, configuration export, native build/run/save support and any private-state transfer contract |
| Project maintainer | Tracked builds/configurations, investigation priorities, proposed gameplay changes and acceptance |

Cemetery does not own an optimizer, population scoreboard or experiment scheduler.
It does not sweep parameters, select a winning profile or assert population
survival gains from its selected scenarios. Configuration variants describe what
was played. An explicitly requested alternative build/configuration may be tried
on a scenario, but it is an investigative trial, not an automatic tuning loop.
Broader validation of a gameplay change belongs in zoo.

This boundary follows the inspected
[zoo design at 912ecb13](https://github.com/diegoami/borg-zoo/blob/912ecb13bb08e99f6d57b381a10b794e22e3423c/docs/DESIGN.md).
It is an integration proposal, not a claim that zoo already exports cemetery
scenario packages or that either repository has been changed to do so.

## 2. Discover over thousands of fixed starting cases

Select a frozen manifest of **many thousands of discovery cases**, initially
targeting **8,192 cases per project** across approved source suites. This is an
operational starting target for encounter diversity, not a statistical power
claim or a hard ceiling. Support larger catalogues and deep-game sources; report
coverage by character, depth and encounter mechanism. Tens of cases are suitable
only for testing the pipeline. Thousands of town deaths still provide little
coverage of a late-game battle.

Reuse zoo's eligible development/discovery suites and their exact birth rules,
caps and seed identities. Where additional cases are needed, their source owner
registers another frozen discovery manifest. Do not silently modify suites,
reinterpret a seed under another engine, or open confirmation/sealed inputs for
exploratory analysis. The 8,192-case catalogue does not exist yet; no seeds are
generated or suites unsealed by this PR. A project without zoo can supply the
same versioned manifest through a native importer.

This catalogue is a source index, not a requirement to rerun every case in
cemetery for every build. Import qualified zoo results first. Request additional
captures only for missing encounter evidence, scenario creation or relevance
checks. Imported original runs and diagnostic reruns have different attempt IDs;
never replace a measured zoo run with a cemetery rerun.

Keep a few tracked builds per project, initially reference/current/previous,
with explicit effective configurations. A thousand indexed outcomes can be
cheap while only a small subset has detailed traces or active investigations.
The detailed scenario-bank quota is independent of discovery catalogue size.

## 3. Components and deployment

```mermaid
flowchart TD
    Z[Zoo runs and evidence] --> I[Versioned import adapters]
    N[Other project harnesses] --> I
    I --> C[Cemetery API and job coordinator]
    C --> D[(Run and scenario documents)]
    C --> O[(External artifact store)]
    C --> W[Isolated CI or local workers]
    W --> C
    C --> H[Human scenario pages and replay bundles]
    H --> B[Borg maintainer investigation and code changes]
    B --> Z
```

Use one PostgreSQL database with constrained identity/status columns and JSONB
for versioned configuration, episode and analysis documents. PostgreSQL provides
indexed JSONB and compound uniqueness/foreign keys; these fit evolving evidence
documents with stable relationships.
([JSONB](https://www.postgresql.org/docs/current/datatype-json.html),
[constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).)
Use an S3-compatible object store for compressed traces, saves, runtime packages,
recordings and report caches. Provider and deployment budget remain review/deploy
decisions; this proposal provisions neither.

The coordinator can use database-backed jobs initially. Workers run in GitHub
Actions or locally through the same API and artifact interface. A local install
uses the same schema plus a filesystem artifact backend. No Kubernetes, separate
message broker, search cluster or hosted AI service is required. An analysis
worker can be a deterministic tool, a human-assisted process or an optional model;
scenario storage and replay do not depend on an AI provider.

## 4. Identity and stored records

| Record | Stable identity and purpose |
| --- | --- |
| Workspace/project | Owner namespace, permissions, adapter and engine family; supports independent users/installations |
| Source case | Source catalogue revision, seed and complete birth/initialization contract |
| Build/configuration | Immutable source/runtime/data identity plus resolved effective settings; display labels can point to newer identities |
| Run attempt | Original source run identity or separate diagnostic execution, actual outcome, provenance and available evidence |
| Episode | Observed encounter sequence within one attempt: boundaries, context, outcome and danger qualification |
| Scenario revision | Immutable runnable start and observation/encounter contract derived from an episode |
| Build assessment | Scenario relevance for one tracked build/configuration, with separate full-seed and saved-position results |
| Investigation/trial | Exact evidence and tool versions, target scenario/build, hypothesis, executed alternative and qualified outcome |
| Artifact/pin/job | Digests, locations, dependency owners, retention state, worker leases and deletion receipts |

A seed is essential provenance but is not a globally unique scenario. The same
seed can contain several battles; different engines give it different meaning.
One encounter may have several checkpoints. Merge duplicate imports by source
identity and payload digest; group related encounters for browsing without
merging distinct original lives or replacing their evidence.

Build identity includes repository, resolved commit, source-input digest,
clean/dirty status, executable/runtime/data digest, compiler/build flags and
instrumentation versions. Configuration records requested overrides **and all
effective defaults**, selected core, native options and relevant environment.
Retain source bytes for dirty inputs or label reconstruction unavailable.
Unknown settings stay unknown; they cannot support a controlled equivalence claim.

Every observation identifies engine tick, player decision and engine event where
available. Keep counters distinct. Outcome labels include death, recovery,
ongoing encounter, alive at horizon, win, stall, policy stop, timeout, failure and
identity/configuration mismatch. A living final sample is not proven recovery.

## 5. Encounters, deaths and genuine near-deaths

An episode starts at the last supported reasonably stable state before tactical
interaction and follows deterioration, engagement, escape, death or recovery.
Extend it backwards when a preparation decision or resource shortage explains
the battle. There is no fixed preceding 10/20/30-turn rule. Record the inferred
boundary, its uncertainty and the actual earlier checkpoint used for replay.

Keep **outcome** separate from **danger qualification**. A routine battle that
the Borg survives is useful evidence and a control, without being a near-death.
Candidates include real deaths, independently detected damage/exposure, Borg
alarms and representative ordinary encounters. Borg fear or low HP alone never
qualifies a near-death.

The initial near-death qualifier verifies a credible lethal exposure from
engine mechanics: hostile actions/residual effects due before the next legal
player decision, actual speed/energy ordering, attack eligibility, hit/damage
distributions, resistances and status effects. A theoretical maximum-damage roll
alone is insufficient. Require a calibrated nontrivial lethal probability and
then observed sustained recovery. Unsupported or incomplete mechanics produce
an unverified candidate, not a fabricated risk score. Other hazard families
need their own reviewed qualifier; strategic starvation is not automatically a
battle near-death.

Calibration uses reviewed positive and negative fixtures, including safe low HP,
fear without an attack opportunity, fast multiple attacks and high-HP lethal
bursts. Sample non-triggered surviving fights to find misses. Version the
qualifier and boundary/recovery rules; threshold values remain pilot findings.
Engine truth is diagnostic evidence and must be separated from what the Borg
could observe. Investigations can explain unknown threats without giving tested
Borgs access to hidden game information.

## 6. Capture and reconstruct executable situations

Import a source's actual evidence inventory and verify retrieved bytes before
claiming durable capture. Zoo's inspected
[evidence inventory](https://github.com/diegoami/borg-zoo/blob/912ecb13bb08e99f6d57b381a10b794e22e3423c/zoo/evidence.py)
describes file hashes and missing files; it is not replay qualification. Its
[borg-rs adapter](https://github.com/diegoami/borg-zoo/blob/912ecb13bb08e99f6d57b381a10b794e22e3423c/zoo/borgrs.py)
has an evidence-retention mode; without it some non-death streams are discarded.
Do not assume surviving battles or private Borg state were recorded historically.
An opt-in producer export/retention hook is future integration work.

During an instrumented run, use periodic checkpoints, a bounded recent trace
buffer and a compact complete replay recipe/input stream. Triggers preserve
checkpoint/context chunks, including surviving encounters, before buffer expiry.
Generate a scenario package containing verified save bytes, engine RNG, runtime
and data dependencies, effective settings, knowledge/inventory observations,
encounter anchors, outcome/recovery criteria and replay instructions. Original
evidence remains immutable when a report or scenario definition is revised.

Two modes must remain explicit:

- **Shared engine save, fresh Borg state:** baseline and alternative load the
  same save/RNG with equally reset Borg state. Useful for position studies and
  supported by the current runner; not the original uninterrupted decision.
- **Original-prefix continuation:** compatible private-state restoration or a
  verified prefix replay to a supported intervention/state-transfer boundary.
  This stronger capability is adapter-specific and not yet implemented here.

Reconstruction requires the exact runtime/data/configuration and all relevant
birth/time/random inputs, plus checkpoints/input streams where needed. A seed
alone is insufficient. Qualify it by matching intermediate world/input digests,
scenario anchor and outcome; reject divergence. Rebuilding from source is a
fallback whose bytes/behavior must be verified. Save compatibility and Borg-state
compatibility are distinct gates. Failure to load or a silently new character
cannot count as surviving a scenario.

## 7. Revalidate relevance before spending analysis effort

A scenario revision preserves its original position and outcome. A new build
creates a new assessment, not a rewritten death account. Assessment belongs to
one project/build/**effective configuration**; another user's result cannot
silently resolve it globally.

When a tracked build changes, import any equivalent source result first, then
queue missing relevance checks for the project's active investigations. Keep
bounded episode-follow-up checks separate from full-seed results: surviving a
seed means a verified living endpoint at its complete original source horizon,
or an engine-confirmed win, under the same birth/ordinary-play contract. Local
follow-up extends past the old episode through its declared recovery window.
Explicitly check whether the encounter occurred where evidence permits. A short
run, stall, failed reconstruction or mismatched contract cannot establish seed
survival. Prioritize active cases; do not launch a duplicate whole-population
experiment.

| New evidence | Investigation action |
| --- | --- |
| Same encounter still kills or produces a qualified near-death | Keep active with the new build's evidence |
| Same encounter is survived with verified recovery | Remove that build/configuration from the active failure queue; keep a bounded regression fixture |
| Full seed survives its source horizon; encounter avoided or unknown | Stop the old death investigation for this build/configuration; preserve the avoided/unknown distinction and make no direct battle-survival claim |
| Shorter continuation passes the old episode without encountering it | Record bounded non-recurrence and provisionally lower priority; no full-seed survival claim |
| Seed survives, but the old saved-position trial still fails | Record both; current run no longer exposes the old position, while its isolated tactical weakness remains reproducible |
| Old position is survived, but the seed dies later | Mark local survival; create/link the later failure as a different episode |
| Check fails, ends too early or lacks encounter evidence | Keep unknown/currently unverified; never resolve by absence of evidence |

Full-seed results and saved-position trials are separate assessment fields. Even
when a new build unexpectedly survives a seed, do not infer which change caused
it. Stop pursuing the now-inactive manifestation by default; a maintainer may
explicitly pin the old position as a tactical study. A later build that fails it
again reopens the assessment and links the regression.

Seed-survival deactivation applies to the old **death manifestation**. A study
of a near-death or an ordinary surviving battle is not dismissed merely because
its source run remains alive; assess its encounter/hazard evidence or the
maintainer's explicit study objective. A recovered but still hazardous encounter
may remain active as a near-death study after its death investigation is inactive.

Before dispatching a deep analysis, check assessment freshness against the
currently tracked immutable build and configuration. Leases pin its evidence.
If a newer build arrives while it runs, keep the result labelled for its old
target and revalidate before presenting it as a current problem. Missing new
evidence sets freshness to pending; it does not establish a fix.

## 8. Analysis and the human interface

Query by project, build/configuration, seed, encounter family, outcome or current
relevance. The job joins observations, messages, available thoughts, inventory,
spells and actions into a readable chronology. It distinguishes observed facts,
Borg beliefs, diagnostic hidden facts and analyst hypotheses. Look broadly for
behavioral or implementation explanations, without a fixed checklist of tactics.

Each retained scenario has a stable landing page: exact seed/build/settings,
start/episode/end timeline, cause or recovery, replay availability, original and
alternative results, inventory/spells, and genuine screenshot animation where
qualified capture allows it. Reports/GIFs are generated and cached on demand;
serialized machine documents are never the required human interface. Downloaded
bundles generate build/watch/play launchers and use verified per-version caches.
Human play is an explicitly labelled alternative attached to the same scenario.

Deliver a feedback packet with the reproducible situation, what the Borg knew,
supported mechanism, competing explanations, earliest useful intervention point,
proposed code/behavior/instrumentation change and focused scenario checks.
Alternative trials report survival, new death, avoidance, recovery, progress and
uncertainty. Local success does not establish a population improvement. The Borg
maintainer implements/reviews changes and asks zoo for broad validation as needed.
The analyzer does not mutate parameters, open upstream issues or publish changes
without a separately authorized action.

## 9. Reuse by other projects and users

Publish a versioned adapter and portable scenario-bundle contract, with capability
levels for metadata, chronology, reconstruction, shared-save trials and private
continuation. Start with borg-rs and borg-reborn-rs adapters, but require no
sibling checkout, owner-specific repository name, fixed filesystem path or CI
provider. Native C and Neo projects can add adapters; sharing record syntax does
not make their seeds, clocks, observations or save formats interchangeable.

Each workspace owns project namespaces, tracked builds, priorities, quotas and
sharing policy. Default evidence is private to that workspace. Explicit exports
produce portable, checksummed bundles; importing one preserves origin and gives
it a local assessment. Sharing a public fixture requires retaining its complete
declared replay dependencies. Metadata-only imports remain usable for browsing
but are not advertised as runnable.

Enforce workspace permissions on queries, jobs, artifacts and downloads. Initially
deduplicate objects only inside one workspace; no cross-user hash/availability
leak or permission inheritance. Trusted publication receives job-scoped upload
access; candidate code receives no database/deletion credentials. Offline bundle
inspection/import must not execute included launchers. Execution is an explicit
isolated worker action. Check archive paths, declared sizes and digests before
extracting untrusted bundles. A small installation can run everything locally.

## 10. Bounded storage and reliable jobs

Keep compact source/run/scenario documents in the database; compress and chunk
large observations/thoughts/input streams in external storage. Git holds tools,
schemas, source-manifest references and small selected fixture manifests. No new
routine report archive or statistical data dump is added to Git under this model.

Initial per-workspace budget proposal: three active builds, **20 GiB of artifact
storage**, and **100 promoted detailed scenarios**, separate from thousands of
indexed discovery cases. These are pilot limits to measure, configurable by the
workspace owner, not global limits imposed on other users. Count artifact
versions/backups and pinned runtimes; expiry dates alone do not bound storage.

| Evidence | Initial retention proposal |
| --- | --- |
| Raw traces and disposable checkpoints | Seven-day capture/investigation window; promote selected episodes before expiry |
| Reports, GIFs and screenshots | Regenerable cache, initially seven days; discard first under pressure |
| Active source recipes and selected scenarios | Keep dependencies needed for their advertised reconstruction/replay level |
| Inactive, unpinned detailed evidence | Thirty-day grace period, then collect; keep a compact result while metadata is retained |
| Retired run detail/assessments | Initially 180 days unless a bounded investigation/regression pin requires them |

Resolved/avoided scenarios release investigation pins after a cooldown unless
selected for the bounded regression bank. Keep diverse failures, recoveries and
ordinary controls, not only spectacular early deaths. Similar reports can share
one representative detailed fixture without erasing distinct run identities.

Pins transitively protect replay dependencies. Live jobs hold temporary leases;
expired leases require a grace period before collection. Garbage collection
plans affected owners, marks objects, waits, then serializes its final reference
check/delete transition with new pin acquisition. Verify imported bytes before
releasing source dependencies. Record unavailable/pruned status and a bounded
deletion receipt. A valid hash without recoverable bytes is not replay evidence.
Bucket lifecycle rules apply only to disposable namespaces, not shared pinned
runtime dependencies. ([S3 lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).)

When protected data fills the quota, pause new admissions and expose the required
retirement decision. Budget database detail, job receipts and backups separately;
use bounded snapshots rather than an infinite history of every assessment.
After metadata expires, the landing route explains that the case is unavailable.
Backups need a restore drill and a defined maximum recovery window before cutover.

Ingestion registers expected captures before execution. Immutable objects are
uploaded and hash-verified before transactionally attaching a complete manifest.
Compound uniqueness prevents duplicate imports; an altered payload under an
existing source ID is a conflict. Attempts and jobs have idempotency keys, leases
and fencing tokens, so late workers cannot overwrite new results. Incomplete
uploads remain explicitly incomplete and orphan objects expire after a grace
period. No failure or missing cell becomes a death or survival.

## 11. Migration and review gates

Retain the current seven cases, human recordings, published downloads and M1
review evidence as migration pins. No evidence is deleted, history rewritten,
service deployed or other repository modified by this proposal.

Reuse native exporters, seed/build receipts, candidate episode extraction,
shared-save runner, recorder/cache and readable-page generators. Add storage and
adapter boundaries rather than copying harness logic. Replace the current
same-source-only batch comparator only where a local scenario comparison needs
cross-build compatibility; leave population comparisons to zoo. Retire routine
results-branch publication after the replacement path is verified.

Proposed delivery slices, subject to architecture/milestone approval:

1. **Imports and portable identity:** ingest pinned zoo and native examples,
   including survivors, with settings/evidence gaps visible. Prove idempotence,
   namespace isolation and thousands-of-cases indexing without new Git data.
2. **Executable episodes:** retain adaptive battle sequences, calibrate the
   independent near-death qualifier, package saves/runtimes and verify replay.
   Prove safe-low-HP/fear-only negatives and real lethal-exposure positives.
3. **Current-build relevance:** implement the assessment table above and job
   freshness. Prove unexpected seed survival deprioritizes an old failure,
   avoidance is distinguished, later death creates a new case and regression
   reopens the old assessment without rewriting it.
4. **Shared investigation service:** on-demand readable pages, human/alternative
   trials and maintainer packets. A second project imports and runs a supported
   package without the original author's checkout or account.
5. **Bounded cutover:** fault-inject collection/pinning races, exercise quotas,
   reproduce a case after discarding its generated report, and restore from a
   backup. Only then stop publishing routine new run data to Git.

Review must settle the source discovery manifests, adapter instrumentation gaps,
near-death calibration method, recovery/encounter predicates, configuration
visibility, hosting and workspace quotas. The requested decision is architecture
direction and changes needed before implementation planning, not milestone
acceptance or permission to start running a new platform.
