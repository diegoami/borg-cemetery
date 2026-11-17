"""Versioned dossier IDs. Identity never depends on registry order or location."""
import hashlib
import json
import re

SCHEMA = 'borg-cemetery/death-id@1'
FILE = 'death-id.json'
RECORD_SCHEMAS = {'borg-rs/death-record@1', 'borg-reborn-rs/death-record@1',
                  'better-borg-c/death-record@1'}
GUIDED_SCHEMA = 'borg-reborn-rs/guided-death-analysis@1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def death_id(family, result):
    if not isinstance(family, str) or not family:
        raise ValueError('Death identity requires an encounter family')
    if not isinstance(result, str) or not re.fullmatch('[0-9a-f]{64}', result):
        raise ValueError('Death identity requires a full original result SHA-256')
    return 'D-' + digest(dict(schema=SCHEMA, encounter_family=family, result_sha256=result))


def metadata(record, raw, directory_name):
    record_sha = hashlib.sha256(raw).hexdigest()
    if record.get('schema') in RECORD_SCHEMAS:
        family = record.get('encounter_family') or record.get('identity', {}).get('encounter_family')
        originals = [a for a in record.get('attempts', []) if a.get('role') == 'original']
        if len(originals) != 1:
            raise ValueError('Death identity requires exactly one original attempt')
        result = originals[0].get('result_sha256')
        canonical = death_id(family, result)
        basis = dict(kind='encounter-result', encounter_family=family, result_sha256=result)
    elif record.get('schema') == GUIDED_SCHEMA:
        # This watched incident has no measured-run family/key-stream identity.
        # Preserve that distinction rather than inventing one for statistics.
        basis = dict(kind='historical-guided-record', record_sha256=record_sha)
        canonical = 'D-' + digest(dict(schema=SCHEMA, **basis))
    else:
        raise ValueError('Unsupported death identity schema: ' + str(record.get('schema')))
    aliases = sorted({str(a) for a in (record.get('id'), directory_name) if a and a != canonical})
    return dict(schema=SCHEMA, id=canonical, basis=basis, aliases=aliases,
                record_sha256=record_sha)


def ensure(directory, check=False):
    raw = (directory / 'record.json').read_bytes()
    value = metadata(json.loads(raw), raw, directory.name)
    if directory.name.startswith('D-'):
        if directory.name != value['id'] or json.loads(raw).get('id') != value['id']:
            raise ValueError(f'{directory}: directory/record does not match canonical death ID')
    path = directory / FILE
    if path.exists():
        if json.loads(path.read_text()) != value:
            raise ValueError(f'{path}: identity metadata differs from retained evidence')
    elif check:
        raise ValueError(f'{path}: missing; run python3 scripts/death_ids.py')
    else:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    return value


def canonical_id(directory, record):
    """Read verified additive metadata; tolerate unmigrated historical imports."""
    if (directory / FILE).exists():
        return ensure(directory, check=True)['id']
    return record.get('id', directory.name)
