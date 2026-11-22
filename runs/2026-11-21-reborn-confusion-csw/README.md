# borg-reborn-rs da097a76, arm reborn-confusion-csw: every death of the confusion small and medium tiers

**Report with each death's last recorded screens:** https://claude.ai/artifact/9n6im9yJT9x2FxiiiTokCB

## Source
- **Specimen:** `4.2.6-reborn-rust-confusion-da097a76` (borg-reborn-rs #837 on main 12c4ce7c), 100,000 turns.
- **Arm:** `reborn-confusion-csw`: `town_confusion_cure_reserve = 1` and `caution_confused_clw_cure = 1`. Control `reborn-confusion-ctl` (shipped).
- **Runs (borg-zoo#581):** 44924461733 (classes-1800 small, starts 1-90), 44936494812 (medium, starts 91-360).
- **Run pages:** `runs/zoo-reborn-confusion-837-small-44924461733`, `runs/zoo-reborn-confusion-837-medium-44936494812`.

## Deaths
11 of 360 (ctl: 5). 0 rescued, 6 newly killed. Every replay's keys match the zoo cell's.

| dossier | character | killed by | game turn | group |
|---|---|---|---:|---|
| [D-3bc1a77cd1](../../deaths/D-3bc1a77cd1f2c0cfb8cd5f3f228c8905470100bfe8e66f6bfaa4e400eaf9d4e3/) | Human Druid, CL1 DL1 | a floating eye | 1,921 | shared with ctl: floating eye |
| [D-3c28ea4987](../../deaths/D-3c28ea4987b2edc3b3ef716c67a9c4b43c563e9d061fbe6d0ce4583e09fe59c1/) | Dwarf Ranger, CL1 DL1 | Fang, Farmer Maggot's Dog | 3,043 | shared with ctl: Fang |
| [D-c4f50f897e](../../deaths/D-c4f50f897e92c8ad7ef7c87cd768d4b8d7a406081bbef7ca2a91a692c1ca3dd6/) | Human Necromancer, CL1 DL1 | a floating eye | 4,249 | shared with ctl: floating eye |
| [D-2615dc1800](../../deaths/D-2615dc1800db7d83366259ab8551493e4d268e3258854b9ec46d2114158abe60/) | Half-Troll Necromancer, CL1 DL1 | a crow | 4,501 | shared with ctl: crow |
| [D-8f0cb831c8](../../deaths/D-8f0cb831c8840dac1d8fc458ff72c149f0b3a304c79e8c39c6c3845e96a8a0bd/) | Elf Necromancer, CL2 DL1 | a grey mushroom patch | 5,088 | new: reserve buys CCW, then mushroom loop |
| [D-fcd23089a1](../../deaths/D-fcd23089a1b427d432b0edb917fcbb78827e40fd633f059e8e062ccfcef1ce31/) | Gnome Necromancer, CL2 DL1 | a grey mushroom patch | 5,297 | new: CLW cure next to a mushroom patch |
| [D-1bc8e0be35](../../deaths/D-1bc8e0be352e0fac7d95958c971ab8057b65013190e649c8e4a2ce110062c28a/) | Elf Rogue, CL2 DL1 | Fang, Farmer Maggot's Dog | 13,373 | shared with ctl: Fang |
| [D-cdc3032329](../../deaths/D-cdc30323294f7b3cddacd602a43ab3a0c8961c9fb14243663659dff9aeccf744/) | Human Mage, CL3 DL1 | poison | 18,520 | new: reserve buys CSW (distant) |
| [D-3198901d80](../../deaths/D-3198901d804c468ebb30528347c5cbb23a540bc211868befed989b470e688737/) | Half-Orc Necromancer, CL4 DL1 | a soldier | 21,698 | new: reserve buys CCW (distant) |
| [D-6aa56ded5b](../../deaths/D-6aa56ded5bbfcec66ea95e2253a9fe088dc099e98b94dca0a4c6f4dcaa638f54/) | Kobold Paladin, CL5 DL2 | a crow | 59,093 | new: reserve buys CCW, healing ran out |
| [D-3b3bfb975c](../../deaths/D-3b3bfb975c2d4a54df938a40fb243446467febad7c205154d3648d81cadae96f/) | Dunadan Priest, CL6 DL1 | a white worm mass | 66,588 | new: CLW cure next to a mushroom patch (distant) |

## Observations
- The five shared deaths are the ctl game key for key; the arm never acted.
- Two newly killed games (459443830, 399497898) part from ctl at a CLW confusion cure next to a grey mushroom patch, which confuses again on its next turn; `clw_walk` plays them identically and dies too; `stuck` lives.
- Four (412975293, 2079962982, 1886935520, 461220874) part from ctl at the first Alchemist visit at CL1: the reserve buys a Cure Critical Wounds for 200 gold (three) or a Cure Serious Wounds for 70 (one), in place of CLW.
- Mage 461220874 casts Magic Missile without the mana and faints (turn 18,421), unrelated to the arm.

Observations only, not a diagnosis (RULES 14).
