# Synthetic suite contract, P1

`borg-cemetery/synthetic-suite@1` is a generated-dungeon definition, not a saved
position or a replay. P1 ships the reborn execution adapter; scheduling, stable
scenario identity, normalized outcomes and reports are separate from execution.
Another engine needs its own reviewed adapter/capability and character-record
contract. An unsupported backend is never advertised as runnable.

The checked-in example is `synthetic/p1-warrior/suite.json`: Human Warrior,
seed 101, starting depths 5/10/15, birth kit and one real observed level-5 tier.
There are six cells, each capped at 5,000 engine turns and 30 wall seconds.
Native downward travel remains legal; depth means **starting depth**. Native
harness stopping is at the first key at/past the cap; actual turns are recorded.

## Definition and identity

| Field | Meaning |
|---|---|
| schema, suite_id, revision | Immutable interpretation and owner-chosen revision |
| seeds, depths | Unique bounded grid values; deterministic sorted generation |
| turn_cap, wall_seconds | Gameplay horizon and independent wall limit |
| candidate_screen | Explicit `low_hp_candidate` rule; never near-death qualification |
| character_builds | Unique ID, race/class, explicit core, exact profile digest, birth or record dependency |
| runtime | Supported repository and exact 40-hex commit; no moving branch |

A record build names exact native-record and catalog files plus SHA256 digests.
Catalog provenance binds a clean measured source/binary, capture receipt, seed,
source log/config/summary hashes, sampling limits and normalization. The source
run and any save bytes are not execution dependencies. P1 uses one actual
observation, not an invented average or a population-representative kit.

The spec digest excludes executable selection. Each scenario hashes canonical
suite identity/revision, seed, starting depth, character/profile/catalog identity,
stop/screen rules and required harness contract. Grid order and another target
executable do not change scenario IDs. Changing these starting conditions does.
The original manifest byte digest is retained separately. Duplicate IDs/JSON
keys, missing definitions, changed dependency bytes, unknown/ambiguous screen
rules and excessive grids are refused. Limits are 64 cells, 100,000 turns and
120 wall seconds per cell; the approved P1 bank is much smaller.

## Adapter and evidence

The real adapter verifies the exact clean target checkout, capability declaration,
source-input digest and binary digest. The engine must support contract
`borg-reborn-rs/synthetic-start@2`, including the requested core. @1 is deliberately
not advertised: its old first-key/player-depth check did not prove the cave was
active before Borg activation. Those old development results are superseded.

Each game runs in an isolated directory under the shared engine lock. The child
receives a small explicit environment, an immutable profile copy and, for a tier,
a private declarative record copy independently hashed by the engine. No account
credentials, arbitrary commands, inherited Borg policy, binary override, data
override or save root comes from the suite. The harness reports actual cave depth,
absence of pending generation, character tier and record digest. Runtime binary
before/after hashes, configuration and first/terminal log boundaries are checked.

Raw output directories are preserved outside Git. Each attempt writes scenario
and result JSON; the suite writes `scenarios.json`, `results.json` and `report.md`.
Existing output directories are never overwritten. Preflight failure produces
one invalid result per scheduled cell, with zero games attempted. Timeouts and
failed receipts retain partial evidence without a death/survival label.

## Independent outcome fields

- Terminal categories: `death`, `survived_to_cap`, `stopped`.
- Invalid execution categories: `harness_failure`, `identity_mismatch`, `timeout`,
  `unsupported`. A dead/alive-looking partial summary cannot override these.
- `qualified_near_death`: coverage `unavailable`, count **null** in P1. The later
  engine null-move evaluator is required; absence of it is not zero exposure.
- `candidate_screen`: distinct sampled engine turns with living HP at/below the
  configured threshold (2 in P1), with explicit pre-key sampling limitations.
  A scenario can die and contain candidate screens; these are separate facts.
- `refusal_messages`: exact generic “Nothing happens.” / “Nothing happens!”
  message counts, with coverage. They do not uniquely identify an action or
  establish its energy/resource cost; inspect adjacent messages for attribution.

Reports preserve every scenario denominator, depth/tier outcome counts, sampled
minimum living HP distribution, death causes and missing evidence. Synthetic
results never enter natural death/population statistics or `deaths/`. The engine
also refuses unmarked one-way save reloads, and the native exporter/reconciler
independently exclude one-way/synthetic lineage. No synthetic dossier is created.

## Commands and cloud path

```sh
python3 scripts/synthetic_suite.py generate --manifest synthetic/p1-warrior/suite.json --out /tmp/p1-scenarios.json
python3 scripts/synthetic_suite.py run --manifest synthetic/p1-warrior/suite.json --source /path/to/exact-built-reborn --out /tmp/p1-results
```

Use a fresh result path. The runner takes the engine lock internally; do not wrap
it in another lock on the same file. Build the exact manifest commit first, with
`BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh`.

`.github/workflows/synthetic-suite.yml` validates the bank, checks out the exact
reborn commit, builds it with Rust 1.100.0, and runs six cells in a read-only job.
It publishes a readable job summary and evidence artifact with 14-day retention.
Raw logs stay in artifacts, not Git; compact reviewed outcomes may be retained.
The workflow does not archive to the natural registry or use write credentials
for gameplay. Source/binary/toolchain identities remain in the result packet.

P2 expands observed catalogs and implements qualified null-move evidence after
review. P3 adds compatible paired two-executable impact comparison. P1 makes no
population, improvement, historical-death-reproduction or average-kit claim.

The P1 runner applies named profiles to the original reborn core. For the
vendored `borg-rs` core it accepts only an empty/comment-only profile, meaning
explicit pinned defaults. Named overrides are rejected instead of silently
ignored; a calibrated core-profile adapter is later work. The engine primitive
and real startup tests support both cores. The approved P1 bank uses reborn.
