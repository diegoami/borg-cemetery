# Recorder playback and human alternatives for S0003

The case-local commands are part of the collection process and work without
session-specific paths. From this directory, run:

```bash
./build.sh
./watch.sh
```

The build prepares the pinned optional recorder integration in the shared,
ignored `.cache/borg-cemetery/` entry in the cemetery checkout. Existing older
user-cache versions are reused, and later calls skip compilation. Watching captures a new run from S0003's exact save at turn 3402,
verifies it, and plays its recorded frames from the inferred stable point.
Press Ctrl-C to stop. For verification without the player:

```bash
./watch.sh --verify-only
```

## Record your alternative human play

```bash
./play.sh --label "My attempt" --note "What I tried differently"
```

You control an X11/WSLg game window at the saved position. The engine uses the
saved RNG and the Borg starts off. Ctrl-X saves and exits; acknowledge any
Return/Escape prompts, including the score screen, until the window closes.
The launcher then attempts full recorder replay verification and attaches your
recording, outcome and notes under **Alternative human play** in death D0007.
If you activate the Borg, the entry is labelled mixed human/Borg play.

The retained save is at turn **3402**, 30 engine ticks before the report's
inferred stable point at **3432**. Fang is out of view at that marked point;
the original Borg is bitten at 3440, and Fang is drawn as `C`. Your own actions
can avoid or change that encounter. `watch.sh` shows the recorded Borg sequence;
`play.sh` lets you make a new continuation from the saved position.

The original death remains unchanged before that appended section, and your
continuation is not counted as another independent life. Compact recording
data and the written entry are kept in D0007's `alternatives/human/` directory;
the exact executable stays in the persistent cache. Commit/push those new
recording/report files when ready. The launcher does not stage unrelated work.

To watch an attached continuation from the death directory:

```bash
./watch.sh --alternative SESSION-ID
```

Use `--cache /path` or `BORG_CEMETERY_CACHE` to select the cache location.
Historical cases without an available save or qualified recorder build state
the limitation explicitly. No different Borg is silently substituted.

## Qualification already performed

A recorded saved-position run was created and fully replay-verified on
2026-11-15. Its keys, messages and state stream matched the previous S0003
trial byte-for-byte: loaded at 3402, died to Fang at 3640. This uses a new
process and fresh Borg memory, rather than reconstructing the original birth.

A fresh pinned build through D0007's launcher passed recorder verification.
An isolated synthetic X11 save-and-quit test also loaded the correct saved
character, recorded terminal input, passed full replay verification, attached
the recording to a temporary report and replay-verified the retained archive.
That synthetic check is not a human alternative in D0007.

The recorder's last rendered game turn can precede the final engine result;
the qualified original trial rendered through 3632 and recorded death at 3640.
The player states the verified final result after the recorded screens.
