import json, pathlib, shlex, subprocess, sys

repo = pathlib.Path(sys.argv[1]).resolve()
build = repo / 'build/rust'
trial = pathlib.Path(sys.argv[2]).resolve()
trial.mkdir(parents=True, exist_ok=True)
src = trial / 'main-borgh.c'
code = (repo / 'engine/frontend/main-borgh.c').read_text()
code = code.replace('keycode_t k = script[script_pos++];', '''if (opt_load && script[script_pos] == SCRIPT_START_BORG && more_prompt_shown()) {
                Term_keypress(ESCAPE, 0);
                return 0;
            }
            keycode_t k = script[script_pos++];''')
if len(sys.argv) > 3:
    code = code.replace('static void prepare_borg_start(void)\n{', pathlib.Path(sys.argv[3]).read_text())
src.write_text(code)
info = next(i for i in json.loads((build / 'compile_commands.json').read_text()) if i['file'].endswith('main-borgh.c'))
args = shlex.split(info['command'])
idx = args.index('-o') + 1
oldobj = args[idx]
args[idx] = str(trial / 'main-borgh.o')
args[args.index(info['file'])] = str(src)
args.append('-I' + str(repo / 'engine/frontend'))
subprocess.run(args, cwd=info['directory'], check=True)
args = shlex.split((build / 'CMakeFiles/angband.dir/link.txt').read_text())
args[args.index(oldobj)] = str(trial / 'main-borgh.o')
args[args.index('-o') + 1] = str(trial / 'angband')
subprocess.run(args, cwd=build, check=True)
