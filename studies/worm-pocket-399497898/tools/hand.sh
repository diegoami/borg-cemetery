#!/bin/bash
# hand.sh K KEYFILE OUT : Borg plays the recorded game to key K, then KEYFILE is played
S=${SCRATCH}
source $S/env.sh
K=$1; KF=$2; OUT=$3
rm -rf $OUT; mkdir -p $OUT; for d in user save archive panic scores; do mkdir -p $OUT/$d; done
cp $B/user/borg.txt $B/user/scary_monsters.txt $OUT/user/
G=$S/diag/build/rust/game; cd $G
env -i BORGH_HANDOVER=$K BORGH_HANDOVER_KEYS=$KF BORGH_MAPDUMP=$OUT/map.txt PATH=/usr/bin:/bin HOME=/tmp TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 BORG_RUN_DIR=$OUT $G/angband -mborgh -n -uBorg -duser=$OUT/user -dsave=$OUT/save -darchive=$OUT/archive -dpanic=$OUT/panic -dscores=$OUT/scores -- -seed 399497898 -race 8 -class 3 -turns 100000 -keylog $OUT/keys.log -summary $OUT/summary.json -menu-letters -exact-turns -statelog $OUT/state.log -msglog $OUT/messages.log 2>$OUT/stderr.log >/dev/null || true
