# Suite 2 preparation — incomplete

Owner request: [borg-zoo#184](https://github.com/diegoami/borg-zoo/issues/184).
This directory freezes the intended preparation; **no Suite 2 bank is frozen**.
Suite 1 remains byte-for-byte unchanged.

The requested source is borg-reborn-rs
`50ae902a68a8732d56a6e1adf47deca4a9db7d7f`, with the commit's own borg-rs
controller and `harness/borg.txt`. `harvest-spec.json` fixes its settings hashes,
native tools, checkpoint cadence, disjoint preparation/smoke seeds, races,
incident definitions, limits and exact class quotas. `exclude-suite1.json`
contains Suite 1's 999 initial save hashes and original source-life seeds.

## Failed smoke and retained evidence

[Zoo run 44121110906](https://github.com/diegoami/borg-zoo/actions/runs/44121110906)
built this source and attempted 12 natural lives per class: 108 lives total,
99 reached the cap and 9 died. **Zero saved starts were qualified.** Every
attempt failed at incident extraction because the expected `encounters.jsonl`
was absent. No full harvest or new suite execution was dispatched.

`preparation-44121110906/` retains every attempted-life journal, configuration,
build and process receipt, and every native natural-death packet (including
payload bytes and canonical death IDs). `evidence.json` records class counts
and original archive hashes. All nine complete raw archives, including every
checkpoint and stream, are retained as release assets at
[the failed preparation release](https://github.com/diegoami/borg-cemetery/releases/tag/suite2-preparation-44121110906).
These are failed preparation inputs, not runnable bank cases, not observed
critical recoveries, and not a completed 999-encounter suite.

## Capture interface needed on the requested source

The source does not implement `BORG_ENCOUNTER_LOG`. Its
`BORG_OBSERVATION_LOG` and `BORG_KNOWLEDGE_LOG` hooks are inside the separate
reborn controller; its stock borg-rs controller does not emit them. Selecting
a different controller, silently changing the Borg source, inferring a threat
from terminal HP, or treating a terminal save as an encounter onset would
change the request or weaken the incident contract.

Before a new preparation:

- Expose a core-independent native observation interface on borg-rs. It must
  retain player-observable monster/contact episodes, turn/depth and HP/SP,
  initial inventory/equipment and static race-name identity needed by the
  incident miner. Do not expose unseen monsters as observable triggers.
- Verify recording does not change keys, states, messages or saved RNG.
  Include a level-1 caster death and an actual <=25%-HP damage/recovery
  witness; changing the HP ratio through a level-up is not a recovery witness.
- Pin that supported source, exact configuration and logging-tool identities
  in a new immutable preparation record. Preserve the failed record above.
- Pass the all-class preparation smoke and bounded 18-case restart smoke
  before the already requested 111-per-class harvest. Freeze only after all
  999 starts validate and source/save overlap and coverage are reported.

The harvest preflight now rejects this known missing capture interface before
starting more natural lives. It remains a negative capability check; detecting
an interface name in source is not a replacement for native smoke validation.
