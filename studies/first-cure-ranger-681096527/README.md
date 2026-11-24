# First healing potion and Phase Door on Elf Ranger 681096527

The original Ranger died to a crow at turn 9,024, CL2, DL1. The [Cemetery dossier](../../deaths/D-c2a30d1b13526ec6b227c09e5b575626568d5b13e370f2952e162dc59a7cdc80/README.md) retains the natural death from Zoo run 45028029063 at borg-reborn-rs `9085c266`. The three builds below are separate birth replays of that same seed. They all use the borg-rs core.

[borg-reborn-rs #1007](https://github.com/diegoami/borg-reborn-rs/issues/1007) records the original #996 experiments. The early build reproduces the original key, state, and message streams with its first-cure setting at zero. On the later #996 build, the one-copy arm dies and the zero-copy arm survives. On the shipped Track P pin, the one- and two-copy arms both reach the cap. One start with an outcome that changes across builds gives no estimate of the policy's survival effect.

## Shopping

The first-cure row credits each healing potion equally until its count is filled, at 200% of the escape weight for each copy. It adds to the healing curve and healing reserve. The Phase Door reserve, remaining gold, and the rest of the basket still determine what the plan can buy.

On `ced0152d`, the zero-copy arm buys six Phase Doors and no healing potion at the turn-541 plan. The one-copy arm buys five Phase Doors and one CLW. The two-copy arm buys three Phase Doors and two CLW. The current Track P replay buys two CLW and two Phase Doors at the shipped Ranger setting of two, or one CLW and three Phase Doors at the one-copy setting. [Zoo #753](https://github.com/diegoami/borg-zoo/issues/753) follows up with a paired pilot on classes that ship zero.

## Reproduce

Use a clean checkout for each full commit in [runs.tsv](runs.tsv), GCC 14.2 x86-64 with right-to-left argument evaluation, and a 100,000-turn cap. The logs in the TSV are the local rerun hashes. The dossier retains the distinct original build and raw hashes.

```sh
BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
# Set COUNT to the value in runs.tsv.
# Use borg_param_town_first_cure on ced0152d and 5069a72a.
# Use borg_param_town_first_cure__ranger on c5501d3c.
BORG_TXT_SET="borg_respawn_race=2;borg_respawn_class=7;${SETTING}=${COUNT}" \
BORG_TOWN_PLAN_RECORD="${OUT}/plan.jsonl" \
flock /tmp/angband-validation.lock harness/run.sh "$OUT" 681096527 2 7 100000 menu,exact
```

Use an absolute `OUT` and the matching pinned Cemetery death tools for each source build. The historical builds use the global key because their shipped profiles lack a Ranger override. The runs use the shipped harness and class files apart from the stated keys, with respawn winners and cheat death disabled. The bulk logs are reproducible from these inputs. [first-shopping.tsv](first-shopping.tsv) retains the confirmed purchase messages that support the first-visit comparison.
