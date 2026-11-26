# Vanilla Borg full-game benchmark deaths (zoo #805, 2026-11-25)

**Source:** zoo run [45711540187](https://github.com/diegoami/borg-zoo/actions/runs/45711540187) (`reborn-fullgame-vanilla-evidence`, zoo issue [805](https://github.com/diegoami/borg-zoo/issues/805)) — the parallel full-game benchmark the owner asked for: the **original C Borg as Angband 4.2.6 ships it** (`4.2.6-reborn-c-pristine`, borg-reborn-rs `fab71554`, Borg sources e473720, vanilla upstream engine), one fresh assigned birth per class, 1,000,000-turn cap, shipped settings, no profiles.

**Selection:** all 7 deaths of the run (the 2 survivors — Blackguard CL20/DL14 and Rogue CL17/DL10 — are alive at the cap and have no dossier).

| dossier (deaths.json) | character | killer | CL | DL | turn |
|---|---|---|---:|---:|---:|
| D-151e8bcd… | Human Warrior | a priest | 10 | 14 (15 max) | 86,481 |
| Human Mage | a kobold | 1 | 1 | 9,802 |
| Human Druid | a rock lizard | 1 | 1 | 8,149 |
| Human Priest | burning to a cinder in lava | 8 | 0 (town) | 357,982 |
| Human Necromancer | a kobold shaman | 3 | 1 | 63,582 |
| Human Paladin | a kobold shaman | 2 | 1 | 26,788 |
| Human Ranger | a crow | 2 | 1 | 13,833 |

**Observations.** This is the classic vanilla C-Borg shape: it dives fast and dies young. Five of the seven deaths land inside the first 64,000 turns, four of those to shallow melee (a crow, a rock lizard, a kobold, two kobold shamans) at CL1–3; the mage and druid die to their **first melee exchange of the game** (turns 9,802 and 8,149). Only the Blackguard (CL20, DL14, alive at cap) and the Rogue (CL17, DL10, alive at cap) got going — they went deeper than anything the zoo's Borg (borg-reborn-rs track-p `242a4724`) reached on the same starts, while the zoo Borg lost exactly 1 of 9 (a druid death at turn 851,040, recorded separately in the zoo run). Safety is the Rust line's margin; depth is the vanilla's.

**Replay:** the zoo evidence-retained re-run keeps each game's key stream; the death report (viewer + play pack) lives beside the zoo issue — `~/borg-play/vanilla-fullgame/` on the zoo machine, and the report is linked from zoo #805.

Context: zoo [805](https://github.com/diegoami/borg-zoo/issues/805) · zoo [792](https://github.com/diegoami/borg-zoo/issues/792) (the R4.5 receiving benchmark that shares this program).

**Death report:** published beside the zoo play pack — `~/borg-play/vanilla-fullgame/report.html` on the zoo machine (viewer: each death's last 100 screens, the gear at death, attack counts; `play.sh` replays the exact game from birth to any turn, or drops you at one of four staged saves before the death). All seven replays verified: keys hash to the zoo cells' play_sha256.

**R4.5 receiving reconciliation (zoo #792 sign-off, 2026-11-26):** the 45-start × 3-arm parity exit slice's natural deaths are reconciled as dossiers `D-002808c1…` (Human Warrior, a crow, CL4/DL2, turn ~86k... seed 212818316-era family: full-0-warrior-2) and `D-007d0f7f…` (Human Necromancer, a crow, CL1/DL1, full-4-necro-3) — the only two natural deaths in the 135 parity games (native arm; check and switch replayed the same deaths identically, verified by the parity gate). Exported from the staged evidence with `scripts/native/export-death.py` and the reconstructed native BUILD_ID.
