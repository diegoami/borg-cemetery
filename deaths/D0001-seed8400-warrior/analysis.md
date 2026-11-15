# D0001 survival analysis — preparation before the terminal fight

Analysis pass: 2026-11-15. Seed **8400**, faithful Rust source `f772eb6dcb93`.
This adds an investigation plan beside the [original report](report.md), not
a new replay or accepted strategy change.

## Sequence that matters

The critical interval is longer than a last-second death window. The Warrior
read known Deep Descent at **35460**. By checkpoint **37004**, it was at depth
13 without Phase Door stock. At **37064**, reading an unidentified scroll
caused blindness. At **37678**, it had **25/113 HP**, estimated danger **52**,
and attacked a pseudo-dragon believed to have **184 HP**. Light breath killed
it at **37680**. Its final attack was not close to a known one-hit finish.

## Best-supported opportunity

Investigate **descent permission as a joint resource/status commitment**, not
only an HP threshold or the final attack. A planned descent consumes access to
the previous refuge and can move the character into a depth where its current
escape reserve is insufficient. Later blindness also changes the usable action
set. A cure/escape that cannot be read while blind must not remain a nominal
reserve in the decision model.

The data supports the ordering of these events, not a finding that refusing
Deep Descent would win the run. Delaying descent can waste time, food or light;
the old level may itself be dangerous. The unknown scroll must remain unknown
at decision time. A rule that magically recognizes “Darkness” is invalid.

## Concrete experiments

1. Reproduce the original birth through the known Deep Descent decision. Record
   current depth target, known carried escapes/cures, legal exits and the exact
   descent-admission reason. Compare the unchanged arm with a declared minimum
   **usable** escape reserve before voluntary depth-changing consumption.
2. Independently test status-aware reserve valuation after blindness. Do not
   combine it with the descent change; retain cases where an unidentified item
   is the only reasonable emergency gamble.
3. Only then investigate the final damage race: compare the attack's legal
   alternatives with their failure/delay branches. A checkpoint at 37004 is
   676 engine ticks before death, not the exact final private Borg state.

No numeric tuning range is justified yet: the relevant original gate and its
actual inputs must be identified at this source. Do not reuse reborn's newer
profile keys in this faithful-port build.

## Acceptance and limits

Measure survival to a common horizon, depth/progress, escape spending and time
lost. Include other seeds where Deep Descent is useful. Reject the proposal if
it only replaces this death with stagnation or creates more losses in controls.
The original two C repeats and matching Rust run are one starting condition;
they neither prove a Rust defect nor supply three independent observations.

Evidence: [original sequence and terminal messages](report.md),
[checkpoint inventory](inventory.md), [build/rerun instructions](REPLAY.md).
No new counterfactual was executed in this pass.
