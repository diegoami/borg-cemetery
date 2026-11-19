# One owner for native death tooling

The owner requested moving the reusable death tools into borg-cemetery and
leaving pointers in borg-reborn-rs. This repository now owns the implementation
under [scripts/native](../scripts/native/PROVENANCE.md), copied with provenance
from reborn commit `83cf442a6bc6c1dec768cab2a1f22530c9caac1e`.

## What is reused

| Reborn facility | Reuse here |
| --- | --- |
| `export-death.py` | Natural-death filtering, immutable source/build/config/seed identity, encounter-family/key deduplication, atomic export and repair of missing files |
| `rerun-death.py` | Exact source-hash check, original key-stream verification, observation/world/knowledge logs, checkpoints and preserved core/errand/ladders/errands-plan settings |
| `reconcile-deaths.py` | No unexported natural run death; comparison with the declared historical reference registry |
| `death_registry.py` | Original-format identity handling and isolated-registry utilities; canonical cemetery presentation is delegated to our own registration step |
| Original tool tests | 35 focused export/rerun/reconciliation/registry checks retained with the moved code |

Reborn still owns the game, Borg, build, measured-run launcher and observations.
Its four existing tool paths become API-checked thin forwarders. CI checks out
an immutable cemetery toolkit revision; local forwarding finds the sibling of
the primary checkout, including linked worktrees, or `BORG_CEMETERY_DIR`.
No engine or policy code is moved or repinned.

Normal measured deaths default to this checkout's `deaths/`. Explicit
`BORG_DEATH_RECORDS_DIR` remains authoritative for temporary validation registries.
Reborn's historical `docs/deaths/` stays preserved as CI/reference evidence;
it is not bulk imported as thousands of new independent lives. Its existing CI
temporary-registry and historical reconciliation assertions are not weakened.

## Why a storage path alone was insufficient

The old registry aggregator rewrites a registry's README and index. Merely
setting its directory to this repository would overwrite our curated historical
index. Canonical exports now invoke [the cemetery registrar](../scripts/register_deaths.py),
which locks the registry, builds human pages and updates
[the unified catalogue](../deaths/CATALOG.md). Original records, reports,
historical index and historical actions stay intact. Temporary custom registries
can still use the original native index format.

## Existing plans that should inform later work

- [Reborn #153](https://github.com/diegoami/borg-reborn-rs/issues/153) specifies a
  blind diagnosis/calibration pilot, candidate fixtures and missing evidence.
  It is a useful evaluation design, not proof that an automated analysis job
  already exists. This repository's current seven-case pass read the prior
  assessments, so it is explicitly **not** a blind calibration hit-rate study.
- [Reborn #212](https://github.com/diegoami/borg-reborn-rs/issues/212) proposes
  timed and tactical errands, outcome criteria and a counterfactual runner.
  Its command layers and engine hooks are plans with preconditions/owner gates,
  not an existing callable facility to copy. If implemented, it could test
  full-prefix interventions without resetting Borg memory, complementing our
  currently qualified saved-engine restarts.

The [survival analysis](death-analysis.md) uses these distinctions. Concrete
proposals name whether they need an existing profile setting, a qualified
native fixture, missing instrumentation or a future intervention facility.
Neither moving tools nor writing an analysis applies a gameplay fix.

## Synthetic execution boundary

Synthetic generated-depth runs are experimental results, not natural deaths.
The exporter and reconciliation share the same conservative guard. In summary
or config, absent/empty/zero `start_depth` is ordinary (JSON numeric zero, including 0.0, or false, or the
literal string `0`); other string spellings, including `00` and `0.0`, are excluded.
The accepted ordinary `synthetic` values are absent, JSON false/numeric zero, empty string,
`0` and lowercase `false`. Values such as `False` or `no` fail closed.
One conflicting synthetic marker suffices to exclude a run.

Supplied and recorded comma-separated flags are stripped and lowercased.
`start-depth` / `start_depth` and `synthetic` tokens are excluded when bare or
followed by `=` or whitespace. The real suite emits `menu,start-depth=N`.

The pair `game_options.birth_force_descend: true` and `birth_no_recall: true`
also excludes unmarked one-way save lineage. This native receipt intentionally
requires JSON booleans, without coercing strings/numbers; `loaded: true` alone
is not evidence of synthetic lineage. An absent/null option object is permitted;
a non-object is malformed and excluded rather than crashing the scan.
Reconciliation prints `SKIPPED: <run>: <reason>` for each exclusion, so strict
marker parsing cannot silently hide a run.

This is the natural-registry boundary for cemetery #5 / borg-reborn-rs #371.
The P1 suite/report layer is documented in [synthetic-suite.md](synthetic-suite.md).
No existing dossier is rewritten or promoted from a synthetic result.

## Zoo deaths (borg-zoo#176, #63)

borg-zoo replays every natural death of a run once, with full logs. It checks
the replay's key stream against the cell's and uploads death bundles as the
run's `deaths-<specimen>-<shard>` artifacts, kept 90 days. A bundle is a run
directory for `export-death.py`. Import a whole run with:

```bash
python3 scripts/import_zoo_deaths.py --run RUN_ID        # downloads with gh
python3 scripts/import_zoo_deaths.py --bundles DIR --run-id ID
```

Each reproduced bundle becomes a `D-<sha256>` dossier, registered with its
README, REPLAY and launchers. The run page `runs/zoo-<experiment>-<run>/`
(README.md, deaths.json) lists every death with its dossier, or with the reason
it has none: not reproduced, failed replay, unsupported harness kind, or a
bundle that no index line names (the zoo shard stopped before indexing it).
Listed bundles are never imported, because the index line carries their
reproduction status and build identity. A death
already in the registry is a repeat. Raw logs stay in the zoo artifact, which
the dossier's `raw_directory` names. Exact reruns of zoo dossiers use the zoo
path of `rerun-death.py` (#59).

### Animate a zoo death's last turns

`scripts/animate_death.py CASE [--turns N] [--every K]` reruns a zoo dossier the
way the zoo ran it, through the zoo path of `rerun-death.py` with its `extra`
borgh options. It refuses to draw unless the rerun reproduces the recorded key
stream. It then replays to the last key of each of the last N turns (default
50, every turn; `--every K` thins them), using `-keys K -screen`. A turn is a
game turn at which the Borg pressed keys. A frame whose keys are not exactly
the original prefix is dropped and listed in the receipt. The GIF and its
receipt go to `CASE/media/last-N-turns.{gif,json}`, and the death page embeds
them. Only zoo
dossiers are supported. Batch episodes use `capture_episode_media.py`.
