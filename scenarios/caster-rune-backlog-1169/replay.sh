#!/usr/bin/env bash
set -eu
case_dir="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath "$1")"
mkdir -p "$trial/saves"
for save in mage-book priest-control priest-scroll; do
    gzip -dc "$case_dir/$save.save.gz" > "$trial/saves/$save.save"
done
gzip -dc "$case_dir/../mage-overweight-cursed-kit-9221204/start.save.gz" > "$trial/saves/mage-original.save"
run() {
    local name="$1" seed="$2" race="$3" class="$4" cap="$5" flags="$6" cadence="${7:-0}"
    SAVE_ROOT="$trial/saves" CHECKPOINT_EVERY="$cadence" RUN_TIMEOUT_SECONDS=90 \
        BORG_TOWN_PLAN_RECORD="$trial/$name-town.jsonl" \
        flock /tmp/angband-validation.lock harness/run.sh "$trial/$name" "$seed" "$race" "$class" "$cap" "$flags"
}
run mage-original 1 4 1 9241204 menu,finalsave,keep-load-rng,save=mage-original.save
run mage-book-departure 1 4 1 9340440 menu,living-save,keep-load-rng,save=mage-book.save 9340423
run priest-control 399497898 8 3 605000 menu,living-save,keep-load-rng,save=priest-control.save
run priest-scroll 399497898 8 3 605000 menu,living-save,keep-load-rng,save=priest-scroll.save
