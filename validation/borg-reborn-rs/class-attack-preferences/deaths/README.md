# Rust Borg death records

Every confirmed natural death gets an immutable source/build/input identity, original observations, an assessment and linked actions. Full raw runs/saves/builds stay outside Git. Death alone does not establish a bug.

> **The canonical registry lives in
> [borg-cemetery](https://github.com/diegoami/borg-cemetery)** — recorded
> Borg runs, written death investigations and playable saved scenarios.
> Historical copies can remain local; temporary registries are isolated
> validation evidence. See [POINTER.md](POINTER.md) for the seam
> (`BORG_DEATH_RECORDS_DIR`) and storage ownership.

Dossiers: 3; distinct starting conditions: 3; retained process attempts: 3 (including repeats). This registry is not a survival-rate estimate.

| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D-65ee280697b91dbffd08ccda2682162ea83db1696e45b5b91a9eb103b0564cfd](D0000-q92110d8eef797bda54eaf2d144a0b0e92acb47d6643640b861d33a3dd9ec4642/report.md) | unassigned | `cce8ccfc320b` | 1011 | a fruit bat | 1979 | unassessed |
| [D-d2c6d23ee5e69492f60ec4e1db958c11fa00ab49908e3b9c8f8917a7ccc54fb7](D0000-q9fc496b138d5689747fea26ba83bf0ad5d15bb8210dd5b52df6da1f555d35f92/report.md) | unassigned | `9289dbc5b4aa` | 1011 | a fruit bat | 1979 | unassessed |
| [D-d743569d2e76562974192016e13255eaa81b249d2cf8184e0b8d3c71c03276c4](D0000-qe3a44ec24bce77f730ebfc2b86b589f16550e3ad4b5a0d739cc84ff23f926a32/report.md) | unassigned | `0c5ad8f77cfa` | 1011 | a fruit bat | 1979 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
