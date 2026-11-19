# Human Paladin 766958386: poison after a yellow jelly fight, borg-reborn-rs main e5cc5469

- **Dossier:** [D-540138fafac2](../../deaths/D-540138fafac2da33673916d4559adb1faff009ba410ebbe753058b440b77d27b/README.md), the `ctl` arm with shipped settings.
- **The same game in other arms:** the same key stream also dies in the run's `recall-wait`, `errands` and `both` arms ([run page](../zoo-reborn-bundle-rest-e5cc-pilot-44599338458/README.md)). It also dies in both arms of borg-zoo's `reborn-throw-as-melee-pilot` (run 44599308992, PR #687 head 7c9b4cd1, `attack_throw_as_melee` 0 and 1). That makes six runs of **one life**, not six samples.
- **Source:** borg-reborn-rs main `e5cc5469` (calmed and the Phase Door rule shipped), borg-zoo `reborn-bundle-rest-e5cc-pilot`, run 44599338458, classes-18.
- **Outcome:** died of **poison** in town (DL0, max DL1) at game turn 5,100, CL3, with 8 gold.
- **Reproduction:** the zoo replayed it with full logs, and the key stream matched the cell's.
- **Lineage:** the same start reached the 100,000-turn cap on main 0d8b61d7 and 592c6984. The path to this death is new on e5cc5469.

## What happened (from messages.log)
1. **Turn 4,842, DL1, CL1, HP 17/17.** Leaving the up staircase, the Paladin stepped next to a **yellow jelly**: never moves, poison touch, drains mana, 44 HP.
   - It noted danger 1,224 and "Fleeing (excessive danger)", then "Leaving (failed to teleport)".
   - It was "Bored but unable to flow to up stairs" and "Considering Phase (twitchy)", but read no Phase Door.
   - Bravery was boosted to 30,000, and it chose `attack type 1` (melee) with utility 2003.
2. **Turns 4,842-4,965.** It fought in melee with a Main Gauche (1d5) for about 120 game turns, poisoned again and again.
   - It drank all 4 Cure Light Wounds ("Healing (outmatched)").
   - It killed the jelly at 13 HP and jumped from CL1 to CL3.
3. **Turns 4,972-5,100.** Poisoned at 10/39 HP, it took the up stairs, entered town, walked toward the Alchemy shop, and died of the poison on the way.

## Had and did not use
- **24 Flasks of oil** in the pack, never thrown. The game is byte-identical with `attack_throw_as_melee = 1` (borg-reborn-rs#568).
- **An unknown Icky Green Potion.**
- **Stepping away from the jelly.** It never moves. `caution_ranged_vs_immobile` (borg-reborn-rs#646) is 0 on e5cc5469.
- **Cure Light Wounds doesn't cure poison in 4.2.** Only Cure Critical Wounds does.

## Links
- borg-zoo report: [reports/reborn-throw-as-melee-pilot-deaths](https://github.com/diegoami/borg-zoo/blob/main/reports/reborn-throw-as-melee-pilot-deaths/README.md)
- borg-reborn-rs#710: cures and oil (question 4, the yellow jelly).
- Cemetery issue: #79.
