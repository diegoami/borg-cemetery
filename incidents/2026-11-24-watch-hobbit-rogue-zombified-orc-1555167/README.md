# Hobbit Rogue killed by a zombified orc on DL5

The owner was watching `Borg261124152430`, a Hobbit Rogue using the borg-rs core on Track P build `3c46575d`. A zombified orc killed the Rogue at **CL16, DL5, turn 1,555,167**. The deepest level reached was DL7, and the terminal recorder frame shows −3 HP. [Terminal frame and inventory](terminal-frame.json) · [Game death log](borg-death-log.txt) · [Manifest](MANIFEST.json)

| Game turn | Recorded event |
| --- | --- |
| 1,554,805–1,554,815 | During the preceding fight, the Rogue quaffs Cure Serious Wounds at 18/83 HP and is at 58/83 HP on the next decision. |
| 1,555,139 | The Borg records the final zombified orc at (38,18) in (x,y) coordinates and attacks at 12/91 HP. |
| 1,555,154–1,555,162 | After three orc hits the Rogue is at 4/91 HP. The fight race estimates one turn to kill and 3.649 expected damage per turn. It reports “winning” and the decision trace records `fight_before_flight`. |
| 1,555,162–1,555,167 | The Rogue's swing misses. The orc hits twice and kills him. |

The terminal inventory contains three potions each of Cure Light, Cure Serious and Cure Critical Wounds, five Phase Door scrolls, and two Word of Recall scrolls. The recording shows the attack that was chosen. Whether another action was usable and would have changed the outcome remains untested. [Combat messages](recorded-combat.jsonl) · [Borg decisions](recorded-decisions.jsonl)

## Evidence and replay

- [Death-time Borg map](death-map.txt) preserves the Borg's map and tracked observations.
- [Character-slot save](working.save.gz) was copied after death. Its internal turn and playability have not been verified. Reloading a save initializes fresh Borg working memory.
- [Complete native recording and diagnostics](https://github.com/diegoami/angband-workspace/releases/download/borg-rogue-zombified-orc-1555167/borg-zombified-orc-final-recording.tar.gz) require access to the owner's private workspace repository.
- The birth seed and exact replay have not been verified. This watched incident is outside the seeded population registry.
