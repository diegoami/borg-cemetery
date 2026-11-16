# One owner for native death tooling

The owner requested moving the reusable death tools into borg-cemetery and
leaving pointers in borg-reborn-rs. This repository now owns the implementation
under [scripts/native](../scripts/native/PROVENANCE.md), copied with provenance
from reborn commit `83cf442a6bc6c1dec768cab2a1f22530c9caac1e`.

## What is reused

| Reborn facility | Reuse here |
| --- | --- |
| `export-death.py` | Natural-death filtering, immutable source/build/config/seed identity, encounter-family/key deduplication, atomic export and repair of missing files |
| `rerun-death.py` | Exact source-hash check, original key-stream verification, observation/world/knowledge logs, checkpoints and preserved core/errand/ladders settings |
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

## Synthetic starts (reborn #371)

Generated-depth scenarios are synthetic evidence, not natural deaths. The native
exporter rejects a synthetic marker or start depth in summary/config, a
`start-depth=N` flag, or the forced-descent/no-recall option pair. Rejection
happens before creating or locking the natural registry, even when called
directly. Natural-death reconciliation uses the same predicate. No synthetic
registry or scenario collection is introduced by this change.
