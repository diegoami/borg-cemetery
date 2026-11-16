# Zoo #123 small tier: why the errands plan adds deaths with the town planner

These are natural deaths from borg-zoo's
[`reborn-plan-m13-small`](https://github.com/diegoami/borg-zoo/actions/runs/43868362767)
(borg-zoo#123, run 43868362767), in two of its arms:
- `reborn-m13-town`: the live town planner, no plan;
- `reborn-m13-plan-town`: the same plus `errands_plan.txt`.

Both arms have the trip policy off. The starts are 1–90 of `classes-1800`, 10 per class,
at 100,000 engine turns with `-exact-turns`.

Plan-town died 23 times against town's 15. This page pairs the two arms start by start and
explains the 16 starts that die only with the plan.

## Provenance

- **Source:** borg-reborn-rs `8a0b57c85700abd48981c2f41a65a0a637f7dc48` (#415), source-hash
  rust `9a4ea3756fb1b566…`, zoo specimen `4.2.6-reborn-rust-plans-m13-fix90`.
- **Plan:** `errands_plan.txt`, sha256 `922372ba849489c5…`. A copy is kept with each plan dossier.
- **Settings:** `borg_reborn_core = borg-rs`, `borg_reborn_errand = none`, `borg_town_plan = 1`,
  `borg_trip_policy = 0`. The rest is the specimen's `harness/borg.txt` (`88296dd1…`). Each
  dossier's `config.txt` records the written `borg.txt` hash and the zoo identity.
- **Replay:** each death was replayed locally through the zoo adapter (`zoo/borgrs.py`,
  `run_cell` with evidence kept).
  - All 62 replayed games (31 starts × 2 arms) produced keys identical to the CI run.
  - CI used binary `116b8316…`; the local build of the same source is `7e80a559…`.
  - The raw `keys.log`, `messages.log` and `state.log` are not committed. Their SHA-256s are in
    each `record.json`; replaying the cell through the zoo at this specimen regenerates them.
- **Independence:** these are 38 natural deaths, 23 plan-town and 15 town. Each is an independent
  life; the two arms are separate encounter families, because their `borg.txt` differs.

## Pairing

| | plan-town lives | plan-town dies |
| --- | ---: | ---: |
| **town lives** | 59 | **16** |
| **town dies** | 8 | 7 |

## The 16 starts that die only with the plan

| Seed | Character | town (no plan) | plan-town |
| --- | --- | --- | --- |
| 176707408 | Human Necromancer | alive at cap, CL6, max DL2 | [D0031](../../deaths/D0031-rust-seed176707408/README.md) a snaga, t90174, CL5 DL1 |
| 300461652 | Hobbit Mage | alive at cap, CL4, max DL2 | [D0032](../../deaths/D0032-rust-seed300461652/README.md) poison, t52940, CL3 DL1 |
| 507571350 | Half-Elf Druid | alive at cap, CL10, max DL3 | [D0033](../../deaths/D0033-rust-seed507571350/README.md) a blue yeek, t7088, CL1 DL1 |
| 740860644 | Dunadan Warrior | alive at cap, CL9, max DL5 | [D0034](../../deaths/D0034-rust-seed740860644/README.md) a giant yellow centipede, t63205, CL4 DL1 |
| 904568879 | Dunadan Necromancer | alive at cap, CL5, max DL1 | [D0035](../../deaths/D0035-rust-seed904568879/README.md) a cave spider, t6744, CL1 DL1 |
| 1217781050 | Human Priest | alive at cap, CL5, max DL2 | [D0036](../../deaths/D0036-rust-seed1217781050/README.md) a cave spider, t10661, CL1 DL1 |
| 1236782037 | Gnome Necromancer | alive at cap, CL5, max DL1 | [D0037](../../deaths/D0037-rust-seed1236782037/README.md) poison, t51620, CL4 DL1 |
| 1269315224 | Half-Orc Rogue | alive at cap, CL4, max DL2 | [D0038](../../deaths/D0038-rust-seed1269315224/README.md) a grey mushroom patch, t6069, CL2 DL1 |
| 1303043906 | Dwarf Priest | alive at cap, CL4, max DL2 | [D0039](../../deaths/D0039-rust-seed1303043906/README.md) burning to a cinder in lava, t62170, CL4 DL0 |
| 1417651640 | Half-Orc Necromancer | alive at cap, CL3, max DL1 | [D0040](../../deaths/D0040-rust-seed1417651640/README.md) a black naga, t35791, CL2 DL1 |
| 1429594888 | Dunadan Mage | alive at cap, CL4, max DL2 | [D0041](../../deaths/D0041-rust-seed1429594888/README.md) a brown mold, t32513, CL3 DL7 |
| 1678303796 | Dunadan Druid | alive at cap, CL7, max DL3 | [D0042](../../deaths/D0042-rust-seed1678303796/README.md) a soldier, t63809, CL4 DL1 |
| 1678765969 | Elf Druid | alive at cap, CL6, max DL3 | [D0043](../../deaths/D0043-rust-seed1678765969/README.md) a kobold shaman, t13847, CL2 DL1 |
| 1705599023 | Dwarf Druid | alive at cap, CL6, max DL3 | [D0044](../../deaths/D0044-rust-seed1705599023/README.md) a soldier, t90541, CL6 DL2 |
| 2002578196 | Hobbit Druid | alive at cap, CL5, max DL2 | [D0045](../../deaths/D0045-rust-seed2002578196/README.md) a grey mold, t20472, CL2 DL1 |
| 2109297965 | Human Druid | alive at cap, CL7, max DL2 | [D0046](../../deaths/D0046-rust-seed2109297965/README.md) poison, t36880, CL4 DL1 |

What the replays show:

1. **Casters carry the excess.** Of the 16, 6 are Druids, 4 Necromancers, 2 Mages and 2 Priests;
   1 is a Warrior and 1 a Rogue. Of the 8 starts the plan rescues, 5 are Rangers, 2 Blackguards
   and 1 a Priest. The plan's caster sections start slower. They hold `loop-levels 0 1` at CL1–3
   and `loop-levels 0 2` from CL4.
2. **They die less experienced than their no-plan twins.** In 14 of the 16, the plan-town
   character died at a lower character level than the town twin reached. In the other 2 the
   levels were equal. Examples:
   - CL1 against CL10 (Druid 507571350);
   - CL4 against CL9 (Warrior 740860644);
   - CL1 against CL5 (Necromancer 904568879, Priest 1217781050).
3. **Every phase they were in starts at the town.** At death, 9 were in a `loop-levels 0 1` phase
   and 7 in `loop-levels 0 2`.
   - Their runs repeat "Errand: loop town overrides the loop" and "restart after town", up to
     60 and 77 times in one game.
   - In 12 of the 16, the plan-town character spent a larger share of game time in town than its
     twin, for example 0.43 against 0.22, 0.61 against 0.40 and 0.48 against 0.24.
   - The loop spends time bouncing through town that the no-plan Borg spends gaining experience.
4. **They die shallow.** 13 died on DL1 and 1 on DL2. 1 died in town (Priest, lava, while
   fleeing) and 1 on DL7 (Mage 1429594888, a brown mold). The plan didn't push them too deep;
   they were still weak on the levels it allowed.
5. **The final fights:**
   - 9 of the 16 were in melee: a Necromancer with a Main Gauche against a snaga or a black naga,
     and Druids with a whip or shovel against soldiers and a kobold shaman.
   - 3 died to stationary spore monsters (grey mushroom patch, brown mold, grey mold) while
     attacking them or standing next to them.
   - 3 died to poison and 1 to lava.
   - Seen beside points 2 and 3, these look like ordinary low-level deaths of characters that
     are under-levelled for the visit, not a new failure mode.

## The other paired deaths

The 8 starts the plan rescues (town dies, plan-town lives), then the 7 where both die.

| Seed | Character | town (no plan) | plan-town |
| --- | --- | --- | --- |
| 60792140 | Half-Troll Ranger | [D0047](../../deaths/D0047-rust-seed60792140/README.md) a blue worm mass, t60462, CL8 DL2 | alive at cap, CL6, max DL2 |
| 167240942 | Gnome Ranger | [D0048](../../deaths/D0048-rust-seed167240942/README.md) a giant yellow centipede, t13088, CL2 DL1 | alive at cap, CL5, max DL2 |
| 255960706 | Dunadan Blackguard | [D0049](../../deaths/D0049-rust-seed255960706/README.md) burning to a cinder in lava, t84053, CL5 DL0 | alive at cap, CL6, max DL2 |
| 807773433 | Dwarf Ranger | [D0050](../../deaths/D0050-rust-seed807773433/README.md) a soldier, t96699, CL5 DL2 | alive at cap, CL5, max DL3 |
| 1248006956 | Hobbit Ranger | [D0051](../../deaths/D0051-rust-seed1248006956/README.md) a baby black dragon, t60678, CL4 DL6 | alive at cap, CL5, max DL2 |
| 1478804878 | Elf Priest | [D0052](../../deaths/D0052-rust-seed1478804878/README.md) a grey mushroom patch, t31855, CL1 DL1 | alive at cap, CL3, max DL2 |
| 1751715076 | Human Blackguard | [D0053](../../deaths/D0053-rust-seed1751715076/README.md) a blue worm mass, t87590, CL6 DL4 | alive at cap, CL5, max DL2 |
| 1758620521 | Half-Elf Ranger | [D0054](../../deaths/D0054-rust-seed1758620521/README.md) a wild cat, t83169, CL5 DL1 | alive at cap, CL5, max DL2 |
| 10488336 | Dwarf Necromancer | [D0055](../../deaths/D0055-rust-seed10488336/README.md) Fang, Farmer Maggot's Dog, t4960, CL1 DL1 | [D0056](../../deaths/D0056-rust-seed10488336/README.md) Grip, Farmer Maggot's Dog, t2651, CL1 DL1 |
| 102088710 | Elf Rogue | [D0057](../../deaths/D0057-rust-seed102088710/README.md) Fang, Farmer Maggot's Dog, t11969, CL2 DL1 | [D0058](../../deaths/D0058-rust-seed102088710/README.md) a grey mushroom patch, t52908, CL3 DL1 |
| 129607500 | Human Ranger | [D0059](../../deaths/D0059-rust-seed129607500/README.md) Fang, Farmer Maggot's Dog, t10219, CL2 DL1 | [D0060](../../deaths/D0060-rust-seed129607500/README.md) a snaga, t95128, CL5 DL7 |
| 247597266 | Half-Elf Mage | [D0061](../../deaths/D0061-rust-seed247597266/README.md) a wild cat, t17884, CL2 DL1 | [D0062](../../deaths/D0062-rust-seed247597266/README.md) a small kobold, t8695, CL2 DL1 |
| 572215387 | Elf Ranger | [D0063](../../deaths/D0063-rust-seed572215387/README.md) a wild cat, t25020, CL4 DL1 | [D0064](../../deaths/D0064-rust-seed572215387/README.md) a fatal wound, t11310, CL2 DL1 |
| 1086352478 | Half-Troll Priest | [D0065](../../deaths/D0065-rust-seed1086352478/README.md) a grey mushroom patch, t29643, CL3 DL1 | [D0066](../../deaths/D0066-rust-seed1086352478/README.md) a giant white louse, t3466, CL2 DL1 |
| 2097768768 | Human Mage | [D0067](../../deaths/D0067-rust-seed2097768768/README.md) a crow, t16786, CL3 DL1 | [D0068](../../deaths/D0068-rust-seed2097768768/README.md) a cutpurse, t11891, CL1 DL1 |

## Limits

- **Sample size:** 10 starts per class. The class pattern, casters harmed and Rangers helped,
  is a lead for the plan's class sections, not a measurement. The zoo's medium tier (40 per
  class) will test it.
- **Trajectories diverge early:** the paired lives split from the first plan decision, so a
  single death's immediate cause is partly chance. The evidence is the consistent direction
  across 16 starts: a lower level at death and more time in town.
- **No new defect:** no frozen-turn stall, key outlier or Home loop appears in these 38 deaths.
  The ambitious-plan stair livelock (borg-reborn-rs#421) is in a different arm.
- **Unassessed:** the dossiers are basic native exports with the core decision-trace tail.
