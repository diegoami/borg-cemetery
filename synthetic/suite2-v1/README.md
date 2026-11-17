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
and original archive hashes. The complete original raw Actions artifacts are retained for 90 days.
`native-death-streams.tgz` permanently retains every raw file and checkpoint
from all nine measured natural deaths; its member hashes and archive digest
are in `native-death-streams.json`. The corresponding compact native packets
retain their original payload hashes and canonical death IDs.
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


## Capture-enabled continuation authorized by the owner

The owner authorized source capture support after the failed smoke. The next
preparation pins borg-reborn-rs candidate `ba26c2abc378302c7d37d4337775d3bd5fe5ad30`
([source PR #508](https://github.com/diegoami/borg-reborn-rs/pull/508)), based on
main `28360152`, with that commit's own stock settings. Capture-on/off native
checks preserve full keys/state/messages and final engine RNG on both
controllers; native compact/full channels also match. The first native state
of four saved-start loads is captured at exactly the saved turn.

The updated immutable Git snapshot of `harvest-spec.json` records this source,
configuration and the core-independent capture interface. Its smoke uses new
seeds starting at 3,000,000, separate from the earlier failed smoke and the
requested full bank's seeds at 2,000,000. The old failed preparation and all
nine natural-death packets/streams remain under `preparation-44121110906/`.
No source PR merge or review acceptance is implied. This is an explicitly
pinned candidate preparation, not a claim that the candidate is main.


## Final collection-controller choice

The capture-enabled stock borg-rs smoke (Zoo run 44129811981) found two
qualified starts in each of eight classes, but none in 32 Blackguard lives.
Those 32 Blackguards all reached 100,000 turns, at levels 2–8 and depths 1–5,
without a death or observed <=25%-HP recovery. This is a coverage shortage,
not a capture-interface failure. A separate one-million-turn Blackguard pilot
ended in starvation at turn 982,010; the first starvation warning was at
914,500, so it is not a qualifying 2,000-turn encounter. Its natural death
and complete raw evidence are retained under
`validation/borg-reborn-rs/encounter-capture-506/blackguard-long-pilot/`.

For Suite 2 **preparation**, use the same `reborn` controller used to harvest
Suite 1, on new source candidate `ba26c2abc378302c7d37d4337775d3bd5fe5ad30`,
with its own default reborn parameter profile. This explicit controller
override is recorded in the manifest and native receipts; it is not described
as the shipped borg-rs configuration. It changes how the bank is collected,
not the supported controller of a subsequent suite run. Stock borg-rs can be
run on these exact saved starts with its separately pinned configuration.
Do not compare outcomes across the two preparation banks as paired results.

The full seed allocation, exclusions, class quotas, incident definitions,
level-1 capture, initial-save deduplication, 2,000-turn horizon and 5-second
restart bounds are unchanged. Freeze this recipe before the next all-class
smoke, and dispatch the full requested harvest only after it succeeds.


## Owner correction: resume with default borg-core

The owner rejected the experimental reborn controller and instructed the
harvest to resume with borg-reborn-rs's default `borg-rs` / vendored borg-core.
This supersedes the collection-controller choice above. The source remains
capture-enabled candidate `ba26c2ab`, with its own unchanged shipped settings.
The expanded all-class smoke searches up to 256 lives per class for two
qualified starts. The requested full harvest retains a maximum 1,024 lives
per class and the exact 111-save quota. A 3 GiB retained-evidence bound leaves
room for the final raw upload; exhausting a bound is a reported shortage,
never permission to duplicate starts or change the <=25% recovery criterion.

Zoo's `resume` dispatch runs the expanded smoke and its native restart gate,
then automatically starts the full harvest on the same pins only if that
smoke succeeds. The experimental-controller smoke is preserved as historical
validation and is not an acceptance gate or input bank for this resumed run.
