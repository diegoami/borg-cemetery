# D0005 survival analysis — admission, reliability and route feasibility

Analysis pass: 2026-11-15. Seed **1532917772**, faithful Rust source
`9881301ceaad`. The [qualified earlier assessment](overall-assessment.md)
already establishes the trajectory and several mechanisms. This pass uses it
and prioritizes experiments; it does not pretend to have collected a new life
or rediscovered its findings independently.

## The decision sequence

The level-2 Necromancer entered D1 at **36014** with **15 HP / 4 mana**, met
Fang at **36094**, and tried two Nether Bolts before using its final Phase
Door **scroll** at **36114**. The landing separated it from the nearby upstairs
by walls. Actual stair-flow and retreat attempts followed; this was not a case
of simply never attempting to run. Fang reappeared, the character took further
retreats, then returned to the final pocket and fought. It died at **36289**.

One known Cure Light Wounds stayed in the pack. A NW step from the final
position was legal and had been traversed earlier. A **complete safe route to
the upstairs is not established**. The tail includes four Nether Bolt attempts
(one hit, three failures), retreats and five melees, not uninterrupted spell spam.

## Three separate opportunities

1. **Recovery admission and priority.** The original caution/recovery ordering
   can exclude ordinary recovery while fleeing and allow attack selection to
   return before later recovery. An unused known potion makes this worth
   tracing; it does not prove that the actual healing branch was legal or that
   one heal would escape Fang. Record the carried-cure counter, current flight
   flags, danger and rejection reason before forcing a quaff experiment.
2. **Reliable native spell confidence.** Qualified observations show Nether
   Bolt cost 1 mana and **36% native failure** while affordable, versus an
   **11% terminal Borg estimate**. The historical ambient-light difference is
   source-supported. However, that terminal estimate is not a simultaneous
   private trace at every cast, and the unique-fight gate can still admit a
   36%-failure spell. Three failures do not themselves prove a bug or that a
   more cautious estimate saves this life.
3. **A route the actor can actually execute.** Phase evaluated immediate
   landing danger, not confirmed connectivity to the stair. Legal NW movement
   is a candidate branch, not a safe-route certificate. Inspect known terrain,
   faster-foe exclusion, local danger and actual stair-flow rejection together.

## Concrete intervention tests

Use the exact historical source/origin. First qualify a read-only private-gate
trace. Then compare **one** legal cure or NW step at a named boundary, separately
from a spell-estimate correction and separately from any earlier Phase timing
change. Retain the following enemy response and the subsequent route; being
alive immediately after quaffing is not a rescue.

For native-failure consistency, assert simultaneous native/Borg values under
lit/unlit controls and with/without carried light, then rerun unchanged play.
A changed estimate may favor melee sooner and worsen the outcome. Test that
possibility rather than declaring lower spell confidence automatically safer.

There was no spare money or sale stock at the earlier town departure. “Buy more
escapes” is therefore not a free one-line alternative for this life. No learned
healing or teleport prayer was available, and Recall was at Home, not carried.

## Ownership and status

The existing historical [Rust investigation #4](https://github.com/diegoami/borg-rs/issues/4)
and its linked native/C leads already cover these questions. This pass neither
duplicates them nor applies a shared-source correction. No new tactical branch
or healing rescue was executed here. Use [recording playback](REPLAY.md) and the
[decision timeline](overall-assessment.md#decision-timeline) to inspect the
observations, then qualify the exact private decision before attributing cause.
