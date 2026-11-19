#!/usr/bin/env python3
"""Verify original native archives and retain every death in portable capsules."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import fcntl
import gzip
import hashlib
import json
from pathlib import Path,PurePosixPath
import shutil
import tarfile
import zipfile
from native.death_identity import ensure
from synthetic_suite import read,sha,write

ROOT=Path(__file__).resolve().parents[1]
STREAMS={'keys.log','state.log','messages.log'}
EXTRA={'process.json':'process.json','configuration.json':'configuration.json','errands_plan.txt':'loaded-errands-plan.txt','user/borg.txt':'applied-borg.txt'}


def retain(study_path,metadata_path,raw,scratch,out):
    if out.exists() or scratch.exists():raise ValueError('fresh evidence and scratch directories required')
    study=read(study_path);artifacts=read(metadata_path);cases={c['id']:c for c in study['cases']};arms={a['id']:a for a in study['arms']}
    expected_deaths={(a,c['id']) for c in study['cases'] for a in arms if c['outcomes'][a]=='death'}
    scratch.mkdir(parents=True);out.mkdir(parents=True)
    def extract(a):
        arm=a['name'].removeprefix('paired-native-').split('-')[0]
        if arm not in arms:raise ValueError('unknown native arm')
        path=raw/str(a['source_run'])/(a['name']+'.zip')
        if sha(path)!=a['digest'].removeprefix('sha256:'):raise ValueError('native artifact ZIP changed')
        hashes={};packets=[]
        with zipfile.ZipFile(path) as z:
            if z.namelist()!=['native.tgz']:raise ValueError('unexpected native artifact layout')
            with z.open('native.tgz') as stream,tarfile.open(fileobj=stream,mode='r|gz') as t:
                for m in t:
                    if not m.isfile():continue
                    p=PurePosixPath(m.name);parts=p.parts
                    if p.is_absolute() or '..' in parts:raise ValueError('unsafe native member')
                    if len(parts)<4 or parts[:2]!=('attempt','native'):continue
                    case=parts[2];key=(arm,case)
                    if case not in cases:raise ValueError('unknown native case')
                    if len(parts)==5 and parts[3]=='run' and parts[4] in STREAMS:
                        h=hashlib.sha256();f=t.extractfile(m)
                        for block in iter(lambda:f.read(1048576),b''):h.update(block)
                        hashes.setdefault(key,{})[parts[4]]=h.hexdigest()
                    elif key in expected_deaths and parts[3]=='run' and '/'.join(parts[4:]) in EXTRA:
                        dest=scratch/'extra'/arm/case/EXTRA['/'.join(parts[4:])];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.extractfile(m).read())
                    elif key in expected_deaths and len(parts)==4 and parts[3]=='profile.txt':
                        dest=scratch/'extra'/arm/case/'reborn-profile.txt';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.extractfile(m).read())
                    elif key in expected_deaths and len(parts)==6 and parts[3]=='native-deaths' and parts[4].startswith('D'):
                        if m.size>16777216:raise ValueError('oversized compact native packet member')
                        dest=scratch/'packets'/arm/case/parts[4]/parts[5]
                        if dest.exists():raise ValueError('repeated native packet member')
                        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.extractfile(m).read())
                        if parts[5]=='record.json':packets.append(dict(arm=arm,case=case,path=dest.parent,artifact_id=a['id'],source_run=a['source_run']))
        for (arm,case),values in hashes.items():
            if values!=cases[case]['details'][arm]['streams']:raise ValueError('original raw gameplay stream differs from collected receipt')
        return hashes,packets
    all_hashes={};packets=[]
    with open('/tmp/angband-validation.lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        with ThreadPoolExecutor(max_workers=4) as pool:
            for i,(hashes,found) in enumerate(pool.map(extract,artifacts),1):
                if set(hashes)&set(all_hashes):raise ValueError('replayed scenario in formal tier chain')
                all_hashes.update(hashes);packets.extend(found)
                print('Verified native archives',i,'/',len(artifacts),flush=True)
    if len(all_hashes)!=1998 or { (p['arm'],p['case']) for p in packets}!=expected_deaths or len(packets)!=len(expected_deaths):raise ValueError('native streams/deaths do not account for the complete study')
    rows=[];pending=[]
    for packet in packets:
        directory=packet['path'];record=read(directory/'record.json');case=cases[packet['case']];arm=arms[packet['arm']];summary=case['details'][packet['arm']]['summary']
        for name,digest in record['files_sha256'].items():
            if Path(name).name!=name or sha(directory/name)!=digest:raise ValueError('native packet payload changed')
        if record['identity']['git_rev']!=arm['source']['commit'] or record['identity']['binary_sha256']!=arm['build']['binary_sha256']:raise ValueError('native packet source/build differs')
        terminal=record['terminal']
        if terminal['turn']!=summary['game_turns'] or terminal['cause']!=summary['death_cause'] or terminal['class_idx']!=case['class_idx']:raise ValueError('native death endpoint differs')
        original=[a for a in record['attempts'] if a['role']=='original']
        if len(original)!=1 or original[0]['raw_sha256']!=case['details'][packet['arm']]['streams']:raise ValueError('native dossier stream identity differs')
        identity=ensure(directory)
        extra=scratch/'extra'/packet['arm']/packet['case']
        if extra.exists():shutil.copytree(extra,directory/'extra')
        row=dict(id=identity['id'],arm=packet['arm'],scenario=packet['case'],source_run=packet['source_run'],artifact_id=packet['artifact_id'],
                 origin=case['origin'],save_sha256=case['save_sha256'],record_sha256=sha(directory/'record.json'),streams=original[0]['raw_sha256'],independent_life=False)
        if packet['source_run']==44046247609:
            existing=ROOT/'validation/borg-zoo/balanced999/paired-smoke-44046247609/native-deaths'/packet['arm']/packet['case']/directory.name
            if sha(existing/'record.json')!=row['record_sha256']:raise ValueError('retained smoke record differs')
            row['record']=existing.relative_to(ROOT).as_posix()+'/record.json'
        else:
            relative=(out/'native-deaths'/packet['arm']/packet['case']/directory.name).relative_to(ROOT)
            dest=ROOT/relative;dest.mkdir(parents=True)
            for name in ('record.json','death-id.json'):shutil.copyfile(directory/name,dest/name)
            row['record']=(relative/'record.json').as_posix();pending.append((row,directory,relative))
        rows.append(row)
    capsules=[]
    for arm in arms:
        group=[p for p in pending if p[0]['arm']==arm]
        for offset in range(0,len(group),50):
            items=group[offset:offset+50];archive=out/'capsules'/f'{arm}-{offset//50:03d}.tgz';archive.parent.mkdir(exist_ok=True)
            with archive.open('xb') as raw_out,gzip.GzipFile(fileobj=raw_out,mode='wb',filename='',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w|') as t:
                for row,directory,relative in items:
                    for path in sorted(directory.rglob('*')):
                        if not path.is_file():continue
                        info=t.gettarinfo(str(path),arcname=(relative/path.relative_to(directory)).as_posix());info.mtime=info.uid=info.gid=0;info.uname=info.gname=''
                        with path.open('rb') as f:t.addfile(info,f)
            digest=sha(archive);ref=archive.relative_to(ROOT).as_posix()
            capsules.append(dict(path=ref,sha256=digest,bytes=archive.stat().st_size,death_packets=len(items)))
            for row,directory,relative in items:
                row['capsule']=ref;row['capsule_sha256']=digest
                write(ROOT/relative/'archive-info.json',dict(archive=ref,archive_sha256=digest,record_sha256=row['record_sha256'],
                     payload_sha256={p.relative_to(directory).as_posix():sha(p) for p in directory.rglob('*') if p.is_file()},independent_life=False))
                (ROOT/relative/'README.md').write_text('# Archived native death packet\n\nCanonical ID: `'+row['id']+'`.\nThe original record and additive identity index are here; complete native payload\nbytes and configuration are in the checked capsule. From the Cemetery root:\n\n```sh\ntar --skip-old-files -xzf '+ref+'\n```\n\nOriginal payload hashes are in record.json; archive-info.json covers the capsule\nand all payload files. This is a saved continuation, not an independent life.\n')
    write(out/'lineage.json',dict(schema='borg-cemetery/paired-native-evidence@1',study_plan_hash=study['plan_hash'],expected_cells=1998,streams_verified=len(all_hashes)*3,
        deaths=len(rows),retained_smoke_packets=20,new_archived_packets=len(pending),capsules=capsules,records=rows,independent_life=False))
    write(out/'artifacts.json',artifacts)
    print('Retained',len(rows),'actual death packets;',len(all_hashes)*3,'original streams verified;',len(capsules),'capsules',flush=True)
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('study','artifacts','raw','scratch','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();retain(a.study.resolve(),a.artifacts.resolve(),a.raw.resolve(),a.scratch.resolve(),a.out.resolve())
