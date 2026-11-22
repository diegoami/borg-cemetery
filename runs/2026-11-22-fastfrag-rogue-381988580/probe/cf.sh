#!/usr/bin/env bash
# cf.sh OUTROOT NAME INJECT_AT "KEYS": replay the exact game; when INJECT_AT keys have been logged,
# feed KEYS (space separated: a character, ESC, RET or 0xNN) instead of the Borg's, then the Borg plays on.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd); root=$1; name=$2; at=$3; keys=$4; mkdir -p "$root"
PROBE_INJECT_AT=$at PROBE_INJECT_KEYS="$keys" PROBE_FROM=62880 PROBE_MON=$root/$name-mon.txt \
  "$here/probe-run.sh" "$root/$name"
python3 -I - "$root/$name" "$name" <<'PY'
import json, sys
d = sys.argv[1]; s = json.load(open(d + '/summary.json'))
print(sys.argv[2], s['stop_reason'], 'turn', s['game_turns'], 'dead', s['dead'], s.get('death_cause'), 'CL', s['clevel'], 'DL', s['depth'], 'hp', s['hp'])
PY
