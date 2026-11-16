# Death identity

Death dossiers use `D-<64 lowercase SHA-256 hex digits>`. Sequential numbers,
including `D0000-q…` validation names, are historical aliases. Never allocate
the next number or reserve a range for a branch.

For a measured death, hash the UTF-8 encoding of canonical JSON (sorted keys,
no whitespace) containing these fields:

```json
{"encounter_family":"<retained encounter family>","result_sha256":"<original keys.log SHA-256>","schema":"borg-cemetery/death-id@1"}
```

The implementation is `scripts/native/death_identity.py`. The original
attempt, rather than a sorted set of all attempts, fixes the ID: adding a
replay, annotation or alternative does not change it. Build/configuration and
starting-position distinctions are already represented by the encounter
family. A rebuild of the same source with identical inputs and keys remains
a repeat under the existing exporter contract. Distinct results in one family
have distinct dossier IDs; this does not make them independent lives.

New exports use the ID for both the directory name and `record.json.id`.
Separate branches exporting the same evidence produce the same ID. Different
evidence cannot compete for the next integer. Full hashes avoid abbreviated-ID
collisions; an existing directory with inconsistent identity is an error and
is never overwritten. The local lock still protects atomic export and repair.
Generated catalogues may still require regeneration when branches merge.

## Retroactive assignment and published aliases

Every retained dossier receives additive `death-id.json` metadata containing
its canonical ID, identity basis, published aliases and original `record.json`
SHA-256. Existing directories and captured records/reports stay unchanged.
This preserves published links, original exports, source/build/parent lineage,
embedded file hashes and release archives. A historical `record.json.id`
therefore remains its published alias; consumers use the verified sidecar for
canonical identity. Generated landing pages and statistics display canonical
IDs. Historical reports and frozen review packets retain their original names.

The watched PlanMage guided incident has no measured-run family/key-stream
pair. Its explicitly separate `historical-guided-record` basis hashes its
immutable record, with schema domain separation. It remains a watched incident,
not a newly measured natural death. Unknown schemas or incomplete measured
identities fail instead of receiving fabricated family/result inputs.

```bash
python3 scripts/death_ids.py
python3 scripts/register_deaths.py
python3 scripts/death_ids.py --check
python3 scripts/death_ids.py --resolve deaths/D0007
python3 scripts/death_ids.py --resolve D-<full-hash>
```

`deaths/ALIASES.json` indexes all retained dossiers in `deaths/`, `validation/`
and `runs/`. Aliases are scoped to their retained path. An ambiguous alias or
an ID retained at multiple paths requires the explicit path; lookup never
silently chooses one. This index is a lookup tool, not a population registry.
For example, `D0007` already names both an original and a collected dossier;
use `deaths/D0007` or its full canonical ID to select the intended evidence.
Original death counts, independence qualifications and synthetic exclusions
are unchanged. The checker verifies every sidecar against retained evidence
and checks that the alias index is current; it runs in CI.

Source repositories pinned to an older Cemetery toolkit continue to use its
old exporter until they update their pin. New evidence authored here must use
the current exporter. Historical imports use additive migration; do not rewrite
their published records to look like new exports.

## Initial migration

The migration covers 213 retained dossiers at Cemetery `5de1a59129a86d5ef0ff7dc3d66079781b985eb1`,
including the evidence merged through PRs #18, #19 and #23. The additive
sidecars and alias index pin each original record's exact bytes. No original
`record.json` or file named in a retained `files_sha256` manifest was modified.
Generated catalogue, landing-page and statistics labels were refreshed;
frozen review evidence and original reports were preserved.

Regression checks exercise opposite export orders in separate registries,
same-family/different-result IDs, unchanged IDs after annotations or later
attempts, additive migration, legacy repeat repair, ambiguous aliases and
rejection of inconsistent identity metadata. The ID contract has a frozen
version-1 test vector.
