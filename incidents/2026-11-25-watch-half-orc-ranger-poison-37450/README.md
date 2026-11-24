# Half-Orc Ranger killed by poison on DL2

The owner was watching Ranger `Borg261125001727` on the borg-rs core of Track P build `52fff0de`. Poison killed him at **CL4, DL2, turn 37,450**. He had reached DL3. The terminal recorder frame shows −1 HP and 80 gold. [Terminal frame and inventory](terminal-frame.json) · [Game death log](borg-death-log.txt) · [Manifest](MANIFEST.json)

| Game turn | Recorded event |
| --- | --- |
| 25,655–26,595 | With 190 gold, the Ranger buys two Cure Serious Wounds potions for 140 gold, then 36 arrows for 36 and a robe for 14. He leaves town with zero gold, three Cure Light Wounds, two Cure Serious Wounds, and one Word of Recall. |
| 35,738–35,748 | The Borg tests an unidentified Indigo Potion at full HP. The potion is Poison. On the next decision he uses his last Neutralize Poison and clears the effect. |
| 36,912–36,975 | He uses the last Cure Light Wounds, then the last Cure Serious Wounds. He has 80 gold and does not reach town again. |
| 37,302–37,320 | A blubbering icky thing inflicts and reapplies poison. At 12/37 HP the trace estimates about 18 poison damage pending and no carried healing. |
| 37,341–37,450 | The Borg uses Phase Door and heads toward the stairs. Poison continues to tick and kills him. Word of Recall is still in his pack. |

The last town visit was cash-limited. By the time healing ran out, he had 80 gold, and the same run had previously paid 20 gold for a Cure Light Wounds potion. The capture does not show what the shop would have offered on another visit. The static healing restock check on this build starts at DL6, and `kit_restock` was off. [Town and encounter frames](town-and-final-frames.jsonl) · [Combat messages](recorded-combat.jsonl) · [Borg decisions](recorded-decisions.jsonl)

The two follow-ups are [remove experimental potion tasting](https://github.com/diegoami/borg-reborn-rs/issues/1213) and [return to town when healing runs out](https://github.com/diegoami/borg-reborn-rs/issues/1214). The tasting used the cure that would otherwise have remained available for the later poisoning. Whether an earlier return or another action would have saved this life remains untested.

## Evidence and replay

- [Death-time Borg map](death-map.txt) preserves the Borg's tracked map and observations.
- [Character-slot save](working.save.gz) was copied after death. Its internal turn and playability have not been verified. Loading a save initializes fresh Borg working memory.
- [Complete native recording and diagnostics](https://github.com/diegoami/angband-workspace/releases/download/borg-ranger-poison-37450/borg-ranger-poison-full.tar.gz) require access to the owner's private workspace.
- The birth seed and exact replay have not been verified. This watched incident is outside the seeded population registry.
