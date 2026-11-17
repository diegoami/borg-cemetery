# Rust Borg death records

Every confirmed natural death gets an immutable source/build/input identity, original observations, an assessment and linked actions. Full raw runs/saves/builds stay outside Git. Death alone does not establish a bug.

> **The canonical registry lives in
> [borg-cemetery](https://github.com/diegoami/borg-cemetery)** — recorded
> Borg runs, written death investigations and playable saved scenarios.
> Historical copies can remain local; temporary registries are isolated
> validation evidence. See [POINTER.md](POINTER.md) for the seam
> (`BORG_DEATH_RECORDS_DIR`) and storage ownership.

Dossiers: 6; distinct starting conditions: 6; retained process attempts: 6 (including repeats). This registry is not a survival-rate estimate.

| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D0000-q0c3c4cd7c15d6f21c982330000e1baf483a55bc9b1be5934e41089dc41d5346e](D0000-q0c3c4cd7c15d6f21c982330000e1baf483a55bc9b1be5934e41089dc41d5346e/report.md) | unassigned | `6d1bca10bc67` | 308 | a giant white mouse | 9285 | unassessed |
| [D0000-q3e362b965f27ffe8cd9bb5ad9d55247efaf8ace704c67203bcc15d532d5f2709](D0000-q3e362b965f27ffe8cd9bb5ad9d55247efaf8ace704c67203bcc15d532d5f2709/report.md) | unassigned | `6d1bca10bc67` | 308 | a small kobold | 3002 | unassessed |
| [D0000-q55ddeb8a244d70a07a11acb7422444d767b901c0f199a462eb13e0e3c7930fd0](D0000-q55ddeb8a244d70a07a11acb7422444d767b901c0f199a462eb13e0e3c7930fd0/report.md) | unassigned | `6d1bca10bc67` | 307 | a cave spider | 5735 | unassessed |
| [D0000-q6a4635de7a2980f41526e8efd9b1c087432f290a7da8deb7daccca2b89a9275c](D0000-q6a4635de7a2980f41526e8efd9b1c087432f290a7da8deb7daccca2b89a9275c/report.md) | unassigned | `6d1bca10bc67` | 305 | a small kobold | 3319 | unassessed |
| [D0000-q82a6b9eefb6fa4586417fd649fed2493929b8a0257d6e5b67f7c2d6e8355f1ca](D0000-q82a6b9eefb6fa4586417fd649fed2493929b8a0257d6e5b67f7c2d6e8355f1ca/report.md) | unassigned | `6d1bca10bc67` | 306 | a giant yellow centipede | 13430 | unassessed |
| [D0000-qe71d86d6d9de0845649d50735e4b7430df505f8391aa3002acb7719756d8e2d4](D0000-qe71d86d6d9de0845649d50735e4b7430df505f8391aa3002acb7719756d8e2d4/report.md) | unassigned | `6d1bca10bc67` | 306 | Fang, Farmer Maggot's Dog | 7950 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
