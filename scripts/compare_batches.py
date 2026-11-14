#!/usr/bin/env python3
"""Compare paired fresh-birth profile runs; not a checkpoint scenario trial."""
import argparse
from pathlib import Path
from run_batch import read_json, write_json


def compare(baseline, candidate):
    left = read_json(baseline / 'batch.json')
    right = read_json(candidate / 'batch.json')
    for key in ('program', 'source_commit', 'race_idx', 'class_idx', 'turns', 'flags'):
        if left.get(key) is None or left[key] != right.get(key):
            raise ValueError(f'batches differ or lack {key}')
    for key in ('source_sha256', 'rustc', 'cc'):
        if not left.get('build', {}).get(key) or left['build'][key] != right.get('build', {}).get(key):
            raise ValueError(f'builds differ or lack {key}')
    if set(left['seeds']) != set(right['seeds']):
        raise ValueError('paired seed sets differ')
    pairs = []
    for seed in left['seeds']:
        a = read_json(baseline / f'seed-{seed}/run.json')
        b = read_json(candidate / f'seed-{seed}/run.json')
        pair = dict(seed=seed, baseline=a.get('status'), candidate=b.get('status'), result='inconclusive')
        valid = all(r.get('status') in ('death', 'turn_cap') for r in (a, b))
        calendars = [r.get('summary', {}).get('calendar') for r in (a, b)]
        # Legacy non-fixed seasonal calendars need a stronger date/replay contract.
        if valid and calendars == ['fixed', 'fixed']:
            pair['result'] = ('rescued' if a['status'] == 'death' and b['status'] == 'turn_cap'
                              else 'newly_killed' if a['status'] == 'turn_cap' and b['status'] == 'death'
                              else 'same_survival_outcome')
            for field in ('game_turns', 'max_depth', 'clevel'):
                pair[field] = dict(baseline=a['summary'].get(field), candidate=b['summary'].get(field))
        pairs.append(pair)
    return dict(schema='borg-cemetery/paired-birth-comparison@1', pairs=pairs,
                rescued=sum(p['result'] == 'rescued' for p in pairs),
                newly_killed=sum(p['result'] == 'newly_killed' for p in pairs),
                inconclusive=sum(p['result'] == 'inconclusive' for p in pairs),
                baseline_profile=left.get('profile_sha256', 'upstream default'),
                candidate_profile=right.get('profile_sha256', 'upstream default'),
                binaries_identical=left['build'].get('binary_sha256') == right['build'].get('binary_sha256'),
                interpretation='Descriptive fresh-birth comparison. Not a verified local scenario trial or automatic promotion.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('baseline', type=Path, help='records directory')
    p.add_argument('candidate', type=Path, help='records directory')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    write_json(args.out, compare(args.baseline, args.candidate))
