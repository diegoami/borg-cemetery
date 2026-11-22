#!/bin/bash
# cf-batch.sh OUTDIR: the counterfactual matrix of README.md, on a build of
# 7f8c6b80 with cf-hook.patch applied (GAME_ROOT). Run under the shared lock:
#   GAME_ROOT=... flock /tmp/angband-validation.lock ./cf-batch.sh OUTDIR
HERE=$(cd "$(dirname "$0")" && pwd); OUT=$1
run(){ name=$1; shift; EXTRA_ENV="$*" $HERE/runcell.sh $OUT/$name stats-ban; echo "$name done"; }
for t in 64384 64394 64404 64414 64424 64434 64444 64454 64462 64472 64479; do run speed-$t BORG_CF=$t:speed; done
run clw-64462 BORG_CF=64462:clw
run unban-64462 BORG_CF_UNBAN=64462
run unban-64384 BORG_CF_UNBAN=64384
run phase-64454 BORG_CF=64454:phase
run phase-64444 BORG_CF=64444:phase
run phase-64414 BORG_CF=64414:phase
