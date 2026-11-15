# Survival analysis of the retained deaths — 2026-11-15

This is an analyst pass over **seven selected deaths**, not an automated causal
analysis job or a survival-rate study. Repeated replays, S0003 version/parameter/human
continuations and overlapping windows are not new independent births.
Original reports, observations and capture metadata are preserved. Each case
below has a written analysis with evidence, alternatives, a proposed experiment
and an explicit limit on the conclusion.

## Most useful findings

| Priority for investigation | Finding | Evidence strength | Next discriminating work |
| --- | --- | --- | --- |
| 1 | [D0006: retreat is undone by exploration using exceptional-mode cached safety](../deaths/D0006-recorded/analysis.md) | Qualified private control-flow trace; the oscillation and absence of attack selection are observed | Separate cache-validity and persistent-intent fixtures, preserving emergency escape and ordinary safe exploration controls |
| 1 | [D0007: a live tactical goal selects arbitrary zero-value movement before the first bite](../deaths/D0007/analysis.md) | Original decision trace and exact source; the human route demonstrates that exposure is avoidable from the retained position | Test tactical-goal termination/no-gain handling from original birth or a private-state fixture; a loaded save resets that goal |
| 1 | [D0007: spell-versus-heal scoring rewards fractional threat removal rather than the actual next-turn outcome](../deaths/D0007/analysis.md) | Recorded scores reproduced numerically from pinned source; a cast cannot kill the observed 16-HP Fang with 3d4, but can induce fear | Model failure, kill/fear outcomes and post-heal danger explicitly; compare isolated actions before claiming a rescue |
| 1 | [D0007: walking gets an additional “free hit” term that needs engine calibration](../deaths/D0007/analysis.md) | Direct source discrepancy question; native movement and monster energy processing inspected | Same-speed/fast/stationary-monster energy-phase fixtures; establish whether pursuit is counted twice before changing it |
| 2 | [D0004: finishing a nearly dead enemy is not a guaranteed safe action](../deaths/D0004-seed8408-blackguard/analysis.md) | Actual miss followed by death; known cure stock at an earlier checkpoint | Confirm final stock and compare healing against the miss branch; avoid a universal never-finish rule |
| 2 | [D0007: interrupted recovery spends the temporary separation without restoring much HP](../deaths/D0007/analysis.md) | Actual rests, positions and HP before Fang catches up again | Test longer threat horizons and time-to-recovery versus time-to-contact; rest duration also changes the goal budget |
| 2 | [D0001: loss was being arranged long before the final attack](../deaths/D0001-seed8400-warrior/analysis.md) | Known Deep Descent, later blindness, missing escape stock and a terminal mismatch | Fresh-birth descent/preparation arms starting before turn 35460; a last-second save cannot test the earlier policy |
| 2 | [D0006: healing stock was sold while fuel stock accumulated](../deaths/D0006-recorded/analysis.md) | Actual item transitions, not a guessed full-pack explanation | Trace shop/inventory valuation, then test a low-level cure reserve with economic/progress controls |
| 2 | [D0005: recovery admission and native spell confidence warrant different experiments](../deaths/D0005-recorded/analysis.md) | Known unused cure, legal first retreat step and qualified native observations; private gates incomplete | Gate trace, isolated cure/step tests and simultaneous native/Borg failure estimates; reuse the existing investigation |
| 3 | [D0002: the terminal decision is too late to explain how a fragile caster became trapped](../deaths/D0002-seed8402-druid/analysis.md) | Actual zero-HP/zero-mana decision; earlier inventory only | Reconstruct first cutpurse knowledge, mana spending and retreat opportunities; do not prescribe a potion by its hidden identity |
| 3 | [D0003: unknown-scroll policy should be evaluated under uncertainty](../deaths/D0003-seed8406-rogue/analysis.md) | Actual emergency reading and delayed effect; unseen scroll identity was unavailable | Compare legal alternatives at the same knowledge state and earlier anti-surrounding choices; do not ban one scroll retrospectively |

Priority means value of the next investigation, not a confirmed-bug severity.
The recurring themes were discovered from these trajectories; they are not an
exhaustive checklist. Similar symptoms in the faithful Rust port and the
redesigned reborn Borg do not establish a shared implementation defect.

## What has actually been demonstrated

- D0006's repeated doorway/stair cycle and the relevant private branches are
  observed on qualified historical replay. No successful minimal correction has
  been demonstrated by this analysis pass.
- D0007's recorded human continuation stays alive to 4873 with 15/15 HP, beyond
  the original death at 3640, with the exact source save captured, no Borg input
  and successful recorder verification. Fang never becomes visible in that
  continuation. This demonstrates an avoidable fatal encounter from that saved
  position, not victory in a forced direct fight or an isolated policy benefit.
- The retained alternative borg-rs version also survives its S0003 horizon.
  Its complete build differs; that result does not identify which mechanism
  made the difference.
- Original D0001–D0004 C/Rust matching traces support investigating shared
  inherited decision rules. Matching alone is not evidence that a decision was
  correct, or that an alleged translation bug exists.

## Proposed bounded parameter experiment

[D0007's five frozen profiles and protocol](../deaths/D0007/analysis-profiles/README.md)
prepare an unchanged control, threat horizons 2 and 3, risk aversion 75, and
rest duration 1, changing one existing parameter per arm. These are diagnostic
values, not recommended defaults. In particular, higher risk aversion can
increase the score credit for damaging a dangerous enemy; it need not prefer
healing. Rest duration also controls Recover's stall budget.

The first attempt respected an occupied native lane; once it became free,
all five arms completed. [Results and retained evidence](../deaths/D0007/analysis-results/README.md):
horizon 2 survived the cap; horizon 3 died; risk aversion 75 reproduced the
control's death. Rest duration 1 also survived, **with a refused-action violation
that cooled recovery and changed the path**. That is not a clean improved-rest
result. Both surviving branches resumed exploration but remained level 1/DL1.
This non-monotonic result is why neither a generic “more cautious” setting nor
survival alone should determine the recommendation.

The strongest model/state-machine proposals still require upstream implementation
or instrumentation, not an invented configuration key. No policy is adopted.

## Validation and rollout

For each candidate, keep unchanged replay, failed outcomes and progress costs.
Use a shared saved start for restart-based comparisons and a qualified original
prefix when testing historical private-state decisions. Then validate from
birth on frozen held-out seeds, including encounters the original policy wins.
Retain resource use, timeouts, stalls and newly introduced deaths. Do not pool
overlapping windows or optimize only these selected losses.

This pass changes no Borg policy, default backend or source pin. It files no
automatic upstream issues and does not duplicate the historical Rust #4/#5 or
their linked C leads. Source ownership and milestone acceptance still apply.

## Case reports

[D0001](../deaths/D0001-seed8400-warrior/analysis.md) ·
[D0002](../deaths/D0002-seed8402-druid/analysis.md) ·
[D0003](../deaths/D0003-seed8406-rogue/analysis.md) ·
[D0004](../deaths/D0004-seed8408-blackguard/analysis.md) ·
[D0005](../deaths/D0005-recorded/analysis.md) ·
[D0006](../deaths/D0006-recorded/analysis.md) ·
[D0007](../deaths/D0007/analysis.md).
