# HP/risk unit separation: named cases

Follow-up to the third owner-supplied reviews. Literal contact HP is now separate from unmodelled spell/status risk. The bow time formula is retained after verification against engine per-arrow damage and rate conversion; the proposed interpretation of the rate as per-shot damage was not applied. The corrected shared specimen is `a4e4d91546cd9a2e1b43a03c0321feaa14b9893f`.

This is selected-case verification, not a population comparison. Every cell below is a birth replay of an explicitly named start, borg-rs core, 100,000 engine turns. Fresh shipped controls and switch arms use the same binary and shipped profile, including accepted main #768 and #779. Earlier case versions remain in the [attempt ledger](local-replay-ledger.json), [preceding review matrix](review-cases.md) and [initial matrix](local-cases.md); they are not relabelled as this specimen.

| Seed | Shipped control | Category1 | Winning1 | Recall1 | All1 |
| --- | --- | --- | --- | --- | --- |
| 425904011 | a wild cat @ 3660 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL5 | Fang, Farmer Maggot's Dog @ 3621 |
| 2095979189 | a wild cat @ 3345 | alive 100k; CL6 | alive 100k; CL7 | a wild cat @ 3345 | alive 100k; CL6 |
| 1976035382 | a wild cat @ 4248 | Grip, Farmer Maggot's Dog @ 4284 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL5 |
| 2049259432 | Fang, Farmer Maggot's Dog @ 4429 | Fang, Farmer Maggot's Dog @ 4429 | alive 100k; CL6 | Fang, Farmer Maggot's Dog @ 4454 | alive 100k; CL4 |
| 807683971 | a black naga @ 1534 | a black naga @ 1534 | a black naga @ 1534 | alive 100k; CL6 | alive 100k; CL7 |
| 1517990203 | a small kobold @ 6338 | a small kobold @ 6338 | a rock lizard @ 6299 | a small kobold @ 6338 | a rock lizard @ 6299 |
| 390305857 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL6 |
| 1548306106 | alive 100k; CL8 | alive 100k; CL7 | — | — | alive 100k; CL6 |
| 1381972077 | alive 100k; CL6 | alive 100k; CL6 | — | — | alive 100k; CL6 |

The first seven rows are the original owner-named cases. Mage 1548306106 (0/1) and Rogue 1381972077 (1/6) were explicitly added by the second review to inspect the old pebble/oil selector defect; their winning/Recall-only arms were not requested.

## Fight time and original cat estimate

Time now books complete commands and whole fallback finishers. A shot retains its actual fractional command duration. Booking a whole melee command is conservative when early death saves unused blow energy (player-attack.c:990-1020). The previous continuous 1.044-turn estimate is not a current winning certificate.
The new non-acting diagnostic preserves the fresh 425904011 control keys and states exactly. Original encounter notes:

```
548 3633 0 # Fight race: 1 attackers, 3.000 turns to kill, 6.579 damage/turn, HP 14: not winning (#759)
548 3633 0 # Fight race targets: wild cat:needs 12 HP, attack 3 4.372 HP/turn
551 3641 0 # Fight race: 1 attackers, 2.000 turns to kill, 6.579 damage/turn, HP 14: winning (#759)
551 3641 0 # Fight race targets: wild cat:needs 8 HP, attack 3 4.372 HP/turn
555 3650 0 # Fight race: 1 attackers, 2.000 turns to kill, 6.579 damage/turn, HP 7: not winning (#759)
555 3650 0 # Fight race targets: wild cat:needs 4 HP, attack 1 3.931 HP/turn
```

## Pebbles versus oil

The pilot on 78b8f297 used family-first ranking. The corrected ranking is expected-damage first. These are new birth trajectories, not saved-encounter counterfactuals. Actual category decisions and executions are retained in [units-comparisons.json](units-comparisons.json); survival at cap alone does not prove that the original terminal encounter was reached or rescued.

## Review dispositions and limits

- Fixed: complete-command race accounting, real-threat category exception, borrowed target-grid restoration, fixed-blow spell counts with shared pre-hit HP caps, observed Haste in the literal HP rate, and own blessed-weapon to-hit. Leap certification is restricted to adjacent targets; unmodelled travel remains excluded.
- Category ranges already gate runtime scare suppression; independent scary rows remain intact outside the active category range. `mage3` is a class-ceiling override, not a restriction to that class. Regression tests cover these semantics rather than inventing a scare for an attack-only row.
- Recall projectability is required for an immobile ranged monster with no walking route. A regression proves that dropping that branch would omit exposure. The code is clarified while retaining that behavior.
- Native status/spell danger is not HP and is excluded from the forecast. Unmodelled contributions refuse explicitly on risk, without a fabricated damage figure. Known harmless non-moving spells add no HP and do not remove contact travel time. Stun/Slow are not assumed to persist. No result here establishes population improvement.
- See [Zoo #511](https://github.com/diegoami/borg-zoo/issues/511) for the explicit new measurement pin. The initial pilot remains attached to 78b8f297. The owner alone schedules any new measurement.


## Actual attack and refusal notes

- Mage1548306106 category-only: crow at83143, attack4, Magic Missile.
  All-switch: wild cat at1913, attack4, Magic Missile.
- Rogue1381972077 all-switch: crow at5444, attack2, oil throw.
  Category-only also chooses oil against a later cat. These are new lives,
  not exact saved-state counterfactuals of the pilot encounter.
- Recall807683971 still refuses at1390 with155.61 modelled contact HP versus
  15HP: the sound plain-HURT naga calculation is preserved.
- [Refusal notes](units-refusal-notes.json) now distinguish quantified contact
  HP from explicitly unmodelled spell/status risk. Native fear prices are
  not multiplied by the delay. The acolyte's HEAL/SCARE alone adds no HP or
  zero-time melee approach; unknown damaging/status/movement contributions
  still refuse conservatively. Such refusal is not a claim of proven lethality.
- Counts are repeated policy considerations, not a count of successful
  Recall reads prevented. Check actual initiation messages and paired actions.

## Bow and regeneration review checks

The bow model's input is a rate: an18HP arrow at3 shots per turn supplies
54HP/turn with a1/3-turn command.30HP needs2 arrows and2/3turn. A rate of
18HP/turn at that speed instead means6HP arrows, needing5 arrows. The actual
engine ranged_damage never multiplies an arrow by firing rate
(player-attack.c:554-582); only command energy changes (:1087). Tests now
use the focused rate conversion as well as finite-ammo/fallback examples.
The field is named hp_per_turn_milli to make the units explicit. The CL20
FAST_SHOT increment is level/3, giving16 shots-tenths before gear, not20
(player-calcs.c:2264-2287). Removing duration would over-credit arrows.

Regeneration is gated by turn%100 in process_monsters
(mon-move.c:1893-1897), independent of how often a monster attacks. The
existing conversion through player energy is retained; the suggested
monster-speed scaling would be a second, incorrect conversion. This is
engine-source verification, not a new population experiment.
