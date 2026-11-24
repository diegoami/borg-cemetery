# Human Paladin killed by Wormtongue on DL8

The owner was watching Human Paladin `Borg261124132707` on the borg-rs core of Track P build `3c46575d`. Wormtongue, Agent of Saruman, killed the Paladin at **CL14, DL8, turn 645,892**. The recorder reports −1 HP at death. [Terminal frame](terminal-frame.json) · [Game death log](borg-death-log.txt) · [Manifest](MANIFEST.json)

| Game turn | Recorded event |
| --- | --- |
| 645,858–645,862 | The Borg used a Wand of Wonder. Wormtongue sped up and cast a frost bolt. |
| 645,868 | At 59/131 HP, the emergency Phase Door check found no adjacent enemy and chose a Wand of Wonder attack. Wormtongue cast another frost bolt. |
| 645,878 | At 21/131 HP, the same Phase Door check rejected the scroll and the Borg used the wand again. |
| 645,882 | Wormtongue cast a venomous cloud, adding poison. |
| 645,888–645,892 | At 3/131 HP, the Borg quaffed Neutralize Poison. It cleared poison. Wormtongue then hit and killed the Paladin. |

The trace reports 33 Cure Light Wounds and 8 Cure Serious Wounds at the last decision. The open question is how the escape, healing, poison and attack checks competed over these turns. The record alone cannot establish whether another action would have saved the Paladin. [Combat messages](recorded-combat.jsonl) · [Borg decisions](recorded-decisions.jsonl)

The earlier ranged-supply observations belong to [borg-reborn-rs #1184](https://github.com/diegoami/borg-reborn-rs/issues/1184). They concern the same life, earlier in the run.

## Evidence and replay

- [Death-time Borg map](death-map.txt) contains the Borg's map and tracked observations at death. It is a diagnostic dump.
- [Character-slot save](working.save.gz) was copied after death. Its internal turn and ability to resume have not been verified. Loading it would initialize fresh Borg working memory.
- [Complete recorder and diagnostics archive](https://github.com/diegoami/angband-workspace/releases/download/borg-1184-paladin-recording/borg-1184-paladin-final-recording.tar.gz) requires access to the owner's private workspace repository.
- The birth seed and exact replay have not been verified. This watched incident is outside the seeded population registry.
