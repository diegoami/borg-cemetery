# Review follow-up for #1102

The three existing arms reproduced keys, messages, state, town plans and
ranged-readiness traces on `20ac7d1903b9a018d0c81fe67d5441a36b483062`.
The pinned native inspections both show 40 ordinary Iron Shots at 3 gold
each. The receipt binds the inspection digests and the exact offer lines.

Two added arms vary only `borg_param_town_ranged_readiness` with the same
165-gold save and `borg_town_target_depth=20`. The in-town readiness trace
records minimum damage 10 in both arms. The native 1d4 shot with the x2
(+15,+6) sling averages 17 damage before criticals and clears the gate.

| DL20 shopping policy | Iron Shots purchased at turn 235 | Shots on first dungeon entry at turn 545 |
| --- | ---: | ---: |
| On | 4 for 12 gold | 4 |
| Off | 0 | 0 |

The original funds test bought three shots with the policy on and none with
it off. The two-gold control demonstrates an unaffordable offer at checkout.
The DL20 override tests the town forecast and qualifying offer, while the
character enters DL1 normally. This is a purchase preference competing within
the same budget. A launcher departure minimum would be a separate policy.
The original two Warrior departures remain open because their planned
depth, available offers, and checkout decisions are unrecorded here.

[Receipts](receipts.json) pin both the new streams and the identical published
streams. [Replay](replay.sh) runs the current-head arms from the source checkout.
