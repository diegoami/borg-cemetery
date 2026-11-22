# Ranger 1895660873: poisoned at 0 HP with unknown cures (borg-reborn-rs#985)

Gnome Ranger (`-race 4 -class 7`), seed 1895660873, borg-rs core, the
zoo's arm `reborn-head-shipped` on borg-reborn-rs track-p. Zoo run
[45028029063](https://github.com/diegoami/borg-zoo/actions/runs/45028029063),
[report](https://github.com/diegoami/borg-zoo/blob/claude/dazzling-hamilton-ejjpi4/reports/reborn-trackp-9085c266-full-other-deaths/README.md).
That report names a dossier branch, `runs/2026-11-22-trackp-9085-full-deaths`,
which is not on this repository's remote as of 2026-11-22, so no dossier is
linked here. Issue
[borg-reborn-rs#985](https://github.com/diegoami/borg-reborn-rs/issues/985);
fix and switches in
[borg-reborn-rs#1003](https://github.com/diegoami/borg-reborn-rs/pull/1003)
(`b5b0f5fd`).

**One life, one start.** Every arm replays the same start: it shows what
this game needed, not a rate. Thresholds are hypotheses until borg-zoo
measures them.

Reproduce with `tools/replay.sh WORKTREE OUT [borg.txt lines...]`. The
script builds `OUT/user/borg.txt` from the worktree's `harness/borg.txt`,
adds the zoo arm's overrides and the extra lines, and runs the zoo report's
command. Each `arms/*/borg.txt` is the file the arm played with.

## Arms (replay.sh, one start each; leads, not measurements)

| arm | build | borg.txt change | keys sha256 | end |
|---|---|---|---|---|
| base | track-p `4b2c2fcf` | none | `31c994254ecdb188` | death by poison, turn 16670, CL3 DL1 |
| floor | #985 `b5b0f5fd` | `caution_cure_hp_floor_percent = 30` | `31c994254ecdb188` | the same game |
| hold | #985 `b5b0f5fd` | `sell_poor_town_unknown_hold = 1` | `3810978f26a68560` | 100,000-turn cap, CL8, max DL3 |

At its defaults (both switches 0), `b5b0f5fd` also plays `31c994254ecdb188`.
The `base` arm's messages and trace are in `evidence/`.

## What the Borg knew

`evidence/pack-at-16644.txt` comes from a temporary stderr-only
instrumented build. It is not on any branch. It prints the Borg's view of
its pack in the think at HP 2/25, danger 44. The cures are unaware flavours:
Tangerine ×6 (sval 8, Cure Light Wounds), Orange ×2 (sval 14, Neutralize
Poison) and Purple ×2 (sval 27, Boldness). `borg_slot` returns -1 for Cure
Light Wounds. #470 never uses an unaware item. `borg_heal_outmatched` applied
(flag 1, loss 92%, danger ≥ HP, no fast-fragile ban) and found nothing to
drink.

The bravery boost held back no cure. `trace-core-16540-16670.jsonl` shows
`avoidance` = HP in every fatal `borg_attack` think. `boost_bravery` resets
it after the rerun, and the brave think does not run `borg_caution`: the
instrumented run logs no caution call with avoidance above the HP. The
boosts' brave flows ("Flowing toward dark-5") still walked the Borg back
into the worm masses at HP 7 (`messages-16440-16670.log`, turn 16617).

## Why the kinds were never learnt

The Orange Potions were picked up at 4794 and the Tangerine ones at 7228.
On every later town visit (6391, 7158, 7820, 8660, ...) the Borg had under
10 gold and logged C's "Nothing to sell in town (leaving)"
(`borg_think_dungeon.rs`: CL < 6, gold < 10, `borg_count_sell` < 5). That
rule runs before the town planner can sell one of an unaware kind. In the
`hold` arm the Borg waits and the planner sells one Orange Potion at 6561
("You had a Potion of Neutralize Poison": `store.c:1947` makes the flavour
aware under `birth_no_selling`). The game plays differently from there.

## Not checked

- Whether either switch changes the death rate: a zoo request.
- The Ranger sells its own spellbook, Lesser Charms, at turn 221 (CL1,
  before its first spell at CL3): [borg-reborn-rs#1004](https://github.com/diegoami/borg-reborn-rs/issues/1004).
