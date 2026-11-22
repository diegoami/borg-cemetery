# borg-zoo #576: caution_ranged_vs_immobile 2 against shipped 0 on main 3b4924ba

## Source
- **Run:** [44909591817](https://github.com/diegoami/borg-zoo/actions/runs/44909591817), `reborn-immobile2-head-big`, 1,080 games: classes-1800 starts 361–900, 100,000 turns, arms `shipped` and `immobile2`. Issue: https://github.com/diegoami/borg-zoo/issues/576.
- **Run page:** `runs/zoo-reborn-immobile2-head-big-44909591817/`.
- **Specimen:** `4.2.6-reborn-rust-main-3b4924ba`.
- **The shipped arm** plays all 540 games as #566's big run, so its 6 deaths are repeats of the dossiers in `runs/2026-11-21-reborn-head-3b4924ba/`.
- **Three games die identically in both arms**, so 13 distinct games and 16 deaths (6 shipped, 10 immobile2).

## Deaths
| dossier | character | killed by | game turn | arm | replay folder |
|---|---|---|---:|---|---|
| [D-0feb5c3a78](../../deaths/D-0feb5c3a78c230039dd87a27a4e590eb7ca6a11246f004cfe15d92856bc9a393/) | Dunadan Mage, CL1 DL1 | a grey mushroom patch | 5,702 | immobile2 only | `replay/1770630957-immobile2` |
| [D-af160e6783](../../deaths/D-af160e6783502f7850f87bcea2cd8b8d56f51f9eaf73a9b2e905ac4248541907/) | Dunadan Ranger, CL1 DL1 | a grey mushroom patch | 6,455 | immobile2 only | `replay/116037261-immobile2` |
| [D-59773017ac](../../deaths/D-59773017ac7f13283a77d18ceb0c2348e7245e75f71abdf0faa39cc81675ee39/) | Elf Ranger, CL2 DL1 | a giant yellow centipede | 6,761 | both arms, same game | `replay/1088421828-immobile2` |
| [D-0c44ce2ba7](../../deaths/D-0c44ce2ba7933d2820a6aea358c59a7ff552fe04d37241b6383853e6fafd6d41/) | Elf Ranger, CL2 DL1 | a giant yellow centipede | 6,761 | both arms, same game | `replay/1088421828-shipped` |
| [D-b460e0fd65](../../deaths/D-b460e0fd654c471e428ebdccc39c4031863e2fb63c2615151b283be795752fc4/) | Dunadan Necromancer, CL2 DL1 | a grey mold | 7,990 | immobile2 only | `replay/1203232169-immobile2` |
| [D-e0f5308d22](../../deaths/D-e0f5308d22195e11535f5edba8e53f64fed196a6d47c74a7e5bd30cc5468bfc3/) | Human Druid, CL1 DL1 | a grey mold | 9,072 | shipped only | `replay/1674396030-shipped` |
| [D-97ab9a69bb](../../deaths/D-97ab9a69bbc696de72b6bcc646bf462d15e4b333c5f8319997b637fae90b1a05/) | Dunadan Mage, CL1 DL1 | a grey mold | 9,503 | immobile2 only | `replay/13040847-immobile2` |
| [D-28d90c6632](../../deaths/D-28d90c6632a7fafd5235927124900cd0fd2e67b5c39c9f28e0944e9cf91b4873/) | Human Ranger, CL1 DL1 | a floating eye | 9,812 | immobile2 only | `replay/1241679603-immobile2` |
| [D-de77b76173](../../deaths/D-de77b76173b781430dcae5367d9cf3712c1480e5783ba09f5ded9636653d48e9/) | Human Blackguard, CL2 DL1 | a clear icky thing | 14,317 | both arms, same game | `replay/2078477958-immobile2` |
| [D-dd54140522](../../deaths/D-dd54140522facc200343c5d9b40c9577c28a79a36871305618b72d4f880a111c/) | Human Blackguard, CL2 DL1 | a clear icky thing | 14,317 | both arms, same game | `replay/2078477958-shipped` |
| [D-8035e6ae9e](../../deaths/D-8035e6ae9ee6728908fa11e5460380825c55b20784491db34fa5d18f0bfc9f87/) | Half-Troll Ranger, CL4 DL2 | a soldier | 26,147 | both arms, same game | `replay/829474344-immobile2` |
| [D-6a1dbd02d6](../../deaths/D-6a1dbd02d6ee9fc5c6466f55c1107dbf218d76df77b4a4b2d9627b827a8728f5/) | Half-Troll Ranger, CL4 DL2 | a soldier | 26,147 | both arms, same game | `replay/829474344-shipped` |
| [D-b533e3a055](../../deaths/D-b533e3a055e5e77a00f0b5be407408ba0064c8af0f884308d6341e6f3226fbdb/) | Dunadan Blackguard, CL4 DL3 | a wild dog | 54,311 | shipped only | `replay/2064233389-shipped` |
| [D-f162774b83](../../deaths/D-f162774b83e2d9bd807f0d3d9f7ec533017345c84efc3d02ebfe18066465ddd8/) | Dwarf Blackguard, CL6 DL1 | poison | 65,280 | immobile2 only | `replay/417396285-immobile2` |
| [D-429644f167](../../deaths/D-429644f167e3ce0857c6e8fe05b602f5c08310233527c1198f48bd1e838ba586/) | Half-Orc Priest, CL7 DL2 | a crow | 94,016 | shipped only | `replay/1626238247-shipped` |
| [D-cc5af38206](../../deaths/D-cc5af382063b133cda22fd72ca035723944f637241e3dba6be804d67a9204086/) | Half-Orc Priest, CL7 DL2 | a crow | 99,925 | immobile2 only | `replay/53289191-immobile2` |

## Observations
- **Result:** shipped 6 deaths, immobile2 10 (3 rescued, 7 newly killed, p 0.34), ΔCL −0.05 ±0.08: leaning worse.
- **5 of the 7 new deaths are to immobile monsters:**
  - **Mage 1770630957 and Ranger 116037261 (grey mushroom patch):** the confusion cure is held while adjacent, then a confused "Desperate for Stairs" walk.
  - **Necromancer 1203232169 and Mage 13040847 (grey mold):** a step away undone by the next flow back into reach.
  - **Ranger 1241679603:** an unseen floating eye.
- The fixes asked for are in borg-reborn-rs#837 and #838.

## Replay
`replay/<SEED>-<ARM>/` replays each death exactly without the zoo artifacts: `runs/replay-zoo-death.sh runs/2026-11-21-reborn-immobile2-head/replay/<SEED>-<ARM>`. See `replay/README.md`.
