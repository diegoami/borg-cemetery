# M13 inventory calibration validation inputs (#433 / P4)

These are retained native compatibility inputs/results for reborn #433,
not a population, tuning or survival comparison. The source implementation
appends 362 neutral policy parameters without changing its default streams.

`runs.json` records the exact baseline/candidate source and executable hashes,
all 90 full-suite run receipts, two bounded override receipts, complete raw
stream payloads and source-qualified death IDs. The two source builds have
45 paired cells; these are not 90 independent observations. All four complete
streams (keys, messages, state and core decision trace) match in every pair.
Identical stream payloads are stored once and referenced by both sources.
Every natural death is retained under the sibling native-controls registry.
The 18 source-qualified dossiers describe nine paired death controls, not
18 independent lives. No class or character level was excluded.

Each payload ZIP contains the original unmodified stream bytes. Run configs,
summaries, full parameter tables, process receipts and borg.txt are retained
separately. Source line and absolute working paths are historical receipts;
reproduce in private output directories, preserving the supplied settings.
Both original executable images are retained with BUILD_ID, for a compatible
host and engine library installation; portable binary execution is not claimed.
Engine data remains pinned upstream 42cd156ac in the source repository.

Reproduce by checking out each recorded source commit, building through
`harness/build.sh`, and running `BORG_CORE=borg-rs BORG_CORE_OVERRIDES=off
JOBS=2 harness/suite.sh full PRIVATE_OUT` under the shared engine lock. The
full suite manifest pins its exact seed/race/class/horizon/flags and checksums.
For the bounded native check, run seed1010/race0/class0, 3000 turns, menu;
the changed attempt adds BORG_PARAM_SHOPPING_MAX_TURNS=1. Both bounded
attempts survive, their keys differ and the override origin is recorded.

The log/attempt limitations in runs.json preserve the initial local tooling
refusal and archival retries; those are not silently relabelled as games.
This package asserts completed-run stream identity, not verified recorder
replay or restored in-memory Borg state. No milestone acceptance is implied.
