#!/usr/bin/env python3
"""Run a larger saved-start bank as independently bounded fast suite shards."""
import argparse
from pathlib import Path
import time

from encounter_suite import prepare, run_suite
from synthetic_suite import COMMIT, local_file, read, sha, write

ROOT = Path(__file__).resolve().parents[1]


def prepare_bank(path, root=ROOT):
    bank = read(path)
    if bank.get('schema') != 'borg-cemetery/encounter-bank@1' or not 1 <= len(bank['shards']) <= 128:
        raise ValueError('unsupported bank or shard budget')
    seen, saves, result = set(), set(), []
    common = None
    for entry in bank['shards']:
        suite = local_file(root, entry['manifest'], entry['sha256'])
        manifest, cases = prepare(suite, root)
        identity = (manifest['baseline_source_commit'], manifest['engine_commit'], manifest['core'])
        if common is not None and identity != common:
            raise ValueError('bank shards disagree on source/engine/core')
        common = identity
        for name, scenario, _ in cases:
            if name in seen:
                raise ValueError('duplicate scenario across bank shards')
            save = read(scenario / 'scenario.json')['save_sha256']
            if save in saves:
                raise ValueError('duplicate saved start across bank shards')
            seen.add(name)
            saves.add(save)
        result.append((suite, len(cases)))
    if len(seen) != bank['expected_cases'] or len(seen) > 1024:
        raise ValueError('bank case count differs or exceeds 1024')
    return bank, result


def run_bank(path, source, output, root=ROOT, target_commit=None):
    bank, shards = prepare_bank(path, root)
    if target_commit is not None and not COMMIT.fullmatch(target_commit):
        raise ValueError('target must be an exact commit')
    if output.exists():
        raise ValueError('use a fresh output directory')
    output.mkdir(parents=True)
    start = time.monotonic()
    document = dict(schema='borg-cemetery/encounter-bank-results@1', bank_id=bank['id'],
                    bank_sha256=sha(path), expected_cases=bank['expected_cases'], shards=[],
                    independent_life=False, target_commit=target_commit or read(shards[0][0])['baseline_source_commit'])
    for index, (suite, count) in enumerate(shards, 1):
        row = dict(manifest=str(suite.relative_to(root)), expected_cases=count)
        try:
            result = run_suite(suite, source, output / f'shard-{index}', root=root, target_commit=target_commit)
            row.update(results=result['results'], invalid_count=result['invalid_count'], elapsed_seconds=result['elapsed_seconds'])
        except Exception as error:
            _, cases = prepare(suite, root)
            row.update(status='harness_failure', reason=str(error), invalid_count=count,
                       results=[dict(id=name, status='not_run', reason=str(error)) for name, _, _ in cases])
        document['shards'].append(row)
        write(output / 'results.json', document)
    document['invalid_count'] = sum(r['invalid_count'] for r in document['shards'])
    document['accounted_cases'] = sum(len(r['results']) for r in document['shards'])
    document['completed_cases'] = sum(c['status'] != 'not_run' for r in document['shards'] for c in r['results'])
    document['elapsed_seconds'] = time.monotonic() - start
    write(output / 'results.json', document)
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--target-commit', help='explicit immutable alternative build; engine/profile/saves remain fixed')
    args = parser.parse_args()
    result = run_bank(args.manifest.resolve(), args.source.resolve(), args.out.resolve(), target_commit=args.target_commit)
    print(f"{result['completed_cases']}/{result['expected_cases']} cases, {result['invalid_count']} invalid, {result['elapsed_seconds']:.2f}s")
    raise SystemExit(int(bool(result['invalid_count'])))
