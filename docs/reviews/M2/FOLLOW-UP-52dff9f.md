# Response to the 52dff9f review

The owner-supplied Claude Code review recommends approving guard/suite changes
with no blocker, not owner acceptance. It independently reproduced the six cells
and all 18 stream comparisons and rechecked package preservation. This delta
addresses its follow-ups without changing reborn or the frozen runtime/bank.

- **A / verification semantics:** verify now checks manifest, exact clean runtime
  and source/capability identities; deterministic terminal/HP/screen/progress
  fields; and hard unavailable/null near-death invariants in both packets.
  Binary/path/timing receipts intentionally remain build/attempt-specific.
  Mutation tests cover source/manifest/near-death/death-cause/HP changes as well
  as all three streams and missing/duplicate cases.
- **B / lineage and binaries:** b55b07a and 52dff9f result files are preserved
  byte for byte under checkpoints, with hashes in results-lineage.json and an
  immutable reference to #15's a5874c3 reproduction. The README explicitly states
  which binaries belong to which execution. Their declared compiler versions
  match; bit reproducibility is not established and the byte-difference cause
  was not isolated. The earlier cross-toolchain explanation is withdrawn.
- **C / CI scope:** action references are pinned to commit SHAs. The gate is a
  regression check; jointly editing runner and reference still needs review.
- **D / interruption:** process-group kill/reap now runs in finally, on normal
  completion, wall timeout and exceptions. CLI SIGTERM raises an exception;
  the real interruption regression stops the separately grouped grandchild.
- **E / evidence completeness:** keys/state/messages are mandatory and appear in
  missing_evidence. Key-line count must equal both state rows and summary.keys.
  Missing/falsy expected binary digests fail identity checks. Tests cover those
  paths, before/after executable digest mismatches, malformed timed_out and a
  terminal turn outside the native signed-32-bit counter.
- **#15 paired-cell scope:** docs now state three caves x two conditions on one
  seed, denominator one per cell, no outcome-rate or isolated-tier-effect claim.
  The ordinary-before-one-way kit/Recall action remains explicitly declared.
- **Docs:** numeric JSON zero and string zero are distinguished in guard wording.
- **Concurrent main:** merge the accepted main and regenerate the qualified-only
  registry index through the importer, preserving parent package blobs. The new
  integrity receipt records this separately from the earlier 73-package merge.

The original prototype and historical packets are not retroactively relabelled.
#15 remains an immutable external reproduction, not new independent lives.
P1 still has one tier and no charged-device qualification/null-move evaluator.
Source #411 owns the per-kind charge follow-up; no native-tool pin/API changes
are needed. The reborn session owns #378; this session changes only Cemetery.

Validation and final exact head/CI are recorded in #7. The owner still decides
acceptance; no merge to main, reviewed-boundary change or acceptance tag is made.

## Validation receipt

58 repo tests and 50 native-tool tests pass, statistics cover 129 reports, and
79 qualified native-control packages pass the scoped immutable-package check.
The new main merge preserves all 869 parent package file blobs (see
followup-merge-integrity.json). A fresh six-cell execution gives four deaths,
two cap survivals and no invalid outcomes; all 18 streams and deterministic
metadata match the unchanged 52dff9f reference. Both attempts' complete receipts
are committed, with a runnable comparison in the follow-up verification.json.
The workflow pins action commits and explicitly selects Rust 1.100.0.
