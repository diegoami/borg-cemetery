#!/usr/bin/env bash
# Start one game exactly as borg-zoo's zoo/borgrs.py command() and run_cell()
# do (borg-zoo at a98b013): every BORG_* variable cleared, the cell's written
# user/borg.txt and scary list, the cell's arguments, exact turns, state and
# message logs. BORG_RUN_DIR is set so the core writes trace-core.jsonl (a
# trace never changes play). Prints the keys.log sha256 (the zoo's play_sha256).
#
#   run-cell.sh BUILD CONFIG SEED RACE CLASS OUT [extra borgh options]
#
# BUILD is the zoo build artifact's directory (game/angband, game/lib,
# scary_lists/scary_monsters.txt), or a borg-reborn-rs build laid out the same.
# CONFIG is the cell's configurations/<sha>.txt (its written user/borg.txt).
# With the injection patch (inject-frontend.patch) built in, BORGH_INJECT_AT
# and BORGH_INJECT are passed through; without them play is unchanged.
set -euo pipefail
B=$1 CFG=$2 SEED=$3 RACE=$4 CLS=$5 OUT=$6; shift 6
rm -rf "$OUT"; for d in user save archive panic scores; do mkdir -p "$OUT/$d"; done
cp "$CFG" "$OUT/user/borg.txt"; cp "$B/scary_lists/scary_monsters.txt" "$OUT/user/"
INJ=(); for v in BORGH_INJECT_AT BORGH_INJECT; do [ -n "${!v:-}" ] && INJ+=("$v=${!v}"); done
cd "$B/game"
env -i "${INJ[@]}" PATH=/usr/bin:/bin HOME="${HOME:-/tmp}" TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 BORG_RUN_DIR="$OUT" \
  ./angband -mborgh -n -uBorg -duser="$OUT/user" -dsave="$OUT/save" -darchive="$OUT/archive" -dpanic="$OUT/panic" -dscores="$OUT/scores" \
  -- -seed "$SEED" -race "$RACE" -class "$CLS" -turns 100000 -keylog "$OUT/keys.log" -summary "$OUT/summary.json" -menu-letters -exact-turns \
  -statelog "$OUT/state.log" -msglog "$OUT/messages.log" "$@" >/dev/null 2>"$OUT/stderr.log" || echo "exit $?" >&2
sha256sum "$OUT/keys.log" | cut -c1-64
