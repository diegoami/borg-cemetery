# Elf Ranger retains two purchased stat-tradeoff potions

On P-Borg build `260e8ad122d15c1b9ce920a74cd1e7c295cb1328`, the level 20 Elf Ranger `Borg261127223028` carried one Potion of Nimbleness and one Potion of Contemplation at DL5, turn 2,317,989. The save and Borg map match. This is a nonfatal incident supporting [borg-reborn-rs #1371](https://github.com/diegoami/borg-reborn-rs/issues/1371).

| Turn | Observation |
| ---: | --- |
| 605,411 | Buys a known Potion of Nimbleness for 1,000 gold in the Alchemy Shop. |
| 2,193,437 | Buys a Potion of Contemplation for 3,000 gold in the Black Market. The purchase message calls it a Metallic Blue Potion. |
| 2,317,989 | Both potions remain in the Ranger’s pack. |

The shop describes wares with `ODESC_STORE`, which shows the true kind. The purchase message omits that flag and prints before the engine records the flavour as learned. P-Borg reads the shop description with that same store flag. Contemplation was a named offer before the purchase.

The engine restores and can raise the target stat, then permanently lowers a different random stat. Nimbleness targets Dexterity. Contemplation targets Wisdom, and the Borg's current intentional use rule for Contemplation excludes Rangers. The final checkpoint can test post-identification disposal. The purchase excerpts document the earlier decisions, which precede the saved state. No full-session replay has been performed.

The [evidence archive](borg-ranger-unused-consumables.tar.gz) includes the native save, Borg map, recorded P-Borg settings, resolved settings, and excerpts around purchase and capture. The [archive checksum](SHA256SUMS) and the manifest inside the archive cover the retained files.
