# M1 review packet — recorded runs, replay and human alternatives

**Status: awaiting owner-selected independent review. Not an approval.**

Implementer: Codex, OpenAI GPT family. The owner will choose or run the reviewer;
a model reviewer should be from a different family. No reviewer has been launched
by this session. The owner merges the milestone review PR and decides acceptance.

## Exact boundary

Baseline: `44d97669ebdf7390b384656c61365b0ca30f3266`.

Implementation: `5c3c69e6544a07f9b84f5d4feb18bf176ee10983`.

Review the complete baseline-to-implementation diff, not only the latest commit.
The review PR also includes subsequent documentation-only review preparation;
its body records the exact publication head. `reviewed` starts at the baseline
only to expose this first review's diff; it does not imply earlier acceptance.

## Delivered work and entry points

| Area | Implementation | Expected result |
| --- | --- | --- |
| Pinned seeded collection | `scripts/run_batch.py`, `.github/workflows/run-borg.yml` | Requested seeds survive setup failures; resolved commits, build identity and outcomes are retained |
| Episode extraction | `scripts/extract_scenarios.py`, `scripts/episode_inventory.py` | Adaptive observed sequences, inventory/spells and eligible original saves; missing evidence is explicit |
| Human presentation | `scripts/death_pages.py`, `scripts/human_readable.py`, `scripts/capture_episode_media.py` | Written pages, actual screenshot GIFs and replay instructions without serialized dumps as the human interface |
| Saved-position comparisons | `scripts/run_scenario.py`, `scripts/compare_batches.py`, `.github/workflows/try-scenario.yml` | Shared starts and honest outcomes; failures do not become rescues |
| Durable storage | `scripts/archive_records.py` | Unique append-only workflow attempts; compact data retained after artifact expiry; launcher permissions restored |
| Case launchers | `scripts/case_launchers.py`, `scripts/case_replay.py` | Generated build/watch/play commands, pinned runtime preparation and qualified recorder playback |
| Human alternatives | `case_replay.py` human capture/attachment | Real input recording, visible verification status, bounded report additions, explicit actor classification and no new-independent-life count |
| Version cache | `case_replay.py`, `tests/test_version_cache.py` | Shared per-version reuse, executable checks, completed phase reuse and no rebuild on a successful cache hit |

These were implemented directly on main before this first review. They are
recorded retrospectively as delivered areas, not fabricated closed task issues.

## Evidence available to a reviewer

- Run the Python suite from a clean checkout after installing
  `requirements-media.txt`. The implementation head contains 31 tests, covering
  runner failures and identity, archive append/modes, episode boundaries,
  readable pages, scenario binding, launchers, human attachment and cache reuse.
- The prior implementation head `2015956` passed
  [GitHub Check cemetery runner](https://github.com/diegoami/borg-cemetery/actions/runs/43658937613).
  The review PR must use the check for its own final head as authoritative;
  this older result is not proof for subsequent changes.
- [D0007](../../../deaths/D0007/README.md) and
  [S0003](../../../scenarios/S0003/README.md) retain the real selected Elf Mage
  death: original seed 102, saved turn 3402, report boundary 3432, death 3640.
  Its stored original-version trial dies; the alternative borg-rs trial reaches
  its requested survival horizon. The builds differ, so this is not isolation
  of a specific policy or a population survival result.
- A fresh pinned optional-recorder build and S0003 capture/replay were exercised
  locally. Its keys, messages and state matched the prior S0003 trial byte for
  byte. The pinned integration is
  `2e648118eedc31904dcaed056db52e14acda2a07`, separately identified from the
  original recorder-off source. An X11 virtual-display save/quit smoke test
  loaded the exact expected turn/character, passed recorder verification,
  attached to a temporary synthetic report, and reverified the retained archive.
  It is not a genuine human continuation or an independent life.
- Those native/UI checks were executed during implementation before the final
  cache-only/startup-clarity corrections. They were not all repeated after that
  correction. The reviewer should reproduce the focused checks required for
  acceptance; local temporary artifacts are not durable public evidence.
- [Original D0005/D0006 downloads](../../../recordings/README.md) include the
  frozen Linux runtime and historical player. Both relocated bundles were
  reexecuted and verified before publication. Published SHA-256 values match
  `recordings/SHA256SUMS`. These are the old headless format, not interchangeable
  with standalone recorder v0.1.0.
- Migration preserved native records, source save/observation data, terminal
  text captures and comparison bindings. The old local-validation tree was
  removed; original D0001–D0006 records remain unchanged. Git history retains
  prior generated views. Owner-generated, uncommitted human continuations are
  deliberately excluded from this implementation review snapshot.

## Known limits and review questions

1. The near-death and reasonably-stable boundaries are heuristics, not established
   definitions of imminent death or safety. The original save may precede the
   report boundary; S0003's difference is 30 engine ticks. Human control can
   avoid the encounter entirely. `watch` and `play` must remain distinct.
2. Native recorder frames for the qualified S0003 run end at turn 3632 while
   the engine reports death at 3640. A verified run does not prove a complete
   visual death sequence. Decide whether M1's playback presentation is acceptable
   or blocked by missing terminal frames, glyph/legend or end-of-run handling.
3. Standalone recorder qualification is deliberately limited to the retained
   reborn version/integration. Other versions must not silently use that Borg.
   Human GUI starts use the separately identified recorder-enabled runtime;
   save compatibility and fair start assertions warrant scrutiny.
4. Human recording verification can fail or capture can be incomplete. Inspect
   attachment behaviour, actor detection, initial position checks, outcome
   wording, timeout cleanup, bounded/atomic report updates and recording retention.
   No human-survival inference follows merely from a final living observation.
5. Small human archives retain recording inputs, not a frozen executable in Git.
   Exact reverification needs the matching cached runtime. Frame viewing and
   portable verified reexecution are different capabilities. Oversized recording
   publication is not automatic; inspect whether preservation is sufficient.
6. Current canonical checked-in cases/scenarios and the CI batch-namespaced
   results layout are related views, not yet one fully reconciled global registry.
   Inspect stale indexes, duplicate-life accounting and discoverability across
   branches. `deaths/index.json` remains the imported historical registry.
7. The full manual run-borg/try-scenario workflows were authored but were not
   dispatched end-to-end in this session. Unit CI is not cloud pipeline proof.
   Assess artifact failure handling, source/write credential separation, archive
   retries and concurrent runs, as well as tool/data availability on fresh runners.
8. Cache identity and reuse must preserve executable bindings and source pins.
   Inspect partial builds, profile/data changes, old cache aliasing, corruption,
   command concurrency and the cost/meaning of integrity checks. Do not accept
   version labels as proof by themselves.
9. Automated causal investigations and tuning proposals are future work. Current
   written reports and traces are useful evidence, not automatic causal analysis.
   No general survival advantage or exact private Borg-memory restoration is claimed.

## Run the review

Use [PROMPT.md](PROMPT.md). Report blockers separately from limitations, with
severity, exact path/line, a reproduction and the smallest necessary correction.
Give an explicit accept / conditional accept / changes-required verdict and list
what was not checked. Do not merge, advance `reviewed`, tag or start new work.
