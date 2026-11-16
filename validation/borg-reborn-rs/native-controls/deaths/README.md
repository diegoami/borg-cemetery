# Rust Borg death records

Every confirmed natural death gets an immutable source/build/input identity, original observations, an assessment and linked actions. Full raw runs/saves/builds stay outside Git. Death alone does not establish a bug.

> **The canonical registry lives in
> [borg-cemetery](https://github.com/diegoami/borg-cemetery)** — recorded
> Borg runs, written death investigations and playable saved scenarios.
> Historical copies can remain local; temporary registries are isolated
> validation evidence. See [POINTER.md](POINTER.md) for the seam
> (`BORG_DEATH_RECORDS_DIR`) and storage ownership.

Dossiers: 10; distinct starting conditions: 10; retained process attempts: 10 (including repeats). This registry is not a survival-rate estimate.

| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D0000-q046b7b25ec35ac47a362315717cd69ac9445a246d478686e59bf986c1da0708d](D0000-q046b7b25ec35ac47a362315717cd69ac9445a246d478686e59bf986c1da0708d/report.md) | unassigned | `4fa86ac995e9` | 1020 | a giant white mouse | 8922 | unassessed |
| [D0000-q0975578bc6c4c631289a8e40935a67163489d1d1331d4724807cf5a32564e7eb](D0000-q0975578bc6c4c631289a8e40935a67163489d1d1331d4724807cf5a32564e7eb/report.md) | unassigned | `5e8454ab390a` | 1011 | a wild dog | 17759 | unassessed |
| [D0000-q1c05af555bc06bf7d7f1e2815e076be974b33bf3ea577de06763ebe2f170aac0](D0000-q1c05af555bc06bf7d7f1e2815e076be974b33bf3ea577de06763ebe2f170aac0/report.md) | unassigned | `4fa86ac995e9` | 1011 | a wild dog | 17759 | unassessed |
| [D0000-q1cca14eef3826d180caab1ff8a268e6a0f1eaef076b61a60018645c20bd4bb26](D0000-q1cca14eef3826d180caab1ff8a268e6a0f1eaef076b61a60018645c20bd4bb26/report.md) | unassigned | `ce3b66f0c3df` | 1020 | a giant white mouse | 8922 | unassessed |
| [D0000-q328eb350c63dfaeab1c4e723720dbcd00122ae49b4ce308fcf5fc9d63782ddd4](D0000-q328eb350c63dfaeab1c4e723720dbcd00122ae49b4ce308fcf5fc9d63782ddd4/report.md) | unassigned | `5e8454ab390a` | 102 | Fang, Farmer Maggot's Dog | 3640 | unassessed |
| [D0000-q52ab4fa20cb07a99aafabb1d45c83f01708e75aaa24b5040909931dba8a156b2](D0000-q52ab4fa20cb07a99aafabb1d45c83f01708e75aaa24b5040909931dba8a156b2/report.md) | unassigned | `ce3b66f0c3df` | 1011 | a cave spider | 18903 | unassessed |
| [D0000-q5fd304921926e8969a3701c865f5a347e7c4200f67f15a7f29c2c04570f77605](D0000-q5fd304921926e8969a3701c865f5a347e7c4200f67f15a7f29c2c04570f77605/report.md) | unassigned | `4fa86ac995e9` | 102 | Fang, Farmer Maggot's Dog | 3640 | unassessed |
| [D0000-q79fc03ae1d57b904212e354f87c49b7e557218b9a73340ea5816562a95dfa9f8](D0000-q79fc03ae1d57b904212e354f87c49b7e557218b9a73340ea5816562a95dfa9f8/report.md) | unassigned | `5e8454ab390a` | 1020 | a giant white mouse | 8922 | unassessed |
| [D0000-q89ae21ffe1c893b758f5257e7e28557ed9e1fde7db3d72dd04beb1e00d37a0d1](D0000-q89ae21ffe1c893b758f5257e7e28557ed9e1fde7db3d72dd04beb1e00d37a0d1/report.md) | unassigned | `499965f3b5fb` | 1011 | a cave spider | 18903 | unassessed |
| [D0000-qd70258a8f0faa3bed5747c7fb492ff61fb1f7b9b20fb2e85c3aad1e0afd8bbb3](D0000-qd70258a8f0faa3bed5747c7fb492ff61fb1f7b9b20fb2e85c3aad1e0afd8bbb3/report.md) | unassigned | `499965f3b5fb` | 1020 | a giant white mouse | 8922 | unassessed |

## Aggregated actions

Each run that dies is exported by tools/export-death.py (harness/run.sh). Curate assessment.json and report.md by hand; regenerate this index with `python3 tools/death_registry.py`; rerun a case with its logs with tools/rerun-death.py. Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.
