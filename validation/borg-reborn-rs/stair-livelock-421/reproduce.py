import argparse,hashlib,json,os,re,shutil,subprocess,pathlib,collections
p=argparse.ArgumentParser();p.add_argument('--binary',required=True,type=pathlib.Path);p.add_argument('--out',required=True,type=pathlib.Path);p.add_argument('--source-root',default='/workspace/work/p351',type=pathlib.Path);p.add_argument('--seed',type=int,default=1019921749);p.add_argument('--race',type=int,default=1);p.add_argument('--cls',type=int,default=0);p.add_argument('--trip',type=int,default=0);p.add_argument('--town',type=int,default=1);p.add_argument('--plan',default='errands_plan_ambitious.txt');p.add_argument('--turns',type=int,default=100000);p.add_argument('--plan-file',type=pathlib.Path);a=p.parse_args()
expected={1019921749:(1,0),926210318:(7,6),1269315224:(6,6)}
if a.seed in expected and (a.race,a.cls)!=expected[a.seed]:raise SystemExit('Known-case race/class mismatch: '+str((a.seed,a.race,a.cls))+' expected '+str(expected[a.seed]))
out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
for n in ['user','save','archive','panic','scores']:(out/n).mkdir()
borg=(a.source_root/'harness/borg.txt').read_text()
settings={'borg_reborn_core':'borg-rs','borg_reborn_errand':'none','borg_town_plan':str(a.town),'borg_trip_policy':str(a.trip)}
for k,v in settings.items():
 borg=re.sub(r'^'+k+r'\s*=.*$',k+' = '+v,borg,flags=re.M) if re.search(r'^'+k+r'\s*=',borg,re.M) else borg+'\n'+k+' = '+v+'\n'
borg+='\nborg_plan = '+a.plan+'\n';(out/'user/borg.txt').write_text(borg)
shutil.copy2(a.plan_file or a.source_root/'harness/plans'/a.plan,out/'user'/a.plan)
exe=a.binary.resolve();env={k:v for k,v in os.environ.items() if not k.startswith(('BORG_','BORGH_','ANGBAND_'))};env.update(BORG_CORE='borg-rs',BORG_ERRAND='none',BORG_RUN_DIR=str(out),LANG='C.UTF-8',LC_ALL='C.UTF-8',TZ='UTC')
command=[str(exe),'-mborgh','-n']+[f'-d{k}={out/k}' for k in ['user','save','archive','panic','scores']]+['-uStair421','--','-seed',str(a.seed),'-race',str(a.race),'-class',str(a.cls),'-menu-letters','-exact-turns','-turns',str(a.turns),'-keylog',str(out/'keys.log'),'-msglog',str(out/'messages.log'),'-statelog',str(out/'state.log'),'-summary',str(out/'summary.json')]
receipt={'command':command,'environment':{k:v for k,v in env.items() if k.startswith('BORG_')},'binary_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'settings':settings,'seed':a.seed,'race':a.race,'class':a.cls,'constructed_plan':a.plan_file is not None,'plan_sha256':hashlib.sha256((out/'user'/a.plan).read_bytes()).hexdigest(),'borg_txt_sha256':hashlib.sha256((out/'user/borg.txt').read_bytes()).hexdigest()}
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (out/'console.log').open('w') as log:r=subprocess.run(command,cwd=exe.parent,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
receipt['exit_code']=r.returncode
if (out/'summary.json').is_file():
 receipt['summary']=json.loads((out/'summary.json').read_text())
 race_names=[line.split(':',1)[1] for line in (a.source_root/'engine/angband/lib/gamedata/p_race.txt').read_text().splitlines() if line.startswith('name:')]
 receipt['birth_matches_request']=receipt['summary']['race']==race_names[a.race]
 assert receipt['birth_matches_request'],receipt['summary']['race']
for n in ['keys.log','messages.log','state.log']:
 if (out/n).exists():receipt[n+'_sha256']=hashlib.sha256((out/n).read_bytes()).hexdigest()
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));raise SystemExit(r.returncode)
