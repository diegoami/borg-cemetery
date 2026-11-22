# Retreat and stair flight undo one another

[Source issue #932](https://github.com/diegoami/borg-reborn-rs/issues/932) ·
[Original Ranger study](../../../studies/fastfrag-stats-ban-ranger-829474344/README.md)

## Live Mage

A Gnome Mage played on recording build `4b2c2fcf913e352ebd7bef5f16a531e8fc50d92a`.
The recorder's executable SHA-256 was
`3a298a35a53bd6e1ba43fe25295ea0c522501a03ae43f724826e02942eb7cf62`.
Between turns 285,860 and 288,710 on DL2, the repeating positions were
(28,21), (27,22), (26,21), (27,22), given as (x,y). From the
middle square, the danger estimate was usually 66 and the retreat
landings were rated 0. The stair flow repeatedly sent the Mage back to
the middle. The DL1 episode from 395,754 to 397,914 showed the same
conflict. The Mage later moved on.

[Coordinate extract](mage-positions.tsv) · [Decision extract](mage-decisions.tsv)

The original recording is `20261122-142315-1.JptJU1/native`. These are
excerpts of observed play. The new Track P code has constructed route
regressions based on this geometry.

## Ranger counterfactual at the original jelly encounter

Control is native Half-Troll Ranger seed 829474344, race/class indexes
7/7, stats-ban arm from [Zoo #596](https://github.com/diegoami/borg-zoo/issues/596),
[run 44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466).
The original Zoo binary and settings reproduced the preserved key log.
The historical overlays apply the route guard to `7f8c6b80a617eba3a6f2b83e4ba9d45b7b552b73`.
To isolate the historical incident, each overlay only enables the guard
from game turn 95,165. All four streams match the control through key
16,284. At turn 95,180 the control next sends `6`; the guarded runs send
`3`.

| Route rule | White jelly touches after turn 95,170 | Result |
| --- | ---: | --- |
| Archived control | 132 | Died of poison at 96,820 |
| [One grid](overlays/one-grid.patch.gz), 8 thinks | 132 | [Died of poison at 96,820](../../../deaths/D-9a6d5f6caf5501925a9dd2bb59df2997447a4fb1485629e63c4998f4bae38c52/report.md) |
| [Nearby recent grids](overlays/several-grids-nearby.patch.gz), 8 thinks | 92 | [Died of poison at 97,710](../../../deaths/D-15c6f65b1386049906ec6014755327ff81078a80cef8fe2d182300c3acde91d3/report.md) |
| [Recent grids on the level](overlays/timed-history.patch.gz), 32 thinks | 21 | Alive at 100,000, 96 HP, DL2 |
| [Recent grids on the level](overlays/timed-history-128.patch.gz), 128 thinks | 1 | Alive at 100,000, 96 HP, DL2 |

The 128-think run took a detour after the second retreat. The Ranger was
still on DL2 at the cap. These variants are continuations of one birth
and serve as regression evidence for the encounter.

### Replay recipe and receipts

Download the original build and death archives from run 44950087466.
Use the stats-ban cell for seed 829474344 in artifact
`deaths-4.2.6-reborn-rust-fast-fragile-7f8c6b80-1`. Copy its
`user/borg.txt` and `user/scary_monsters.txt` into the fresh output's
`user` directory. The [retained settings](../../../studies/fastfrag-white-jelly-829474344/borg-stats-ban.txt) and [scary list](ranger-scary-monsters.txt) are also retained here. For an overlay, apply the selected patch with
`gzip -dc PATCH | git apply` at the historical pin, build using
`BORG_IMPL=rust harness/build.sh` on x86-64 GCC, and append
`borg_param_caution_retreat_reentry_ticks = N` with the table's value.
The archived control uses the unmodified build and settings. Create the
five directories below before invoking the binary from its game directory.

```sh
TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 ./angband -mborgh -n -uBorg \
  -duser="$out/user" -dsave="$out/save" -darchive="$out/archive" \
  -dpanic="$out/panic" -dscores="$out/scores" -- -seed 829474344 \
  -race 7 -class 7 -turns 100000 -menu-letters -exact-turns \
  -keylog "$out/keys.log" -statelog "$out/state.log" \
  -msglog "$out/messages.log" -summary "$out/summary.json"
```

The 128-think build used GCC 15.2.0 and Rust 1.98.1. Its build-input
SHA-256 was `be053c59ac31dcfa11fefe8a051fdacb93a37bed677b9ac7df9a4a5128573b24`,
and its binary SHA-256 was
`ca94e50ea4a7788b79b84206dd661dd5c92cc8d66367d1a669aa61025e3de1de`.
The control key SHA-256 was
`798335ae2821113ed4fac2726bb3acfb34e1e12f0426aeb60e6391bfcbd639dc`;
the 128-think key SHA-256 was
`3e6f020127cae5753d1a9f959329341a7b5dc4bb09eabf43134b9488318ee22d`.
