# Zoo #138 small tier: plan-town deaths with the #423 survival fixes

These are the 18 natural deaths of the `reborn-m13-plan-town` arm in borg-zoo's
[`reborn-survival-small`](https://github.com/diegoami/borg-zoo/actions/runs/43874782892)
(borg-zoo#138, run 43874782892): the live town planner plus `errands_plan.txt`, trip policy
off, on the first 90 starts of `classes-1800`. They are compared, start by start, with the
same arm before the fixes:
[the zoo #123 small tier](../2026-11-16-zoo-reborn-plan-m13-small/README.md), whose 23
plan-town deaths are D0031–D0068 here.

## Provenance

- **Source:** borg-reborn-rs `4ecb93d77c625e03d2b838837da597d07bfbabe2`, the merge of #423:
  flee healing (#369) and Phase Door stock (#380). Source-hash rust `2317021cfad2c97c…`.
  Zoo specimen `4.2.6-reborn-rust-plans-m13-survival`.
- **Before:** borg-reborn-rs `8a0b57c8` (source-hash `9a4ea375…`). The fixes change play in
  every arm, so the two runs are different games on the same starts.
- **Unchanged inputs:** the plan `errands_plan.txt` (`922372ba…`) and `harness/borg.txt`
  (`88296dd1…`).
- **Replay:** all 18 deaths were replayed locally through the zoo adapter, with keys identical
  to the CI run (CI binary `a785eeb6…`; local build of the same source `f5891f15…`). Raw logs
  are not committed; their SHA-256s are in each `record.json`.

## Before and after, same 90 starts

| | after: lives | after: dies |
| --- | ---: | ---: |
| **before: lives** | 62 | **5** |
| **before: dies** | **10** | 13 |

- **Deaths:** 23 before, 18 after. **Caster deaths** (Mage, Druid, Priest,
  Necromancer): 18 before, 12 after.
- **Identical play:** 25 of the 90 starts play the same keys in both games.
- **Rescued by the fixes (10):** 3 Necromancer, 2 Mage, 2 Priest, 1 Ranger, 1 Warrior, 1 Druid.
- **Newly killed (5):** 1 Priest, 1 Druid, 1 Warrior, 1 Ranger, 1 Paladin.
- **Died in both games (13):** 5 Druid, 2 Necromancer, 2 Rogue, 2 Mage, 1 Ranger, 1 Priest.

The #123 investigation found the plan's excess deaths among casters who die under-levelled
in town-endpoint phases. That is where the fixes should act. Flee healing lets a fleeing character drink a cure it
previously skipped, and Phase Door stock keeps Mages buying Phase Door scrolls. The caster
excess falls, but it doesn't disappear.

## Rescued by the fixes

| Seed | Character | before the fixes (`8a0b57c8`) | with the fixes (`4ecb93d7`) |
| --- | --- | --- | --- |
| 300461652 | Hobbit Mage | [D0032](../../deaths/D0032-rust-seed300461652/README.md) poison, t52940, CL3 DL1 | alive at cap, CL4, max DL1 |
| 572215387 | Elf Ranger | [D0064](../../deaths/D0064-rust-seed572215387/README.md) a fatal wound, t11310, CL2 DL1 | alive at cap, CL5, max DL2 |
| 740860644 | Dunadan Warrior | [D0034](../../deaths/D0034-rust-seed740860644/README.md) a giant yellow centipede, t63205, CL4 DL1 | alive at cap, CL5, max DL2 |
| 904568879 | Dunadan Necromancer | [D0035](../../deaths/D0035-rust-seed904568879/README.md) a cave spider, t6744, CL1 DL1 | alive at cap, CL5, max DL2 |
| 1217781050 | Human Priest | [D0036](../../deaths/D0036-rust-seed1217781050/README.md) a cave spider, t10661, CL1 DL1 | alive at cap, CL5, max DL2 |
| 1236782037 | Gnome Necromancer | [D0037](../../deaths/D0037-rust-seed1236782037/README.md) poison, t51620, CL4 DL1 | alive at cap, CL5, max DL2 |
| 1303043906 | Dwarf Priest | [D0039](../../deaths/D0039-rust-seed1303043906/README.md) burning to a cinder in lava, t62170, CL4 DL0 | alive at cap, CL6, max DL2 |
| 1417651640 | Half-Orc Necromancer | [D0040](../../deaths/D0040-rust-seed1417651640/README.md) a black naga, t35791, CL2 DL1 | alive at cap, CL5, max DL2 |
| 1429594888 | Dunadan Mage | [D0041](../../deaths/D0041-rust-seed1429594888/README.md) a brown mold, t32513, CL3 DL7 | alive at cap, CL3, max DL2 |
| 1705599023 | Dwarf Druid | [D0044](../../deaths/D0044-rust-seed1705599023/README.md) a soldier, t90541, CL6 DL2 | alive at cap, CL7, max DL2 |

## Newly killed with the fixes

| Seed | Character | before the fixes (`8a0b57c8`) | with the fixes (`4ecb93d7`) |
| --- | --- | --- | --- |
| 652511567 | Gnome Priest | alive at cap, CL3, max DL2 | [D0075](../../deaths/D0075-rust-seed652511567/README.md) a radiation eye, t8460, CL2 DL1 |
| 1169386844 | Half-Orc Druid | alive at cap, CL6, max DL2 | [D0077](../../deaths/D0077-rust-seed1169386844/README.md) a soldier, t65689, CL4 DL1 |
| 1356248624 | Elf Warrior | alive at cap, CL5, max DL2 | [D0079](../../deaths/D0079-rust-seed1356248624/README.md) a fruit bat, t43418, CL4 DL1 |
| 1834235471 | Dunadan Ranger | alive at cap, CL4, max DL7 | [D0082](../../deaths/D0082-rust-seed1834235471/README.md) a soldier, t68805, CL6 DL7 |
| 1956591784 | Half-Troll Paladin | alive at cap, CL5, max DL2 | [D0083](../../deaths/D0083-rust-seed1956591784/README.md) poison, t98990, CL8 DL18 |

## Died in both games

| Seed | Character | before the fixes (`8a0b57c8`) | with the fixes (`4ecb93d7`) |
| --- | --- | --- | --- |
| 10488336 | Dwarf Necromancer | [D0056](../../deaths/D0056-rust-seed10488336/README.md) Grip, Farmer Maggot's Dog, t2651, CL1 DL1 | [D0069](../../deaths/D0069-rust-seed10488336/README.md) Grip, Farmer Maggot's Dog, t2721, CL1 DL1 |
| 102088710 | Elf Rogue | [D0058](../../deaths/D0058-rust-seed102088710/README.md) a grey mushroom patch, t52908, CL3 DL1 | [D0070](../../deaths/D0070-rust-seed102088710/README.md) a grey mushroom patch, t52908, CL3 DL1 |
| 129607500 | Human Ranger | [D0060](../../deaths/D0060-rust-seed129607500/README.md) a snaga, t95128, CL5 DL7 | [D0071](../../deaths/D0071-rust-seed129607500/README.md) Fang, Farmer Maggot's Dog, t16943, CL2 DL1 |
| 176707408 | Human Necromancer | [D0031](../../deaths/D0031-rust-seed176707408/README.md) a snaga, t90174, CL5 DL1 | [D0072](../../deaths/D0072-rust-seed176707408/README.md) a giant white mouse, t12940, CL2 DL1 |
| 247597266 | Half-Elf Mage | [D0062](../../deaths/D0062-rust-seed247597266/README.md) a small kobold, t8695, CL2 DL1 | [D0073](../../deaths/D0073-rust-seed247597266/README.md) a fruit bat, t40862, CL3 DL1 |
| 507571350 | Half-Elf Druid | [D0033](../../deaths/D0033-rust-seed507571350/README.md) a blue yeek, t7088, CL1 DL1 | [D0074](../../deaths/D0074-rust-seed507571350/README.md) a blue yeek, t8718, CL2 DL1 |
| 1086352478 | Half-Troll Priest | [D0066](../../deaths/D0066-rust-seed1086352478/README.md) a giant white louse, t3466, CL2 DL1 | [D0076](../../deaths/D0076-rust-seed1086352478/README.md) a giant white louse, t3581, CL2 DL1 |
| 1269315224 | Half-Orc Rogue | [D0038](../../deaths/D0038-rust-seed1269315224/README.md) a grey mushroom patch, t6069, CL2 DL1 | [D0078](../../deaths/D0078-rust-seed1269315224/README.md) a grey mushroom patch, t6069, CL2 DL1 |
| 1678303796 | Dunadan Druid | [D0042](../../deaths/D0042-rust-seed1678303796/README.md) a soldier, t63809, CL4 DL1 | [D0080](../../deaths/D0080-rust-seed1678303796/README.md) a soldier, t63809, CL4 DL1 |
| 1678765969 | Elf Druid | [D0043](../../deaths/D0043-rust-seed1678765969/README.md) a kobold shaman, t13847, CL2 DL1 | [D0081](../../deaths/D0081-rust-seed1678765969/README.md) a kobold shaman, t13847, CL2 DL1 |
| 2002578196 | Hobbit Druid | [D0045](../../deaths/D0045-rust-seed2002578196/README.md) a grey mold, t20472, CL2 DL1 | [D0084](../../deaths/D0084-rust-seed2002578196/README.md) a wild dog, t22189, CL2 DL1 |
| 2097768768 | Human Mage | [D0068](../../deaths/D0068-rust-seed2097768768/README.md) a cutpurse, t11891, CL1 DL1 | [D0085](../../deaths/D0085-rust-seed2097768768/README.md) a cutpurse, t11891, CL1 DL1 |
| 2109297965 | Human Druid | [D0046](../../deaths/D0046-rust-seed2109297965/README.md) poison, t36880, CL4 DL1 | [D0086](../../deaths/D0086-rust-seed2109297965/README.md) poison, t36880, CL4 DL1 |

## Limits

- **Sample size:** 10 starts per class; descriptive only.
- **Divergent lives:** a rescued or newly killed start is a different life after the first
  changed decision, not the same fight with a different result.
- **Unassessed:** the dossiers are basic native exports with the core decision-trace tail.
