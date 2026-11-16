# Narrow replacements after the owner-requested rollback

The owner rejected the combined behavior changes in#355. Source rollback
PR379 restores pre355 runtime input hash87717140. These trials evaluate
separate minimal proposals and do not accept any zoo result or population claim.
All four saved positions are alternative branches of the same recorded life,
with engine RNG restored and fresh Borg memory. The immutable source fixture
hashes remain in the scenario manifests; launchers use private save copies.

## Healing: one outer gate removed

Source499965f3 changes only the fleeing eligibility condition in borg_caution:
existing healing now runs even when danger reaches current HP. Wound/level
limits, chance gates, tiers, resource ordering and the CCW helper are unchanged.
The four rollback controls die; all four candidate starts survive the bounded
2000-engine-turn horizon at26/26HP. Borg turn batches may overshoot the cap.
At411668, the first action is `q c` (CLW): HP rises4→19 after the cat responds.
It drinks additional cures while fighting through using unchanged attack policy.
This is not a guarantee of surviving longer games.

The native regression also lowers the existing CLW/CSW maximum-level and
maximum-loss parameters so these ordinary tiers cannot apply at the opening.
The opening CLW disappears and the character dies. Later status-cure paths
retain their original policy and can have different terminal causes.

A first manual tier-control attempt accidentally copied a previously played
working save (loaded411898 rather than411668). It is retained under
`heal-411668-disabled-tiers` as an invalid setup, excluded from comparisons.
The corrected `fresh-input` attempt reloads the immutable411668 fixture and dies.
The committed native test checks loaded_turn and uses a new archive copy each time.

## Phase Door: remove one spell suppression

Sourcece3b66f0 removes only the rule that sets physical PHASE weight tozero
when the spell is learned. Existing weights and affordability constraints apply.
A native town save at407718 matches original command-frame26394's world hash.
The one-shopping-round counterfactual disables only automatic plan selection,
leaving recorded shopping settings intact. Control buys no Phase Door; candidate
buys and retains one for15gold. Both stop normally in town. The native fixture
is `scenarios/planmage-town-phase-407718/fixture.zip`.

## Magic Missile and oil remain investigations

Read-only observation of the original whole-stream verified replay gives melee25
versus normal Magic Missile17 at411668. Magic Missile was available. Melee adds
two-turn full danger while bolt scoring adds one-turn partial danger; this is a
source-supported explanation of the preference, not a measured component breakdown.
No attack default was changed in either narrow proposal.

The town snapshot shows two oil flasks at the General Store and ten at Home;
it assigns2500 milli-damage attack supply per flask. Thus these flasks were
available and oil was not zeroed merely because this was a Mage. The current
planner still left them behind. Why it preferred that kit, whether its oil
utility/throw damage is correct and how the separate Home-loop defect#368
interacts remain separate investigations. No mandatory oil quota was added.

## Scope and retained evidence

`narrow-fix-trials/results.json` records exact build/source identities and outcomes.
`native-trials.zip` retains trial traces, messages, settings and failed setup.
Unchanged raw parent recordings remain in player-cemetery. No dossier payload
belongs in either source-policy PR. Zoo comparison remains paused for the owner
to inspect the small changes.
