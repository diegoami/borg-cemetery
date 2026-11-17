# Caster encounter bank: 361 runnable starts

**361 distinct saved starts**, covering only low-level casters. The full bank
ran **361/361 valid in 245.06 seconds** on accepted reborn main `6d1bca10`.
The separate eight-case smoke suite ran twice in **4.85 seconds**, with all24
key/state/message stream hashes matching. No build or birth replay is in either
timed loop. Individual class shards contain at most eight cases.

| Class | Cases |
|---|---:|
| Mage | 100 |
| Druid | 40 |
| Priest | 129 |
| Necromancer | 92 |

There are **40 source lives**, not361 independent games. The bank combines eight
previously published starts with encounters from32 prespecified natural births.
Those new births produced14 deaths and18 cap survivors. Every death is retained,
including level1 and town deaths. All14 reproduce from exact birth seed/build/
configuration with matching death endpoints and key/state/message hashes;
[recipes and verification](evidence/reproduction/) require no recorder.

Observed starting levels are1–4. [Coverage](coverage.json) records **13 equipment
kind/slot combinations**,29 empty-mana,82 partial-mana and250 full-mana starts.
These are observed combinations, not an exhaustive equipment matrix. Each case
keeps its actual equipment and pack state; charged, enchanted or otherwise
complex native items stay in the engine save. Eight older cases' equipment
coverage is established by the first actual loaded observation, archived in
`evidence/legacy-initial-coverage/`. Race, source-family, gear, inventory and
resource details are available per case. Druid counts are smaller because these
runs died earlier; we did not pad them with duplicate starts.

## Run the bank or a fast subset

Use the clean, already-built source commit
`6d1bca10bc67d02150a1a717f111891976e98069`, binary SHA
`afc233212a09a61625120c54d71e2f147f614f61a5ffd0d4140c274e5fb6a776`.
Its engine is `42cd156ac9f95ddf4311e88dd7ad462292d6d1d6`.
Set `BORG_CEMETERY_DIR` to a native-tools checkout matching that source's
`death-tools-pin.txt` (`1afd9423d7f8a1340eca9d74cff85443e769b1a9`) when the
current Cemetery native subtree differs. The source still enforces its byte
check. This does not need the separate draft caster-loader PR450.

```sh
# Routine smoke: two cases per class, about five seconds here.
python3 scripts/encounter_suite.py \
  --manifest synthetic/caster-encounters-v2/smoke-suite.json \
  --source /path/to/built-borg-reborn-rs --out /tmp/caster-smoke-001

# Full bank: all361 cases, about four minutes here.
python3 scripts/encounter_bank.py \
  --manifest synthetic/caster-encounters-v2/bank.json \
  --source /path/to/built-borg-reborn-rs --out /tmp/caster-bank-001
```

Always use a fresh output directory. Both tests load saved engine/RNG state and
start fresh private Borg memory. The core is fixed to reborn, with the pinned
profile. Each case has a1,000-engine-turn horizon and5-second wall limit.
The full-bank outcome was34 deaths and327 finite-horizon survivals. These
selected correlated encounters are not a survival-rate estimate or an
improvement comparison. No qualified near-death diagnostics are available.

To run just one class shard, use e.g. `all-mage-01.json` with
`encounter_suite.py`. [bank.json](bank.json) lists47 pinned class shards.
For an explicit alternative build with the same compatible engine, pass
`--target-commit FULL_SHA` to the bank runner and supply that built checkout.
Save, profile and engine semantics remain checked. Missing/failed shards stay
in the denominator, and every case in an unrun shard receives a `not_run` row.

For **borg.txt/errands configuration comparisons**, use
[the existing arm runner](../../studies/fast-caster-config/README.md) and select
one of these shard manifests in the study specification. It fixes borg-rs as
the controller that reads those files; it is separate from the reborn-core
baseline. Three configurations × eight starts is24 cells, within its32-cell
budget. Freeze every definition and input hash; run additional shards as
separate attempts. Native readback limits and finite-horizon interpretation
remain the same. A cross-controller result is not a one-knob comparison.

## How starts were selected

The reusable preparation tools are `harvest_encounters.py`,
`curate_encounters.py`, `expand_encounters.py` and `index_encounters.py`.
Preparation is outside routine test timing:

1. Execute the two prespecified16-cell harvest specs once, with100-tick private
   checkpoints and observable decision logs. Preserve every attempt and death.
2. Identify uninterrupted visibility episodes with recorded combat or targeting
   contact. For bulk discovery, contact must fall between the first visible
   think and ten engine ticks after the last. Town/unseen/poison terminal
   incidents also have separately curated observable-contact starts.
3. Select a checkpoint at/before first visibility/contact; deduplicate identical
   uncompressed engine saves across the bank. Keep family lineage, not an
   independent-life label. Monster kind association does not prove the terminal
   individual's identity. Postmortem poison is linked to observed poisoning
   contact; a hidden killer is never revealed to the playing Borg.
4. Check checkpoint/resource witnesses, retain observed equipment/inventory,
   and load every qualified start with the real Borg. Runtime checks cover
   source/build, engine, input/profile hashes, initial HP/SP, and declared
   initial gear kind/slot and inventory coverage. Older cases retain their
   existing resource checks and separate verified coverage receipts.

Two preparation ledgers retain25 resource-witness mismatches, duplicate starts
and38 contact-association exclusions. Earlier selection attempts also disclose
town eligibility, poison-attribution and HP-minimum association corrections.
A level-up can lower HP/maxHP without damage; such a life gets a labeled
surviving combat control rather than an invented near death. No new seeds were
rerolled to conceal failures. `bank-batch1.json` and its214-case run are
**preparation evidence**, superseded for encounter qualification by `bank.json`.
They preserve their original inputs/hashes; do not use the preparation bank as
the final Zoo registration.

Each bulk case has a saved start, profile, scenario, selected initial/onset
witnesses and contact evidence. Large panel/store fields are explicitly omitted
from reduced witnesses; original line and full-stream hashes remain available.
Natural key/state/message/trace streams, literal configurations, summaries,
process receipts, static knowledge and **all intermediate checkpoints** are
archived under `evidence/harvest*`. Checkpoints are losslessly stored in
per-life `checkpoints.tar.gz` with file-hash inventories; extracting and
ungzipping restores the original files. Full large observation streams remain
compressed in the original local harvest directories; they are **not published
in Git**. Their retention receipts state that limit; selected witness fields
and hashes are published here. The source/build/game-data recipe permits
regeneration, and death reproduction is separately verified.

`evidence/trials/` retains all full/smoke/preparation trial receipts and compressed
key/state/message streams. Sixty native restart-death packets across those
attempts are retained under `evidence/restart-deaths/`. Their explicit
[restart lineage](evidence/restart-lineage.json) connects each packet to its
source life; generic native starting-condition counts never turn these branches
into new natural lives. [Validation summary](evidence/validation-summary.json)
contains exact timings and repeated-stream checks.

To grow further, discover/materialize another bounded harvest and combine its
ready scenario references with `all-cases.json`, preserving exclusions. Then:

```sh
python3 scripts/index_encounters.py \
  --cases /path/in/this/repository/to/combined-cases.json \
  --template synthetic/fast-caster-encounters/suite.json \
  --out synthetic/my-next-caster-index
```

The indexer writes fresh class shards, a bank manifest, coverage and an eight-case
resource-varied smoke suite when coverage permits. A bank is bounded at512
cases/64 shards; individual suite and configuration-cell limits stay small.

## Cemetery and Zoo

Cemetery owns the authoritative bank, saves, provenance, continuation evidence
and immutable input pins. Zoo owns execution orchestration, aggregate
comparisons and presentation. Register the **final bank.json** or its pinned
shards through the saved-state extension tracked in
[Zoo #144](https://github.com/diegoami/borg-zoo/issues/144). Zoo's reviewed
PR145 generated-birth/target-build contract remains separate. Its proposed
publication paths are `scenario-experiments/`, results-branch
`scenario-results/EXPERIMENT/RUN-ATTEMPT`, and `/scenarios/`. Zoo code has not been
changed here and no large Zoo experiment has been dispatched.
