#!/usr/bin/env bash
set -eu
case_dir="$(cd "$(dirname "$0")"/.. && pwd)"
trial="$(realpath "$1")"
"$case_dir/replay.sh" "$trial"
for flag in 0 1; do
    name="warrior-depth20-$flag"
    BORG_TXT_SET="borg_town_target_depth=20;borg_param_town_ranged_readiness=$flag"         SAVE_ROOT="$trial/saves" BORG_TOWN_PLAN_RECORD="$trial/$name-town.jsonl" RUN_TIMEOUT_SECONDS=30         flock /tmp/angband-validation.lock harness/run.sh "$trial/$name" 1184 0 0 1511         menu,living-save,keep-load-rng,save=warrior-165.save
done
