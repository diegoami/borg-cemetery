# Owner-supplied review corrections: named cases

Follow-up to the MiniMax-M3 and Claude Opus 5.5 reviews of source PRs #763/#764. The owner explicitly approved a real-threat exception for category attacks. The corrected shared specimen is `394f2aea1f7c218359f182b0e55a3f6ae56ddeca`.

This is selected-case verification, not a population comparison. Every cell below is a birth replay of an explicitly named start, borg-rs core, 100,000 engine turns. Fresh shipped controls and switch arms use the same binary and shipped profile, now including accepted main #768. Earlier case versions remain in the [attempt ledger](local-replay-ledger.json) and [previous matrix](local-cases.md); they are not relabelled as this specimen.

| Seed | Shipped control | Category1 | Winning1 | Recall1 | All1 |
| --- | --- | --- | --- | --- | --- |
| 425904011 | a wild cat @ 3660 | alive 100k; CL6 | alive 100k; CL7 | alive 100k; CL5 | Fang, Farmer Maggot's Dog @ 3621 |
| 2095979189 | a wild cat @ 3345 | alive 100k; CL6 | alive 100k; CL6 | a wild cat @ 3345 | alive 100k; CL6 |
| 1976035382 | a wild cat @ 4248 | Grip, Farmer Maggot's Dog @ 4284 | alive 100k; CL7 | alive 100k; CL6 | alive 100k; CL6 |
| 2049259432 | Fang, Farmer Maggot's Dog @ 4429 | Fang, Farmer Maggot's Dog @ 4429 | alive 100k; CL5 | Fang, Farmer Maggot's Dog @ 4454 | alive 100k; CL5 |
| 807683971 | a black naga @ 1534 | a black naga @ 1534 | a black naga @ 1534 | alive 100k; CL5 | alive 100k; CL8 |
| 1517990203 | a small kobold @ 6338 | a small kobold @ 6338 | a rock lizard @ 6299 | a small kobold @ 6338 | a rock lizard @ 6299 |
| 390305857 | alive 100k; CL6 | alive 100k; CL7 | alive 100k; CL6 | alive 100k; CL6 | alive 100k; CL7 |
| 1548306106 | alive 100k; CL8 | alive 100k; CL7 | — | — | alive 100k; CL5 |
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

The pilot on 78b8f297 used family-first ranking. The corrected ranking is expected-damage first. These are new birth trajectories, not saved-encounter counterfactuals. Actual category decisions and executions are retained in [review-comparisons.json](review-comparisons.json); survival at cap alone does not prove that the original terminal encounter was reached or rescued.

Actual examples (engine turns, all-switch arm):

- Mage 1548306106: at 1913 the wild-cat category selects attack 4 and casts
  Magic Missile, rather than firing pebbles. Its category-only trajectory
  never meets a cat/crow, so that arm is not an original-encounter replay.
- Rogue 1381972077: at 5444 the crow category selects attack 2 and throws
  oil (15 flasks remain after the throw). It later runs out of oil at10615;
  its later pebble shot at a cat at12391 is therefore a resource fallback,
  not the old defect of preferring pebbles while oil is available.
- Rogue category-only: at79325 it also selects an oil throw against a cat.

These examples prove the selected available attack in new lives, not a
saved-state replay of the pilot's exact encounters.

## Review dispositions and limits

- Fixed: complete-command race accounting, real-threat category exception, borrowed target-grid restoration, fixed-blow spell counts with shared pre-hit HP caps, observed Haste on the native danger copy, and own blessed-weapon to-hit. Leap certification is restricted to adjacent targets; unmodelled travel remains excluded.
- Category ranges already gate runtime scare suppression; independent scary rows remain intact outside the active category range. `mage3` is a class-ceiling override, not a restriction to that class. Regression tests cover these semantics rather than inventing a scare for an attack-only row.
- Recall projectability is required for an immobile ranged monster with no walking route. A regression proves that dropping that branch would omit exposure. The code is clarified while retaining that behavior.
- Native status/spell danger is a conservative risk estimate, not measured literal HP damage. Spell flags remain a coarse ranged proxy. Stun/Slow are not assumed to persist. No result here establishes population improvement.
- See [Zoo #511](https://github.com/diegoami/borg-zoo/issues/511) for the explicit new measurement pin. The initial pilot remains attached to 78b8f297. The owner alone schedules any new measurement.


The three [fresh won-fight examples](review-won-fights.json) refer to
three distinct kills, not repeated verdicts during one fight. In the new
425904011 all-switch death, the final verdict at3613 is not-winning
(4 commands, 4.660 incoming, 2HP); ordinary shooting follows a refused
Recall and Fang kills it at3621. This is retained as a failure, not a
winning-fight success. An earlier divergence can still cause later exposure.
