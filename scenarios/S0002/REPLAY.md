# How to watch, replay and test this case

Choose the operation below. Watching screenshots, verifying a recording and starting another Borg from a save have different requirements.

## Watch the recorded screenshots

[Open the animated episode](media/episode.gif). No installation is needed.

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
git clone https://github.com/diegoami/borg-reborn-rs.git /tmp/cemetery-S0002-e9a6a521
git -C /tmp/cemetery-S0002-e9a6a521 checkout e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71
BORG_IMPL=rust bash /tmp/cemetery-S0002-e9a6a521/harness/build.sh
```

## Let a Borg play from the saved position

The saved game starts at engine turn 3302. Both original and alternative versions start with fresh Borg memory and the saved engine RNG.

```bash
python3 scripts/run_scenario.py run --source /tmp/cemetery-S0002-e9a6a521 \
  --scenario scenarios/S0002 --turns 1000 --out /tmp/S0002-original-trial
```

For an alternative version, build that version in a separate checkout and replace the `--source` path. Use the same scenario and turn budget, with a different output directory. This is a saved-position survival test, not an uninterrupted original-memory replay.

[Run the same comparison through GitHub Actions](https://github.com/diegoami/borg-cemetery/actions/workflows/try-scenario.yml). The scenario path is `scenarios/S0002`. Choose the cemetery branch containing it and the alternative Borg version.

## Rerun the birth seed

This starts a new process from the original birth. It does not verify a missing recorder bundle.

```bash
BORG_IMPL=rust BORG_DEATH_RECORDS_DIR=/tmp/S0002-diagnostic-deaths \
  bash /tmp/cemetery-S0002-e9a6a521/harness/run.sh /tmp/S0002-seed-rerun 102 2 1 4352 menu
```
