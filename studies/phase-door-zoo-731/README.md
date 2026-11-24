# Phase Door refusals in Zoo #731

This case study follows [borg-reborn-rs #1073](https://github.com/diegoami/borg-reborn-rs/issues/1073)
and the [four-arm Zoo run](https://github.com/diegoami/borg-zoo/actions/runs/45125828988).
The [original Cemetery study](../lvl1-deaths-trackp-206cf4e7/README.md)
covers the earlier fatal Priest and Blackguard starts. The two starts
below were selected from the newly killed starts in the later Zoo run.

## Tested cases

| Start | Both on | Both off | Unknown only | Newcomer only |
| --- | --- | --- | --- | --- |
| [Kobold Priest 30279795](../../deaths/D-ef9134d01a5b1175a66478c33cc0239369dc554a2c1a17cd09b040dff7bb0d54/README.md) | Centipede death at 12,722 | Survived | Survived | Survived |
| [Gnome Mage 1247074959](../../deaths/D-cf06da4b6187c33fb44f7a3c3ba7ded1b2f7cc45725a61bafddc76e5ec5e42bb/README.md) | Fang death at 4,412 | Survived | See Zoo cell | See Zoo cell |

All six local runs reproduced the corresponding Zoo key-stream SHA-256.
The local binary differs from Zoo's binary. These are repeated plays of
two starts. For the population comparison see [Zoo's full-tier read](https://github.com/diegoami/borg-zoo/issues/731#issuecomment-7096054302).

## Decisions

**Kobold Priest.** At turn 12,683, the shipped rule deferred Phase Door at
17/17 HP. The race against the adjacent target estimated 3.42 damage per
turn and the ranged threat another 6. After one action, the Priest faced
the next emergency at 13/17 HP. With newcomer wait alone, it read Phase
Door at 12,693 and survived. With both switches enabled the emergency
check counted 82 unseen cells against a tolerance of 75. Other sites
also refused. The Priest died at 12,722. Unknown-only took a different
action at the first split and eventually passed a sample of exactly
75 at turn 12,713.

**Gnome Mage.** At turn 4,382 and 8/8 HP, the control accepted the
after-teleport check and read a scroll. The shipped arm refused the same
site after counting 92 unseen samples against a tolerance of 50.
The later checks refused too. Fang killed the Mage at 4,412. The
published unknown-only cell has the shipped play hash and the published
newcomer-only cell has the control hash.

The two cases can test whether narrowing the treatment of unseen
landings preserves a needed emergency escape. They do not establish a
survival effect across starts.

## Replay

Use borg-reborn-rs `6cd5c8bf82459dc60328d1eb426eb9614385a19c`,
GCC with right-to-left call argument evaluation, the shipped borg-rs core
and normal world. Use `harness/run.sh OUT SEED RACE CLASS 100000 menu,exact`.
Set the two parameters in `BORG_TXT_SET` as recorded in
[replays.tsv](replays.tsv). Shipped is `1/1`, both off is `0/0`,
unknown only is `1/0`, newcomer only is `0/1`. The replay table
uses the local written configuration and the key hash shared with Zoo.
