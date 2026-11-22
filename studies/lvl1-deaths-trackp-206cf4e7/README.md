# Level-1 deaths of track-p 206cf4e7: the owner's notes, the stair leash, and what to change

The owner: "if we can cut the deaths at lvl 1 we should be golden." This study reads the 20 deaths of one zoo run, answers the owner's note on each, assesses the owner's stair-leash proposal, and replays every death seed with candidate settings. Read it with **one rule in mind: a replay is one start.** It shows what that game needed, not a rate (borg-reborn-rs RULES 14, 20). Every proposal below is a hypothesis until borg-zoo measures it.

- **Run:** borg-zoo [45070528012](https://github.com/diegoami/borg-zoo/actions/runs/45070528012), attempt 2. Experiment `reborn-trackp-206cf4e7-full` (borg-zoo#695), specimen `4.2.6-reborn-rust-trackp-206cf4e7` (borg-reborn-rs `206cf4e769081fb4454fbfe5830d1215706ba76a`), arm `reborn-head-shipped`, classes-1800 full slice: 900 starts, 100,000 turns. 879 reached the cap, 20 died, and 1 hit `wall_timeout` (Human Warrior 1352670668; not studied here).
- **Dossiers:** borg-cemetery#137 (`runs/2026-11-22-trackp-206cf4e7-full-deaths`, open).
- **Reproduction:** all 20 deaths were replayed from birth with the death-report recorder. Every `keys.log` hashes to the zoo cell's `play_sha256`. The replays in the arms tables use the same command line (`tools/arm.py`).
- **Head:** track-p has moved since the specimen. The arms also run on **track-p `7a466d73`** (#1057), which ships `kill_live_zero_hp` (#975), the lone-slow bundle (#878), no-overexert (#1056), `town_first_cure__ranger = 2` (#987) and more.

## The numbers

| | count |
|---|---:|
| deaths | 20 of 900 |
| at CL1 / CL2 / CL4 / CL5 / CL6 | 7 / 6 / 4 / 1 / 2 |
| died with a Cure Light, Serious or Critical Wounds potion in the pack (gear at death, from the recorder's last frame) | 10 |
| the same death (turn and cause) on the previous baseline `9085c266` (run 45028029063) | 8 |
| replayed on the head `7a466d73`, shipped settings: still dead in the **same game** (identical keys) | 7 |
| ... dead in another game | 1 |
| ... alive at the cap (a different game; not proof of a fix) | 12 |

The 7 identical deaths on the head are the target set for anything new: **1024822556, 1194051723, 1398933929, 781905420, 848342657** (all CL1), **2125189042** (CL2) and **1868115537** (CL4). 592754909 still dies on the head, to the same crow by another path.

## The stair leash (the owner's main proposal)

> a character of lvl 1 and or less than 20 HP, without monster detection, never goes further from the stairs than it can get back from in time if a fast monster appears; explores concentrically from the stairs; stair-scums when needed.

**What exists.** C's leash, with its numbers exposed as parameters (#732): `flow_leash_per_level = 3`, `flow_leash_base = 9`. That is 12 flow steps from an up staircase at CL1 for the far exploration flows (`borg_flow_dark_4/5`, the near ones check `borg_flow_far_from_stairs`) and for item pickup. On top sits a return leash of 3 x CL + 14 = 17 (Chebyshev, to the nearest up staircase, `borg_think_dungeon.rs:692`: `# Return to Stair (wandered too far. Leash: 17)`). The kit leash (#840, `kit_leash`, ships 0) shrinks both while the kit is short. Rest-at-the-stairs (#614: `recover_rest_reach_stairs`, `caution_stairs_leave_on_monster`) ships 0.

**Where the Borgs were.** The stairs a Borg knew were rebuilt from the recorded screens: every `<` and `>` drawn, placed on the map through the `@`'s screen position. This is an inference, because the Borg's own map can hold more. 13 deaths were at CL ≤ 2 and 12 of them to monsters:

- in **2** the leash had a hole. Mage 592754909 arrived on a **down** staircase after going back up, and the leash counts only up staircases. Druid 1024822556 hit a teleport trap that threw it 84 squares away, 79 flow steps from the up staircase;
- in the other **10**, the Borg stood **2 to 8 steps (Chebyshev) from a known up staircase when its killer appeared** in 9, and 11 in one (Paladin 1194051723).

So the deaths happened inside the leash. What killed them is what they did at first sight: attack on sight, a fight race "won" on means, a rest, a spell, where a 10–15 HP character should have walked 2–8 steps and taken the stairs.

**A leash measured in time is a few steps.** Grip, Fang, the crow and the wild cat have `speed:120` (`monster.txt`): two moves per player turn. Running away, the Borg loses one square per turn to such a monster. A monster coming from the stairs' side is never escaped. A torch lights 2 grids, so in a corridor the monster is first seen 2–3 squares away. With 10–15 HP the Borg lasts about 2 turns in contact (7–8 damage per turn by its own estimate). The leash that guarantees getting back is about 4–5 steps in a corridor: stair scumming.

**What a tighter leash has cost when measured.** The kit-leash study on track-p `9085c266` (borg-zoo#646, small + medium pooled, 360 paired starts) found:

| arm | deaths | CL ≤ 2 deaths | survivors reaching DL3 | median first turn at DL3 | reaching DL5 | mean CL at 100k |
|---|---:|---:|---:|---:|---:|---:|
| ctl | 7 | 2 | 129 | 64,873 | 11 | 6.34 |
| kit_leash linear (min 1) | 12 | 8 | 127 | 65,606 | 6 | 6.34 |
| kit_leash squared (min 0) | 9 | 4 | 111 | 75,215 | 6 | 6.22 |

(Starts alive in both the arm and the control, 344–353 per arm. Recounted from the results branch's `cells.jsonl`.) A lead, not a measurement. It does not support a tighter leash by itself. The progress baseline is low anyway: 11 of 353 control survivors reach DL5 by 100,000 turns, so "time to CL5 or DL5" is best read as the share that gets there.

**The owner's design, `stair_scum`** (borg-reborn-rs [#1061](https://github.com/diegoami/borg-reborn-rs/issues/1061)). An exploration **mode**, not a tighter leash, while max HP is under a threshold and there is no monster detection. The threshold is 25 to start (14 of the 20 dead Borgs had less), set per class with the existing `__<class>` suffix, plus a per-race delta (the owner; it needs a race suffix):
- the Borg explores only grids from which it can get back to a staircase before anything fast reaches it. The radius is *R* = ⌊*D* / (*r* − 1)⌋ + *k*, from how early a monster is seen there (*D*: the light radius in a corridor, the room in a lit room), the speed ratio of DL1's fast monsters (*r* = 2) and the turns of contact it survives (*k*). With a torch in a corridor that is the owner's **two or three steps**;
- radially, without committing to a corridor, returning toward the staircase between targets;
- a door inside the radius is opened, then the Borg steps back and looks;
- it fights from the staircase and leaves when the fight is lost, and takes a new level when the safe area is used up.

Separately, the C leash's holes are closed ([#1062](https://github.com/diegoami/borg-reborn-rs/issues/1062)): staircases of either kind count, the nearest is measured, a leash remains when no staircase is known, and Recall is read after a teleport strands a weak Borg.

**The owner's summary of the rest**, which the deaths bear out: too few healing potions (the first town trip, below), misjudgement of when to drink and when not to, and Phase Door read where it did not help (694417276, 2025089708, 1194051723). The exception is one that should have phased earlier.

## The deaths, with the owner's notes

Turns are game turns (10 per player turn at normal speed). "Stairs" is the distance to the nearest known up staircase when the killer was first seen (Chebyshev; walk distance where the rebuilt map gives one). "Head" is the replay on track-p `7a466d73` with shipped settings.

### CL1

**781905420, Human Druid, 12 HP. Grey mushroom patch, turn 13,333. Head: same death.**
*Owner: "should he have not quaffed a potion at half HP?"* **Yes.** It stood two steps from the up staircase it had just arrived on, next to an unseen patch (`SPORE:CONFUSE:1d4`, `NEVER_MOVE`). It threw a flask confused (by direction; it missed). Then #969's new floor declined the attack on sight because "a cure or an escape [was] at hand", and #867 declined the cure: "Not fixing Confusion next to an immobile confuser: attacking first". Neither happened. It walked confused into a wall and died with 8 CLW. A CLW heals 20 (a full heal) but does not cure confusion (CSW does, `object.txt`). Drinking, then stepping away from a monster that cannot follow, was the way out. This start lived to the cap on `9085c266`, before #969. New issue: the #969/#867 deadlock.

**1194051723, Elf Paladin, 15 HP. "A fatal wound" after Fang, turn 1,700. Head: same death.**
*Owner: "too many flasks of oil, too few healing [potions], or [flee] earlier. Phase door rather than heal if you are just prolonging the inevitable."* **Half agree.** The first trip bought 3 torches, 6 Phase Door, 29 flasks of oil (87 gold), 4 rations and 5 CLW. Fang (25 HP, AC 36) bit first from the dark, 11 steps from the stairs. The fight race said "winning, 2 turns to kill" at HP 10 or more and "not winning" below. So it alternated, throw, CLW, throw, CLW: 6 throws at Fang, 1 hit, 5 CLW drunk. It read Phase Door at 2 HP and bled to death from a graze. Phase Door against a +10 dog buys one or two turns. The real mistakes were the coin-flip fight race (borg-reborn-rs #992, #986) and not walking back 11 steps at the first bite. **`town_first_cure = 2` on the head saves this game**: the trip buys its CLW before the oil.

**1398933929, Dwarf Necromancer, 13 HP. Wild cat, turn 1,830. Head: same death.**
*Owner: "if he had opened the door next to the stairs he would have known there was a cat there earlier. Maybe. Not sure if worth to save this."* **I read it differently.** It arrived on the up staircase and stepped 2 squares to pick up a scroll. Then came "You hear a door burst open!" twice (turns 1,805 and 1,810). The cat burst the door next to the staircase at 1,812. Opening the door itself would not have told it more than the two warnings did. The cheap rule: at CL1, a door bursting open nearby means step back onto the staircase. It instead threw 2 flasks of oil (both missed) and died 2 turns after first sight, still 2 steps from the stairs, with 9 CLW and 6 Phase Door. **#926's 75th-percentile escape test (`fast_fragile_escape_quantile = 75`) saves it on the head**: it reads Phase Door one turn earlier, at 8/13.

**848342657, Hobbit Priest, 10 HP. Grip, turn 2,852. Head: same death.**
*Owner: "also a difficult one. I think lvl 1 characters should stay close to the stairs [...]"* **Agree on the outcome, not the cause.** It was 7–8 steps from the stairs. A crow (attack on sight, #842) took it to 5/10. It read Phase Door, then **rested at 5/10** with the crow still around. Grip arrived at distance 2 and the crow came back; it died 1 turn later with 2 Cure Serious Wounds unused. At 10 max HP against a crow and Grip (more than 10 damage per turn together), healing in contact would not have helped. Not resting at half HP with a fast monster nearby, and walking the 7 steps right after the Phase Door, might have. **Saved on the head by `kit_leash = 1`, by rest-at-the-stairs, and by `item_test_unknown_potions = 0`**, but every one of those diverges hundreds of turns earlier: chance, not a fix.

**1024822556, Dunadan Druid, 13 HP. Fang, turn 3,086. Head: same death.**
*Owner: "same as above"* (the stair leash). **Disagree on the cause.** The leash held: it was exploring 2–4 steps from its arrival staircase until a **teleport trap** (turn 1,671) threw it 84 squares away. The only known up staircase was then 79 flow steps off. It walked back ("heading up, bored"). Fang found it 38 steps short and chased it for 70 player turns: 7 CLW and 6 Phase Door spent, "Refusing flight Recall" more than 50 times (#986). The leash cannot help after a teleport. Reading Word of Recall at the quiet moment right after the trap (DL1: a trip to town) would have. New issue (leash holes, part 3).

**453254028, Half-Elf Necromancer, 12 HP. Grip, turn 3,421.** (borg-reborn-rs #974.) **Head: alive (another game).**
*Owner: "same as above."* **Disagree on distance.** Grip appeared 2 squares away while the Borg stood 4 steps from the staircase at full HP. It threw a flask instead of walking. A Necromancer's throw skill is 20 + 5 (Half-Elf) at CL1, and against AC 36 its throw hits about 12% of the time, little more than the engine's automatic hit (`player-attack.c` `hit_chance`: a to-hit of about 24 against AC x 2/3 = 24). Then a Phase Door landed it next to a grey mushroom patch: confused, three attackers, death 16 turns after first sight. The stair retreat at first sight is exactly this case.

**282602274, Hobbit Ranger, 12 HP. Grey mold, turn 5,467. Head: alive.**
*Owner: "again too much exploring for a lvl 1, and [not] a CLW to cure confusion when at half HP."* **Disagree.** There was no confusion in this game (no "confus" in its messages). It was 8 steps from the stairs. It shot the grey mold once (the mold lived at 0 HP), rated it at 0 HP and walked next to it: 12 -> 5 in one turn, a missed melee, dead. That is #975, fixed on the head by `kill_live_zero_hp = 1`, which the replay confirms (the game diverges at the mold).

### CL2

**592754909, Kobold Mage, 8–11 HP. Crow, turn 3,574. Head: crow, turn 3,569.** (borg-reborn-rs #990.)
*Owner: "a lvl 1 mage should have a stronger leash."* **Agree, and the leash had a hole.** It went down, then back up ("Needing to get back on correct depth"), and arrived on DL1 on a **down** staircase. The leash counts only up staircases, so it had none, and it was 26 steps away when a crow bit it from 8/8 to 3/8. Its death came from a Magic Missile cast without the mana ("You faint from the effort!"), fixed by #1056. On the head it still dies at 3/11: the crow is at range, so neither Phase Door nor a cure is allowed (#990). **Saved on the head by `town_first_cure = 2`** (an early divergence), **and by #926's heal floor at the fatal moment** (it drinks CLW at 3/11 with the crow not adjacent).

**142490685, Human Ranger, 18 HP. Poison, turn 4,210. Head: alive (another game).**
*Owner: "Seriously - tried a potion because he felt [safe], and then it started exploring like it was nothing? Go up the stairs, drink something, recover, and go back to exploring."* **Agree.** Standing on DL1's up staircase, it drank its unknown "Cloudy Potions" as the #983 test: Poison, `10+2d7` turns at 1 HP each with no regeneration. It explored on from 18 HP to 0 and died 6 steps from the stairs. Its only Neutralize Poison had gone into an earlier test. At 18 HP a test that turns out to be Poison kills with probability 57% without a cure (P(10+2d7 ≥ 18)). New issue: a max-HP gate for #983 and a poisoned-on-the-stairs rule.

**269489578, Dunadan Priest, 20 HP. Grip, turn 6,595. Head: alive.**
*Owner: "too far from stairs at lvl 1."* **Partly.** It was 5 steps from the stairs (8 walking) when Grip bit. It had walked next to an unseen grey mold first and spent its only CLW there. At 6/20 it melee'd Grip twice, because the Phase rule said "fight not lost (danger 4, HP 6)" while the fight race said "not winning". At 2/20, fleeing, it spent turns learning two prayers and swapping its torch. The whole game it bought one CLW: its first trip was 3 torches, 4 Phase Door and 3 rations. All four Priests among these deaths left their first town trip with no cure.

**2125189042, Half-Troll Necromancer, 15–17 HP. Crow, turn 8,350.** (borg-reborn-rs #982.) **Head: same death.**
*Owner: "too far from stairs at lvl 1 and cannot [...]"* **Disagree on distance:** 4 steps (Chebyshev). The crow bit first (11/15). Attack on sight: Nether Bolt, which failed. Down to 2/15, it read Phase Door, threw a flask at a mouse, studied a spell, and **rested at 2/17 with 12 CLW**. The crow came back. Rest-at-the-stairs on the head walks it on instead, and it dies 5 turns earlier. The answer at 2 HP out of contact is the potion (#982).

**2136378178, Human Necromancer, 14 HP. Wild cat, turn 18,834. Head: alive.**
*Owner: "unlucky, too far from stairs."* **Not unlucky.** It was 5 steps from the stairs. It spent 8 confused turns swinging at a grey mushroom patch ("You chip away futilely with your weapon at the granite wall"), 14 -> 3 HP with one CLW between. A wild cat arrived as the patch died. At 3/14, confused, it threw a flask "by direction" (75% of confused aims go a random way: `player_confuse_dir`). The CLW would only have reset one cat turn (8 damage per turn against 14 HP). The mistake was the long confused fight at the patch, not the last turn.

**327746368, Gnome Priest, 17 HP. Crow, turn 50,310. Head: alive.**
*Owner (later note): "Again a fragile character too far away from stairs and with few healing potions."* **Agree on the potions.** It was still CL2 after 50,000 turns, with 7 gold and no cure at all. It was 7 steps from the stairs. It attacked the crow on sight in melee, read Phase Door at 3/17 twice and rested twice, then cast Bless (a "boost"), and the crow killed it. On `9085c266` this start died at turn 4,712 to a grey mushroom patch, so #969 bought it 45,000 turns.

### CL4–CL6

**1868115537, Half-Elf Warrior, 31 -> 57 HP (CL2 -> 4 at the end). A poison pit, turn 11,236. Head: same death.**
*Owner: "poisoned, he does not go back to the stairs, where are his healing potions."* **Agree on the potions: it never had one.** Its first trip bought 2 torches, 6 Phase Door, 4 rations and 10 flasks of oil. Three steps from its arrival staircase it fell into a poisonous spiked pit, cured the poison with its only Neutralize Poison, and set off a blinding gas trap. Blind, it fought an invisible monster down to 4/57. It tried to go back: "Bored but unable to flow to up stairs", every think. The staircase was 5 steps up a corridor and the known gas trap sat on the only path. It stepped the other way onto an unknown pit. Crossing a blinding gas trap (no damage, `trap.txt`) at 5 HP with nothing in view was the safe move. **`town_first_cure = 2` on the head saves it** (it buys one CLW), as does `kit_leash = 1` (an early divergence). New issue: a known harmless trap blocking the only path to the stairs.

**645909552, Dwarf Mage, 26 HP. "A fatal wound" after a crow, turn 57,530. Head: alive.**
*Owner: "no idea."* It came up from DL2 onto a **down** staircase (no leash: only `>` known) and opened two doors 30 steps away. A crow bit first. Attack on sight (#842) cast Magic Missile **three times and failed all three** ("You failed to concentrate hard enough!"), 26 -> 21 -> 16 -> 11 -> 0. Phase Door came at 0 HP, and the graze bled it out. It carried **10 CLW and 5 CSW** (CSW cures cuts). #842 bans healing in contact. Here a CLW (20 HP) outheals the crow (6.4 per turn by its estimate) three times over and would have bought three more casts.

**584191223, Half-Elf Mage, 17 HP. "A fatal wound" after a crow, turn 41,550. Head: alive.**
*Owner: "at 41521 he has a graze and no healing potions. It seems a pattern, we should nudge the inventory to buy a few more healing potions at the beginning. And why he goes so far from the stairs with no healing potions - I have a kit_leash turned off but it does not seem to help. Having no healing potions is the same as being lvl 1 [...] he has HP < 20."* **Agree.** CL4, 17 HP, no cure, 2 gold. The crow bit first, 14 -> 3 in one turn with a graze. It read Phase Door at 3/17 and bled to death 4 turns later, 19 steps (Chebyshev) from the stairs. `kit_leash` ships 0 (switched off), so it cannot have helped. With `kit_leash = 1` the leash would shrink with no cures in the pack, which is the owner's "no healing potions is the same as being lvl 1". The zoo has measured it only on `9085c266` (above). Gold is the binding constraint here: it had 2.

**312081895, Half-Troll Blackguard, 67 HP. Poison (a white jelly), turn 39,700. Head: alive.** (borg-reborn-rs #984, #1023; cemetery study `recall-shallow-blackguard-312081895`.)
*Owner: "at 39,399 I guess he forgets that the jelly is there and he needs to go there, I guess we need 890 for that, check if the 899 PR would have saved."* **Not forgetting: the jelly is on screen** (`j` two squares west, in view, at turn 39,437). The loop is #1023's. The strategic retreat steps one square east, and the next think's exploration flow (`Flowing toward dark-2`) walks back west next to the jelly, because the only unexplored grids lie behind it. 132 such turns poisoned it to death. #890 (`unseen_belief`) only aims ranged attacks at monsters believed in the dark. With the jelly in view it would not change this, and the replay with `unseen_belief = 1` agrees (arms table). #899 is the cursed-torch issue, and this Blackguard had no cursed light. **I could not identify which "899 PR" is meant**: please name it and I will replay it. The deeper cause is the earlier study's (#984): it read its only Recall in town at CL4 and was stranded on DL2 with no staircase found for 28,700 turns.

**694417276, Half-Troll Priest, 55 HP. A cave spider, turn 28,692. Head: alive.**
*Owner: "I would have not phased door, stand and fight or go back to the stairs, at 28,617. Once in that room there was nothing more to do."* **Agree.** At 41/55 the fight race had said "winning" against the adjacent soldier. An apprentice came into view, danger rose to 67, and "escape 1 emergency" read Phase Door. The landing check counted 0 scary grids of 100 because the room was unexplored. It held a shrieker, four cave spiders (hasted by the shriek) and an icky thing. It was dead 75 game turns later, 5 steps from the stairs. New issue: Phase Door into unexplored grids.

**2025089708, Half-Elf Blackguard, 60 HP. A soldier, turn 40,759. Head: alive.**
*Owner: "not sure how he got himself in that situation, probably would need to go back there, I would guess he phased door when he should not have."* **Agree, the second Phase Door.** A door burst open: an apprentice (it blinks and blinds), a soldier and a shrieker. It was 3 steps from the up staircase ("Close enough to Stair") with the soldier in the way. At 43/60 it read Phase Door ("escape 3.3 danger fallback", 74 scary landing grids of 100, limit 75) and landed farther from the stairs. At 15/60, carrying **13 CLW**, it walked "Desperate for Stairs" into the soldier without drinking (borg-reborn-rs #908) and died.

**526144893, Human Ranger, 45 HP. A cave spider, turn 56,769. Head: alive.**
*Owner: "at 56,655 the best strategy would have been using arrows - but ... he has no arrows left? That is even worse than no healing potions. With speed he might have dashed to the door."* **Agree on both.** Its last arrow went at turn 44,470, and its last town visit was at turn 17,055: almost 40,000 turns without restocking, with 395 gold at death (#935 is the same pattern). It carried **2 Potions of Speed** and drank neither (#913). Against a swarm of +10 spiders, with no arrows and no cure, Speed and the door were the only way out. Its only known staircase was a down one, so no leash either. `kit_restock = 1` exists for the restock half and ships 0.

## Replays (one start each; leads, not measurements)

`tools/arm.py NAME 'param=value,...' [seeds] [game]` replays every death seed from birth with the bundle's `user/` (or, with `HARNESS=`, a build's `harness/borg.txt`), with the overrides written into `borg.txt`, to 100,000 turns. `tools/vs.py REF ARM...` pairs an arm against a reference arm by keys. "Same game" means identical keys; "diverges" gives the game turn of the first differing key.

**Read the "saved" counts with care.** The control survives 879 of 900 starts (97.7%). Any change that alters a game early "saves" most of these 20 seeds by chance: on the specimen, `item_test_unknown_potions = 0` alone "saved" 11. A rescue is targeted only when the arm plays the same game until near the fatal point.

| arm | borg.txt change on track-p `7a466d73` | deaths of 20 | same game as the control | saved (game turn the game splits) | newly killed |
|---|---|---:|---:|---|---|
| h-base | (none: the head control) | 8 | 20 | - | - |
| h-firstcure2 | town_first_cure = 2 | 4 | 10 | 1194051723 (591), 1868115537 (481), 592754909 (171), 781905420 (181) | - |
| h-startres | kit_start_reserve = 1 | 5 | 11 | 1194051723 (591), 1868115537 (481), 592754909 (171), 781905420 (181) | 142490685 (dies at 83,535, a wild cat) |
| h-ffheal | fast_fragile_heal_floor = 50, fast_fragile_escape_quantile = 75, fast_fragile_count_dot = 1 | 6 | 18 | 1398933929 (1,822; at the fatal moment), 592754909 (3,562; at the fatal moment) | - |
| h-cure-ff | town_first_cure = 2 + the #926 bundle | 3 | 9 | 1194051723 (591), 1398933929 (1,822; at the fatal moment), 1868115537 (481), 592754909 (171), 781905420 (181) | - |
| h-cure2p400-ff | town_first_cure = 2, town_first_cure_percent = 400 + the #926 bundle | 2 | 6 | 1194051723 (581), 1398933929 (341), 1868115537 (481), 2125189042 (831), 592754909 (171), 781905420 (171) | - |
| h-cure-ff-notest | town_first_cure = 2 + the #926 bundle + item_test_unknown_potions = 0 | 2 | 1 | 1194051723 (591), 1398933929 (1,822; at the fatal moment), 1868115537 (481), 592754909 (171), 781905420 (181), 848342657 (1,192) | - |
| h-notest | item_test_unknown_potions = 0 | 7 | 6 | 848342657 (1,192) | - |
| h-reststairs | recover_rest_reach_stairs = 20, caution_stairs_leave_on_monster = 1 | 6 | 11 | 592754909 (1,602), 848342657 (1,962) | - |
| h-kitleash | kit_leash = 1 | 5 | 9 | 1398933929 (781), 1868115537 (981), 848342657 (621) | - |
| h-restock | kit_restock = 1 | 7 | 17 | 1868115537 (9,328) | - |
| h-unseen | unseen_belief = 1, cave_light_engine_radius = 1 | 3 | 2 | 1024822556 (321), 1194051723 (1,191), 1868115537 (901), 592754909 (571), 781905420 (2,111), 848342657 (771) | 282602274 (dies at 20,280, a wild cat) |

On the specimen `206cf4e7` itself (the bundles' own `borg.txt`): `item_test_unknown_potions = 0` 9 of 20 dead, `kit_start_reserve = 1` 14, rest-at-the-stairs 12. `town_first_cure` does not exist there.

**What the head table says.** The cure purchases and the #926 bundle add up, and kill no seed the control kept alive: control 8 dead, `town_first_cure = 2` 4, the bundle 6, both 3, both with `town_first_cure_percent = 400` **2**. The bundle's two rescues are at the fatal moment. In 1398933929 the 75th percentile of the cat's damage (9.0) reaches its 8 HP, so it reads Phase Door a turn earlier. In 592754909 it drinks a CLW at 3/11 with the crow at range. The cure rescues split at the first town trip, as they should: the Paladin buys 5 CLW before 29 flasks of oil, and the Warrior buys 1 CLW instead of 6 more flasks. Two deaths survive every arm but the light-radius one (which reshuffles 18 of 20 games): 1024822556, the teleport trap (#1062), and the 79-gold Priest 848342657. At 79 gold, 4 Phase Door (60) win over a first CLW (20) even at 400 percent; that is the stair-scum case (#1061).

## Settings proposals (borg-reborn-rs `harness/borg.txt`)

Each needs the zoo before it ships (the PR below). For shipping, the evidence the owner asks for is a medium-tier paired study and a confirmation.

| setting | proposed | the deaths it addresses (head replays) | status |
|---|---|---|---|
| `town_first_cure` | 2 for every class (ships 0; the Ranger 2) | Paladin 1194051723, Warrior 1868115537, Mage 592754909, Druid 781905420 saved; in the study's reading also 269489578, 327746368, 584191223 (no cure; they live on the head anyway) | borg-reborn-rs#1006 asks the zoo; in the pilot |
| `town_first_cure_percent` | 400 (ships 200) | adds 2125189042 | in the pilot |
| `fast_fragile_heal_floor`, `fast_fragile_escape_quantile`, `fast_fragile_count_dot` | 50, 75, 1 (ship 0) | 1398933929 and 592754909, both at the fatal moment | in the pilot (#926; the zoo's pilot at 25/50 showed nothing at its size) |
| `kit_leash` | measure, do not ship | 3 saved in early-splitting games; more CL ≤ 2 deaths in borg-zoo#646 | in the pilot, as the owner's leash's nearest existing switch |
| `recover_rest_reach_stairs`, `caution_stairs_leave_on_monster` | 20, 1 (ship 0) | 592754909, 848342657 (early splits); 2125189042 dies 5 turns sooner | in the pilot |
| `item_test_unknown_potions` | keep 1, gate it in code (#1063) | 0 only reshuffles games (14 of 20 split) | not proposed |
| `kit_start_reserve` | not proposed | the same four as `town_first_cure`, and kills 142490685 | - |
| `unseen_belief` | not proposed for these deaths | no attributable rescue; it does not touch 312081895 (the jelly is in view) | - |
| `kit_restock` | a separate study | 526144893 (no arrows for 12,000 turns, no town for 40,000) | - |

## Code proposals

| issue | what | the deaths |
|---|---|---|
| [#1061](https://github.com/diegoami/borg-reborn-rs/issues/1061) | `stair_scum`: the owner's exploration mode under 25 max HP | the CL1–2 deaths within 2–8 steps of the stairs; 848342657 on the head |
| [#1062](https://github.com/diegoami/borg-reborn-rs/issues/1062) | the C leash's holes; Recall after a teleport strands a weak Borg | 592754909, 645909552, 526144893; 1024822556 on the head |
| [#1063](https://github.com/diegoami/borg-reborn-rs/issues/1063) | #983's test at low HP: a max-HP gate, and the poisoned-on-the-stairs rule | 142490685 |
| [#1064](https://github.com/diegoami/borg-reborn-rs/issues/1064) | #969/#867 deadlock: the cure #969 counted is taken | 781905420 (same death on the head) |
| [#1065](https://github.com/diegoami/borg-reborn-rs/issues/1065) | the fast-fragile heal ban by HP-to-damage ratio (the owner's objection, in numbers) | 645909552; 2125189042 with #982 |
| [#1066](https://github.com/diegoami/borg-reborn-rs/issues/1066) | Phase Door into unexplored grids counted as safe | 694417276, 2025089708 |
| [#1067](https://github.com/diegoami/borg-reborn-rs/issues/1067) | a known harmless trap on the only path to the stairs | 1868115537 (same death on the head) |

Already open and confirmed by these deaths: #982 (rest at 2 HP with 12 CLW, 2125189042), #986 and #992 (the fight race against Fang, 1194051723, 1024822556), #990 (crow at range, 592754909), #974 (453254028), #1023 (the retreat loop beside the jelly, 312081895), #908 ("Desperate for Stairs" while hit, 2025089708), #913 (Speed never drunk, 526144893), #935 (out of arrows, no town).

**Else to investigate.**
- Why the four Priests' first trips bought no cure. At 79 gold the Phase Door reserve outbids `town_first_cure` even at 400 percent. Whether the planner counts a Priest's Minor Healing prayer as a cure is a hypothesis to check in `borg_town_capability.rs` (a Priest learns its prayers at random, and 327746368 had none to heal with).
- Three Wooden Torches bought on most first trips (18 of 70–80 gold) before any cure.
- The throw's hit chance against AC 36 for weak throwers (a CL1 Necromancer hits Grip about 12% of the time) and whether the fight race counts it (#986).
- The `wall_timeout` cell (Human Warrior 1352670668) was not reproduced here.

## Test plan

1. The 20 death seeds, replayed above, on the head `7a466d73` (done; the tables).
2. A zoo pilot on track-p `7a466d73`, then verysmall, as a definition PR in borg-zoo ([borg-zoo#708](https://github.com/diegoami/borg-zoo/pull/708), not dispatched). It covers the control, `town_first_cure = 2` for every class (also at 400 percent with the bundle), the #926 bundle, the two together, the kit leash and rest-at-the-stairs. The gate is the usual one (no config_error, one binary, every cell ends). At these tiers the endpoint is directional only. At about 2% deaths, 45 starts per arm expect one death, so a claim needs the medium tier and then a confirmation on an unopened block (RULES 14). Dispatch is the owner's call.
3. The code proposals, once written, replay these 20 seeds first (targeted rescues at the fatal point), then join the same ladder.

## Tools

- `tools/arm.py`: replay arms (above).
- `tools/vs.py`: pair arms by keys.
- `tools/stairmap.py`: rebuild the staircases each Borg saw from the recorder's `frames.jsonl` (every `<` and `>` drawn on the map, placed through the `@`'s screen position). Then give, per death, the Chebyshev and walk distance from the nearest known staircase when the killer was first created and at death. An inference: the Borg's own map can know more than the screens showed.
- `arms/*.json`: every replay's outcome (dead, cause, game turn, max CL and DL) and the sha256 of its `keys.log`. `h-*` ran on track-p `7a466d73` with its `harness/borg.txt`; `s-*` on the specimen with the bundles' `user/borg.txt`. `s-base` reproduces the keys of all 20 zoo games; `h-base` those of the 7 deaths that repeat on the head.
- The scripts were run from a scratch directory: `S` at the top of each is that directory. It holds `W/d/<seed>` (the zoo bundles), `W/src` (the specimen, with the death-report recorder build) and `W/head/build/plain/game` (track-p `7a466d73`, `cmake -S engine -B build/plain -DCMAKE_BUILD_TYPE=Release -DBORG_FEATURES= -DSUPPORT_X11=OFF`). Set it before reusing them.
