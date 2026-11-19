#!/usr/bin/env python3
"""Run one saved encounter with an exact already-built Borg and configuration."""
import argparse
import fcntl
import hashlib
import os
from pathlib import Path
import subprocess

from encounter_suite import prepare
from run_batch import command
from run_scenario import run_scenario
from scenario_config import run_configured
from synthetic_suite import COMMIT, read, sha, write

ROOT=Path(__file__).resolve().parents[1]


def execute(suite,case_id,source,source_commit,core,tools,out,borg_txt=None,errands=None,profile=None):
    if not COMMIT.fullmatch(source_commit):raise ValueError('full source commit required')
    head=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    if head!=source_commit or subprocess.check_output(['git','-C',str(source),'status','--porcelain','--untracked-files=no'],text=True).strip():raise ValueError('source must be the exact clean requested checkout')
    if subprocess.check_output(['git','-C',str(tools),'rev-parse','HEAD'],text=True).strip()!=(source/'death-tools-pin.txt').read_text().strip():raise ValueError('native tools differ from this source required pin')
    manifest,cases=prepare(suite,ROOT)
    engine=dict(line.split('=',1) for line in (source/'engine/UPSTREAM').read_text().splitlines() if '=' in line)
    if engine['commit']!=manifest['engine_commit']:raise ValueError('saved encounter engine is incompatible')
    selected=[c for c in cases if c[0]==case_id]
    if len(selected)!=1:raise ValueError('case must occur exactly once in this suite')
    _,scenario,default_profile=selected[0]
    if core=='borg-rs' and (borg_txt is None or profile is not None):raise ValueError('borg-rs needs borg.txt; reborn parameter profiles are a different controller')
    if core=='reborn' and (borg_txt is not None or errands is not None):raise ValueError('file-based borg.txt/errands configuration requires borg-rs core')
    if out.exists():raise ValueError('fresh output directory required')
    previous=dict(os.environ)
    try:
        for key in list(os.environ):
            if key.startswith(('BORG_','ANGBAND_','BORGH_')) or key in ('SAVE_ROOT','STALL_TIMEOUT_SECONDS'):os.environ.pop(key)
        os.environ.update(BORG_CEMETERY_DIR=str(tools),BORG_CORE=core)
        with open('/tmp/angband-validation.lock','a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            if core=='borg-rs':
                rc=run_configured(source,scenario,out,borg_txt,errands,manifest['horizon_engine_turns'],manifest['wall_seconds'],exact_turns=True)
            else:
                def exact(src,binary,raw,save,spec,cap,env,wall):
                    return command(['bash','harness/run.sh',str(raw),str(spec['birth_seed']),str(spec['race_idx']),str(spec['class_idx']),str(cap),
                                    'menu,exact,keep-load-rng,save=input.save'],cwd=src,env=env,log=raw.parent/'launcher.log',timeout=wall+30)
                rc=run_scenario(source,scenario,out,manifest['horizon_engine_turns'],manifest['wall_seconds'],profile=profile or default_profile,execution_adapter=exact)
    finally:
        os.environ.clear();os.environ.update(previous)
    trial=read(out/'trial.json')
    receipt=dict(schema='borg-cemetery/single-encounter@1',case=case_id,source_commit=source_commit,core=core,suite_sha256=sha(suite),
                 scenario_sha256=sha(scenario/'scenario.json'),save_sha256=read(scenario/'scenario.json')['save_sha256'],trial_sha256=sha(out/'trial.json'),
                 borg_txt_sha256=sha(borg_txt) if borg_txt else None,errands_plan_sha256=sha(errands) if errands else None,
                 profile_sha256=sha(profile or default_profile) if core=='reborn' else None,status=trial['status'],exact_turns=True,
                 streams={name:sha(out/'run'/name) for name in ('keys.log','state.log','messages.log') if (out/'run'/name).exists()},independent_life=False)
    write(out/'single-encounter.json',receipt)
    print(trial['status']);return rc


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('suite','source','native-tools','out'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--case',required=True);p.add_argument('--source-commit',required=True);p.add_argument('--core',choices=['reborn','borg-rs'],required=True)
    p.add_argument('--borg-txt',type=Path);p.add_argument('--errands-plan',type=Path);p.add_argument('--profile',type=Path)
    a=p.parse_args()
    return execute(a.suite.resolve(),a.case,a.source.resolve(),a.source_commit,a.core,a.native_tools.resolve(),a.out.resolve(),
                   a.borg_txt.resolve() if a.borg_txt else None,a.errands_plan.resolve() if a.errands_plan else None,a.profile.resolve() if a.profile else None)


if __name__=='__main__':raise SystemExit(main())
