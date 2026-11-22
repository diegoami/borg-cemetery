# Source refresh report (2026-11-21)

## angband (angband/angband)

- at pin 574b618c3bfe, nothing new
- upstream C Borg commits: all listed in `engine/upstream-borg.txt`

## borg-rs (diegoami/borg-rs)

- **7 commits** since pin 8c5d000a58e9 (head d75e17a5ae74, read on 2026-11-19)
- copy `docs` → `reference/borg-rs`: 0 added, 2 changed, 0 removed
- vendored core `borg-core/` at 8c5d000a58e9: 1 borg-rs commits since touch its files (re-vendor: `scripts/borg-core-vendor.py refresh REV`, in its own PR)
- issues updated since 2026-11-19: 2
  - #111 [open] Rust v15R diverges from C v15 only for Necromancers: 6 of 30 medium starts end differently (zoo #463
  - #110 [open] Carry two upstream C Borg fixes: 007bea95 (largest slay multiplier) and 95387b06 (landing check with

## better-borg-c (diegoami/better-borg-c)

- **201 commits** since pin 46037038cb0c (head cc4c3e43aa0a, read on 2026-11-13)
- copy `docs/deaths` → `reference/deaths/better-borg-c`: 44 added, 2 changed, 0 removed
  - **new death cases:** D0020-collected, D0021-collected, D0022-collected, D0023-collected, D0024-collected, D0025-collected, D0026-collected, D0027-collected, D0028-collected, D0029-collected, D0030-collected
  - changed registry documents: README.md, index.json
- **new tags** `4.2.6-impact-v*`: 4.2.6-impact-v10, 4.2.6-impact-v11, 4.2.6-impact-v12, 4.2.6-impact-v13, 4.2.6-impact-v14, 4.2.6-impact-v15, 4.2.6-impact-v8, 4.2.6-impact-v9, 4.2.6-impact-v9.1 (a new milestone: a new specimen for borg-zoo to consider)
- **cited C Borg functions changed:** borg-danger.c:borg_danger, borg-danger.c:borg_danger_one_kill, borg-flow-dark.c:borg_flow_dark_interesting, borg-flow-kill.c:borg_update_kill_old
- issues updated since 2026-11-13: 40
  - #547 [open] Milestone 15 review: official master 574b618c3 and three upstream retirements
  - #544 [closed] Fix observer-only reporting, listing and frontend classification after recorder retirement
  - #542 [closed] Milestone 14 review: six carries since impact v13
  - #540 [open] Adopt source629: run the dive gates whether or not an up staircase has been seen
  - #538 [closed] Adopt source593: check teleport landing zones with either kind of teleport
  - #536 [open] Adopt source174: name the electricity resistance in the resist-electricity note
  - #534 [open] Adopt source192: mark every rubble grid around the borg when the rubble is removed
  - #529 [open] Adopt source595: model Phase Door landings at the distances the game uses
  - #527 [open] Adopt source591: model Mind Blast as 8d8 damage plus confusion
  - #525 [open] Adopt source590: do not use Deep Descent as an emergency escape

## neo-angband-tracker (diegoami/neo-angband-tracker)

- **21 commits** since pin c2ddf2ca045d (head dbde80762dd4, read on 2026-11-13)
- copy `docs/c-borg` → `reference/c-borg`: 0 added, 1 changed, 0 removed
- issues updated since 2026-11-13: 47
  - #641 [closed] Adopt the exact Neo Angband 1.23.0-beta.4 release
  - #640 [open] Seed continuation: Neo birth clock starts at 0 while pinned C starts at 1
  - #637 [closed] Seed comparison: C rand_loc argument order differs from Neo coordinate draws
  - #636 [open] Neo class starting equipment retains parse order instead of C's prepended list order
  - #635 [open] Neo store/home stock insertion appends instead of C head insertion, shifting seeded maintenance
  - #630 [open] C Borg: all four 'Normal in town' fear branches are dead code (BI_CLEVEL is never 0)
  - #629 [open] C Borg: the dive gates in borg_flow_stair_more() are skipped whenever no up staircase has been seen 
  - #619 [closed] Evidence packages: borg.txt is a git error message, so fixtures ran with built-in defaults
  - #616 [open] C Borg: cold melee danger checks temporary acid resistance instead of cold
  - #615 [open] C Borg: a hurt Borg standing on a down staircase recalls instead of taking the stairs

## borg-zoo (diegoami/borg-zoo)

- problem: fetch failed, using what is already fetched (offline?): no message
- problem: cannot resolve origin/HEAD

## borg-runner (diegoami/borg-runner)

- at pin e55ac6f384f2, nothing new
- issues updated since 2026-11-13: 0

