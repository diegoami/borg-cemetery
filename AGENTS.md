# Delivery

The owner expects completed, authorized changes to be committed and pushed.
After appropriate checks, commit the task's changes and push the working branch
without asking again. Do not stop with local-only changes unless the owner
explicitly requests that, or a concrete blocker prevents delivery. Report the
commit and push result, including any blocker. Preserve unrelated work.

# Milestone reviews

Use [PLAN.md](PLAN.md) for the active milestone and review boundary. At a
milestone boundary, prepare a review PR from `main` to `reviewed`, with an
exact implementation pin, evidence, known limitations and a runnable reviewer
prompt. The owner chooses and runs the reviewer; do not select or launch one.
If a model reviews, it should be from a different family than the implementer.
Do not merge the review PR, mark the milestone accepted, create its acceptance
tag or start another milestone without the owner's acceptance/instruction.
Owner-requested fixes during preparation are included before the review freeze;
later fixes must update the review's pinned head and validation evidence.
