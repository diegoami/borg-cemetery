# Exploratory class-preference profiles

Owner-requested bounded local smoke of the main-promoted native preference
implementation. These are trial hypotheses, not calibrated class advice or new
defaults. One open full-suite seed per class, paired neutral/profile runs, exact
100,000 engine-turn cap, same executable and birth settings. No population or
survival-improvement claim can follow from one paired seed per class.

## Edit the configuration

Each file in `profiles/` is an ordinary borg-zoo profile object with `description`
and `settings`. The test reads these files; weights are not embedded in the
runner. Copy an object under a named key in a Zoo catalogue's `profiles` map to
use the same settings there. For ordinary native play, its settings are the
same `name = integer` lines in `ANGBAND_DIR_USER/borg.txt`.

All omitted attack-family settings default to1000. The starting hypotheses are:

| Class | Non-neutral settings |
| --- | --- |
| Warrior | melee2000, spell800 |
| Mage | spell2000 |
| Druid | spell2000 |
| Priest | spell1700 |
| Necromancer | spell2000 |
| Paladin | melee1800, spell1200 |
| Rogue | melee2000, projectile1200 |
| Ranger | projectile2000 |
| Blackguard | spell2000 |

Warrior spell800 is inert because that class has no spells. Weapon spells remain
spells; arrow activations remain activations. Control/emergency actions retain
their invocation family, and waiting stays fixed at1000. These semantics matter
when interpreting results; do not infer that class fantasy determines an optimum.

## Run

```sh
python3 run.py --source /path/to/borg-reborn-rs \
  --zoo /path/to/pinned-borg-zoo --output /new/private/run-directory --jobs 2
```

The immutable binary/source identities in `plan.json` select the exact validated
runtime promoted through source PR407. The actual executable was built at8e007cdd;
its input hash is identical to main4a2cb910. It is not relabeled as a new build.
The runner uses the pinned Zoo configuration writer/command builder and the
source supervisor, then preserves logs and exports every natural death through
the pinned Cemetery tools. It retains the effective file-origin parameter table,
command, profile bytes/hash, source/build identities, process receipt and all
attempts. It never edits the source's harness/borg.txt or production defaults.

Both arms use tracing. Per-invocation analysis checks the arithmetic and winner,
and counts boosted winners that differ from the raw best in that same state.
Those are local ranking counterfactuals, not matched full-game continuations:
after different actions, the neutral and configured games can diverge.

Each run must verify the full effective parameter table: only the configured
weights may differ from defaults, with origin `borg.txt`. Crashes, timeouts and
validation failures remain explicit. Re-runs are repeats, not new independent
samples. Raw large logs and binaries stay outside Git; report/receipts and
source-qualified death packages are retained here.
