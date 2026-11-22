# Blackguard 312081895: pulled back to DL2 with no Word of Recall (borg-reborn-rs#984)

Half-Troll Blackguard (`-race 7 -class 8`), seed 312081895, borg-rs core.
This is the zoo's arm `reborn-head-shipped` on borg-reborn-rs track-p. Zoo
run [45028029063](https://github.com/diegoami/borg-zoo/actions/runs/45028029063),
[report](https://github.com/diegoami/borg-zoo/blob/claude/dazzling-hamilton-ejjpi4/reports/reborn-trackp-9085c266-full-other-deaths/README.md).
The death's dossier is
`deaths/D-6fb7bf106e604e3c6e4fc07700e7c609aa2e4e71195737f8efa50eb32ee96ad6`
on branch `runs/2026-11-22-trackp-9085c266-full-deaths`
([#129](https://github.com/diegoami/borg-cemetery/pull/129), open).
The issue is [borg-reborn-rs#984](https://github.com/diegoami/borg-reborn-rs/issues/984).
The switches are in [borg-reborn-rs#997](https://github.com/diegoami/borg-reborn-rs/pull/997),
and the zoo request is [borg-zoo#688](https://github.com/diegoami/borg-zoo/issues/688).

**One life, one start.** Every arm replays the same start, so the arms
show what this game needed, not a rate. Each switch stays a hypothesis
until borg-zoo measures it.

Reproduce with `tools/replay.sh WORKTREE OUT [borg.txt lines...]`. The
script builds `OUT/user/borg.txt` from the worktree's `harness/borg.txt`,
adds the zoo arm's overrides and the extra lines, and runs the zoo
report's command. It also writes the town plan records (`plan.jsonl`,
`dump.txt`); they do not change play, since the base hash is the same
with them on. Each `arms/*/borg.txt` is the file that arm played with,
and each `keys.sha256` is the full hash of its `keys.log.gz`.

## Arms (replay.sh, one start each; leads, not measurements)

| arm | build | borg.txt change | keys sha256 | end |
|---|---|---|---|---|
| base | track-p `4b2c2fcf` | none | `4aa99f20ea1ca7e6` | death by poison, turn 39700, CL4, DL2 |
| floor0 | track-p `4b2c2fcf` | `buy_recall_from_gold = 0` | `4aa99f20ea1ca7e6` | the same game |
| head-default | #997 `e0b97ea6` | none | `4aa99f20ea1ca7e6` | the same game |
| urgent | #997 `e0b97ea6` | `town_recall_urgent_depth = 1` | `858a7f7de5dcaff7` | 100,000-turn cap, CL7, max DL4 |
| hold | #997 `e0b97ea6` | `caution_recall_dl1_hold_up = 1` | `f0903d718796c565` | 100,000-turn cap, CL8, max DL3 |
| both | #997 `e0b97ea6` | both lines | `f0463d22b1d8928a` | 100,000-turn cap, CL5, max DL2 |

`e0b97ea6` is #997's head after the merge of track-p `c15a4e73`. The
earlier PR heads (`1eecc73d`, `434d5371`) give the same four hashes.

## What happened (`evidence/messages-*.log`, `evidence/state-*.log`)

In `messages.log` the third column is not the depth. Read the depth in
`state.log` (`dN/max`).

1. **10848, DL1** (`d1/2`): "Scary guy on level". The Borg reads its last
   Word of Recall as a flight ("# Fleeing the level (recall)").
2. **10848–10948**: it walks to an up staircase ("Desperate for Stairs
   (one)") and takes it, using caution's "Take stairs up". The Recall is
   still pending. The C Borg does the same (`borg-caution.c:1171`); only
   its down staircase checks `goal.recalling` (`:1189`).
3. **10948, town** (`d0/2`): it buys a torch at the General Store (6
   gold), then heads for the Alchemist to sell an unknown scroll.
4. **10990**: "You feel yourself yanked downwards!" This is not a
   trapdoor. The pending Recall fires in town and takes the Borg to its
   maximum depth, DL2 (`game-world.c:707-731`). The delay is 15 to 34
   world ticks from the reading (`effect-handler-general.c:1145`). The
   visit lasted 42 game turns.
5. It stays on DL2 until its death at 39700, on a scary level with no up
   staircase found (borg-reborn-rs#935). The end is the jelly two-step of
   borg-reborn-rs#932.

## Why no scroll was bought (`evidence/plan-records-visit9-*.jsonl`)

These are the plan records of town visit 9 (seq 14–16; `turn` is the
borg turn, `gturn` the game turn). `evidence/town-dump-visit9-base.jsonl`
is the same visit with names (Alchemist slot 10 = "Scrolls of Word of
Recall", 40 in stock, price 125).

- **base:** the urgent pass holds one torch (`urgent [[0,3,1]]`), and the
  Recall's `available` row is `[4,10,0]`. The stock cap
  (`borg_town_shadow.rs:496-505`) gives (241 − 6 − 200) / 125 = 0 copies,
  so the `buy_recall_from_gold` floor of 200 removed it. The urgent Recall
  rule (#859) bypasses the floor only for trips to `prepared_recall_depth`
  (5) or deeper, and this trip was to DL2–3. The plan spends all 235 gold
  on Phase Door, oil, Cure Serious and Cure Light Wounds.
- **floor0:** the Recall is available (`[4,10,35]`), but the solve keeps
  the same plan and the same game. On a shallow trip, one scroll is worth
  less to the planner than those supplies.
- **urgent:** the first scroll is urgent (`urgent [[4,10,128]]`), and the
  first action is the Recall (`act [4,10,1,125]`). The Borg heads straight
  for the Alchemist, but the pending Recall still fires before it arrives.
  It is stranded on DL2 until 45792. After that it buys a Recall first on
  every visit and survives to the cap.
- **hold:** the Recall fires on DL1 ("yanked upwards", 10990), and the
  Borg reaches town with nothing pending. Without the urgent switch the
  floor still holds the scroll back, but the game goes on differently and
  survives to the cap.
- **both:** the same as hold, and it buys a Word of Recall at 11291.

## Not checked

- **Whether either switch changes the death rate** or costs deaths on DL1
  with a Recall pending: [borg-zoo#688](https://github.com/diegoami/borg-zoo/issues/688).
- **The DL2 stranding** (29,000 turns, "no up stairs found"):
  [borg-reborn-rs#935](https://github.com/diegoami/borg-reborn-rs/issues/935).
