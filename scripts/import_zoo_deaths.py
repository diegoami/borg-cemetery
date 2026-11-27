#!/usr/bin/env python3
"""Import a borg-zoo run's deaths as replayable dossiers (borg-zoo#176, #63).

borg-zoo replays every natural death of a run with full logs and checks the
replay's key stream against the cell's. It uploads the result as death
bundles in the run's deaths-<specimen>-<shard> artifacts. Each bundle is a run
directory for scripts/native/export-death.py, and this script exports it:

  python3 scripts/import_zoo_deaths.py --run 43874782892
  python3 scripts/import_zoo_deaths.py --bundles DIR --run-id local-1

Every reproduced bundle becomes a D-<sha256> dossier with README, REPLAY,
launchers and catalogue entry. A death the registry already has (same
encounter family and key stream) is a repeat and is not added again. Bundles
that are not reproduced, failed or unsupported are listed on the run page
with their reason and are never dropped silently. Raw logs stay in the zoo
artifact (90 days); each dossier records where.

The run page goes to runs/zoo-<experiment>-<run>/ (README.md and
deaths.json), with one row per death linking to its dossier. Set
BORG_DEATH_RECORDS_DIR to export into a temporary registry instead; the
run page then goes beside it.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZOO = 'diegoami/borg-zoo'


def exporter():
    spec = importlib.util.spec_from_file_location('export_death', ROOT / 'scripts/native/export-death.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def download(run_id, repo, dest):
    """The run's deaths-* artifacts, one directory each, under DEST."""
    subprocess.run(['gh', 'run', 'download', str(run_id), '-R', repo, '-p', 'deaths-*', '-D', str(dest)],
                   check=True)
    return dest


def artifact_of(root, path):
    """The artifact a path under ROOT belongs to: the download directory holds
    one directory per artifact; a shard directory given alone is its own."""
    rel = Path(path).relative_to(root).parts
    return Path(root).name if (Path(root) / 'index.jsonl').exists() or len(rel) < 2 else rel[0]


def entries(root):
    """(artifact name, bundle base dir, index entry) for every index.jsonl under ROOT."""
    root = Path(root)
    for index in sorted(root.rglob('index.jsonl')):
        artifact = artifact_of(root, index)
        for line in index.read_text().splitlines():
            if line.strip():
                yield artifact, index.parent, json.loads(line)


def unindexed(root, found):
    """Rows for bundle directories no index line names: a shard cut short
    while the bundle was being written or indexed. Listed, never imported:
    the index line carries the reproduction status and build identity."""
    named = {(base.resolve() / e['bundle']) for _, base, e in found if e.get('bundle')}
    rows = []
    # A replay starts with pborg.yaml on combined builds, or borg.txt on
    # historical builds. Combined builds add the legacy text receipt at exit.
    markers = (marker.parent.parent for name in ('borg.txt', 'pborg.yaml')
               for marker in Path(root).rglob(f'user/{name}'))
    for bundle in sorted(set(markers)):
        if bundle.resolve() in named:
            continue
        manifest = {}
        if (bundle / 'zoo-death.json').exists():
            try:
                manifest = json.loads((bundle / 'zoo-death.json').read_text())
            except ValueError:
                pass
        rel = bundle.relative_to(root).parts
        cell = manifest.get('cell') or '/'.join(rel[-4:])
        row = {k: manifest.get(k) for k in ('seed', 'specimen', 'profile', 'character', 'cause', 'status', 'experiment')}
        row.update(cell=cell, artifact=artifact_of(root, bundle), imported='skipped',
                   final={k: (manifest.get('final') or {}).get(k) for k in ('turn', 'level', 'depth', 'max_depth')},
                   reason='not imported: no index entry (the shard stopped before indexing this bundle)')
        if row['seed'] is None and rel[-1].isdigit():
            row['seed'] = int(rel[-1])
        row['profile'] = row['profile'] or (rel[-2] if len(rel) >= 2 else None)
        rows.append(row)
    return rows


def import_one(export, artifact, base, entry, run_id, repo):
    """Export one bundle; a row for the run page."""
    row = {k: entry.get(k) for k in ('cell', 'seed', 'specimen', 'profile', 'character', 'cause', 'status')}
    row['final'] = {k: (entry.get('final') or {}).get(k) for k in ('turn', 'level', 'depth', 'max_depth')}
    row['artifact'] = artifact
    if entry.get('status') != 'reproduced':
        row['imported'] = 'skipped'
        row['reason'] = entry.get('error') or entry.get('status')
        return row
    impl = (entry.get('build') or {}).get('impl')
    if not entry.get('bundle') or not impl:
        row.update(imported='skipped', reason='index entry has no bundle or build identity')
        return row
    bundle = base / entry['bundle']
    keys = bundle / 'keys.log'
    if not keys.is_file() or sha256(keys) != entry.get('play_sha256'):
        row.update(imported='skipped', reason='bundle keys.log missing or not the cell\'s key stream')
        return row
    location = (f'borg-zoo run {run_id}, artifact {artifact}, {entry["bundle"]}'
                + (f' (https://github.com/{repo}/actions/runs/{run_id}, 90-day retention)'
                   if str(run_id).isdigit() else ''))
    try:
        case, what = export.export(bundle, impl, bundle / 'BUILD_ID', raw_location=location)
    except export.InvalidPborgYaml as error:
        row.update(imported='skipped', reason=str(error))
        return row
    row['case'], row['imported'] = case, what
    if case is None:
        row['reason'] = what
    return row


def page(rows, run_id, repo, experiment, registry, out):
    """The run's death page: one row per death, linking its dossier."""
    out.mkdir(parents=True, exist_ok=True)
    (out / 'deaths.json').write_text(json.dumps({'schema': 'borg-cemetery/zoo-run-deaths@1', 'run': str(run_id),
                                                 'repository': repo, 'experiment': experiment, 'deaths': rows},
                                                indent=2, sort_keys=True) + '\n')
    link = os.path.relpath(registry, out)
    run = f'[{run_id}](https://github.com/{repo}/actions/runs/{run_id})' if str(run_id).isdigit() else f'`{run_id}`'
    done = [r for r in rows if r.get('case')]
    lines = [f'# Zoo deaths: {experiment}, run {run_id}', '',
             f'The natural deaths of borg-zoo run {run}, imported by `scripts/import_zoo_deaths.py` (borg-zoo#176). '
             f'{len(done)} of {len(rows)} deaths have a dossier. Every dossier was replayed in the zoo with full logs, '
             'and its key stream matched the cell\'s. A repeat is a death the cemetery already had.', '',
             '| Dossier | Profile | Seed | Character | Cause | Turn | Level | Depth (max) | Import |',
             '| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |']
    for r in sorted(rows, key=lambda r: (r.get('profile') or '', r.get('seed') or 0)):
        f = r['final']
        case = f"[{r['case'][:14]}]({link}/{r['case']}/README.md)" if r.get('case') else 'none'
        status = r['imported'] + (f": {r['reason']}" if r.get('reason') else '')
        lines.append(f"| {case} | {r.get('profile')} | {r.get('seed')} | {r.get('character')} | {r.get('cause')} | "
                     f"{f.get('turn')} | {f.get('level')} | {f.get('depth')} ({f.get('max_depth')}) | "
                     f"{status.replace('|', '/')} |")
    lines += ['', 'Each dossier\'s REPLAY.md has the build, watch and rerun commands. A replay and its original are '
              'one life, not two samples.', '']
    (out / 'README.md').write_text('\n'.join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--run', help='borg-zoo workflow run id: download its deaths-* artifacts')
    src.add_argument('--bundles', type=Path, help='already downloaded deaths-* artifacts (or one shard directory)')
    ap.add_argument('--run-id', help='the run id to record with --bundles')
    ap.add_argument('--repo', default=ZOO)
    ap.add_argument('--runs-dir', type=Path, help='where the run page goes (default runs/, or beside a temporary registry)')
    a = ap.parse_args(argv)
    if a.run and a.run_id:
        ap.error('--run-id is for --bundles; --run already names the run')
    run_id = a.run or a.run_id or 'local'
    export = exporter()
    registry = export.registry_dir().resolve()
    with tempfile.TemporaryDirectory(prefix='zoo-deaths-') as tmp:
        root = download(a.run, a.repo, Path(tmp)) if a.run else a.bundles
        found = list(entries(root))
        orphans = unindexed(root, found)
        if not found and not orphans:
            print(f'import_zoo_deaths: no death bundles in run {run_id}', file=sys.stderr)
            return 1
        rows = [import_one(export, *item, run_id, a.repo) for item in found] + orphans
    experiments = sorted({e.get('experiment') for _, _, e in found if e.get('experiment')})
    if not experiments:
        experiments = sorted({r.get('experiment') for r in orphans if r.get('experiment')})
    experiment = experiments[0] if len(experiments) == 1 else '+'.join(experiments) or 'unknown'
    if any(r.get('case') for r in rows):
        export.aggregate(registry)
    runs = a.runs_dir or (ROOT / 'runs' if registry == (ROOT / 'deaths').resolve() else registry.parent / 'runs')
    out = runs / f'zoo-{experiment}-{run_id}'
    page(rows, run_id, a.repo, experiment, registry, out)
    counts = {}
    for r in rows:
        key = r['imported'].split(':')[0]
        counts[key] = counts.get(key, 0) + 1
    print(json.dumps({'run': str(run_id), 'deaths': len(rows), **counts, 'page': str(out)}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
