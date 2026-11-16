# Spell-for-item substitution audit

Scope: receiving M13 at1443c2d1 and upstream main7251f64a9c3bf75fb8b90940d3fda54c4fa610bb.
This is an investigation, not an assertion that every redundant item must be
kept or that every candidate has caused a recorded death.

## Confirmed in PlanMage

The town model set the phase capability weight to zero despite a stock of
40 Phase Door scrolls at the Alchemist and available gold. The character
repeatedly collected and then disposed of complete Phase Door stacks; the
last four were disposed at335771–335781. At the last shopping snapshot,
phase curve4 was [4,0,480,0,0], urgent needs empty and unmet0. The planner
left with no physical Phase Door. Base item cost is15 gold; the fight began
with165 gold, and the120 copper pickup raised it to285.

The direct cause is borg_town_capability.rs:477–484. A learned spell that
passes borg_spell_legal_fail(...,20) causes the entire phase curve weight to
be set to0. That predicate checks whether the book/spell is known and can
be afforded at **maximum**, rested mana; it does not require current mana,
light, or freedom from blindness/confusion. It is a preparedness predicate,
not evidence of unlimited emergency casts. The same pattern remains in the
inspected current upstream file. This is a confirmed retention/purchase defect,
not a claim that every spell/item substitution is wrong.

## Similar source-supported candidates

| Resource | Substitution rule | Evidence status and concern |
| --- | --- | --- |
| Food / hunger-removal items | Town capability FOOD is zeroed by a learned hunger spell. Legacy BI_FOOD gets1000 even at up to80% spell failure. | Code-confirmed assumption; not a recorded starvation attribution here. Test zero mana, inability to cast, and enough food to recover. Legacy weakness handling partly removes the sentinel and must be preserved. |
| Recall scrolls | Town RECALL curve is zeroed by a learned recall spell. Legacy BI_RECALL gets1000 at up to40% failure. | Code-confirmed assumption; not a recorded recall death here. Test exhausted mana, missing/disabled book access and a spare return option. |
| Mapping and trap/door/monster/invisible detection | Corresponding town curves are zeroed by learned spells. Legacy traits similarly use1000. | Context-dependent: resting in safety can make duplication wasteful, but a zero value ignores shared mana and urgent use. Do not call every sale a bug without a scenario. |
| Illumination and digging devices/scrolls | ILLUMINATE and DIG curves are zeroed by learned spells. Legacy abilities also credit spells/activations. | Test ability while out of mana or unable to cast, and whether an independent device retains useful option value. Not yet an observed bad disposal in this case. |
| Healing and speed/utility activations | Legacy traits credit some activations or spells with1000 without making those physical consumables. | Audit charge/cooldown and usage semantics. The M13 physical-healing model already deliberately separates actual potions; do not erase that correction or infer a new failure solely from the sentinel. |

The common issue is treating several services as independently renewable from
the same finite mana pool. Merely switching the test to current mana while
shopping is insufficient: the character can leave at full mana and exhaust
that pool later. Emergency physical reserves need independent value.

## Existing related issues

- [borg-rs#33](https://github.com/diegoami/borg-rs/issues/33): survival stock,
  affordable Phase Doors/cures, and retention. Its design is superseded by
  the broader inventory redesign; it is related policy work, not proof of
  this exact zero-weight bug.
- [borg-rs#31](https://github.com/diegoami/borg-rs/issues/31), closed: prior
  spending/stock classification problems. Historical context, not an active
  duplicate and not a claim that its old fix covers the new model.
- [borg-rs#4](https://github.com/diegoami/borg-rs/issues/4): recorded Fang
  spell-confidence/availability mismatch. A distinct case demonstrating why
  native castability and private Borg confidence must be checked separately.
- [borg-rs#41](https://github.com/diegoami/borg-rs/issues/41): inventory plan
  review and reserve/parameter contracts; useful for preserving intended
  behavior while correcting the concrete defect.

Suggested controlled cases: known escape spell with zero mana; the same at
full mana but one emergency scroll; failure/status-blocked casting; food and
recall backups under the same constraints; and a safe-rest information service
where discarding a duplicate is genuinely reasonable. Label constructed cases
and do not count these repeated trials as independent lives.

## Mage-specific refinement at source6c89d9a2

This section is a source audit, not a newly observed sale or death. The earlier
resource table covers all caster classes; it must not be read as saying a Mage
learns every spell named there. In engine42cd156ac's Mage class, Word of Recall,
Remove Hunger and Turn Stone to Mud are absent. Their spell-based suppression
rules apply to other classes, not to this Mage merely because it uses magic.

M13's loop at borg_town_capability.rs:473–486 suppresses the entire weight of
selected capability categories after a learned, nonzero-rated spell passes
borg_spell_legal_fail(...,20). That checks maximum rested mana (borg_magic.rs:
435–461), not an emergency reserve of current mana. It is effect-based, not a
blanket Mage check; another caster with a qualifying spell can trigger it too.

| Actual Mage case | Item value affected | Why it matters |
| --- | --- | --- |
| Learned Treasure Detection, eligible atCL10 and rated5, once failure passes20% | Magic Mapping scrolls, Mapping staves, Magic Mapping rods, Enlightenment potions: MAP service weight becomes0 | Definite semantic mismatch in the classifier: ore/gold/object sensing is put in MAP alongside terrain mapping. Treasure Detection does not reveal the dungeon layout. Minimum learn level is not proof of learning or current qualification. |
| Learned Detect Monsters, eligible atCL3, when reliable enough | Detect Evil staff: MONSTERS service weight becomes0 | Engine Detect Monsters excludes invisible races, while Detect Evil tests evil regardless of invisibility. The shared category incorrectly treats these as complete substitutes. |
| Learned Reveal Monsters, eligible atCL15, when reliable enough | Detect Invisible scroll/staff: INVISIBLE weight becomes0 | Physical detection backup loses its service value despite finite/shared spell mana. Actual disposal has not been reproduced here. |
| Learned Reveal Monsters under the same conditions | True Seeing potion loses its SINVIS service value | A detection snapshot and sustained See Invisible are different abilities but share INVISIBLE. The potion can retain blindness-cure value; do not call the whole potion worthless. |
| Learned Light Room, when reliable enough | Lighting component of Light scroll/staff and Illumination rod becomes0 | These items also have light-sensitive-monster damage in the engine; that ATTACK component remains. Rod/Wand of Light use a light beam and are not simply erased as illumination duplicates. |
| All supplied MAP/MONSTERS/INVISIBLE categories covered by qualifying learned spells | Detection rod's modeled services can all become0 | Composite devices require a per-effect audit; one suppressed category alone does not prove the whole device has no value. |

The Mage spell ratings are at borg_magic.rs:130–160 (Treasure Detection is5,
Detect Monsters85 and Reveal Monsters85); actual class spell/effect definitions
are engine/angband/lib/gamedata/class.txt's Mage block at172–448. Item effects
are in lib/gamedata/object.txt. Engine effect-handler-general.c distinguishes
MAP_AREA(1201), DETECT_ORE(1519), SENSE_GOLD(1682), SENSE_OBJECTS(1725),
DETECT_VISIBLE_MONSTERS(1854), DETECT_INVISIBLE_MONSTERS(1874) and
DETECT_EVIL(1911). The capability conflations are at
borg_town_capability.rs:225–254, with SINVIS classification at timed_cap.

There is no analogous blanket learned-spell suppression of M13 ATTACK, HEAL,
MANA, SPEED, TELEPORT or OTHER categories. In particular, attack wands are not
assigned zero merely because a Mage knows attack spells. Legacy equipment
activation scoring does give some abilities lower class-dependent bonuses:
Teleport Other500 for a Mage versus1000 for a Warrior; Resist All650 versus
25650 with current defaults (borg_power.rs:110–130; params.rs:1048–1060).
These are bonuses within equipment valuation, not total item prices or a proof
that an item will be discarded.

Separate capability gaps affect all classes: Stun Monster wands, Confuse Monsters
staves and Wonder wands have no modeled direct combat benefit in this M13
classifier. The first two are explicitly excluded pending their consumer
support; Wonder lacks a guaranteed-effect model. They are not Mage spell-
replacement cases, and other item contributions must still be considered.

No policy, item quota or shopping implementation was changed by this audit.
The concrete mapping/detection equivalence problems deserve isolated native
scenarios before any broader replacement of resource valuation.
