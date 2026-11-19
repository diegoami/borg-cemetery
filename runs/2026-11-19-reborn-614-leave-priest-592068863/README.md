# Half-Elf Priest 592068863: death in a giant white mouse colony (borg-reborn-rs #614 leave arm)

**Dossier:** [`deaths/D-5153ba001e086c3d3d5975d2820cadc1822412aaab3311c6481cd41402e0b240`](../../deaths/D-5153ba001e086c3d3d5975d2820cadc1822412aaab3311c6481cd41402e0b240/)

## Provenance
- **Source:** diegoami/borg-reborn-rs `8a427494fa3cf16cefabe24cd1681b287b0137d2`, branch `task/T614-rest-at-stairs` (PR #616): main `951eecbd` plus #614's change. Clean build (`git_dirty=no`), source hash `c663dfcb…`, binary `b6f14caf…`, engine upstream `42cd156ac`.
- **Run:** `BORG_CORE=borg-rs BORG_TXT_SET="borg_param_caution_stairs_leave_on_monster=1" harness/run.sh OUT 592068863 1 3 100000 exact,menu`. The start is classes-18's Half-Elf Priest (race 1, class 3), 100,000 game turns. The shipped `harness/borg.txt` has one line rewritten: the #614 leave rule on (its companions at their shipped 10 and 1).
- **Outcome:** killed by a giant white mouse on DL1 at game turn 86,224, CL6.
- **Reproduction:** verified. The key stream equals the first local run of the same arm, on the dirty build that preceded the clean commit (the same source and binary hashes). This dossier was exported with this repository's current `scripts/native/export-death.py`.
- **Lineage:** the same start with both #614 switches at 0 plays a different game from game turn 1,281 and lives to 100,000. So this is one life of one arm, not an independent sample.

## What happened
- **The rule this arm tested is not involved.** Its last firing (`# Leaving by the stairs: a monster while recovering`) was at game turn 63,020, 23,000 turns before the death.
- **The last level:** DL1, from game turn 73,503 to 86,224 (12,700 game turns). Scary the whole time: `Fleeing and leaving the level. (scaryguy)` over 1,000 times, `Fleeing (breeder level)` at 74,564.
- **A flight that never progressed,** 162 times from 50,859 to 84,786. Each round:
  1. one step toward a staircase 18 flow steps away (`Flowing toward stairs at cost 18`);
  2. a mouse adjacent, so `borg_caution`'s back-away moves it back (`Backing up to …`, 172 times);
  3. it kills a mouse (321 in all), then takes the same flight step again.

  The danger in the loop was 5–37 against 40–50 HP.
- **The end:** `Possibility of being surrounded (monsters/safegrids)(10/0)`, then death at 0 HP after the last mouse kill.
- **Before that level:** a burst of staircase bouncing (`You enter a maze of up/down staircases` dozens of times around game turns 71,233–72,803), the town↔DL1 loop of borg-reborn-rs #604.

## Settings in play (shipped values)
- `caution_breeder_fight 1`;
- `caution_breeder_hunt_max_count 4` (#558): the colony was far larger, so the Borg fled instead of hunting;
- `caution_breeder_exit 0` (#544 B, off): no walk out of the colony;
- `caution_breeder_stand_radius 5`, `caution_breeder_easy_escape_steps 5`.

## Reading
The flight never owned the movement. Each back-away step undid it, so the Borg neither escaped nor fought the colony down while it grew. This is the case for borg-reborn-rs #556 ("the exit owns the movement until reached"): once committed to a staircase on a breeder level, back-away and retreat moves must not undo the flight while the danger is well below the HP. Related: #614 (no rest before the committed staircase), #488 (stand or escape against breeders), #558 (the hunt's breeder cap).
