# Review follow-up for #1169

All four original replays reproduced keys, messages, state and town-plan
streams on Track P `20ac7d1903b9a018d0c81fe67d5441a36b483062`. The
[published starts](../receipts.json) and their historical evidence stay
at their original pins. The following endpoints are from the first town
plan and the last plan before the first stair. Free weight means the
planner's carry allowance minus total carried weight. Negative values
are over the allowance.

| Arm | Town arrival plan, free slots / lb | Departure plan, free slots / lb | Actual departure turn | Case daggers carried at stair |
| --- | ---: | ---: | ---: | --- |
| Mage, no book | 1 / −100.8 | 6 / 1.8 | 9,231,654 | Five unknown, 6.0 lb |
| Mage, book, normal schedule | 13 / −51.5 | 14 / 1.2 | 9,340,413 | Zero |
| Mage, same book, earlier diagnostic schedule | 13 / −51.5 | 14 / 1.2 | 9,340,413 | Zero |
| Priest, no scrolls | 2 / 5.5 | 2 / 5.0 | 601,631 | One unknown, 1.2 lb |
| Priest, three scrolls | 2 / 5.5 | 2 / 5.2 | 603,163 | Zero |

For the six original Mage daggers, the table gives the absolute end turn
of each unknown interval. All intervals start at 9,221,204. Stop at the
first identification of the last unknown rune, actual disposition while
still unknown, or the arm's first stair if still carried unknown.

| Original slot | No book, stop turn | Book, either schedule, stop turn |
| --- | ---: | ---: |
| 11 | 9,231,365, drop | 9,228,494, identified |
| 12 | 9,231,654, stair | 9,224,494, identified |
| 13 | 9,231,654, stair | 9,222,514, identified |
| 14 | 9,231,654, stair | 9,222,514, identified |
| 15 | 9,231,654, stair | 9,228,514, identified |
| 16 | 9,231,654, stair | 9,225,814, identified |

This is 62,411 unknown slot-turns without the book and 25,120 with the
book. All book-arm identifications precede the common cutoff at the
control's first stair, so those unknown totals also hold at the common
cutoff. Counting **actual occupied pack slots** through the common
cutoff gives 62,411 slot-turns without the book and 57,926 with it.
Through its own much later stair, the book arm used 233,905 total
dagger slot-turns, including the 22-turn gap between drop and pickup of
slot 12. That longer observation window makes its total incomparable
with the control's first-stair total. The book arm left with more
free slots and slightly less free weight. Its route, loot and other
dispositions also changed.

The Priest pair demonstrates the scroll and sale mechanism. The sale
removed one dagger from the pack. Other items used the room and net
departure slots stayed at two. The additional Wand of Light merged
into an existing stack. The case therefore establishes the sequence
of actions and no net slot relief at departure.

## Same-book scheduling contrast

A [local diagnostic patch](identify-diagnostic.patch.gz) moved the existing
spell opportunity ahead of ordinary movement. It reused the shipped
headroom thresholds of fewer than two free slots or less than five
pounds free, and required an unknown pack wearable, a castable spell
and the existing safety checks. The normal scroll and identification
paths remained available through their existing call sites.

The exact same book-equipped save was used in both arms. The early call
site handled 14 identification decisions and the ordinary call handled
one. On the clean build the ordinary call handled all 15. The keys,
messages, state and town plan are byte-identical between the two arms.
For this Mage the original schedule already found those safe windows.
The result supports having a usable source in this case and gives no
observed benefit from moving the call earlier. Any production scheduling
change needs a named case where a usable source is delayed, with a
headroom trigger and the same safety and target safeguards.

[Receipts](receipts.json) pin both clean and diagnostic builds and the
streams. Run [the original replay script](../replay.sh) from the clean
pin to reproduce the four clean arms. To reproduce the diagnostic arm,
apply the patch in a separate checkout at the clean pin and build.
Use the same `mage-book.save` from the original replay's private saves
directory, the same flags and cap, and a fresh output path. The exact
configuration is in the diagnostic receipt.
