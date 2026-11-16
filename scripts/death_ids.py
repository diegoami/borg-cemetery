#!/usr/bin/env python3
"""Assign canonical IDs retroactively without modifying published evidence.

python3 scripts/death_ids.py [--check] [--resolve ID_OR_ALIAS]
Aliases are scoped to their retained path; ambiguous aliases never pick a case.
"""
import argparse
import json
from pathlib import Path

from native.death_identity import ensure, RECORD_SCHEMAS, GUIDED_SCHEMA


def inventory(root, check=False):
    rows = []
    for tree in ('deaths', 'validation', 'runs'):
        for path in sorted((root / tree).rglob('record.json')):
            record = json.loads(path.read_text())
            if record.get('schema') not in RECORD_SCHEMAS | {GUIDED_SCHEMA}:
                continue
            value = ensure(path.parent, check=check)
            rows.append(dict(id=value['id'], aliases=value['aliases'],
                             path=str(path.parent.relative_to(root)),
                             record_sha256=value['record_sha256']))
    return dict(schema='borg-cemetery/death-aliases@1', records=rows)


def refresh(root, check=False):
    value = inventory(root, check)
    path = root / 'deaths/ALIASES.json'
    content = json.dumps(value, indent=2, sort_keys=True) + '\n'
    if check:
        if not path.exists() or path.read_text() != content:
            raise ValueError(f'{path}: stale; run python3 scripts/death_ids.py')
    else:
        path.write_text(content)
    return value


def resolve(root, query):
    rows = inventory(root, check=True)['records']
    matches = [r['path'] for r in rows if query == r['id'] or query in r['aliases'] or query == r['path']]
    if len(matches) != 1:
        raise ValueError(f'{query}: expected one retained path, found {len(matches)}: {matches}')
    return root / matches[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--resolve')
    args = parser.parse_args()
    if args.resolve:
        print(resolve(args.root.resolve(), args.resolve))
    else:
        result = refresh(args.root.resolve(), args.check)
        print(f"{'Verified' if args.check else 'Assigned'} canonical IDs for {len(result['records'])} retained dossiers")
