#!/usr/bin/env python3
"""Register native exporter dossiers without rewriting historical registry files."""
import argparse
import fcntl
from pathlib import Path

from death_pages import dossier_page, read, source_link, text


def register(root):
    registry = root.resolve() / 'deaths'
    registry.mkdir(parents=True, exist_ok=True)
    with (registry / '.registry.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _register(root)


def _register(root):
    root = root.resolve()
    registry = root / 'deaths'
    entries = []
    for path in sorted(registry.glob('D*/record.json')):
        record = read(path)
        identity, terminal = record.get('identity', {}), record.get('terminal', {})
        if not record.get('id') or not record.get('encounter_family'):
            raise ValueError(f'Incomplete native death identity: {path}')
        dossier_page(path.parent)
        program = 'borg-reborn-rs' if str(record.get('schema', '')).startswith('borg-reborn-rs/') else 'borg-rs'
        version = identity.get('git_rev', identity.get('source'))
        entries.append(f"| [{text(record['id'])}]({path.parent.name}/README.md) | {text(identity.get('seed', 'Not used / saved RNG'))} | "
                       f"{source_link(program, version)} | {text(record.get('raw_cause', 'Not recorded'))} | "
                       f"{terminal.get('turn', identity.get('turn', 'Not recorded'))} |")
    content = ['# Death catalogue', '',
               'Each entry opens the human-readable death report, evidence and available replay commands. '
               'Case identifiers are records, not a survival-rate denominator; repeats and alternatives are not additional independent lives.', '',
               '| Case | Seed | Version | Cause | Death turn |', '| --- | --- | --- | --- | --- |', *entries, '',
               '[Cross-case survival analysis](../docs/death-analysis.md) · [Historical registry and actions](README.md)', '']
    temporary = registry / '.CATALOG.md.tmp'
    temporary.write_text('\n'.join(content))
    temporary.replace(registry / 'CATALOG.md')
    return len(entries)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(f'Registered {register(args.root)} retained death dossiers')
