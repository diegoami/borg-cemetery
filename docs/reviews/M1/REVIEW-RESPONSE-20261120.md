# Response to the independent M1 review (2026-11-20)

Status: reviewer recommendation is conditional accept; owner acceptance is pending.
The [MiniMax-M3 review](https://github.com/diegoami/borg-cemetery/pull/1#issuecomment-7037479075)
found no defect in the frozen M1 implementation. Its three findings concern the
relationship between that review and the moving `main` branch.

## F1: moving PR head and inaccurate scope statement

Confirmed. The M1 implementation remains
`cd562eabc40267a15be3eb7d2036d65e6f0c4a5a`, with historical publication
`7d5d1422d4429db932c5f3d3b6279a837ec9123b`, from baseline
`44d97669ebdf7390b384656c61365b0ca30f3266`.
PR #1 is `main` to `reviewed`, as required by AGENTS.md. Later work continued
on main, so its current diff includes M2, canonical death identities, additional
schemas, runners and evidence outside the frozen M1 review. The earlier
documentation-only statement describes the historical publication interval;
it does not describe the live PR.

PLAN.md, the packet and PR metadata now distinguish these boundaries. The
dated integration snapshot checked for this response is
`3c2614a7cf177ef4b72cf40e59541d07b2c9f87c`. The response publication commit
is recorded separately in the PR body; it only changes review documentation.
Later main commits require their own validation and do not silently extend
the reviewed M1 scope.

This corrects the description but does not review or accept the intervening
implementation. Do not merge PR #1 on the strength of this M1 recommendation:
that would advance `reviewed` across later work too. The concrete acceptance
proposal is to accept M1 only at its historical publication pin, keeping
`reviewed` unchanged until the intervening scopes have their own decisions.
If the owner instead wants a merge containing only M1, a frozen-head PR requires
an explicit exception to AGENTS.md's `main` to `reviewed` rule. Neither option
has been selected or performed by this response.

## F2: later regenerated case pages

Confirmed as later presentation changes, not a request to undo canonical IDs.
The D0007 page and other generated views acquired content-derived identities
after M1. Those current pages are outside the historical M1 publication scope.
The old presentation remains available at the publication pin; original raw
evidence and published hashes are not changed by this response. Canonical IDs
and historical alias pointers remain intact under the owner's identity rule.

## F3: receipts for the actual integration snapshot

Confirmed. Historical CI remains evidence for its own exact commits only.
The GitHub PR-triggered checks for integration snapshot `3c2614a7` both passed:

- [Check cemetery runner, run 44724544300](https://github.com/diegoami/borg-cemetery/actions/runs/44724544300).
- [Synthetic P1 suite, run 44724544258](https://github.com/diegoami/borg-cemetery/actions/runs/44724544258).

These results validate that snapshot, not later commits or milestone acceptance.
The PR body records local checks and any CI receipts for the response publication
separately. The review's missing end-to-end manual cloud workflow and native/UI
re-execution coverage remains explicit; no such execution is claimed here.

## Response validation

The response leaves code and gameplay evidence unchanged. Canonical identity
validation covers 1,700 retained dossier locations; deterministic statistics
validation covers 137 reports. Response links, code fences and whitespace
checks pass, and the M2 item-type reproduction command was executed against
the exact runtime Git object. The local repository suite was interrupted while
waiting for the shared game-execution lock in a fake-adapter encounter test;
no completed local repository-suite pass is claimed for this response. Use
the response publication's own GitHub checks for its completed suite receipt.
