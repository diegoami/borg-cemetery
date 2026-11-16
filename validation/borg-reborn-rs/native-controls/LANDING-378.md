# #378 integrated-main landing controls

Owner authorized landing reborn #378 after the independent review/re-review.
Accepted reborn main `4ecb93d77c625e03d2b838837da597d07bfbabe2` was merged
into the feature branch, preserving recorder v0.2.0, survival fixes and both
harness receipt/plan checks. Clean measured integration commit:
`88a9437a7cbc96ceb7de16c1eecd9cc49c8b4bfb`.
Source digest: `2d1420b704fa8faa4a1972fe9548fdd2ebaa2a5fde98c9ff7ce9f4ba51d2ecef`.
Binary digest: `cfa793dbc42701d96f30345595aa9b5d4905977ca0d17507ca5ede5135d7b1a7`.

Three ordinary control deaths are appended through the immutable native
importer: the ordinary smoke Elf Mage (seed 102), vendored-core control
(seed 1011, Elf Mage, pristine core settings), and ordinary Druid control
(seed 1020). Raw game outputs remain in the source workspace; dossier payloads
preserve the actual source/build/configuration and log hashes. These are
integration controls, not additional independent population samples and not
synthetic scenario dossiers. No existing package or reviewed scenario packet
is overwritten. The earlier P1 bank remains tied to its original measured
runtime; no claim that this integration is the same runtime is made.

Scoped integrity check verifies all 82 qualified packages. All 869 previously
published package files retain their Git blob hashes; only generated union
index/README change. Ordinary and exact source smoke match all three stored
reference streams, 3/3 each. Synthetic-start/build contract tests run as part of
source CI before merging #378; no missing-death assertion is weakened.
