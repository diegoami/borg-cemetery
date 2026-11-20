# Named local cases: before and after

Selected regression checks only. These seven starts are not a population measurement.
Every game uses borg-rs, the shipped profile plus the stated switch overrides, and a 100,000-engine-turn cap.
Population measurement is [borg-zoo #511](https://github.com/diegoami/borg-zoo/issues/511); its initial pilot used 78b8f297 and found no survival-leading arm. The corrected specimen remains unmeasured.

| Seed | Shipped control | Categories 1 | Winning 1 | Recall 1 | All three 1 |
| --- | --- | --- | --- | --- | --- |
| 425904011 | a wild cat @ 3660 | alive 100k; CL5 | alive 100k; CL6 | alive 100k; CL5 | alive 100k; CL5 |
| 2095979189 | a wild cat @ 3345 | alive 100k; CL7 | alive 100k; CL5 | a wild cat @ 3345 | alive 100k; CL6 |
| 1976035382 | a wild cat @ 4248 | Grip, Farmer Maggot's Dog @ 4284 | alive 100k; CL7 | alive 100k; CL6 | a large white snake @ 17873 |
| 2049259432 | Fang, Farmer Maggot's Dog @ 4429 | Fang, Farmer Maggot's Dog @ 4429 | alive 100k; CL5 | Fang, Farmer Maggot's Dog @ 4454 | alive 100k; CL6 |
| 807683971 | a black naga @ 1534 | a black naga @ 1534 | a black naga @ 1534 | alive 100k; CL6 | alive 100k; CL6 |
| 1517990203 | a small kobold @ 6338 | alive 100k; CL6 | a rock lizard @ 6299 | a small kobold @ 6338 | alive 100k; CL5 |
| 390305857 | alive 100k; CL6 | alive 100k; CL7 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL6 |

The six Ranger controls reproduce their old deaths. Rogue 390305857 survives in the shipped control;
its reported crow death came from PR #757 flight-on. Its rows are behavior checks, not a rescue claim.
A changed life can diverge before its original killer appears; survival alone does not prove a specific encounter rescue.

## Mechanism checks

- Earlier category version 2095979189: the wild cat is the first priority target at 3309, fired on again at 3319; it is killed instead of sustaining the old cure/flight loop.
- Earlier category version 1976035382: the cat is targeted at 4194/4204; the life later dies to Grip. The table retains that death rather than calling it a 100k rescue.
- Seed 425904011 changes earlier actions and never meets the original cat in its active category/winning runs. Its original finishing state is checked separately in the non-acting diagnostic below.
- Winning 1517990203: the estimate becomes not-winning with two attackers at 6245 (5.315 turns, 5.544 incoming, 10 HP); ordinary flight/cures resume. It later dies to a rock lizard. This is not a retained winning commitment at death.
- Recall 425904011: the read at 3650 is refused (223.70 forecast damage over 34 ticks, 7 HP); the life survives the cap.
- Recall 807683971: the initial awake-only guard allowed the read at 1390 because the naga was asleep; it woke and killed the Borg at 1534. Owner 2026-11-20 explicitly chose to include possible wake-up. The final guard refuses that read (155.61 exposure against 15 HP), and Recall-only now survives 100k at CL6. Forecasting uses an awake copy of observed knowledge; it does not mutate the sleeping creature. Sleep is not assumed to persist for the entire delay.
- Pending Recall is checked before forecasting. The initial implementation printed misleading refusal notes while a read was already pending; the follow-up removes those while preserving keys/states. Only paired first-decision changes and actual Recall messages prove a prevented read.

## Damage-first correction after the initial zoo pilot

The category/all columns above now use 5acb8104. Earlier versions and all their deaths remain in the attempt ledger. The old category selector preferred attack family before damage; the corrected selector ranks expected damage first, with family order only breaking ties. See [pilot investigation](zoo-pilot-investigation.md).
The corrected all-switch life for 1976035382 dies to a large white snake at engine turn 17873 (CL2), after an earlier fork and a surrounded fight involving Fang and an apprentice. The terminal actions are ordinary attack and cure handling; no winning/category commitment is asserted there. Six other all-switch lives reach 100k. This supersedes the earlier selected result in which all seven survived; it is retained, not hidden.

## Non-acting estimate validation

`caution_winning_fight=2` logs estimates while preserving the control actions. It is a diagnostic, not a measurement arm.
Seed 425904011 keeps exact control keys and states. At the unchanged original cat encounter:

| Turn | Damage points needed | Best attack | Turns to kill | Incoming / Borg turn | Player HP | Verdict |
| ---: | ---: | --- | ---: | ---: | ---: | --- |
| 3633 | 12 | missile | 2.809 | 6.579 | 14 | not winning |
| 3641 | 8 | missile | 1.873 | 6.579 | 14 | winning |
| 3650 | 4 | melee | 1.044 | 6.579 | 7 | winning |

At 3650, turns to die are 7/6.579 = about 1.064, so active mode selects the finishing attack rather than the control Recall.
The control logs two melee attack commands (3633 and 3641), then Recall at 3650; the earlier issue narrative described this approximately.
Rogue 390305857 retains exact keys and states for the full 100k in diagnostic mode, with 39 winning verdicts available for inspecting won fights.
All six diagnostic Ranger runs are checked against control keys/states; details and source/build/stream hashes are retained in the JSON.

## Provenance and limits

The individual before/after records, exact builds, first differing key lines and mechanism-note counts are in [local-comparisons.json](local-comparisons.json).
Natural deaths are retained in canonical Cemetery cases; [local-replay-ledger.json](local-replay-ledger.json) links attempts without inflating independence.
The ledger retains both initial awake-only runs and the wake-aware follow-up, without overwriting their streams. Refusal notes are policy considerations, not a count of successful reads that would otherwise happen; use paired decisions and actual initiation messages.
No local 50-per-class or 600-start candidate comparison was run. Range/priority and conservative-estimate choices remain hypotheses for zoo measurement.
