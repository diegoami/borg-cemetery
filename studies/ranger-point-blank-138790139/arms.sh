#!/usr/bin/env bash
# The arms of this study, exactly as run (2026-11-22). Usage:
#   arms.sh MAIN_CHECKOUT OLD_CHECKOUT OUTDIR
# MAIN_CHECKOUT: borg-reborn-rs at 47b9bbb6 (origin/main); OLD_CHECKOUT: at
# 7f8c6b80 (the zoo specimen). Both built with
#   BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
# BORG_CEMETERY_DIR: a borg-cemetery checkout at death-tools-pin.txt
# (4697893660942ed142744306c634583ec630f88a).
set -euo pipefail
MAIN=$1 OLD=$2 OUT=$3
run() { # checkout name env...
    local dir=$1 name=$2; shift 2
    (cd "$dir" && env "$@" flock /tmp/angband-validation.lock \
        harness/run.sh "$OUT/$name" 138790139 0 7 100000 menu,exact)
}
PB=BORG_PARAM_ATTACK_ARROW_POINT_BLANK_DIVISOR__RANGER
# main, shipped settings
run "$MAIN" armA X=1
run "$MAIN" armB $PB=1
run "$MAIN" armC $PB=1 BORG_PARAM_FAST_FRAGILE_BY_STATS=1
# the zoo's death game on its own build
FF="BORG_PARAM_FAST_FRAGILE_POLICY=1 BORG_PARAM_FAST_FRAGILE_BY_STATS=1 BORG_PARAM_FAST_FRAGILE_NO_HEAL=1"
run "$OLD" old-ctl X=1
run "$OLD" old-ctl-div1 $PB=1
run "$OLD" old-ban $FF
run "$OLD" old-ban-div1 $FF $PB=1
# tables: python3 fights.py OUT/<arm> ; python3 crow.py OUT/<arm>
