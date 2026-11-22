#!/usr/bin/env bash
# zoorun.sh OUT BORGTXT_DIR [extra borgh options...]  -- seed 829474344, Half-Troll Ranger, as borg-zoo started it
set -euo pipefail
OUT=$1; SRC=$2; shift 2
GAME=${GAME:?set GAME to the build/rust/game directory of borg-reborn-rs 7f8c6b80}
mkdir -p "$OUT"/{user,save,archive,panic,scores}
cp "$SRC/borg.txt" "$SRC/scary_monsters.txt" "$OUT/user/"
cd "$GAME"
env -i PATH=/usr/bin:/bin HOME=/root TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 BORG_RUN_DIR="$OUT" ${EXTRA_ENV:+"$EXTRA_ENV"} \
  ./angband -mborgh -n -uBorg -d"user=$OUT/user" -d"save=$OUT/save" -d"archive=$OUT/archive" -d"panic=$OUT/panic" -d"scores=$OUT/scores" \
  -- -seed 829474344 -race 7 -class 7 -turns ${TURNS:-100000} -keylog "$OUT/keys.log" -summary "$OUT/summary.json" -menu-letters -exact-turns \
  -statelog "$OUT/state.log" -msglog "$OUT/messages.log" "$@" > /dev/null 2> "$OUT/stderr.log"
