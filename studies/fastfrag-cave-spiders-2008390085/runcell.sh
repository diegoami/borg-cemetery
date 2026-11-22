#!/bin/bash
# runcell.sh OUT ARM: play seed 2008390085 (High-Elf Rogue) from birth exactly as
# the zoo cell did (zoo/borgrs.py command(): -menu-letters -exact-turns, 100,000
# turns, TZ=UTC, ambient settings cleared), with the arm's borg.txt
# (borg-ARM.txt here: stats-ban sha256 58b6d86c..., ctl fbf2663e...) and the
# build's harness/scary_monsters.txt (sha256 9766d882...).
#   GAME_ROOT   borg-reborn-rs checkout at 7f8c6b80, built with
#               BORG_IMPL=rust harness/build.sh (default ../borg-reborn-rs)
#   EXTRA_ENV   e.g. "BORG_CF=64414:speed" for the counterfactual build
#   TURNS       stop turn (default 100000, the zoo's cap)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
W=${GAME_ROOT:-$HERE/../../../borg-reborn-rs}
OUT=$(mkdir -p "$1" && cd "$1" && pwd); ARM=$2; TURNS=${TURNS:-100000}
rm -rf "$OUT"/*; for d in user save archive panic scores; do mkdir -p $OUT/$d; done
cp $HERE/borg-$ARM.txt $OUT/user/borg.txt
cp $W/harness/scary_monsters.txt $OUT/user/scary_monsters.txt
cd $W/build/rust/game
env -i PATH=$PATH HOME=$HOME TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 $EXTRA_ENV ./angband -mborgh -n -uBorg \
  -duser=$OUT/user -dsave=$OUT/save -darchive=$OUT/archive -dpanic=$OUT/panic -dscores=$OUT/scores \
  -- -seed 2008390085 -race 9 -class 6 -turns $TURNS -keylog $OUT/keys.log -summary $OUT/summary.json \
  -menu-letters -exact-turns -statelog $OUT/state.log -msglog $OUT/messages.log 2>$OUT/stderr.log
