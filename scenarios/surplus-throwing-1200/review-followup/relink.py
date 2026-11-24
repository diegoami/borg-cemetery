import json
import shlex
import subprocess
import sys
from pathlib import Path

build, work = map(Path, sys.argv[1:])
entry, = [row for row in json.loads((build / "compile_commands.json").read_text())
          if row["file"].endswith("/frontend/main-borgh.c")]
original = Path(entry["file"])
source = work / "main-borgh-fixture.c"
text = original.read_text()
text = text.replace("static void prepare_borg_start(void)", '#include "fixture.inc"\n\nstatic void prepare_borg_start(void)')
text = text.replace("\t\tRand_quick = false;\n", "\t\tRand_quick = false;\n\t\tfixture_prepare();\n", 1)
source.write_text(text)
object_file = work / "main-borgh-fixture.o"
command = shlex.split(entry["command"])
command[command.index(str(original))] = str(source)
command[command.index("-o") + 1] = str(object_file)
subprocess.run(command, cwd=build, check=True)
link = shlex.split((build / "CMakeFiles/angband.dir/link.txt").read_text())
link[link.index(entry["output"])] = str(object_file)
link[link.index("-o") + 1] = str(work / "angband-fixture")
subprocess.run(link, cwd=build, check=True)
