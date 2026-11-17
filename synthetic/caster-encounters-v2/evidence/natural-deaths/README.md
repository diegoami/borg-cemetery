# Rust Borg death records

Every confirmed natural death gets an immutable source/build/input identity, original observations, an assessment and linked actions. Full raw runs/saves/builds stay outside Git. Death alone does not establish a bug.

> **The canonical registry lives in
> [borg-cemetery](https://github.com/diegoami/borg-cemetery)** — recorded
> Borg runs, written death investigations and playable saved scenarios.
> Historical copies can remain local; temporary registries are isolated
> validation evidence. See [POINTER.md](POINTER.md) for the seam
> (`BORG_DEATH_RECORDS_DIR`) and storage ownership.

Dossiers: 8; distinct starting conditions: 8; retained process attempts: 8 (including repeats). This registry is not a survival-rate estimate.

| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D0000-q01b1247571815e48f39f858869b7dabd0275abfe9e4e47b24edf380eac073f06](D0000-q01b1247571815e48f39f858869b7dabd0275abfe9e4e47b24edf380eac073f06/report.md) | unassigned | `6d1bca10bc67` | 303 | a battle-scarred veteran | 864 | unassessed |
| [D0000-q06453971543abf9b4cd88812817b4b93eb3171a9990a14fab05332e261e60dd0](D0000-q06453971543abf9b4cd88812817b4b93eb3171a9990a14fab05332e261e60dd0/report.md) | unassigned | `6d1bca10bc67` | 302 | a metallic blue centipede | 7046 | unassessed |
| [D0000-q84f9ba49c2976e32e9bbb252ce7d8d29528404954b9741bdc3b856ef6a6d432e](D0000-q84f9ba49c2976e32e9bbb252ce7d8d29528404954b9741bdc3b856ef6a6d432e/report.md) | unassigned | `6d1bca10bc67` | 301 | a grey mold | 13547 | unassessed |
| [D0000-q8682034932fd8e59b388bf0172081fc04efab7768a4d2ee28679a3db9ac94a4b](D0000-q8682034932fd8e59b388bf0172081fc04efab7768a4d2ee28679a3db9ac94a4b/report.md) | unassigned | `6d1bca10bc67` | 304 | a small kobold | 9107 | unassessed |
| [D0000-q8de4650b6f3e1bbc2b33b59444947d1951916c6e7bb3accf106590cc52464fd9](D0000-q8de4650b6f3e1bbc2b33b59444947d1951916c6e7bb3accf106590cc52464fd9/report.md) | unassigned | `6d1bca10bc67` | 303 | a soldier | 11710 | unassessed |
| [D0000-q90e440d5591c6b7bb1c60e08c361f93c99f7aa9f00e562be18295ef9f03cdeb5](D0000-q90e440d5591c6b7bb1c60e08c361f93c99f7aa9f00e562be18295ef9f03cdeb5/report.md) | unassigned | `6d1bca10bc67` | 302 | poison | 9790 | unassessed |
| [D0000-q96c6746c80eb45c65398f918a61f1d9e721f57a1ab9b3ecad93c79737b5f6e8b](D0000-q96c6746c80eb45c65398f918a61f1d9e721f57a1ab9b3ecad93c79737b5f6e8b/report.md) | unassigned | `6d1bca10bc67` | 301 | Fang, Farmer Maggot's Dog | 13674 | unassessed |
| [D0000-qa1fdf24382a1ff446eefaeb32d903dc5e0cd292b8b601bfc73df0f8d2b1c73b8](D0000-qa1fdf24382a1ff446eefaeb32d903dc5e0cd292b8b601bfc73df0f8d2b1c73b8/report.md) | unassigned | `6d1bca10bc67` | 301 | a wild dog | 6329 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
