#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage from the borg-reborn-rs checkout: bash replay.sh NEW_TRIAL_DIRECTORY" >&2
    exit 2
fi

fixture="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath -m "$1")"
mkdir "$trial"
mkdir "$trial/saves"
export SAVE_ROOT="$trial/saves"
export RUN_TIMEOUT_SECONDS=45
export BORG_DEATH_RECORDS_DIR="$trial/deaths"

run_arm() {
    local name="$1" save="$2" floor="$3" expected_price="$4" market="${5:-0}"
    gzip -dc "$fixture/$save.save.gz" > "$SAVE_ROOT/$save.save"
    local settings="borg_param_town_restore_life_reserve=1;borg_param_town_restore_life_min_gold=$floor"
    if [ "$market" -ne 0 ]; then
        settings+=";borg_param_town_black_market_min_gold=$market;borg_param_town_black_market_level_delta=100"
    fi
    BORG_TXT_SET="$settings" BORG_TOWN_PLAN_RECORD="$trial/$name-plan.jsonl" \
        flock /tmp/angband-validation.lock harness/run.sh "$trial/$name" 1 4 1 10815543 \
        "menu,finalsave,keep-load-rng,save=$save.save"
    python3 - "$trial/$name" "$expected_price" <<'PY'
import json
import re
import sys
from pathlib import Path

run = Path(sys.argv[1])
price = int(sys.argv[2])
summary = json.loads((run / 'summary.json').read_text())
assert summary['stop_reason'] == 'turns' and not summary['dead'], summary
paid = [int(gold) for gold in re.findall(
    r'You bought a Potion of Restore Life Levels for (\d+) gold\.',
    (run / 'messages.log').read_text())]
expected = [price] if price else []
assert paid == expected, (run.name, paid, expected)
print(f'{run.name}: {paid or "no purchase"}')
PY
}

run_arm healthy-floor0 healthy-999 0 400
run_arm healthy-below-floor healthy-999 1000 0
run_arm healthy-at-floor healthy-1000 1000 400
run_arm drained-below-floor drained-999 1000 400
run_arm market-below-floor market-2999 1000 0 7500
run_arm market-at-floor market-3000 1000 1200 7500
