# Half-Elf Druid killed by a Blacklock Mage on DL5

The owner was watching game 13 on the borg-rs core of Track P build `d3d1629f`. The original recording ends with the Druid dead at game turn **896,150**, character level **17**, dungeon level **5**, deepest level **7**. The recorder names a Blacklock Mage as the killer, and the game's archive confirms the same death. [Manifest](MANIFEST.json) · [Terminal frame](terminal-frame.json) · [Game archive excerpt](borg-death-log.txt)

| Game turn | Recorded event |
| --- | --- |
| 895,867 | The Druid enters the sampled fight at 147/147 HP. |
| 895,973–896,083 | It kills two Blacklock Mages. In between it is repeatedly blinded, confused and poisoned. It quaffs Cure Light Wounds three times. |
| 896,083 | At 76 HP and confused, the emergency Phase Door check reports 100 scary grids out of 100, 97 never seen. |
| 896,120–896,142 | Blind and confused, the Druid drops from 14 to 0 HP. Phase Door remains vetoed. The stair fallback reports a down-stair route at cost 139. |
| 896,150 | A poison spell hits and the recorder reports −21 HP and death. |

Five Phase Door scrolls, two Word of Recall scrolls, and two Neutralize Poison potions remained in the inventory at death. The trace documents repeated control effects and the escape decisions. It does not establish that any single alternative would have saved the character. [Original message excerpt](recorded-messages.jsonl) · [Recorded positions](recorded-positions.tsv)

[The original Borg action stream](recorded-actions.txt.gz) is retained in full and hash-verified. [The working save](working.save.gz) was copied from slot 13 after the death. Its contents have not been validated as a playable checkpoint. The birth seed is unknown, and this watched recording was not replayed or included in the seeded population registry.
