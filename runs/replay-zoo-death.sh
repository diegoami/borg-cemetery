#!/usr/bin/env bash
# Replay a zoo death exactly from its inputs in this repository; no GitHub token or zoo artifact needed.
#   runs/replay-zoo-death.sh runs/<case>/replay/<SEED> [WORKDIR] [SOURCE]
# SOURCE: a borg-reborn-rs checkout to build (default: clone it into WORKDIR at the death's commit). Pass your own
# branch's checkout to test a change on the same game; the key check then reports whether the game still matches.
# Needs git, Rust/Cargo, CMake, a C compiler and python3. Writes WORKDIR/run/{messages,state,keys}.log.
set -euo pipefail
C=$(cd "$1" && pwd); WD=${2:-$PWD/replay-$(basename "$C")}; mkdir -p "$WD"; WD=$(cd "$WD" && pwd)
REV=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['build']['ref'])" "$C/zoo-death.json")
SRC=${3:-$WD/src}
if [ ! -d "$SRC" ]; then git clone -q https://github.com/diegoami/borg-reborn-rs "$SRC"; git -C "$SRC" checkout -q "$REV"; fi
SRC=$(cd "$SRC" && pwd)
[ -x "$SRC/build/rust/game/angband" ] || (cd "$SRC" && BORG_IMPL=rust bash harness/build.sh)   # the zoo build: no X11, recorder off
eval "$(grep -E '^(race_idx|class_idx|turns)=' "$C/config.txt")"
SEED=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['seed'])" "$C/zoo-death.json")
W=$WD/run; rm -rf "$W"; mkdir -p "$W"/{save,archive,panic,scores}; cp -r "$C/user" "$W/user"
cd "$SRC/build/rust/game"
env $(env | grep -o '^BORG_[A-Z_]*' | sed 's/^/-u /') TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  ./angband -mborgh -n -uPlayer -duser="$W/user" -dsave="$W/save" -darchive="$W/archive" -dpanic="$W/panic" -dscores="$W/scores" \
  -- -seed "$SEED" -race "$race_idx" -class "$class_idx" -turns "$turns" -keylog "$W/keys.log" -summary "$W/summary.json" \
  -menu-letters -exact-turns -msglog "$W/messages.log" -statelog "$W/state.log" >/dev/null 2>&1 || true
got=$(sha256sum "$W/keys.log" | cut -c1-64)
want=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['play_sha256'])" "$C/zoo-death.json")
if [ "$got" = "$want" ]; then echo "same game as the zoo (keys $got); logs in $W"
else echo "a different game from the zoo's (keys $got, zoo $want); compare $W/messages.log with $C/messages.log"; fi
