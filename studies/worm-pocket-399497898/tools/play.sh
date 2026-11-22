#!/bin/bash
# play.sh BIN OUTDIR [extra borgh args]  -- the zoo invocation of this cell
set -e
BIN=$1; OUT=$2; shift 2
source ${SCRATCH}/env.sh
rm -rf $OUT; mkdir -p $OUT; for d in user save archive panic scores; do mkdir -p $OUT/$d; done
cp $B/user/borg.txt $B/user/scary_monsters.txt $OUT/user/
cp $B/config.txt $OUT/; mkdir -p $OUT/checkpoints
G=$(dirname $BIN)
cd $G
env -i BORG_DIAG_PATH=$BORG_DIAG_PATH BORGH_MAPDUMP=$BORGH_MAPDUMP PATH=/usr/bin:/bin HOME=/tmp TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 BORG_RUN_DIR=$OUT $BIN -mborgh -n -uBorg -duser=$OUT/user -dsave=$OUT/save -darchive=$OUT/archive -dpanic=$OUT/panic -dscores=$OUT/scores -- -seed 399497898 -race 8 -class 3 -turns 100000 -keylog $OUT/keys.log -summary $OUT/summary.json -menu-letters -exact-turns -statelog $OUT/state.log -msglog $OUT/messages.log "$@" 2>$OUT/stderr.log >/dev/null || true
