# Compare borg.txt and errands files

Run identical saved starts with several **configuration arms**, as Zoo does
with experiment cells. Build the Borg once; no birth replay/build is in the
comparison loop. This adapter fixes the controller to **borg-rs** (the controller
that consumes these files), the source commit, engine, saves and run horizon.
It is separate from the four-case reborn-core failure baseline.

From the Cemetery checkout containing this change:

```sh
python3 scripts/compare_encounters.py freeze \
  --spec studies/fast-caster-config/study.json \
  --out /tmp/my-config-definition.json
python3 scripts/compare_encounters.py run \
  --definition /tmp/my-config-definition.json \
  --source /path/to/built-borg-reborn-rs \
  --out /tmp/my-config-comparison
cat /tmp/my-config-comparison/comparison.md
```

Use a fresh definition and output path for each attempt. The example pins
`6d1bca10bc67d02150a1a717f111891976e98069`; the source checkout and its clean build
must match. As in [the suite setup](../../synthetic/fast-caster-encounters/README.md),
set `BORG_CEMETERY_DIR` to a separate checkout whose native tools match the
source's `death-tools-pin.txt` when necessary. No rebuild is performed by the
runner. Standard Python is sufficient for the comparison scripts.

Copy `study.json` and edit its repository-relative input paths. Each arm names a
literal `borg_txt` file and an optional `errands_plan`. Freeze computes all input
hashes, including the suite and saved-start references. Editing a frozen input
causes refusal; freeze a new definition after changing it. There are 2–4 arms,
up to 8 scenarios and at most 32 cells. Set `suite` to `expanded-suite.json`, a
class subset or your own qualified manifest. Edit `source_commit` before
freezing to test another built commit with the same compatible engine; changing
both source and configuration is a separate experiment, not this single-axis
comparison.

The supplied example isolates two hypotheses:

| Arm | borg_param_caution_clw_min_loss | Errands depth cap |
|---|---:|---:|
| base | 30 | 1 |
| earlier-heal | 10 | 1 |
| deeper-plan | 30 | 2 |

These are illustrative settings, not tuning recommendations. Both starts are
low-level casters: a Priest departing town and a Mage approaching Fang. The town
case gives the plan a chance to act; a brief combat-only case usually says
little about an errands policy. Each cell has a 500-engine-turn horizon and
5-second wall limit. Longer-term errands evaluation needs appropriate starts
and horizons, not an inference from one encounter.

Two actual runs completed **6 cells in 3.59 and 3.71 seconds**. All six survived
the horizon in each run; there is **no demonstrated survival improvement**.
Native readback confirmed the requested named healing parameter (30 versus 10,
origin `borg.txt`) and the loaded errands file's exact hash. The archived
[definition](evidence/definition.json), [first report](evidence/attempt-1/comparison.md)
and [repeat report](evidence/attempt-2/comparison.md) include receipts and streams.

Outputs include `comparison.md`, machine-readable `comparison.json`, and each
cell's `trial.json`, private applied `borg.txt`, native parameter receipt, loaded
plan, process/build identity and key/state/message streams. Reports show paired
survival outcomes, ending HP/depth and elapsed engine turns. Deaths, timeouts,
invalid receipts, missing cells and early stops remain visible. A rescue means
survival to this horizon only. Recollect after an interrupted attempt with:

```sh
python3 scripts/compare_encounters.py collect \
  --definition /tmp/my-config-definition.json --out /tmp/my-config-comparison
```

Every cell starts a fresh Borg from the same saved engine/RNG state. Private
Borg memory is not restored. Race/class and core are fixed; cheat death and
winner respawn are disabled. Ambient BORG/ANGBAND overrides are cleared. Each
arm gets a private user directory and plan copy. Source/build/input consistency
is checked before running; collection rechecks cell/trial/raw receipts and
rejects copied or stale cells. These checks are not cryptographic signatures.

**Verification limit:** named `borg_param_*` values have native effective-value
readback, and plans have a native loaded-file receipt. Other classic `borg_*`
flags currently have input-file evidence only on this Rust core. You may vary
them, but affected pairs are labeled `unverified_configuration`, never a proved
rescue. The normalized race/class/core/cheat fields cannot be experiment knobs.
A loaded plan receipt also does not prove every branch was exercised.

Cemetery owns the canonical saves and continuation evidence. Zoo owns aggregate
reports/presentation. Its existing [scenario integration PR](https://github.com/diegoami/borg-zoo/pull/145)
currently qualifies generated birth scenarios and the target-build axis;
saved-state and configuration-axis ingestion require an explicit extension
tracked in [Zoo #144](https://github.com/diegoami/borg-zoo/issues/144). The agreed
placement follows Zoo's proposal: definitions in `scenario-experiments/`, compact
run snapshots under `scenario-results/EXPERIMENT/RUN-ATTEMPT` on its results
branch, discovery at `/scenarios/`, with canonical input references here.
