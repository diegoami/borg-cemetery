# First healing potion and Phase Door on Elf Ranger 681096527

The original Ranger died to a crow at turn 9,024, CL2, DL1. The [Cemetery dossier](../../deaths/D-c2a30d1b13526ec6b227c09e5b575626568d5b13e370f2952e162dc59a7cdc80/README.md) retains the natural death from Zoo run 45028029063 at borg-reborn-rs `9085c266`. The three builds below are separate birth replays of that same seed. They all use the borg-rs core.

[borg-reborn-rs #1007](https://github.com/diegoami/borg-reborn-rs/issues/1007) records the original #996 experiments. The early build reproduces the original key, state, and message streams with its first-cure setting at zero. On the later #996 build, the one-copy arm dies and the zero-copy arm survives. On the shipped Track P pin, the one- and two-copy arms both reach the cap. One start with an outcome that changes across builds gives no estimate of the policy's survival effect.

## Shopping

The first-cure row credits each healing potion equally until its count is filled, at 200% of the escape weight for each copy. The same potion supplies the healing curve, healing reserve, and first-cure row. With a count of two, the second potion receives the same first-cure credit as the first. The Phase Door reserve, remaining gold, and the rest of the basket still determine what the plan can buy.

On `ced0152d`, the zero-copy arm buys six Phase Doors and no healing potion at the turn-541 plan. The one-copy arm buys five Phase Doors and one CLW. The two-copy arm buys three Phase Doors and two CLW. On current Track P, both purchases are in planner visit 2. The state log records an earlier descent at turn 441, no descent between the purchases, and the next descent at turn 801. The receipt turns below are the Borg's purchase notes, ten turns after the plans.

| Plan / receipt turn | One-copy arm | Shipped Ranger two-copy arm |
| --- | --- | --- |
| 541 / 551 | 97 gold, buys 3 Phase Doors | 97 gold, buys 2 CLW |
| 621 / 631 | 38 gold, buys 1 CLW | 43 gold, buys 2 Phase Doors |

Both arms carry one Recall scroll in these plan snapshots. At turn 661, the one-copy snapshot shows 1 CLW and 3 Phase Doors, and the two-copy snapshot shows 2 CLW and 2 Phase Doors. The net trade across the two purchase decisions is one extra CLW for one fewer Phase Door.

[Zoo #753](https://github.com/diegoami/borg-zoo/issues/753) compares global zero against one in classes that ship zero, with the Ranger fixed at two. Only three of 18 paired starts changed. In the resolved-kind purchase read, Druid seed 934061548 bought eight versus six Phase Doors. Mage seed 1548306106 bought twelve versus six Phase Doors and three versus zero Recall scrolls. These are whole-run purchase counts. The pilot gives no basis to raise the global setting or to change the Ranger setting.

## Reproduce

Use a clean checkout for each full commit in [runs.tsv](runs.tsv), GCC 14.2 x86-64 with right-to-left argument evaluation, and the matching pinned Cemetery death tools. Set `COUNT` to the requested count in the TSV and `OUT` to an absolute output path. The command selects the override by source checkout and checks the effective Ranger value from the completed run.

```sh
set -eu
case "$(git rev-parse HEAD)" in
  ced0152de0d94b002400a954aa727e24f2fed7c2|5069a72a4ab8eedf12cf2a42ee654a5156ecbaee)
    setting=borg_param_town_first_cure ;;
  c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894)
    setting=borg_param_town_first_cure__ranger ;;
  *) echo "Use a source commit from runs.tsv" >&2; exit 2 ;;
esac
BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
BORG_TXT_SET="borg_respawn_race=2;borg_respawn_class=7;${setting}=${COUNT}" \
BORG_TOWN_PLAN_RECORD="${OUT}/plan.jsonl" \
flock /tmp/angband-validation.lock harness/run.sh "$OUT" 681096527 2 7 100000 menu,exact
python3 - "$OUT/settings-resolved.json" "$COUNT" <<'PYCODE'
import json
import sys
with open(sys.argv[1]) as receipt:
    resolved = json.load(receipt)
effective = resolved["effective_settings"].get("town_first_cure", 0)
if resolved["class_name"] != "ranger" or effective != int(sys.argv[2]):
    raise SystemExit(f"Unexpected resolved arm: {resolved['class_name']} first cure {effective}")
PYCODE
```

The runs use the shipped harness and class files apart from the stated keys, with respawn winners and cheat death disabled. The dossier records the original build, and its key, state, and message hashes match the early zero-copy replay. The [shopping receipts](first-shopping.tsv) pair the relevant purchase notes with planner visit, turn, budget, and Recall stock. Purchases outside those selected decisions are omitted.
