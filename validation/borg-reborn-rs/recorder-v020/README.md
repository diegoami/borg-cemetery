# Recorder v0.2.0 adoption evidence

Canonical evidence for borg-reborn-rs task #351 / source PR #393. The source
repository retains implementation/tests and pinned pointers; gameplay reports
and retained natural-death packages live here under Cemetery ownership.

- [Current-base report](P351-VALIDATION.md) and [per-case receipts](P351-VALIDATION.json).
- [Current-base dossier map](P351-DOSSIER-MAP.json).
- [Historical pre-revert report](P351-PRE-REVERT-VALIDATION.md) and its JSON/map.
- [Byte-preserving migration manifest](migration.json).

The first epoch compared source 0f2e003f with recorder adoption b2532940 before
the owner reverted #355. The final epoch compares restored source 87717140
with recorder adoption 7d2af920. Both epochs preserve their actual identities;
no old result is relabelled as a result of the restored policy.

All 54 packages retain their original qualified IDs, original record bytes
and every payload byte. All producer report/map bytes are unchanged. Their
old docs/deaths paths are historical source paths; migration.json maps them
to validation/borg-reborn-rs/native-controls/deaths here. Runtime images,
raw sessions and saves stay outside Git; frozen image locators and hashes
are retained, not executable bundles. Paired/repeated validation packages
are not independent population lives or a survival-improvement claim.

The v2 consumer passes fresh/captured-load replay and final-save/checkpoint
checks. All 45 recorder-off play triples match in each before/after epoch.
V1/v2 recordings are incompatible; exact old sessions/images are preserved.
Coverage limits and actual dirty/clean metadata are explicit in the reports.
