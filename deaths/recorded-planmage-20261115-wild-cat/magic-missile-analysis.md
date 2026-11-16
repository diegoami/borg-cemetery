# Why melee beat Magic Missile at411668

An observational debugger run of the frozen original binary reproduced the
whole original recording, with the recorder verifier returning0. It did not
change game/Borg state, RNG, settings or queued actions. The Mage has4/26HP
and2/10SP. Both candidates target the adjacent wild cat at(x131,y41).

| Component | Rapier melee | Normal Magic Missile |
| --- | ---: | ---: |
| Modeled damage entering target scoring | 1 | 7 |
| Danger bonus added by target scoring | 24 | 10 |
| Returned attack score | 25 | 17 |

The damage inputs and score returns were directly observed. The added bonuses
are the differences; source explains their origin. `melee_score` adds the
target's two-turn **full-damage** danger; `borg_launch_bolt_aux_hack` adds one-turn
**partial** danger. AtCL5 the melee partial-kill discount (only aboveCL15) does
not apply. Magic Missile received no kill multiplier here. Thus a very weak
nonlethal melee hit gets a large threat-removal bonus, and inconsistent danger
horizons/modes outweigh the spell's stronger modeled damage.

Magic Missile is not unavailable and this is not mana conservation: at this
level it is the Mage's primary spell, and `borg_attack_aux_spell_bolt` returns
its simulated score before the reserve-mana penalties. It costs1SP, with5%
recorded failure. The current score does not numerically discount that failure
(the code has an explicit TODO about failure rates). Its3d4 average is7.5;
the integer damage formula truncates it to7. That half-point truncation cannot
explain an eight-point score gap. Rapier damage1 is already after the existing
hit-chance and Mage-melee adjustments; it is a modeled value, not a guaranteed
landed point of damage.

Source at original820140e0: borg-core/src/borg_fight_attack.rs,
`borg_thrust_damage_one`319–465, `melee_score`476–503,
`borg_launch_bolt_aux_hack`1330–1442, primary/normal spell2515–2635,
and Magic Missile candidate3862. Defaults are named in params.rs:
attack_melee_danger_horizon2; attack_bolt_danger_horizon1;
attack_melee_partial_min_level15. Engine class.txt gives Magic Missile's1SP
cost and spell dice; class and object mechanics remain upstream42cd156ac.

A correction should compare attacks over the same horizon and danger mode and
examine how much future danger a nonlethal hit actually removes. Merely rewarding
an attacked dangerous target as if its damage disappeared is questionable. That
is a separate focused combat proposal; neither the Phase Door stock patch nor
the small fleeing-heal patch changes any scoring parameter or attack algorithm.
No population improvement or hypothetical survival is claimed here.

Curated raw observations, observer script and verification receipt are in
`magic-missile-components/`. Some exploratory breakpoints hit optimized/inlined
code with stale argument registers; those probes are deliberately excluded from
the curated component evidence. All retained summaries distinguish measured
returns from source-derived attribution. Source investigation issue:#391.
