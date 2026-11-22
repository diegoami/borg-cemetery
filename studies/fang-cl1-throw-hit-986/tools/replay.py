import re, sys, subprocess, os, shutil, pathlib, hashlib
src, out, seed, race, cls = sys.argv[1], pathlib.Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4], sys.argv[5]
turns = sys.argv[6] if len(sys.argv) > 6 else '100000'
extra = sys.argv[7:]  # name=value overrides
src = pathlib.Path(src).resolve(); game = src/'build/rust/game'
def ov(text, name, value):
    line = f'{name} = {value}'
    pat = re.compile(rf'^[ \t]*{re.escape(name)}[ \t]*=.*$', re.M)
    if pat.search(text): return pat.sub(line, text)
    m = '[BEGIN FORMULA SECTION]'
    if m in text: return text.replace(m, line + '\n\n' + m, 1)
    return text.rstrip('\n') + '\n' + line + '\n'
if out.exists(): shutil.rmtree(out)
for d in ('user','save','archive','panic','scores'): (out/d).mkdir(parents=True)
t = (src/'harness/borg.txt').read_text()
for n, v in [('borg_respawn_race', race), ('borg_respawn_class', cls), ('borg_cheat_death','FALSE'), ('borg_respawn_winners','FALSE'),
             ('borg_reborn_core','borg-rs'), ('borg_reborn_errand','none')] + [tuple(e.split('=',1)) for e in extra]:
    t = ov(t, n, v)
t = re.sub(r'^[ \t]*borg_world[ \t]*=[ \t]*(\S*)[ \t]*\n?', '', t, flags=re.M)
(out/'user/borg.txt').write_text(t)
shutil.copy(src/'harness/scary_monsters.txt', out/'user/scary_monsters.txt')
argv = [str(game/'angband'), '-mborgh', '-n', '-uBorg'] + [f'-d{d}={out/d}' for d in ('user','save','archive','panic','scores')] + \
  ['--','-seed',seed,'-race',race,'-class',cls,'-turns',turns,'-keylog',str(out/'keys.log'),'-summary',str(out/'summary.json'),'-menu-letters','-exact-turns',
   '-statelog',str(out/'state.log'),'-msglog',str(out/'messages.log')]
pre = os.environ.get('PRE','').split()
env = dict(os.environ, TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8')
for n in [n for n in env if n.startswith('BORG_')]: del env[n]
with open(out/'stderr.log','w') as e: rc = subprocess.run(pre+argv, cwd=game, env=env, stdout=open(out/'stdout.log','w'), stderr=e).returncode
print('rc', rc, hashlib.sha256((out/'keys.log').read_bytes()).hexdigest()[:16], (out/'summary.json').read_text()[:300] if (out/'summary.json').exists() else '')
