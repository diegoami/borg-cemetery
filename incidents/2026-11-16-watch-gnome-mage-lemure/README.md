# Watched game, 2026-11-16: Gnome Mage killed by a lemure on DL13

A watched game (`watch-borg.sh --name RustBorg`, X11, recorder off) of
borg-reborn-rs, played with the `borg-rs` core and an errands plan. It is an
**incident**, not a measured run and not a native death: nothing recorded it, so
there is no key stream or birth seed, and the native exporter cannot take it.
It is not counted as an independent life in the statistics.

| | |
| --- | --- |
| Character | RustBorg, Gnome Mage |
| Outcome | killed by a lemure on dungeon level 13, character level 9/9 |
| Exp, gold, turn | 1728, 4225, game turn 848506 |
| Source | `diegoami/borg-reborn-rs` at `f02cd2940a7439a8965b3883270a9a73df7e0bf5`, clean tree |
| Watch binary | sha256 `906a3995cef841dc9d7c8f953eb2e9592ef3dfc7323b3208e0ff599f26cb268b` (local, not in Git; rebuild with `./watch-borg.sh --build-only`) |

## Configuration

`borg.txt` is `harness/borg.txt` of that commit with `borg_reborn_core =
borg-rs`, `borg_town_plan = 1`, `borg_trip_policy = 1`,
`borg_trip_unknown_stacks = 5`, `borg_trip_pack_slack = 1`, the
`borg_param_caution_heal_when_outmatched = 1` and 16 attack-preference values
changed, and `borg_plan = errands_plan.txt` appended. `errands_plan.txt` is
`harness/plans/errands_plan.txt`. File hashes are in
[MANIFEST.json](MANIFEST.json).

## Open question

The plan caps a level 9 mage at `max-depth 4` (`[mage]`, `level == 9`), yet the
Borg died on DL13. The configuration was valid: a plan that fails to load exits
with code 2 before play. So the plan probably loaded but did not hold the Borg
at depth 4. Not yet determined, and no file can settle it (no trace, no move
log): a trapdoor, Deep Descent, a stair move, or manual play. Reproducing it as
a recorded `harness/run.sh` game, or starting a recording from process startup
(`start-recording.sh` in borg-rs), would allow analysis.

## Files

- `RustBorg.save`: the working save, copied while the game was still running.
  Its header says "saved, not dead", while `borg-log.txt` records the death.
- `borg-log.txt`, `borg.dat`, `RustBorg.map`, `CharOutput.txt`: the game's
  archive and character output.
- `borg.txt`, `errands_plan.txt`: the exact configuration.
