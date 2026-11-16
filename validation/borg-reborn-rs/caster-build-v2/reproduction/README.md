# Reproduce the natural deaths from birth

All four new natural deaths have a frozen recipe, literal Borg/profile inputs,
source/binary/game-data identities, expected endpoint and all three expected
stream hashes. **All four have been reproduced** with the original binary:
seed 202 Druid, seed 102 Elf Mage, seed 1011 vendored-core Elf Mage, and seed 1020
Human Druid. `*/verified.json` contains each successful receipt. No recording is
required. No class/level gate controls collection; early deaths are included.

Example:

```sh
python3 scripts/reproduce_native_death.py \
  --recipe validation/borg-reborn-rs/caster-build-v2/reproduction/druid-seed202/recipe.json \
  --source /path/to/clean-source-at-aae2c194 \
  --out /tmp/reproduce-druid-202-attempt-001
```

The source checkout must be exactly `aae2c194a18b9ff943e94aa97a60214f2a231dc2`;
build it once using that source's toolchain and harness. Recipes check the source
inputs, build receipt, actual executable and game data before execution. A
cached original executable is retained locally with all game data under
`/workspace/work/caster-natural-validation/runtime/`; this is workspace retention,
not a claim of a remotely published binary. Repository pins and file hashes
allow checking a rebuilt runtime. Another compiler may change the executable;
`--allow-rebuilt-binary` explicitly qualifies such a rerun and still requires
exact source/game inputs and matching endpoint/streams. It never relabels the
new binary as the original.

Set `BORG_CEMETERY_DIR` to the source's pinned native tools checkout if this
Cemetery revision has newer native code. The source's byte verification remains
active. Output must be fresh. Failed reruns retain their receipts and raw logs;
only a matching death endpoint, effective settings and key/state/message hashes
gets `reproduced`. Optional diagnostic level capture is omitted from reruns;
its read-only behavior is separately verified against capture-off controls.
The original smoke output had an incomplete suite publication, so its literal
inputs were materialized from a repeat with all three original streams matched.

This slower birth check establishes provenance. Routine regression testing uses
[the fast encounter suite](../../../../synthetic/fast-caster-encounters/README.md),
which loads the curated onset saves and finishes all four cases in about 2.5s.
