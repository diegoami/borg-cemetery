# PR #26 review response

Review: [findings 1–7](https://github.com/diegoami/borg-cemetery/pull/26#issuecomment-6919006081)
against `7e362f916a744400388637359afba7bd855408a7`.

1. **Frame-less dossiers:** synchronized Cemetery main through `9b38f76` without
   rewriting any raw evidence. The candidate index now individually includes all
   37 terminal-level-1–10 caster dossiers without selected frames: 13 Druid,
   9 Mage, 8 Necromancer, 7 Priest. Each has `no_recorded_frames`, unknown
   inventory/spells, record digest and verified canonical death-ID reference.
   The 14 observed dossiers are explicitly only the frame-backed subset.
2. **Equipment counts:** the original 52 raw description signatures remain
   provenance, not equipment diversity. Fuel/stack-normalized, separately
   projected signatures yield 14 equipped sets and 21 pack type sets. Each case
   has exactly one equipped set across its seven selected T−105..T−5 frames.
   The README and PR headline now state this limitation. Normalization uses
   visible descriptions and declared plural folding, not inferred engine kinds.
3. **Living HP=0:** the screen now requires an explicit alive flag and includes
   HP=0. There are 41 qualifying observations, including the four zero-HP frames.
   Dead/unknown-death-state frames are excluded from this living screen; tests
   cover all three states.
4. **Recall/depth confounding:** independently checked the retained raw streams:
   all eight depth-3/5 cells consume the inert Recall scroll, versus zero of four
   depth-1 cells. A small timestamp correction to the review: consumption is at
   **engine turn 11, key positions 6 or 7** (`messages.log` records key position
   before engine turn). The README states the split and prohibits interpreting
   depth as an isolated effect. No birth kit or historical result was changed.
5. **Short horizon:** all four cap survivors cover 300 player turns; the actual
   engine stop boundaries are 3,001–3,003. Independently checked the capped
   Necromancers' state streams: 19 and 42 distinct positions, both still level 1.
   These limits are now explicit, without successful-progression claims.
6. **Hardening:** spell metadata and learned spells have field whitelists.
   Frames with missing spells are retained where record class metadata identifies
   the caster, with missing state explicit. Unknown/conflicting class metadata
   gets an explicit exclusion. Record digests are checked against death-ID
   sidecars where available; the README distinguishes them from published frame
   hashes. Input preflight now rejects tracked **and untracked** changes in
   `deaths/` or `scenarios/`. Regression tests cover these boundaries.
7. **Previously fixed runner gates:** no new runner change is necessary.
   `scripts/synthetic_suite.py:verify_results` already checks exact clean source
   commit/digest/capability identity and enforces near-death unavailable/null
   invariants. `classify` requires a valid expected binary hash and matching
   before/after receipts, rejecting `None`, empty strings and false values.
   `test_retained_comparison_detects_changed_streams_and_incomplete_cases` and
   `test_identity_and_key_log_receipts_cannot_be_bypassed` exercise those checks.
   Binary hashes may legitimately differ across toolchains; source and gameplay
   stream agreement are checked separately. No runner/native implementation was
   edited for this bank's review response.

Validation: 71 Cemetery tests and 53 native-tool tests pass; canonical death IDs
verify for all 213 retained dossiers; statistics check covers 131 reports; the
updated candidate index regenerates exactly apart from the documented checkout
pin after a commit. Retained attempts still match 12 scenarios and 36 streams.
`git diff --check` passes. No new gameplay runs were needed for extractor/docs
changes; existing outcomes and both attempts' build identities remain intact.

Caster equipment application is still unsupported pending reborn #382. This
response does not accept a milestone, merge into main or restore private Borg
memory in saved scenarios. The owner chooses/runs any re-review.
