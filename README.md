# borg-cemetery

Recorded Angband Borg runs, written death investigations and playable saved scenarios.

Borg and engine code stays in [borg-rs](https://github.com/diegoami/borg-rs)
and [borg-reborn-rs](https://github.com/diegoami/borg-reborn-rs). This repository
owns the [shared native death tools](docs/native-death-tools.md), run outputs,
reports and CI collection/analysis scripts. Borg-reborn-rs keeps compatibility
pointers to the shared tools. `angband-recorder` is being extracted from borg-rs
(borg-rs#62).

M1 is [awaiting owner-run milestone review](https://github.com/diegoami/borg-cemetery/pull/1).
The [pinned review packet](docs/reviews/M1/README.md) lists scope, evidence and
limitations. It is not yet an accepted milestone.

## Proposed redesign

The [controlled-experiment redesign](docs/cemetery-redesign.md) proposes a fixed
seed suite, a small set of exact build/configuration variants, database-backed
run tracking and bounded external artifact storage. It defines independent
near-death qualification, on-demand reconstruction and analysis, and a feedback
loop through saved scenarios and cohort validation. This is a design proposal;
the collection and Git archive behavior described below is still the current
implementation.

## Statistics by build

[Statistics](statistics/README.md) separates the seven curated cemetery dossiers
from a pinned inventory of the historical borg-reborn-rs archive. Browse exact
builds, causes, character types, death turns and depths, seeds and source reports.
Repeated attempts and scenario/human branches do not inflate the death counts;
these selected death archives do not provide a mortality-rate denominator.
New native death registration refreshes the local statistics automatically.

## Browse deaths

- [Historical death registry](deaths/README.md): every case has its own landing page.
- [Fang, seed 102](scenarios/S0003/README.md):
  report, inventory, animation and saved scenario together.

Each death directory opens a `README.md` landing page on GitHub. CI generates
these for new deaths and their episodes, including explicit unavailable states
for evidence that was not retained. Original reports and records stay intact.

## Read and replay

Every death and scenario directory has executable launchers, generated as part
of collection and analysis:

```bash
cd deaths/D0007
./build.sh
./watch.sh
./play.sh --label "My attempt" --note "What I tried differently"
```

`build.sh` uses pinned source or a checksum-verified frozen runtime. `watch.sh`
verifies and plays the retained recording or qualified saved-position replay.
`play.sh` opens an available saved position in X11/WSLg, with the Borg initially
off. Ctrl-X saves and exits; follow the Return/Escape prompts until the window
closes. It then retains your recording and adds **Alternative human play** to
the death report, with your notes, the last observed outcome, replay verification
and a command to watch it. Activating the Borg is labelled mixed human/Borg play;
neither kind of branch counts as a new independent life.

Runtime builds and working recordings share this checkout's ignored
`.cache/borg-cemetery/` entry, keyed by program/version rather than death. If
the older user cache already exists, that entry links to it so existing builds
and recording paths are reused immediately. `--cache` or `BORG_CEMETERY_CACHE`
can select another location. A successful version is hash-checked and reused;
`build.sh` prints **Using cached …** without invoking CMake, Cargo or the native
build script again. Interrupted recorder-tool builds reuse the completed game
phase. Original seed-only builds also get reusable version receipts. Compact human
recording archives and written entries are retained under the death's
`alternatives/human/` directory. Executables stay out of Git. The launcher does
not automatically stage or publish your working tree; commit/push the resulting
recording and report when ready. Reverification needs the exact recorded runtime;
recorded-frame viewing remains available when a matching rebuild is unavailable.

For non-interactive checks, use `./watch.sh --verify-only` or
`./watch.sh --dump-turn 3432`. A historical case without a retained recording or
save explains that limitation. Saved-position Borg playback requires a qualified
recorder-enabled version; a different Borg is never silently substituted.

If using data from a `results`-branch checkout, set `BORG_CEMETERY_HOME` to a
full `main` checkout so the case-local launchers can find the shared tools.

- [Deaths](deaths/README.md): written accounts, character details, inventory and playback instructions.
- [Complete death catalogue](deaths/CATALOG.md) includes new native exports without rewriting the imported historical registry.
- [Saved scenarios](scenarios/README.md): written situation reports and commands for trying alternative Borgs.
- [Original recordings of D0005 and D0006](https://github.com/diegoami/borg-cemetery/releases/tag/recordings-2026-11-15): downloadable bundles with the matching executable and recorder/player.
- [Run records](runs/): batch provenance and outcomes.

[The recorded human alternative to D0007](deaths/D0007/alternatives/human/20261115T004527-7541a0/README.md)
stayed alive to turn 4873 with 15/15 HP, beyond the original death at 3640.
It demonstrates survival from the retained starting position; Fang was never
recorded as visible in that continuation. The original capture metadata and
recording are preserved alongside the readable comparison.

The human pages use prose, tables, pictures and executable commands. Machine-readable files are retained for tools; they are not required reading.

[Survival analysis across the retained deaths](docs/death-analysis.md) ranks
evidence-backed improvement hypotheses and gives per-case experiments. It is
an analyst pass; proposed profile files are not accepted tuning changes.

The [native export/rerun/reconciliation tools](scripts/native/PROVENANCE.md)
are owned here, brought over from borg-reborn-rs with their provenance and tests.
That repository retains its harness and game instrumentation plus thin pointers
to these commands. Set `BORG_CEMETERY_DIR` to this checkout when it is not beside
the consumer checkout. Explicit `BORG_DEATH_RECORDS_DIR` overrides still support
isolated validation registries. Historical reborn validation cases are not bulk
imported as new independent deaths.

## Pinned seeded runs in CI

Choose **Actions → Run pinned Borg → Run workflow**. Select `borg-rs` or
`borg-reborn-rs`, enter a commit SHA (recommended), tag or branch, and supply
1–20 explicit seeds, separated by commas. Choose race/class birth-menu indices
(default Human Warrior), the game-turn cap and a wall limit of up to 120 seconds
per seed. No runs are scheduled automatically.

The workflow builds the selected source once and records its full commit,
build-input and executable hashes, compiler versions, seed, birth settings,
summary, process receipt and evidence hashes. It writes the seeds **before**
fetch/build and checks the game's reported seed and birth against the request.
Death reports come from the original run. A timeout is never recorded as death.

Compact records and scenario screening are appended to the **`results` branch**
under `runs/<workflow-run-id>-<attempt>/`. This survives CI artifact expiry.
Original logs and upstream-generated death dossiers are downloadable in the
workflow's `evidence-…` artifact for 90 days. Periodic checkpoints are captured
(default every 100 engine turns); only saves selected as scenarios are compressed
and permanently archived with the reports. Other save/panic/archive directories
are excluded from artifacts. The workflow needs permission to write the `results` branch; source
execution has read-only repository permissions, and a separate archive job gets
the write credential. Check the archive job succeeds before relying on durable
storage. Cancellation or runner loss can prevent final artifact upload.

The analysis job reconstructs the sequence from the last inferred reasonably
stable state through deterioration, death or recovery. Reports join messages,
health/resource changes and available Borg decisions, with source line references.
The initial "okay-ish" boundary uses sustained HP and available threat estimates;
it is a calibratable heuristic, not a fixed turn window or proof of safety.

Each episode retains a compressed save from at or before that boundary, plus
its seed, source version, save hashes and starting turn. If no suitable checkpoint
exists, the report explicitly marks the scenario as unavailable. See a
[real sequence report](scenarios/S0003/report.md).

Choose **Actions → Compare Borgs on a saved scenario → Run workflow** to test an
alternative version. Enter the cemetery branch/commit containing the scenario,
its directory path, and the candidate project/ref. The workflow builds both the
original and candidate versions and loads the **same saved game and engine RNG**
into each, with fresh Borg memory. It reports survival to a shared turn horizon,
new deaths and inconclusive failures, and archives the comparison to `results`.
An incompatible load or a silent new birth cannot count as survival. This is a
saved-position benchmark; restoring the original Borg's private memory is a
separate, stronger requirement for exact uninterrupted continuation.

The design for episode reconstruction, open-ended discovery of survival
improvements and experiments is in [the analysis pipeline](docs/analysis-pipeline.md).

Each episode also links an **inventory/equipment/spell report** and a small
**animated GIF of actual terminal screens**, where supported. The GIF includes
the last observed carried items and Borg decision beside the monochrome screen.
Screens are sampled by verified replays of the pinned executable from birth;
each replay's input and state prefix must match the original. Diagnostic replays
are not additional independent lives. Missing screenshots or inventory stay
explicitly unavailable, and a time budget can produce a partial preview.

See the [Fang landing page with inventory and animation](scenarios/S0003/README.md)
or open its [GIF](scenarios/S0003/media/episode.gif).

For a reborn parameter experiment, commit a candidate profile to this checkout
and supply its path in the optional `profile` input. Unknown or invalid keys
must be rejected by the pinned Borg. The profile is copied into the run records.
Run the same seeds/ref/birth/cap with the default and candidate profiles, then
compare downloaded record directories:

```bash
python3 scripts/compare_batches.py baseline/records candidate/records --out comparison.json
```

Local collection uses the same runner (Python standard library, Git, Rust,
CMake, Make, C compiler and any native dependencies of the selected version):

```bash
flock -n /tmp/angband-validation.lock python3 scripts/run_batch.py \
  --program borg-reborn-rs --ref FULL_COMMIT_SHA --seeds 101,102 \
  --turns 100000 --out /tmp/cemetery-batch
python3 -m pip install -r requirements-media.txt
flock -n /tmp/angband-validation.lock python3 scripts/capture_episode_media.py /tmp/cemetery-batch
python3 scripts/extract_scenarios.py /tmp/cemetery-batch
python3 -m unittest discover -s tests -v
```

Every output directory must be new. Local runs do not publish anything.
For new batches, capture media before extracting the final reports so the GIFs
are included. The CI workflow does this automatically. Media generation uses
Pillow; original run collection and save-scenario trials otherwise use the
Python standard library and the selected project's native tools.

## Layout

```
deaths/        death dossiers: one directory per case, plus the registry
runs/          batch provenance and outcomes
scenarios/     written situation reports, starting saves and trial results
recordings/    recording download index and playback guide
```

### `deaths/`

The death records. One directory per case (`D0001-…`), with:
- the record (`record.json`) and its build/input identity;
- the curated native evidence;
- the assessment and actions;
- for the recorded cases, the snapshots near the death.

The registry files sit next to the cases: `README.md`, `index.json`, `owner-reviews.json`, `discussion.json`, `cohort-2026-11-07.md`, `window-profile-v2.json`.

- **Where they come from.** D0001–D0006 were moved here on 2026-11-14 from borg-rs `docs/deaths/`. They are byte-identical to borg-rs commit [`4ed3263`](https://github.com/diegoami/borg-rs/tree/4ed3263ba340ce907484465f2d3addbdf5eab8ed/docs/deaths), the last commit that holds them there (borg-rs#62).
- **Relative paths in the reports.** Some reports refer to `../../validation/…`. That is borg-rs's [`docs/validation/`](https://github.com/diegoami/borg-rs/tree/4ed3263ba340ce907484465f2d3addbdf5eab8ed/docs/validation), which stays in borg-rs. The dossiers are kept as they were written, not rewritten.
- **The process** (how a case is collected, reviewed and discussed) is borg-rs's [`docs/death-workflow/`](https://github.com/diegoami/borg-rs/tree/feature/recordings-with-branches/docs/death-workflow). Owner feedback goes to borg-rs#3.
- **Writing new cases here.** borg-rs's launchers export each natural death into a registry directory. Point them at this checkout:

  ```bash
  export BORG_DEATH_RECORDS_DIR=/path/to/borg-cemetery/deaths
  ./scripts/start-borg.sh NAME          # or scripts/run-borg-headless.py, scripts/produce_death.py
  ```

  Then review what was written and commit it here. The registry lock (`deaths/.registry.lock`) is ignored.

### `recordings/`

[The recording guide](recordings/README.md) lists the complete original D0005
and D0006 recordings. Each download includes the matching frozen Linux
executable, game data and recorder/player, with a written guide inside. They
were copied to a new location and fully replay-verified before packaging.
The archives are release assets so frozen game binaries do not enter Git.

Other cases may retain screenshot animations and playable engine saves without
having a complete recorder input recording. Each case says exactly which is
available. A GIF is a visual account; an engine save starts a new Borg; a full
recorder replay verifies the original recorded run. These capabilities are not
interchangeable. Future slim recorder integrations should retain the minimal
supported replay inputs and identify the exact runtime they require.

## Rules

- **Records are kept as written.** Corrections and later analysis are added beside the original files, not over them.
- **No game binaries.** Saves are retained only when deliberately curated as
  dossier evidence or compressed scenario starting states; disposable checkpoint
  collections stay outside Git.
- **A rerun or a backup branch is not an independent life.** It is never counted as a new death.
- **Licence:** the records are produced by Angband and the Borgs, under the Angband licence (GPL-2.0-or-later or the Angband licence; see the borg-rs `angband/docs/copying.rst`).

## Recorded incident: PlanMage

[Wild-cat incident and playable positions](deaths/recorded-planmage-20261115-wild-cat/README.md)
retain the canonical report, actual saved states and behavioral trials.
Original recordings stay in player-cemetery; source repos link to this case.
