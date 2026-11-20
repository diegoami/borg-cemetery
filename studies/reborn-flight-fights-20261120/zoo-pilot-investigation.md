# Initial zoo pilot: attack choice investigation

The [Zoo result](https://github.com/diegoami/borg-zoo/issues/511#issuecomment-7045769634) owns the population comparison. This note investigates the recorded death bundles from [run 44774352123](https://github.com/diegoami/borg-zoo/actions/runs/44774352123), specimen `78b8f2972e1fbf8dabfb55ba34d94873e791d0e2`. No games were dispatched or replayed for this inspection. Eight death bundles, including the unchanged control/Recall Druid pair, were inspected. Build receipts, input paths and stream hashes are in [zoo-pilot-death-inputs.json](zoo-pilot-death-inputs.json).

## Confirmed selector defect

Rogue 1381972077 in `all` repeatedly used pebbles against a crow and died at 15747 while the death inventory still contained eight oil flasks. The category selector ranked attack family before expected damage: any eligible missile outranked a stronger throw. Mage 1548306106 in `attack-sight` likewise repeatedly shot pebbles at its terminal wild cat (52641). The latter observation alone does not prove a stronger alternative was eligible.

Fix `64f20bb45f07d489b5251e566037f28097a81686` sorts expected damage, including failure probability, first; missile/spell/throw/melee order only resolves equal scores. Its regression test makes stronger oil beat weaker pebbles. Integrated future specimen `5acb8104115dcd52fd9db8bfb72888cf5ca2fde4` also contains the owner-approved possible-wake Recall guard and accepted main synchronization. Neither change was present in the pilot. The generic test is not a successful replay claim for either pilot death. Local replays remain restricted to the seven owner-named starts.

## Other terminal observations

- Rogue 1502695781, attack-sight: dies of poison at 16890 during ordinary stair/flight behavior. The terminal trace does not show a category commitment holding it in combat.
- Necromancer 300036923, winning-fight: dies to a grey mushroom patch at 15976 during ordinary caution/escape handling, with 4/4 mana. The terminal trace does not establish a false winning verdict keeping it engaged.
- Ranger 226104090, all: opens a door and dies to Fang at 20737 before another decision. This is an exposure/trajectory problem; it does not by itself demonstrate a wrong winning-fight estimate.
- Ranger 226104090, Recall-safe: crow death at 3633 needs comparison of the blocked Recall and alternatives; the pilot used the initial awake-only guard, not the later possible-wake forecast.

These observations identify one implementation defect, not a complete causal explanation for every newly killed life. Reading terminal logs cannot show what the fixed policy would have done at all earlier forks. The original pilot found no survival-leading arm. The corrected specimen remains unmeasured, switches remain shipped off, and the owner chooses any subsequent zoo run or tier.
