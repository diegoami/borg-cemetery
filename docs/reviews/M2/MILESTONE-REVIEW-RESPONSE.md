# Independent M2 / synthetic P1 review response

Owner-supplied review: Claude Code, 2026-11-16, reborn 34cec1fc / Cemetery
b55b07a. The reviewer independently ran the six-cell suite twice, reconstructed
the observed tier, verified repeatability and ordinary references, and ran the
Rust/engine/Cemetery checks. This covers the broader P1 scope missing from the
earlier guard-only review. The recommendation was conditional on the merge
blocker, not owner acceptance. No PR is merged or milestone accepted here.

## Findings and ownership

1. **Merge blocker resolved:** merged accepted Cemetery main 5abfdbe at 74cb8ff.
   Only generated native-control README/index conflicted. The immutable importer
   regenerated the union. All 803 qualified-package files from both parents
   retain their original Git blob hashes; 73 qualified packages pass the scoped
   integrity checker. See merge-integrity.json. No accepted dossier is replaced.
2. **Birth kit declared:** frozen P1 birth cells retain the ordinary Warrior kit
   before one-way options are applied. At native class.txt:157 a one-way birth
   omits Word of Recall; P1 retains it and spends one at turn 3 without effect.
   This is now explicit in the bank, schema docs and packet. It is not described
   as a native one-way kit. Runtime 99473510, bank/spec IDs and gameplay streams
   are preserved; the owner still decides acceptance of this bounded choice.
3. **Registry isolation belongs to the coordinated reborn session:** that session
   owns a stacked source fix checking native-tool bytes against death-tools-pin,
   including modified/missing files. Its planned subtree comparison allows safe
   documentation/evidence-only descendants and rejects stale API-1 guards. This
   Cemetery session has parked its overlapping source drafts and will publish
   the exact Cemetery head for that session to reference. No API/pin race and no
   second startup implementation is introduced. See the coordination comments
   on #7 and #378 for the final source fix/validation.
4. **Retained-stream CI gate implemented:** machine evidence now includes keys.log
   as well as state/messages hashes. The verify command rejects altered outcomes,
   runtime/spec identities, missing/duplicate cells and changed/missing stream
   receipts. CI runs it after the real bank. Tests mutate each of the three
   streams independently and exercise missing/duplicate cases and changed status.
5. **Timeout cleanup fixed:** the runner owns the launcher/engine process group;
   an outer timeout kills that group and reaps the launcher. A real parent/child
   regression checks the grandchild is no longer running. **Charge bound remains
   a declared limit:** pval has a numeric ceiling, not a per-kind charge cap. This
   fixed observed kit has no charged devices and all pvals are zero. A stricter
   native cap is parked for source-side qualification, rather than changing the
   reviewed runtime or implying this bank qualifies wider charged-item tiers.

## Review boundary

Keep measured runtime 99473510940b8a7bd6e77ad61e3a2b00c72a6e6d and the original
401597 catalog provenance distinct. Re-run the bank with the changed Cemetery
runner, preserve all outcomes/attempt receipts, and compare all 18 gameplay
streams before updating the retained packet. Current-head CI and the exact paired
publication heads are linked from #7/#378. Earlier packets remain immutable in Git.

The prior statement that P1 itself was not reviewed is superseded by this
independent milestone review; new review fixes and owner acceptance remain open.
M1 and the competing #386 remain separate. Do not advance reviewed/tags or start
P2/P3 based only on this recommendation.

## Coordinated source follow-up references

The reborn session published its source-only fix as reborn #412, head
2faaadb1a8c9aee07fddcae905eee46699e99005, stacked on #378. It reports 94 tool and
19 script tests passing and real stale-toolkit/synthetic-death rejection with no
registry creation. It will integrate only into #378 after CI; that session owns
the source branch and body. The low-priority kind-specific charge follow-up is
reborn #411. No source/runtime/native-tool pin/API change is required by the
Cemetery fixes. Current integration and checks are recorded in the PR bodies
and the coordination comments, without treating either as owner acceptance.
