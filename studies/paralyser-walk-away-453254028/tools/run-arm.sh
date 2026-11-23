#!/usr/bin/env bash
# One arm of this study: seed 453254028 (Half-Elf Necromancer, menu letters
# race 1 class 4) from birth, 100,000 turns, exact turns, on borg-reborn-rs
# d8b55d64 with tools/1125-on-d8b55d64.patch applied (a scratch tree, never
# committed there). Usage, from that tree after BORG_IMPL=rust harness/build.sh:
#   run-arm.sh OUTDIR "borg_param_NAME=VALUE;..."   ("" for the off arm)
set -euo pipefail
OUT=$1; SET=${2:-}
BORG_DEATH_RECORDS_DIR="$OUT.deaths" BORG_TXT_SET="$SET" \
  flock /tmp/angband-validation.lock harness/run.sh "$OUT" 453254028 1 4 100000 menu,exact
