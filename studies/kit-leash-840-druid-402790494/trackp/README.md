# The same start on track-p `e2d8919e`

Owner, 2026-11-22: "have you tested on main or on track-p? Main was many commits behind" and
"track-p is being merged". These are the study's arms replayed on borg-reborn-rs `origin/track-p`
**`e2d8919e`** (merge of #937; 105 commits ahead of main `b34196c5`, nothing on main missing),
plus a `town_hunt`-only arm (H). It is still one start and an anecdote (RULES 14); the zoo's
`track-p` re-run of #589 is borg-zoo#646 (definitions in borg-zoo#647, the `town-hunt` arm in #653).

## Build and method

As in the parent study: `BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh`
(GCC 13.3, `arg_order=rtl`, binary sha256 `8c738545bb4d…5a83`), then
`harness/run.sh OUT 402790494 10 2 100000 menu,exact` per arm with `BORG_PARAM_*` overrides on
`track-p`'s `harness/borg.txt` (borg_txt_sha256 `42c47806…9823`). Every override is in the run's
`params-core.json` with origin `environment`. `track-p` ships every kit switch and `town_hunt` at
0, like main. `../arms.sh OUT <track-p worktree>` plays A–F; H is `BORG_PARAM_TOWN_HUNT=1`.
Files: `arms.json` (full hashes, counts) and `extracts/` (same files as the parent study).

## Arms

| arm | settings | outcome | CL | max DL | params_core | keys.log | first key differing from A |
|---|---|---|---|---:|---|---|---|
| A | none (control) | alive at the cap | 7 | 2 | `21a3f54b…` | `21caaa12…` | — |
| B | `kit_leash=1` | alive | 8 | 3 | `b2322ec4…` | `2c5a54c5…` | turn 13,476 |
| C | `kit_leash=1 kit_leash_min=2` | alive, = B | 8 | 3 | `29f81f91…` | `2c5a54c5…` | 13,476 |
| D | `kit_leash=1 kit_leash_power=2` | alive | 6 | 2 | `6f2aadac…` | `c2b4349f…` | 13,476 |
| E | `kit_leash=1 kit_money_first=1` | alive, = B | 8 | 3 | `5c818389…` | `2c5a54c5…` | 13,476 |
| F | kit-money-hunt (`kit_leash=1 kit_leash_min=2 kit_money_first=1 town_hunt=1`) | alive | 7 | 2 | `8a292a12…` | `df24ccbf…` | 471 |
| H | `town_hunt=1` (town-hunt) | alive | 6 | 2 | `3beb7ecb…` | `a4ac4301…` | 471 |

| arm | turns at 0 gold | gold at 10k / 30k / 50k / 70k / 90k / cap | max gold | "You bought" lines | flasks thrown | crow killed at (bites taken) | game turns in town / DL1 / DL2 | town arrivals |
|---|---:|---|---:|---:|---:|---|---|---:|
| A | 4,432 | 9 / 8 / 112 / 2 / 0 / 76 | 376 | 23 | 54 | never met | 15,205 / 78,009 / 6,775 | 82 |
| B, C, E | 13,768 | 9 / 0 / 13 / 96 / 254 / 299 | 548 | 32 | 67 | 27,715, 34,699, 39,092 (7) | 20,362 / 66,231 / 13,321 | 82 |
| D | 18,382 | 9 / 9 / 0 / 110 / 224 / 369 | 376 | 21 | 57 | 88,607 (0) | 14,990 / 75,769 / 9,238 | 110 |
| F | 0 | 2 / 289 / 22 / 326 / 25 / 130 | 636 | 35 | 41 | 9,576, 30,339, 78,035 (2) | 17,606 / 66,450 / 15,755 | 20 |
| H | 9,893 | 2 / 289 / 0 / 11 / 109 / 9 | 376 | 38 | 47 | 9,576, 30,339 (2) | 21,227 / 70,520 / 8,248 | 28 |

## What it shows

- **No arm dies on track-p either.** The control is alive at the cap, CL7, max DL2.
- **track-p's opening differs from main's from turn 781** (keys line 108): its town plan buys
  6 Phase Door first (90 gold) and then 9 Cure Light Wounds (180), 24 flasks (72), 3 rations;
  main buys a Cure Serious Wounds first (70), then 27 flasks and 6 CLW. The Detect Invisible
  scroll comes later (2,381). So this is a third game, distinct from both the zoo's and main's.
- **The kit leash acts much earlier than on main**, at turn 13,386 (CL2, DL1): the flasks drop
  below 5 (`Kit 0.96 (10/3 cures, 7/2 Phase, 0 missiles+4 oil …; short: ranged): leash 14`,
  C's 15 at CL2). At 13,476 the control flows to `dark-3 at cost 2`, B to `dark-4 at cost 10`:
  the first different key. As on main, the shorter leash acts through the choice of
  exploration target.
- **B, C and E are again one game.** Neither `kit_leash_min=2` nor `kit_money_first` changes a
  key on this start.
- **The leash arms meet crows the control never meets**: B/C/E kill three, taking 7 bites in
  all, and reach DL3 (the only arms that do), ending CL8 against the control's 7. D (power 2)
  ends CL6, with 18,382 turns at 0 gold and the most town arrivals (110).
- **F and H both differ from the control at turn 471, in town**, from the town hunt (as on
  main: the control flees a mean-looking mercenary to DL1, these arms keep shopping). F and H
  then play the same keys, crows at 9,576 and 30,339 included, until 35,001, after F's kit first
  goes short (33,590). So F's first difference from the control is the town hunt's,
  and its later ones are the kit's.

## For borg-zoo#589 / #646 (hypotheses)

- On both lines `kit_leash_min=2` and `kit_money_first` play the `leash` arm's keys on this
  start; expect identical plays among those arms.
- `town_hunt` alone (H) moves this game as early as kit-money-hunt does; the `town-hunt` arm of
  borg-zoo#653 is what separates the two effects over many starts.
