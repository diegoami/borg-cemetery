#!/bin/bash
# replay.sh WORKTREE OUT [extra borg.txt lines...]
# WORKTREE: a borg-reborn-rs checkout built with BORG_IMPL=rust harness/build.sh.
# Writes the town plan records too (BORG_TOWN_PLAN_RECORD, BORG_TOWN_DUMP); they do not change play.
set -e
WT=$1; OUT=$2; shift 2
rm -rf $OUT; mkdir -p $OUT/user $OUT/save $OUT/archive $OUT/panic $OUT/scores
grep -v -E '^(borg_respawn_race|borg_respawn_class|borg_cheat_death|borg_respawn_winners|borg_reborn_core|borg_reborn_errand)\b' $WT/harness/borg.txt > $OUT/user/borg.txt
cat >> $OUT/user/borg.txt <<X
borg_respawn_race = 7
borg_respawn_class = 8
borg_cheat_death = FALSE
borg_respawn_winners = FALSE
borg_reborn_core = borg-rs
borg_reborn_errand = none
X
for l in "$@"; do k=${l%% *}; sed -i "/^$k *=/d" $OUT/user/borg.txt; echo "$l" >> $OUT/user/borg.txt; done
cp $WT/harness/scary_monsters.txt $OUT/user/
cd $WT/build/rust/game
env -u BORG_PROFILE -u BORG_CORE -u BORG_ERRAND -u BORG_PLAN TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  BORG_TOWN_PLAN_RECORD=$OUT/plan.jsonl BORG_TOWN_DUMP=$OUT/dump.txt \
  ./angband -mborgh -n -uBorg -duser=$OUT/user -dsave=$OUT/save -darchive=$OUT/archive -dpanic=$OUT/panic -dscores=$OUT/scores \
  -- -seed 312081895 -race 7 -class 8 -turns ${TURNS:-100000} -keylog $OUT/keys.log -summary $OUT/summary.json -menu-letters \
  -exact-turns -statelog $OUT/state.log -msglog $OUT/messages.log > $OUT/stdout.txt 2>&1 || true
sha256sum $OUT/keys.log | cut -c1-16
