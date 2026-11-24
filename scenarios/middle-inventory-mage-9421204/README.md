# CL18–19 Mage inventory continuation

This is a continuation of the [Cemetery overweight Mage](https://github.com/diegoami/borg-cemetery/tree/0cca725f4f59bd70f91467ba6af6c6fa8604a1e6/scenarios/mage-overweight-cursed-kit-9221204), for [#810](https://github.com/diegoami/borg-reborn-rs/issues/810), [#846](https://github.com/diegoami/borg-reborn-rs/issues/846), and [#1169](https://github.com/diegoami/borg-reborn-rs/issues/1169). The new start is the living end of the earlier 200,000-turn replay, on DL6 at CL18. A fresh Borg resumed with saved engine RNG and the shipped borg-rs core on `c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894`.

| Saved state | Turn | CL | DL | Max DL |
| --- | ---: | ---: | ---: | ---: |
| `mage-before-continuation` | 9421204 | 18 | 6 | 9 |
| `mage-before-wand-use` | 9430001 | 19 | 5 | 9 |
| `mage-after-wand-use` | 9440009 | 19 | 1 | 9 |
| `mage-living-after-50k` | 9471205 | 19 | 2 | 9 |

The replay reached its turn cap alive. Its first observed departure was 9.8 lb over the planner's allowance with five free pack slots. It aimed a Wand of Light, used a Wand of Wonder twice in emergency combat, and then discarded both while charges remained. This sequence motivates an item-specific value and safe-use replay. These checkpoints are from the same life and the deepest level reached was DL9, one floor short of the middle-game study band.

The original continuation input reproduced #1154 with a pending learning message and zero Borg keys. Use [prepare-resume.py](../late-inventory-mage-10815143/prepare-resume.py) for a private copy with `auto_more` enabled, and give the headless run a cap above the saved turn. No change is made to the recorded bytes. See [receipts.json](receipts.json) for save and stream hashes.
