#!/usr/bin/env bash
# replay.sh BIN OUTDIR TURNS [extra args...]: exact replay of seed 390305857 with the bundle's user/ dir
set -euo pipefail
BIN=$1; O=$2; T=$3; shift 3
B=${WORK:?set WORK to a scratch dir}/yeek/b
rm -rf "$O"; mkdir -p "$O"/{user,save,archive,panic,scores}
cp "$B"/user/* "$O/user/"
cd "$(dirname "$BIN")"
env -u BORG_PROFILE -u BORG_CORE -u BORG_ERRAND -u BORG_PLAN TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  ./angband -mborgh -n -uPlayer -duser="$O/user" -dsave="$O/save" -darchive="$O/archive" -dpanic="$O/panic" -dscores="$O/scores" \
  -- -seed 390305857 -race 4 -class 6 -turns "$T" -keylog "$O/keys.log" -msglog "$O/messages.log" -statelog "$O/state.log" -summary "$O/summary.json" \
  -menu-letters -exact-turns "$@" > "$O/run.log" 2> "$O/stderr.log" || true
