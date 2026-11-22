# A Ranger and a Rogue sell their first spellbook at CL1 (borg-reborn-rs#1004)

Built from borg-reborn-rs `task/1004-ranger-first-book`, commit
[`7b83dd11`](https://github.com/diegoami/borg-reborn-rs/commit/7b83dd11cffb878dc7a85a05bdcb3cd8fd4a6cad):
track-p `6bc4de1d` plus `town_book_lookahead_levels`, compiled and shipped at 0. Core: borg-rs. Settings: the
shipped `harness/borg.txt` plus the zoo arm `reborn-head-shipped` overrides (`tools/run.sh`). Each
`arms/*/borg.txt` is the file the run used.

**One start per row.** Each row shows what one game did, not a rate. The setting's value is a hypothesis
until borg-zoo measures it.

## Cause (code and engine)
- The town planner supplies a class book only while one of its spells is castable now: `slevel` at most
  the level and `smana` at most the max SP (`borg_town_capability.rs`).
- The Ranger's first spell is Remove Hunger at level 3 (`class.txt`, `magic:3`). The Rogue's is Detect
  Monsters at level 5 (`magic:5`).
- At CL1 both books are worth nothing, and the first town visit sells them for no gold
  (`birth_no_selling`).
- The seven other classes have a level-1 spell in their first book.

## Runs (`summary.tsv`)
- **def, at 0 (today):**
  - The named start 1895660873, from borg-reborn-rs#985, sells Lesser Charms at turn 221 and dies of
    poison at 16670. This is the zoo's game, `31c994254ecdb188`.
  - Seeds 11, 22 and 33, Rogue (class 6) and Ranger (class 7): all six sell their first book on the first
    visit, at turns 161–411.
  - In 3,000-turn runs of the same seeds, the seven other classes never do (0 of 21).
- **la4, `town_book_lookahead_levels = 4`** (the Rogue's gap):
  - No start sells its first book early.
  - The sales left are duplicate copies ("Books of ...") and other classes' books found in the dungeon,
    the earliest at turn 41,931.
  - 1895660873 plays differently from its first town visit and reaches the 100,000-turn cap at CL7.

## Not shown
- The death rate. The changed game of 1895660873 is one start: the switch keeps the book, which changes
  every later event.
