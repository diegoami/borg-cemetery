#!/usr/bin/env python3
"""Copy only frozen selected inputs for assembly; full harvest stays a raw artifact."""
import argparse
from pathlib import Path
import shutil
from synthetic_suite import read


def pack(harvest, out):
    if out.exists():raise ValueError('fresh output required')
    doc=read(harvest/'harvest.json');out.mkdir(parents=True)
    for name in ('harvest.json','spec.json','build.json'):shutil.copyfile(harvest/name,out/name)
    attempts={r['source_attempt'] for r in doc['selected']}
    for name in attempts:
        source=harvest/'attempts'/name;dest=out/'attempts'/name;dest.mkdir(parents=True)
        for file in ('config.txt','summary.json','process.json'):
            if (source/file).exists():shutil.copyfile(source/file,dest/file)
        if (source/'native-deaths').exists():shutil.copytree(source/'native-deaths',dest/'native-deaths')
    for row in doc['selected']:
        source=harvest/'cases'/row['directory'];dest=out/'cases'/row['directory'];dest.mkdir(parents=True)
        for file in ('start.save.gz','profile.txt','initial-observation.json','incident.json'):shutil.copyfile(source/file,dest/file)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--harvest',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();pack(a.harvest.resolve(),a.out.resolve())
