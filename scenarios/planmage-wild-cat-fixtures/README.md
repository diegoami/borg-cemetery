# PlanMage wild-cat checkpoint fixtures

- `checkpoints.zip`: the original archive. It holds the game saves, `borg.txt`
  and `errands_plan.txt` exactly as the recorded game used them, in
  loop-levels form. It is immutable evidence of what was played.
- `checkpoints-max-depth.zip` (borg-reborn-rs #440, 2026-11-16): derived from
  it. The saves and `borg.txt` are byte-identical, and `errands_plan.txt` is
  rewritten `loop-levels A B` -> `max-depth B`, because borg-reborn-rs removed
  `loop-levels` (owner). `manifest.json` adds `derived_from` with both
  archives' and both plans' hashes. borg-reborn-rs's survival-incident
  regression uses this one.
