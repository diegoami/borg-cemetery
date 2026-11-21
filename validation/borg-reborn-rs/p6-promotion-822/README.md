# P6 promotion-tree smoke (#822)

Validation of the re-review's final question: main advanced to398f76ef after
the reviewed head29c44cbc, including #862 and new smoke references. Exact
validation merge31e94a65 has treefd6b1141, equal to the read-only merge of
those published parents. It is retained on source branch task/T822-promotion-smoke,
not merged into track-p. No source edits, parameter tuning or main promotion.

Clean source/build, GCC right-to-left argument order. Build identity and
compressed exact executable retained. Three native borg-rs/no-errand smoke
runs stop alive at their fixed20k turn caps; no deaths or aliases added.
All keys/messages/states independently match main's retained xz references
byte-for-byte in3/3 runs. Reference bytes are preserved, not re-recorded.
This is smoke coverage only, not a new cohort or a claim of improvement.

receipt.json records parents/tree/build identity, outcomes, independent
stream hashes and decompression checks. Every raw run file is retained;
files larger than64k are gzip-compressed with original-byte hashes in the
receipt. file-manifest.json hashes every stored artifact except itself.
No prior validation package is modified. Existing Zoo611's passing18-pair
evidence remains scoped to its older exact pair; this packet adds only the
promotion-tree/reference consistency check, not a new production override.

Review: verify manifest/decompression/binary, exact merge tree and clean build,
all three configs/receipts/native runs/outcomes, and equality of the supplied
reference and candidate streams. Check current CI. Owner chooses reviewer
and accepts P6/main promotion; neither is implied by publication.
