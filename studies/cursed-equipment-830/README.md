# Cursed equipment (borg-reborn-rs#830): three deaths, with and without the fix

Three zoo deaths in which the Borg wore an item whose curse it then lived with
until it died, each replayed from the zoo's own build and then played again
with the change of [borg-reborn-rs#832](https://github.com/diegoami/borg-reborn-rs/pull/832)
(`Closes #830`). These are **single games, not measurements**: they show what
the change does in the games that prompted it. Whether it improves survival is
a borg-zoo request (borg-zoo run request linked from the PR).

| | |
| --- | --- |
| Owner's words (2026-11-21) | "avoid cursed objects if possible, and if not when cursed make it a priority to go back to town and buy a remove curse scroll"; and "don't spend a Remove Curse scroll on an item not worth keeping" |
| Source of the deaths | borg-zoo#566 (main `3b4924ba`, run 44894233710 Ranger, run 44894215287 Priest) and borg-zoo#501 (`e8b3acfd`, run 44738444831 Warrior) |
| Change under test | PR #832, head `3be3f186`: a worn item known to carry a harmful curse comes off at once (`borg_cursed.rs`); a trip to town for Remove Curse when a removable curse stays worn; a pack item counts for Remove Curse only when it is worth the scroll (100 gold) |
| Files | [MANIFEST.json](MANIFEST.json) (hashes, builds), `runs/<run>/{excerpt.txt,summary.json,keys.log.gz,messages.log.gz}`, `patches/` |

## How each run was made

- **Control runs** play the zoo's own commit unchanged. The key stream of the
  Warrior replay equals the zoo cell's `play_sha256`
  (`1981819c…`) and its `messages.log` is byte-identical to the cell's. The
  Ranger and Priest controls die at the zoo's turns (6,761 and 93,357) with
  the zoo's causes. The local binaries are built from the same source but are
  not the zoo's bytes (the Warrior's is `1e1cd6b4…`, the zoo's `5b46e909…`),
  so the match is of the key stream and messages, not of the binary.
- **Fixed runs** play the same commit with a patch (`patches/`), built the zoo's
  way (`BORG_IMPL=rust harness/build.sh`) and played with
  `harness/run.sh OUT SEED RACE CLASS 100000 menu,exact` (Elf=2, Half-Orc=6;
  Warrior=0, Priest=3, Ranger=7) and the shipped `harness/borg.txt` of that
  commit. Replaying the Ranger and the Priest a second time from a rebuilt
  gate binary gave identical key streams. The Warrior's cell used the zoo's
  settings, kept in `runs/warrior-zoo-replay/zoo-cell-user/`.
- `patches/e8b3acfd-take-off.patch`: only the take-off. That commit has no
  `Reason::fixed` for the trip, and the gate was not applied there.
- `patches/3b4924ba-take-off-and-gate.patch`: the whole change (take-off,
  trip, gate). `patches/3b4924ba-take-off-gate-inert.patch` is the same with
  the gate's test made always true, the control that separates the gate from
  the take-off.

## Elf Ranger 1088421828 (3b4924ba)

| run | what happens |
| --- | --- |
| `ranger-base` | 6,651 wears `Pair of Leather Sandals [1,+0] {??}`; the annoyance curse shows at once (`{cursed, ??}`, −10 speed, aggravate); 6,711 "prevents you teleporting"; **dies 6,761** to a giant yellow centipede, 110 game turns after putting them on |
| `ranger-take-off-and-gate` | same until 6,661 (the aggravation notice); **6,671 `# Removing cursed Pair of Leather Sandals [1,+0] {cursed, ??} (annoyance: -10 speed, aggravate)`**; alive at 100,000 (CL 5, DL 2) |

On the PR head the game is the same up to the take-off (`head-ranger`: 6,671).

## Half-Orc Priest 354395849 (3b4924ba)

| run | what happens |
| --- | --- |
| `priest-base` | 44,659 wears a found `Cloak [1,+0] {??}`; 53,364 takes it off (paralysis curse shown, old behaviour); 71,751 reads Remove Curse on the cloak in the pack, 71,761 wears it again `{??}`, 71,771 buys another scroll; **93,200 "Your Cloak prevents you teleporting"; dies 93,357** (an acolyte) |
| `priest-take-off-only` | same as the base until 53,364 (there the fixed Borg removes the cursed cloak, the base swaps the plain one on; the plain one is worn at 53,369 either way); 64,884 reads a scroll on the cloak, 64,894 wears it, 64,904 buys another; **83,138 "prevents you teleporting", 83,148 `# Removing cursed Cloak … (anti-teleportation: no teleport, no Phase Door)`**; alive at 100,000 |
| `priest-take-off-and-gate` | same as `priest-take-off-only` until 64,874, where the town plan no longer picks the scroll (shop 4 slot 3 instead of slot 8); **no Remove Curse scroll is bought or read in the whole game, and the `{??}` cloak is not worn again after 53,369**; no teleport-ban message; alive at 100,000 (CL 6, DL 3) |

The cloak is `[1,+0]`, worth 3 gold; the scroll is 100. The gate is what
spares the two scrolls and the second wearing of a cloak that still carried a
second curse (anti-teleportation was most likely on it all along; that is an
inference, the Borg learned it only at 83,138 and 93,200).

## Half-Orc Warrior 1653223723 (e8b3acfd, zoo cell settings)

| run | what happens |
| --- | --- |
| `warrior-zoo-replay` | 52,672 wears `Robe [2,+3] {??}`; 54,100 paralysis curse shown, 54,208 takes it off; 56,842 reads Remove Curse, 56,852 wears it again; 56,862 buys scrolls; **68,279 "Your Robe prevents you teleporting"; dies 68,399** to a yellow jelly (CL 6, DL 3) |
| `warrior-take-off` | the messages are line-for-line the same as the replay (apart from the wording of the 54,208 take-off note) through 68,279; **68,289 `# Removing cursed Robe [2,+3] {cursed} (anti-teleportation: no teleport, no Phase Door)`**; alive at 100,000 (CL 7, DL 3) |

The gate was not applied to this game: whether it would have declined the
scroll on `Robe [2,+3]` at 56,842 is not tested here.

## The PR head on the same starts (shipped settings, main `88d98537` plus the change)

`head-ranger` and `head-priest` take the same actions as the fixed runs above
(sandals off at 6,671; cloak off at 53,364) and are alive at 100,000. The
Warrior start (`head-warrior`) never meets a curse on the head (main has moved
since `e8b3acfd`), so it shows nothing about this case.

## Not shown

- **The trip for Remove Curse** ("restock remove curse") was not seen in any
  game: no run kept a worn item with a mild known curse and enough gold.
  `start-build` rejects curses, so the scenario cannot be built with the
  harness. Its decision is unit-tested in the PR.
- **Survival**: nothing here estimates it. Three starts, one seed each.
- A fix at the old commits is not the PR; the PR head's `head-*` runs are the
  PR's own games.

## Reproduce

For the controls, `repro.sh` of borg-reborn-rs#830 (clones, builds the commit,
downloads the zoo bundle, replays, checks `play_sha256`). For a fixed run,
check out the commit in a clean tree, `git apply` the patch, build, run as
above. Sandals, cloak and robe lines are in each run's `excerpt.txt`; the full
`messages.log` and `keys.log` are gzipped beside it.
