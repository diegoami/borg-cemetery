# Surplus throwing weapons (#1200)

Constructed encounters on the borg-rs core at
[`9c8024ea4e7e82d9683609a62bacef43a4cd5a67`](https://github.com/diegoami/borg-reborn-rs/commit/9c8024ea4e7e82d9683609a62bacef43a4cd5a67).
The [recorded Mage](../mage-overweight-cursed-kit-9221204) and the separate
[natural Priest checkpoint](../caster-rune-backlog-1169/priest-original.save.gz)
supply the player state and saved RNG. The author clears existing monsters,
lights open flooring, supplies a specified gear set and places a kobold.
The authoring engine only writes and inspects the fixtures. The normal
build plays each input with fresh Borg memory.

## Native results

| Case | Attack selected | Calculated odds or damage | Engine result |
| --- | --- | --- | --- |
| CL17 Gnome Mage at distance 4 | Plain Dagger | 74% hit, 4 of 10 tiles | The dagger left the pack on a miss and landed on the floor |
| CL10 Dunadan Priest at distance 4 | Plain Dagger | 75% hit, 4 of 10 tiles | Hit for 3 and left the pack |
| Same Priest, Spear | Plain Spear | 75% hit, 4 of 7 tiles | Hit for 6 and left the pack |
| Mage and Priest at distance 4, switch off | Melee after closing | Throw utility 0 | The spare was excluded from attacking |
| Priest starts at distance 11 | Dagger only after closing | Throw utility 0 outside ten tiles, 73% hit at distance 10 | Hit for 3 at the limit without an out-of-range prompt |
| Mage with a castable book | Electric Arc | 93% cast success, roughly 19.5 expected HP | Spell did 22. The dagger stayed in the pack |
| Mage with an Acid Bolts wand | Wand | 97.3% activation success, roughly 43.8 expected HP | One charge did 70. The dagger stayed in the pack |
| Mage with Sling and Iron Shots | Launcher shot | 83.83% hit at four tiles, roughly 34.4 expected HP per shot | An Iron Shot hit for 40. The dagger stayed in the pack |
| Priest already adjacent | Mace melee | 81.84% hit per swing with the equipped weapon | Missed once, then hit for 12. The spare stayed in the pack |
| Mage with an unknown resist-nexus Dagger | No throw | Throw utility 0 | Wielded as gear with its rune still unknown |
| Mage with a Dagger (+0,+8) | No throw | Throw utility 0 | Kept in the pack |

The plain Dagger averages 7.5 damage per hit, or roughly 5.6 expected HP
at four tiles. The Borg's integer rating truncates 7.5 before applying
hit chance. The Spear averages 21 per hit, or 15.75 at 75%. The spell and
device have one cast or activation check and no separate hit roll. The
figures exclude overkill, criticals and the Borg's utility weights.
The before-save TSV files call the native chance functions.

Raw throw utility was 5 against 40 for Electric Arc, 39 for Acid Bolts
and 44 for the launcher. The adjacent Priest used the existing
close-fight path. The core trace records raw and class-weighted utilities
where the normal attack ranking ran.

## Verifying the object

The immediate runs stop just after the throw and show an empty pack.
The engine reports the named Dagger or Spear leaving the pack. The key
streams contain `v / a 5`: the existing prompt handler sends one slash
to select inventory. The longer runs can recover the spent projectile
from the floor. A prototype queued an extra slash and selected the
equipped Mace. The corrected build uses the existing handler.

The switch is off in the shipped profile. These controlled starts grant a
spare and establish eligibility, selection and native execution. They give
no population estimate or reason to buy or stockpile throwing weapons.

[Receipts](receipts.json) pin the build, settings, inputs and logs.
[Replay](replay.sh) runs the named local cases from the pinned source.
