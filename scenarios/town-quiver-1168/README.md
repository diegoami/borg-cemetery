# Town quiver trim on a retained Mage

These paired native replays exercise [PR #1171](https://github.com/diegoami/borg-reborn-rs/pull/1171) at 284fc47d401bbb42f19d3f4dc67b30aba58d6180, based on Track P 3c1aa9397c68fd67f0757f60c6655e0e8c4f9692. Each pair uses one input, a fresh Borg, the saved engine RNG, and the shipped borg-rs core. The only policy change between arms is the quiver reserve set to 0 or 40.

| Starting kit | Reserve | Plain shots dropped | First departure allowance | Free pack slots |
| --- | ---: | ---: | ---: | ---: |
| CL37, 300 pebbles | 0 | 0 | 131.2 lb over | 3 |
| CL37, 300 pebbles | 40 | 170 | 63.2 lb over | 7 |
| CL37, 40 pebbles | 0 or 40 | 0 | 27.2 lb over | 10 |
| CL45, 40 pebbles | 0 or 40 | 0 | 5.0 lb free | 2 |

A native inventory read found 210 plain and 90 enchanted shots in the 300-pebble start. The enchanted stacks contain 22 (+3,+1), 40 (+2,+2), 18 (+1,+6) and 10 (+2,+3) shots. The candidate drops four plain stacks of 40 and one of 10. The native inventory message then reports 40 matching plain shots and the next recorded transaction is at the Bookseller. The 130 retained shots weigh 52 lb. Of that, 36 lb is enchanted ammo. Everything outside the ammunition accounts for the other 11.2 lb of the overage. With 40 or fewer total shots in the control saves, each pair's key stream matched.

The parent and the previous receipt are in [late-inventory-mage-10815143](../late-inventory-mage-10815143). The previous comparison enabled auto_more for the startup prompt. On these private inputs, [restore-option.py](restore-option.py) restores the option from the [original save](../mage-rubble-10815143/start.save.gz) and adjusts its options checksum. All other payload bytes are preserved. The updated frontend handles the startup prompt.

[Receipts](receipts.json) pin the save bytes, effective settings, build, endpoints and stream hashes. Compressed messages and native town plans are in the evidence directory. The two runs in each pair share one start. The cases establish the trim and reserve behaviour for these kits. A class and launcher comparison belongs in Zoo before activation.

The [six replays after the Track P sync](replays/e216d344/receipts.json) use the same saves on `e216d344140f6d46d561df7d5aaadaf879dd23c8` with Track P `37b501043b5fe741b1085e6bb73833c107632a36`. Every arm reproduced the earlier key, message, and state hashes and the same departure and stop results. The new receipts identify the effective settings on the synced build and retain the town plans whose bytes changed.

The [ranged-readiness sync replays](replays/f556d21c/receipts.json) repeat all six cases at `f556d21c` on Track P `515775ac`. Their key, message, and state logs and departure outcomes match. The same build resolved 40 for the saved CL37 Mage and 80 for an early Ranger canary under the [class profile in Zoo #781](https://github.com/diegoami/borg-zoo/issues/781). The Ranger canary checks configuration resolution.

Build the pinned PR head from an isolated checkout with the repository's normal harness. From that checkout, run the following with a new private trial directory.

```sh
bash "$fixture/replay.sh" "$trial"
```
