# near_death_candidate: observed sequence

Boundary: stable_observation; start turn 3342; endpoint 3352; resolution recovered_to_stable.

The start is inferred from sustained HP and available Borg threat estimates, not proof of safety. Missing threat, inventory or perception evidence stays unknown. Follow earlier causes beyond this boundary when needed.

Save scenario: ready_for_restart_trials; startup: fresh Borg, saved engine RNG. Alternative Borgs share a game state; original Borg memory is not restored.

Retained save turn: 3302; inferred stable boundary: 3342.

At the saved/report starting point (turn 3302), the character had 9/9 HP at depth 1. The lowest logged HP was 9/9 at turn 3302. Observed Borg mode sequence: engage.

Chronology is ordered by engine turn. Cross-stream ordering at the same turn is unresolved. Full observations are in sequence.json.

| Turn | Evidence | Observation |
| --- | --- | --- |
| 3302 | state.log:744 | HP 9/9; SP 2/2; depth 1; position 102,6 |
| 3302 | trace.jsonl:341 | Borg mode engage; goal win the exchange; choice Walk(3); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3312 | trace.jsonl:342 | Borg mode engage; goal win the exchange; choice Walk(2); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3320 | messages.log:61 | You hear a door burst open! |
| 3322 | trace.jsonl:343 | Borg mode engage; goal win the exchange; choice Walk(8); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3332 | trace.jsonl:344 | Borg mode engage; goal win the exchange; choice Walk(2); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3342 | trace.jsonl:345 | Borg mode engage; goal win the exchange; choice Walk(8); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3352 | messages.log:62 | You have 2 Scrolls of Phase Door (e). |
| 3352 | trace.jsonl:346 | Borg mode engage; goal win the exchange; choice Read { item: 4 }; threat {'horizon': 1, 'expected': 7.8374999999999995, 'worst': 13.2, 'p_death': 0.2679296875, 'disabling': 0.0, 'summoning': 0.0, 'economic': 3.135, 'sources': [{'index': 45, 'race': 53, 'name': 'Sméagol', 'dist': 1, 'speed': 130, 'awake': True, 'in_view': True, 'confused': False, 'stunned': False, 'group': 1, 'confidence': 1.0, 'rounds': 3.3, 'expected': 7.8374999999999995, 'worst': 13.2, 'disabling': 0.0, 'ranged': False}]} |
| 3362 | trace.jsonl:347 | Borg mode engage; goal win the exchange; choice Walk(4); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3372 | trace.jsonl:348 | Borg mode engage; goal win the exchange; choice Walk(4); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |
| 3382 | trace.jsonl:349 | Borg mode engage; goal win the exchange; choice Walk(4); threat {'horizon': 1, 'expected': 0.0, 'worst': 0.0, 'p_death': 0.0, 'disabling': 0.0, 'summoning': 0.0, 'economic': 0.0} |

Terminal observation: recovered_to_stable.

Investigate any evidence-backed survival improvement. Separate facts, hypotheses and missing observations; propose a mechanism, intervention, prediction and experiment. No predefined behavior checklist limits the investigation.

[Inventory, equipment and spells](inventory.md): available.

![Episode: actual terminal screenshots](media/episode.gif)

Animation capture: complete; provenance in media/media.json.
