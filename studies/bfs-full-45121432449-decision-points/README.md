# Decision points of the 25 deaths of borg-zoo run 45121432449 (breadth-first on/off, track-p 1c071812), poison first

**Source.**
- borg-zoo#730, Actions run [45121432449](https://github.com/diegoami/borg-zoo/actions/runs/45121432449) attempt 1, experiment `reborn-bfs-full`.
- Specimen `4.2.6-reborn-rust-trackp-1c071812` (borg-reborn-rs `1c07181217a7f7076dc6d3c158bebeb00b968f76`, borg-rs core).
- Arms `reborn-bfs-ctl` (shipped, `explore_breadth_first 1`) and `reborn-bfs-bfs0` (`explore_breadth_first 0`): classes-1800 full slice, 900 starts each, 100,000 turns. 25 deaths: 13 ctl, 12 bfs0.
- Dossiers and the case page: [runs/zoo-reborn-bfs-full-45121432449](../../runs/zoo-reborn-bfs-full-45121432449/README.md), [runs/2026-11-23-bfs-poison-deaths](../../runs/2026-11-23-bfs-poison-deaths/README.md) (borg-cemetery#144). This page was written from the bundles before reading that case page, then checked against it. One correction came from it: the Paladin 1200156945's unused potions, confirmed in the recorder's final frame.

**Evidence used.**
- For every death: `messages.log`, `state.log` (the poison counter is timed index 7), `keys.log` and `trace-core.jsonl` from the zoo bundles.
- A replay from birth with a recorder build of 1c071812. Its keys hash to the cell's `play_sha256` for all 25, and its last frame gives the gear at death.
- Engine facts from `engine/angband` at 1c071812, cited by file and line.
- Counterfactual replays: [tools/](tools/), results in [evidence/](evidence/).

Follow-ups: the proposals are borg-reborn-rs#1134; a zoo pilot for the three settings is proposed as borg-zoo#738 / borg-zoo#739 (not dispatched).

Inferences are marked *inference*. Every number here was recounted against `state.log`, `messages.log` or the result files.

## Findings in short

- **Poison is the leading cause: 7 of 25 deaths** (4 ctl, 3 bfs0). It covers two mechanisms:
  - **Bleed-out: 3.** All three meleed a never-moving **white jelly** while its touches pushed the counter to 190, 284 and 110. Meanwhile they drank Cure Light Wounds, which does not cure poison.
  - **Attrition ended by a poison tick: 4.** Breeding worm masses, a blubbering icky thing, a tamer's pack. Poison only stopped regeneration and took the last HP.
- **None of the 7 drank a poison cure.** Only one carried one (the Paladin: 2 Neutralize Poison and 10 CLW, unused). Four of the 7 are Druids at CL4–7, who could cast Cure Poison from [Gifts of Nature] (CL4, base cost 400); none owned it, and none was ever in town at CL ≥ 4 with 400 gold.
- **20 of the 25 died holding a Phase Door or a cure potion** (17 Phase Door, 12 CLW/CSW, 4 Neutralize Poison). The common blocker is the owner's Phase rule (borg-reborn-rs#584). It allows Phase only when the danger without fear reaches 100% of HP, and that danger leaves out poison and paralysis. It logged a refusal ("the fight is not lost") at some point in 18 of the 25 games (whole-game count), and at the fatal episode in several of the deaths below.
- **Counterfactuals:**
  - `escape_phase_lost_danger_percent = 50` rescues 5 deaths at the fatal point, 2 of them poison;
  - `caution_confused_clw_cure = 1` rescues 2;
  - the borg-reborn-rs#932 / borg-reborn-rs#1023 oscillation breaker rescues 1;
  - none of them killed any of the 18 sampled survivors.
  - borg-reborn-rs#934's switch and the status flight change nothing here.
  - Turning off borg-reborn-rs#758's Recall check rescues 3, but it reverts an owner decision. The code change C4 is proposed instead.
- **Breadth-first exploration:** no signal in the deaths (13 against 12, one start dying in both arms).

## Per-death table

Sorted with poison first, then the other deaths in reading order. Turns are game turns (t), keys are `messages.log` key numbers.

| # | seed | arm | character | CL | DL | killer | what happened at the fatal point (key, game turn) | kit at death (recorder) | what it could have done instead |
|---:|---:|---|---|---:|---:|---|---|---|---|
| 1 | 799968561 | ctl | Elf Druid | 4 | 0 | poison | Opened a door beside a **white jelly** (key 2705, t21877). From t21887 it meleed the jelly with a Whip (1d3) ("attack type 1 with value 11") for about 30 player turns and drank 11 Cure Light Wounds. Poison counter 4 → 190 (t22187) at HP 15/21; poison passed HP at t21894 (15 vs 11). It took the stairs to town at t22327 with poison 162, HP 29/32 and 53 gold, sold and dropped items there (keys 2902–2983), and died at t22600 with 108 poison turns left. | Phase ×4; no cure | Step out of the jelly's reach: the jelly never moves, and at first contact the poison was 4 at HP 18. Do not drink CLW against poison (it does not cure it). By town it was lost: 53 gold buys no Neutralize Poison (base 75). |
| 2 | 626789725 | ctl | Half-Elf Rogue | 3 | 1 | poison | A **blubbering icky thing** (seen t26863, then lost) crawled on it mid-flow (key 3341, t27219). It stayed adjacent: the Phase rule said "enemy adjacent but the fight is not lost (danger 8, HP 11)", so it threw oil point-blank and drank 3 CLW + 1 CSW. It killed the thing at t27273 with poison 28 vs HP 12/15. In town (t27333: HP 14/19, poison 21, **9 gold**) it bought a Cloak and a Flask of oil, went back down, then up and down the stairs, and died at t27480 with poison 7 left. | Phase ×6, oil ×20 | Phase Door at the first crawl (HP 10, poison 5), then oil from range (it had 20; the thing has 18 HP). With 9 gold the town could not help. |
| 3 | 956247604 | ctl | Elf Ranger | 5 | 1 | poison | DL2, key 10268 (t86980): meleed a **white jelly** with a Main Gauche while a cutpurse stole 79 gold. Under "Fleeing and leaving the level (scaryguy)" it went on meleeing the jelly (value 13) until it died at t87094: poison 7 → 110, HP 35/47, 4 CLW drunk. It reached DL1 at t87372 with poison 82, HP 37/47, 2 CLW and 171 gold, and then **explored DL1** (dark-bfs) instead of climbing. "Leaving (bleeding/poison)" fired only at t87912 (HP 13; the rule needs HP < MAXHP/2 and a 25% roll). Recall was refused ("34 poison HP included"). It oscillated on a down staircase and died at t88060. | Recall, Phase ×5 | Leave the jelly when the poison passes the HP (t87012: 32 vs 29). At DL1, keep climbing: the Alchemist always stocks CLW, and 171 gold buys several (inference: about 77 HP of healing against 82 poison is marginal without town). |
| 4 | 1575381233 | ctl | Elf Druid | 7 | 1 | poison | A level of breeding **white worm masses**. After t91000 it made 49 melee attacks with a Whip. It drank its last CLW at t91546, so poison (≤ 14 turns) kept regeneration at 0 while crawls added more. HP 40/45 → 0 over 674 game turns. It was in "scaryguy" mode with no up stair known, and Recall was refused every think (borg-reborn-rs#758: 44–94 HP of modelled exposure vs HP 22–29). It read Phase only at HP 0 (t92036). | Phase ×13, Speed ×4, 460 gold | Walk away: the worms have speed 100 against its 110, so it moves twice per worm move. Or Phase Door, then Recall. It had 13 Phase and 4 Speed potions. |
| 5 | 727698927 | bfs0 | Dunadan Druid | 7 | 2 | poison | Saw a **white jelly** at t61494 (danger 48) and retreated; the next flow brought it back beside the jelly (t61544). It attacked (value 98), cast Slow Monster on it, then meleed with a Whip until the jelly died at t61939: poison 0 → 284, HP 16/57, 5 CLW drunk. Recall was refused the whole time ("124.37 HP"). It started an 79-step stair flow in Fox Form and died at t62100 with 236 poison turns left. | Phase ×16, Speed, 644 gold | Do not melee a 36 HP never-moving poison-toucher with 1d3; step out of reach. The poison passed the HP at t61592 (40 vs 39). |
| 6 | 1200156945 | bfs0 | Half-Elf Paladin | 6 | 2 | poison | Opened a door at full HP (49/49, t91909) onto a **tamer** and its pets (scaryguy, danger 68). It stayed and meleed with a Dagger. The tamer slowed it, and a giant black ant and a blubbering icky thing joined. The Phase rule refused Phase down to HP 10 ("danger 12 without fear", 89 with); the Phase then landed with 100 of 100 grids scary, and it was confused. Died at t92070 from a poison tick (poison 10). | **CLW ×10, Neutralize Poison ×2, Phase ×27, Recall** | Phase Door at the first sight of a scary pack, or quaff CLW. Poison was incidental: the death is a lost multi-monster melee with every remedy unused. |
| 7 | 1902932078 | bfs0 | Human Druid | 7 | 1 | poison | A worm-mass level (89 worms killed over the game). From about t52391 it oscillated between (44,165) at danger 32 and (44,166) at danger 1 ("Retreating to 44,166", then "Flowing toward down-stairs at cost 57", "Spent too long on level") for about 70 player turns. Each step back was crawled on, and poison ≤ 8 kept regeneration at 0. HP 39 → 0. It read Phase only at about HP 1 (t53091). | Phase ×16, 120 gold | Phase Door out of the pocket, or any route that does not re-enter the worms' reach. Its last CLW went at t51871. |
| 8 | 1397430180 | ctl | Dunadan Priest | 1 | 1 | a cutpurse | During an 8-key walk (keys 337–345, t2511–2591) a cutpurse hit 4 times: HP 14 → 3. It read Phase (HP 3), then walked 9 squares toward the up stairs with the cutpurse following. Died at t2645. | **CSW ×2**, Phase ×7, oil ×7 | Quaff CSW (heals 40, i.e. full) after the Phase, or throw oil from range. |
| 9 | 1520819173 | ctl | Gnome Mage | 1 | 1 | a crow | A gas trap confused it (t1421). It rested while confused (t1431). A crow arrived (t1531). Confused, it cannot read (player-util.c:1182), so it threw oil in a random direction (borg-reborn-rs#867). Died at t1541. | Phase ×6, **CLW ×6** | CLW shortens confusion by 20 turns (object.txt), then Phase Door. `caution_confused_clw_cure` (borg-reborn-rs#837) ships 0. |
| 10 | 1896645817 | ctl | Half-Troll Priest | 2 | 1 | a giant white mouse | Breeding mice. It read its last Phase at t5562, and a mouse blocked the stairs. Surrounded (7–10 monsters), at HP 4/26 it spent a turn **studying a prayer** (t5622). Died at t5638. | Neutralize Poison, Recall | (Inference) Leave the mouse level earlier; never study while surrounded. |
| 11 | 389489263 | ctl | Gnome Priest | 2 | 1 | Fang | Fight race "not winning" (borg-reborn-rs#759) yet it kept fighting ("Boosting bravery"). Phase landing was refused (94 of 100 grids scary, at most 20). At HP 1 and 0 it walked onto copper twice (t4460, t4500), read Recall at t4520, and died at t4571 before it activated. | books, Speed | Phase earlier, while landing grids were acceptable. Not picking up gold at 1 HP. |
| 12 | 500978646 | ctl | Kobold Priest | 3 | 1 | Grip | Fight race "not winning"; CSW at HP 8. Recall refused (borg-reborn-rs#758, exposure 136–171 HP). It walked toward stairs 60–71 steps away, and Grip caught it. Died at t4747. | CLW, Recall | (Inference) Against a speed +20 dog, neither Recall nor a 60-step walk works; the fight (or no engagement at CL3) decides. |
| 13 | 220674435 | ctl | Half-Troll Druid | 2 | 1 | a fatal wound | A **soldier** (level 6) at DL1. The fight race said "winning" (7.1 modelled damage/turn); the soldier did 15 HP in one turn (28 → 13), then 14 more while the Borg walked 2 squares ("Desperate for Stairs (two)"). Died at t11460. | **CLW ×14, Phase ×6**, oil ×19 | Phase Door at HP 13/28 beside a soldier, then oil from range. |
| 14 | 965142510 | ctl | Human Paladin | 3 | 1 | a floating eye | While walking a dark-bfs flow it stepped beside an unseen **floating eye** (t20928). Paralysis lock until death at t21310: the keys are only `-more-` dismissals, and no Borg think happened. | Phase ×6, CLW ×4 | Nothing once paralysed. Before: no Free Action, and the eye was first seen by its gaze (inference: unlit). |
| 15 | 1308765461 | ctl | Hobbit Priest | 1 | 1 | Grip | Fight race "not winning" at HP 2; 2 CSW. Recall refused ("unmodelled spell/status risk"; 207 HP). Meleed Grip; died at t10997. | Recall | With recall0 the Borg reads Recall at t10394 and lives (see counterfactuals). |
| 16 | 1315192163 | ctl | Human Priest | 2 | 1 | a floating eye | A stair flow passed a **floating eye** (paralysed at t67431). Freed at HP 13/19, it chose **melee on the eye** ("attack type 1 with value 604") over Phase. The Phase rule said "danger 0 without fear". Paralysis lock; died at t67731. | Phase ×12, CSW ×2 | Phase Door or step away; never melee a paralysing gazer without Free Action. |
| 17 | 1308765461 | bfs0 | Hobbit Priest | 1 | 1 | a grey mold | Read Recall at t9758, then walked a 75-step stair flow that passed beside a **grey mold** at HP 8/10 (spores). Minor Healing failed; died at t9907, before the Recall acted. | Phase ×8 | Stay put (or Phase) while the Recall counts down. |
| 18 | 2063715385 | bfs0 | Half-Elf Priest | 2 | 1 | a white worm mass | "Breeders: 5 known … the level is lost"; a worm blocked the stairs. A floating eye paralysed it among the worms (t4698). Died at t4773. | **CSW ×2, Phase ×6, Speed ×2** | Phase Door out of the worm pocket before the eye. `osc` rescues this game (see counterfactuals). |
| 19 | 1741676259 | bfs0 | Human Priest | 2 | 1 | Fang | Last Phase at HP 6 (t17910). Recall refused (180–330 HP). A 46-step stair flow; cornered, it cast Bless; Fang bit it to HP 1. Died at t18142. | Recall | With recall0 the game diverges at t17128 and lives. |
| 20 | 1136345005 | bfs0 | Dunadan Mage | 3 | 1 | a soldier | Oil at a **soldier**; its last Phase was read at full HP 18 (t13518). The soldier found it again; fight race "winning" (8.4/turn). Two soldier turns took 18 HP. Died at t14129. | **CLW ×7**, oil ×6, Recall | Avoid a level-6 soldier at CL3 (18 HP); one Phase Door is not enough. |
| 21 | 251498236 | bfs0 | Dwarf Mage | 6 | 2 | a soldier | A shrieker hasted a soldier, cutpurses, cave spiders and a white jelly (t26308). At full HP 44 it walked a 6-step "Desperate for Stairs" through them. Phase was refused ("danger 14 without fear", HP 34), and HP went 34 → 3 in three turns. Died at t26387. | **Phase ×4, CLW ×5, Neutralize ×2** | Phase Door (or kill the shrieker first); the damage-only danger ignored the haste. |
| 22 | 344339521 | bfs0 | High-Elf Priest | 3 | 1 | a gallant | A long chase by a **gallant**: 3 Phase Doors, "Resting to gain Mana" with it near, stair flows of 25–41 steps at HP 11–21/40. Died at t44518. | Recall only | (Inference) Out-matched at CL3; Recall was never read. |
| 23 | 1004587769 | bfs0 | High-Elf Necromancer | 5 | 2 | a wild cat | **Disarmed a gas trap** (t66970) with a wild cat nearby; paralysed and killed. Died at t67045. | full kit (CLW ×19, Phase ×18, …) | Do not disarm (walk around) with an awake monster in reach and no Free Action. |
| 24 | 1350161869 | bfs0 | Hobbit Druid | 3 | 1 | a giant white mouse | Breeding mice. It was **confused**, so it could not read its 2 Phase. It meleed a 1-HP mouse and swung into the granite ("You chip away futilely"). Recall was refused 230 times (borg-reborn-rs#758) and was unreadable anyway. Died at t20059. | Phase ×2, no cure | Leave the breeder level earlier; it had 0 CLW (8 drunk earlier). |
| 25 | 1575424768 | bfs0 | Hobbit Druid | 2 | 1 | a crow | A fast-fragile crow, then the last Phase (t13831) landed beside a **floating eye**. It quaffed a CLW to full, then **meleed the eye** ("attack type 1 with value 601"). Paralysed; the crow killed it at t13879. | CLW ×4, Speed, Recall | Never melee a paralysing gazer; step away from the eye. recall0 reads Recall at t13494 and lives. |

## Poison

### The engine (574b618c, as built at 1c071812)

- **Damage and regeneration.** Poison deals 1 HP each world tick (10 game turns at normal speed) through `take_hit` (game-world.c:513-519). It also stops HP regeneration entirely (player-util.c:468).
- **How the counter falls.** It drops by `adj_con_fix[CON] + 1` per tick (game-world.c:317-320). In these 7 games `state.log` shows 1 per tick. So the remaining counter is, to first order, the HP the poison will still take.
- **How it grows.** Each poisoning blow adds `5 + 1d(monster level)` (mon-blows.c:683-684).
- **What cures it.** Among potions, only **Cure Critical Wounds** and **Neutralize Poison** cure it (object.txt). Cure Light Wounds (heal 20) and Cure Serious Wounds (heal 40) do not. The other cures are the Druid's **Cure Poison** (CL4, 4 mana, in [Gifts of Nature], base cost 400, always stocked by the Bookseller), the Ranger's Herbal Curing (CL9), Priest/Paladin Healing (CL30) and some foods and mushrooms.
- **Town stock.** The Alchemist *always* stocks Cure Light Wounds, Phase Door and Word of Recall. Neutralize Poison, CSW and CCW are only *normal* stock (store.txt), so they are not always on the shelf.

### The sources

`state.log` logs the exact counter (timed index 7). That gives each game's last poisoning episode:

| seed | arm | source | poison at start → peak | HP at peak | poison first ≥ HP | cures drunk in the episode | gold | poison when it died |
|---:|---|---|---|---|---|---|---:|---:|
| 799968561 | ctl | white jelly (meleed) | 4 → 190 | 15/21 | t21894 (15 vs 11) | CLW ×11 | 53 | 108 |
| 626789725 | ctl | blubbering icky thing (crawl) | 5 → 28 | 12/15 | t27230 (12 vs 12) | CLW ×3, CSW ×1 | 9 → 0 | 7 |
| 956247604 | ctl | white jelly (meleed) | 7 → 110 | 35/47 | t87012 (32 vs 29) | CLW ×6 | 250 → 171 (stolen) | 14 |
| 1575381233 | ctl | white worm masses (meleed) | 6 → 14 | 29/45 | t91956 (12 vs 10) | CLW ×1 | 460 | 2 |
| 727698927 | bfs0 | white jelly (meleed) | 0 → 284 | 16/57 | t61592 (40 vs 39) | CLW ×5 | 644 | 236 |
| 1200156945 | bfs0 | blubbering icky thing (tamer's pack) | 0 → 13 | 10/49 | t92040 (13 vs 10) | none | 0 | 10 |
| 1902932078 | bfs0 | white worm masses (meleed) | 4 → 8 | 18/58 | t53091 (4 vs 1) | CLW ×1 | 120 | 2 |

Three monsters, all shallow:

| monster | depth | speed | HP | poisoning blow | moves? |
|---|---:|---:|---:|---|---|
| white jelly | 2 | +10 | 36 | `TOUCH:POISON:1d2` | `NEVER_MOVE` |
| white worm mass | 1 | -10 | 10 | `CRAWL:POISON:1d2` | erratic (`RAND_25 \| RAND_50`), `MULTIPLY` |
| blubbering icky thing | 2 | +0 | 18 | `CRAWL:POISON:1d4` | moves |

Two different deaths share the cause "poison":

- **Poison bleed-out (3: 799968561, 727698927, 956247604).** All three meleed a white jelly while the counter climbed far past the HP (190, 284, 110). They drank Cure Light Wounds, which heals but leaves the counter, and the jelly added 6–7 turns per touch. After the poison passed HP + the healing in the pack, nothing but a cure could save them.
- **Poison as the last tick of an attrition loss (4: 626789725, 1575381233, 1200156945, 1902932078).** The counter stayed small (≤ 28), but it kept regeneration at 0 while the Borg kept fighting or oscillating beside breeders or a pack. The 1 HP tick happened to be the last hit. The Rogue 626789725 sits between the two: its counter (21) exceeded its HP (14) when it reached town with 9 gold.

### How it was handled

- **Cure potions.** None of the 7 drank a poison cure. Four drank CLW/CSW against the poison: 26 CLW/CSW in total in the episodes above: 799968561 11, 626789725 4, 956247604 6, 727698927 5. That heals but leaves the counter running.
- **Neutralize Poison was held only by the Paladin 1200156945** (2, plus 10 CLW). It drank none, because its final fight ran at danger 46–89 against an avoidance (HP) of 8–19. Every cure in `borg_heal` is skipped while danger > avoidance × 2/10 (borg_caution.rs:721, "Dont do these in the middle of a fight").
- **Recall.**
  - Four games (956247604, 1575381233, 727698927, 1902932078) logged "Flight Recall forecast: 34 poison HP included (#880)" followed by "Refusing flight Recall … (#758)".
  - Once poisoned, the forecast charges all 34 ticks of the Recall delay as poison (`recall_poison_hp`, borg_caution.rs:3139-3145), whatever the counter is. In 1575381233 the counter was 6–14 at those refusals, so the forecast over-charged by about 20–28 HP.
  - The refusals there also stood on contact exposure alone (44–60 HP against HP 22–24 without poison). So the over-charge was not decisive in this game.
  - In 727698927 the counter (≈ 280) was far *above* the 34 charged, and Recall could not have saved it at that point.
- **Stairs.**
  - "Leaving/Fleeing (bleeding/poison)" (borg_caution.rs:4226-4235) needs HP < MAXHP / 2 and a 25% roll.
  - The Ranger 956247604 reached DL1 with poison 82 at HP 37/47, above half. So no flight fired, and it explored DL1 for 54 player turns. When it fired (HP 13) it was too late.
- **Town.**
  - Two of the 7 reached town poisoned: 799968561 (53 gold, poison 162 at HP 29) and 626789725 (9 gold, poison 21 at HP 14).
  - Both were already lost there: neither could afford Neutralize Poison (base 75), and CLW (base 20) was out of the Rogue's reach.
  - The town planner did what its rules say:
    - `Need::Poison` is urgent only for an item that *cures* poison (borg_town_usefulness.rs:131);
    - no rule buys CLW to outlast a counter;
    - the Borg cannot rest while poisoned (borg_recover.rs:536, 569, 642).
  - So 799968561 spent its last turns selling and dropping junk at the Alchemist while the counter ran.
- **The Druid's own cure.**
  - Four of the 7 are Druids at CL4–7, the level of **Cure Poison** (CL4, 4 mana, 30% fail), but none owned [Gifts of Nature].
  - None was ever in town at CL ≥ 4 with the book's base cost of 400 in gold. Gold at those visits was 53 (799968561), 5 (1575381233) and at most 268 (1902932078); 727698927 never returned at CL ≥ 4.
  - The two that died with 460 and 644 gold earned them after their last visit.

### What the potion and cure logic knows about poison

- **Perception.** The Borg holds poison as a flag, `BI_ISPOISONED` (borg_trait.rs:2851-2853), set from the engine timer through `engine::player_timed`. The amount is read in one place only: the town planner's poison demand (borg_town_capability.rs:1018-1019). Nothing parses "You are more poisoned!". The borg-reborn-rs#934 issue and borg_caution.rs:2320 record the choice: "The screen shows one grade, 'Poisoned', so the amount is not used".
- **What counts as a poison cure.** These are right everywhere they are asked:
  - `has_poison_cure` (borg_caution.rs:2345): Neutralize Poison, CCW, Healing, *Healing*, Life and the two spells;
  - the fast-fragile `dot_cure` (borg_fast_fragile.rs:237-246);
  - the town's `Need::Poison`: Neutralize Poison and CCW, never CLW/CSW.
- **Where CLW/CSW are still treated as poison remedies.**
  - The pack value gives CSW a "Reward Cure Poison and Cuts" bonus while poisoned (borg_power.rs:1172-1183).
  - The poison *critical* check drinks CLW/CSW "to buy time" below HP 2 or MAXHP/20 (borg_caution.rs:788-793).
  - Neither is a cure claim, but neither weighs the counter.
- **When a real cure is drunk.**
  - In `borg_heal`, only while poisoned *and* HP < MAXHP/2 *and* danger ≤ 20% of avoidance (borg_caution.rs:721-727).
  - In `borg_recover`, on a 25% roll for the costly cures (Neutralize Poison, CCW with HP < 10).
  - `borg_quaff_crit` keeps the last 2 CCW (`item_use_ccw_min_stock`) except in the emergency path.
- **What is not modelled anywhere.**
  - That a poison counter larger than HP + carried healing is fatal without a cure.
  - That every touch of a poison-toucher adds 5 + 1d(level) to it.
  - The danger the Phase rule reads (`escape_phase_lost_damage_only = 1`) prices poison only as a *fear* term (`danger_monblow_poison_fear`), and the damage-only scope zeroes it. To the Phase gate a white worm mass or jelly is 2–6 danger, whatever the counter.
- **Switches already written for the white-jelly case (borg-reborn-rs#931–borg-reborn-rs#934, borg-reborn-rs#1023, borg-reborn-rs#964)** all ship 0, as does `caution_ranged_vs_immobile` (owner, 2026-11-20: "stepaway flag is not a solution"). borg-reborn-rs#934 (`caution_poisoned_no_cure_retreat_hp_percent`) acts only before a *retreat*. In these 25 games it changed no key (all 25 plays identical), because the Borgs were meleeing, not retreating.

## Counterfactuals

**Method.**
- Each of the 25 deaths was replayed from birth at 1c071812 with the recorder build: same seed, same race and class, the bundle's own `user/` files, and only the named `borg_param_*` lines changed.
- Without changes, all 25 deaths and an 18-game survivor sample reproduce the zoo's `play_sha256` exactly.
- A changed game is classed by where its key stream first departs from the original:
  - **near** = within 2,000 game turns of the original death, i.e. at the fatal episode;
  - **early** = before that.
- An early divergence that lives is a *different game*, not a rescue of this death. It counts only as noise in both directions.
- A death bank is a chosen sample: the zoo already found that rescues on chosen death starts did not carry over to fresh starts (borg-zoo#429, borg-zoo#501).

| arm | settings |
|---|---|
| p934 | `caution_poisoned_no_cure_retreat_hp_percent = 75` (borg-reborn-rs#934) |
| flee100 | `caution_flee_status_chance = 100` |
| flee1 | `caution_flee_status_hp_divisor = 1`, `caution_flee_status_chance = 100` (leave whenever poisoned or cut below full HP) |
| osc | `caution_retreat_oscillation_limit = 3`, `caution_retreat_oscillation_backaway = 1` (borg-reborn-rs#932, borg-reborn-rs#1023) |
| bundle | p934 + flee100 + osc |
| conf | `caution_confused_clw_cure = 1` (borg-reborn-rs#837) |
| phase50 | `escape_phase_lost_danger_percent = 50` (shipped 100) |
| phasefear | `escape_phase_lost_damage_only = 0` (shipped 1, borg-reborn-rs#878) |
| recall0 | `caution_recall_survival = 0` (shipped 1, borg-reborn-rs#758) |

| seed | arm | killer | p934 | flee100 | flee1 | osc | bundle | conf | phase50 | phasefear | recall0 |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 727698927 | bfs0 | poison | = | = | l | = | = | l | = | l | = |
| 1200156945 | bfs0 | poison | = | = | = | = | = | l | **L** | l | = |
| 1902932078 | bfs0 | poison | = | = | = | d | d | = | D | l | = |
| 626789725 | ctl | poison | = | D | D | = | D | = | **L** | l | = |
| 799968561 | ctl | poison | = | = | D | = | = | = | d | = | l |
| 956247604 | ctl | poison | = | D | l | l | l | = | l | l | l |
| 1575381233 | ctl | poison | = | = | l | = | = | = | D | D | l |
| 251498236 | bfs0 | a soldier | = | = | = | = | = | **L** | l | l | = |
| 344339521 | bfs0 | a gallant | = | = | D | = | = | = | **L** | l | = |
| 1004587769 | bfs0 | a wild cat | = | = | l | = | = | = | = | = | l |
| 1136345005 | bfs0 | a soldier | = | = | = | = | = | l | l | l | l |
| 1308765461 | bfs0 | a grey mold | = | = | = | = | = | = | = | = | = |
| 1350161869 | bfs0 | a giant white mouse | = | = | = | = | = | = | d | l | l |
| 1575424768 | bfs0 | a crow | = | = | = | = | = | = | = | = | **L** |
| 1741676259 | bfs0 | Fang, Farmer Maggot's Dog | = | = | = | = | = | = | **L** | = | **L** |
| 2063715385 | bfs0 | a white worm mass | = | = | = | **L** | **L** | = | = | D | = |
| 220674435 | ctl | a fatal wound | = | = | = | = | = | = | = | l | = |
| 389489263 | ctl | Fang, Farmer Maggot's Dog | = | = | = | = | = | = | **L** | = | = |
| 500978646 | ctl | Grip, Farmer Maggot's Dog | = | = | = | = | = | = | = | = | l |
| 965142510 | ctl | a floating eye | = | = | = | = | = | l | = | = | = |
| 1308765461 | ctl | Grip, Farmer Maggot's Dog | = | = | = | = | = | = | = | = | **L** |
| 1315192163 | ctl | a floating eye | = | = | = | = | = | = | l | **L** | = |
| 1397430180 | ctl | a cutpurse | = | = | = | = | = | = | = | = | = |
| 1520819173 | ctl | a crow | = | = | = | = | = | **L** | = | = | = |
| 1896645817 | ctl | a giant white mouse | = | = | = | = | = | = | D | **L** | = |
| **L** | | lives, diverged ≤ 2,000 game turns before the death | 0 | 0 | 0 | 1 | 1 | 2 | 5 | 2 | 3 |
| D | | still dies, diverged near | 0 | 2 | 3 | 0 | 1 | 0 | 3 | 2 | 0 |
| l | | lives, diverged earlier | 0 | 0 | 4 | 1 | 1 | 4 | 4 | 10 | 7 |
| d | | dies, diverged earlier | 0 | 0 | 0 | 1 | 1 | 0 | 2 | 0 | 0 |
| = | | identical play | 25 | 23 | 18 | 22 | 21 | 19 | 11 | 11 | 15 |

**Survivor sample.** 18 games that lived to the cap: one per class per arm-of-origin, the lowest seed that died in neither arm. Each was replayed with the arms above.

| arm | plays changed (of 18) | deaths (of 18) |
|---|---:|---:|
| none (shipped) | 0 (all 18 match the zoo's `play_sha256`) | 0 |
| phase50 | 1 | 0 |
| osc | 5 | 0 |
| conf | 8 | 0 |
| recall0 | 9 | 0 |
| phasefear | 11 | 0 |

Zero deaths in 18 games bounds nothing tight: at a 1.4% base death rate, 18 games would show about 0.25 deaths. The sample only shows that no arm is grossly harmful; the zoo measures the rest. The p934, flee100, flee1 and bundle arms were not run on survivors.

## Proposals

Ranked by deaths addressed **at the fatal point**, then by risk. A setting is a candidate for a zoo arm, not for shipping: nothing here is a claim until the zoo measures it (RULES 14).

### Settings (harness/borg.txt)

| rank | change | deaths addressed at the fatal point (counterfactual **L**) | near, still dies | survivors changed / killed | risk |
|---:|---|---|---|---|---|
| 1 | `borg_param_escape_phase_lost_danger_percent = 50` (from 100) | 5: 626789725 (poison), 1200156945 (poison), 344339521, 389489263, 1741676259 | 3: 1575381233 (lives 6,000 turns longer), 1896645817 (dies earlier), 1902932078 (dies later) | 1 / 0 | **Medium.** The owner's borg-reborn-rs#584 rule stays; only its threshold moves. The rule was confirmed at 100 (borg-zoo#347: 89 against 128 deaths), and 150 was worse than 100 (medium: 12 against 8). Below 100 was never measured. Since then `escape_phase_lost_damage_only = 1` (borg-reborn-rs#878) shrank the danger the gate reads (for a worm mass 2 instead of 32), which made the same 100 much stricter. Costs Phase Doors. |
| 2 | `borg_param_caution_confused_clw_cure = 1` (from 0) | 2: 1520819173 ("Fixing Confusion. Level 2" at t1431, where the original rested confused), 251498236 | 0 | 8 / 0 | **Low–medium.** The trigger is narrow (confused, with CLW in the pack), but it changed 8 of 18 survivor plays. The engine fact is direct: CLW `TIMED_DEC:CONFUSED` 20, and confusion blocks reading (player-util.c:1182). |
| 3 | `borg_param_caution_retreat_oscillation_limit = 3` + `borg_param_caution_retreat_oscillation_backaway = 1` | 1: 2063715385 | 0 near; 1902932078 diverged earlier and still dies. There the breaker fired, then the Phase rule refused Phase ("danger 2 without fear") and the worms killed it. | 5 / 0 | **Low.** Already in borg-zoo#712's jelly worlds. On its own it does not fix the worm pocket; with rank 1 it might. |
| — | `borg_param_caution_recall_survival = 0` (from 1) | 3: 1308765461 ctl, 1575424768, 1741676259 | 0 | 9 / 0 | **High: not proposed as a setting.** It reverts the owner's borg-reborn-rs#758 decision ("It really reads recall too often"), and borg-reborn-rs#758's own deaths (Recall read beside a killer) would come back. Use the code change C4 instead. A zoo arm only if the owner wants the number. |
| — | `borg_param_escape_phase_lost_damage_only = 0` (from 1) | 2: 1315192163, 1896645817 | 2: 1575381233, 2063715385 | 11 / 0 | **Medium-high, not proposed.** It changes 11 of 18 survivor plays (a broad change) and reverses borg-reborn-rs#878 (the Mage 461220874 worm case). Rank 1 reaches more deaths with fewer changed survivors. |
| — | borg-reborn-rs#934 `caution_poisoned_no_cure_retreat_hp_percent = 75`; `caution_flee_status_chance = 100`; `caution_flee_status_hp_divisor = 1` | 0 | flee100 2, flee1 3 | — | **No effect here.** borg-reborn-rs#934 acts only before a retreat; these Borgs were meleeing. The status flight fires, but too late to matter. |
| — | `caution_ranged_vs_immobile = 2` | not run | — | — | **Owner rejected it (2026-11-20).** borg-zoo#461 lost games with it. |

The borg.txt lines for a zoo arm (not for shipping before the zoo says so):

```
borg_param_escape_phase_lost_danger_percent = 50
borg_param_caution_confused_clw_cure = 1
borg_param_caution_retreat_oscillation_limit = 3
borg_param_caution_retreat_oscillation_backaway = 1
```

### Code

Each would sit behind a switch shipped 0 (house practice).

| rank | change | deaths it addresses (from the logs; *inference* where marked) | risk | existing issue |
|---:|---|---|---|---|
| C1 | **Pending poison in the fight and escape tests.** Keep a pending-poison figure: the engine counter / (`adj_con_fix` + 1). If the owner keeps the screen-only perception, estimate it from "You are poisoned/more poisoned!" × (5 + level/2) less decay, as borg-reborn-rs#1083 proposes. Count it in the Phase rule's "fight lost" test, and stop meleeing a poisoner when pending poison ≥ HP + the HP the pack's CLW/CSW can restore. | 799968561, 727698927, 956247604 (the jelly bleed-outs: the counter passed HP at t21894, t61592, t87012 with the poisoner still adjacent); 626789725, 1200156945 (phase50 rescues both, *inference*: an earlier Phase from the same gate); 1575381233, 1902932078 (Phase refused at "danger 2" beside worms) | Medium: touches the Phase gate. | borg-reborn-rs#1083 (open, in progress); borg-reborn-rs#928 |
| C2 | **A real cure beats the 20% danger gate.** When pending poison ≥ HP (C1), drink Neutralize Poison / CCW / Cure Poison even while danger > avoidance × 2/10 (borg_caution.rs:721), and override `item_use_ccw_min_stock`. | 1200156945 (2 Neutralize Poison, 10 CLW unused; *inference*: the poison there was small, its fight was lost on HP) and every future jelly Borg that carries a cure | Low | borg-reborn-rs#985, borg-reborn-rs#710 |
| C3 | **Paralysers (borg-reborn-rs#1125).** No melee on a monster with a PARALYZE gaze/blow without Free Action. Its danger is never "0 without fear", so Phase or step away is allowed. | 1315192163 (melee value 604), 1575424768 (melee value 601). Not 965142510, where the eye was never seen before it gazed. | Low | borg-reborn-rs#1125 (open), borg-reborn-rs#1132 |
| C4 | **A two-sided Recall check.** Refuse a flight Recall only when the alternative the Borg will take (the stair walk at its distance, or the fight by borg-reborn-rs#759's race) is modelled as safer than the Recall delay. Cap the poison it charges at the counter: `min(counter / decay, 34)` instead of 34. | 1308765461 ctl, 1575424768, 1741676259 (recall0's near rescues); *inference*: 500978646 | Medium: borg-reborn-rs#758's cases must stay fixed. | borg-reborn-rs#758 (closed), borg-reborn-rs#880 |
| C5 | **Poisoned flight goes to town.** Replace "Leaving (bleeding/poison)"'s HP < MAXHP/2 and 25% roll with pending poison ≥ HP + carried healing. Once fleeing for a cure, keep climbing: no exploring DL1. | 956247604 (reached DL1 with poison 82, HP 37/47, 171 gold, then explored for 54 player turns) | Low–medium | — |
| C6 | **Town triage when poisoned.** On arrival with pending poison ≥ HP: buy and drink Neutralize Poison or CCW if stocked and affordable, else enough CLW to outlast the counter (CLW is always stocked), before any sale or drop. `Need::Poison` today needs a *cure*, and a carried CCW held back by the stock floor cancels it. | None in this run: both town arrivals were broke (53 and 9 gold). With C5, 956247604 (171 gold). | Low | — |
| C7 | **The Druid's Cure Poison.** Value [Gifts of Nature] as a poison cure for a Druid at CL ≥ 4 (it gives `poison_cures` + 1000) and allow a town trip for it once gold ≥ its price. | 4 of the 7 poison deaths are Druids at CL4–7, but none was in town at CL ≥ 4 with ≥ 400 gold. *Inference*: it prevents later deaths, not these. | Low | — |
| C8 | **No disarm with an awake monster in reach** (gas, paralysis) without Free Action: walk around. | 1004587769 | Low | — |
| C9 | **No long walks while Recall counts down** past known never-moving attackers; rest or Phase instead. | 1308765461 bfs0 (grey mold: Recall read at t9758 acts 15–34 player turns later, t9908 at the soonest; it died at t9907) | Low | borg-reborn-rs#582, borg-reborn-rs#583 |
| C10 | **No study or pickups at low HP with an enemy adjacent.** | 1896645817 (studied at HP 4/26 surrounded), 389489263 (picked up copper at HP 1 and 0) | Low | — |

## Investigations still open

1. **Why the Paladin 1200156945 drank nothing.** It had 10 CLW and 2 Neutralize Poison, and fell HP 19 → 10 → 8 at danger 89/46/32 against avoidance 19/10/8. The trace shows only attack candidates. *Inference*: `borg_heal` skips cures above 20% of avoidance (borg_caution.rs:721), and no heal level fired with danger far above HP. Needs a decision trace of `borg_heal` per think. Related borg-reborn-rs#985 (the bravery boost overrides every cure; 1575381233 logs "Boosting bravery (2) from 1 to 220!" at HP 1).
2. **Why the Ranger 956247604 kept meleeing the jelly** under "Fleeing and leaving the level (scaryguy)" ("attack type 1", value 13 seven times and 12 once, keys 10294–10330). The flight did not move it.
3. **The fight race against a soldier.**
   - 220674435 was "winning" at HP 28 against a soldier modelled at 7.1 damage/turn; it took 15 in one turn.
   - 1136345005 was "winning" at HP 18 (8.4/turn).
   - A soldier's 2 × 1d10 has a long tail at these HP. Check borg-reborn-rs#759's race against the blow maximum when HP is low.
4. **Unseen floating eyes.**
   - 965142510 walked a dark-bfs flow beside an eye it never saw before the gaze.
   - 1315192163's stair flow passed one.
   - Check light radius and the flow's unknown-grid cost (borg-reborn-rs#881, borg-reborn-rs#1132).
5. **Stair dither.**
   - 956247604 stood on a down staircase five times in its last 100 game turns (t87962–t88042) while "Looking for Up Stair", and never took it.
   - 799968561, in town, re-entered the Alchemist three times at HP 6/32 to sell junk.
6. **Recall's poison charge.** 34 HP whatever the counter (`recall_poison_hp`). In 1575381233 the counter was 6–14 when charged 34. Not decisive in this run (C4).
7. **Druid books.** How often does a Druid reach CL ≥ 4 with ≥ the price of [Gifts of Nature] in town? Use the zoo cells' milestones (gold by CL) to size C7 before building it.
8. **Breadth-first on/off** (the experiment's own question, for completeness).
   - Deaths: 13 ctl, 12 bfs0, with one start dying in both (1308765461).
   - Poison: 4 ctl, 3 bfs0.
   - Nothing in these 25 deaths points at the exploration order.
   - One link: 727698927's retreat from the jelly was undone by the next flow ("dark-3"). That is the borg-reborn-rs#928 / borg-reborn-rs#1125 pattern under either order.

## Test plan

1. **Decision tests (borg-core, no engine):** one per code change, as borg-reborn-rs#1091 does for the immobile-toucher switches.
   - C1:
     - the pending-poison estimate from a message sequence;
     - the Phase gate allowing Phase at "danger 2" when pending poison ≥ HP;
     - no melee on a poisoner when pending poison ≥ HP + carried healing.
   - C3: no melee on a PARALYZE gazer without `BI_FRACT`.
   - C4: `recall_poison_hp` capped at the counter; Recall not refused when the alternative's exposure is higher.
   - C6: `urgent_needs` buying CLW for poisoned and broke-for-a-cure.
2. **Replay bank (local, minutes).**
   - Inputs:
     - the 25 deaths here;
     - 829474344 (borg-reborn-rs#934, borg-reborn-rs#1083);
     - 453254028 (borg-reborn-rs#1125).
   - Play each from birth at the candidate commit, once per arm, with the scripts in this study's `tools/`.
   - Report:
     - rescues at the fatal point (divergence ≤ 2,000 game turns before the death) apart from early divergence;
     - an 18-game survivor sample for deaths introduced (on chosen starts, harm shows only weakly).
   - This is a mechanism check, not a measurement.
3. **Worlds (zoo, pilot):** the existing jellies-x4/x8, white-worm-mass-x4 and breeders-x4 worlds (borg-zoo#712, borg-zoo#692), for C1/C2/C5 and the poison-specific arms, where poisoners are dense enough to see an effect.
4. **Normal world (zoo), tiers in order (RULES 14).**
   - Pilot (classes-18) as the gate.
   - Then verysmall (starts 1-45), small-rest, medium, big, full; the owner dispatches each.
   - Primary endpoint: deaths by 100,000 turns, paired exact McNemar against ctl.
   - Secondary endpoints:
     - poison deaths;
     - deaths at CL ≤ 3;
     - Phase Door reads and CLW quaffs per game;
     - Recall reads;
     - starts reaching DL3/DL5;
     - mean final CL.
   - The settings arms are defined in the definition PR. The code arms follow when the switches exist.
5. **Before any ship:** re-record `smoke-borg-rs` (`scripts/rerecord-smoke-borg-rs.sh`) in the same PR, as AGENTS.md requires for a change to how the borg-rs core plays.
