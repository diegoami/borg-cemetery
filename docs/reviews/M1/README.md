# M1 review packet — recorded runs, replay and human alternatives

**Status: independently reviewed; conditional acceptance recommendation.
Owner acceptance remains pending.**

Implementer: Codex, OpenAI GPT family. The owner-selected MiniMax-M3 review
found no M1 implementation defect and raised review-boundary/receipt findings.
See [the response and remaining acceptance boundary](REVIEW-RESPONSE-20261120.md).
The owner decides acceptance; no review merge or acceptance tag is implied.

## Exact boundary

Baseline: `44d97669ebdf7390b384656c61365b0ca30f3266`.

Implementation: `cd562eabc40267a15be3eb7d2036d65e6f0c4a5a`.

Review the complete baseline-to-implementation diff, not only the latest commit.
Historical publication: `7d5d1422d4429db932c5f3d3b6279a837ec9123b`.
Only the implementation-to-historical-publication interval was documentation-only
preparation. PR #1 follows moving `main`; its current diff also includes later
code, data, M2 and identity work. Those additions are outside this M1 review.
The PR body records a dated integration snapshot and its checks separately.
`reviewed` remains at the baseline; merging current main would advance it across
later work as well, so a scoped M1 recommendation alone is insufficient to merge
PR #1. See the response before making an acceptance decision.

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
  `requirements-media.txt`. The implementation head contains 46 own tests plus 35 retained native-tool tests, covering
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
  prior generated views. The owner explicitly requested publication of the real human continuation
  after the initial review pin. Its original archive and capture metadata are
  retained unchanged beside a new readable comparison and checksum/start binding
  checks. The new implementation pin includes that recording and the automatic
  comparison logic.

## Owner-requested human continuation addition

After the initial review packet, the owner requested that the real human
continuation be published in the report. The implementation pin above supersedes
`5c3c69e6544a07f9b84f5d4feb18bf176ee10983` and includes this correction.

[The recorded human alternative](../../../deaths/D0007/alternatives/human/20261115T004527-7541a0/README.md)
loaded the original S0003 save at 3402 and was alive at 4873, level 2 with 15/15
HP: 1233 engine ticks beyond the original death at 3640. The archived captured
file inputs contain the exact source save bytes, the archive matches its capture
hash, recorder verification passed at capture, there are no Borg input events,
and the observed flags show no cheat-live/wizard/debug use. Fang was never
recorded as visible; this is survival from the retained starting position, not
proof of defeating Fang in a direct fight or of a general policy improvement.
Original capture metadata is preserved; the comparison is added beside it.
New attachments produce this distinction and summary automatically.

## Owner-requested analysis and tool ownership addition

The owner requested an actual analysis pass on all seven retained deaths and
then requested bringing the reusable reborn death tools here, leaving pointers
there. The current pin includes [that pass](../../death-analysis.md), seven
per-case reports, frozen profiles and the complete bounded D0007 result set.

Five restart-based arms share S0003, the original e9a6a521 executable and a
1000-engine-turn cap. The unchanged control reproduces its retained terminal
summary (except wall time). Horizon 2 survives, horizon 3 dies, risk aversion 75
reproduces the death, and rest duration 1 survives with **four refused-action
violations**. This is not an accepted tuning improvement; all arms and logs are
retained, and the short-rest result is explicitly qualified as a refusal/cooldown
interaction. No Borg source/default profile or population experiment changed.

Native exporter, registry utilities, source-checked rerun and reconciliation
code plus 35 retained tests moved from reborn 83cf442a (and the concurrent
#276 registry-template/tests addition) into scripts/native with
licence/provenance. Canonical registration protects existing records/indexes and
adds readable pages/catalogue. Reborn [task PR #282](https://github.com/diegoami/borg-reborn-rs/pull/282)
keeps thin API-1 forwarders and pins this toolkit in CI, preserving temporary
registries and historical guards. Its integration head is `ca43b3796b1b8464e7aa3f922f0f41be7d862221`, using the
unchanged toolkit pin `33c375527a8e443cdfcda19e864e4561f0c1c9ef`. Full integration CI is [green](https://github.com/diegoami/borg-reborn-rs/actions/runs/43709250234)
for that exact head (Rust, engine and recorder), including the full deterministic
suite, missing-death reconciliation and exact-source rerun. PR #282 merged as
`811f338a44428bacda79492690e7ac903a8e0c8b`. The primary local consumer checkout
was not modified. Exact toolkit CI is [green](https://github.com/diegoami/borg-cemetery/actions/runs/43709191890).
The concurrent pointer-only change in reborn #276 is preserved; historical case
links resolve to the retained source archive rather than unimported cemetery URLs. Review this cross-repository boundary and mutable local API resolution;
do not infer compatibility from a copied function name alone.

Cemetery batch, saved-scenario and diagnostic screenshot runners explicitly
supply their own toolkit checkout, because isolated Borg source clones cannot
discover it as a sibling. The batch fixture checks that the owned API is present
even when an inherited BORG_CEMETERY_DIR points to a stale location. All 39 own
and 35 native tests pass after this fix; [implementation CI](https://github.com/diegoami/borg-cemetery/actions/runs/43710142197)
and [review-publication CI](https://github.com/diegoami/borg-cemetery/actions/runs/43710159948)
are green. The later integration receipt changes documentation only.

## Owner-requested statistics by build

[Statistics](../../../statistics/README.md) inventories the seven curated local
cases (four builds) and the 2,378 historical reborn dossiers (114 builds) at
`ec9058d18625056154e7f69a21b63036932ff739`. The external files remain in reborn;
only normalized statistical fields and source-file hashes are retained here,
with report links pinned to that revision. No historical IDs are migrated.
One declared/qualified starting-family key occurs in both archives, so the two
registries are not pooled into an independent-life denominator.

Build groups include project, commit, source-input and executable hashes,
implementation and dirtiness. Recorded cores/profiles/settings are shown within
each build. Death causes and terminal turn/depth/level summaries weight retained
dossiers; scenario/human branches and repeated attempts do not become independent
births. This is not a complete CI/all-game cohort or a mortality-rate estimate.

Native registration regenerates local reports, ordinary regeneration preserves
the frozen external inventory, and CI checks that reports are current. Seven new
regression checks cover repeat/family accounting, build separation, absent/saved
seeds, unknown identity, stale outputs, pinned external inputs and living-record
rejection. All 46 own tests and 35 native tests pass; the statistics check passes.

## Known limits and review questions

The owner subsequently requested a [controlled-experiment redesign](../../cemetery-redesign.md).
That document proposes a fixed cohort, complete build/configuration run tracking,
independent near-death qualification and bounded external storage. It is planning
only; it does not implement a new milestone, change M1's implementation pin or
delete evidence. Review current delivered behavior against the M1 contract,
without treating the proposed architecture as already available. The publication
head also includes these design/navigation documents.

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
