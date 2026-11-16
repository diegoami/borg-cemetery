# M2 / synthetic P1 milestone packet

Status: prepared for owner-run review, not accepted. M1's review and implementation
pin remain separate and unchanged. The paired PR bodies pin the exact review heads.

## Runtime and bank

- Exact reborn runtime: `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d`.
- Runtime input digest: `bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a`.
- Local measured binary: `000d8d6f08d976fa25df75d9b330a13e529ad9dff0b3716e07f6ca2a0abcc6a7`.
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

- Cemetery: 54 runner/tests, 50 native-tool tests; statistics check over 129 reports.
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
