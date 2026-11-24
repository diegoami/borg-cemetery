#!/usr/bin/env bash
set -eu
case_dir="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath "$1")"
mkdir -p "$trial/saves"
for gold in 165 2; do
    gzip -dc "$case_dir/warrior-$gold.save.gz" > "$trial/saves/warrior-$gold.save"
done
for pair in 165-1 165-0 2-1; do
    gold="${pair%-*}"
    flag="${pair##*-}"
    SAVE_ROOT="$trial/saves" RUN_TIMEOUT_SECONDS=30 BORG_TOWN_PLAN_RECORD="$trial/warrior-$pair-town.jsonl" \
        BORG_TXT_SET="borg_param_town_ranged_readiness=$flag" flock /tmp/angband-validation.lock \
        harness/run.sh "$trial/warrior-$pair" 1184 0 0 1511 menu,living-save,keep-load-rng,save="warrior-$gold.save"
done
