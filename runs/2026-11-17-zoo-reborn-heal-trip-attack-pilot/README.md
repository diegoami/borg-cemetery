# Zoo pilot: the two deaths of the bundle with `errands_plan.txt`

Natural deaths from borg-zoo's [`reborn-heal-trip-attack-pilot`](https://github.com/diegoami/borg-zoo/actions/runs/43973026635)
(borg-zoo#164, run 43973026635), arm `reborn-heal1-trip1-attack1-plan`: 2 deaths in 18 games on `classes-18`.
Report with the 72-cell table: borg-zoo `reports/reborn-heal-trip-attack-pilot-deaths`.

## Provenance

- **Source:** borg-reborn-rs `f02cd2940a7439a8965b3883270a9a73df7e0bf5`, source-hash rust `bb27c7c3740aacdd…`, zoo specimen `4.2.6-reborn-rust-heal`.
- **The arm ("the bundle"):** `borg_reborn_core = borg-rs`, `borg_reborn_errand = none`, `borg_town_plan = 1`,
  `borg_trip_policy = 1` (`unknown_stacks` 5, `pack_slack` 1), `borg_param_caution_heal_when_outmatched = 1`,
  the 15 class `borg_param_attack_preference_*_permille` values of the owner's preferences, and `borg_plan = errands_plan.txt`.
  Each dossier's `config.txt` lists them and the written `borg.txt` hash (`03e46521…`).
- **Replay:** replayed locally through the zoo adapter with evidence kept; both replays' `keys.log` SHA-256 equal the CI run's
  `play_sha256`. CI used binary `6abfdf38…`, the local build of the same source is `9728702e…`.
  Raw `keys.log`, `messages.log` and `state.log` are not committed; their hashes are in each `record.json`.
- **Saved with** borg-zoo `tools/save-deaths.py`.

## What the two replays show (observations, not a diagnosis)

| start | killed by | level, depth | `# Healing (outmatched).` | notes |
|---|---|---|---|---|
| seed 888896726, Half-Elf Blackguard | giant white mouse | CL4, DL1, turn 57520, 2183 keys | 0 | HP between 0 and 5 of 41 for the last ~800 game turns while mice kept biting; both Cure Light Wounds potions were used earlier (turns 54684 and 55810); 1,722 "Fleeing" notes |
| seed 934061548, Half-Elf Druid | crow | CL2, DL1, turn 27401, 3861 keys | 0 | two Cure Light Wounds potions and the last Phase Door scroll used in the final ~60 game turns; 19 max HP, bitten 4 times between turns 27396 and 27401 |

- The heal flag was on in both arms and never fired. Whether the cure potions were used by the older logic or the flag should have fired is a question for the borg-reborn-rs owner; this page does not claim a cause.
- Both starts die identically (same keys, same turn) in all four arms of the pilot, control included, so neither death is caused by, or rescued by, the bundle or the plan.
