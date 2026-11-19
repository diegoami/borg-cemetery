# Human Druid 102023799: death in a giant white mouse colony after judging it unstoppable (borg-reborn-rs #556, `caution_breeder_stoppable` arm)

**Dossier:** [`deaths/D-da2d8ad044d97f1fd5de584c56d2cfae7d7f03f6616ed8013d723c7333d4a3ab`](../../deaths/D-da2d8ad044d97f1fd5de584c56d2cfae7d7f03f6616ed8013d723c7333d4a3ab/)

## Provenance
- **Source:** diegoami/borg-reborn-rs `cfd011a6b2ff41385c0b6445b26f55132d0a53dd`, branch `task/T556-breeder-avoid` (PR #632, open). That is main `3ba17e2c` plus #556's redesign: "kill breeders first; flee only what cannot be stopped". Clean build (`git_dirty=no`), source hash `1f41b613…`, binary `94e912c0…`, engine upstream `42cd156ac`.
- **Run:** `BORG_CORE=borg-rs BORG_TXT_SET="borg_param_caution_breeder_stoppable=1" harness/run.sh OUT 102023799 0 2 100000 exact,menu`. classes-18's Human Druid (race 0, class 2), 100,000 game turns. The shipped `harness/borg.txt` with one line rewritten: the #556 switch on, its companions at their shipped values (births weight 200%, attack window 10 Borg turns).
- **Outcome:** killed by a giant white mouse on DL1 at game turn 11,412, CL3.
- **Reproduction:** verified. The key stream equals the same arm's run in the local classes-18 comparison.
- **Lineage:** with the switch off, the same start plays main's keys and lives to 100,000 (CL8). The game first differs from main at game turn 1,003, on the switch's first decision about breeders. So this is one life of one arm, not an independent sample.

## What happened
- **The decision:** at game turn 9,654 the Druid was **CL1**: 9/12 HP, 2/2 SP, no Phase Door left (it had just read its last one). Three giant white mice were known. The switch judged them unstoppable:

  `# Breeders cannot be stopped: 3 known, 0.39 births a turn, 1.7 turns a kill, danger 10, HP 9`

  0.39 births a turn × 2 (the births weight) = 0.78, against 1 / 1.7 = 0.59 kills a turn. The level was then lost to the breeders (latched until a new level), and the breeder flees acted ("Fleeing (no recall)").
- **What the kill rate missed:**
  - **18 Flasks of oil.** The rate counts melee, a missile from a bow, and the attack the last ranking chose, but **not thrown objects**. A flask (2d6 fire) kills a 2 HP mouse in one throw. The Druid had made no attack in the turns before, so the "last ranking" term was empty too, and the verdict rested on its CL1 whip alone (1d3).
  - **The danger:** 10 against 9 HP. That alone stops the stand for one think; it does not latch the level.
- **After the decision:**
  - No staircase was known: "no up stairs found" 87 times, "Looking for any stair" 66 times. So the flight had no goal, and the Borg wandered (dark and spastic flows) through the colony for about 1,750 game turns.
  - It killed 50 mice, while 98 were seen appearing, and rose to CL3 on their experience.
  - It drank its last Cure Light Wounds at 9,854 and never threw a flask.
- **Fox Form:** the Druid knows Fox Form (level 1, 2 mana; a fox has an extra move a turn, shape.txt `MOVES[1]`). The core's fox escape (#551, `escape_fox_form`) ships off, and it casts only at a flight step toward a goal; here there was no goal. So the shape that outruns mice was never used.
- **The end:** stuck at 2–4 HP for about 200 game turns, then death at 11,412.

## Reading
The switch's decision was wrong on its inputs, not its rule. It judged the colony unstoppable on melee alone, while the Druid carried 18 flasks that each kill a mouse in one throw. Three mice at 0.39 births a turn were well within reach of a thrower.

Found for borg-reborn-rs #556:
1. The kill rate must count thrown objects (`best_throw`, the attack planner's own choice of what to throw).
2. A flight with no known staircase has nowhere to go. Fox Form (#551, shipped off) would at least make the Druid faster than the mice.
3. Whether a CL1 character should flee at all with no staircase known, instead of fighting on, is a further question for the owner.
