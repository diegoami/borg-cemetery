#!/usr/bin/env python3
"""Create birth reproduction recipes for all retained natural incident deaths."""
import argparse
from pathlib import Path
import shutil
import re

from reproduce_native_death import inputs
from synthetic_suite import read, sha, write, kv

ROOT=Path(__file__).resolve().parents[1]


def create(dataset,source,runtime,artifact,root=ROOT):
    shared=dataset/'reproduction-inputs'
    shared.mkdir(parents=True,exist_ok=True)
    build=kv(runtime/'BUILD_ID');binary=runtime/'game/angband'
    if sha(binary)!=build['binary_sha256']:raise ValueError('original runtime binary differs')
    for name,path in [('base-borg.txt',source/'harness/borg.txt'),('profile.txt',source/'harness/profiles/reborn-default.txt')]:
        dest=shared/name
        if dest.exists() and dest.read_bytes()!=path.read_bytes():raise ValueError('configuration changed')
        if not dest.exists():shutil.copyfile(path,dest)
    data=runtime/'game/lib'
    manifest=dict(schema='borg-cemetery/native-runtime@1',source_commit=build['git_rev'],source_sha256=build['source_sha256'],binary_sha256=build['binary_sha256'],
        build=build,artifact=artifact,game_data_files={'lib/'+p.relative_to(data).as_posix():sha(p) for p in sorted(data.rglob('*')) if p.is_file()})
    runtime_path=shared/'runtime.json'
    if runtime_path.exists() and read(runtime_path)!=manifest:raise ValueError('runtime manifest changed')
    write(runtime_path,manifest)
    def ref(path):return dict(path=path.relative_to(root).as_posix(),sha256=sha(path))
    recipes=[]
    for harvest in sorted((dataset/'preparation').glob('class-*/harvest.json')):
        document=read(harvest)
        for attempt in document['attempts']:
            if not attempt.get('summary',{}).get('dead'):continue
            path=harvest.parent/'attempts'/attempt['id'];records=list((path/'native-deaths').glob('*/record.json'))
            if len(records)!=1:raise ValueError('natural death dossier absent')
            record=read(records[0]);identity=record['identity']
            if identity['binary_sha256']!=manifest['binary_sha256']:raise ValueError('natural death used different binary')
            text=(shared/'base-borg.txt').read_text()
            for key,value in [('borg_respawn_race',record['terminal']['race_idx']),('borg_respawn_class',record['terminal']['class_idx']),('borg_cheat_death','FALSE')]:
                text=re.sub('^'+key+' = .*$',key+' = '+str(value),text,flags=re.MULTILINE)
            config=shared/'borg-configs'/('race'+str(record['terminal']['race_idx'])+'-class'+str(record['terminal']['class_idx'])+'.txt')
            config.parent.mkdir(exist_ok=True)
            if config.exists() and config.read_text()!=text:raise ValueError('effective borg configuration changed')
            if not config.exists():config.write_text(text)
            recipe=dict(schema='borg-cemetery/native-death-recipe@1',start='birth',repository='diegoami/borg-reborn-rs',
                source_commit=identity['git_rev'],source_sha256=identity['source_sha256'],binary_sha256=identity['binary_sha256'],
                seed=identity['seed'],race_idx=record['terminal']['race_idx'],class_idx=record['terminal']['class_idx'],turn_cap=100000,flags='menu',
                environment=dict(BORG_CORE='reborn'),record=ref(records[0]),borg_txt=ref(config),profile=ref(shared/'profile.txt'),runtime=ref(runtime_path),
                original_continuation_verified=False,independent_life=False)
            inputs(recipe,root)
            dest=path/'reproduction-recipe.json'
            if dest.exists() and read(dest)!=recipe:raise ValueError('frozen death recipe changed')
            if not dest.exists():write(dest,recipe)
            recipes.append(dict(id=read(records[0].parent/'death-id.json')['id'],recipe=ref(dest)))
    checks=[];known={r['recipe']['sha256'] for r in recipes}
    for path in sorted((dataset/'reproduction-checks').rglob('reproduction.json')):
        check=read(path)
        if check.get('status')=='reproduced' and check.get('recipe_sha256') in known:checks.append(path.relative_to(dataset).as_posix())
    write(dataset/'reproduction-recipes.json',dict(schema='borg-cemetery/incident-reproduction-recipes@1',cases=recipes,verified_count=len(checks),verified_checks=checks))
    return recipes


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('dataset','source','runtime','artifact'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();rows=create(a.dataset.resolve(),a.source.resolve(),a.runtime.resolve(),read(a.artifact))
    print(len(rows),'natural birth recipes validated; endpoint reproduction remains unverified')
