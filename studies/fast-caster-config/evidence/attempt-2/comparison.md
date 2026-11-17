# fast-caster-config-smoke

Same saved engine/RNG starts; fresh Borg per arm. No population claim.

| Scenario | Baseline | Candidate | Baseline result | Candidate result | Comparison |
|---|---|---|---|---|---|
| town-departure-priest-human-203 | base | earlier-heal | survived_horizon | survived_horizon | both_survived |
| mage-fang-102 | base | earlier-heal | survived_horizon | survived_horizon | both_survived |
| town-departure-priest-human-203 | base | deeper-plan | survived_horizon | survived_horizon | both_survived |
| mage-fang-102 | base | deeper-plan | survived_horizon | survived_horizon | both_survived |

Survival means alive at the finite horizon, not an eventual win. Loaded plan identity does not prove every plan branch was exercised.

| Scenario | Arm | End HP | End depth | Max depth | Engine turns elapsed |
|---|---|---:|---:|---:|---:|
| town-departure-priest-human-203 | base | 12 | 0 | 1 | 500 |
| mage-fang-102 | base | 9 | 0 | 1 | 509 |
| town-departure-priest-human-203 | earlier-heal | 12 | 0 | 1 | 500 |
| mage-fang-102 | earlier-heal | 9 | 0 | 1 | 509 |
| town-departure-priest-human-203 | deeper-plan | 12 | 0 | 1 | 500 |
| mage-fang-102 | deeper-plan | 9 | 0 | 1 | 509 |
