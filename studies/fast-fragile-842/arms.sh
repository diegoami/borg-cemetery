#!/usr/bin/env bash
# usage: arms.sh OUTDIR ARMNAME "borg_param_x = 1;borg_param_y = 1" seeds...
# Replays the 3b4924ba crow cases on the worktree build with extra borg.txt lines.
set -euo pipefail
OUT=$1; ARM=$2; LINES=$3; shift 3
SRC=${SRC:-$HOME/borg-reborn-rs}
CEM=${CEM:-$(cd "$(dirname "$0")/../.." && pwd)}
R=$CEM/runs/2026-11-21-reborn-head-3b4924ba/replay
for s in "$@"; do
  D=$OUT/$ARM/cases/$s
  rm -rf "$D"; mkdir -p "$D"; cp -r "$R/$s"/. "$D"/
  if [ -n "$LINES" ]; then
    printf '\n' >> "$D/user/borg.txt"
    echo "$LINES" | tr ';' '\n' | sed 's/^ *//' >> "$D/user/borg.txt"
  fi
  flock /tmp/angband-validation.lock "$CEM/runs/replay-zoo-death.sh" "$D" "$OUT/$ARM/run-$s" "$SRC" >/dev/null 2>&1 || true
done
