# D-cd41503969ecd7a6ec37a1af8cccc92ef60f9206955ff19fb0d4ed10ecee438c: a crow at turn 2041

Half-Troll Necromancer, character level 1, depth 1 (max 1), seed 1043, implementation `rust`, flags `menu`.

Build `24be98732748230062882fe2b7d9601dba5e2cc0` (dirty: no), binary `e58e7d190068`. Keys `5b2269df3829`; raw logs stay in `https://github.com/diegoami/borg-zoo/actions/runs/45685728667/artifacts/15057175436 archive member partial/full-4-necro-3` (not committed).

Core decision trace: the last 167 of 167 thinks in `trace-core-tail.jsonl`, with selected check, queued keys and `params-core.json`.

**Unassessed.** Basic dossier written by `tools/export-death.py` at the end of the run (RULES 12). Upgrade it with the full death tooling (T1.6) before investigating.

## Original run evidence

The shipped native Borg produced this dossier during the Track R4.5 parity suite at the fixed `24be98732748230062882fe2b7d9601dba5e2cc0` source pin. The `check` and `switch` arms used candidate `83e28cd4c3fb9a3a0eb4cb75e0ff8d635f25a9d2` and produced the same key, message and state streams and terminal outcome. The three runs represent one game for death reconciliation. [Zoo full gate](https://github.com/diegoami/borg-zoo/actions/runs/45685728667/job/139508652763)

The original cell was `partial/full-4-necro-3` in native shard 3. Its ZIP SHA-256 was `0820b9c5c82a009ac3ee5d1aa35cf24528199f149a3d05f0c60d2216ac1ed43f`. The suite manifest supplies the build identity, and the native runner export gave this same dossier ID. [Original shard](https://github.com/diegoami/borg-zoo/actions/runs/45685728667/artifacts/15057175436) · [Preserved suite manifest](evidence/suite-manifest.txt)

- [Original keys](evidence/keys.log.gz) · [Original messages](evidence/messages.log.gz) · [Original state](evidence/state.log.gz)
- [Effective borg.txt](evidence/borg.txt.gz) · [Birth profile](evidence/reborn-default.txt) · [Resolved settings](evidence/settings-resolved.json) · [Evidence checksums](evidence/SHA256SUMS)

The stream hashes in the record cover the original uncompressed bytes. The birth inputs and original streams are retained here. A fresh rerun was not performed as part of this import.
