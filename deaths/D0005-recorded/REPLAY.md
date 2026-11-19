# How to watch, replay and test this case

Choose the operation below. Watching screenshots, verifying a recording and starting another Borg from a save have different requirements.

## Case-local commands

```bash
./build.sh
./watch.sh
./watch.sh --verify-only
./play.sh --label "My alternative" --note "What I tried"
```

Builds and recording work share this checkout's ignored `.cache/borg-cemetery/` entry, keyed by program/version. An existing older user cache is reused through that entry, preserving its recording paths. A successful version prints "Using cached …" and skips compilation on later calls. Set `BORG_CEMETERY_CACHE` or pass `--cache /path` to choose another location. The first saved-position build needs Git, Rust/Cargo, CMake, a C compiler, Make and X11 development headers. It builds the pinned optional recorder integration separately from the original recorder-off version. Human control needs an X11 display such as WSLg; Ctrl-X saves and exits (acknowledge Return/Escape if prompted). When you exit, the process retains your recording, attempts replay verification, and adds an Alternative human play entry. Verification failures remain labelled; activating the Borg makes the entry mixed human/Borg play. These are repository changes for you to commit/push; unrelated changes are not staged automatically.

## Replay the original recording

[Download the complete D0005 recording](https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0005.tar.xz). It includes the matching Linux executable, game data and its recorder/player.

Requirements: 64-bit x86 Linux, glibc 2.39 or newer, Python 3.12 or newer, and the X11 runtime libraries (Debian/Ubuntu package `libx11-6`). A terminal is needed for viewing; headless verification needs no running X server. Download and unpack the archive:

```bash
curl -L --fail -o D0005.tar.xz https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/D0005.tar.xz
tar -xJf D0005.tar.xz
python3 D0005-recorded/runtime/tool-source/replay-borg.py D0005-recorded --verify-only --output /tmp/D0005-replay-proof --timeout 60
python3 D0005-recorded/runtime/tool-source/replay-borg.py D0005-recorded --from-turn 36184
```

The first command reruns and verifies the original input, message, state, screen and save streams. The second opens the human-readable terminal player near the death. Use a new proof directory on a subsequent verification.

This is the historical Borg recorder format and its bundled replay player. It is not the newer standalone angband-recorder format. The original executable is included because recompiling the same source does not guarantee an identical executable.

## Build the original version

Install Git, Rust/Cargo, a C compiler, Make, CMake and the X11 development headers. Run from the cemetery checkout; use new output directories.

```bash
git clone https://github.com/diegoami/borg-rs.git /tmp/cemetery-D0005-9881301c
git -C /tmp/cemetery-D0005-9881301c checkout 9881301ceaad91d0c68a61bed1a8ccdde100e660
BORG_IMPL=rust bash /tmp/cemetery-D0005-9881301c/harness/build.sh
```

## Rerun the birth seed

This starts a new process from the original birth. It does not verify a missing recorder bundle.

```bash
BORG_CEMETERY_DIR="$PWD" BORG_IMPL=rust BORG_DEATH_RECORDS_DIR=/tmp/D0005-recorded-diagnostic-deaths \
  bash /tmp/cemetery-D0005-9881301c/harness/run.sh /tmp/D0005-recorded-seed-rerun 1532917772 2 4 37289 menu
```
