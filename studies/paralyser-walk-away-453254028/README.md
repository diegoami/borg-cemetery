# Walking away from a floating eye: switch arms for Half-Elf Necromancer 453254028

This is a counterfactual trial of one recorded death,
[D-88768638033650b6…](../../deaths/D-88768638033650b62916128147e2e9ee8ce6e53590c6d119d2d538df88f09e08/analysis.md)
(borg-cemetery#141). The Borg was a Half-Elf Necromancer, CL3, 29 HP. On DL1 a floating eye's paralysis lock killed it at turn 77,923.

The arms play the four switches of
[borg-reborn-rs#1125](https://github.com/diegoami/borg-reborn-rs/issues/1125)
(PR [borg-reborn-rs#1129](https://github.com/diegoami/borg-reborn-rs/pull/1129)), one by one and in pairs. Owner: "from paralyzing monsters it is necessary to walk away".

**One life, one start.** Every arm is the same birth played again with other settings. That makes the arms continuations of one life, not independent samples. They show what this game needed, not a rate (borg-reborn-rs RULES 12, 14). The population measure is [borg-zoo#735](https://github.com/diegoami/borg-zoo/issues/735).

## The switches
All four are compiled and shipped 0 in #1129, and each acts only without Free Action:
1. `escape_paralyser_fight_lost`: next to an awake paralyser, the Phase rule's fight is lost, and the Phase Door is allowed.
2. `caution_paralyser_step_away`: next to a never-moving paralyser, the first action is a step out of its reach.
3. `caution_paralyser_no_reach`: no flow enters a known paralyser's grid or the eight around it.
4. `caution_remember_never_move`: a `NEVER_MOVE` record survives the anti-bounce reset and the 2000-turn expiry.

## Reproduction
- **Build.** borg-reborn-rs [`d8b55d64`](https://github.com/diegoami/borg-reborn-rs/commit/d8b55d647ec941676ac2449ad97a786ecf8f235f) (the case's build) plus `tools/1125-on-d8b55d64.patch`. The patch is #1129's code on that base, with its params entries placed by hand; it was never committed to borg-reborn-rs. Build with `BORG_IMPL=rust harness/build.sh`, using GCC 13.3, rtl argument order and rustc 1.97. The binary's sha256 is `1c0d856bc6c8…`.
- **Command.** `tools/run-arm.sh OUTDIR "<overrides>"`: seed 453254028, menu letters race 1 class 4, 100,000 turns, exact turns, played from birth.
- **The review fixes of borg-reborn-rs `01055045` change no arm.** The patch now carries them: no flow destination in a paralyser's reach, and no early fight beside an awake paralyser. Every arm replayed with them plays the same keys as before.
- **The off arm is the case.** Its `keys.log` is `9fb2a2318e93…`, the dossier's `result_sha256`. Its messages and state logs equal the dossier's as well. The switches at 0 change nothing.

## Arms
The exact hashes and `borg_txt_sha256` of each arm are in `arms.tsv`.

| arm | result | first keys.log line differing from off |
|---|---|---:|
| off | dead at 77,923 (floating eye), CL3 | — |
| 1 | the cap, CL4, DL1 | 8,428 |
| 2 | **dead at 77,933** (floating eye), CL3 | 8,428 |
| 3 | dead at 77,923, **same keys as off** | — |
| 4 | the cap, CL5, DL1 | 6,131 |
| 1+2 | **dead at 77,933**, same keys as arm 2 | 8,428 |
| 2+3 | the cap, CL4, DL3 | 8,428 |
| all | the cap, CL5, DL1, same keys as arm 4 | 6,131 |

## What each arm shows
- **Arm 1 reads the Phase Door.** At 77,789, the case's one decision at HP 7, the rule judges the fight lost. The landing is ok ("0 scary landing grids of 100"), and the Borg reads a Phase Door with the eye adjacent. It is never next to the eye again. See `evidence/notes-77780-p1.txt`.
- **Arm 2's step is undone.** At 77,789 it steps out (`# Stepping out of the reach of the paralysing floating eye, no Free Action (#1125)`). On the next think `Flowing toward dark-bfs (ring 3)` walks back beside the eye. It is paralysed at 77,803 and gets no further decision; it dies 10 game turns after the case. See `evidence/notes-77780-p2.txt`.
  - Its first attempt, on an earlier draft, found "no grid out of its reach". The case's 400-turn flow loop had raised the anti-bounce count past `caution_bounce_limit`, and `bouncing()` refused every grid. #1129's step skips that test.
- **Arm 1+2 plays arm 2's game key for key.** The step runs before the Phase rule is asked. After the walk back the Borg is never free to decide again, so switch 1 never acts.
- **Arm 3 changes nothing.** From 77,419 the anti-bounce reset (counts 500–503) wipes every monster record each think, including the eye. The flow is closed only around known paralysers, so with the record gone nothing is closed. That reset is the case's actual "forgetting", not a loss of view.
- **Arm 2+3 steps out and stays out.** After the step, the eye's reach is closed, and the record is still there, re-created at 77,789. The Borg explores on and descends to DL3 by the cap. See `evidence/notes-77780-p23.txt`.
- **Arm 4 is a different game from turn 62,148.** It meets another floating eye at (7,32) on an earlier level, during another bounce reset. With the switch off that eye is forgotten and re-created each think, and the Borg goes on with `dark-bfs (ring 17)`. With the switch on the record is kept, and the flows choose differently (`evidence/notes-62100-off.txt` and `notes-62100-p4.txt`). The case's level is never reached in the same state, so the arm does not test the case's eye.
- **"All" plays arm 4's game.** The other three switches never act in it.

## Conclusions (hypotheses)
- **Switch 2 needs switch 3, and switch 3 needs a record of the eye.** Switch 4 keeps that record through a bounce reset. The zoo request bundles 2+3+4 into one arm.
- **Switch 1 alone saved this game,** but it acts only at a decision the Borg gets while next to the eye. Here that was one decision in 336 game turns of paralysis.
- **Not tested here:**
  - mobile paralysers (homunculus DL15, carrion crawler, ghoul and deeper);
  - games with Free Action;
  - whether closed reaches cut a level and raise stalls or `bouncing-borg` exits (asked of the zoo).
- **Out of scope:** the 400-turn loop between `dark-bfs (ring 3)` and `targetable position` next to the eye is not addressed by #1125.

## Deaths in this study
Arms 2 and 1+2 died, both in the same new game (keys `242e72f7…`). They are continuations of the case's life under trial settings, not natural deaths of a measured run. So they are recorded here as trial results, with their hashes, and get no dossier of their own.
