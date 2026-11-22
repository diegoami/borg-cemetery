#!/usr/bin/env bash
# port-arm.sh NAME [VAR=VALUE ...]: play the zoo cell on GAME_DIR (7f8c6b80 + counterfactuals/switches-port-7f8c6b80.patch)
# with the given BORG_PARAM_* settings, into OUT_ROOT/port/NAME; prints the outcome and where it splits from the death.
S=${OUT_ROOT:?set OUT_ROOT}; mkdir -p "$S/port"; name=$1; shift
env "$@" $CASE_DIR/probe/probe-run.sh $S/port/$name > /dev/null
python3 -I - $S/port/$name $name "$CASE_DIR" <<'PY'
import json,sys,hashlib
d=sys.argv[1]; s=json.load(open(d+'/summary.json')); k=hashlib.sha256(open(d+'/keys.log','rb').read()).hexdigest()[:12]
m=[l for l in open(d+'/messages.log') if '(#908)' in l or '(#911)' in l or 'Healing (outmatched)' in l]
first=None
o=open(sys.argv[3]+'/replay/keys.log').read().split('\n'); n=open(d+'/keys.log').read().split('\n')
for i,(a,b) in enumerate(zip(o,n)):
    if a!=b: first=(i+1,b.split()[0]); break
print(f"{sys.argv[2]}: {s['stop_reason']} turn {s['game_turns']} {s.get('death_cause') or ''} CL{s['clevel']} keys {k} split_at_key {first} new_notes {len(m)}")
PY
