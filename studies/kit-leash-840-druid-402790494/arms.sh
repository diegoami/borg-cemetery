#!/usr/bin/env bash
# Replays the Kobold Druid start of borg-zoo run 44950087466 (seed 402790494,
# race 10, class 2, 100,000 game turns, exact boundary) for the kit-leash study.
# usage: arms.sh OUTDIR SRC_MAIN [SRC_SPECIMEN]
#   SRC_MAIN      a borg-reborn-rs worktree at 47b9bbb6, built with
#                 BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
#   SRC_SPECIMEN  optional worktree at 7f8c6b80 (the zoo specimen), built the same way
# BORG_CEMETERY_DIR must name a borg-cemetery checkout at the source's
# death-tools-pin.txt (46978936...) for the death export of the specimen arms.
set -euo pipefail
OUT=$1; MAIN=$2; SPEC=${3:-}
mkdir -p "$OUT"
play() { # name src env...
  local n=$1 src=$2; shift 2
  (cd "$src" && env "$@" flock /tmp/angband-validation.lock \
     harness/run.sh "$OUT/$n" 402790494 10 2 100000 menu,exact >"$OUT/$n.out" 2>&1) || echo "$n: run.sh failed"
}
play A "$MAIN" ARM=control
play B "$MAIN" BORG_PARAM_KIT_LEASH=1
play C "$MAIN" BORG_PARAM_KIT_LEASH=1 BORG_PARAM_KIT_LEASH_MIN=2
play D "$MAIN" BORG_PARAM_KIT_LEASH=1 BORG_PARAM_KIT_LEASH_POWER=2
play E "$MAIN" BORG_PARAM_KIT_LEASH=1 BORG_PARAM_KIT_MONEY_FIRST=1
play F "$MAIN" BORG_PARAM_KIT_LEASH=1 BORG_PARAM_KIT_LEASH_MIN=2 BORG_PARAM_KIT_MONEY_FIRST=1 BORG_PARAM_TOWN_HUNT=1
# Fast-fragile settings on main (both play A's game key for key):
play S0 "$MAIN" BORG_PARAM_FAST_FRAGILE_POLICY=0 BORG_PARAM_FAST_FRAGILE_NO_HEAL=0
play S1 "$MAIN" BORG_PARAM_FAST_FRAGILE_BY_STATS=1
if [ -n "$SPEC" ]; then
  play Z0 "$SPEC" ARM=control
  play Z1 "$SPEC" BORG_PARAM_FAST_FRAGILE_POLICY=1 BORG_PARAM_FAST_FRAGILE_BY_STATS=1 BORG_PARAM_FAST_FRAGILE_NO_HEAL=1
fi
for d in "$OUT"/*/; do
  [ -f "$d/summary.json" ] || continue
  printf '%s %s %s\n' "$(basename "$d")" "$(sha256sum <"$d/keys.log" | cut -c1-64)" \
    "$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d["stop_reason"],d["game_turns"],d["clevel"],d["max_depth"],d["death_cause"])' "$d/summary.json")"
done
