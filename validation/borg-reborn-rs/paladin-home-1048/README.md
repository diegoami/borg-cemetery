# Paladin Home diversity and excess stock

[Duplicate stacks #1048](https://github.com/diegoami/borg-reborn-rs/issues/1048)
· [Unwanted items #1049](https://github.com/diegoami/borg-reborn-rs/issues/1049)

The owner's CL26 Paladin was recorded on source
`206cf4e7`, executable SHA-256
`3374405c8a7581f1185b7152368dccec3c7fd535e72de324776c0382a058a93c`.
The recording is `20261122-213635-4.2N64ju/native`. The captured
town visit's source save is at turn 3,220,167 and has SHA-256
`b06b73650bb8315560c205a7b557a648cc5a2306a367fef70b7cb5142b94e6b4`.

At turn 3,220,177 the plan record lists 359 Phase Door scrolls across
nine Home stacks and 20 carried. It also lists 68 Treasure Detection
scrolls across two Home stacks, plus three carried. Home has 24 used
slots. The source recording shows Treasure Detection being deposited in
the headroom pass. The Phase Door reserve is six carried scrolls.

The ordinary model gives long-term minor positive value to additional
Phase Door. A departure headroom sale can store it instead of disposing
of it, and the existing Home sale rule requires zero carried and reserve
value. The physical stack-limit rule protects the carried reserve, clears
additional Home stacks and excludes the already-covered kind from
nonurgent purchases. The separate unwanted-stock rule reuses the known
kinds the capability planner deliberately excludes, including Treasure
Detection. It allows a no-selling shop to accept those copies even
when it pays zero.

## Controlled visits

Both candidates start from a private copy of the same save, with the
saved engine RNG, original per-character game settings and fresh Borg
memory. A debugger clears the pending Recall counter (17) at the first
native turn callback in each private run. This gives the Paladin time
to complete the town pass. The uninterrupted game was not changed.

| Candidate | Phase Door at Home | Carried Phase Door at last plan | Treasure Detection at Home | Carried Treasure Detection | Free Home slots |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original at the start | 359 (9 stacks) | 20 | 68 (2 stacks) | 3 | 0 |
| Cap only, `1bd1ef79` | 80 (2 stacks) | 6 | 68 (2 stacks) | 3 | 7 |
| Cap plus unwanted stock, `ffa2fa3f` | 80 (2 stacks) | 6 | 0 | 0 | 9 |

The final Home withdrawals are followed by recorded sales, despite
“Buying” appearing in the Borg's generic Home-withdrawal message.
The combined run leaves town with 50 tenths of a pound and five pack
slots free. Both trials reach their prescribed caps alive. The new town
records identify known item roles, Home eligibility, and the physical
counts before each transaction.

[First and last plan receipts](stock.tsv)
