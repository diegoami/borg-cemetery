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
| [D-18705b445aed8b77655de7924d4d08af4247557f64b1240efc68fe5c0514dead](D-18705b445aed8b77655de7924d4d08af4247557f64b1240efc68fe5c0514dead/report.md) | unassigned | `09a7090650bf` | 102023799 | a clear icky thing | 37759 | unassessed |
| [D-30366e42d0d92607ff975d79c385edcb1806bf32c17bd14b58ecbb818841a827](D-30366e42d0d92607ff975d79c385edcb1806bf32c17bd14b58ecbb818841a827/report.md) | unassigned | `09a7090650bf` | 102023799 | a clear icky thing | 37759 | unassessed |
| [D-41faa5e2fe53dd02eb3147b6dfadd5c698432640b961f9c245797cb77765371c](D-41faa5e2fe53dd02eb3147b6dfadd5c698432640b961f9c245797cb77765371c/report.md) | unassigned | `09a7090650bf` | 102023799 | a clear icky thing | 37759 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
