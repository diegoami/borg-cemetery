# Mage recovery shuttle on DL1

The owner-saved Gnome Mage from [borg-reborn-rs #1118](https://github.com/diegoami/borg-reborn-rs/issues/1118) is in `start.save.gz`. Both saves are unmodified game bytes, with checksums and build information in `scenario.json`.

The uninterrupted recording shows the Mage repeatedly walk between (107,44) and (114,44). From turns 4,076,660 to 4,078,780 it selected thirty seven-step recovery routes while the breeder rest policy refused to rest and said to leave. The owner stopped the Borg on turn 4,078,820 at (111,44) with 47 HP and 2 SP. The position and message excerpts preserve that sequence.

The final save loaded at 4,078,820 in the reported build. The headless front end stopped at startup without Borg decisions. The earlier autosave in `earlier-autosave.save.gz` loaded at 4,074,710 and reached the cap at 4,081,000 alive, at depth two. Both checks preserved the engine RNG and started with fresh Borg memory. The active loop is documented by the uninterrupted recording.
