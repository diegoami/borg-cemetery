#!/usr/bin/env bash
# cf.sh NAME "SPEC"  -- one counterfactual of seed 829474344 on the scratch build
set -euo pipefail
W=${CF_WORK:?set CF_WORK to a scratch directory holding the cell bundle in $CF_WORK/d and the factual replay in $CF_WORK/replay}
export GAME=${GAME:?set GAME to build/rust/game of the borg-reborn-rs 7f8c6b80 checkout with cf-hook.patch applied}
rm -rf "$W/cf/$1"; mkdir -p "$W/cf"
EXTRA_ENV="BORG_CF=$2" flock /tmp/angband-validation.lock "$(dirname "$0")/zoorun.sh" "$W/cf/$1" "$W/d/user"
python3 -I - "$W/cf/$1" "$W/replay" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]+'/summary.json'))
a=open(sys.argv[1]+'/keys.log').read().split('\n'); b=open(sys.argv[2]+'/keys.log').read().split('\n')
div=next((i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y), None)
print(f"{sys.argv[1].split('/')[-1]}: first differing key {div}; end turn {d['game_turns']} dead={d['dead']} cause={d.get('death_cause')} CL{d['clevel']} DL{d['depth']} maxDL{d['max_depth']} keys {d['keys']}")
PY
