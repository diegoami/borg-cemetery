# Results: class preference profile smoke

**18/18 runs completed and verified; no game crash, timeout or configuration
failure.** Nine paired open-suite starts, exact100000 engine-turn cap. Both
arms used the same real executable and tracing. All54 preference parameters
were inspected per run: only profile-specified values differed from defaults,
with provenance `borg.txt`, not environment overrides.

Profiles are editable in [profiles/](profiles/); engine facts and the rationale
are in [README.md](README.md) and [engine-class-facts.json](engine-class-facts.json).
The initial numerical examples were superseded before any game ran. Profile
commit3230269d5a155529b4c8568cdc151638c77a02e1 was published before execution.
These coefficients are hypotheses informed by class mechanics; class.txt itself
contains no utility-permille preference settings, and the native evaluator already
uses class-derived accuracy, blows, damage and spell mechanics.

## Observed outcomes

Level/depth columns are terminal character level / maximum dungeon depth.
Changed rankings count configured-state invocations whose weighted winner differs
from the raw winner in that same state. They are not matched neutral-game turns.

| Class | Neutral outcome | Level / depth | Profile outcome | Level / depth | Changed rankings | Keys changed |
| --- | --- | --- | --- | --- | ---: | --- |
| Warrior | alive at100000 | 7 / 3 | alive at100000 | 7 / 3 | 0 | no |
| Mage | alive at100000 | 4 / 1 | alive at100000 | 3 / 1 | 1 | yes |
| Druid | death at9547 | 1 / 1 | death at9547 | 1 / 1 | 0 | no |
| Priest | alive at100000 | 4 / 2 | alive at100000 | 4 / 2 | 0 | no |
| Necromancer | alive at100000 | 5 / 2 | alive at100000 | 3 / 2 | 3 | yes |
| Paladin | alive at100000 | 4 / 2 | alive at100000 | 4 / 2 | 0 | no |
| Rogue | death at4923 | 1 / 1 | death at4923 | 1 / 1 | 0 | no |
| Ranger | alive at100000 | 7 / 2 | alive at100000 | 7 / 4 | 34 | yes |
| Blackguard | alive at100000 | 3 / 2 | alive at100000 | 3 / 2 | 0 | no |

The Ranger reached maximum DL4 versus DL2, with the same terminal CL7. Mage
finished CL3 versus CL4; Necromancer CL3 versus CL5. These are descriptive outcomes
from one paired seed each; neither survival improvement nor an optimal setting
is established. Druid and Rogue died in both arms with identical keys. Six
classes had unchanged key streams in the states reached; that does not establish
that their profile can never matter later or with different equipment.

## Direct selection examples

- Mage turn42945: raw melee16 beats Magic Missile14; spell2000 makes Magic
  Missile28 and changes the winner.
- Necromancer turn9957: raw melee6 ties Nether Bolt6, so the earlier melee
  candidate wins; spell1800 raises Nether Bolt to10.
- Ranger turn64492: raw thrown-object4 ties launch4; projectile2000 makes
  launch8 and changes the winner.

No runtime policy, class.txt, production default or Zoo catalogue was edited.
The configuration writer and command builder come from a clean git-archive of
pinned Zoo c5f1b0429ea898c8d5484aa4f1ac0d681972aac7. Complete key/message/state logs,
traces, profile/config bytes and per-game process records remain in
/workspace/work/class-profiles-20261116-01. Their hashes and summaries are retained
in results.json and attempts/. Source/build identity is the main-promoted runtime
290fd89e with executable29936aa5, actually built at8e007cdd; it is not relabeled
as a build of the promotion commit4a2cb910.

## Retained runner defect

The first runner used `name` for the subdirectory-creation loop, replacing its
receipt label with `scores`. That caused a shared root supervisor text log and
root attempt-file overwrites. It did not alter per-game paths, parameters,
commands or engine execution. All18 unique game directories/process receipts and
all18 in-memory attempt objects in the final results survive. Original results,
runner-used.py, scores.attempt.json and the mixed scores.supervisor.log are kept
unchanged. attempts/ contains derived receipts adding a class/arm identity while
retaining the original label; none substitutes for the original evidence.
run.py now fixes the local variable name for future use. No game was rerun,
dropped or relabeled as a new independent sample because of this defect.

## Death custody

Four natural-death packets (paired Druid and Rogue starts) are source-qualified
in the parent deaths/ archive, retaining original records and payload bytes.
They are four configuration-specific packets from two paired starts, not four
independent birth seeds. The complete archive verifies110 qualified packages.
Reconciliation against these retained packets and run outputs is recorded in
reconciliation.txt; package counts are not population denominators.

The initial reconciliation command scanned the whole working root, including
copied death packets and pinned-Zoo historical examples, and counted the copied
packet summaries again. That diagnostic is retained separately. The corrected
command enumerates all18 actual game directories, finding4 natural deaths and
zero unexported/unrecorded cases; it excludes no measured attempt.
