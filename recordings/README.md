# Original game recordings

These are complete original recordings with a working replay player, not just
collections of reports. The frozen Linux executable and game data are included
because replay must use the recorded version. Python 3 and a 64-bit Linux
machine are required; a terminal is needed for interactive viewing. The frozen
executables require glibc 2.39 or newer and the X11 runtime libraries
(`libx11-6` on Debian/Ubuntu). Use Python 3.12 or newer. Headless replay
verification does not need an X server.

| Death | Download | Written playback guide |
| --- | --- | --- |
| D0005: Fang, seed 1532917772 | [D0005 recording, 3.8 MB](https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0005.tar.xz) | [Instructions](../deaths/D0005-recorded/REPLAY.md) |
| D0006: grey mold, seed 2647001198 | [D0006 recording, 3.7 MB](https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0006.tar.xz) | [Instructions](../deaths/D0006-recorded/REPLAY.md) |

Each archive contains HOW-TO-REPLAY.md. Both relocated recordings were rerun
using their bundled recorder/player on 2026-11-15, verifying original keys,
messages, player state, terminal frames, final saves and scheduled saves.
The repeated verifications do not count as new independent lives.

These use the historical borg-rs headless recorder format. The newer standalone
angband-recorder uses a different format; its commands must not be applied to
these archives. Other case pages clearly state when they have screenshots or
engine saves but no complete recorder input recording.

The source versions are borg-rs 9881301ceaad91d0c68a61bed1a8ccdde100e660
for D0005 and aa4ad6cfeea2cf19870e224219dfe66688175c6e for D0006.
The recorded programs retain their original Angband/Borg licensing.
