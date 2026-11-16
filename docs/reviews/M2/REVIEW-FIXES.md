# P1 review response, 2026-11-16

Reviewer: Claude Code. Implementer: GPT-6 / Codex family. This response addresses
owner-supplied review input; it is not acceptance or a substitute for review of
the P1 runner. Exact source/runtime and paired publication heads are in the PRs.

## Reborn #378, reviewed d406d2c9

- Missing capture: fixed. Every requested capture reports `build_capture_status`
  (`captured` or `absent`) and `build_capture_requested_level`. Only a successful
  capture has turn/level/hash fields. Absence includes an unreached or skipped
  exact level, and does not alter the gameplay outcome. A real 300-turn level-15
  request now asserts absence, no file/hash and identical control streams; the
  successful level-5 parity test asserts the positive status too.
- Level lifecycle: the wrapper now guards leave with `character_dungeon`, matching
  upstream. Its patch names `run_game_loop` and the exact engine pin, with an
  explicit lifecycle/arena recheck at pin bumps. Fresh starts are non-arena.
- One-way starvation: documented as an unmeasured policy limitation. A hungry
  no-food character can choose return-home actions refused by the native rules
  and stall. The six cells do not establish long-horizon policy competence.
  #386's policy changes remain a separate follow-up; no second primitive lands.
- OpenSSL: retained intentionally. Adapter/zoo hosts need libcrypto and builds
  need its development package. The engine attests the applied bytes independently
  of run.sh using the maintained implementation; a custom SHA-256 implementation
  is not added for this milestone.
- Unsupported capture: remains an explicit harness failure that can terminate
  its run. It must not be used as a successful paired control. RNG neutrality is
  empirically shown for the supported seed-101 level-5 kit, not claimed as an
  exhaustive proof over every possible item. These limits are now explicit.
- `initial_generation_pending` is a postcondition receipt: successful startup
  must record false. A pending cave fails before Borg activation.

## Cemetery #7, reviewed e750549

- Marker flags are stripped/lowercased and recognize `start-depth`, `start_depth`
  and `synthetic`, bare or followed by equals/whitespace, from either flag source.
  Regression cases cover all six spellings listed by the reviewer, twice each.
- Reconciliation prints `SKIPPED: path: reason` for exclusions, including strict
  marker aliases rejected conservatively and malformed native option receipts.
- Non-object `game_options` now fails closed instead of raising AttributeError.
  Export tests cover nonempty/empty lists, strings, integers and booleans. A mixed
  reconciliation scan includes malformed options, one-way lineage, synthetic and
  strict-config exclusions plus an ordinary death; it continues and reports the
  ordinary death as missing its dossier.
- Natural preservation now covers JSON false together with config `synthetic=0`
  and `start_depth=0`. The native one-way pair intentionally requires JSON true
  on both options; loaded alone or string/numeric lookalikes do not prove lineage.
  A test and comment pin that choice. Explicit synthetic/depth markers still
  fail closed independently.
- Native-tool docs now state the literal accepted ordinary markers, the native
  one-way rule, malformed-receipt behavior and visible scan output. The heading
  is separated correctly. PR descriptions/pins describe the complete P1 scope.

## Validation and retained evidence

- Reborn local engine suite: 81 tests, 16 existing dependency/fixture skips,
  zero failures. Final tools: 91 tests; script tests: 19. Runtime source code
  changes are in the frontend/wrapper only; current-head cloud CI validates the
  full Rust, recorder, instrumented engine/reference and reconciliation gates.
- Cemetery: 54 repo tests, 50 native-tool tests; statistics check: 129 reports.
- Clean runtime: `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d`, source digest
  `bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a`.
- Refreshed six-cell P1 run: four deaths, two cap survivals, zero failures.
  All 18 key/state/message streams equal the prior reviewed runtime's streams.
  Raw logs: task workspace `p1-review-suite`; exact receipts/hashes: results.json.
  Previous runtime evidence remains immutable in the e750549 Git snapshot.
- Ordinary smoke matches all three stored-reference streams for all three cases.
  Three new-source ordinary control packages are retained in Cemetery's native
  control registry, using the immutable importer. No synthetic outcome is counted
  as a natural control. Registry/source/build identities are retained separately.

The Cemetery reviewer explicitly did not review the P1 runner/catalog/evidence
or retained controls. The owner-selected milestone review still needs to cover
that scope using PROMPT.md. Nothing here accepts M1/M2, merges/closes a PR or
advances the reviewed boundary. Canonical landing recommendation remains #7 then
#378, with #386/#377/#6 excluded from that competing startup path.
