# Low-level caster scenario bank

Owner-directed expansion after reborn #378: prioritize low-level casters and observed equipment combinations. This is separate from the frozen M2 Warrior pilot and does not accept a milestone or authorize P2/P3 population comparisons.

## Incident extraction

`candidates.json` indexes preserved evidence at Cemetery commit `5f81ac33ca5d8626191e671388272da63d0b4af3`. Each record, selected frame and retained compressed save has a SHA-256 reference. Published frame hashes are checked; mismatches abort extraction. Five frames without published hashes are explicitly excluded, not silently recovered. The scan covers selected frames, not every turn of every recording.

There are 14 cases at observed levels 1–10, 52 distinct full inventory/equipment configurations within those cases, and 37 low-HP observations. Configuration counts include pack changes; they are not 52 equipment experiments. Eight existing caster save scenarios are indexed: two near-death candidates, five death checkpoints and one with an unspecified event kind. Multiple checkpoints, configurations and observations of a life are correlated. No near-death qualification or original-continuation verification is asserted.

| Case | Character | Observed levels | Full kit configurations |
|---|---|---|---:|
| [D0007-collected](../../deaths/D0007-collected/record.json) | Measure Gnome Mage | 4 | 6 |
| [D0008-collected](../../deaths/D0008-collected/record.json) | Measure Human Priest | 1 | 7 |
| [D0009-collected](../../deaths/D0009-collected/record.json) | Measure Half-Troll Necromancer | 10 | 1 |
| [D0013-collected](../../deaths/D0013-collected/record.json) | Measure Dunadan Druid | 1 | 7 |
| [D0015-collected](../../deaths/D0015-collected/record.json) | Measure Dunadan Necromancer | 1 | 1 |
| [D0016-collected](../../deaths/D0016-collected/record.json) | Measure Human Necromancer | 1 | 2 |
| [D0018-collected](../../deaths/D0018-collected/record.json) | Measure Dunadan Druid | 2 | 7 |
| [D0019-collected](../../deaths/D0019-collected/record.json) | Measure Half-Troll Necromancer | 2, 3 | 1 |
| [D0020-collected](../../deaths/D0020-collected/record.json) | Measure Human Priest | 3 | 7 |
| [D0021-collected](../../deaths/D0021-collected/record.json) | Measure Elf Necromancer | 1 | 2 |
| [D0025-collected](../../deaths/D0025-collected/record.json) | Measure Human Necromancer | 2, 3 | 2 |
| [D0027-collected](../../deaths/D0027-collected/record.json) | Measure Kobold Mage | 9 | 1 |
| [D0028-collected](../../deaths/D0028-collected/record.json) | Measure Half-Orc Mage | 7 | 7 |
| [D0029-collected](../../deaths/D0029-collected/record.json) | Measure Elf Necromancer | 1 | 1 |

Only player-visible item descriptions are projected. Diagnostic `actual_kind` fields are excluded. Missing inventory/spell observations remain unknown. These descriptions do not encode every engine item flag, stat, HP roll or knowledge bit, so none is passed off as an executable build record.

## Executed birth matrix

Four race/class starts: Gnome Mage, Human Priest, Dunadan Druid, Elf Necromancer. Seed 202, depths 1/3/5, 3,000 engine-turn cap, 30 seconds per case. These are generated initial conditions with ordinary birth kits and a fresh Borg, not reconstructions of the indexed incidents. Birth-kit normalization and the one-way dungeon contract are inherited from the runner. Class and race vary together; this matrix cannot isolate either effect.

Runtime: `83da6679c76dfa2a0bee369b3d839a364422e4a4`.

Source digest: `2d1420b704fa8faa4a1972fe9548fdd2ebaa2a5fde98c9ff7ce9f4ba51d2ecef`.

Binary digest: `f8233c8c4f96803b373807744999b9d9b68e607d3c14612e93ee1312cda8a668`.

Both attempts: **12/12 valid, 8 deaths, 4 cap survivals, zero execution failures**. The repeated attempts match all 36 key/state/message streams. Repetition establishes this local determinism check, not independent sample size or an improvement. Full outcomes and stream hashes are under `evidence/attempt-{1,2}/`; raw attempts remain outside Git at `/workspace/work/caster-birth-attempt-{1,2}`. Synthetic deaths stay outside the natural death registry.

The existing runner includes sampled HP=0 under its historical “minimum living HP” label; treat that field as sampled pre-key HP, not a proof that zero HP is safe. The birth runner uses an absolute HP<=2 candidate screen; the incident extractor separately uses living HP<=25% maximum. Neither is qualified near-death coverage.

## Run and review

```sh
python3 scripts/caster_candidates.py --out /tmp/caster-candidates.json
python3 -m unittest discover -s tests
python3 scripts/synthetic_suite.py run --manifest synthetic/low-level-casters/suite.json --source /path/to/clean-built-reborn-83da --out /tmp/caster-attempt
python3 scripts/synthetic_suite.py verify --actual /tmp/caster-attempt/results.json --expected synthetic/low-level-casters/evidence/attempt-1/results.json
```

Use a new output path for every attempt. Rebuild/source identity checks apply; another toolchain may yield a different binary hash, which must be retained rather than relabeled. Candidate regeneration on this branch has identical cases/saves/exclusions; its `input_commit` records the actual checkout rather than rewriting the historical input pin.

## Equipment execution dependency

Reborn [#382](https://github.com/diegoami/borg-reborn-rs/issues/382) owns the caster build-application extension. Current record application supports Human Warrior only. All 52 observed configurations remain `requires_caster_build_adapter`. Save scenarios require original-build qualification and fresh-Borg restart semantics; they do not gain current-build compatibility from appearing here.

Next equipment selection should use the observed equipped slots, pack resources and spell state together: preserve an observed baseline, then specify matched armor/weight, casting-stat/protection and escape-stock variants with explicit assumptions. Do not infer spell success or manufacture missing item properties from descriptions. The source contract must retain learned/forgotten spell state, book availability, mana recalculation, item legality/knowledge and fail-closed tests before these variants run.

Reviewer: inspect the extractor’s hash/path checks and knowledge boundary, regenerate the candidate projection, check the 12-case matrix and repeated stream receipts, and verify that unsupported equipment and saved-state qualifications are visible. The owner selects/runs the reviewer.
