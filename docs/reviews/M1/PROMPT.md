# Independent M1 reviewer prompt

Review diegoami/borg-cemetery M1: recorded runs, replay and alternative human play.
This is a milestone-wide independent review, not a request to implement the next
stage or to rubber-stamp passing tests. The owner chooses the reviewer and will
decide acceptance. The implementation was produced by Codex/OpenAI GPT family;
if using a model reviewer, use another family.

## Pinned implementation

Baseline: `44d97669ebdf7390b384656c61365b0ca30f3266`.

Implementation head: `cd562eabc40267a15be3eb7d2036d65e6f0c4a5a`.

The review PR body additionally pins its publication head, including review/process
documents. Read those documents from the PR, then audit the exact implementation
diff above. Check any difference between that implementation pin and PR head:
review preparation must not hide further code/data changes. A changed implementation
requires refreshed pins and validation.

## Contract and scope

Read AGENTS.md, PLAN.md, README.md, docs/analysis-pipeline.md and the M1 packet.
Inspect the code and evidence rather than trusting their claims. The owner wants:

- CI runs of specific borg-rs/reborn versions, especially retaining seeds;
- real death/near-death sequences from an inferred reasonably stable point,
  human-readable accounts, inventory/spells and actual visual evidence;
- executable saved scenarios for comparing versions without confusing branches
  and reruns with independent lives;
- real recorder playback where available, with exact requirements and honest
  separation of original replay, recorded frames and new saved-position play;
- generated per-case build/watch/play commands, shared cached versions, and human
  continuations indexed under Alternative human play in the original report;
- durable evidence, clear unavailable states, preserved original records and
  no fabricated success, human control, exact start or general survival result.

## Check independently

1. Inspect the full diff and changed workflows. Review persistent identities,
   mutable refs, seed validation, summaries, failure/cancellation paths and archive
   publication. Check that no failure can become a death/rescue or disappear.
2. Follow one case as a person from the root index, through its report, inventory,
   animation, build/watch instructions and saved/human alternative replay. Readable
   Markdown must not merely relabel serialized machine dumps.
3. Verify save/hash/turn/version bindings, checkpoint eligibility, repeated-key
   stability logic, detector assumptions, episode overlap and actual world/player
   timing. Especially inspect S0003: saved 3402, marked 3432, death 3640; Fang is
   the visible canine glyph C once encountered. Human actions can avoid the encounter.
4. Audit recorder paths and immutable pins, partial/last-frame behaviour, GUI
   capture/replay, fresh-Borg/saved-RNG semantics, actor classification, exact-cache
   requirements and whether replay verification proves the claims shown to people.
5. Audit human recording attachment and later attachments: preserve original and
   unrelated report content, retain evidence after failures, avoid fake independence
   and misleading living-outcome statements, and make future replay practical.
6. Prove cache hits do not invoke compilers/configuration. Examine interrupted
   build phases, shared per-version use, executable/resource identity, relocation,
   source/cache modifications and concurrency. Do not remove unique evidence.
7. Audit the manual seven-case analysis and the five bounded D0007 arms. Check
   score calculations against the pinned source, negative outcomes, refusal
   violations, fresh-Borg limitations and whether proposals exceed the evidence.
   This pass is not a blind calibration study or proof of general survival gain.
8. Audit the native-tool ownership move, source-context forwarding, immutable CI
   toolkit pin, registry lock and canonical-index guard. Historical reborn IDs
   collide with cemetery IDs; there is no bulk migration. Reconciliation checks
   records, not publication. Check both sides of the linked integration PR.
9. Audit statistics/build separation, known/missing seed provenance, selected-death
   denominators, family overlaps and repeats. The external historical inventory
   is a pinned statistical snapshot, not a migration or a complete run cohort.
   Check dirty builds, different executables at one commit, core/profile settings,
   pinned source links and offline deterministic regeneration.
10. Run focused checks. Basic suite:

```bash
python3 -m venv /tmp/borg-cemetery-review-venv
/tmp/borg-cemetery-review-venv/bin/pip install -r requirements-media.txt
/tmp/borg-cemetery-review-venv/bin/python -m unittest discover -s tests -v
/tmp/borg-cemetery-review-venv/bin/python -m unittest discover -s scripts/native/tests -v
/tmp/borg-cemetery-review-venv/bin/python scripts/build_statistics.py --check
```

Use a fresh isolated checkout/cache for destructive or failure-injection checks.
Native builds/runs use `/tmp/angband-validation.lock`; do not race an active game.
Case commands accept `--cache /tmp/your-review-cache`. Do not attach synthetic
play to real cases, modify sibling repositories, publish new recordings, merge,
tag acceptance or select the next milestone. A temporary synthetic case is
appropriate for report-mutation tests; label it accordingly.

## Deliverable

Post a review on the milestone PR. For each finding give severity, exact path/line,
trigger and observable consequence, evidence/reproduction, and an actionable fix.
Separate confirmed defects, missing evidence, acceptance decisions and later-work
suggestions. Assess the known limitations in the packet explicitly. Finish with
an accept / conditional accept / changes-required verdict and what you did not
check. The owner decides and merges; this review does not auto-accept itself.
