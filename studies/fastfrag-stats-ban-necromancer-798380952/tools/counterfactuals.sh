#!/usr/bin/env bash
# Run every case of cases.txt (who name inject_at inject) with a build that has
# inject-frontend.patch: the exact game is played from birth by the same Borg
# up to key inject_at, the injected keys (or the melee policy) take the next
# decisions, then the same Borg (memory intact) plays on to the 100,000 cap.
#   counterfactuals.sh BUILD NEC_CONFIG RGR_CONFIG OUTDIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
B=$1 NEC=$2 RGR=$3 OUT=$4
mkdir -p "$OUT"
while read -r who name at what; do
  if [ "$who" = nec ]; then CFG=$NEC; A="798380952 1 4"; else CFG=$RGR; A="829474344 7 7"; fi
  (BORGH_INJECT_AT=$at BORGH_INJECT="$what" "$HERE/run-cell.sh" "$B" "$CFG" $A "$OUT/$name" > "$OUT/$name.hash") &
  while [ "$(jobs -r | wc -l)" -ge "${JOBS:-4}" ]; do sleep 1; done
done < "$HERE/cases.txt"
wait
