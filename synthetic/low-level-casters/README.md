# Low-level caster scenario bank

Owner-directed expansion after reborn #378: prioritize low-level casters and observed equipment combinations. This is separate from the frozen M2 Warrior pilot and does not accept a milestone or authorize P2/P3 population comparisons.

## Incident extraction

`candidates.json` indexes preserved evidence at Cemetery commit `58f9ba3b0afa1bd5979008cc748f8cc3a4a694bd`. Each record, selected frame and retained compressed save has a SHA-256 reference. Published frame/save hashes are checked; mismatches abort extraction. Record hashes are computed from the checked-out bytes and, where available, checked against the canonical death-identity sidecar. They are not independently published recording digests. The input tree must have no tracked or untracked changes under `deaths/` or `scenarios/`. Historical paths remain aliases; each case includes its canonical death identity and sidecar reference.

**Coverage: 14 caster dossiers have usable selected frames; another 37 low-level caster dossiers have no recorded frames** (13 Druid, 9 Mage, 8 Necromancer, 7 Priest). The latter are individually indexed under `unobserved_cases` with `no_recorded_frames`, terminal level and unknown inventory/spells. They are not silently omitted or treated as reconstructed scenarios. Five frames without published hashes are explicitly excluded; these belong to non-caster records.

The 14 observed dossiers cover levels 1–10 and exactly 98 selected observations: seven fixed frames per case, T−105, T−82, T−60, T−40, T−25, T−12 and T−5 before death. This is the last roughly 100 engine ticks, not full-run coverage or an inventory-development history. There are **41 living low-HP observations**, including four alive at HP=0 (`dead: 0`); dead or unknown-death-state frames are not screened as living.

The previous headline of 52 configurations was a count of raw description signatures, including consumable quantities and changing torch fuel. It is retained only as raw observation provenance. With fuel and stack quantities normalized, the bank has **14 equipment-only sets and 21 pack-only type sets**. Every case has one equipped set throughout its sampled window: no within-case equipment swap was observed. The normalized sets ignore pack order, duplicate stacks and aggregate weight, and fold the recorded English plural forms; they preserve visible bonuses. They are description comparisons, not complete engine item identities or executed equipment experiments.

Eight existing caster save scenarios are indexed: two near-death candidates, five death checkpoints and one with an unspecified event kind. Multiple checkpoints, configurations and observations of a life are correlated. No near-death qualification or original-continuation verification is asserted.

| Case | Character | Observed levels | Equipment sets | Pack type sets |
|---|---|---|---:|---:|
| [D0007-collected](../../deaths/D0007-collected/record.json) | Measure Gnome Mage | 4 | 1 | 2 |
| [D0008-collected](../../deaths/D0008-collected/record.json) | Measure Human Priest | 1 | 1 | 2 |
| [D0009-collected](../../deaths/D0009-collected/record.json) | Measure Half-Troll Necromancer | 10 | 1 | 1 |
| [D0013-collected](../../deaths/D0013-collected/record.json) | Measure Dunadan Druid | 1 | 1 | 1 |
| [D0015-collected](../../deaths/D0015-collected/record.json) | Measure Dunadan Necromancer | 1 | 1 | 1 |
| [D0016-collected](../../deaths/D0016-collected/record.json) | Measure Human Necromancer | 1 | 1 | 2 |
| [D0018-collected](../../deaths/D0018-collected/record.json) | Measure Dunadan Druid | 2 | 1 | 1 |
| [D0019-collected](../../deaths/D0019-collected/record.json) | Measure Half-Troll Necromancer | 2, 3 | 1 | 1 |
| [D0020-collected](../../deaths/D0020-collected/record.json) | Measure Human Priest | 3 | 1 | 1 |
| [D0021-collected](../../deaths/D0021-collected/record.json) | Measure Elf Necromancer | 1 | 1 | 2 |
| [D0025-collected](../../deaths/D0025-collected/record.json) | Measure Human Necromancer | 2, 3 | 1 | 2 |
| [D0027-collected](../../deaths/D0027-collected/record.json) | Measure Kobold Mage | 9 | 1 | 1 |
| [D0028-collected](../../deaths/D0028-collected/record.json) | Measure Half-Orc Mage | 7 | 1 | 3 |
| [D0029-collected](../../deaths/D0029-collected/record.json) | Measure Elf Necromancer | 1 | 1 | 1 |

Only player-visible item descriptions are projected. Diagnostic `actual_kind` fields are excluded. Spell metadata and learned-spell entries both use explicit field whitelists. A caster frame with missing spell observations is retained using recorded class metadata where available, with missing spell state explicit; conflicting class metadata is explicitly excluded. Missing inventory/spell observations remain unknown. These descriptions do not encode every engine item flag, stat, HP roll or knowledge bit, so none is passed off as an executable build record.

## Executed birth matrix

Four race/class starts: Gnome Mage, Human Priest, Dunadan Druid, Elf Necromancer. Seed 202, depths 1/3/5, 3,000 engine-turn cap (about 300 player turns), 30 seconds per case. These are generated initial conditions with ordinary birth kits and a fresh Borg, not reconstructions of the indexed incidents. Birth-kit normalization and the one-way dungeon contract are inherited from the runner. In the retained attempts, all 8 depth-3/5 starts read the inherited, inert Word of Recall scroll at engine turn 11 (key positions 6 or 7), producing “Nothing happens.” and consuming the scroll; none of the 4 depth-1 starts does. This opening resource/action difference confounds depth: the matrix cannot isolate a pure depth effect. Class and race vary together; this matrix cannot isolate either effect.

Runtime: `83da6679c76dfa2a0bee369b3d839a364422e4a4`.

Source digest: `2d1420b704fa8faa4a1972fe9548fdd2ebaa2a5fde98c9ff7ce9f4ba51d2ecef`.

Binary digest: `f8233c8c4f96803b373807744999b9d9b68e607d3c14612e93ee1312cda8a668`.

Both attempts: **12/12 valid, 8 deaths, 4 cap survivals, zero execution failures**. The four cap survivals each cover only 300 player turns (3,001–3,003 engine ticks at the stop boundary). The two capped Elf Necromancers remain level 1, visiting only 19 and 42 distinct positions. These are short bounded survival observations, not successful progression. The repeated attempts match all 36 key/state/message streams. Repetition establishes this local determinism check, not independent sample size or an improvement. Full outcomes and stream hashes are under `evidence/attempt-{1,2}/`; raw attempts remain outside Git at `/workspace/work/caster-birth-attempt-{1,2}`. Synthetic deaths stay outside the natural death registry.

The existing runner includes sampled HP=0 under its “minimum living HP” label. In the incident extractor, an explicit alive flag includes HP=0 in the living low-HP screen; unknown or dead flags do not. The birth runner uses an absolute HP<=2 candidate screen; the incident extractor separately uses living HP<=25% maximum. Neither is qualified near-death coverage.

## Run and review

```sh
python3 scripts/caster_candidates.py --out /tmp/caster-candidates.json
python3 -m unittest discover -s tests
python3 scripts/synthetic_suite.py run --manifest synthetic/low-level-casters/suite.json --source /path/to/clean-built-reborn-83da --out /tmp/caster-attempt
python3 scripts/synthetic_suite.py verify --actual /tmp/caster-attempt/results.json --expected synthetic/low-level-casters/evidence/attempt-1/results.json
```

Use a new output path for every attempt. Rebuild/source identity checks apply; another toolchain may yield a different binary hash, which must be retained rather than relabeled. Candidate regeneration on this branch has identical cases/saves/exclusions; its `input_commit` records the actual checkout rather than rewriting the historical input pin.

## Equipment execution dependency

Reborn [#382](https://github.com/diegoami/borg-reborn-rs/issues/382) owns the caster build-application extension. Current record application supports Human Warrior only. All 14 observed cases, including their normalized equipment/pack sets, remain `requires_caster_build_adapter`. The 37 frame-less dossiers also require observation capture before a build can be reconstructed. Save scenarios require original-build qualification and fresh-Borg restart semantics; they do not gain current-build compatibility from appearing here.

Next equipment selection should use the observed equipped slots, pack resources and spell state together: preserve an observed baseline, then specify matched armor/weight, casting-stat/protection and escape-stock variants with explicit assumptions. Do not infer spell success or manufacture missing item properties from descriptions. The source contract must retain learned/forgotten spell state, book availability, mana recalculation, item legality/knowledge and fail-closed tests before these variants run.

Reviewer: inspect the extractor’s hash/path checks and knowledge boundary, regenerate the candidate projection, check the 12-case matrix and repeated stream receipts, and verify that unsupported equipment and saved-state qualifications are visible. The owner selects/runs the reviewer.
