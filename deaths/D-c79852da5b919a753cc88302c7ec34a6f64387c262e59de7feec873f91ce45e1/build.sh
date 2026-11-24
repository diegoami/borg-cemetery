#!/usr/bin/env bash
set -euo pipefail
case_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root="${BORG_CEMETERY_HOME:-$case_dir}"
while [ ! -f "$root/scripts/case_replay.py" ]; do
  parent="$(dirname -- "$root")"
  if [ "$parent" = "$root" ]; then
    echo 'Use a full borg-cemetery main checkout, or set BORG_CEMETERY_HOME to one.' >&2
    exit 2
  fi
  root="$parent"
done
exec python3 "$root/scripts/case_replay.py" build --case "$case_dir" "$@"
