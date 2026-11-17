# Delivery

The owner expects completed, authorized changes to be committed and pushed.
After appropriate checks, commit the task's changes and push the working branch
without asking again. Do not stop with local-only changes unless the owner
explicitly requests that, or a concrete blocker prevents delivery. Report the
commit and push result, including any blocker. Preserve unrelated work.

# Death identity rule

New death dossiers use `D-<full SHA-256>` from the versioned encounter-family
and original key-stream identity in `scripts/native/death_identity.py`. Never
allocate sequential death numbers or reserve number ranges per branch. The
same evidence must receive the same ID across branches and independent
registries. Different continuations remain separate results of their original
life, not independent samples.

Historical numbers and paths are aliases, not canonical identities. Preserve
published evidence bytes and hashes; assign retroactive IDs in additive
`death-id.json` files. Run `python3 scripts/death_ids.py` after importing
historical evidence and `python3 scripts/death_ids.py --check` before delivery.
See `docs/death-identity.md` for the contract and alias resolution.

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

# Death reproduction and fast scenarios (owner, 2026-11-16)

Retain every natural death regardless of class or level, including early caster
deaths. A requested character-build capture level is only a projection diagnostic,
never a death-collection filter. Preserve source/build, game data, seed,
race/class, complete configuration, lineage and expected outcome/stream hashes.
For deterministic birth runs, a verified seed/build/configuration reproduction
recipe is sufficient; recorder capture is not required. Mark reproduction as
verified only after the endpoint and key/state/message streams match.

Prepare encounter starts separately from routine testing. Prefer when the
eventual killer or near-lethal threat first becomes observable, with a nearby
earlier checkpoint; for invisible enemies use first observable contact. Do not
select only the last desperate action. Fast suites load those states into an
already-built Borg with short bounded horizons. Declare fresh-Borg memory and
saved engine RNG semantics, missing state, incompatibility and all failures.

# Canonical gameplay evidence ownership (owner, 2026-11-16)

Latest owner clarification: Cemetery owns saves, scenarios, run/continuation
records, intermediate checkpoints and canonical investigation evidence. Zoo
owns aggregation, comparison reports and report presentation. Design the
shared database/artifact contract in Cemetery first (Cemetery #32, coordinated
with Zoo #114). Support both Zoo execution of pinned Cemetery inputs and
Cemetery saved-scenario execution locally or optionally in Cemetery CI; Zoo
ingests immutable result snapshots from either mode (#144). Keep one
authoritative save store with private execution copies. Historical reports
remain preserved. See `docs/cemetery-redesign.md` for the recorded direction.

This repository is the canonical home for gameplay incident reports, death
investigations, reusable scenarios and behavioral/counterfactual trial results.
Author and publish those here, including validation incidents; source repos
keep implementation, tests, fixture references and short validation summaries.
Player-cemetery holds original human/mixed recordings and working play/save
state, with links to cases here rather than duplicate incident reports.
Preserve source/build/parent-lineage identities and immutable raw evidence.
Label constructed scenarios and fresh-Borg restarts; never count replay or
alternative continuations of one life as independent samples. Historical
public exports retain their hashes; use pointers for misplaced current pages.
