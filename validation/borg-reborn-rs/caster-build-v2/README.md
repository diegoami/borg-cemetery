# Native caster build @2 validation

Source increment: reborn #446 / parent #382. Clean runtime commit
`aae2c194a18b9ff943e94aa97a60214f2a231dc2`, source digest
`c97ca9f2a5c8371a3366dc806268880edf29f3c413dbfc3d56f72b5f4c0564a1`,
binary `20bdfe9161b17eae949251acb6b66d0f88653c5a133374d9ed348142fda3ca94`.
Exact compiler/build receipt is in `build.json`; per-run process/config/summary
receipts are retained separately from the full raw logs.

Four ordinary seed-202 capture/control conditions, 20,000 engine-turn cap:
Gnome Mage, Dunadan Druid, Human Priest and Elf Necromancer. The initial optional schema-validation capture target was
level 2; it never filtered death collection. Mage/Priest/Necromancer produce the three observed level-2 records here; Druid
has an explicit absent capture because it dies at level 1. Its death is retained and an additional natural level-1 Druid record is now
retained too; no state is invented for it. All four capture/control pairs match keys, state and messages (12/12
stream pairs). This checks read-only capture on these supported runs, not all
possible unsupported items/effects. Birth-level support for all four classes is
also tested by the source's native contract tests.

The three level-2 records include actual learned/worked flags and learning order;
the additional Druid record captures its real level-1 starting state,
partial HP/SP, base stats and mundane carried/equipped kit. They are observations,
not representative population averages. See `catalog.json` for record hashes,
source selection and capture receipts. Source schema @2 preserves integral
observed HP/SP; fractional resources reset, nutrition normalizes to birth, and
other historical knowledge/private Borg state is not restored.

All four records are applied through the native harness at depth 3, seed 202,
3,000 engine-turn cap twice: eight executions of four starting conditions.
Outcomes are four cap survivals, two Priest deaths and two Druid deaths. The
four repeat pairs match all 12 key/state/message streams. They are synthetic starts, not historical encounter
replays or eight independent natural lives. `applied.json` retains every result and
stream digest. They do not qualify near deaths or establish improvement.

Cemetery's portable synthetic-suite build parser/catalog still only accepts @1.
These declarative records are `native_harness_validated`, **not portable-suite qualified**;
`requires_cemetery_v2_adapter` remains explicit. Description-only dossiers in
the incident bank are not converted by this validation. Stat-modifier gear,
charged devices and active status/drain/shapechange remain unsupported.

Ordinary and exact smoke each match all three reference runs' key/state/message
streams. Their initial suite attempts completed gameplay but failed publication
because this environment lacked `bc`; the partial directories and per-game
receipts are indexed as infrastructure failures in `catalog.json`. After adding
the locally installed tool to PATH, separate fresh attempts complete and match.
The failed suite attempts are not silently counted as successful suites.

Four natural death families from capture/controls and baseline checks are
preserved as immutable qualified packages under `../native-controls/deaths/`,
with canonical death-ID sidecars. The source's older pinned native exporter
produces historical numeric aliases; qualification preserves every original
record/payload byte and canonical sidecars supply identity. Repeats do not add
independent deaths. The four new packages pass the source's strict importer
check in an isolated registry before additive identity metadata; canonical IDs
are then independently verified in the full repository. No pre-existing package
payload is changed. Generated indexes/aliases are refreshed.

Raw logs and initial failed suite directories remain outside Git under
`/workspace/work/caster-natural-validation/`. Readable evidence and immutable
compact receipts here are the canonical report; source keeps only brief links.
No Zoo population experiment was dispatched. Zoo pushid comparison remains #144.


## All-death reproduction and fast encounter starts

Owner clarification: **collect every natural death regardless of class/level**.
A level-target build capture is optional projection validation, never a filter.
All four new natural death families now have literal input files, pinned runtime
and game-data manifests, runnable birth recipes and successful death/three-stream
checks under `reproduction/`. The original non-recording executable and data are
cached locally; no remote binary retention is claimed. Recording is unnecessary.

The separate `synthetic/fast-caster-encounters/` bank selects saves at/before
first observable threat contact. It loads directly into an already-built Borg,
so the routine test does not replay each birth. Four cases ran in about2.2s on accepted main,
three times with matching streams. These are fresh-Borg counterfactuals, distinct
from exact birth reproductions. See `DRUID-UNSEEN-RECOVERY.md` for the early Druid
failure motivating the unseen-contact case.

`prior-fixture-union.json` records a byte-preserving additive union of the source's
previously adopted evidence pin77dd467, including its max-depth save archive and
nine prior control packages absent from Cemetery main. Generated union indexes
are regenerated; existing immutable payloads are never replaced. Those historical
controls are not newly measured games in this validation.

Optional recorder probes launched before the owner clarified that recording was
unnecessary remain indexed under `auxiliary_probes`; one initial replay failed
terminal-call verification. They are excluded from scenario/reproduction claims.
No additional recorder work is required by this bank.
