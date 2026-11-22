#!/bin/bash
# usage: replay.sh WORKTREE OUT SEED RACE CLASS [extra borg.txt lines...]
set -e
WT=$1; OUT=$2; SEED=$3; R=$4; C=$5; shift 5
rm -rf "$OUT"; mkdir -p "$OUT"/{user,save,archive,panic,scores}
python3 - "$WT/harness/borg.txt" "$OUT/user/borg.txt" "$R" "$C" "$@" <<'PY'
import sys,re
src,dst,r,c=sys.argv[1:5]; extra=sys.argv[5:]
ov={'borg_respawn_race':r,'borg_respawn_class':c,'borg_cheat_death':'FALSE','borg_respawn_winners':'FALSE','borg_reborn_core':'borg-rs','borg_reborn_errand':'none'}
for e in extra:
    k,v=[s.strip() for s in e.split('=',1)]; ov[k]=v
out=[];seen=set()
for line in open(src):
    m=re.match(r'\s*([A-Za-z0-9_]+)\s*=',line)
    if m and m.group(1) in ov:
        out.append(f"{m.group(1)} = {ov[m.group(1)]}\n"); seen.add(m.group(1))
    else: out.append(line)
for k,v in ov.items():
    if k not in seen: out.append(f"{k} = {v}\n")
open(dst,'w').writelines(out)
PY
cp "$WT/harness/scary_monsters.txt" "$OUT/user/"
cd "$WT/build/rust/game"
env -u BORG_PROFILE -u BORG_CORE -u BORG_ERRAND -u BORG_PLAN TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  ./angband -mborgh -n -uBorg -duser=$OUT/user -dsave=$OUT/save -darchive=$OUT/archive -dpanic=$OUT/panic -dscores=$OUT/scores \
  -- -seed $SEED -race $R -class $C -turns 100000 -keylog $OUT/keys.log -summary $OUT/summary.json -menu-letters \
  -exact-turns -statelog $OUT/state.log -msglog $OUT/messages.log > $OUT/stdout.log 2>&1 || true
sha256sum $OUT/keys.log | cut -c1-16
