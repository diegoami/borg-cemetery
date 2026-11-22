from pathlib import Path
import fcntl,hashlib,json,os,shutil,signal,subprocess,time
root=Path('/tmp/T788-town-fight'); out=root/'named-checks-5f41b563';out.mkdir(exist_ok=False)
snaps={k:json.loads((root/f'{k}-snapshot.json').read_text()) for k in ('control','candidate')}
cases=[]
for seed,race,cls in [(101,0,0),(102,2,1)]:
 for build,mode in [('control',0),('candidate',0),('candidate',2),('control',1),('candidate',1)]:cases.append((seed,race,cls,build,mode))
for build in ('control','candidate'):cases.append((807683971,0,7,build,1))
assert len(cases)==12
(root/'named-plan.json').write_text(json.dumps({'scope':'two exact named smoke starts and the previously named naga regression; no population arm','turn_cap':100000,'cases':cases,'snapshots':snaps},indent=2)+'\n')
records=[]
for seed,race,cls,build,mode in cases:
 snap=snaps[build];dest=out/f'{build}-mode{mode}-{seed}-{race}-{cls}';assert not dest.exists()
 settings=[f'borg_param_caution_winning_fight={mode}']
 argv=['python3',str(root/'zrun.py'),snap['game'],snap['harness'],str(dest),str(seed),str(race),str(cls),'100000',*settings]
 record={'start':[seed,race,cls],'build':build,'mode':mode,'overrides':settings,'source_commit':snap['head'],'argv':argv,'runner_rc':None,'failure':None}
 with open('/tmp/angband-validation.lock','a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
  try: stdout,stderr=process.communicate(timeout=180);record.update(runner_rc=process.returncode,stdout=stdout,stderr=stderr)
  except subprocess.TimeoutExpired:
   os.killpg(process.pid,signal.SIGKILL);process.communicate();record['failure']='timeout'
 dest.mkdir(exist_ok=True)
 shutil.copyfile(Path(snap['game'])/'BUILD_ID',dest/'BUILD_ID')
 summary=dest/'summary.json'
 if summary.exists():
  record['summary']=json.loads(summary.read_text())
  if record['summary'].get('stop_reason') not in ('death','turns'):record['failure']=record['summary'].get('stop_reason')
 else:record['failure']=record['failure'] or 'missing_summary'
 params=dest/'params-core.json'
 if params.exists():
  actual={p['name']:p['value'] for p in json.loads(params.read_text())}
  if actual.get('caution_winning_fight')!=mode:record['failure']='parameter_mismatch'
 else:record['failure']=record['failure'] or 'missing_params'
 record['hashes']={n:hashlib.sha256((dest/n).read_bytes()).hexdigest() for n in ('keys.log','state.log','messages.log','params-core.json','user/borg.txt','user/scary_monsters.txt') if (dest/n).exists()}
 # Match harness/native-export metadata, retaining the exact copied profile.
 receipt=dict(l.split('=',1) for l in (dest/'BUILD_ID').read_text().splitlines() if '=' in l)
 config={'borg_impl':'rust','borg_core':'borg-rs','borg_errand':'none','flags':'exact,menu','borg_txt_sha256':record['hashes'].get('user/borg.txt',''),'borg_scary_list_sha256':record['hashes'].get('user/scary_monsters.txt',''),'params_core_sha256':record['hashes'].get('params-core.json','')}
 config.update({f'build_id_{k}':v for k,v in receipt.items()})
 (dest/'config.txt').write_text(''.join(f'{k}={v}\n' for k,v in sorted(config.items())))
 (dest/'trial.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
 (out/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
 d=record.get('summary',{});print(dest.name,d.get('stop_reason'),d.get('game_turns'),d.get('death_cause'),d.get('max_clevel'),'failure=',record['failure'],flush=True)
 if record['failure'] or record['runner_rc']!=0:raise SystemExit('named replay failed; all completed/failed attempts retained')
