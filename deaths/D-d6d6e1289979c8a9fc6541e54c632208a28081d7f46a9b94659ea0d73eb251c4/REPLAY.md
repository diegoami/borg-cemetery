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

## Replay with angband-recorder

**No complete angband-recorder recording is retained for this case.** An engine save or screenshot GIF does not contain the recorder input streams, so neither can be passed to the recorder as a full recording.

For a future case that includes a recorder-enabled recording bundle and its exact recorded executable, the commands are:

```bash
angband-recorder view /path/to/recording 1
angband-recorder replay --verify /path/to/recording /tmp/new-verified-replay
```

The first displays an actual recorded frame; the second reexecutes and verifies the recording. These commands require a compatible bundle and the exact executable at the location recorded by the recorder. They are format instructions, not a claim that this case already contains such a bundle.

[Recorder installation and supported format](https://github.com/diegoami/angband-recorder#readme).

## Build the original version

Install Git, Rust/Cargo, a C compiler, Make, CMake and the X11 development headers. Run from the cemetery checkout; use new output directories.

```bash
git clone https://github.com/diegoami/borg-reborn-rs.git /tmp/cemetery-D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-f02cd294
git -C /tmp/cemetery-D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-f02cd294 checkout f02cd2940a7439a8965b3883270a9a73df7e0bf5
BORG_IMPL=rust bash /tmp/cemetery-D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-f02cd294/harness/build.sh
```

## Rerun the original death

Zoo ran this game with its own `borg.txt` settings (and errands plan, if any), not through `harness/run.sh`. This rebuilds that `borg.txt` from `config.txt`, refuses it unless its sha256 matches the recorded one, runs the game as Zoo did and checks that the key stream equals the recorded one.

```bash
python3 scripts/native/rerun-death.py deaths/D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4 /tmp/D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-original-rerun \
  --source-root /tmp/cemetery-D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-f02cd294
```

## Rerun the birth seed

This starts the same birth with the default harness profile and no Zoo settings or plan, so the Borg does not play the original game.

```bash
BORG_CEMETERY_DIR="$PWD" BORG_IMPL=rust BORG_DEATH_RECORDS_DIR=/tmp/D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-diagnostic-deaths \
  bash /tmp/cemetery-D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-f02cd294/harness/run.sh /tmp/D-d6d6e1289979c8a9fc6541e54c632208a28081d7f46a9b94659ea0d73eb251c4-seed-rerun 934061548 1 2 28401 menu
```
