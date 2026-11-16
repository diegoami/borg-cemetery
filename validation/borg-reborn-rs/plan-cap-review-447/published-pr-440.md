## What changed
The owner asked, on 2026-11-16, for a phase to be "an additional check, not a forced behaviour", and for the loop errand to be removed entirely.

- **New plan command `max-depth N`** (`borg-core/src/errands_plan.rs`), now the only phase command.
  - The phase installs no errand: the core plays as itself, with its own dives, town trips, shopping and recovery.
  - It is never prepared for a level below DL N. The phase sets `borg_no_deeper` to N+1, never above the configured value.
  - N is 1–126; anything else exits 2.
- **The level-loop errand is removed** (`borg-core/src/shell.rs`).
  - Gone: `/loop-levels`, the loop route, its town restart, and #421's hold.
  - A plan using `loop-levels` exits 2 with "loop-levels was removed; use max-depth N".
  - Gone with it: `test_loop_levels.py`, `test_loop_livelock.py` and their fixture. #421 can't recur, because nothing forces a route any more.
- **Both shipped plans are rewritten**, `loop-levels A B` → `max-depth B`:
  - `errands_plan.txt` `084bc3e8999697bd8edf7fd302ea75d65b50ef2714afdd3a47354a1f24137e87`
  - `errands_plan_ambitious.txt` `c301858598cbb76d529fd49ef6c0c1c75332e4f229785e62459e46b986c6e0c9`
- **The wild-cat survival regression** uses a new derived archive, borg-cemetery `scenarios/planmage-wild-cat-fixtures/checkpoints-max-depth.zip` (sha256 `8b1ad205…`). Its saves and `borg.txt` are byte-identical to the recording, and its plan is capped. The original archive stays as the record of what was played.
- **CI evidence:** borg-cemetery `77dd467e` (PR borg-cemetery#29) holds the CI death controls for source `ef85f725…` and the derived archive.
- **Docs:** `GAME-PLAN-LANGUAGE.md`, `ERRANDS.md`, `harness/plans/README.md`, `ZOO-INTERFACE.md` (RULES 7), handover.
- **Accepted by the owner:** the core's own cap lets a "spent too long on level, leaving" move step onto the level below for one move; it climbs straight back.

Source hash: `6b3b9e99…` → `ef85f725b5d26b22e7b4ea8f318e99d031442241c399d6d938c564c390ef1f9b`. `harness/borg.txt` is unchanged.

## How it was checked
**90 `classes-1800-small` starts**, using the zoo adapter's borg.txt, town planner on, 100k turns. Descriptive only.

| arm | deaths | caster deaths | stalls | mean CL | mean DL | time in town |
|---|---|---|---|---|---|---|
| town (no plan) | 17 | 5 | 0 | 4.91 | 2.62 | 30.2% |
| plan, max-depth | 15 | 5 | 0 | 4.83 | 2.32 | 31.7% |
| plan, max-depth + trip policy | 14 | 4 | 0 | 4.81 | 2.29 | 32.2% |
| ambitious, max-depth | 17 | 5 | 0 | 4.89 | 2.60 | 30.9% |
| plan, old loop-levels (before removal) | 20 | 12 | 0 | 4.27 | 2.22 | 33.8% |

**Other checks:**
- Removing the loop code doesn't change capped play: 6 cells are byte-identical to the table's runs.
- Release core tests 325 (8 loop-only tests removed, one cap-restore test added); workspace tests 156; engine tests 84 pass (15 skipped).
- fmt and clippy pass; `import-deaths --check` passes; all CI deaths reconcile locally.
- Both survival-incident tests pass on the derived archive.

**Needs review before merge.** It changes what a plan means and removes an errand. It was written by Claude Opus 5.5, so the owner picks the reviewer.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
