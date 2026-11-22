#!/usr/bin/env bash
# probe-run.sh OUT [extra borgh args]: play seed 381988580 (Dunadan Rogue) as the zoo cell did,
# with the probe build. PROBE_* variables (see probe.patch) pass through.
#   GAME_DIR  the probe build's game directory (build/rust/game of 7f8c6b80 + probe.patch)
#   CASE_DIR  this case directory (for replay/user/borg.txt and scary_monsters.txt)
set -euo pipefail
: "${GAME_DIR:?set GAME_DIR}"; CASE_DIR=${CASE_DIR:-$(cd "$(dirname "$0")/.." && pwd)}
out=$1; shift
rm -rf "$out"; for d in user save archive panic scores; do mkdir -p "$out/$d"; done
cp "$CASE_DIR/replay/user/borg.txt" "$CASE_DIR/replay/user/scary_monsters.txt" "$out/user/"
cd "$GAME_DIR"
env -u BORG_RUN_DIR TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 ./angband -mborgh -n -uBorg -duser=$out/user -dsave=$out/save \
  -darchive=$out/archive -dpanic=$out/panic -dscores=$out/scores -- \
  -seed 381988580 -race 8 -class 6 -turns 100000 -keylog $out/keys.log -summary $out/summary.json -menu-letters -exact-turns \
  -statelog $out/state.log -msglog $out/messages.log "$@" > /dev/null 2> $out/stderr.log || echo "rc=$?"
