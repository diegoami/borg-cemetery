# D0007 — proposed bounded parameter arms

These are frozen diagnostic profiles for **one saved starting condition**,
S0003 at engine turn 3402. They are not tuned defaults or independent births.
Use the original reborn source `e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71`,
its validated executable and the same saved RNG in every arm.

| Arm | One changed value | Question |
| --- | --- | --- |
| control | None | Does the unchanged control reproduce the retained death? |
| horizon-2 | threat horizon 1 → 2 player turns | Does earlier pursuer awareness change recovery/contact? |
| horizon-3 | threat horizon 1 → 3 | Does a longer horizon improve the sequence or over-constrain it? |
| risk-75 | risk aversion 50 → 75 | Does a more pessimistic damage estimate help, or favor aggressive threat-removal credit? |
| rest-1 | requested rest 75 → 1 player turns | Does short rest change repeated interruption? It also changes Recover's goal budget. |

All other values are written explicitly from the actual captured parameter
table, rather than relying on newer defaults. After each run, compare the
written effective parameters and require exactly the named difference.

## Current execution status

**Completed after the native lane became free.** All five arms were run. The
control reproduced death at 3640; horizon 2 survived the 4402 cap, horizon 3 died
at 3650, risk aversion 75 reproduced the death, and rest duration 1 survived
with a refused-action violation. [Read all outcomes and qualifications](../analysis-results/README.md).
No default setting was changed and no population benefit is claimed.

## Reproduce when the native lane is free

From the cemetery checkout, with the original source built in ORIGINAL:

```bash
flock -n /tmp/angband-validation.lock python3 scripts/run_scenario.py run \
  --source ORIGINAL --scenario scenarios/S0003 --profile deaths/D0007/analysis-profiles/control.txt \
  --turns 1000 --wall-seconds 30 --out /tmp/D0007-analysis-control
flock -n /tmp/angband-validation.lock python3 scripts/run_scenario.py run \
  --source ORIGINAL --scenario scenarios/S0003 --profile deaths/D0007/analysis-profiles/horizon-2.txt \
  --turns 1000 --wall-seconds 30 --out /tmp/D0007-analysis-horizon2
```

Use new directories, repeat for the other profiles, and retain all outcomes.
The requested cap is turn 4402; the legacy frontend can stop at its next
boundary. Compare alive-at-cap/dead/stopped/timeout separately, with the final
turn, HP, progression, healing/escape use and action sequence. Confirm the
unchanged control before interpreting any candidate. A longer life ending in
death is not a rescue. Do not pick only the best outcome and call it a policy.

A loaded save starts fresh Borg memory. The original live Engage goal is an
important separate hypothesis and needs original-prefix or private-state
fixture tests; these saved-position arms do not isolate that historical goal.
