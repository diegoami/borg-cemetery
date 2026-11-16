# Death records

This directory is the cemetery's archive of **dossiers**: one folder per
confirmed natural death of a Borg (an automatic player) in Angband. A dossier says
*what* died, *on which source build, configuration and seed*, *how*, and what is
known about *why*. It is the place to start from when you want to read a death,
replay it, or look for patterns across deaths.

A death alone does not establish a bug. Every dossier keeps observations
(native facts) apart from hypotheses, and an assessment never changes game play
by itself.

## How to use it

- **Browse:** [CATALOG.md](CATALOG.md) lists every dossier with its canonical ID,
  seed, source commit, cause and death turn. Each entry opens the case's landing
  page (`README.md`), with the character, build, replay/watch commands and the
  original report.
- **Look up an old name:** the `D0001`-style numbers are aliases. Canonical
  identities are `D-<64 hex digits>` (a SHA-256 of the encounter family and the
  original key stream). [ALIASES.json](ALIASES.json) maps one to the other; the
  rule is in [../docs/death-identity.md](../docs/death-identity.md). Never
  allocate a "next number".
- **Read the patterns:** [../statistics/README.md](../statistics/README.md) groups
  deaths by build, cause, character and depth, and
  [../docs/death-analysis.md](../docs/death-analysis.md) is the cross-case
  survival analysis.

## What is in here (88 dossiers, 2026-11-17)

| Group | Dossiers | Source | What they are |
| --- | ---: | --- | --- |
| `D0001`–`D0004` (`-seedNNNN-class`) | 4 | borg-rs `f772eb6d` | First imported nine-class cohort, 2026-11-07 ([cohort page](cohort-2026-11-07.md)) |
| `D0005`, `D0006` (`-recorded`) | 2 | borg-rs | Recorded games with original recordings ([release](https://github.com/diegoami/borg-cemetery/releases/tag/recordings-2026-11-15)) |
| `D0007` | 1 | borg-reborn-rs `e9a6a521` | Seed 102 validation birth: report, GIF, three playable scenarios |
| `D0006`–`D0030` (`-collected`) | 25 | better-borg-c (C Borg) | Natural deaths collected from CI, several builds |
| `D0031`–`D0068` (`-rust-seedNNN`) | 38 | borg-reborn-rs `8a0b57c8` | Zoo #123 small tier, plan and town arms ([run report](../runs/2026-11-16-zoo-reborn-plan-m13-small/README.md)) |
| `D0069`–`D0086` (`-rust-seedNNN`) | 18 | borg-reborn-rs `4ecb93d7` | Zoo #138 small tier with the #423 survival fixes ([run report](../runs/2026-11-16-zoo-reborn-survival-small/README.md)) |

Numbers repeat between the two lineages (for example `D0006` and `D0007` exist
twice, once recorded and once collected); the canonical `D-…` IDs are unique.

These are **records, not a sample**. Counts here are not a survival rate or a
mortality denominator: starts that survived are not stored, repeats and
alternative continuations of one life are not independent lives, and different
groups ran on different builds and settings. Use the zoo's reports for
comparisons across builds.

## What a dossier contains

| File | Purpose |
| --- | --- |
| `README.md`, `report.md` | Human-readable landing page and written report |
| `record.json`, `death-id.json` | Immutable identity (source, build, configuration, seed, key-stream hash) and the canonical ID |
| `summary.json`, `build.json`, `config.txt` | Run summary, build identity and the Borg's configuration for that life |
| `assessment.json` | Curated findings and linked actions; evolves, the identity does not |
| `params-core.json`, `trace-core-tail.jsonl` | Native Borg parameters and the last decisions before death |
| `errands_plan.txt` | The plan the Borg followed, when it had one |
| `REPLAY.md`, `play.sh`, `watch.sh`, `build.sh` | Commands to rebuild the exact source and replay or watch the death |

Raw logs, saves and builds stay outside Git; their SHA-256s are recorded in
`record.json`. Older dossiers may lack some files, and say so on their page.

## How a death gets here

1. A measured run (borg-reborn-rs `harness/run.sh`, or a zoo/CI run) ends in a
   natural death. Constructed, synthetic and loaded-save lives are excluded
   ([why](../docs/native-death-tools.md)).
2. `scripts/native/export-death.py` writes the dossier under its canonical ID.
3. `scripts/register_deaths.py` builds the landing page, refreshes the
   [catalogue](CATALOG.md), aliases and [statistics](../statistics/README.md).
   Run `python3 ../scripts/death_ids.py --check` before delivering.

Incidents that are not natural measured deaths (a watched game without a
recording, for example) live in [../incidents](../incidents), not here.

## Historical registry (the first seven cases)

The table and actions below are the curated registry of the first imported cases,
kept as written. They show the original registry statistics: six distinct starting
conditions and 14 retained attempts, plus one selected validation birth (D0007).
Neither is a survival-rate estimate. Cases after these have their own pages and are
listed in the [catalogue](CATALOG.md).


| Case | Discussion | Actual source | Seed | Raw cause | Death turn | Diagnosis |
| --- | --- | --- | --- | --- | --- | --- |
| [D0001](D0001-seed8400-warrior/README.md) | unassigned | `f772eb6dcb93` | 8400 | a pseudo-dragon | 37680 | C/Rust parity observed; defect not established |
| [D0002](D0002-seed8402-druid/README.md) | unassigned | `f772eb6dcb93` | 8402 | a cutpurse | 5590 | C/Rust parity observed; defect not established |
| [D0003](D0003-seed8406-rogue/README.md) | unassigned | `f772eb6dcb93` | 8406 | a giant yellow centipede | 5600 | C/Rust parity observed; defect not established |
| [D0004](D0004-seed8408-blackguard/README.md) | unassigned | `f772eb6dcb93` | 8408 | a wild cat | 6231 | C/Rust parity observed; defect not established |
| [D0005](D0005-recorded/README.md) | [Discuss](https://github.com/diegoami/borg-rs/issues/3) | `9881301ceaad` | 1532917772 | Fang, Farmer Maggot's Dog | 36289 | Fang death assessed; recovery/retreat gates and spell-confidence causality unresolved |
| [D0006](D0006-recorded/README.md) | [Discuss](https://github.com/diegoami/borg-rs/issues/3) | `aa4ad6cfeea2` | 2647001198 | a grey mold | 22841 | Grey-mold stair/exploration loop assessed; qualified private trace shows emergency movement and danger-cache reuse |
| [D0007](D0007/README.md) | unassigned | `e9a6a521f3ac` | 102 | Fang, Farmer Maggot's Dog | 3640 | Written report, GIF and three playable scenarios; one saved-position comparison |

## Aggregated actions

- Prioritize escape-stock/restocking and the decision to descend. A controlled rerun from original birth is needed before attributing survival to another policy; loading the prior engine save starts fresh Borg memory. — recorded; needs causal investigation; cases D0001.
- Investigate avoiding adjacent lethal encounters with exhausted mana and minimal starting resources. No port-specific defect or guaranteed unused known escape is established. — recorded; needs causal investigation; cases D0002.
- Investigate emergency unknown-scroll policy and earlier avoidance. The actual hidden kind is diagnostic information, not knowledge available to the Borg. — recorded; needs causal investigation; cases D0003.
- Prioritize a controlled healing-versus-finishing-attack counterfactual. Last-checkpoint stock alone is not proof a particular alternative would survive; no tactical change is made from this observation. — recorded; needs causal investigation; cases D0004.
- [D0005: observe exact recovery, retreat/stairs and competing attack gates on original source before any change](https://github.com/diegoami/borg-rs/issues/4) — open; next discriminating evidence, no gameplay change; cases D0005.
- [D0005: compare separately a specified CLW and legal NW diagnostic branch after private-gate qualification](https://github.com/diegoami/borg-rs/issues/4) — provisional; not executed, depends on exact gate trace; cases D0005.
- [D0005: qualify simultaneous native/Borg spell confidence and coordinate existing ambient-light296 through C consumer](https://github.com/diegoami/borg-rs/issues/4) — open; existing source lead, no duplicate C report or immediate adoption; cases D0005.
- [D0006: construct legal native mode-transition cache scenario with emergency/safe/blocked controls; coordinate existing C ownership before any correction](https://github.com/diegoami/borg-rs/issues/5) — open; next discriminating evidence, no gameplay change; cases D0006.
- [D0006: separately test stair descent/hold/door-close and one adjacent mace attempt with declared source/RNG/continuation limits](https://github.com/diegoami/borg-rs/issues/5) — provisional; no alternate-action branch run, distinguish serialized human branch from uninterrupted private-state continuation; cases D0006.
- [D0006: explain actual CSW-sale and fuel/escape reserve choices from native inventory-power/shop score trace](https://github.com/diegoami/borg-rs/issues/5) — open; evidence before policy change; cases D0006.

[Earlier nine-class cohort and assessments](cohort-2026-11-07.md) · [Feedback process](FEEDBACK.md) · [Review template](REVIEW-TEMPLATE.md).

Original-C defect leads go to neo-angband-tracker under the repository policy; no automatic issues or gameplay changes are made by the logger.

[Download and replay the original D0005 and D0006 recordings](https://github.com/diegoami/borg-cemetery/releases/tag/recordings-2026-11-15). Each case has written download and playback instructions.

[Survival-analysis pass and ranked experiments](../docs/death-analysis.md) · [Complete catalogue](CATALOG.md).
