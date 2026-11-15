# D0007 survival analysis — where the decision model can improve

Analysis pass: 2026-11-15. Original seed **102**, reborn source
`e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71`. This analysis uses the retained
[written sequence](../../scenarios/S0003/report.md), actual decision candidates,
[parameters](PARAMETERS.md), exact source and the qualified recorder diagnostic.
It proposes tests; no new default or upstream gameplay change is applied.

## Finding 1: tactical goal persistence is choosing travel with no tactical value

At **3402 and 3432**, Engage stays active because “a live goal keeps its mode.”
Its goal began at **3272**, last progressed at **3362**, and its candidate
movements and Hold all score **zero**. The tie selects southwest. The history
includes repeated lock-picking and then entry into Fang's reach; the first
bite is **3440**. This is an earlier opportunity than the final failed spell.

The pinned strategy gives Engage a stall budget of one tenth of
`explore_budget_turns`: **200 game turns** with the actual value 2000. Seventy
turns without progress therefore do not retire the tactical goal at 3432.
This is source-consistent behaviour, not a claim that a guard malfunctioned.

**Proposal:** explicitly replan or retire a tactical goal when no current
tactical gain remains, rather than letting deterministic zero-score movement
act as a travel policy. Do not simply make Hold win every tie: that could
replace the encounter with a stall. Preserve deliberate pursuit when justified
and pass travel decisions back to the appropriate planner when not.

**Test:** replay from birth or construct the private goal state, including
start/progress times and remembered enemies. A loaded S0003 save resets this
memory and cannot alone prove the effect on the original goal. Test a stalled
phantom fight, a legitimate pursuit and a fleeing live enemy. An existing
`explore_budget_turns` sweep would also alter exploration, so it is not an
isolated tactical-budget experiment.

## Finding 2: the terminal scores explain the spell choice, but not its survival value

| Decision | Character state | Selected score | Cure score | Observation |
| --- | --- | --- | --- | --- |
| 3612 | 6/9 HP, 2 mana | Magic Missile −3.5483 | −4.3313 | Spell chosen; it hits Fang |
| 3622 | 0/9 HP, 1 mana | Cure +1.6688 | Selected | Potion restores HP; subsequent bites leave 4 HP |
| 3632 | 4/9 HP, 1 mana | Magic Missile −1.4204 | −2.3313 | Spell chosen, concentration fails, then death |

At 3632 Fang has **16 HP** in the qualified diagnostic recording. The learned
spell is **3d4**, native failure **14%**: at most 12 damage, so this cast cannot
kill Fang immediately. The code does already discount expected spell damage
for failure: 7.5 × 0.86 = **6.45**. “Failure chance was ignored” would be an
incorrect diagnosis.

The scoring then treats expected damage divided by target HP as fractional
threat removed. With the actual composite risk **7.33125**, its credited share
is 6.45/16 = **0.403125**. Twice the credited gain minus current risk reproduces
the recorded spell score **−1.4204297**. A cure restores the missing 5 HP and
scores 5 − 7.33125 = **−2.33125**. The spell wins by approximately **0.911**.

**Proposal:** evaluate candidate outcome branches, including post-heal HP,
failure retaliation, kill probability and morale/status effects. Losing HP
does not linearly reduce an ordinary melee monster's bite damage. However,
nonlethal damage **can induce fear** in this engine, and Fang is not fear-immune.
Thus “cannot kill” does not imply zero possible defensive benefit. The model
must assess that effect rather than either awarding a generic fraction of all
threat or removing all offensive benefit by assumption.

**Test:** at a qualified common boundary, compare the original spell, one cure
and legal movement; retain next monster actions and the subsequent continuation.
Also use a fear-immune enemy, a killable target, and a target whose breath scales
with HP. Do not replace the model with a universal potion-first rule. There is
no existing knob that directly repairs this action-outcome semantics.

## Finding 3: walking has an extra risk term needing native validation

The response ladder assesses danger at the destination **and adds one melee
round** from a mobile adjacent enemy when leaving its reach. Its comment calls
that an engine “attack of opportunity.” In the inspected native engine, legal
empty-grid movement swaps the player and spends movement energy; monster attacks
are scheduled by the normal energy loop. No independent leave-reach attack is
present in that movement path. The destination threat model already subtracts
the approach distance from monster action slots.

This is a concrete **model-consistency concern**, not yet a proven arithmetic
double-count in every energy phase. A faster Fang can legitimately move and
attack during one player action. Removing all pursuit risk would also be wrong.
But the concern fits the recorded late movement scores of **−7.33125** when
the ladder instead prefers attacking or healing.

**Test first:** legal retreat fixtures at equal speed and at Fang's speed,
with different current energy phases and a stationary-monster control. Count
actual moves/blows over the same horizon and compare destination-plus-extra
prediction. If the additional round has no native counterpart, remove or
replace that term upstream and re-evaluate all responses. This is a behaviour/
model correction proposal, not a made-up profile key.

## Finding 4: recovery spends temporary separation without securing recovery

After Phase at **3442**, the Borg rests at (76,8) from **3452**, still 5 HP.
It retreats briefly at 3502, re-enters contact and spends its last Phase at
**3532**. Recovery at (84,6) begins at **3542**; by **3602** it is still 5 HP
while the model sees Fang approaching. It reaches only 6 HP before renewed
contact at 3612. Requested `Rest(75)` is not evidence that 75 uninterrupted
player turns elapsed: disturbance breaks the rest.

**Proposal:** compare expected recovery benefit and pursuer arrival time, and
preserve a post-escape recovery/exit intent. The one-player-turn threat horizon
can label short separation safe while not answering whether it lasts long
enough to recover. Goal hysteresis and later contact make this more than a
single rest-duration constant.

[The prepared profiles](analysis-profiles/README.md) test horizons 2/3, risk
aversion 75 and rest duration 1 against the actual baseline. They are not
recommended defaults. Higher risk aversion can actually favor damaging a
dangerous enemy: it also increases the threat-removal credit above. At the
3632 values, the same formula gives an even larger spell-over-cure margin at
75 than at 50. Rest duration also changes Recover's stall budget (twice that
parameter), so a rest-1 result would not isolate command duration alone.

## What the successful alternatives establish

The human continuation is alive at **4873**, level 2, **15/15 HP**, with no
Borg inputs and a verified recording bound to the original save. Fang is never
recorded as visible. The state at **3402** is therefore not an unavoidable
death under that recorded continuation. It supports investigating encounter
selection and movement, not a claim that an adjacent fight was won.

The alternative borg-rs build survives to **4411**. That compares complete
versions. Neither result isolates one proposed model or parameter correction.
No general policy improvement follows from these selected alternatives.

## Evidence and exact source

- Decision trace entries 351/353/354/355/360/363/364/370–373 are retained in the
  scenario's chronology. [Readable original sequence](../../scenarios/S0003/report.md).
- [Pinned tactical scoring](https://github.com/diegoami/borg-reborn-rs/blob/e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71/borg-reborn-rs/src/tactics.rs#L270):
  damage share, destination/extra movement risk and cure scoring.
- [Pinned strategy](https://github.com/diegoami/borg-reborn-rs/blob/e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71/borg-reborn-rs/src/strategy.rs#L786):
  recovery and [goal budget](https://github.com/diegoami/borg-reborn-rs/blob/e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71/borg-reborn-rs/src/strategy.rs#L1079).
- [Spell expectation already includes failure](https://github.com/diegoami/borg-reborn-rs/blob/e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71/borg-reborn-rs/src/spells.rs#L154).
- Native engine `e473720`: [movement](https://github.com/angband/angband/blob/e473720ed88a0f0c7ca66815cef3000eb4a38bc3/src/cmd-cave.c#L1058),
  [monster turns](https://github.com/angband/angband/blob/e473720ed88a0f0c7ca66815cef3000eb4a38bc3/src/mon-move.c#L1630),
  [fear from damage](https://github.com/angband/angband/blob/e473720ed88a0f0c7ca66815cef3000eb4a38bc3/src/mon-util.c#L1150).
- [Qualified diagnostic observations](analysis-evidence.md) state exactly which
  channels matched and retain the deciding HP/score arithmetic in readable form.

The first attempt respected the occupied shared native lane. Once it became
free, five arms completed; [all results and evidence are retained](analysis-results/README.md).
Horizon 2 survived the cap, horizon 3 died, and risk aversion 75 reproduced the
control. Rest duration 1 survived with an explicit refused-rest violation and
immediate Recover cooldown/Explore transition at 3452. That exposes an executor/
refusal interaction, not a clean recommendation for one-turn resting. The
survivors explored at the cap but remained CL1/DL1. These are one saved starting
condition's branches; no source or default policy is changed.
