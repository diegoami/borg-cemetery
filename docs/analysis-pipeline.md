# Death analysis and tuning pipeline

Human entry points are the death and scenario README pages, written reports,
inventory/spell tables, animations and REPLAY guides. Serialized observations
remain tool inputs; human pages must not print their object/array syntax or
require readers to inspect those files to understand an event or launch replay.

The process generates executable `build.sh`, `watch.sh` and `play.sh` in each
death/run and extracted scenario directory. The entry points locate shared
cemetery tools rather than embedding workstation or temporary-session paths.
They use persistent caches and immutable source/archive pins. The current
cache entry is the checkout's ignored `.cache/borg-cemetery/`; existing user
caches are reused through an alias without relocating recorded executables.
Original source builds and optional recorder runtimes have per-version hash
receipts, and interrupted recorder-tool builds preserve the completed game
phase. Cache hits do not invoke build tools. The current
qualified standalone recorder side-build covers the original seed-102 reborn
version and its optional integration; other unqualified versions are refused
rather than replayed using a different Borg. Historical frozen recordings use
their bundled player and runtime.

## Alternative human play

`play.sh` starts a copy of the retained engine save in an isolated X11 profile,
with saved RNG and a fresh process whose Borg starts off. It captures actual
terminal polling through the standalone recorder. After the window closes it
attempts full replay verification and attaches a human-readable entry under
`alternatives/human/<session>/`, indexed in the original death report. It records
the starting-save identity, runtime identity, user label/notes, last observed
outcome and verification status. Mixed human/Borg control is labelled from
recorded bot events; automated Borg replays cannot masquerade as human play.
An alive final observation is not promoted into a survival-to-horizon result.
When a recording passes the original death time, the report explicitly compares
those turns. Qualification binds the original save bytes, initial character,
replay verification, continuous observations and ordinary-play flags; restarting
or resurrecting a different life cannot supply the comparison. This establishes
one observed continuation from the saved position, not a prescribed fight or
population survival advantage. The raw capture is retained unchanged and the
comparison is written beside it. Future report attachments include this summary
automatically instead of leaving readers to infer it from timestamps.

The original death account is preserved before a bounded appended section.
Replay failures and incomplete streams remain explicit; no alternative is
attached when the recording fails to demonstrate the expected starting turn
and character. These branches are not independent lives. Small recording data
archives are retained in the case, with binaries left in the persistent cache.
Oversized archives remain locally retained with an explicit publication note.
The process does not automatically upload recordings or stage unrelated changes.

The selected seed-102 evidence is consolidated as death D0007, scenarios
S0001–S0003 and run 2026-11-14-seed102. The former local-validation tree and
duplicate generated versions have been removed after byte-preservation checks
of native records, saved games, inventory observations and terminal captures.
Historical D0005/D0006 recordings are available as release downloads, with
their frozen player/runtime and written instructions; both were verified after
relocation. The seed-102 case has screenshots and engine saves but no complete
standalone-recorder input bundle. Pages must state that distinction explicitly.

The first implementation lives in this repository: pinned seeded runs, original
evidence, adaptive episode reports, curated save-game scenarios, version trials,
parameter-profile inputs, and paired fresh-birth comparison. Automatic causal
analysis/tuning proposals and exact restoration of private Borg memory remain
subsequent work. Shared-save trials already support alternative Borg versions.

The analysis objective is to **discover changes that could reduce the chance of
death**, then test whether they help. Stair retreat, willingness to fight,
potions, objects and spells are examples supplied by the owner, not a fixed
checklist or a limit on the search. Discoveries may concern tactics, long-term
preparation, perception, memory, planning, implementation defects or something
not anticipated in this plan. Parameter tuning is one possible intervention;
the analysis must not discard a useful finding because no tuning knob exists.

## CI stages

1. **Run**: choose `borg-rs` or `borg-reborn-rs`, a source ref, explicit seeds,
   birth menu indices and a turn cap. Resolve the source once, build once, verify
   `BUILD_ID`, run each seed once. Record the requested seeds before fetching.
   Natural deaths, turn caps, early stops, timeouts and harness failures stay
   distinct. Optional reborn profiles are copied and hashed with the records.
2. **Analyze**: screen for living HP at or below 25% or estimated lethal risk
   (death chance >=10% or worst damage >=HP when available), plus natural death.
   These are candidate detectors and do not exhaust dangerous situations.
   Reconstruct each episode from the last inferred reasonably stable state
   through decline, death or sustained recovery. Join state observations,
   messages and available structured thoughts into a chronology with original
   source line numbers. Curate the nearest preceding save as an executable
   scenario. A terminal low-HP episode and its death are one episode.
   Generate a GitHub-rendered landing page (`README.md`) in every episode
   directory, linking the seed/version, report, inventory, GIF and saved scenario.
   Each run and its episode collection also get navigation pages; missing assets
   are labelled unavailable instead of becoming broken links. Historical dossiers
   receive additive landing pages without changing their original evidence.
   Retain inventory/equipment/spell observations and their changes across the
   episode, and embed a small screenshot GIF when verified capture succeeds.
3. **Archive**: append compact records and analysis to `results`, one directory
   per workflow run and attempt. Preserve original raw evidence as a 90-day
   artifact. Curated compressed scenario saves are retained with their hashes;
   disposable checkpoints and binaries stay outside Git. Analysis never edits the
   historical `deaths/D0001`–`D0006` dossiers.

These stages are implemented by `.github/workflows/run-borg.yml`. The separate
`try-scenario.yml` workflow builds the original and an alternative Borg version,
loads the same saved game in each, compares survival and archives results.
Open-ended causal investigation and automated proposal generation below remain
a delivery plan, not jobs that already exist.

## Inventory and visual review

Reborn's existing `BORG_OBSERVATION_LOG` records its observed inventory,
equipment, quiver and spell availability. The collector retains that full stream
compressed, and episode reports project player-facing descriptions, quantities,
known-state flags and spells at the start, on changes and at the last available
observation. Diagnostic hidden item-kind identifiers are not promoted into the
inventory report. borg-rs's native frame stream supplies player-visible item
descriptions instead. Missing instrumentation is explicitly reported.

The pinned reborn frontend does not provide continuous screen recording.
`capture_episode_media.py` therefore uses its existing key-limit and terminal
dump support: replay the same birth to sampled key positions, check both key
and state prefixes byte-for-byte, then retain the genuine terminal text. The
final death screen is taken directly from the original stderr stream. No engine
or Borg source is patched, and divergent replays cannot become accepted frames.

Pillow renders these terminal screenshots in monochrome, with recorded inventory
and the last available decision beside them, into a GIF. The side panels are
labelled observations and may precede the screen. Sampling/timing is for viewing,
not real-time execution. Frame text, hashes and errors accompany the GIF. The
default limits are 24 sampled screens per episode and 300 seconds of replay work
per batch; missing or partial capture is visible in the report. Replays remain
diagnostics belonging to the original life, never new deaths for statistics.

## Discover opportunities before selecting interventions

Review the game trajectory and available decision evidence without assuming
which behavior caused the death. Reconstruct what happened, what the Borg knew,
which decisions changed its exposure to risk, and where a feasible alternative
could have changed the outcome. Compare deaths with near-death recoveries and
successful runs to distinguish recurring weaknesses from unlucky outcomes or
behavior that is usually beneficial. A death does not by itself imply a mistake.

The initial health/threat detectors are only ways to select episodes. Discovery must
also seek dangerous situations outside that detector, including apparent
recoveries that leave the character exposed later. Add new detectors when the
evidence supports them rather than treating the initial heuristic as the
definition of near death.

Infer the episode boundary from the observed trajectory, not a fixed number
of preceding turns. Extend backwards when the decisive choice occurred earlier: preparation, resource depletion, route selection or an
incorrect belief may precede the terminal encounter by much more than 30 turns.
An analysis should identify the earliest supported opportunity to alter the
outcome, not merely the last action before death.

Produce a ranked set of concrete, falsifiable improvement hypotheses. Each must
link an observed pattern to a plausible mechanism, a feasible intervention and
a discriminating experiment. Rank by expected survival benefit, recurrence
across independent births, strength of evidence, regression risk and cost to
test. Include alternative explanations and uncertainty. Record unsupported or
inconclusive leads rather than forcing every episode into a proposal.

Analysis can discover and report hypotheses before exact rewind exists. A documented shared-start
contract gates scenario comparisons; verified original continuation gates
stronger causal claims about the uninterrupted run, not investigation itself.

## Shared-save scenario trials and optional exact continuation

A scenario is an actual compressed engine save plus a manifest identifying its
hash, original seed, birth, source/binary version, checkpoint turn and input
position. Both the baseline and alternative Borg load a copy of the same save,
preserve its engine RNG and start with fresh Borg memory. This is an intentional
shared starting condition for measuring which version survives. Restoring
private Borg memory is not a prerequisite for these restarted-Borg trials.

Collection currently takes periodic saves (default every 100 engine turns,
configurable). The analysis chooses the newest valid save at or before the
inferred stable boundary, never a later save that already skips the decline.
It reports the actual checkpoint lead time. Saves occur at native command
boundaries; cadence is not a guarantee of an exact requested turn. If there is
no eligible save, mark the scenario `missing_checkpoint`; retain the report and
request denser capture or a supported reconstruction, rather than fabricating a
start state. Only selected saves are compressed and retained permanently.

The first boundary heuristic requires HP >=70% for three distinct observed
engine turns, with zero estimated death chance, worst damage below current HP
and disabling chance <=5% where the trace provides these estimates. Missing
threat information stays explicitly unknown. This approximates "okay-ish";
it is not proof of safety. Calibrate or replace it using complete encounter,
resource and perception evidence. Reports must permit moving the boundary
earlier if a prior strategic decision explains the deterioration.

Keep the chronological sequence from the saved starting point through the
original endpoint, with the inferred stable boundary marked separately. A
near-death episode also includes recovery or an explicit unresolved ending.
Preserve the original state stream, messages and structured decision evidence;
report observations separately from causal interpretations. Preserve overlapping
episodes' relationship to the same independent birth.

`run_scenario.py` verifies compressed and raw save hashes, target source/build
identity, successful loading at the expected turn and birth, and the common
startup contract. A silent fresh birth or incompatible load is a failure, not
survival. Versions may carry different engine changes as well as Borg changes;
such trials compare those complete versions and do not isolate Borg logic by
themselves. Record both build identities. Each trial uses a fixed engine-turn
horizon relative to the saved turn; timeouts, stops and load failures remain
inconclusive rather than becoming deaths or rescues.

A restarted original may differ from the uninterrupted original because its
Borg memory was reset. Record that observation; it does not invalidate the
shared-save benchmark if both arms use the same documented startup contract.
A claim about replacing one decision in the uninterrupted original is stronger:
that requires verified prefix/control continuation with the relevant private
state preserved or reconstructed. Keep that exact-continuation qualification
separate from the implemented shared-save trials.

Local trials use an already-built, pinned source checkout:

```bash
flock -n /tmp/angband-validation.lock python3 scripts/run_scenario.py run \
  --source /path/to/original-borg --scenario /path/to/event-1 \
  --turns 1000 --out /tmp/scenario-baseline
flock -n /tmp/angband-validation.lock python3 scripts/run_scenario.py run \
  --source /path/to/alternative-borg --scenario /path/to/event-1 \
  --turns 1000 --out /tmp/scenario-candidate
python3 scripts/run_scenario.py compare /tmp/scenario-baseline/trial.json \
  /tmp/scenario-candidate/trial.json --out /tmp/scenario-comparison.json
```

Selected scenario directories contain `scenario.json`, `start.save.gz`,
`sequence.json` and `report.md`. Optional original custom profiles are retained
beside them and used when running the original source version. A trial may pass
`--profile` for an alternative reborn profile; its effective hash is checked.

## Evidence-backed investigation and proposal job

For each selected episode, reconstruct the information available to the Borg at
each relevant decision. Engine truth can diagnose a failure, but cannot justify
a policy that would require hidden knowledge. Follow the evidence wherever it
leads. The owner's examples can prompt questions, without becoming mandatory
report categories or exhaustive candidate interventions:

- **Stair retreat**: known stairs, reachability, estimated arrival time,
  movement costs, intervening threats and the first turn retreat was feasible.
- **Fight or disengage**: the selected action and alternatives, their scores,
  threat estimate, mode, goal age, escape route and pursuit/recovery behavior.
- **Potions and objects**: known inventory, legal use, expected effect, reserve
  policy, availability at the decision and the risk of spending that turn.
- **Spells**: knowledge, mana, failure chance, legal targets and alternatives.

The report must separate observed facts, missing instrumentation and causal
hypotheses. Borg trace fields are evidence, not an account of unlogged thoughts.
Each proposal must describe the suspected mechanism, evidence line references,
a concrete intervention, a predicted survival effect, alternative explanations,
a regression risk and the experiment that could support or reject it.

For a parameter proposal, name an existing parameter supported by that pinned
version, its original value and a bounded candidate range. For a behavior or
implementation change, specify the required upstream change and its acceptance
criteria. For an unresolved hypothesis, specify the missing observation and an
instrumentation experiment. These are valid outputs even when the current
profile runner cannot execute them. Do not invent configuration keys or reduce
the search to the parameters already exposed. No automatic upstream issue/comment
or default-policy change.

Suggested proposal contract:

```json
{
  "scenario_ids": ["run/seed/event"],
  "source_commit": "full SHA",
  "baseline_profile_sha256": "SHA-256",
  "hypothesis": "observed weakness and proposed causal mechanism",
  "intervention": {
    "kind": "parameter | behavior_change | defect_fix | instrumentation",
    "description": "concrete change or discriminating observation"
  },
  "evidence": [{"file": "trace.jsonl", "line": 123}],
  "prediction": "specific observable change",
  "alternative_explanations": ["another explanation to distinguish"],
  "regression_risk": "specific adverse outcome",
  "experiment": "control, candidate, endpoint and rejection criterion",
  "startup_contract": "fresh_borg_saved_engine_rng",
  "original_continuation_required": false
}
```

## Trial and validation jobs

Run the original version and each candidate from each saved scenario,
using the same engine state, saved RNG and fresh-Borg startup contract. Keep the
triggering death, related episodes,
near-death recoveries, and control encounters where the original policy worked.
Do not tune and evaluate on the same selected deaths alone.

Choose the experiment's scope to match the hypothesis. A local tactical change
may fit a short replay; a preparation or strategic change needs a longer replay
or a fresh-birth cohort. Behavior changes and defect fixes require separately
pinned upstream builds. Do not reject such proposals merely because a local
parameter trial cannot represent them.

Report paired rescued/newly killed outcomes, survival to a fixed horizon,
minimum HP, damage, escape success/time, resource spending, depth progress,
stalls and infrastructure failures. A longer life is not necessarily a rescue;
reaching a cap is censored survival. Compare within scenario families and then
validate candidates from birth on a frozen held-out seed suite. Never pool
overlapping windows as independent trials or optimize only the easiest replay.

The existing `scripts/compare_batches.py` is a narrower tool: it compares two
fresh-birth batches with the same program, source, build inputs/toolchain,
birth, seeds and cap. It reports rescues, new deaths and inconclusive pairs,
and discloses whether binaries match. It requires a reported fixed calendar;
older versions without that evidence are inconclusive. It does not claim local
scenario causality or automatically accept a tuning change.

Acceptance for automated tuning: documented shared starts, supported parameter
validation, reproducible paired variants, held-out validation and a report that
includes regressions and unresolved failures. Promotion to a default remains a
separate reviewed upstream delivery.
