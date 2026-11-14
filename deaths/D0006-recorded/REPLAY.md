# How to watch, replay and test this case

Choose the operation below. Watching screenshots, verifying a recording and starting another Borg from a save have different requirements.

## Replay the original recording

[Download the complete D0006 recording](https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0006.tar.xz). It includes the matching Linux executable, game data and its recorder/player.

Requirements: 64-bit x86 Linux, glibc 2.39 or newer, Python 3.12 or newer, and the X11 runtime libraries (Debian/Ubuntu package `libx11-6`). A terminal is needed for viewing; headless verification needs no running X server. Download and unpack the archive:

```bash
curl -L --fail -o D0006.tar.xz https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0006.tar.xz
tar -xJf D0006.tar.xz
python3 D0006-recorded/runtime/tool-source/replay-borg.py D0006-recorded --verify-only --output /tmp/D0006-replay-proof --timeout 60
python3 D0006-recorded/runtime/tool-source/replay-borg.py D0006-recorded --from-turn 22736
```

The first command reruns and verifies the original input, message, state, screen and save streams. The second opens the human-readable terminal player near the death. Use a new proof directory on a subsequent verification.

This is the historical Borg recorder format and its bundled replay player. It is not the newer standalone angband-recorder format. The original executable is included because recompiling the same source does not guarantee an identical executable.

## Build the original version

Install Git, Rust/Cargo, a C compiler, Make, CMake and the X11 development headers. Run from the cemetery checkout; use new output directories.

```bash
git clone https://github.com/diegoami/borg-rs.git /tmp/cemetery-D0006-aa4ad6cf
git -C /tmp/cemetery-D0006-aa4ad6cf checkout aa4ad6cfeea2cf19870e224219dfe66688175c6e
BORG_IMPL=rust bash /tmp/cemetery-D0006-aa4ad6cf/harness/build.sh
```

## Rerun the birth seed

This starts a new process from the original birth. It does not verify a missing recorder bundle.

```bash
BORG_IMPL=rust BORG_DEATH_RECORDS_DIR=/tmp/D0006-recorded-diagnostic-deaths \
  bash /tmp/cemetery-D0006-aa4ad6cf/harness/run.sh /tmp/D0006-recorded-seed-rerun 2647001198 1 3 23841 menu
```
