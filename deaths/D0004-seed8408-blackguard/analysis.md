# D0004 survival analysis — a likely kill still has a miss branch

Analysis pass: 2026-11-15. Seed **8408**, faithful Rust source `f772eb6dcb93`.

## Observations

At checkpoint **6006**, the Blackguard had **six known Cure Light Wounds
potions** and one Phase Door scroll. Phase was used at **6186** and depleted.
At **6225**, with **4/16 HP** and estimated danger **18**, the Borg attacked
a wild cat estimated at **1 HP**, using a Tulwar. It missed. Repeated claws
killed it at **6231**. No healing quaff is logged in the reported interval.

## Strongest hypothesis

The finishing attack should be compared with **its miss/failure branch**, not
treated as a certain kill because the target is nearly dead. Surviving one
miss is especially important when a faster enemy can make multiple attacks.
This is an action-outcome question, not simply “always heal at 25% HP.”

The known potion stock is from an earlier checkpoint, so final availability
must be confirmed. Even with a potion, spending the healing action allows
retaliation. The evidence does not yet demonstrate that quaffing at 6225 wins.
Conversely, the observed miss is not evidence that an attack was unreasonable
under every probability model.

## Experiment to perform

Verify the exact original prefix and final item stock, then record which
healing and attack branches are admitted. Compare one native healing attempt
with the original attack from a qualified common boundary, retaining the hit,
miss and next-monster-action results. Separate action-priority admission from
the attack value itself: changing both at once would hide which mattered.

If the scoring layer represents kills by expected damage, propose an explicit
kill-probability and failure-retaliation term. This exact source's implementation
must be inspected before selecting a tuning key; a similarly named reborn
parameter cannot be assumed to exist here.

A held-out control set should include cheap, nearly certain finishing attacks
where healing would waste stock or turns. The desired outcome is fewer fatal
misses without replacing good finishes with stalls and unnecessary drinking.

Evidence: [original sequence and miss](report.md), [inventory at 6006](inventory.md).
C and Rust reproduced the same sequence. No healing rescue is established by
this analysis pass, and no default gameplay rule is changed.
