#!/usr/bin/env bash
set -eu
case_dir="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath "$1")"
mkdir -p "$trial/saves"
for variant in mage-dagger mage-unknown mage-upgrade mage-spell mage-device mage-launcher priest-dagger priest-melee priest-outside priest-spear; do
    gzip -dc "$case_dir/$variant.save.gz" > "$trial/saves/$variant.save"
    seed=1 race=4 class=1 cap=9221350
    if [[ "$variant" == priest-* ]]; then seed=399497898 race=8 class=3 cap=600150; fi
    for flag in 0 1; do
        if [[ "$variant" != *-dagger && "$flag" == 0 ]]; then continue; fi
        receipt="$trial/verified-$variant-$flag"
        SAVE_ROOT="$trial/saves" BORG_OBJECT_LOG="$receipt.objects.log" RUN_TIMEOUT_SECONDS=30 \
            BORG_TXT_SET="borg_param_attack_throw_surplus=$flag" flock /tmp/angband-validation.lock \
            harness/run.sh "$receipt" "$seed" "$race" "$class" "$cap" menu,living-save,keep-load-rng,save="$variant.save"
    done
done
for variant in mage-dagger priest-dagger priest-spear; do
    seed=1 race=4 class=1 cap=9221205
    if [[ "$variant" == priest-* ]]; then seed=399497898 race=8 class=3 cap=600017; fi
    SAVE_ROOT="$trial/saves" RUN_TIMEOUT_SECONDS=30 \
        BORG_TXT_SET=borg_param_attack_throw_surplus=1 flock /tmp/angband-validation.lock \
        harness/run.sh "$trial/immediate-$variant" "$seed" "$race" "$class" "$cap" menu,exact,living-save,keep-load-rng,save="$variant.save"
done
