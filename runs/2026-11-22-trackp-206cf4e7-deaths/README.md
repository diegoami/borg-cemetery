# The deaths and the stall of trackp 206cf4e7

Source: borg-zoo#695 (baseline of borg-reborn-rs trackp `206cf4e7`, shipped settings, classes-1800 full slice, 900 starts, 100,000 turns), run [45070528012](https://github.com/diegoami/borg-zoo/actions/runs/45070528012), attempt 2. All 20 deaths were replayed from birth (keys match the zoo cell's); the dossiers are listed in [zoo-reborn-trackp-206cf4e7-full-45070528012](../zoo-reborn-trackp-206cf4e7-full-45070528012/README.md).

Report with each death's last recorded screens: https://claude.ai/artifact/RSq87BTmLYmrupAj9pPTYm
Play pack: `~/borg-play/trackp206-full` (`./play.sh`).

## Observations

- 20 deaths, against 28 on 9085c266 (run 45028029063) on the same starts; 9 starts died on both. The grey mushroom patch kills once (11 on 9085c266).
- 10 of the 20 died carrying Cure Light or Cure Serious Wounds; 8 of those 10 drank none in their last 150 log lines. The Dwarf Mage ([D-17849d47f294](../../deaths/D-17849d47f294ed7867d2b87baaeeadd4952be4af357cdf0729dba341d27bce07/README.md)) held 10 CLW and 5 CSW, cast Magic Missile at 11 HP (failed twice) and bled out after a Phase Door at 0 HP.
- The patch death ([D-aaf3e284f5b9](../../deaths/D-aaf3e284f5b9c76a5c02e8b6379cbb96bf4a47b01b3862353c43de5cf21b7e26/README.md), Human Druid) is two rules cancelling: #969 declines the attack at 5/12 HP because a cure or an escape is at hand, and #867 declines the cure because it is "attacking first". It held 8 CLW and 6 Phase Door.
- The Kobold Mage ([D-159daa885baf](../../deaths/D-159daa885bafa3c658596c777eb7f96104e0c21f430379a82fd10be717213e3c/README.md)) fainted casting the emergency Magic Missile beyond its mana, and a crow killed it while it was paralysed. #980's `attack_reserve_spell_overexert` is in this build but ships as 1, the old behaviour.
- In 7 of the 20 the Borg refused Word of Recall on the modelled exposure (#758) at 0 to 5 HP in its final 150 log lines.

## The stall (no dossier)

Human Warrior, seed 1352670668, `wall_timeout`. A local replay at the same commit reproduces it. At game turn 56227 on DL2, after an invisible poisoner's unseen bump to the north, `borg_twitchy` picks the bumped grid, the #781 guard `unseen_bump_blocked` refuses it and no key is sent. With no key, game time does not move, so the 200-turn bump never expires. The zoo's stall record (turn 38541) is the first 64 KB flush of `keys.log`, not where the game stopped.
