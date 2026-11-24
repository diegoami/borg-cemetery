# Half-Troll Warrior killed by a tengu on DL5

The owner was watching `Borg261124143216`, a Half-Troll Warrior using the borg-rs core of Track P build `3c46575d`. A tengu killed the Warrior at **CL15, DL5, turn 279,663**, after he reached DL7 earlier in the same life. The recorder reports −2 HP at death. [Terminal frame and inventory](terminal-frame.json) · [Game death log](borg-death-log.txt) · [Manifest](MANIFEST.json)

| Game turn | Recorded event |
| --- | --- |
| 278,613–278,635 | The Borg first tracks a tengu and confuses it with a wand. The first logged command pulling the Warrior back follows at 278,635. |
| 278,826–279,122 | Flight Recall repeatedly refuses because of estimated contact damage and unmodelled spell or status risk. |
| 279,503 | The Warrior quaffs Cure Light Wounds. |
| 279,617–279,657 | The Borg uses emergency Phase Door at 25, 17, and 9 HP. The messages between attempts include repeated commands pulling it back. |
| 279,661–279,663 | After the last Phase Door, two return commands and several tengu hits are logged. The final hit kills the Warrior. |

The combat excerpt contains 61 return-command messages in the encounter. The terminal inventory still has 32 Phase Door scrolls, seven Word of Recall scrolls, 51 Cure Light Wounds potions, one Cure Serious Wounds potion, and five Cure Critical Wounds potions. The capture records when these actions were chosen. The outcome of any alternative action remains untested. [Combat messages](recorded-combat.jsonl) · [Borg decisions](recorded-decisions.jsonl)

This is the same Warrior that paused during the DL1 breadth-first loop at turn 5,852. The loop and the later death are separate events in that life. [Source issue #1189](https://github.com/diegoami/borg-reborn-rs/issues/1189)

## Evidence and replay

- [Death-time Borg map](death-map.txt) preserves the Borg's map and tracked observations.
- [Character-slot save](working.save.gz) was copied after death. Its internal turn and playability have not been verified. Reloading a save initializes fresh Borg working memory.
- [Complete native recording and diagnostics](https://github.com/diegoami/angband-workspace/releases/download/borg-warrior-dl1-loop/borg-warrior-final-recording.tar.gz) and the [earlier DL1 loop snapshot](https://github.com/diegoami/angband-workspace/releases/download/borg-warrior-dl1-loop/borg-warrior-dl1-loop-evidence.tar.gz) require access to the owner's private workspace repository.
- The birth seed and exact replay have not been verified. This watched incident is outside the seeded population registry.
