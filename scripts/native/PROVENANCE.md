# Native death tools moved to borg-cemetery

Original source: **diegoami/borg-reborn-rs**, commit
`83cf442a6bc6c1dec768cab2a1f22530c9caac1e` (2026-11-15).
Original file hashes are retained in `PROVENANCE.json`; its GPL-2.0 licence
is retained as `LICENSE`. Existing source comments describe earlier origins.

Moved implementation:

- `export-death.py`: natural-death filtering, source/build/config/seed identity,
  encounter-family + key-stream deduplication, atomic export and repeat repair.
- `death_registry.py`: original-format identity and temporary-registry utilities.
- `rerun-death.py`: source-checked birth rerun, original key-stream verification,
  observation/world/knowledge capture, checkpoints and preserved errand settings.
- `reconcile-deaths.py`: every natural run death must have a matching exported
  family/key stream, plus comparison with a declared baseline registry.
- The original export/rerun/reconciliation test cases are retained under `tests/`.

Local adaptations are storage/context only: canonical default output is this
repository's `deaths/`; source/harness execution accepts its actual consumer
root; canonical catalogue updates use `scripts/register_deaths.py` instead of
overwriting the historical README/index; arbitrary temporary registries retain
their original native index behaviour. No game policy, RNG or engine code moved.

`API_VERSION` declares forwarding API 1. borg-reborn-rs keeps thin compatibility
pointers at its old command paths and pins this toolkit in CI. It continues to
own game instrumentation, the measured harness and source builds. Normal exports
belong here; its historical validation dossiers stay in place and CI explicitly
uses temporary registries with its existing reconciliation guard.

From the cemetery checkout, for a dossier exported by the reborn harness:

```bash
python3 scripts/native/rerun-death.py deaths/CASE /tmp/new-rerun \
  --source-root /path/to/the/exact/borg-reborn-rs-checkout --checkpoint-every 100
```

The source/build must match the dossier. A loaded-save dossier cannot be
recreated from a birth seed alone. `--any-build` remains explicitly diagnostic,
not a successful reproduction. Machine identity files are tool inputs; the
case's README, report, analysis and replay guides are the human interface.

The concurrent reborn pointer PR #276 (`f441296ff55b2a452daeaed11e5ffbb45f0ce224`)
added a canonical-home notice to the native index template and four registry
regression tests. These are retained here too; supplemental donor hashes are
in `PROVENANCE.json`. The original source baseline above is unchanged.
