#!/usr/bin/env python3
"""Freeze and compare file-based Borg configuration arms on saved encounters."""
import argparse
import fcntl
from pathlib import Path
import re
import subprocess
import time

from encounter_suite import prepare
from scenario_config import run_configured, settings
from synthetic_suite import COMMIT, STATE, hashed, local_file, read, sha, write

ROOT = Path(__file__).resolve().parents[1]
VALID = {'death', 'survived_horizon', 'stopped'}


def freeze(spec_path, output, root=ROOT):
    if output.exists():
        raise ValueError('use a fresh frozen definition path')
    spec = read(spec_path)
    if spec.get('schema') != 'borg-cemetery/encounter-comparison-spec@1' or spec.get('core') != 'borg-rs':
        raise ValueError('this adapter supports fixed borg-rs core, configuration axis only')
    if not COMMIT.fullmatch(spec.get('source_commit', '')):
        raise ValueError('exact source commit required')
    def ref(name):
        path = local_file(root, name, sha(root / name))
        return dict(path=name, sha256=sha(path))
    suite = ref(spec['suite'])
    manifest, cases = prepare(root / suite['path'], root)
    arms, seen = [], set()
    if not 2 <= len(spec['arms']) <= 4 or len(spec['arms']) * len(cases) > 32:
        raise ValueError('require 2..4 arms and at most 32 cells')
    for arm in spec['arms']:
        name = arm['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', name) or name in seen:
            raise ValueError('invalid/duplicate arm ID')
        seen.add(name)
        borg = ref(arm['borg_txt'])
        parsed = settings((root / borg['path']).read_text())
        plan = ref(arm['errands_plan']) if arm.get('errands_plan') else None
        if parsed.get('borg_plan') and not plan:
            raise ValueError('a selected plan must be pinned in the arm')
        arms.append(dict(id=name, borg_txt=borg, errands_plan=plan))
    value = dict(schema='borg-cemetery/encounter-comparison@1', id=spec['id'], core='borg-rs',
                 comparison_axis=['configuration'], source_commit=spec['source_commit'],
                 engine_commit=manifest['engine_commit'], suite=suite, arms=arms)
    write(output, value)
    return value


def load(path, root=ROOT):
    value = read(path)
    if (value.get('schema') != 'borg-cemetery/encounter-comparison@1' or value.get('core') != 'borg-rs'
            or value.get('comparison_axis') != ['configuration']):
        raise ValueError('unsupported comparison contract')
    suite = local_file(root, value['suite']['path'], value['suite']['sha256'])
    manifest, cases = prepare(suite, root)
    if not COMMIT.fullmatch(value.get('source_commit', '')) or value.get('engine_commit') != manifest['engine_commit']:
        raise ValueError('invalid source/engine identity')
    arms = []
    if not 2 <= len(value['arms']) <= 4 or len(cases) * len(value['arms']) > 32:
        raise ValueError('invalid comparison work budget')
    seen = set()
    for arm in value['arms']:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', arm['id']) or arm['id'] in seen:
            raise ValueError('invalid/duplicate arm ID')
        seen.add(arm['id'])
        borg = local_file(root, arm['borg_txt']['path'], arm['borg_txt']['sha256'])
        plan = local_file(root, arm['errands_plan']['path'], arm['errands_plan']['sha256']) if arm['errands_plan'] else None
        arms.append((arm, borg, plan))
    return value, manifest, cases, arms


def classify_pair(a, b, unverified=()):
    if a is None or b is None:
        return 'missing'
    if a['status'] not in VALID or b['status'] not in VALID:
        return 'invalid'
    if unverified:
        return 'unverified_configuration'
    if a['status'] == 'stopped' or b['status'] == 'stopped':
        return 'inconclusive'
    return {('death', 'death'): 'both_died', ('survived_horizon', 'survived_horizon'): 'both_survived',
            ('death', 'survived_horizon'): 'rescued', ('survived_horizon', 'death'): 'newly_killed'}[(a['status'], b['status'])]


def validate_cell(row, dest, definition_path, definition, manifest, arm, scenario_dir, template, plan):
    """Reject stale/copied receipts; these are consistency checks, not signatures."""
    scenario = read(scenario_dir / 'scenario.json')
    pairing = hashed(dict(definition=sha(definition_path), scenario=sha(scenario_dir / 'scenario.json'),
                          save=scenario['save_sha256'], source=definition['source_commit'], core='borg-rs'))
    if not isinstance(row, dict) or row.get('arm') != arm['id'] or row.get('scenario') != scenario['id'] or row.get('pairing_hash') != pairing:
        raise ValueError('cell identity differs from frozen inputs')
    if row['status'] not in VALID:
        return
    trial = read(dest / 'trial.json')
    if row.get('trial_sha256') != sha(dest / 'trial.json'):
        raise ValueError('trial receipt changed')
    for key in ('status', 'summary', 'build', 'configuration'):
        if row.get(key) != trial.get(key):
            raise ValueError('cell differs from trial: ' + key)
    expected = dict(source_commit=definition['source_commit'], scenario_sha256=sha(scenario_dir / 'scenario.json'),
                    save_sha256=scenario['save_sha256'], startup_contract='fresh_borg_saved_engine_rng',
                    borg_memory_restored=False, horizon_engine_turns=manifest['horizon_engine_turns'],
                    start_turn=scenario['start_turn'], cap_turn=scenario['start_turn'] + manifest['horizon_engine_turns'],
                    exit_code=0)
    if any(trial.get(k) != v for k, v in expected.items()):
        raise ValueError('trial inputs differ from frozen comparison')
    build, process = trial['build'], trial['process']
    if (build.get('git_rev') != definition['source_commit'] or build.get('engine_upstream') != definition['engine_commit']
            or build.get('inputs_dirty') != 'no' or process.get('status') != 'success'
            or process.get('executable_sha256_before') != build.get('binary_sha256')
            or process.get('executable_sha256_after') != build.get('binary_sha256')):
        raise ValueError('build/process identity differs')
    if row.get('execution_hash') != hashed(dict(pairing=pairing, arm=arm, build=build)):
        raise ValueError('execution identity differs')
    raw = dest / 'run'
    if read(raw / 'summary.json') != trial['summary'] or read(raw / 'process.json') != process:
        raise ValueError('raw receipts differ')
    summary = trial['summary']
    if any(summary.get(k) != v for k, v in dict(loaded=True, loaded_turn=scenario['start_turn'],
            seed=scenario['birth_seed'], race_idx=scenario['race_idx'], class_idx=scenario['class_idx']).items()):
        raise ValueError('loaded identity differs')
    if (row['status'] == 'death' and (summary.get('dead') is not True or summary.get('stop_reason') != 'death')
            or row['status'] == 'survived_horizon' and (summary.get('dead') is not False
                or summary.get('stop_reason') != 'turns' or summary.get('game_turns', 0) < expected['cap_turn'])):
        raise ValueError('terminal outcome differs')
    first = STATE.match((raw / 'state.log').read_text().splitlines()[0])
    if not first or list(map(int, first.groups()[3:])) != [scenario['initial_observed'][k] for k in ('hp', 'max_hp', 'sp', 'max_sp')]:
        raise ValueError('initial loaded state differs')
    proof = trial['configuration']
    if proof != read(raw / 'configuration.json') or proof.get('core') != 'borg-rs' or proof.get('template_sha256') != sha(template):
        raise ValueError('configuration receipt differs')
    if proof.get('applied_borg_txt_sha256') != sha(raw / 'user/borg.txt'):
        raise ValueError('applied configuration changed')
    requested = settings(template.read_text())
    actual = {p['name']: p for p in read(raw / 'params-core.json')}
    for name, value in requested.items():
        if name.startswith('borg_param_'):
            p = actual.get(name.removeprefix('borg_param_'), {})
            if p.get('value') != value or p.get('origin') != 'borg.txt' or proof['named_parameters'].get(name) != value:
                raise ValueError('named parameter not effective: ' + name)
    if plan and (proof.get('plan_sha256') != sha(plan) or proof.get('loaded_plan_sha256') != sha(plan)
                 or sha(raw / 'errands_plan.txt') != sha(plan)):
        raise ValueError('loaded errands plan differs')


def collect(definition_path, output, root=ROOT):
    definition, manifest, cases, arms = load(definition_path, root)
    cells = []
    base_settings = settings(arms[0][1].read_text())
    pairs = []
    checked = {}
    common_binary = None
    for arm, template, plan in arms:
        for name, scenario, profile in cases:
            dest = output / 'cells' / arm['id'] / name
            row = None
            if (dest / 'cell.json').exists():
                try:
                    row = read(dest / 'cell.json')
                    validate_cell(row, dest, definition_path, definition, manifest, arm, scenario, template, plan)
                    if row['status'] in VALID:
                        binary = row['build']['binary_sha256']
                        if common_binary is not None and binary != common_binary:
                            raise ValueError('configuration arms used different binaries')
                        common_binary = binary
                except (ValueError, KeyError, OSError, TypeError, IndexError, AttributeError) as error:
                    row = dict(arm=arm['id'], scenario=name, status='invalid_receipt', reason=str(error))
            checked[arm['id'], name] = row
    def cell(arm, name):
        return checked[arm['id'], name]
    for arm, template, plan in arms:
        for name, scenario, profile in cases:
            row = cell(arm, name)
            cells.append(row or dict(arm=arm['id'], scenario=name, status='missing'))
        if arm['id'] == arms[0][0]['id']:
            continue
        candidate = settings(template.read_text())
        changed = [k for k in base_settings.keys() | candidate.keys() if base_settings.get(k) != candidate.get(k)]
        # Named core knobs have native readback; the current Rust core does not
        # attest all classic flags. Do not call an unverified change a rescue.
        unverified = [k for k in changed if not k.startswith('borg_param_') and k != 'borg_plan']
        for name, scenario, profile in cases:
            a, b = cell(arms[0][0], name), cell(arm, name)
            pairs.append(dict(scenario=name, baseline=arms[0][0]['id'], candidate=arm['id'],
                              outcome=classify_pair(a, b, unverified), unverified_changed_settings=unverified,
                              baseline_terminal=(a or {}).get('status', 'missing'), candidate_terminal=(b or {}).get('status', 'missing')))
    document = dict(schema='borg-cemetery/encounter-comparison-results@1', id=definition['id'],
                    definition_sha256=sha(definition_path), core='borg-rs', source_commit=definition['source_commit'],
                    expected_cells=len(cases) * len(arms), cells=cells, pairs=pairs,
                    independent_life=False, qualified_near_death=dict(coverage='unavailable', count=None))
    timing = output / 'execution.json'
    if timing.exists():
        receipt = read(timing)
        if receipt.get('definition_sha256') == sha(definition_path):
            document['elapsed_seconds'] = receipt['elapsed_seconds']
    write(output / 'comparison.json', document)
    text = ['# ' + definition['id'], '', 'Same saved engine/RNG starts; fresh Borg per arm. No population claim.', '',
            '| Scenario | Baseline | Candidate | Baseline result | Candidate result | Comparison |',
            '|---|---|---|---|---|---|']
    for p in pairs:
        text.append('| ' + ' | '.join(p[k] for k in ('scenario', 'baseline', 'candidate', 'baseline_terminal', 'candidate_terminal', 'outcome')) + ' |')
    text += ['', 'Survival means alive at the finite horizon, not an eventual win. Loaded plan identity does not prove every plan branch was exercised.', '',
             '| Scenario | Arm | End HP | End depth | Max depth | Engine turns elapsed |',
             '|---|---|---:|---:|---:|---:|']
    for row in cells:
        summary = row.get('summary') or {}
        scenario = next(read(s / 'scenario.json') for n, s, _ in cases if n == row['scenario'])
        turns = summary.get('game_turns')
        text.append('| ' + ' | '.join(str(v) for v in (row['scenario'], row['arm'], summary.get('hp', '—'),
                    summary.get('depth', '—'), summary.get('max_depth', '—'),
                    turns - scenario['start_turn'] if turns is not None else '—')) + ' |')
    (output / 'comparison.md').write_text('\n'.join(text) + '\n')
    return document


def run(definition_path, source, output, root=ROOT):
    definition, manifest, cases, arms = load(definition_path, root)
    if output.exists():
        raise ValueError('output exists; preserve attempts')
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if head != definition['source_commit']:
        raise ValueError('target source is not the frozen commit')
    engine = dict(line.split('=', 1) for line in (source / 'engine/UPSTREAM').read_text().splitlines() if '=' in line)
    if engine.get('commit') != definition['engine_commit']:
        raise ValueError('engine semantics differ')
    output.mkdir(parents=True)
    start = time.monotonic()
    with open('/tmp/angband-validation.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for arm, template, plan in arms:
            for name, scenario_dir, profile in cases:
                dest = output / 'cells' / arm['id'] / name
                scenario = read(scenario_dir / 'scenario.json')
                pairing = hashed(dict(definition=sha(definition_path), scenario=sha(scenario_dir / 'scenario.json'),
                                      save=scenario['save_sha256'], source=head, core='borg-rs'))
                row = dict(arm=arm['id'], scenario=name, pairing_hash=pairing, status='harness_failure')
                tick = time.monotonic()
                try:
                    run_configured(source, scenario_dir, dest, template, plan,
                                   turns=manifest['horizon_engine_turns'], wall_seconds=manifest['wall_seconds'])
                    trial = read(dest / 'trial.json')
                    row.update(status=trial['status'], summary=trial.get('summary'), configuration=trial.get('configuration'),
                               build=trial.get('build'), trial_sha256=sha(dest / 'trial.json'))
                    if row['status'] in VALID:
                        first = STATE.match((dest / 'run/state.log').read_text().splitlines()[0])
                        expected = [scenario['initial_observed'][k] for k in ('hp', 'max_hp', 'sp', 'max_sp')]
                        if not first or list(map(int, first.groups()[3:])) != expected:
                            raise ValueError('initial loaded state differs')
                        config = row['configuration']
                        if not config or config['template_sha256'] != sha(template):
                            raise ValueError('configuration receipt missing/mismatched')
                        if plan and config['loaded_plan_sha256'] != sha(plan):
                            raise ValueError('plan receipt mismatched')
                    row['execution_hash'] = hashed(dict(pairing=pairing, arm=arm, build=row.get('build')))
                except Exception as error:
                    row.update(status='harness_failure', reason=str(error))
                row['elapsed_seconds'] = time.monotonic() - tick
                write(dest / 'cell.json', row)
    result = collect(definition_path, output, root)
    result['elapsed_seconds'] = time.monotonic() - start
    write(output / 'execution.json', dict(definition_sha256=sha(definition_path),
                                         elapsed_seconds=result['elapsed_seconds']))
    write(output / 'comparison.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('freeze')
    p.add_argument('--spec', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    for action in ('run', 'collect'):
        p = sub.add_parser(action)
        p.add_argument('--definition', required=True, type=Path)
        p.add_argument('--out', required=True, type=Path)
        if action == 'run':
            p.add_argument('--source', required=True, type=Path)
    args = parser.parse_args()
    if args.action == 'freeze':
        freeze(args.spec, args.out)
        return 0
    if args.action == 'run':
        result = run(args.definition, args.source.resolve(), args.out.resolve())
        print(f"{len(result['cells'])} cells in {result['elapsed_seconds']:.2f}s; " + str([p['outcome'] for p in result['pairs']]))
    else:
        result = collect(args.definition, args.out)
    return int(any(c['status'] not in VALID for c in result['cells']))


if __name__ == '__main__':
    raise SystemExit(main())
