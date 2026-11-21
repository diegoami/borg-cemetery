# P6 final reconciliation local evidence (#814)

Exact accepted main07aa4b1e and track-p221a2504 merge at sourcea3635ad8,
treec960c16f. Engine574b618c, donor8c5d000a, accepted native tool pin46978936.
The registry conflict preserves main's new resolved-settings receipt test
and the P6 bounds/provenance test. Subtracting the reviewed P6 additions
recovers exact main registry/parser/test bytes; both subject modules are
exact reviewed #680 code. Main's other runtime/settings/references/pins stay
unchanged. source-proof.json records exact parents, tree and changed paths.

Local native smoke is3/3 identical keys/messages/states against the preserved
main smoke reference. Required checks pass: core568/4 ignored, engine/contract
93/4 skipped, fmt/clippy/workspace/vendor,2293 citations,39 script and96 tool
tests. Build and all gameplay checkouts are clean.

## Named-case results, including negative coverage

All trials use the same historical start: seed1001, race1, class0, menu.
At100000 turns, the old town-limit0 witness no longer changes keys/traces.
A separate fixed300000-turn replay of that same start, default and town-limit0,
also remains equal. These results are retained, not discarded or called a
positive witness. The observed borg_enchanting action is dungeon curse removal,
not town enchanting. No sampling batch or local cohort was run.

Using that observed action, the dungeon-limit0 trial at the original100000 cap
changes the first key at index2711/turn19991, trace think1944/depth1:
default borg_enchanting queues [57344,57344,114,102,111,156]; override
borg_flow_dark queues [50]. The named-dungeon-override params-core.json records
enchant_dungeon_max_turns default5500/value0/origin environment. Town-limit
negative controls keep dungeon default5500. Both complete sides of every
comparison are in runs/. This demonstrates control, not improved play.

There are eight local attempts:3 smoke,2 named100k,2 named300k and1 dungeon
witness paired with the retained default100k. They reuse starts and do not
represent eight independent lives. All stop alive; zero native dossiers or
alias changes are needed.

Broader build compatibility is pending Zoo571, baseline07aa4b1e versus
a3635ad8, pilot first. Old Zoo520 full45 at4e9af99e/d0657712 remains immutable
and is not new-main proof. No broader local batch was run under RULES20.

Source refresh attempted an unbounded fetch of Zoo remote history; it was
stopped before exhausting local disk, and the incomplete cache was removed.
The report's Zoo error is retained. Direct upstream HEAD was independently
observed in checks/t814-zoo-head.txt; the contract checkout stayed at its
retained pin7b373a70. No “nothing new” or complete fresh Zoo-report claim is
made, and no source or pin was changed to resolve this local cache issue.

## Artifact map and reproduction

build/ contains the exact executable (gzip; hash after decompressing) and
BUILD_ID. runs/ preserves original configs, summaries, parameter receipts and
all compressed key/message/state/trace streams, including negative controls.
smoke-reference/ retains the accepted reference bytes. inputs/ pins settings,
smoke suite, engine/core/tool sources. checks/ records every exit and log.
file-manifest.json hashes every other artifact. receipt.json gives exact
source/build pins and first divergence. Quiet harness stdout is retained as-is;
the transcript is the runs/* streams plus effective parameter receipts.

Build the exact source with BORG_IMPL=rust harness/build.sh under the shared
lock. Use Cemetery tools46978936; BORG_CORE=borg-rs, BORG_CORE_OVERRIDES=on,
BORG_ERRAND=none, BORG_STOPSCARED=off, private BORG_DEATH_RECORDS_DIR.
Run harness/suite.sh smoke then harness/diff --suite smoke --expect-impl rust
OUT harness/reference/smoke-borg-rs. For the named start use
harness/run.sh OUT 1001 1 0 CAP menu; CAP100000 for defaults/town0/dungeon0,
CAP300000 for the extended default/town0 trials. Apply exactly one corresponding
BORG_PARAM_ENCHANT_{TOWN,DUNGEON}_MAX_TURNS=0 environment override. No
stale/unknown/incomplete switches. Broader comparisons go to Zoo, not this recipe.

Old0529ff6f/be61aeff receipts stay byte-exact. Their default witness traces
already exist; stdout emptiness is quiet success, not missing evidence.
No runtime/tool implementation, historical ID or population claim is added.
This publication does not accept #814/P6 or authorize a source main merge.
