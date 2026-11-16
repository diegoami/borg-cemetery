# Stair-livelock incident and bounded fix validation (#421)

The original Half-Elf Warrior reproduction matches the reported key hash `5d6b065592fb935e42697e0cbd48a6a40e5b43de152d01dc7e1378aa6ef22d6b`: 79,397 keys, 22 turns with at least1,000 keys, peak7,196 at turn62,632. It used the preserved71978c7b recorder-off executable whose game policy equals accepted8a0b57c8. Its source identity remains1573e6ca; it is not relabelled as an8a build.

The trace shows a dungeon-only `loop-levels3 9` arriving on DL1, refusing DL2 because the native preparedness check fails, going immediately to town and restarting targetDL3. Repeated connected stair transitions can consume many keys at one global game turn. `shell::walk` both redirected the loop home and issued an upstairs action.

The candidate changes only the readiness-refusal path of loops with both endpoints above town: keep the waypoint, clear the obsolete flow and defer this descent to native play on the current level. It does not force descent or alter engine energy/time, native preparedness, retreat or town-ended/one-shot behavior. No new retry/timeout threshold or policy parameter.

The synchronized baseline includes accepted main4ecb93d7 and the existing neutral-default preference implementation from track-p0edee14b. Its source5ac02350 and candidate sourced012f3af differ in runtime inputs only in shell.rs. The Half-Troll Rogue still reproduces the reported two bursts (peak1,098) on that baseline. Candidate peak248, zero threshold bursts. A constructed fresh-birth positive interval gives a short causal regression: baseline peak1,409 at turn2,092; candidate peak39. The test fails on the preserved baseline binary and passes on the candidate.

Current-baseline Warrior and Half-Orc trials already have zero threshold bursts after other independently accepted fixes. Their new results are safety/regression checks, not a claimed reduction from an active current-baseline stall. Both Warrior trip-policy variants match each other on the candidate. No survival or population claim.

All source/build/command/config identities, summaries and raw-file hashes are in `validation.json`. Raw logs/executables remain outside Git at the recorded paths. Initial library-path failure and misselected-race controls are preserved and explicitly excluded from reported-character reproduction claims. No completed development trial died; CI natural deaths are retained separately in the canonical native-control registry.

| Raw directory | Source | Actual race/class | Keys | Peak keys/turn | Turns≥1000 | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| p421-baseline-half-orc | 5ac02350 | Half-Orc Rogue | 14628 | 183 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-baseline-half-troll | 5ac02350 | Human Rogue | 15567 | 93 | 0 | Additional control with a race different from the reported incident; not counted as reproduction of that reported character. |
| p421-baseline-rogue-orc | 5ac02350 | Elf Rogue | 18044 | 76 | 0 | Additional control with a race different from the reported incident; not counted as reproduction of that reported character. |
| p421-baseline-rogue-troll | 5ac02350 | Gnome Rogue | 16482 | 85 | 0 | Additional control with a race different from the reported incident; not counted as reproduction of that reported character. |
| p421-baseline-troll-verified | 5ac02350 | Half-Troll Rogue | 21836 | 1098 | 2 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-baseline-warrior | 5ac02350 | Half-Elf Warrior | 11714 | 39 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-candidate-constructed | d012f3af | Half-Elf Warrior | 727 | 39 | 0 | Constructed positive-loop regression; not the shipped ambitious schedule. |
| p421-candidate-orc | d012f3af | Half-Orc Rogue | 13602 | 93 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-candidate-troll | d012f3af | Half-Troll Rogue | 16758 | 248 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-candidate-warrior | d012f3af | Half-Elf Warrior | 15618 | 183 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-candidate-warrior-trip | d012f3af | Half-Elf Warrior | 15618 | 183 | 0 | Reported-seed/settings trial, qualified by exact source epoch. |
| p421-constructed-baseline | 5ac02350 | Half-Elf Warrior | 2878 | 1409 | 1 | Constructed positive-loop regression; not the shipped ambitious schedule. |
| p421-original-repro | 1573e6ca | no gameplay | — | — | — | configuration failure |
| p421-original-repro2 | 1573e6ca | Half-Elf Warrior | 79397 | 7196 | 22 | Reported-seed/settings trial, qualified by exact source epoch. |
