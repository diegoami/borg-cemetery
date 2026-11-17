## 2026-11-16: plan phases become depth caps (`max-depth N`)

- Owner: a phase should be an additional check, not forced behaviour.
  New plan command `max-depth N` (borg-core/src/errands_plan.rs): no
  errand; the core plays as itself and is not prepared below DL N (the
  phase sets `borg_no_deeper` to N+1, never above the configured value).
  Review of #440: hand-back at a gap and cancel now restore the configured
  value (the last cap used to persist after level 50).
- Owner: remove the loop errand entirely. `/loop-levels` and the plan
  command `loop-levels` are gone (a plan using it exits 2 with "loop-levels
  was removed; use max-depth N"), with the level-loop code in shell.rs,
  including #421's hold, test_loop_levels.py and test_loop_livelock.py.
  #421 cannot recur: nothing forces a route any more.
- Both shipped plans rewritten: `loop-levels A B` -> `max-depth B` (new
  hashes).
- The core's own cap lets a "spent too long, leaving" move step onto the
  level below for one move and climb straight back; owner: not an issue.
- Local, 90 classes-1800-small starts, town planner on, trip off:
  deaths town 17, max-depth plan 15, +trip 14, max-depth ambitious 17,
  old loop plan 20 (caster deaths 5/5/4/5/12). Descriptive only.
- CI deaths for source 2d8693c8 are retained on borg-cemetery
  `evidence/borg-reborn-rs-max-depth-ci-controls-v2`; its 77dd467e (after the review fix) also
  adds `checkpoints-max-depth.zip`, the wild-cat archive with the plan
  capped (saves and borg.txt unchanged; the original stays as evidence).

