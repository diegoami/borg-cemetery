# borg-cemetery

Where the runs of the Angband Borgs are kept: the death records, and (to come) the recordings.

The code lives elsewhere:
- [borg-rs](https://github.com/diegoami/borg-rs): the Rust Borg and its toolkit, which write these records;
- `angband-recorder`: the recorder, being extracted from borg-rs (borg-rs#62).

This repository holds only what the runs produced.

## Layout

```
deaths/        death dossiers: one directory per case, plus the registry
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
- **Slim recordings, committed here.** A recording holds only what cannot be recomputed: the input streams, the start save, the save points (compressed) and a small digest per frame. The screens and logs are rebuilt on replay. It names the build it needs and does not carry the executable (borg-rs#67, #66).
- **Release assets only if necessary.** A recording that is still too large goes into a GitHub release of this repository, with an entry under `recordings/` that points at the asset.

Why: a full recording bundle today is 100–180 MB, with the frozen executable about 14 MB and the run's checkpoint saves and frames most of the rest. GitHub refuses files over 100 MB, and a repository of such runs grows without bound. Recordings come here once borg-rs#67 has slimmed them.

## Rules

- **Records are kept as written.** Corrections and later analysis are added beside the original files, not over them.
- **No game binaries.** No raw saves, unless a dossier deliberately curates one.
- **A rerun or a backup branch is not an independent life.** It is never counted as a new death.
- **Licence:** the records are produced by Angband and the Borgs, under the Angband licence (GPL-2.0-or-later or the Angband licence; see the borg-rs `angband/docs/copying.rst`).
