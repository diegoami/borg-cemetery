#!/usr/bin/env bash
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath "$1")"
"$here/../replay.sh" "$trial"
for pair in oil:mage-oil-distance9 oil-no-launcher:mage-oil-no-launcher; do
    label="${pair%:*}"
    save="${pair#*:}"
    gzip -dc "$here/$save.save.gz" > "$trial/saves/$save.save"
    for flag in 0 1; do
        BORG_TXT_SET="borg_param_attack_throw_surplus=$flag;borg_param_attack_throw_as_melee=0"             SAVE_ROOT="$trial/saves" RUN_TIMEOUT_SECONDS=30 flock /tmp/angband-validation.lock             harness/run.sh "$trial/$label-$flag" 1 4 1 9221225 menu,exact,living-save,keep-load-rng,save="$save.save"
    done
done
