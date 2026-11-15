# D0002 survival analysis — explain the trap before the zero-HP decision

Analysis pass: 2026-11-15. Seed **8402**, faithful Rust source `f772eb6dcb93`.

## What is observed

At **5582**, the level-1 Druid had **0/12 HP**, **0/2 mana**, an adjacent
cutpurse, estimated danger **346**, and explicit scary-level/fleeing notes.
It attacked with a Whip; the next hit killed it at **5590**. Zero HP was a
living decision boundary here; it is not proof that no command was possible.

The earlier checkpoint is **5002**, 588 engine ticks before death. Its
inventory includes a potion later identified diagnostically as Speed. That
identity was unknown during play, and the checkpoint does not prove the item
was still held or usable at the final decision.

## Opportunity worth investigating

The strongest question is **why a fragile, mana-exhausted character entered or
remained in a lethal adjacent exchange**, and whether an earlier retreat was
legal. The final attack alone cannot explain resource spending, first monster
knowledge, pursuit, or the point at which an escape route was lost.

This could be encounter selection, mana budgeting, late flight admission or
an inherited tactical branch that chooses attack before later recovery. It
could also be a situation with no reliable rescue by the last decision. The
evidence does not establish a particular rejected escape, a guaranteed safe
step, or a missing known Speed-potion action.

## Discriminating experiment

Reconstruct from birth, preserving the original prefix, and identify the first
cutpurse observation. At each meaningful decision, log HP/mana, known inventory,
legal movement, flight intent and the selected/rejected response reasons.
Separate an early encounter-admission/mana-reserve change from an emergency
action change. Test the last decision only after proving its actual choices.

Candidate behaviour: leave a melee exchange before mana and movement options
are exhausted when predicted retaliation exceeds the character's recoverable
margin. The numerical margin is a hypothesis to calibrate, not a value inferred
from this single death. Do not require mana to be held forever: failing to
spend it can itself be lethal or prevent progress.

Score survival and progress alongside mana and emergency-item spending. Include
low-mana fights the original character wins. An unidentified-item experiment
must use only the labels/knowledge available to the actor, retaining harmful
outcomes as well as lucky ones.

Evidence: [original report and final messages](report.md),
[earlier inventory](inventory.md). C/Rust parity was observed in the original
cohort; no isolated translation fault or new rescue is demonstrated here.
