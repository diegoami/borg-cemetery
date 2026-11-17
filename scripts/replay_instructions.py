"""Written playback instructions, with missing recordings stated explicitly."""
import os
from pathlib import Path
import re


def repository_path(directory):
    directory = directory.resolve()
    root = Path(__file__).resolve().parents[1]
    if directory.is_relative_to(root):
        return str(directory.relative_to(root))
    if 'records' in directory.parts and os.environ.get('GITHUB_RUN_ID'):
        after = directory.parts[directory.parts.index('records') + 1:]
        return '/'.join(('runs', os.environ['GITHUB_RUN_ID'] + '-' + os.environ.get('GITHUB_RUN_ATTEMPT', '1'), *after))
    return '/path/to/this-scenario'


def instructions(directory, program, source, seed, race, cls, endpoint, scenario=None, case_id=None):
    lines = ['# How to watch, replay and test this case', '',
             'Choose the operation below. Watching screenshots, verifying a recording and starting another Borg from a save have different requirements.', '',
             '## Case-local commands', '',
             '```bash', './build.sh', './watch.sh', './watch.sh --verify-only', './play.sh --label "My alternative" --note "What I tried"', '```', '',
             'Builds and recording work share this checkout\'s ignored `.cache/borg-cemetery/` entry, keyed by program/version. '
             'An existing older user cache is reused through that entry, preserving its recording paths. '
             'A successful version prints "Using cached …" and skips compilation on later calls. '
             'Set `BORG_CEMETERY_CACHE` or pass `--cache /path` to choose another location. '
             'The first saved-position build needs Git, Rust/Cargo, CMake, a C compiler, Make and X11 development headers. '
             'It builds the pinned optional recorder integration separately from the original recorder-off version. '
             'Human control needs an X11 display such as WSLg; Ctrl-X saves and exits (acknowledge Return/Escape if prompted). '
             'When you exit, the process retains your recording, attempts replay verification, and adds an Alternative human play entry. '
             'Verification failures remain labelled; activating the Borg makes the entry mixed human/Borg play. '
             'These are repository changes for you to commit/push; unrelated changes are not staged automatically.', '']
    if (directory / 'media/episode.gif').is_file():
        lines += ['## Watch the recorded screenshots', '', '[Open the animated episode](media/episode.gif). No installation is needed.', '']
    local_session = (directory / 'RECORDER.md').is_file()
    if local_session:
        lines += ['## Prepared local recorder session', '',
                  '[Use the verified standalone-recorder session](RECORDER.md). It records a new run from this saved position and matches the previous scenario trial.', '']
    if case_id in ('D0005', 'D0006'):
        name = case_id + '-recorded'
        turn = 36184 if case_id == 'D0005' else 22736
        url = f'https://github.com/diegoami/borg-cemetery/releases/download/recordings-2026-11-15/{case_id}.tar.xz'
        lines += ['## Replay the original recording', '',
                  f'[Download the complete {case_id} recording]({url}). It includes the matching Linux executable, game data and its recorder/player.', '',
                  'Requirements: 64-bit x86 Linux, glibc 2.39 or newer, Python 3.12 or newer, '
                  'and the X11 runtime libraries (Debian/Ubuntu package `libx11-6`). A terminal is needed for viewing; '
                  'headless verification needs no running X server. Download and unpack the archive:', '',
                  '```bash', f'curl -L --fail -o {case_id}.tar.xz {url}', f'tar -xJf {case_id}.tar.xz',
                  f'python3 {name}/runtime/tool-source/replay-borg.py {name} --verify-only --output /tmp/{case_id}-replay-proof --timeout 60',
                  f'python3 {name}/runtime/tool-source/replay-borg.py {name} --from-turn {turn}', '```', '',
                  'The first command reruns and verifies the original input, message, state, screen and save streams. '
                  'The second opens the human-readable terminal player near the death. Use a new proof directory on a subsequent verification.', '',
                  'This is the historical Borg recorder format and its bundled replay player. It is not the newer standalone angband-recorder format. '
                  'The original executable is included because recompiling the same source does not guarantee an identical executable.', '']
    else:
        lines += ['## Replay with angband-recorder', '',
                  ('**The original birth was not captured by the standalone recorder. A verified saved-position recording is available locally through the guide above.** '
                   if local_session else '**No complete angband-recorder recording is retained for this case.** ') +
                  'An engine save or screenshot GIF does not contain the recorder input streams, so neither can be passed to the recorder as a full recording.', '',
                  'For a future case that includes a recorder-enabled recording bundle and its exact recorded executable, the commands are:', '',
                  '```bash', 'angband-recorder view /path/to/recording 1',
                  'angband-recorder replay --verify /path/to/recording /tmp/new-verified-replay', '```', '',
                  'The first displays an actual recorded frame; the second reexecutes and verifies the recording. '
                  'These commands require a compatible bundle and the exact executable at the location recorded by the recorder. '
                  'They are format instructions, not a claim that this case already contains such a bundle.', '',
                  '[Recorder installation and supported format](https://github.com/diegoami/angband-recorder#readme).', '']
    if program in ('borg-rs', 'borg-reborn-rs') and re.fullmatch(r'[0-9a-f]{40}', str(source)) and all(isinstance(v, int) for v in (seed, race, cls, endpoint)):
        work = '/tmp/cemetery-' + (case_id or directory.name) + '-' + str(source)[:8]
        lines += ['## Build the original version', '',
                  'Install Git, Rust/Cargo, a C compiler, Make, CMake and the X11 development headers. Run from the cemetery checkout; use new output directories.', '',
                  '```bash', f'git clone https://github.com/diegoami/{program}.git {work}',
                  f'git -C {work} checkout {source}', f'BORG_IMPL=rust bash {work}/harness/build.sh', '```', '']
        if scenario and (directory / 'start.save.gz').is_file():
            path = repository_path(directory)
            lines += ['## Let a Borg play from the saved position', '',
                      f'The saved game starts at engine turn {scenario.get("start_turn")}. Both original and alternative versions start with fresh Borg memory and the saved engine RNG.', '',
                      '```bash', f'python3 scripts/run_scenario.py run --source {work} \\',
                      f'  --scenario {path} --turns 1000 --out /tmp/{directory.name}-original-trial', '```', '',
                      'For an alternative version, build that version in a separate checkout and replace the `--source` path. '
                      'Use the same scenario and turn budget, with a different output directory. This is a saved-position survival test, not an uninterrupted original-memory replay.', '',
                      '[Run the same comparison through GitHub Actions](https://github.com/diegoami/borg-cemetery/actions/workflows/try-scenario.yml). '
                      f'The scenario path is `{path}`. Choose the cemetery branch containing it and the alternative Borg version.', '']
        lines += ['## Rerun the birth seed', '', 'This starts a new process from the original birth. It does not verify a missing recorder bundle.', '',
                  '```bash', f'BORG_CEMETERY_DIR="$PWD" BORG_IMPL=rust BORG_DEATH_RECORDS_DIR=/tmp/{directory.name}-diagnostic-deaths \\',
                  f'  bash {work}/harness/run.sh /tmp/{directory.name}-seed-rerun {seed} {race} {cls} {endpoint + 1000} menu', '```', '']
    (directory / 'REPLAY.md').write_text('\n'.join(lines))
    return lines
