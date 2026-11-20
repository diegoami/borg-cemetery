#!/usr/bin/env python3
"""Join one class's sharded harvest selections into one selection (borg-zoo#184).

Each input is a packed selection (pack_incident_selection.py) of one shard of
one class, made by harvest_incidents.py --shard K from a specification with
`shard_size`. Shards are joined in block order (K = 0, 1, ...), and inside a
shard in its own prespecified seed order, so the result is the selection one
sequential search over the class's seed ordinals would have made: the first
`target` unique saves.

A shard that stopped before the end of its block for any reason but a full
quota (the retained-evidence budget) leaves a gap in seed order: no case from
a later shard is taken after it. Missing shards are a gap too. The output is a
selection directory materialize_incidents.py reads like any other.
"""
import argparse
from pathlib import Path
import shutil

from synthetic_suite import read, write

SCHEMA = 'borg-cemetery/balanced-incident-harvest@1'


def shard_inputs(inputs, cls):
    """{shard: (directory, document)} for class CLS under INPUTS."""
    found = {}
    for path in sorted(inputs.rglob('harvest.json')):
        document = read(path)
        if document.get('schema') != SCHEMA or document.get('class_idx') != cls:
            continue
        shard = document.get('shard')
        if shard is None:
            raise ValueError(f'{path}: not a sharded harvest')
        if shard in found:
            raise ValueError(f'class {cls}: shard {shard} twice')
        found[shard] = (path.parent, document)
    return found


def merge(inputs, out, cls, target=111):
    if out.exists():
        raise ValueError('fresh output required')
    shards = shard_inputs(inputs, cls)
    if not shards:
        raise ValueError(f'class {cls}: no shards')
    specs = {d['spec_sha256'] for _, d in shards.values()}
    if len(specs) != 1:
        raise ValueError(f'class {cls}: shards of different specifications')
    first_dir = shards[min(shards)][0]
    build = read(first_dir / 'build.json')
    for directory, _ in shards.values():
        if read(directory / 'build.json') != build:
            raise ValueError(f'class {cls}: shards of different builds')
    selected, attempts, rejected, seen, used, gap = [], [], [], set(), [], None
    for shard in range(max(shards) + 1):
        if len(selected) >= target:
            break
        if shard not in shards:
            gap = f'shard {shard} missing'
            break
        directory, document = shards[shard]
        used.append(shard)
        attempts.extend(document['attempts'])
        rejected.extend(document.get('rejected', []))
        for case in document['selected']:
            if case['save_sha256'] in seen:
                rejected.append(dict(case, reason='duplicate_in_suite'))
                continue
            if len(selected) < target:
                seen.add(case['save_sha256'])
                selected.append(dict(case, source_shard=shard, source_directory=str(directory)))
            else:
                rejected.append(dict(case, reason='quota_complete'))
        if len(selected) < target and document.get('stop_reason') not in ('range_exhausted', 'quota_complete'):
            gap = f"shard {shard} stopped early ({document.get('stop_reason')})"
            break
    out.mkdir(parents=True)
    for name in ('spec.json', 'build.json'):
        shutil.copyfile(first_dir / name, out / name)
    for case in selected:
        directory = Path(case.pop('source_directory'))
        for kind, name in (('cases', case['directory']), ('attempts', case['source_attempt'])):
            dest = out / kind / name
            if not dest.exists():
                shutil.copytree(directory / kind / name, dest)
    document = dict(schema=SCHEMA, spec_sha256=next(iter(specs)), class_idx=cls, target=target, stage='harvest',
                    attempts=attempts, selected=selected, rejected=rejected, independent_life=False,
                    shards_used=used, shards_found=sorted(shards), gap=gap)
    write(out / 'harvest.json', document)
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--class-index', type=int, required=True)
    parser.add_argument('--target', type=int, default=111)
    args = parser.parse_args()
    result = merge(args.inputs.resolve(), args.out.resolve(), args.class_index, args.target)
    print('class', args.class_index, 'selected', len(result['selected']), '/', args.target,
          'shards used', result['shards_used'], 'gap', result['gap'])
    raise SystemExit(int(len(result['selected']) != args.target))
