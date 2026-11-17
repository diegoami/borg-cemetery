# Fast caster encounter suite

Four curated encounter starts, **already-built Borg, no birth replay or build in
the timed test**. Three runs on accepted main took **2.20, 2.23 and 2.39 seconds**
for the entire suite. All four loaded successfully and died in each attempt;
all12 key/state/message stream hashes match across the repeated main runs.
These are current failure/regression cases, not a survival improvement claim.

```sh
python3 scripts/encounter_suite.py \
  --manifest synthetic/fast-caster-encounters/suite.json \
  --source /path/to/built-borg-reborn-rs \
  --out /tmp/fast-caster-attempt-001
```

The baseline source is accepted main `6d1bca10bc67d02150a1a717f111891976e98069`
(reborn #444). It does not depend on the separate caster-loader PR #450. Checkout and build it once before testing. The source's native death
export tools must match its `death-tools-pin.txt`; preserve an explicit
`BORG_CEMETERY_DIR` pointing at that pin (for this source, `1afd9423`) if your
Cemetery checkout has newer native code. A separate pinned tools worktree is
sufficient. The source enforces its byte check; no verification is bypassed.
Always choose a fresh output directory.

Each case has a 1,000-engine-turn horizon (roughly 100 normal-speed player turns)
and a 5-second wall limit. Actual cases end after 45–605 engine turns; the
reported 2.2–2.4 seconds includes loading, identity checks and receipt writing.
The wall limit is per case, not a promise that every machine finishes in 2.5s.
Failures, timeouts and missing evidence stay in the denominator. The runner
clears inherited tuning/recording variables, uses the pinned profile with the
reborn core, checks saved-state hashes, engine compatibility and actual starting
HP/SP, and writes machine outcomes and stream hashes after each case.

## Where play starts

| Case | Start turn | First encounter observation | Lead | Initial HP / SP | Original death turn |
|---|---:|---:|---:|---|---:|
| Dunadan Druid / invisible contact, seed 202 | 7605 | 7608, first “Something touches you” | 3 | 13/13 HP, 2/2 SP | 7818 |
| Elf Mage / Fang, seed 102 | 3402 | 3442, first visible Fang | 40 | 9/9 HP, 2/2 SP | 3640 |
| Human Druid / small kobold, seed 1020 | 602 | 602, first visible killer kind | 0 | 12/12 HP, 2/2 SP | 1207 |
| Elf Mage / cave spider, seed 1011 | 18803 | 18823, first Borg sighting of that spider | 20 | 7/10 HP, 0/4 SP | 18903 |

These starts are selected from encounter onset, not a last-HP threshold or the
final action. The invisible enemy cannot supply a visible-appearance trigger;
its first observable attack is used. Fang is unique. The kobold record does not
prove terminal individual identity, so its selection explicitly says first
visible **kind**, not a known individual. The spider's original Borg log names
monster index 50. Selection basis, source observation/message digest and lead
are recorded per scenario. No hidden monster is revealed to the playing Borg.

Checkpoint preparation is separate, one-time work: reproduce each original run
from its exact seed/build/configuration, enable read-only private-engine
checkpoints and observations, confirm all three original streams match, select
the checkpoint at/before the trigger, then gzip/hash it. The four small saved
states are retained in this bank. Routine suite runs load them directly.
Recording streams are unnecessary.

## What the results mean

These are **fresh-Borg counterfactuals from saved engine state**. Saved engine
RNG is preserved; private Borg memory is not. The first three original deaths
used the reborn core. The spider's original source run used borg-rs; this suite
explicitly uses reborn for all four. Do not infer controller equivalence or
attribute the spider's changed endpoint to one variable. Accepted-main results are in `evidence/main-attempt-{1,2}/` and `main-final/`;
preparation results on source `aae2c194` remain in `evidence/attempt-{1,2,3}/`
with their original manifest in `evidence/preparation-suite.json`. On these targets: the first three die at original death turns,
while the spider trial dies at 18848. No exact original suffix claim is made.
Repeated executions of one condition do not create independent lives.

Birth reproduction is a separate check, not part of the fast suite:
[death reproduction recipes](../../validation/borg-reborn-rs/caster-build-v2/reproduction/). That bank contains four runnable seed/build/config
recipes and successful death/three-stream verification receipts. All natural
deaths are collected regardless of level/class; level-2 build capture was only
a schema-validation diagnostic, not eligibility for death capture or scenarios.
The Druid also has an observed level-1 build record.

Loaded trial deaths are retained separately under
`validation/borg-reborn-rs/fast-encounter-trials/`, with explicit parent-death
lineage and `independent_life: false`. They never inflate natural population
counts. Older descriptions or missing state do not become replayable just
because they are indexed.

For another exact source commit with the same pinned engine and qualified save
format, provide `--target-commit FULL_SHA` and that clean, built checkout. The
starting saves/profile remain identical. Zoo orchestration and paired pushid
reporting are tracked in borg-zoo #144; this runner does not make population
claims or launch large experiments.

## More cases and configuration comparisons

The original four-case `suite.json` remains frozen. `expanded-suite.json` adds
four surviving encounter controls, making **eight cases, two per caster class**.
Two real runs completed 8/8 valid in **6.19 and 5.17 seconds**. Class subsets are
`mage-suite.json`, `druid-suite.json`, `priest-suite.json` and
`necromancer-suite.json`. Priest/Necromancer subsets use 500-engine-turn horizons
and ran in **1.12 / 1.29 seconds**; Mage/Druid retain the 1,000-turn baseline.

The expansion prespecified Human/Hobbit Priest seeds 203/204 and Elf/Half-Orc
Necromancer seeds 203/204. All four survived the 20,000-turn natural harvest;
all attempts are retained in `evidence/expansion-harvest.json`. Their observed
minimum HP fractions were approximately 43%, 30%, 73% and 42%. These are
**surviving controls, not qualified near deaths**. Starts precede the latest
continuous encounter with the attacker before the observed HP minimum. Each
case has observation/contact witnesses and a parent encounter-family identity;
none invents a parent death or an independent life for a restart.

For varying literal `borg.txt` values or errands plans with one fixed build,
use the [configuration comparison instructions](../../studies/fast-caster-config/README.md).
The supplied three-arm, two-case example takes about four seconds and produces
paired Markdown/JSON reports. `plan-suite.json` includes a town-departure start
so plan tests are not limited to immediate combat.
