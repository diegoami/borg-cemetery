# borg-reborn-rs with the owner's attack-preference and return-trip criteria

A paired run of 90 fresh starts with and without the settings below, at 1,000,000
game turns, plus an audit of why the errands plan's depth cap does not hold.
It follows the watched Gnome Mage incident
([2026-11-16](../../incidents/2026-11-16-watch-gnome-mage-lemure/README.md)), which used these
settings and died on DL13 although the plan caps a level 9 Mage at depth 4.

**Short answer.** (1) The criteria made no measurable difference to survival in this
sample: 51 deaths against 52. (2) The plan's `max-depth` cap does not hold in either arm,
and the main reason is **Scrolls of Deep Descent**, which the Borg reads deliberately. This is
a strong candidate for the watched game's DL13, though that game had no recording and is
not itself explained.

## What was run

| | |
| --- | --- |
| Source | `diegoami/borg-reborn-rs` `f02cd2940a7439a8965b3883270a9a73df7e0bf5`, clean; source hash `bb27c7c3…`; binary `d66bded1…` (the build the watched game used) |
| Core and plan | `BORG_CORE=borg-rs`, `harness/plans/errands_plan.txt` (`084bc3e8…`, [copy](errands_plan.txt)) in both arms |
| Starts | 9 classes × 10 seeds (3000–3089), race = (class + k) % 11, `menu`, 1,000,000 game turns, `harness/run.sh` via `suite.sh` ([suite](suite)) |
| Arms | **criteria** and **control**: identical starts, one difference in `borg.txt` ([diff](criteria-borg.txt.diff)) |
| Result | 90/90 runs completed in each arm, no timeouts or failed runs, `overrides=none` ([criteria manifest](manifest-criteria.txt), [control manifest](manifest-control.txt)) |

Criteria arm settings (everything else is the repository default, including `borg_town_plan = 0`):

- `borg_param_caution_heal_when_outmatched = 1`
- attack preference (permille): warrior melee 1800, projectile 1200, thrown 1200; mage spell 2000, device 1200; druid spell 1700; priest spell 1700; necromancer spell 1800, device 1200; paladin melee 1800, spell 1200; rogue projectile 1300, thrown 1600; ranger projectile 2000; blackguard melee 1600, spell 1400
- return policy on (`borg_trip_policy = 1`), return with 1 pack space left (`borg_trip_pack_slack = 1`), return at 5 eligible unknown stacks (`borg_trip_unknown_stacks = 5`)

The Borg's own parameter table (`params-core.json`) records the values in effect in every run
(for example mage spell 2000 against 1000 in the control, `caution_heal_when_outmatched` 1 against 0).

**Not the same as the watched game:** that game also had `borg_town_plan = 1`, which this list
does not name, so it was left off. Add it as a third arm if an exact match is wanted.

## Survival: no measurable difference

| | criteria | control |
| --- | ---: | ---: |
| Starts | 90 | 90 |
| Died | **51** | **52** |
| Alive at 1,000,000 turns | 39 | 38 |
| Median highest character level | 11 | 11 |
| Median deepest level | 9 | 7 |
| Deepest level reached | 24 | 22 |

Paired by start: both die 41, both live 28, criteria lives and control dies 11, criteria dies and
control lives 10. Only 16 of 90 starts play identical keys in both arms, so most starts are
different lives after the first changed decision. A 11-to-10 split is what chance alone gives.

| Class | Dies: criteria | Dies: control | Median max CL (criteria / control) | Deepest DL (criteria / control) |
| --- | ---: | ---: | --- | --- |
| Warrior | 6/10 | 7/10 | 16 / 15 | 23 / 22 |
| Mage | 2/10 | 4/10 | 12 / 10 | 13 / 11 |
| Druid | 7/10 | 6/10 | 10 / 14 | 20 / 17 |
| Priest | 7/10 | 6/10 | 9 / 9 | 13 / 13 |
| Necromancer | 6/10 | 4/10 | 8 / 9 | 17 / 10 |
| Paladin | 5/10 | 4/10 | 16 / 15 | 24 / 19 |
| Rogue | 5/10 | 7/10 | 14 / 9 | 18 / 18 |
| Ranger | 8/10 | 7/10 | 9 / 11 | 20 / 16 |
| Blackguard | 5/10 | 7/10 | 16 / 17 | 19 / 17 |

Per-class gaps (such as Mage 2 against 4) are 10 starts each and are not evidence of a class effect.
Per-run results are in [results.csv](results.csv).

## The depth cap does not hold, and Deep Descent is why

The plan caps depth by character level and class (a level 9 Mage: 4; levels 10–14: 8). A character
cannot legitimately sit deeper than the cap for its *final* level, since caps only rise with
level. We count runs whose deepest level exceeds that cap:

| | criteria | control |
| --- | ---: | ---: |
| Runs deeper than the cap for their final level | 38 of 90 | 36 of 90 |
| of which fell by Deep Descent | 32 | 29 |
| Runs with at least one Deep Descent fall | 52 | 48 |
| Deaths on a level deeper than the cap for the level at death | 22 of 51 | 18 of 52 |

The mechanism is visible in the logs. In `crit-0-warrior-1` the Borg logs
`# Reading Scrolls of Deep Descent.`, the game says `The air around you starts to swirl...` and
then `The floor opens beneath you!`, and the next arrival is five levels below the previous deepest
level: DL3 → 8 → 13 → 18 over three reads, at character level 6, where the cap is 3. This engine's
Deep Descent counts from the **maximum** depth, so repeated reads compound.

The remaining over-cap runs are mostly one level past a cap of 1 early in the game, plus a
Blackguard that fell through trapdoors; they are minor next to Deep Descent.

**What this means for the watched game.** DL13 is two +5 steps from DL3, and the Mage's cap
at that point was 4. Deep Descent is therefore a plausible mechanism, but the watched game had no
recording and no move log, so it is **not established** for that death. A recorded reproduction
would settle it. The pattern is, however, reproduced as a common event in measured runs of the same
build, in both arms, so it is not caused by the criteria.

The Borg treats the plan's cap as a limit on its own dives and does not veto a scroll that
teleports it past the cap. Whether that is intended is a question for borg-reborn-rs; this report
does not change play and files nothing there.

## Causes of death

51 criteria deaths and 52 control deaths over roughly 40 distinct causes. The most frequent in both arms
are Fang, Farmer Maggot's Dog (4 and 4), crows (2 and 3), wild cats (2 and 2) and Grip (2 and 2);
no cause is concentrated enough to read as an effect of the settings. The full list is in
`results.csv`.

## Limits

- 10 starts per class, one seed set, one build. Descriptive only; no improvement or harm claim.
- The criteria change many things together (preferences for nine classes, healing, trips). The
  comparison cannot say which one matters. A null result for the bundle is not a null for each part.
- The arms are different games after the first changed decision, not the same fight with another
  result. Repeats and continuations of one life are not independent samples.
- "Over the cap" uses the final level, so it undercounts; Deep Descent falls were found from the
  game's own messages, not from a decision trace.
- `borg_town_plan` is off (see above).

## Evidence

- In Git here: [results.csv](results.csv) (both arms, per start, with the first 16 hex digits of each
  key stream's SHA-256), [suite](suite), [plan](errands_plan.txt), the [settings diff](criteria-borg.txt.diff),
  both manifests, and the scripts [`compare.py`](compare.py) and [`deep_descent_audit.py`](deep_descent_audit.py)
  that produced the tables (they read the raw suite outputs and are not runnable from this directory alone).
- **Not in Git** (about 37 GB of raw logs and 277 MB of exported death dossiers): the 103 natural
  deaths were exported with the pinned native tools (`586d0c13`) into two scratch registries, now kept
  outside the repository at `/home/diego/borg-cemetery-evidence/2026-11-17-criteria-attack-trip/`
  (`dossiers-criteria`, `dossiers-control`, both with the old sequential numbering). They have **not**
  been registered in [deaths/](../../deaths/README.md): that needs the canonical hash IDs, and about
  2 MB each would add roughly 280 MB to the repository. Say if you want them imported, or a
  subset such as the deaths deeper than the cap.
- Raw outputs stay in the run's scratch directory and may be cleared; the per-run key hashes allow
  a check of any rerun.
