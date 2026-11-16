# Attack preference review follow-up #424 / PR #426

Source 76d05952 labels raw and weighted selected-attack utility only when they
differ; default notes stay unchanged. Source hash 3c0df6b9e0da84576d669fdcc48b0d350d995b9d5269b78cb050b1ea5337e276.

The native Mage neutral control (seed1011/race2/class1/cap100000) has identical
keys/messages/state to the pre-follow-up 25e89494 control in recorder-sync/full.
It dies to a cave spider at18903 with keys6c02605eeaac. The deliberately weighted
spell500/melee2000 case logs melee raw6/weighted12; trace on/off keys/messages/state
match. The original-core seed102/race2/class1/cap20000 retains Fang's exact
50491fa13924 key hash. No survival or independent-population claim.

Initial CI43873596430 stopped on strict reconciliation because this source identity
was absent from the old immutable archive; its original artifact is retained.
Local controls were independently generated and imported before a fresh CI run,
which must reconcile against this published evidence. Do not compare the fresh
registry only with itself. All four imported source records and their payloads
are preserved; two weighted processes are repeats of one life, not independent.
An attempted original-core run used the invalid selector `original` and exited2;
its diagnostic is retained. The corrected run uses the supported selector `reborn`.

Local formatting/Clippy,165 workspace tests,336 core tests/four existing ignores,
vendor check and strict package integrity pass. Original gameplay logs/builds
remain under /workspace/work/424-*; the receipts retain actual hashes and settings.
