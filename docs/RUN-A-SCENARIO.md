# Run one saved scenario with a specific Borg

Cemetery owns the saves, native runners, exact configuration inputs and
reproduction evidence. Zoo owns scheduling, aggregate comparisons and the
[Scenarios dashboard](https://diegoami.github.io/borg-zoo/scenarios/index.html).
A case page in that dashboard links here and gives its exact scenario ID.

This example runs the level1 Druid case `c2-r2-s1020000-i000` with the exact
Zoo speed30 setup. It is one of the paired smoke's six rescued cases: the reborn
baseline died, while the speed30 setup survived the2000-engine-turn horizon.
This compares the complete setups; it does not isolate the speed setting.

## 1. Get the bank and this runner

```sh
git clone --branch evidence/paired-smoke-validation https://github.com/diegoami/borg-cemetery.git
cd borg-cemetery
git rev-parse HEAD  # retain this Cemetery runner/evidence revision with your result
tar -xzf synthetic/balanced-999-incidents/bank-43979480269.tgz
```

The archive is the original999-case bank, with111 starts per class. Its SHA256
is `186066b039ccc8451642cbcbd77e714c6615c20d99d0de4b18963289c5748cbf`;
`synthetic/balanced-999-incidents/bank-artifact.json` records its source.
Extraction creates `synthetic/balanced-999-incidents/generated/` with the
individual saves and125 small suite manifests. The example is in `shards/000.json`.
The runner hash-checks the save and scenario before loading a private copy.

## 2. Restore the Borg build once

For the exact original cloud binary, use the paired run's build artifact:

```sh
git clone https://github.com/diegoami/borg-reborn-rs.git ../borg-speed30
git -C ../borg-speed30 checkout 193d9076747cd5c52e1fe1f6ea314570d8f3873a
git clone https://github.com/diegoami/borg-cemetery.git ../tools-speed30
git -C ../tools-speed30 checkout 09225018dd5f2d4336a16b29478793d902c70dc3
gh run download 44046247609 -R diegoami/borg-zoo --name paired-build-speed30 --dir /tmp/borg-speed30-build
tar -C ../borg-speed30 -xzf /tmp/borg-speed30-build/build-speed30.tgz
```

Build artifacts have90-day retention. If unavailable, rebuild that exact source
once (a rebuilt binary has its own binary hash):

```sh
cd ../borg-speed30
BORG_CEMETERY_DIR="$(realpath ../tools-speed30)" BORG_IMPL=rust \
  flock /tmp/angband-validation.lock harness/build.sh
cd ../borg-cemetery
```

The game's engine must match the saved bank's engine pin. The native death tools
must match the selected source's `death-tools-pin.txt`; different Borg source
revisions can require different tool revisions. The CLI checks both identities.
For a rebuild, retain the compiler/toolchain and BUILD_ID, and compare actual
outcome/streams before claiming byte-identical reproduction.

## 3. Run exactly one scenario

From the Cemetery checkout:

```sh
python3 scripts/single_encounter.py \
  --suite synthetic/balanced-999-incidents/generated/shards/000.json \
  --case c2-r2-s1020000-i000 \
  --source ../borg-speed30 \
  --source-commit 193d9076747cd5c52e1fe1f6ea314570d8f3873a \
  --core borg-rs \
  --native-tools ../tools-speed30 \
  --borg-txt studies/balanced999-speed30/borg.txt \
  --errands-plan studies/balanced999-speed30/errands_plan.txt \
  --out /tmp/druid-speed30-example
```

The two supplied files are the complete original Zoo bundle and literal
errands file, not just the speed parameter. They include the healing, shopping,
trip and class attack preferences; attack speed fight danger tenths is30.
The adapter normalizes race/class for the chosen save, forces cheat death off,
and selects the borg-rs controller. Its private `selected-plan.txt` is checked
against the exact requested errands-file SHA. Named parameters are checked
against native `params-core.json`, including their `borg.txt` origin.
Classic settings without native readback remain input-file verified.

The example uses fresh Borg memory and the save's engine RNG. It begins at the
curated encounter onset, rather than replaying the original life from birth or
starting on its final desperate action. Bounds come from the suite:2000 engine
turns,5 native wall seconds, exact turn boundary. The compiled build is reused;
no full-game birth harvest or recording is needed. The runner takes the shared
validation lock internally; do not wrap it in another lock.

## Run the same case with the baseline or another Borg

For the reborn baseline, restore source
`6d1bca10bc67d02150a1a717f111891976e98069`, artifact
`paired-build-baseline` from the same Zoo run, and native tools
`1afd9423d7f8a1340eca9d74cff85443e769b1a9`. Then:

```sh
python3 scripts/single_encounter.py \
  --suite synthetic/balanced-999-incidents/generated/shards/000.json \
  --case c2-r2-s1020000-i000 \
  --source ../borg-baseline \
  --source-commit 6d1bca10bc67d02150a1a717f111891976e98069 \
  --core reborn --native-tools ../tools-baseline \
  --out /tmp/druid-baseline-example
```

The baseline uses the saved scenario's numeric reborn profile. An explicit
`--profile FILE` selects a different reborn profile. `borg.txt`/errands settings
belong to the borg-rs controller, which is selected with `--core borg-rs`.
For a different build, change `--source`, `--source-commit`, its required native
tools and the appropriate configuration files. Keep the same save/suite/horizon
for a paired comparison. Unsupported parameters, incompatible engines and
incorrect source/tool pins are failures, never silent fallbacks.

Choose a new output directory for each attempt. For another case, find its
manifest in `generated/all-cases.json` and the125 shard files, or copy the
case-specific command from its Zoo dashboard page. The common speed30 template
can be used for any class: the adapter fixes birth race/class to that save.

## Read and compare the output

- `single-encounter.json`: requested Borg/core/configuration, trial identity and
  original key/state/message SHA256 values.
- `trial.json`: native outcome, exact build/binary, loaded state, process receipt
  and requested horizon. Death, survival to horizon and stopped are distinct.
- `run/summary.json`: observed endpoint; `run/state.log` starts with loaded
  resources and pack/equipment/rune hashes.
- `run/config.txt`, `run/params-core.json`, `run/configuration.json` and
  `run/errands_plan.txt`: configuration and loaded-plan evidence for borg-rs.
  The reborn core writes `run/params.json` instead.
- `native-deaths/`: every actual death's native dossier. Repeated or alternative
  continuations stay linked to their original life; they are not independent
  population samples.

The command above was actually tested with the original cloud binary. It
matched the Zoo outcome and both key and state streams byte for byte. The raw
message stream differs only in one Plan diagnostic containing the absolute
output path; normalizing that run-root path makes the messages equal. Original
hashes are preserved, not rewritten. See
`validation/borg-zoo/balanced999/single-scenario-example/verification.json`.
A message hash difference after moving directories is not automatically a
change in game play; inspect the difference. Exact reproduction claims must
state which streams matched and any normalization used.

The paired smoke's two cloud executions matched all108 key/state/message
streams with identical cloud paths, demonstrating that the corrected adapter
changed evidence handling rather than play. Its native archives and recovered
first-run death dossiers are in `validation/borg-zoo/balanced999/`.
