# Rust Borg death records

Every confirmed natural death gets an immutable source/build/input identity, original observations, an assessment and linked actions. Full raw runs/saves/builds stay outside Git. Death alone does not establish a bug.

> **The canonical registry lives in
> [borg-cemetery](https://github.com/diegoami/borg-cemetery)** — recorded
> Borg runs, written death investigations and playable saved scenarios.
> Historical copies can remain local; temporary registries are isolated
> validation evidence. See [POINTER.md](POINTER.md) for the seam
> (`BORG_DEATH_RECORDS_DIR`) and storage ownership.

Dossiers: 5; distinct starting conditions: 5; retained process attempts: 5 (including repeats). This registry is not a survival-rate estimate.

| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D0000-q0c72aebde67fa73b3cd237e6057827f0f14f9f17649b040550a696c8c32967af](D0000-q0c72aebde67fa73b3cd237e6057827f0f14f9f17649b040550a696c8c32967af/report.md) | unassigned | `6d1bca10bc67` | 301 | a grey mold | 13547 | unassessed |
| [D0000-q8320ce94d435bcbc80c38468b074dad329b065c908dd12f8e45786a1113fe87c](D0000-q8320ce94d435bcbc80c38468b074dad329b065c908dd12f8e45786a1113fe87c/report.md) | unassigned | `6d1bca10bc67` | 301 | a wild dog | 6329 | unassessed |
| [D0000-q8c32408c9c9a0c41003f99b336bc957bd95abae19b64ffb0c00e66eb236b5f0f](D0000-q8c32408c9c9a0c41003f99b336bc957bd95abae19b64ffb0c00e66eb236b5f0f/report.md) | unassigned | `6d1bca10bc67` | 301 | Fang, Farmer Maggot's Dog | 13674 | unassessed |
| [D0000-q9a58330a95029af2f57137fe4b1f20a320ffc1f9ee538f8229e30c7bea804370](D0000-q9a58330a95029af2f57137fe4b1f20a320ffc1f9ee538f8229e30c7bea804370/report.md) | unassigned | `6d1bca10bc67` | 302 | a metallic blue centipede | 7051 | unassessed |
| [D0000-qd018166a4c3c74fdfcc1446644362418b7a62ae627be5d6bec36d35f95201953](D0000-qd018166a4c3c74fdfcc1446644362418b7a62ae627be5d6bec36d35f95201953/report.md) | unassigned | `6d1bca10bc67` | 303 | a soldier | 11710 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
