# M2 / synthetic P1 milestone packet

Status: prepared for owner-run review, not accepted. M1's review and implementation
pin remain separate and unchanged. The paired PR bodies pin the exact review heads.

## Runtime and bank

- Exact reborn runtime: `401597cafd16f8330590763aa9bc15c10e40e5be`.
- Runtime input digest: `8a61938aa14162168a6b669b8b5b7ca40ff21ff04890665c5e533984f85fb076`.
- Local measured binary: `f039fa852ff368cff59187e5260fa3e13f91bb01dfd8b7b46cf9b44d79e73a20`.
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
`p1-real-suite` / `p1-real-suite-repeat` evidence directories. Cloud runs upload
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

- Cemetery: 53 runner/tests, 46 native-tool tests; statistics check over 129 reports.
- Reborn: formatting, Clippy, 165 workspace tests and 328 core release tests pass
  (four existing ignored); 88 tool tests, 19 script tests, vendor audit pass.
- Native local suite: 80 tests, 16 dependency/fixture skips, zero failures. CI
  supplies the missing upstream Git object, bindgen, zoo and incident fixtures.
- Ordinary and exact smoke each match all three stored-reference streams, 3/3.
- Three ordinary control dossiers for the new source baseline are retained with
  immutable qualified IDs; the original 2,584-package snapshot verified and controls reconcile.
  All six task-control packages and the gameplay packets are now retained only
  in Cemetery under the accepted ownership rule; source pages become pointers.
  See ownership-migration.json for byte-preserving receipts.
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
