# Restore Life Levels checkout at the purse floor

These six native runs check [#1112](https://github.com/diegoami/borg-reborn-rs/pull/1112) with the shipped borg-rs core at `270177ba1822cde9027434b03aed826510b5cb4c`. The Gnome Mage has max CL45 and max DL45. The drained arm begins live play at CL44 and restores CL45. All arms are counterfactuals from one constructed start, using fresh Borg memory and the saved engine RNG.

| Shop | XP | Starting gold | Purchase floor | Engine checkout |
| --- | --- | ---: | ---: | --- |
| Alchemist | Full | 999 | 0 | Bought for 400 |
| Alchemist | Full | 999 | 1,000 | No purchase |
| Alchemist | Full | 1,000 | 1,000 | Bought for 400 |
| Alchemist | Drained | 999 | 1,000 | Bought for 400 and quaffed in town |
| Black Market | Full | 2,999 | 3,000 | No purchase |
| Black Market | Full | 3,000 | 3,000 | Bought for 1,200 |

The first two rows use identical save bytes. The Black Market pair uses a 7,500-gold base and a 100-gold deduction per character level to test a 3,000-gold threshold at CL45. At 3,000 gold the existing 60-percent spending cap above the 500-gold exclusion leaves 1,500, enough for the 1,200-gold potion. At 2,999 the ordinary solver receives a zero share. The threshold and the configured cap still apply after the first purchase.

[Receipts](receipts.json) record input hashes, effective overrides, decision and checkout evidence, build and stream hashes. The compressed messages and town plan files retain each run's records.

## Construction and replay

The parent is [the retained CL45 town start](../late-inventory-mage-10815143/late-mage-town-fit.save.gz). The fixture uses the pinned Angband engine to remove unequipped shots, mushrooms and devices for carry headroom, clear the Home and retail stock, and add one known potion at the named shop. The Mage keeps the same wearable equipment and remaining kit. [author.gdb](author.gdb) records the changes before Borg activation. It was run in a debug build from `c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894`, from its game directory, with the uncompressed parent save on a private path. Set `FIXTURE_SAVE_DIR` to an existing private output directory when regenerating. The market stock passed the native `black_market_ok` check.

From a clean borg-reborn-rs checkout at the pinned candidate, build with `BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh`. Then run this with the path to this case and a new trial directory whose parent exists.

```sh
bash "$fixture/replay.sh" "$trial"
```

The script verifies purchase confirmations from the live engine and stops each run at the fixed turn cap. The tests establish checkout behaviour for these two offers. Purchase rates, competing stock and class differences need a Zoo comparison across starts.
