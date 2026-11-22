# Human Mage 461220874: poisoned by one white worm mass it retreated from instead of killing, borg-reborn-rs da097a76

- **Source:** borg-zoo `reborn-confusion-837-medium`, run 44936494812, suite `classes-1800-medium`,
  specimen `4.2.6-reborn-rust-confusion-da097a76` (borg-reborn-rs `da097a76`, main 12c4ce7c plus #837).
- **Core:** the vendored **borg-rs core** (`borg-core/`): the cell's `requested_profile_settings` say
  `borg_reborn_core: borg-rs` (not `BORG_CORE=reborn`).
- **Arm:** `reborn-confusion-csw` (`caution_confused_clw_cure 1`, `town_confusion_cure_reserve 1`). The same start
  **reached the 100,000-turn cap at CL6–7** in the run's `ctl`, `clw_walk` and `stuck` arms (other key streams).
  The csw arm changed the town purchases, and after that the game took a different path. This is one life, and the
  other arms are not rescues of it.
- **Outcome:** died of **poison** on DL1 at game turn 18,520, key 2,167, CL3, HP 20 max, SP 0/5, 393 gold, 0 Phase
  Door and 0 Cure Light Wounds left.
- **Reproduction: verified.** Built locally at da097a76 (`BORG_IMPL=rust harness/build.sh`), then played with the
  cell's own `user/borg.txt` (sha256 `0cb0b9f9…`). The keys.log sha256 is `d8a39edf…434d`, which equals the cell's
  `play_sha256`. `runs/replay-zoo-death.sh runs/2026-11-22-reborn-confusion-csw-mage-461220874/replay/461220874`
  replays it. The logs in [replay/461220874/](replay/461220874/) come from that pristine build.
- **Dossier:** no `D-…` dossier yet. This session could not download the run's `deaths-*` artifacts: the proxy
  refuses the artifact blob host. `python3 scripts/import_zoo_deaths.py --run 44936494812` from a machine that can
  reach it imports the run's 22 deaths (RULES 12); this page then links the dossier.

Columns of messages.log: key, game turn, message type, text. Borg notes give `(y,x)`; state.log gives `x,y`.

## What happened

| key | turn | what (messages.log / state.log) |
|---|---|---|
| 1461 | 15042 | "The white worm mass wakes up." Mage at (7,73) in a dark corridor, worm at (7,72), adjacent. HP 20/20, SP 5/5, 16 CLW, 3 Phase Door. |
| 1462 | 15047 | `Danger:p=32`. The core trace (think 938) ranks **Magic Missile first** (utility 50, weighted 100, ahead of throw 34 and melee 31), but `borg_caution` acts before the attack step: "Retreating to 7,74 (distance 1) via 7,74 (32 > 1)". |
| 1463 | 15057 | "There was a monster 'white worm mass' at (7,72)", then "Forgetting" it, two grids away. With the worm forgotten, the Borg "Flowing toward dark-2" walks straight back to (7,73). |
| 1464 | 15062 | "The white worm mass crawls on you. You are poisoned!" HP 18. |
| 1465 | 15067 | Re-created at (7,72). "Phase rule (from escape 1 emergency): enemy adjacent and the fight looks lost (danger 32, HP 18)". **Phase Door read** (2 left). |
| 1478–1512 | 15147–15487 | "No rest: 1 breeders known on the level, leaving", while "Bored but unable to flow to up stairs" (none known yet). It neither rests nor leaves. |
| 1588–1603 | 15899–15939 | "You hit something" (an unseen monster, (9,45) "occupied"). Oil thrown 3 times at the grid, then **Phase Door (unseen bump)** at "danger 1, nearest awake monster 28" (1 left). |
| 1623 | 16071 | **Phase Door (unseen bump)** again at HP 20/20, "danger 0" (0 left). |
| 1695–2046 | 16711–17951 | It now fights: 19 Magic Missile casts, **9 white worm masses destroyed**. SP reaches 0 at 17181 and **never recovers**, because it never rests. 11 of the casts are the C Borg's *reserve spell* at 0 SP ("Emergency use of an Attack Spell"): 11 × "You faint from the effort!" / "You are paralysed!", 4 × "You have damaged your health!". 15 CLW quaffed between 16811 and 18381. |
| 2118–2167 | 18291–18520 | Death loop, every 2–3 keys: worm adjacent → "Retreating … (32 > 1)" one step → worm now 2 grids away in the dark → "Forgetting" → "Flowing toward up-stairs … Stair hugging" (the stairs lie past the worm) → adjacent again → crawl, more poison. HP 17 → 7 → 3 → −1. The last worm had 3 HP. |

## The questions

### 1. Where danger 32 comes from

`borg_danger` (borg-core/src/borg_danger.rs, at da097a76) for the one worm at distance 1, CL3, speed +0:

| step | value | source |
|---|---|---|
| blow CRAWL:POISON 1d2 → `z = dice × sides` | 2 | monster.txt:688; borg_danger.rs:232–233 |
| + poison "fear" (`danger_monblow_poison_fear`, 10) | 12 | borg_danger.rs:242; C borg-danger.c:136–137 |
| full damage: hit chance not applied (`full_damage` forced true) | 12 | borg_danger.rs:2639 |
| monster moves: speed 100 → energy 5, player 110 → 10 (game-world.c:80–81); `q = 5` → rounded to 10, floor 10 | ×1 | borg_danger.rs:2177, 2196 |
| breeder below CL20: `v1 += v1 × 15/10` (comment says "extra 50%", the code adds **150%**) | 30 | borg_danger.rs:2224–2227; same in C borg-danger.c:2422–2425 |
| regional and monster fear maps | +2 | borg_danger.rs:2617–2627 (inferred: the retreat grid two away scores 1, where the worm itself contributes 0 because `q == 10 && d > 1`, borg_danger.rs:2370) |

**What the engine actually does per player turn:** the worm gets half a turn (energy 5 against 10). On each of its
turns it first tries to breed (one in 8 alone, mon-move.c:1042, 1564). Then it staggers at random 75% of the time
(RAND_25 + RAND_50, mon-move.c:1087–1101, 1571), so it bites about 0.3 times per turn of its own. Each bite does 1d2
and adds `5 + randint1(1)` turns of poison (mon-blows.c:683–684). Poison does 1 HP every 10 game turns
(game-world.c:513–515, 1079–1081) and stops HP regeneration (player-util.c:468). That is **well under 1 HP per
player turn of direct damage, plus about 1 HP per player turn while poisoned**. The Borg's 32 is about 30 times
that. Of the 32, 28 points are fear terms (poison 10, then the 150% breeder bonus on it), not damage.

### 2. Why "32 > 1" chose retreat over Magic Missile

The dungeon think calls `borg_caution` (borg_think_dungeon.rs:796) before `borg_attack` (borg_think_dungeon.rs:889).
In `borg_caution` the strategic retreat (borg_caution.rs:2987) runs when:

- `pos_danger > avoidance / caution_retreat_danger_divisor`, i.e. 32 > 20/3 (borg_caution.rs:2980; C borg-caution.c:1430);
- a happy grid in view where the first step is safe: `p1 = 1 < HP × 4/10 = 8` and `1 ≤ 32 × 5/10`
  (borg_caution.rs:1241–1250, `caution_retreat_step_hp_tenths 4`, `caution_retreat_step_danger_tenths 5`). Grid
  (7,74) scores 1 because `borg_danger` gives a speed-100 monster **zero** danger beyond distance 1
  (borg_danger.rs:2370), which assumes one step away is safe from it;
- `may_move_away` (borg_caution.rs:1885–1904) and its one exception, `borg_adjacent_kill_in_one_blow`
  (borg_caution.rs:1913–1947, better-borg-c I-001). That exception counts only **melee**
  (`borg_thrust_damage_one >= kill.power`, :1942). A Mage's dagger does not kill 10 HP in one blow, so the
  exception never applies to a caster's spell. The breeder stand (`breeder_stand_here`, #503) did not hold either:
  the Borg had Phase Door and so an "easy escape" (borg_caution.rs:3422–3431).

The trace confirms it. At think 938 the attack ranking already had Magic Missile as the winner, and caution acted first.

### 3. Why escape 1 called the fight "lost" at HP 18/20

Shipped `harness/borg.txt` (the same on main f57499d0, lines 882–883) sets `escape_phase_lost_test = 0` and
`escape_phase_lost_danger_percent = 100`. The fight is "lost" when `danger × 100 ≥ HP × 100` (borg_escape.rs:923–930,
951): 32 ≥ 18. The direction of the test is right (more danger than HP means you could die). Its input is wrong:
`danger` is the fear-weighted number above, not damage. Every low-HP character next to any poisoning or breeding
monster fails it. Test 1 (the fight compared) would fail here too, because HP/danger = 18/32 < 1 turn.

Fixing the comparison does not help as long as danger is inflated. The decision has to use a damage estimate.

The same inflated danger also triggers the **reserve spell**. `borg_attack_aux_spell_bolt_reserve`
(borg_fight_attack.rs:3060–3175; C borg-fight-attack.c:2519) casts with faked mana when danger ≥ 2 × HP
(:3094, `attack_reserve_spell_danger_multiplier 2`). That is 32 ≥ 2 × 16 at HP ≤ 16. The engine then sets
SP to 0 and faints the caster for `randint1(5 × oops + 1)` turns, with a 50% chance to drain CON
(player-spell.c:541–553; player-util.c:825–842). That happened 11 times, 4 of them with CON damage, each time
next to a biting worm.

### 4. The forget/re-create flicker: a perception bug, confirmed

Diagnosis: a scratch build of da097a76 adds one `borg_note` in `borg_follow_kill`
([perception/diag-note.patch](perception/diag-note.patch)). Notes do not touch keys or either RNG, and the
instrumented replay's keys.log hash is still `d8a39edf…`. The note records what the game knows about the grid
the Borg "expects" to see.

At key 1463 the game has the worm (midx 19) at (7,72). The square is **not lit**: `square_islit` is false, and the
monster's mflag is 0x2 (ACTIVE only, neither VIEW nor VISIBLE). The player's `cur_light` is 2. The Borg's own grid
info is 0x3d, so it thinks the grid is in view and lit.

The cause is the light radius:

- In 4.2 a Wooden Torch is `LIGHT_2` (object.txt:241), but the game lights `radius = ABS(light) - 1`, i.e. distance ≤ 1
  (cave-view.c:658, add_light :616–646).
- The Borg marks distance 2 as lit whenever `BI_LIGHT >= 2` (borg_cave_light.rs:134 "Radius 2 -- lantern radius";
  C borg-cave-light.c:111–112). The defect is lifted from the C Borg.
- `borg_follow_kill_aux` (borg_flow_kill.rs:609–640) then says the monster "should be visible". When it is not on
  screen, `borg_follow_kill` deletes it (borg_flow_kill.rs:694ff, "C bug 24": every path deletes, nothing moves the
  record).

Over the whole life, 44 of the 50 forget events for white worm masses were this case: the monster still there,
2 grids away, on an unlit grid ([perception/diag-mage.log](perception/diag-mage.log)).

**Did it suppress the attack?** It did not cause the first retreat at key 1462; the danger did. It did cause the
**walk back into contact** at key 1463, and the death loop: each one-step retreat put the worm at distance 2,
the worm was forgotten, and the stair flow walked back next to it. The danger and the light model together make a
ping-pong. In about half of those keys the Borg did not know the worm existed, so it could neither attack nor avoid it.

### 5. Unseen-bump Phase Doors and staying on the level

- **Phase (unseen bump)** at 15939 and 16071 spent the last 2 Phase Doors at danger 1 and 0, HP 18–20, with the
  nearest awake monster 28 grids away. The second read had no bump at all in the preceding keys. They left the Mage
  with no escape when the fight came. They also switched off `breeder_stand`'s "easy escape" in the other direction:
  with no Phase Door the stand rule applied, too late. **Contributed.**
- **"No rest: breeders known, leaving"** (52 times from 15147) kept the Mage from resting, so SP stayed at 0 for the
  last 1,340 game turns and poison blocked HP regeneration. It never left either: first "unable to flow to up
  stairs", later "Stair hugging" toward up stairs that lay past the worm. **Contributed.** It turned a fight it was
  winning (9 worms killed) into one with 0 SP and fainting.
- **Word of Recall** (owner, 2026-11-22: "in this situation a recall was not wrong"). The Mage had none: it read its
  only scroll at key 504, turn 5363, and never bought another (gold at most 393, under `buy_recall_from_gold = 400`).
  The 23 "Refusing flight Recall: unmodelled spell/status risk from 1 reachable monsters" notes (16711–18421) are
  forecasts that run before the scroll check (`flight_recall_survivable(st) && borg_recall(st)`,
  borg_escape.rs:106). They still show a defect. The #758 forecast treats every blow outside
  HURT/ACID/ELEC/FIRE/COLD/NONE as unmodelled (`modelled_blow`, borg_caution.rs:2285–2287), so one 1d2 POISON
  crawl vetoes Recall, which the owner judges a sound exit here. The Priest 399497898 logged 91 such refusals, also
  with no scroll (its last was read at turn 45022).
- **Where csw split from ctl:** at key 30, turn 131, the csw arm buys a Cure Serious Wounds first (the confusion-cure
  reserve), then 6 CLW instead of ctl's 8 CLW. The two games differ from then on (ctl replay: keys `210ffc05…`, the
  cell's hash).
- 15 CLW potions bought by the csw arm only bought time. CLW heals 20 but does not cure poison (object.txt:3156–3172).

### 6. Counterfactual: Magic Missile from turn 15047

The save is the recorded game stopped after key 1461 (`-keys 1461 -save-living-on-stop`). It is at turn 15037, the
corridor step before the worm wakes. The key prefix equals the zoo's keys.log. File:
[counterfactual/start-key1461-turn15037.save](counterfactual/start-key1461-turn15037.save).

Each arm continued with `-load … -keep-load-rng`, the cell's borg.txt plus the arm's lines, to turn 100,000.
**Fresh-Borg memory:** the Borg does not restore its map or monster memory from a save, so even the shipped arm is
a fresh Borg, not the original continuation.

| arm | changes ([diffs](counterfactual/)) | first contact (15047–15057) | end |
|---|---|---|---|
| ship | none | Phase Door at once ("danger 32, HP 20") | cap, CL7 |
| stay | `caution_move_max_hp 0` (no retreat or back-away) | Phase Door at once | cap, CL6 |
| **stayfight** | stay + `escape_phase_lost_danger_percent 1000` | **Magic Missile at 15047 and 15057; "The white worm mass is destroyed" at 15057. HP 20/20, SP 5 → 3, no bite, no poison.** | cap, CL7, DL3 |
| fear | stayfight + `danger_breeder_melee_extra_tenths 5` (danger 18) | as stayfight | cap, CL7, DL3 |

The owner's call checks out: two Magic Missiles, 2 SP, no damage. By the engine, Magic Missile at CL3 is 3d4
(class.txt:211–214, `D = (CL−1)/5 + 3`), mean 7.5, against 10 ± 2 HP (mon-make.c:956–971). It costs 1 SP with
22% base fail, less 3 per level above 1 and the INT adjustment, minimum 5% (player-spell.c:396–428). Five SP is
two to three kills' worth.

The fresh-Borg ship arm also survived, so **this death depends on the path**: the original Borg's memory and
retreat put it in the forget loop, and the fresh Borg's Phase Door at first contact did not. Lives saved are a
question for the zoo, not for this one case (RULES 14, 20).

### 7. Is this a pattern?

- **The same specimen, small tier** (run 44924461733): Dunadan Priest **399497898**, CL6, killed by a white worm
  mass at turn **66,588** in both the `clw_walk` and `csw` arms (the owner's "CL6 priest" is from that run, not 44936494812).
  Local replay of the csw cell: keys sha256 `dde95ceb…` = the cell's `play_sha256` (config in
  [related/399497898/](related/399497898/)). The mechanism differs: a breeder colony fought in melee. It destroyed
  73 worms and was hit 84 times, with 97 retreats and 27 back-ups, 8 Phase Doors and 91 "Refusing flight Recall".
  At the end the stairs were "not reachable: white worm mass in the way". Only 3 of its 258 follow-deletes were
  the unlit-distance-2 case: its rooms were lit ([perception/diag-priest.log](perception/diag-priest.log)). It shares
  the inflated breeder danger that triggers retreat and back-away, not the light bug.
- In the same specimen's three runs (pilot, small, medium), 4 of 30 deaths are white worm mass or poison: the Mage,
  the Priest twice (one life) and a Ranger (129607500, "poison", `stuck` arm, not examined).
- Across every reborn cell on the zoo's results branch, 1,478 of 20,203 deaths (7.3%) have the cause "a white worm
  mass" or "poison". In the recent runs (flight-fixes, head, immobile2-head, tonight, confusion) it is 10 of 136.
  These are descriptive counts over different builds and suites, not a rate comparison.
- Earlier cases: D-4c54abc984 (Human Priest 809881907, CL6, flight-fixes), borg-reborn-rs#675 (Blackguard in a
  yellow worm mass colony), #503/#544/#556 (breeder stand and exit rules).

## The rule this case suggests (hypothesis, RULES 14)

None of this is measured. The candidate values below come from this case and from the engine; borg-zoo has to
measure every arm before any of it ships.

1. **Attack on sight, a caster against a lone slow monster.** Before `borg_caution`'s retreat, back-away and the Phase
   rule: if exactly one awake monster is within `R` grids (candidate 1–3), it is not faster than the Borg, and the
   Borg's best ranged attack is expected to kill it within `N` casts that its current SP pays for (fail rate
   included, as `escape_phase_lost_mana` already computes), then attack. Candidates: `N ≤ 3`, and expected damage
   taken over those turns, from blows (dice × hit chance × monster moves, no fear terms), below `X%` of current HP
   (candidate 25–50%). This is the spell counterpart of `borg_adjacent_kill_in_one_blow` (I-001), which today
   counts melee only.
2. **Decide on damage, not fear.** The Phase rule (`escape_phase_lost_test`) and the reserve spell
   (`attack_reserve_spell_danger_multiplier`) should compare HP with an expected-damage estimate that leaves out
   `danger_monblow_*_fear` and the breeder and friends bonuses. The fear terms can stay for whether to engage at all.
   Separately: `danger_breeder_melee_extra_tenths = 15` is +150%, though its comment says 50% (C has the same
   mismatch). Candidate arms: 5 and 15.
3. **No reserve-spell cast next to an attacker** whose expected damage over the faint turns
   (`randint1(5 × oops + 1)`) exceeds what the cast saves.
4. **Light radius** (perception, not a parameter): mark lit only within `cur_light − 1` (cave-view.c:658). With that
   fix the Borg keeps an unseen monster where it was last seen instead of deleting it.
5. **The owner's idea: shoot along a corridor at a believed monster.** Keep a position belief for a monster that
   stepped out of light, or that bumped or hit unseen. Use its last grid, speed and erratic flags: a speed-100,
   RAND_75 worm rarely moves far. Fire a bolt along the line, where the first monster in the path takes it.
   Magic Missile is a bolt (`BOLT_OR_BEAM`, class.txt:212), so a shot down a straight corridor hits whatever is in it.
   This is useful well beyond worms: unseen bumps, monsters at the edge of light, invisible attackers (#699).
   Candidate: when the believed monster is in a straight line within range and nothing known is between, and the
   ranged attack's expected value beats the alternative. For light-sensitive monsters (HURT_LIGHT) a Mage's
   Light Room hurts them and also lights the corridor (class.txt:221–223).
6. **Recall forecast: model POISON (and other damage-over-time) blows** as damage, from dice plus the poison
   timer (mon-blows.c:683–684, 1 HP per 10 game turns), instead of as an unknown risk that vetoes a flight Recall.
   Then, with a scroll, "Recall when the level is a losing breeder fight and no stairs are reachable" is a candidate
   rule (owner: Recall was a reasonable exit here). Keep the Recall purchase floor in mind: this Mage never had
   400 gold.
7. **Phase (unseen bump) needs a recent bump.** Do not read Phase at danger 0–1 with nothing awake within, say, 10 grids.

Fixes 1–3, 6 and 7 are behaviour switches that borg-zoo can measure as arms against the shipped `harness/borg.txt`.
Fix 4 is a perception fix that every core build shares.

## Files

- [replay/461220874/](replay/461220874/): `config.txt`, `zoo-death.json` (with the zoo cell record), `user/borg.txt`,
  `user/scary_monsters.txt`, and the verified replay's `keys.log`, `messages.log`, `state.log`, `summary.json`.
- [counterfactual/](counterfactual/): the save at key 1461, each arm's borg.txt diff, summary, and first-contact messages.
- [perception/](perception/): the diagnostic patch (scratch only, never for commit) and its notes for both lives.
- [related/399497898/](related/399497898/): the priest's csw borg.txt and replay key hash.

Issues: see the links added below once filed.
