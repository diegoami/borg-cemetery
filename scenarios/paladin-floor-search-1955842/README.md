# Paladin secret-door search loop on ordinary floor

The owner-saved High-Elf Paladin from [borg-reborn-rs #1131](https://github.com/diegoami/borg-reborn-rs/issues/1131) is in `start.save.gz`. Decompress it before loading. The original and compressed checksums, build, and runtime settings are in `scenario.json`.

The uninterrupted recording shows fragments of dark exploration and a two-step secret-door search counteracting each other on DL3. From turns 1,954,262 to 1,955,842, the character made 158 moves across (171,26), (172,26), and (173,26). The action excerpt shows two keys west and two east. The owner stopped the Borg at (172,26), at CL17 with 163 HP and 16 SP. The position, message, and action excerpts preserve the loop.

The same-build headless reload with saved engine RNG loaded the Paladin at 1,955,842. It reported `borg_stopped` before sending a Borg key. The reload did not reproduce the active loop.
