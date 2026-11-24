# Town checkout with an empty sling (#1102)

A constructed Human Warrior case tests the shopping path from
[#1188](https://github.com/diegoami/borg-reborn-rs/pull/1188) on shipped borg-rs
[`e34d04b788a5f6a9b600268231cfe6c4e260e820`](https://github.com/diegoami/borg-reborn-rs/commit/e34d04b788a5f6a9b600268231cfe6c4e260e820).
The parent checkpoint is the ordinary seed 1184 town at turn 11.
The author advances the character to CL22, sets max DL7, equips a sling
with (+15,+6), and gives it 12 Phase Door scrolls and eight Cure Serious
Wounds potions. It verifies 40 ordinary Iron Shots at three gold each in
the native General Store. The pack and quiver contain zero shots.

| Town shopping readiness | Starting gold | Iron Shots bought | Compatible shots at first dungeon entry |
| --- | ---: | ---: | ---: |
| Shipped on | 165 | 3 for 9 gold | 3 |
| Off | 165 | 0 | 0 |
| Shipped on | 2 | 0 | 0 |

The funded arm bought and carried shots while the off arm bought oil for
range. Both funded arms also bought light, food and armour. They left town
with two gold. The low-purse control stayed at two gold, below the verified
price of one shot.

This establishes that the merged shopping code can fill the empty launcher
when shots are affordable and there is room in the budget. The shopping
row is a value alongside other needs. An absolute departure guarantee
would require a separate policy. The published #1102 ticket gives inventory
snapshots and two purses from the original life. The exact save and the
shop offer at those turns were unavailable here. The recorded cause and
the ticket remain open.

[Receipts](receipts.json) pin both input saves and all three streams.
Run from the pinned source checkout after a clean harness build, passing
a private destination to [replay.sh](replay.sh).
