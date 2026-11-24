#!/usr/bin/env bash
set -euo pipefail
fixture="$(cd "$(dirname "$0")" && pwd)"
trial="$(realpath -m "${1:?Give a new trial directory}")"
mkdir "$trial"
export SAVE_ROOT="$trial/saves" RUN_TIMEOUT_SECONDS=60 BORG_DEATH_RECORDS_DIR="$trial/deaths"
mkdir "$SAVE_ROOT"

run_pair() {
    local name="$1" input="$2" cap="$3"
    gzip -dc "$fixture/$input.save.gz" > "$SAVE_ROOT/$input.save"
    for reserve in 0 40; do
        local arm="$name-reserve$reserve"
        BORG_TOWN_PLAN_RECORD="$trial/$arm-plan.jsonl" \
          BORG_TXT_SET="borg_param_town_quiver_trim_reserve=$reserve" \
          flock /tmp/angband-validation.lock harness/run.sh "$trial/$arm" 1 4 1 "$cap" \
            "menu,finalsave,keep-load-rng,save=$input.save"
    done
}
run_pair 300 mage-quiver-300-town 10818143
run_pair 40 mage-quiver-40-town 10818143
run_pair fit late-mage-town-fit 10816143
cmp "$trial/40-reserve0/keys.log" "$trial/40-reserve40/keys.log"
cmp "$trial/fit-reserve0/keys.log" "$trial/fit-reserve40/keys.log"
python3 - "$trial" <<'PY'
import re
import sys
from pathlib import Path

trial = Path(sys.argv[1])
logs = [(trial / f'300-reserve{reserve}' / 'messages.log').read_text() for reserve in (0, 40)]
drops = re.findall(r'You drop (\d+) Rounded Pebbles .*\{borg ignore\}', logs[1])
assert drops == ['40', '40', '40', '40', '10'], drops
for log, weight, slots in zip(logs, (-1312, -632), (3, 7)):
    first = re.search(r'Town departure room: weight (-?\d+) free .* slots (\d+) free', log)
    assert first and first.groups() == (str(weight), str(slots)), first
PY
