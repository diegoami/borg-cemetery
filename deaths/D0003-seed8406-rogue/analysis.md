# D0003 survival analysis — uncertainty and an emergency that acts too slowly

Analysis pass: 2026-11-15. Seed **8406**, faithful Rust source `f772eb6dcb93`.

## Observed terminal sequence

At **5596**, the Rogue had **1/11 HP**, a rock lizard and giant yellow
centipede adjacent, and a logged surrounding assessment of **2 monsters / 0
safe grids**. It read an unidentified scroll. The air began to swirl and the
scroll was revealed as Deep Descent; a level gain occurred, but the lizard
and centipede bit before any escape. Death was at **5600**.

## Improvement hypothesis

The terminal item did not produce an immediate separation from the attackers.
The useful design question is **how to value uncertain emergency actions and
when to prevent the surrounding state**, not how to retroactively ban the
hidden kind that this scroll happened to have.

At one HP, every time-consuming alternative may already have a poor outcome.
The chosen gamble might still dominate doing nothing. An analysis that says
“use a better scroll” without establishing one was known, present and readable
would not be an actionable improvement.

## Proposed tests

1. Reconstruct the earlier approach, first knowledge of both threats and the
   last genuinely available escape route. Test earlier anti-surrounding or
   corridor-selection behaviour separately from terminal item use.
2. At the same knowledge state, enumerate legal attacks, movements, known
   resources and unidentified-item choices. Score **whether the effect happens
   before retaliation**, not only its nominal category as an escape.
3. Evaluate any generic unknown-consumable policy on multiple frozen cases.
   It must not read true item kinds, seed-specific future outcomes or diagnostic
   postmortem reveal. Include harmful blind/confused outcomes and situations
   where an unknown-item gamble is the only chance.

No existing profile parameter has been established for this original rule.
This is first a knowledge/timing instrumentation proposal; a policy threshold
comes only after the actual action set and timing are reproduced.

Evidence: [original final events](report.md), [checkpoint inventory](inventory.md).
The retained checkpoint is 5002, not the private state at 5596. No alternative
action or counterfactual survival was run in this pass.
