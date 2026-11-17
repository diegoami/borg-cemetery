#!/usr/bin/env python3
"""Retain compact native death/reproduction evidence from an exact raw Actions ZIP.

Raw streams/checkpoints remain byte-for-byte in the original archive. This
extracts all attempted-life journals and native death packets, including
unselected deaths and saved-start probes. It never rewrites a packet.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
import zipfile

from native.death_identity import ensure
from synthetic_suite import read, sha, write

SMALL={'harvest.json','spec.json','build.json','harvest-progress.json','config.txt','summary.json',
       'process.json','selection.json','checkpoint-archive.json','errands_plan.txt'}


def retain(archive, metadata, out):
    if out.exists():raise ValueError('fresh evidence directory required')
    if sha(archive) != metadata['digest'].removeprefix('sha256:'):
        raise ValueError('original artifact ZIP digest differs')
    out.mkdir(parents=True)
    inventory=[]
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if len(names)!=1 or not names[0].startswith('harvest-class-') or not names[0].endswith('.tgz') or '/' in names[0]:
            raise ValueError('unexpected raw artifact layout')
        with z.open(names[0]) as stream,tarfile.open(fileobj=stream,mode='r|gz') as t:
            for member in t:
                path=PurePosixPath(member.name)
                if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0]!='harvest' or member.issym() or member.islnk():
                    raise ValueError('unsafe archive member')
                if not member.isfile():continue
                if 'native-deaths' in path.parts:
                    # Native packets are compact, and every payload is retained.
                    if path.name.startswith('.'):continue
                elif path.name not in SMALL and 'completed' not in path.parts:continue
                if member.size>16*1024*1024:raise ValueError('unexpected large compact evidence member')
                relative=Path(*path.parts[1:]);dest=out/relative
                if dest.exists():raise ValueError('duplicate archive member')
                data=t.extractfile(member).read();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
                inventory.append(dict(path=relative.as_posix(),sha256=hashlib.sha256(data).hexdigest()))
    dossiers=[]
    for record_path in sorted(out.rglob('native-deaths/*/record.json')):
        record=read(record_path)
        for name,digest in record.get('files_sha256',{}).items():
            path=(record_path.parent/name).resolve();path.relative_to(record_path.parent.resolve())
            if sha(path)!=digest:raise ValueError('native dossier payload differs')
        identity=ensure(record_path.parent)
        dossiers.append(dict(id=identity['id'],path=record_path.parent.relative_to(out).as_posix(),
                             encounter_family=record['encounter_family'],terminal=record['terminal']))
    document=read(out/'harvest.json')
    natural=[]
    for row in document['attempts']:
        if row.get('summary',{}).get('dead'):
            packets=list((out/'attempts'/row['id']/'native-deaths').glob('*/record.json'))
            if len(packets)!=1:raise ValueError('natural death missing its retained dossier')
            natural.append(row['id'])
    result=dict(schema='borg-cemetery/incident-artifact-retention@1',artifact=metadata,
                archive_sha256=sha(archive),files=inventory,native_dossiers=dossiers,natural_deaths=natural,
                independent_life=False,raw_streams='Original artifact ZIP, retained separately without rewriting')
    write(out/'retention.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('archive','metadata','out'):p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=retain(a.archive.resolve(),read(a.metadata),a.out.resolve())
    print(len(r['natural_deaths']),'natural deaths;',len(r['native_dossiers']),'native packets retained')
