#!/usr/bin/env bash
set -euo pipefail

# Run from the pinned borg-reborn-rs source checkout after harness/build.sh.
fixture_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output="$(realpath -m -- "${1:?usage: reproduce.sh OUTPUT_DIRECTORY}")"
mkdir -p "$output"

export BORG_IMPL=rust BORG_CORE=borg-rs
export BORG_DEATH_RECORDS_DIR="$output/deaths"

run_case() {
    local name="$1" shopping="$2" recovery="$3" seed="$4" class="$5" turns="$6"
    local run_dir="$output/$name"
    BORG_TXT_SET="borg_param_town_ranged_readiness=$shopping;borg_param_trip_ranged_readiness=$recovery;borg_param_ranged_readiness_trace=1" \
        BORG_TOWN_DUMP="$run_dir/town.jsonl" BORG_TOWN_PLAN_RECORD="$run_dir/plan.jsonl" \
        BORG_TRIP_RECORD="$run_dir/trip.jsonl" \
        harness/run.sh "$run_dir" "$seed" 0 "$class" "$turns" menu
}

for name in bow lantern; do
    data_dir="$output/$name-data"
    mkdir -p "$data_dir"
    cp -a engine/angband/lib/. "$data_dir/"
    patch -s -p1 -d "$data_dir" < "$fixture_dir/$name.patch"
done

BORGH_DATA_ROOT="$output/bow-data" run_case bow-shopping 1 0 1184 5 3500
BORGH_DATA_ROOT="$output/lantern-data" run_case lantern-shopping 1 0 1184 5 3000
run_case ranger-both 1 1 1184 7 15000
run_case paladin-control 0 0 302 5 100000
run_case paladin-shopping 1 0 302 5 100000
run_case paladin-recovery 0 1 302 5 100000
run_case paladin-both 1 1 302 5 100000
