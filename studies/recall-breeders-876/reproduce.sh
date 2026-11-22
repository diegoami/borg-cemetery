#!/usr/bin/env bash
# Rebuild the priest game of borg-zoo run 44924461733 (seed 399497898) from
# birth, then the flight-Recall counterfactuals of borg-reborn-rs#876.
#
#   studies/recall-breeders-876/reproduce.sh BORG_REBORN_RS_CHECKOUT WORKDIR
#
# BORG_REBORN_RS_CHECKOUT: a borg-reborn-rs checkout (any branch); this script
# adds two detached worktrees of it at da097a76 under WORKDIR.
# Runs take the shared lock (borg-reborn-rs RULES 17).
set -euo pipefail
SRC="$(realpath "$1")"; WORK="$(realpath -m "$2")"
HERE="$(cd "$(dirname "$0")" && pwd)"
COMMIT=da097a764239c64cdcdd0fb469d5a05577a6823e
ARM="borg_param_caution_confused_clw_cure=1;borg_param_town_confusion_cure_reserve=1"   # reborn-confusion-csw
mkdir -p "$WORK"

run() {  # run TREE OUT [ENV...]
    local tree=$1 out=$2; shift 2
    rm -rf "$out"
    (cd "$tree" && env "$@" BORG_TXT_SET="$ARM" flock /tmp/angband-validation.lock \
        harness/run.sh "$out" 399497898 8 3 100000 exact,menu >"$out.out" 2>&1) || true  # exit 1 = death exporter
    printf '%-12s keys %s  %s\n' "$(basename "$out")" "$(sha256sum <"$out/keys.log" | cut -c1-16)" \
        "$(grep -o '"game_turns": [0-9]*\|"death_cause": "[^"]*"' "$out/summary.json" | tr '\n' ' ')"
}

# 1. The original build, unchanged: the zoo's game, key for key.
[ -d "$WORK/orig" ] || git -C "$SRC" worktree add --detach "$WORK/orig" "$COMMIT"
(cd "$WORK/orig" && BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh >"$WORK/orig-build.log" 2>&1)
run "$WORK/orig" "$WORK/base"
echo "zoo play hash  dde95ceb4cce4cb57309baa4c1aea2281d496c9f78b06b76a5c9c6169d17a4e9"

# 2. The same commit plus diagnostic.patch (stderr only; with no BORG_CF_*
#    variable set it plays the same game, which run 'dbg' checks).
[ -d "$WORK/cf" ] || { git -C "$SRC" worktree add --detach "$WORK/cf" "$COMMIT"; git -C "$WORK/cf" apply "$HERE/diagnostic.patch"; }
(cd "$WORK/cf" && BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh >"$WORK/cf-build.log" 2>&1)
run "$WORK/cf" "$WORK/dbg" BORG_CF_DEBUG=1
# 3. Counterfactuals: the #758 survival check forced to allow from a turn on.
for T in 46802 64022; do run "$WORK/cf" "$WORK/cf$T" BORG_CF_DEBUG=1 BORG_CF_ALLOW_FROM_TURN=$T; done
grep '^CFSUM' "$WORK/dbg/stderr.log" | sed 's/^CFSUM //' | diff - "$HERE/evidence/forecasts.txt" && echo "forecasts.txt reproduced"
