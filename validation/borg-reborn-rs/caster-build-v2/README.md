# Native caster build @2 validation

Source increment: reborn #446 / parent #382. Clean runtime commit
`aae2c194a18b9ff943e94aa97a60214f2a231dc2`, source digest
`c97ca9f2a5c8371a3366dc806268880edf29f3c413dbfc3d56f72b5f4c0564a1`,
binary `20bdfe9161b17eae949251acb6b66d0f88653c5a133374d9ed348142fda3ca94`.
Exact compiler/build receipt is in `build.json`; per-run process/config/summary
receipts are retained separately from the full raw logs.

Four ordinary seed-202 capture/control conditions, 20,000 engine-turn cap:
Gnome Mage, Dunadan Druid, Human Priest and Elf Necromancer. Requested capture
level 2. Mage/Priest/Necromancer produce the three observed records here; Druid
has an explicit absent capture because it dies at level 1. No state is invented
for it. All four capture/control pairs match keys, state and messages (12/12
stream pairs). This checks read-only capture on these supported runs, not all
possible unsupported items/effects. Birth-level support for all four classes is
also tested by the source's native contract tests.

The three records include actual learned/worked flags and learning order,
partial HP/SP, base stats and mundane carried/equipped kit. They are observations,
not representative population averages. See `catalog.json` for record hashes,
source selection and capture receipts. Source schema @2 preserves integral
observed HP/SP; fractional resources reset, nutrition normalizes to birth, and
other historical knowledge/private Borg state is not restored.

Each record is applied through the native harness at depth 3, seed 202, 3,000
engine-turn cap twice: six executions of three starting conditions. Outcomes are
four cap survivals and two Priest deaths. The three repeat pairs match all nine
key/state/message streams. They are synthetic starts, not historical encounter
replays or six independent natural lives. `applied.json` retains every result and
stream digest. They do not qualify near deaths or establish improvement.

Cemetery's portable synthetic-suite build parser/catalog still only accepts @1.
These records are `native_harness_validated`, **not portable-suite qualified**;
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
