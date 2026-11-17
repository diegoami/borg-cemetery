# Plan cap review #447

## Historical #440 comparison custody

The adjacent published PR and handover are preserved verbatim historical
summaries, not raw run evidence. The PR reports a 90-start comparison; its
numbers have not been independently verified in this follow-up. The original
seed manifest, per-arm configurations, raw runs and death inventory have not
been located. Do not count these summaries as reproducible evidence or new
samples. Original reporting errors, including the handover source hash, are
preserved here for audit; reviewed #440 source was
`ef85f725b5d26b22e7b4ea8f318e99d031442241c399d6d938c564c390ef1f9b`.

Source PR: https://github.com/diegoami/borg-reborn-rs/pull/440
Reviewed head: `82d8c985790e4915249b57a1440e0f2878e6a6f7`.
Follow-up: https://github.com/diegoami/borg-reborn-rs/issues/447

The fixture archive is copied byte for byte from Cemetery commit
`6dbad9fb0b1b9be81fedba8b2954685345f178d8`, with SHA-256
`8b1ad20508492af4bc991c760a6aa55aee2992f791ebb7e1bbd21fe5fc337615`.
The original archive remains untouched.

## #447 validation controls

Clean implementation commit `4a7a851902b0d5f5b39e20aed679cfc248a82200`,
source `3ec00513b59af9d2def75209ee98292c00e1e9ad9c0591db39aa6e2e911dbdbc`,
binary `fd41edabab253f4df08c3189ab8cdc9df666b892b31889752059f6ad15d28f9e`.
Three ordinary harness controls: borg-rs overrides off, seed 1011/race2/class1/100000;
original core seed102/race2/class1/20000; original core seed1020/race2/class2/100000.
All three natural deaths retained in the sibling native-controls registry,
with canonical encounter/key identities, actual configuration and build metadata.
These are validation controls, not an improvement study.
