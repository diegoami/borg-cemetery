# borg-cemetery

Where the runs of the Angband Borgs are kept: the death records, and (to come) the recordings.

The code lives elsewhere:
- [borg-rs](https://github.com/diegoami/borg-rs): the Rust Borg and its toolkit, which write these records;
- `angband-recorder`: the recorder, being extracted from borg-rs (borg-rs#62).

This repository holds run outputs and the CI scripts that collect and analyze
them. Borg and engine implementation code stays in the source repositories.

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
[real sequence report](runs/local-validation-2026-11-14-reborn-seed102/sequence-analysis-v2/event-1/report.md).

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
python3 scripts/extract_scenarios.py /tmp/cemetery-batch
python3 -m unittest discover -s tests -v
```

Every output directory must be new. Local runs do not publish anything.

## Layout

```
deaths/        death dossiers: one directory per case, plus the registry
runs/          curated local validation reports and scenario evidence
recordings/    recordings of games (not yet: see below)
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

### `recordings/` (not yet)

**Decided (owner, 2026-11-14):**
- **Slim recordings, committed here.** A recording holds only what cannot be recomputed: the input streams, the start save, the save points (compressed) and a small digest per frame. The screens and logs are rebuilt on replay. It names the build it needs and does not carry the executable (borg-rs#67, borg-rs#66).
- **Release assets only if necessary.** A recording that is still too large goes into a GitHub release of this repository, with an entry under `recordings/` that points at the asset.

Why: a full recording bundle today is 100–180 MB, with the frozen executable about 14 MB and the run's checkpoint saves and frames most of the rest. GitHub refuses files over 100 MB, and a repository of such runs grows without bound. Recordings come here once borg-rs#67 has slimmed them.

## Rules

- **Records are kept as written.** Corrections and later analysis are added beside the original files, not over them.
- **No game binaries.** Saves are retained only when deliberately curated as
  dossier evidence or compressed scenario starting states; disposable checkpoint
  collections stay outside Git.
- **A rerun or a backup branch is not an independent life.** It is never counted as a new death.
- **Licence:** the records are produced by Angband and the Borgs, under the Angband licence (GPL-2.0-or-later or the Angband licence; see the borg-rs `angband/docs/copying.rst`).
