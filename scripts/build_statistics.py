#!/usr/bin/env python3
"""Generate readable death-archive statistics; no mortality-rate denominator is inferred."""
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import fcntl
import hashlib
import json
from pathlib import Path
import posixpath
import re
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('program', 'commit', 'source_sha256', 'binary_sha256', 'impl', 'inputs_dirty', 'git_dirty')


def read(path):
    return json.loads(path.read_text()) if path.exists() else {}


def encoded(value):
    return json.dumps(value, sort_keys=True, indent=2) + '\n'


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def cell(value):
    return str(value if value is not None else 'Unknown').replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def normalize(directory, registry, program=None, revision=None):
    record = read(directory / 'record.json')
    if record.get('schema') not in ('borg-rs/death-record@1', 'borg-reborn-rs/death-record@1',
                                    'better-borg-c/death-record@1'):
        raise ValueError(f'Unsupported death schema: {directory}')
    identity = record.get('identity', {})
    build = read(directory / 'build.json') or record.get('build', {})
    assessment = read(directory / 'assessment.json')
    summary = read(directory / 'summary.json')
    config_text = (directory / 'config.txt').read_text() if (directory / 'config.txt').exists() else ''
    config = dict(line.split('=', 1) for line in config_text.splitlines() if '=' in line)
    original = next((a for a in record.get('attempts', []) if a.get('role') == 'original'), {})
    program = program or ('better-borg-c' if record['schema'].startswith('better-borg-c/')
                          else ('borg-reborn-rs' if record['schema'].startswith('borg-reborn-rs/') else 'borg-rs'))
    terminal = record.get('terminal', {})
    if terminal.get('dead') is False:
        raise ValueError(f'Living record in death registry: {directory}')
    family = record.get('encounter_family') or identity.get('encounter_family')
    if assessment.get('encounter_family_qualification', {}).get('status') == 'verified':
        family = assessment.get('encounter_family') or family
    build_identity = dict(program=program,
                          commit=identity.get('git_rev') or identity.get('source') or build.get('git_rev') or original.get('source_commit'),
                          source_sha256=identity.get('source_sha256') or build.get('source_sha256'),
                          binary_sha256=identity.get('binary_sha256') or identity.get('binary') or build.get('binary_sha256') or original.get('binary_sha256'),
                          impl=identity.get('impl') or build.get('impl'),
                          inputs_dirty=build.get('inputs_dirty'),
                          git_dirty=identity.get('git_dirty') or build.get('git_dirty'))
    seed = identity.get('seed')
    # An input seed is not an effective RNG seed for a loaded saved game.
    saved = identity.get('start_save') is not None
    if summary.get('loaded'):
        saved |= 'keep-load-rng' in str(identity.get('flags', '')) or config.get('keep_load_rng') == '1'
    attempts = [{k: a.get(k) for k in ('role', 'outcome', 'source_commit', 'binary_sha256', 'result_sha256')}
                for a in record.get('attempts', [])]
    hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
              for name in ('record.json', 'build.json', 'assessment.json', 'summary.json', 'config.txt')
              if (directory / name).exists()}
    report = (f'https://github.com/diegoami/{program}/blob/{revision}/docs/deaths/{directory.name}/report.md'
              if revision else f'deaths/{directory.name}/README.md')
    return dict(registry=registry, case=directory.name, id=record.get('id'), build=build_identity,
                family=family, seed=None if saved else seed,
                seed_basis='saved RNG' if saved else 'recorded input' if seed is not None else 'not recorded',
                character=record.get('character'), cause=record.get('raw_cause') or terminal.get('cause'),
                turn=number(terminal.get('turn', identity.get('turn', summary.get('game_turns')))),
                depth=number(terminal.get('depth')), level=number(terminal.get('level')),
                settings={key: identity.get(key) or config.get(key) for key in ('profile_sha256', 'borg_txt_sha256', 'borg_core', 'borg_core_overrides', 'params_core_sha256', 'borg_errand', 'params_errand_sha256', 'params_ladders_sha256')}, attempts=attempts,
                report=report, files_sha256=hashes)


def local_source(root):
    rows = [normalize(p.parent, 'cemetery') for p in sorted((root / 'deaths').glob('D*/record.json'))]
    return dict(name='cemetery', description='Curated dossiers retained in this checkout',
                revision=None, records=rows)


def import_external(checkout, revision):
    """Require a clean, pinned input tree; never run the donor's code."""
    revision = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', revision + '^{commit}'], text=True).strip()
    paths = ['docs/deaths/*/' + name for name in ('record.json', 'build.json', 'assessment.json', 'summary.json', 'config.txt')]
    subprocess.run(['git', '-C', str(checkout), 'diff', '--exit-code', revision, '--', *paths], check=True, capture_output=True)
    # Untracked dossiers must not enter a report attributed to the pinned tree.
    tracked = subprocess.check_output(['git', '-C', str(checkout), 'ls-tree', '-r', '--name-only', revision, '--', 'docs/deaths'], text=True).splitlines()
    records = sorted(p for p in tracked if re.fullmatch(r'docs/deaths/D[^/]+/record\.json', p))
    if not records:
        raise ValueError('No pinned external death records')
    tracked = set(tracked)
    for record in records:
        for name in ('record.json', 'build.json', 'assessment.json', 'summary.json', 'config.txt'):
            relative = str(Path(record).with_name(name))
            if (checkout / relative).exists() and relative not in tracked:
                raise ValueError(f'Untracked metadata cannot be attributed to the pinned revision: {relative}')
    rows = [normalize((checkout / p).parent, 'reborn-historical', 'borg-reborn-rs', revision) for p in records]
    return dict(name='reborn-historical', description='Historical borg-reborn-rs archive; dossiers remain in that repository',
                repository='diegoami/borg-reborn-rs', revision=revision, records=rows)


def build_id(row):
    identity = row['build']
    suffix = {k: identity.get(k) for k in FIELDS}
    if not identity.get('binary_sha256') and not identity.get('source_sha256'):
        suffix['unknown_identity_case'] = [row['registry'], row['case']]
    commit = identity.get('commit') or 'unknown'
    return f"{identity['program']}-{commit[:12]}-{fingerprint(suffix)[:16]}"


def report_link(row, location):
    target = row['report']
    if not target.startswith('https://'):
        target = posixpath.relpath(target, location)
    return f"[{cell(row['case'])}]({target})"


def table(headers, rows):
    return ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |',
            *['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows], '']


def counts(rows):
    return [len(rows), len({r['family'] for r in rows if r['family']}),
            sum(not r['family'] for r in rows), sum(len(r['attempts']) for r in rows),
            sum(a['role'] == 'repeat' for r in rows for a in r['attempts'])]


def distribution(rows, field):
    values = [r[field] for r in rows if r[field] is not None]
    if not values:
        return [field, 0, 'Unknown', 'Unknown', 'Unknown', 'Unknown']
    return [field, len(values), min(values), f'{statistics.median(values):g}', f'{statistics.mean(values):.2f}', max(values)]


def render(sources):
    outputs, groups = {}, defaultdict(list)
    all_rows = [r for source in sources for r in source['records']]
    for row in all_rows:
        groups[build_id(row)].append(row)
    lines = ['# Cemetery statistics', '',
             'Death-archive statistics, separated by registry and exact retained build. '
             'These are selected death records, not a complete sample of games. **No mortality or survival rate is calculated.**', '',
             '## Archive coverage', '']
    lines += table(['Registry', 'Dossiers', 'Known start families', 'Missing family', 'Retained attempts', 'Explicit repeats', 'Build groups'],
                   [[f"[{s['name']}](sources/{s['name']}.md)", *counts(s['records']), len({build_id(r) for r in s['records']})] for s in sources])
    family_sets = [{(r['build']['program'], r['family']) for r in s['records'] if r['family']} for s in sources]
    overlap = sum(len(a & b) for i, a in enumerate(family_sets) for b in family_sets[i + 1:])
    lines += [f'Shared declared/qualified family keys across registry pairs: **{overlap}**. '
              'Registry totals are not pooled into an independent-birth count. Different family keys do not prove unrelated births.', '',
              'A dossier is one retained case. Start families group declared/qualified starting conditions; '
              'saved games, verification repeats, human continuations and tuning trials do not become new births. '
              'Terminal distributions below weight dossiers, including multiple dossiers of one family.', '',
              '[Retained extra attempts](attempts.md) lists repeats and unclassified/alternative attempt roles separately. '
              'Scenario and human-play outcomes remain in their original reports and are excluded from death distributions.', '',
              '## Patterns among retained deaths', '']
    for source in sources:
        lines += [f"### {source['name']}", '']
        lines += table(['Cause', 'Dossiers'], Counter(r['cause'] or 'Unknown' for r in source['records']).most_common(5))
        lines += table(['Metric', 'Known records', 'Minimum', 'Median', 'Mean', 'Maximum'],
                       [distribution(source['records'], field) for field in ('turn', 'depth', 'level')])
    lines += ['## Builds', '',
              'A build group uses project, commit, source-input hash, executable hash, implementation and dirtiness flags. '
              'Different binaries at the same commit stay separate. Missing provenance is printed as Unknown; '
              'a dirty build must not be treated as the pristine named commit. Profiles are reported separately on each build page.', '']
    for source in sources:
        name, rows = source['name'], source['records']
        selected = sorted({build_id(r) for r in rows}, key=lambda key: (-sum(r['registry'] == name for r in groups[key]), key))
        lines += [f'### {name}', '']
        lines += table(['Build / source commit', 'Implementation', 'Input dirtiness', 'Dossiers', 'Start families', 'Median death turn', 'Median depth'],
                       [[f"[{groups[key][0]['build']['program']} · {(groups[key][0]['build']['commit'] or 'unknown')[:12]} · {key[-16:]}](builds/{key}/README.md)",
                         groups[key][0]['build']['impl'], groups[key][0]['build']['inputs_dirty'],
                         len(part := [r for r in groups[key] if r['registry'] == name]),
                         len({r['family'] for r in part if r['family']}), distribution(part, 'turn')[3], distribution(part, 'depth')[3]]
                        for key in selected])
        source_lines = [f'# {name}: source and coverage', '', source['description'] + '.', '']
        if source.get('revision'):
            source_lines += [f"Pinned registry revision: [`{source['revision']}`](https://github.com/{source['repository']}/tree/{source['revision']}/docs/deaths).", '',
                             'This is a frozen statistical inventory of external records, not a dossier migration. '
                             'Links open the original reports at that revision; identically numbered cemetery cases are different records.', '']
        else:
            source_lines += ['Recomputed from `deaths/D*/record.json` and accompanying identity/summary/assessment files in this checkout.', '']
        source_lines += [f"Input inventory SHA-256: `{fingerprint(rows)}`.", '',
                         'The companion snapshot for an external source retains normalized statistical fields and per-file hashes, '
                         'not raw logs, saves or executables. Unknown seeds are not replaced by requested seed values.', '']
        source_lines += table(['Cause', 'Dossiers'], Counter(r['cause'] or 'Unknown' for r in rows).most_common())
        source_lines += ['## Terminal distributions', '', 'Among retained death dossiers only; no comparison of survival performance is implied.', '']
        source_lines += table(['Metric', 'Known records', 'Minimum', 'Median', 'Mean', 'Maximum'], [distribution(rows, f) for f in ('turn', 'depth', 'level')])
        source_lines += ['## Characters', ''] + table(['Character', 'Dossiers'], Counter(r['character'] or 'Unknown' for r in rows).most_common())
        source_lines += ['[Statistics index](../README.md)', '']
        outputs[f'sources/{name}.md'] = '\n'.join(source_lines)
    lines += ['## Updating', '', '```bash', 'python3 scripts/build_statistics.py', 'python3 scripts/build_statistics.py --check', '```', '',
              'Normal regeneration refreshes the local registry and preserves the explicitly pinned external snapshot. '
              'Native death registration also refreshes these reports. To update the external inventory from a clean checkout:', '',
              '```bash', 'python3 scripts/build_statistics.py --external-checkout /path/to/borg-reborn-rs --external-ref FULL_COMMIT_SHA', '```', '',
              'The tool reads and hashes records only; it does not execute source tools, copy historical dossiers, '
              'or include ignored validation caches. External refreshes must be committed with the reports. '
              'Coverage is the direct death registries listed above. Seeded CI batches, all-run denominators and scenario outcomes are not read by this report.', '']
    outputs['README.md'] = '\n'.join(lines)
    extra = ['# Extra retained attempts', '',
             'Only non-original attempts embedded in death dossiers are listed here. '
             'A different executable is kept explicit, never assigned the original executable or counted as a new independent birth. '
             'Standalone scenario/tuning trials and human continuations are outside this table.', '']
    extra_rows = []
    for key, rows in sorted(groups.items()):
        location = f'statistics/builds/{key}'
        build = rows[0]['build']
        page = [f"# {build['program']} · {(build['commit'] or 'Unknown')[:12]}", '',
                'Exact primary-case build identity. Counts are death dossiers, not mortality rates. '
                'Embedded attempts can use other builds; their actual executable hashes appear in the [extra-attempt table](../../attempts.md).', '']
        page += table(['Identity field', 'Value'], [[field, build.get(field)] for field in FIELDS])
        page += table(['Registry', 'Dossiers', 'Known start families', 'Missing family', 'Embedded attempts (all builds)', 'Embedded repeats (all builds)'],
                      [[s['name'], *counts(part)] for s in sources if (part := [r for r in rows if r['registry'] == s['name']])])
        page += ['## Causes by registry', '']
        for source in sources:
            part = [r for r in rows if r['registry'] == source['name']]
            if not part:
                continue
            page += [f"### {source['name']}", '']
            page += table(['Cause', 'Dossiers'], Counter(r['cause'] or 'Unknown' for r in part).most_common())
            page += table(['Metric', 'Known records', 'Minimum', 'Median', 'Mean', 'Maximum'], [distribution(part, f) for f in ('turn', 'depth', 'level')])
        page += ['## Settings', '', 'Builds can run different cores or profiles. The recorded settings below stay separate; unavailable fields remain Unknown.', '']
        settings_groups = defaultdict(list)
        for row in rows:
            settings_groups[(row['registry'], fingerprint(row.get('settings', {})))].append(row)
        for (registry, digest), part in sorted(settings_groups.items()):
            page += [f'### Settings {registry} {digest[:12]}', '', f'{registry}: {len(part)} dossiers.', '']
            page += table(['Setting / identity', 'Recorded value'], sorted(part[0].get('settings', {}).items()))
        page += ['## Cases', '']
        page += table(['Registry', 'Case report', 'Seed', 'Seed basis', 'Character', 'Cause', 'Turn', 'Depth', 'Level', 'Settings', 'Start family'],
                      [[r['registry'], report_link(r, location), r['seed'], r['seed_basis'], r['character'], r['cause'], r['turn'], r['depth'], r['level'], f"[settings](#settings-{r['registry']}-{fingerprint(r.get('settings', {}))[:12]})", r['family']] for r in rows])
        page += ['[Statistics index](../../README.md)', '']
        outputs[f'builds/{key}/README.md'] = '\n'.join(page)
        for row in rows:
            for attempt in row['attempts']:
                if attempt['role'] != 'original':
                    extra_rows.append([row['registry'], report_link(row, 'statistics'), attempt['role'], attempt['outcome'],
                                       attempt['source_commit'], attempt['binary_sha256'], attempt['result_sha256']])
    extra += table(['Registry', 'Case', 'Role', 'Outcome', 'Actual source', 'Actual executable SHA-256', 'Result/key-stream SHA-256'], extra_rows)
    extra += ['[Statistics index](README.md)', '']
    outputs['attempts.md'] = '\n'.join(extra)
    outputs['generated-files.json'] = encoded(sorted([*outputs, 'generated-files.json']))
    return outputs


@contextmanager
def stats_lock(root):
    path = root / 'statistics'
    path.mkdir(parents=True, exist_ok=True)
    with (path / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def generate(root=ROOT, external_checkout=None, external_ref=None, check=False):
    root = root.resolve()
    target = root / 'statistics'
    with stats_lock(root):
        snapshot_path = target / 'sources/reborn-historical.snapshot.json'
        external = import_external(external_checkout.resolve(), external_ref) if external_checkout else read(snapshot_path)
        sources = [local_source(root)] + ([external] if external else [])
        outputs = render(sources)
        if external_checkout:
            outputs['sources/reborn-historical.snapshot.json'] = encoded(external)
        old = read(target / 'generated-files.json') or []
        stale = set(old) - set(outputs)
        # The source snapshot is retained as an input, rather than treated as a generated page.
        stale.discard('sources/reborn-historical.snapshot.json')
        changed = [name for name, data in outputs.items() if not (target / name).exists() or (target / name).read_text() != data]
        if check:
            if changed or stale:
                raise ValueError('Statistics need regeneration: ' + ', '.join(sorted(set(changed) | stale)))
            return len(outputs)
        for name, data in outputs.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_name('.' + path.name + '.tmp')
            temp.write_text(data)
            temp.replace(path)
        for name in stale:
            if re.fullmatch(r'builds/[a-z0-9-]+/README\.md', name):
                (target / name).unlink(missing_ok=True)
        return len(outputs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--external-checkout', type=Path)
    parser.add_argument('--external-ref')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if bool(args.external_checkout) != bool(args.external_ref):
        parser.error('--external-checkout and --external-ref are required together')
    if args.check and args.external_checkout:
        parser.error('Refresh the snapshot first, then use --check')
    print(f'Statistics: {generate(args.root, args.external_checkout, args.external_ref, args.check)} reports checked/generated')


if __name__ == '__main__':
    main()
