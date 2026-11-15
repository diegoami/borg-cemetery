# D0006 survival analysis — retain the meaning of an emergency escape

Analysis pass: 2026-11-15. Seed **2647001198**, faithful Rust source
`aa4ad6cfeea2`. The [earlier qualified private-state assessment](overall-assessment.md)
is the primary evidence. The useful next work is a discriminating correction
test, not another vague request for every private field.

## Observed mechanism

The Priest was safe from the stationary grey mold's melee on a down staircase
at **(33,49)**. Opening the door and entering **(33,48)** put it diagonally
adjacent to the mold at **(34,47)**. The mold had **2 HP**, native speed 110,
and two adjacent spore blows. It could not pursue onto the stair by itself.

At doorway decisions **22784 / 22804 / 22824**, current danger **16** made
caution take an emergency south step to the stair, returning before attack
selection. At stair decisions **22794 / 22814 / 22834**, current danger was
zero and persistent flee/leave/descent flags remained false. Exploration sent
the Priest north again. The fourth exposure killed it at **22841**.

The qualified trace records the normal exploration flow reusing the doorway's
cached **known, not-danger-blocked** status after an emergency flow. This is
an observed interaction of temporary exception mode, cached safety and missing
persistent intent. It is stronger evidence than merely noticing a repeated
two-tile path, but it does not identify the one safe minimal fix by itself.

## Highest-priority correction experiment

Construct a legal small fixture that exercises **emergency → ordinary flow**.
Compare the original against a narrowly scoped cache-generation/mode-validity
change. Include three controls: emergency escape through a dangerous tile must
still work; ordinary safe exploration must remain possible; a truly blocked
route must remain blocked. Assert whether danger is recomputed when ordinary
exploration considers the previously exceptional doorway.

Test persistent escape intent separately: reaching the stair after an emergency
should not immediately mean “resume exploration into the threat.” Compare
declared hold/door-close/descent continuations. A down stair here leads to D2,
not to town; the new level may be worse. Persistent fleeing must have a release
condition so a correction does not create permanent avoidance or stair churn.

## Other useful but independent investigations

- **Combat as an alternative:** a landed 2d4 mace hit is a credible kill attempt
  against a 2-HP mold, but could miss. The observed adjacent decisions never
  reached attack selection; there is no losing attack score to “tune.” Test a
  single strike as its own branch. Do not force combat against all stationary
  monsters; floating eyes and other disable threats are separate controls.
- **Resource valuation:** two known Cure Serious Wounds were sold at **271**
  and **281**, Recall was stored at Home, and the one Phase scroll was spent
  at **14801**. Nine spare torches remained near death, with pack capacity
  available. Trace the actual shop/inventory scores before asserting that fuel
  crowded out a cure. Test a low-level cure reserve independently, including
  money/growth costs and the cases where buying fuel is essential.
- **Learning:** the Priest actually learned Detect Evil and Call Light. The
  book study selection is random for this class; a misleading “Bless” note is
  not evidence of a learned heal. Unidentified Speed was unknown during play.
  Neither a magically selected healing prayer nor a known Speed potion is a
  valid alternative under the recorded knowledge state.

## Status and acceptance

No cache/intent patch or successful alternative is executed in this pass.
Preserve the existing [Rust #5 investigation](https://github.com/diegoami/borg-rs/issues/5)
and linked shared-source ownership. A qualified saved-engine restart starts
new Borg memory; a private-cache regression should use a controlled in-process
fixture or a reproduced original prefix. Population survival/progress evidence
is required before promoting a broad tactical change.
