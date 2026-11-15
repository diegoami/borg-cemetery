# Replay S0003 with angband-recorder

A real standalone-recorder session was prepared on the owner's Ubuntu/WSL
machine on 2026-11-15. It starts from S0003's exact save at engine turn 3402,
preserves the saved engine RNG, and starts a fresh Borg. It is a recording of
that saved-position trial, rather than a recovered recording of the original
birth.

## Watch it now

In the Ubuntu/WSL terminal, run:

```bash
bash /tmp/S0003-recorder-session/watch.sh
```

This calls the standalone recorder's own frame viewer and advances through
the recorded terminal screens. It starts at frame 15, engine turn 3432, near
the inferred reasonably stable point. Press Ctrl-C to stop. To watch from the
loaded save instead, run:

```bash
bash /tmp/S0003-recorder-session/watch.sh 1
```

## Reexecute and verify

```bash
bash /tmp/S0003-recorder-session/verify.sh
```

The helper sets the headless frontend and profile environment, calls
`angband-recorder replay --verify`, and retains a new verification output
directory. The recorder checks its recorded executable identity and verifies
the replayed streams. This does not change the repository's starting save.

## What was checked

- The starting save hash matches S0003.
- Capture and standalone recorder replay both completed successfully.
- Keys, messages and engine-state logs match the earlier original-version
  S0003 trial byte-for-byte.
- The new process loaded turn 3402 and died to Fang at turn 3640.
- The recorder retained 98 terminal frames. Frame 15 is turn 3432. Its last
  rendered game turn is 3632; the verified game result records death at 3640.

## Runtime and location

The capture uses the existing optional recorder-enabled reborn integration
build, with angband-recorder v0.1.0, rather than altering the original
recorder-off binary. Matching the previous trial's input/message/state logs
qualifies this particular saved-position run; it is not a general parity claim.

- Recorder: `/home/diego/projects/angband/angband-recorder/target/debug/angband-recorder`
- Recorder-enabled game: `/tmp/reborn-recorder-build/game/angband`
- Complete captured streams: `/tmp/S0003-recorder-session/record/`
- First verified replay: `/tmp/S0003-recorder-session/replay/`
- Original run output retained separately: `/tmp/S0003-recorder-session/original-run/`

This is a prepared local session, not a published portable download. It needs
the existing executable, profile and session files on that machine. `/tmp`
may be cleared; the scripts above will then need the session to be recreated.
The frozen source save, GIF and written account remain in this repository.
