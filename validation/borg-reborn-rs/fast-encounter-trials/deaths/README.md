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
| [D-2c2925e9a1aa59443ad641085ff8b2d025863e231449bc66c86d0478cacff0a1](D0000-q09a7c7197e5689945c122190982c8758bd60ca2d732f766451ef239435a75d06/report.md) | unassigned | `aae2c194a18b` | 202 | a clear icky thing | 7818 | unassessed |
| [D0000-q30f434291b3aab558d798c5ae6bab4d52fba4ea58b7911df9010e1f23b440dee](D0000-q30f434291b3aab558d798c5ae6bab4d52fba4ea58b7911df9010e1f23b440dee/report.md) | unassigned | `6d1bca10bc67` | 1011 | a cave spider | 18848 | unassessed |
| [D0000-q452ee3d4ed9d2f306620f4c7e8c266321b5f5fc175d779b972e767f7ab210933](D0000-q452ee3d4ed9d2f306620f4c7e8c266321b5f5fc175d779b972e767f7ab210933/report.md) | unassigned | `6d1bca10bc67` | 102 | Fang, Farmer Maggot's Dog | 3640 | unassessed |
| [D0000-q6c4a363f572a3026a0f83286ebb45fbaa142b75378f312ccb45fa1e2442680a5](D0000-q6c4a363f572a3026a0f83286ebb45fbaa142b75378f312ccb45fa1e2442680a5/report.md) | unassigned | `6d1bca10bc67` | 202 | a clear icky thing | 7818 | unassessed |
| [D-ace04888b9d00c325cdbb1a1534abba91b669168612444d35b4859ace10459cb](D0000-qa3c33e917fc745c91b1e0acfecc87941f162ece4fe6fcc7901b9d018b84d0a4f/report.md) | unassigned | `aae2c194a18b` | 1011 | a cave spider | 18848 | unassessed |
| [D-8b8d8ade37f1dbdf6d8a720479c8461b83d24fcb00be47c2efc274d1a1a81d53](D0000-qae088f7b51fff8f5c85197cad26e125ccb1cc232badcfaec62b7e6e62a5a1a32/report.md) | unassigned | `aae2c194a18b` | 102 | Fang, Farmer Maggot's Dog | 3640 | unassessed |
| [D0000-qb77bb5503bfbaa66d3ad26bf205bd5510fad3406ff580fafaca9c1cf4dcf0cdd](D0000-qb77bb5503bfbaa66d3ad26bf205bd5510fad3406ff580fafaca9c1cf4dcf0cdd/report.md) | unassigned | `6d1bca10bc67` | 1020 | a small kobold | 1207 | unassessed |
| [D-4e164be03854dc215a3c7ea986328e5e15c827eda33d96871d43d2ce810e252f](D0000-qe6aaaeb263731e575d07e683c632488c0d134e465702559197f03c5c1c3d153f/report.md) | unassigned | `aae2c194a18b` | 1020 | a small kobold | 1207 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
