# M2 / synthetic P1 milestone packet

Status: prepared for owner-run review, not accepted. M1's review and implementation
pin remain separate and unchanged. The paired PR bodies pin the exact review heads.

The independent review of this scope is
[INDEPENDENT-REVIEW.md](INDEPENDENT-REVIEW.md) (reviewer MiniMax-M3, 2026-11-20,
Cemetery `ec332c62`, paired reborn `2faaadb1`, runtime `99473510`). It
recommends conditional accept, with one Low-severity wording finding in this
packet's charged-device statement. It is not owner acceptance.

## Runtime and bank

- Exact reborn runtime: `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d`.
- Runtime input digest: `bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a`.
- Local measured binary: `8336a9cad4d28eba8c9b284bce1f0ab3b2318eb65b6924413284eb2969d4e5c6`.
- Suite spec digest: `8030348f3d9a16d7b1cc5ef093806d0fe7934d4cf2b2aa7b0aff700a274031c9`.
- Bank: `synthetic/p1-warrior/`; one class, one seed, three starting depths,
  birth plus one observed level-5 tier. Six cells, 5,000 engine turns and
  30 wall seconds each. The declarative record is not a save.

## Actual evidence

All six local scenarios completed with valid evidence: **four deaths, two cap
survivals, zero harness/identity/timeout/unsupported failures**. A second execution
of all six cases has identical key, state and message streams. They are repeated
attempts of the same six cases, not twelve independent population lives.

The readable table is [report.md](report.md); compact machine outcomes and
per-stream evidence hashes are [results.json](results.json), with exact generated
[scenario specs](scenarios.json). Raw logs remain outside Git in the task's
`p1-real-suite`, `p1-real-suite-repeat`, and final-runner
`p1-final-suite-executed` evidence directories. A separate final-runner preflight
was rejected before any gameplay because a scratch build symlink was untracked;
its six identity-mismatch rows are retained in `p1-final-suite` and excluded from
valid gameplay outcomes. The corrected clean worktree reused the unchanged,
hash-verified 401597 build; no build identity was edited. Cloud runs upload
their own exact source/binary receipts and raw logs with 14-day retention.

Every qualified-near-death count is null with unavailable coverage. Low-HP
screens and generic refusal messages are explicitly provisional diagnostics.
Birth cases each recorded one “Nothing happens.” message and no “Nothing
happens!” message; observed-tier cases recorded neither. Adjacent birth messages
show a Recall scroll being consumed. No case stopped on the stall guard; all
terminal receipts say death or turns. These facts do not establish optimal play.

The tier came from a clean ordinary seed-101 Human Warrior run at level 5,
turn 18057: 58/72 source HP, synthetically healed to 72. Its capture digest and
clean source/binary/process/log identities are in the bank's catalog. Capture
on/off tests preserve all three play streams. One observation is not an average
or a claim that this kit is common. Normalization and missing historical knowledge
are explicitly declared; source saves/private Borg state are not restored.

## Validation and review findings

- Cemetery: 58 runner/tests, 50 native-tool tests; statistics check over 129 reports.
- Reborn: formatting, Clippy, 165 workspace tests and 328 core release tests pass
  (four existing ignored); 91 tool tests, 19 script tests, vendor audit pass.
- Native local suite: 81 tests, 16 dependency/fixture skips, zero failures. CI
  supplies the missing upstream Git object, bindgen, zoo and incident fixtures.
- Ordinary and exact smoke each match all three stored-reference streams, 3/3.
- Three ordinary control dossiers for the new source baseline are retained with
  immutable qualified IDs; the original 2,584-package snapshot verified and controls reconcile.
  All six task-control packages and the gameplay packets are now retained only
  in Cemetery under the accepted ownership rule; source pages become pointers.
  See [ownership-migration.json](ownership-migration.json) for byte-preserving receipts.
  These ordinary records are distinct from synthetic suite results.
- Direct export of a real synthetic death is rejected; reconciliation reports
  zero natural deaths for the six synthetic games, with no natural registry.
- The #378 review exposed a genuine bug: @1 could log requested player depth
  before the new cave was active. That evidence is marked superseded. @2 completes
  native generation before activation and checks real cave depth/pending state.
- Both cores now have real repeated startup tests. Only the two validated
  synthetic birth-option exceptions are authorized; ordinary behavior is intact.
- Unmarked one-way save reload is refused and independently excluded by exporter.

Current-head GitHub checks and the pinned synthetic workflow are authoritative
for cloud validation; see the PR bodies. The old @1 result packet is not reused
as accepted generated-cave evidence. Cemetery #7 merges before the reborn pin is
promoted; competing primitive #386 must not be merged on top without reconciliation.

## Boundary

This is a small execution/catalog/classification milestone. P2's wider catalogs
and qualified null-move evaluation, and P3's paired two-executable impact
comparison, remain unimplemented. No population or Borg-improvement claim is made.
Use [PROMPT.md](PROMPT.md) for the runnable owner-selected review.

## Review follow-ups (2026-11-16)

The owner-supplied reviews of reborn d406d2c9 and Cemetery e750549 are reviewer
input, not acceptance. The reborn reviewer built and ran both startup/build
suites (11 tests); the Cemetery reviewer ran 54 repo and 46 native-tool tests
but explicitly did not review the P1 runner, catalog, retained controls or suite
evidence. That part of the milestone still requires its scoped owner review.

One-way starvation remains unmeasured: a hungry character without food may
select return-home actions refused by the native rules and stall. The six cells
cannot establish long-horizon policy competence. #386's policy changes remain
separate. The libcrypto dependency is retained deliberately and documented for
adapter hosts; successful supported capture has empirical parity at seed 101,
not an exhaustive RNG-neutrality proof. Unsupported capture can terminate its
run as a harness failure and cannot stand in for a successful paired control.

The refreshed packet uses clean runtime 99473510 after the capture/lifecycle
review fixes. Its six outcomes and all 18 gameplay streams match the previously
reviewed runtime; raw logs are in `p1-review-suite`. Prior packets remain in Git
at e750549 and are not retroactively relabelled. The observed-tier catalog still
names its original 401597 source capture, independently of this execution pin.

## Independent milestone review and coordinated response

The full P1 scope has now been independently reviewed at reborn 34cec1fc /
Cemetery b55b07a. This supersedes the earlier note about guard-only coverage.
See [MILESTONE-REVIEW-RESPONSE.md](MILESTONE-REVIEW-RESPONSE.md) for the findings,
merge integrity, source-session ownership and remaining declared limitations.
The recommendation is conditional, not owner acceptance.

In particular, the birth cells retain an ordinary-before-one-way-option kit:
native one-way birth omits the Recall scroll that these cells consume at turn 3.
This is declared P1 normalization; the bank does not claim native one-way kits.
The observed tier contains no charged devices, and does not qualify the parser's
current generic pval ceiling as a kind-specific charge bound.

The final coordinated runner execution is retained from `p1-milestone-suite`
(clean runtime 99473510 in an isolated worktree). All 18 streams match the
previous `p1-review-suite`; evidence now also binds keys.log. The workflow's
verify step enforces these hashes against the retained packet automatically.
Cemetery checks after the follow-ups: 58 repo tests, 50 native-tool tests,
statistics over 129 reports. The reviewed birth normalization is unchanged.

## Scope and packet lineage after the 52dff9f review

The six scenario specifications are **paired conditions on three generated caves**,
all from seed 101. Birth and observed-tier cells at a depth share the initial
cave/coordinates (d5 50,15; d10 28,36; d15 159,16). The source tier also came
from seed 101. Each cell has denominator one. Four deaths and two cap survivals
are descriptive counts, not an outcome rate from six independent lives. Repeats
add no independent observations. Birth/observed differences include the inert
Recall-scroll action and the declared projection, so this is not an experiment
isolating character level alone.

Historical result files are now retained byte for byte as
[the b55b07a packet](checkpoints/p1-results-b55b07a.json) and
[the 52dff9f packet](checkpoints/p1-results-52dff9f.json).
[results-lineage.json](results-lineage.json) gives their exact file/build hashes
and an immutable reference to the #15 pilot. `results.json` is now frozen byte for byte at the 52dff9f reference. It historically
replaced the b55b07a packet (000d8d6f… → 8336a9ca…); both original files and
hashes are preserved above. Fresh follow-up results are retained separately in
`reproductions/20261116-followup/`, with both sets of stream hashes and a runnable
comparison receipt. Path/timing receipts differ; historical builds are not relabelled.

Three binaries have been recorded for runtime 99473510 / source bf9a451c:
`000d8d6f…` (b55b07a packet), `ba06d6fa…` (#15 pilot), and `8336a9ca…`
(52dff9f and the latest execution). All three report rustc 1.100.0 and GCC 14.2.0,
but were built in different directories. Same-toolchain bit reproducibility was
**not established**. The specific cause of the byte differences was not isolated;
we do not attribute them solely to toolchain versions, paths or timestamps.
This corrects the earlier cross-toolchain-only explanation. Full build identities
remain separate, while identical gameplay streams establish the limited observed
behavioural reproduction. See [FOLLOW-UP-52dff9f.md](FOLLOW-UP-52dff9f.md).

The latest follow-up leaves results.json unchanged, and records its new attempt
separately. All six outcomes and 18 streams match the frozen baseline under the
stricter semantic verifier. Checks: 58 repo tests, 50 native-tool tests and
statistics over 129 reports. Main's new qualified controls are merged without
replacing prior packages; the separate follow-up integrity receipt records it.
