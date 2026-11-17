"""Private-file configuration adapter for the existing borg-rs controller.

As Zoo's borgrs adapter does: write a per-cell borg.txt, normalize fixed birth/
cheat fields, ship a pinned plan, clear ambient BORG variables and run the native
frontend. Named parameters and the loaded plan have native readback receipts;
classic flags without a native receipt stay explicitly unverified.
"""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from run_batch import command
from run_scenario import run_scenario
from synthetic_suite import read, sha, write


def settings(text):
    result = {}
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line or not line.startswith('borg_'):
            continue
        match = re.fullmatch(r'(borg_[a-z0-9_]+)\s*=\s*(.*?)\s*', line)
        if not match or match[1] in result:
            raise ValueError('malformed/duplicate borg.txt setting: ' + line)
        value = match[2]
        if value.upper() in ('TRUE', 'FALSE'):
            value = int(value.upper() == 'TRUE')
        elif re.fullmatch(r'-?[0-9]+', value):
            value = int(value)
        result[match[1]] = value
    return result


def override(text, name, value):
    pattern = re.compile(r'^\s*' + re.escape(name) + r'\s*=.*$', re.MULTILINE)
    line = name + ' = ' + str(value)
    if pattern.search(text):
        return pattern.sub(line, text)
    return text.rstrip('\n') + '\n' + line + '\n'


def configured_adapter(template, plan=None, exact_turns=False):
    original = template.read_text()
    requested = settings(original)
    if requested.get('borg_plan') and plan is None:
        raise ValueError('borg.txt names a plan but no pinned errands file was supplied')
    def execute(source, binary, raw, save, scenario, cap, inherited, wall):
        for name in ('user', 'save', 'archive', 'panic', 'scores'):
            (raw / name).mkdir(parents=True, exist_ok=True)
        text = original
        fixed = dict(borg_respawn_race=scenario['race_idx'], borg_respawn_class=scenario['class_idx'],
                     borg_cheat_death='FALSE', borg_respawn_winners='FALSE', borg_reborn_core='FALSE')
        for name, value in fixed.items():
            text = override(text, name, value)
        if plan:
            shutil.copyfile(plan, raw / 'user/selected-plan.txt')
            text = override(text, 'borg_plan', 'selected-plan.txt')
        (raw / 'user/borg.txt').write_text(text)
        env = {k: v for k, v in inherited.items() if not k.startswith(('BORG_', 'ANGBAND_'))}
        for name in ('BORG_CEMETERY_DIR', 'BORG_OBSERVATION_LOG'):
            if name in inherited:
                env[name] = inherited[name]
        env.update(BORG_CORE='borg-rs', BORG_CORE_OVERRIDES='on', BORG_RUN_DIR=str(raw),
                   TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
        argv = [str(binary), '-mborgh']
        argv += ['-d' + name + '=' + str(raw / name) for name in ('user', 'save', 'archive', 'panic', 'scores')]
        argv += ['-uBorg', '--', '-seed', str(scenario['birth_seed']), '-race', str(scenario['race_idx']),
                 '-class', str(scenario['class_idx']), '-turns', str(cap), '-menu-letters', '-screen',
                 '-load', str(save), '-keep-load-rng', '-summary', str(raw / 'summary.json')]
        if exact_turns:
            argv += ['-exact-turns']
        for flag, filename in (('-keylog', 'keys.log'), ('-msglog', 'messages.log'), ('-statelog', 'state.log')):
            argv += [flag, str(raw / filename)]
        rc = command([sys.executable, source / 'harness/supervise.py', '--receipt', raw / 'process.json',
                      '--diagnostics', raw, '--timeout', str(wall), '--', *argv],
                     cwd=binary.parent, env=env, log=raw / 'stderr.log', timeout=wall + 30)
        config = dict(flags='menu,keep-load-rng', keep_load_rng='1', save_sha256=sha(save),
                      borg_txt_sha256=sha(raw / 'user/borg.txt'), borg_core='borg-rs', borg_core_overrides='on')
        proof = dict(core='borg-rs', template_sha256=sha(template), applied_borg_txt_sha256=config['borg_txt_sha256'],
                     fixed_settings=fixed, named_parameters={}, classic_settings_verification='input_file_only',
                     plan_sha256=sha(plan) if plan else None, loaded_plan_sha256=None)
        if (raw / 'params-core.json').exists():
            config['params_core_sha256'] = sha(raw / 'params-core.json')
            actual = {v['name']: v for v in read(raw / 'params-core.json')}
            for name, value in requested.items():
                if name.startswith('borg_param_'):
                    row = actual.get(name.removeprefix('borg_param_'))
                    if not row or row['value'] != value or row['origin'] != 'borg.txt':
                        raise ValueError('parameter not effective: ' + name)
                    proof['named_parameters'][name] = value
        elif not rc:
            raise ValueError('selected core did not produce its parameter receipt')
        if plan and not rc:
            loaded = raw / 'errands_plan.txt'
            proof['loaded_plan_sha256'] = sha(loaded) if loaded.exists() else None
            if proof['loaded_plan_sha256'] != proof['plan_sha256']:
                raise ValueError('requested errands file was not loaded')
            config['borg_errands_plan_sha256'] = proof['plan_sha256']
        (raw / 'config.txt').write_text(''.join(k + '=' + v + '\n' for k, v in config.items()))
        if not rc:
            process = read(raw / 'process.json')
            if process.get('executable_sha256_before') != sha(binary) or process.get('executable_sha256_after') != sha(binary):
                raise ValueError('executed binary identity differs')
        if (raw / 'messages.log').exists():
            proof['plan_messages'] = sum('Plan:' in line for line in (raw / 'messages.log').read_text().splitlines())
        write(raw / 'configuration.json', proof)
        # Keep every natural/loaded-branch death using the source's pinned exporter.
        if (raw / 'summary.json').exists() and read(raw / 'summary.json').get('dead') is True:
            export_env = dict(env, BORG_DEATH_RECORDS_DIR=str(raw.parent / 'native-deaths'))
            result = subprocess.run([sys.executable, source / 'tools/export-death.py', raw, '--impl', 'rust',
                '--build-id', binary.parent.parent / 'BUILD_ID', '--flags', config['flags']],
                env=export_env, capture_output=True, text=True)
            (raw / 'death-export.log').write_text(result.stdout + result.stderr)
            if result.returncode:
                raise ValueError('death preservation failed: ' + result.stderr[-500:])
        return rc
    return execute


def run_configured(source, scenario, out, template, plan=None, turns=1000, wall_seconds=5, exact_turns=False):
    return run_scenario(source, scenario, out, turns, wall_seconds,
                        execution_adapter=configured_adapter(template, plan, exact_turns=exact_turns))
