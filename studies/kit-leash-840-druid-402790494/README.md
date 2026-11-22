# The kit leash on one start: the Kobold Druid of borg-zoo run 44950087466

An experiment on **one start**, for [borg-reborn-rs#840](https://github.com/diegoami/borg-reborn-rs/issues/840)
(owner, 2026-11-22: "does the kit leash (the smaller the kit, the smaller the leash) change this
game, and how?"). **One start is an anecdote.** Nothing here measures the kit leash; every
general statement below is a hypothesis for [borg-zoo#589](https://github.com/diegoami/borg-zoo/issues/589)
(borg-reborn-rs RULES 14, 20).

The start: seed 402790494, race 10 (Kobold), class 2 (Druid), suite classes-1800-big,
100,000 game turns, exact boundary. On specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`
the druid died to a crow in both arms of the run: `reborn-fastfrag-ctl` at game turn 26,206
and `reborn-fastfrag-stats-ban` at 28,549, CL2, DL1
(dossier `D-db67fee6d6ca…` in `runs/2026-11-22-fastfrag-stats-ban`, borg-cemetery#109).

## The short answer

1. **On current main (`47b9bbb6`) this druid no longer dies**, with or without the kit leash.
   Main's control (shipped settings, every kit switch 0) is alive at the cap, CL8, max DL2.
   It is a different game from the zoo's from **game turn 3,140**, before any kit setting can
   act: in the Alchemist, main buys 5 Phase Door and 1 Detect Invisible (75 + 15 gold) where the
   specimen bought 6 Phase Door (90). Bisected over main's merges: the change is
   borg-reborn-rs#836 (#830/#831, "buy Detect Invisible with spare gold"), merged into the
   specimen's line by #847's merge `5987e1fe` (`b9ea1b82` plays the specimen's key, `0a3889db`
   main's). One different key changes the next level and the rest of the game (gold found at
   5,670, CL2 at 8,231, CL5 at 23,093 against CL2 for life in the specimen). That is the RNG,
   not a measured effect of #831.
2. **On main, the kit leash changes this game only from turn 44,307–44,327**, when the druid's
   flasks of oil drop below 5 (the only short item: score 0.96, leash 23 instead of C's 24).
   Before that the kit is complete from turn 3,380 and the leash is C's. All five kit arms
   survive to the cap, as the control does.
3. **The crow is met by every arm except F, and killed by every one that meets it** — the same
   crow (index 52, at (20,128) on DL2). The leash arms meet it 50–80 game turns earlier, at full
   HP: B/C/E take 2 bites and kill it in the first round (44,537), D 4 bites (44,507); the control
   takes 9 bites, falls to 16/32 HP and kills it at 44,607. Whether that is the leash or the
   combat dice of a different turn cannot be told from one game.
4. **B, C and E are the same game key for key.** `kit_leash_min=2` only matters at scores the
   druid never reaches in the dungeon after shopping (its lowest is 0.68 for one think when the
   torch swapped); `kit_money_first` never holds because the druid is CL5 when its kit first goes
   short (`kit_money_first_max_level` = 2).
5. **F (kit-money-hunt) is changed by `town_hunt`, not by the kit**: at turn 471 a mean-looking
   mercenary makes the control flee town to DL1 ("Scary guy on level"); F keeps shopping instead.
   It never meets a crow, ends CL7 (one level lower), spends the least time on DL2, and has the
   fewest town arrivals (24 against 83).
6. **In the zoo's dying game the kit leash would have been on** (estimate, not run: the specimen
   has no kit code, and main does not reach that game). From turn 14,906 the druid holds fewer
   than 5 flasks and from 19,232 none; at death it held 4 CLW, 6 Phase Door, lit torches and
   6 rations, so its score would be 0.80, its exploration leash 12 instead of C's 15 (CL2:
   3×2+9) and its stair leash 16 instead of 20 (C's 3×CL+14). It died after a crow chase on DL1
   with the up stairs "at cost 34". A shorter leash would have kept it nearer the stairs: a
   hypothesis that only the zoo can test on the specimen-like games of #589's arms.

## Build and method

- borg-reborn-rs `origin/main` **`47b9bbb6`** (merge of #866), built with
  `BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh` (GCC 13.3, x86-64,
  `arg_order=rtl`, binary sha256 `03a35be7…afd1`). Default core: borg-rs (`borg_core=borg-rs`).
- Each arm: `harness/run.sh OUT 402790494 10 2 100000 menu,exact` under the lock, settings as
  `BORG_PARAM_<NAME>=N` overrides on `harness/borg.txt` (borg_txt_sha256 `5e49bc66…4d54` in
  every main arm). Every override is in the run's `params-core.json` with origin `environment`
  (checked; listed in `arms.json`). `arms.sh` reproduces all of them.
- The zoo's two games were replayed on the specimen commit **`7f8c6b80`** (binary `84768152…`):
  `Z1` (stats-ban: `fast_fragile_policy=1 by_stats=1 no_heal=1`) dies to a crow at 28,549 with
  keys.log sha256 **`8dd87995…6b28b`, the `result_sha256` of the zoo's dossier `D-db67fee6d6ca`**,
  so the local build plays the zoo's game key for key. `Z0` (the zoo's ctl: no override) dies
  to a crow at 26,206, the zoo's turn.
- The death export needed `BORG_CEMETERY_DIR` at borg-cemetery `46978936` (the source's
  `death-tools-pin.txt`; the sibling checkout failed the pin check on `PROVENANCE.md`). The
  local exports of Z0/Z1 went to that scratch checkout only; nothing new is recorded here, since
  the zoo's Z1 dossier is the same key stream (RULES 12, #464).
- First divergence: the first line where the arm's `keys.log` differs from A's.
- No code was changed and no reference was recorded.

## Fast-fragile settings main ships (`harness/borg.txt`, #842)

`fast_fragile_policy = 1`, `fast_fragile_no_heal = 1`, `fast_fragile_by_stats = 0`,
`fast_fragile_escape_percent = 100`, `fast_fragile_phase_landing = 0`,
`fast_fragile_speed_margin = 5`, `fast_fragile_kill_turns = 2`, `fast_fragile_damage_percent = 25`,
`fast_fragile_group_max = 2`. That is neither of the zoo's arms (ctl had the policy off;
stats-ban adds `by_stats = 1`). On main it makes no difference to this start: `S0` (policy and
heal ban off, like the zoo's ctl) and `S1` (by_stats on, like stats-ban) play A's game key for key
(the crow is a named entry, and the game splits from the zoo's at 3,140 anyway).

## Arms

| arm | build | settings (on top of the shipped borg.txt) | outcome | game turn | CL (max) | max DL | params_core sha256 | keys.log sha256 | first key differing from A |
|---|---|---|---|---:|---|---:|---|---|---|
| A | main 47b9bbb6 | none (control) | alive at the cap | 100,000 | 8 (8) | 2 | `236784fe…` | `80b932e9…` | — |
| B | main | `kit_leash=1` | alive | 100,000 | 8 (8) | 2 | `78859157…` | `c135c7c2…` | line 5,133, turn 44,327 |
| C | main | `kit_leash=1 kit_leash_min=2` | alive (= B) | 100,000 | 8 (8) | 2 | `277412f7…` | `c135c7c2…` | line 5,133, turn 44,327 |
| D | main | `kit_leash=1 kit_leash_power=2` | alive | 100,000 | 8 (8) | 2 | `41bd90d5…` | `cb6acc0c…` | line 5,131, turn 44,307 |
| E | main | `kit_leash=1 kit_money_first=1` | alive (= B) | 100,000 | 8 (8) | 2 | `941a54b4…` | `c135c7c2…` | line 5,133, turn 44,327 |
| F | main | `kit_leash=1 kit_leash_min=2 kit_money_first=1 town_hunt=1` | alive | 100,000 | 7 (7) | 2 | `9bd0f604…` | `1eaa72d0…` | line 64, turn 471 |
| S0 | main | `fast_fragile_policy=0 fast_fragile_no_heal=0` | alive (= A) | 100,000 | 8 (8) | 2 | `91a8dfbf…` | `80b932e9…` | none |
| S1 | main | `fast_fragile_by_stats=1` | alive (= A) | 100,000 | 8 (8) | 2 | `2eaf3646…` | `80b932e9…` | none |
| Z0 | specimen 7f8c6b80 | none (zoo ctl) | **died, a crow** | 26,206 | 2 (2) | 1 | `1c544a18…` | `40160f64…` | line 434, turn 3,140 |
| Z1 | specimen 7f8c6b80 | `fast_fragile_policy=1 by_stats=1 no_heal=1` (zoo stats-ban) | **died, a crow** | 28,549 | 2 (2) | 1 | `0cc8a206…` | `8dd87995…` | line 434, turn 3,140 |

Full hashes, overrides and counts: `arms.json`. `town_hunt` exists on main
(`borg-core/src/params.rs:56`, `borg_town_hunt.rs`), so F was played.

### What each arm did

| arm | turns at 0 gold | gold at 10k / 30k / 50k / 70k / 90k / cap | max gold | purchases | flasks thrown (last) | crow | game turns in town / DL1 / DL2 | town arrivals |
|---|---:|---|---:|---:|---|---|---|---:|
| A | 3,276 | 7 / 12 / 3 / 24 / 313 / 161 | 442 | 31 | 69 (99,683) | met 44,587, 9 bites, killed 44,607 | 18,109 / 71,421 / 10,465 | 83 |
| B, C, E | 2,520 | 7 / 12 / 367 / 352 / 17 / 397 | 447 | 26 | 67 (89,018) | met 44,537, 2 bites, killed 44,537 | 15,208 / 70,783 / 14,004 | 63 |
| D | 2,520 | 7 / 12 / 412 / 168 / 963 / 371 | 963 | 36 | 69 (79,382) | killed 44,507 (4 bites) and 70,415 | 17,489 / 70,965 / 11,541 | 56 |
| F | 0 | 5 / 64 / 4 / 89 / 248 / 598 | 598 | 28 | 42 (97,869) | never met | 16,566 / 76,232 / 7,191 | 24 |
| Z0 | 23,066 (3,140 to death) | 0 / – | 376 | 6 | 27 (19,232) | died 26,206 (27 bites) | 9,508 / 16,697 / – | 68 |
| Z1 | 23,288 (3,140–26,428) | 0 / – | 376 | 6 | 27 (19,232) | died 28,549 (47 bites) | 9,508 / 19,040 / – | 68 |

"Town arrivals" counts every step from the dungeon to town, including the stair hops of the
opening (the town's scary townspeople send the druid down and up). Purchases: `extracts/<arm>-purchases.txt`
("You bought" lines). Gold, depth and CL at every change: `extracts/<arm>-gold-depth-cl.tsv`.

**The opening is the same in A–E** (main): torch 6, 1 CSW 70, 27 flasks 81, 6 CLW 120,
3 rations 9, 5 Phase Door 75, 1 Detect Invisible 15 = 376 gold, all of it, by turn 3,150 (the
zoo's game: 6 Phase Door 90 instead of 5 + Detect Invisible, also 376). Gold is 0 from 3,150 to
5,670 on main and from 3,140 for 23,000 turns in the zoo's game ("Nothing to sell in town" with
`birth_no_selling`). F's opening differs (town_hunt): 5 CLW, 24 flasks, a cloak, gloves and two
torches, 11 gold left.

**Where the flasks went** (`extracts/<arm>-flask-throws.tsv`, every hit or miss with its target):
in every arm mostly at harmless or slow monsters, as the owner saw in the zoo's game. A: giant
white mice 9, wild dogs 9, white worm masses 6, grey molds 5, floating eyes 4, fruit bats 4,
… and 1 at Fang. B/C/E: white worm masses 12, giant white mice 10, wild dogs 9, … The zoo's
game: white worm masses 5, giant white mice 4, floating eyes 4, fruit bats 3, rock lizards 2,
giant white centipedes 2, …; the last at turn 19,232. The kit leash does not decide what is
thrown at; it only counts the flasks.

## The kit score and the leash it produced

Formula (`borg-core/src/borg_kit.rs` at `47b9bbb6`):
- shares (`share`, `shares`, lines 118–139): each item's holding over its target, capped at 1;
  the ranged share is the larger of missiles/`kit_missile_target` and flasks/`kit_flask_target`
  (a Mage's or Necromancer's spell makes it 1);
- the score (`score_permille`, 142–150): the weighted mean, permille;
- the leash (`scaled_leash`, 163–169; `leash`, 310–323): `kit_leash_min + (C's leash −
  kit_leash_min) × score^kit_leash_power`, rounded, while the kit is short (`leash_active`,
  291–293; `applies`, 278–280: a kit switch on, in the dungeon, CL ≤ `kit_max_level` 15);
  with `kit_money_first` held (`money_first_hold`, 297–304) at least `kit_money_leash` 6;
- the notes (`tick`, 436–495): `# Kit S (… short: …): leash N` when the score or leash moves.
- Targets and weights (`targets`, 177–187; defaults `borg-core/src/params.rs:58–88`): CL1–5
  3 cures and 2 Phase Door, CL6+ 5 and 4; 20 missiles or 5 flasks; 1,000 light turns; 3 food;
  all weights 1.
- Callers: `borg_get_leash` (`borg_flow_misc.rs:192–200`), the exploration and pick-up leash
  (`borg_flow_dark.rs:742, 796`, `borg_flow_take.rs:514`), and C's stair leash 3×CL+14
  (`borg_think_dungeon.rs:693–707`, floored at 3).

Over the game (`extracts/<arm>-kit-notes.txt`):

| arm | in the opening (CL1, stair hops to DL1, turns 561–2,081) | complete | short after shopping | score range then | leash then (C's) |
|---|---|---|---|---|---|
| B, C | 0.33 → 0.59, leash 5 → 8 (no oil yet, then no cures/Phase) | from 3,380 | from 43,757 (4 flasks), on and off to the cap | 0.68–0.96, short of ranged only (once light, for one think at a torch swap) | 21–32 (24–33) |
| D | same scores, leash 2 → 5 | from 3,380 | from 43,757 | 0.76–0.97 (it picked up missiles later) | 17–31 |
| E | same, leash 6 (money-first floor) | from 3,380 | from 43,757 | as B | as B |
| F | — (stayed in town) | from 2,871 | from 71,194 | 0.80–0.96 | 23–27 |

Each time the druid restocked oil (≥ 5 flasks) the kit was complete again and the leash C's.
The leash pulled it back ("Return to Stair (wandered too far)") only once in any arm, at
20,727 with C's 26, before any kit leash applied: the shorter leash acted through the choice of
exploration targets, not through stair returns.

### The first difference from A

- **B, C, E (turn 44,307–44,327, DL2, CL5)**: after the kit note `Kit 0.96 (… 0 missiles+4 oil
  …; short: ranged): leash 23` (C's 24), at 44,307 the exploration target changes
  (`Flowing toward dark-3 at cost 2` instead of `dark-2 at cost 3`); at 44,327 a trip check and
  `Flowing toward dark-5 at cost 21`, a different key (A: 36, B: 32). The druid reaches the
  crow 50 turns earlier, at 27/32 HP, and kills it with the first attack after 2 bites.
- **D (turn 44,307)**: the same moment with leash 22 (0.96² ≈ 0.92); a different key one think
  earlier; the crow is killed at 44,507 after 4 bites. Later D buys Word of Recall, a Scroll of
  Teleportation and Heroism (67,674) and reaches CL8 at 66,183 (A 79,635).
- **F (turn 471, town, CL1)**: `town_hunt` replaces the control's "Scary guy on level → leave"
  with continued shopping; see 5 above.

## The zoo's death (Z1, stats-ban): the last 50 lines of messages.log

`extracts/Z1-last50-messages.txt` (and Z0's). Summary, from 28,282 to 28,549 on DL1, CL2, 22 max HP:
the crow (speed +11, 7.1 damage a turn) attacks; the fast-fragile policy reads Phase Door twice
at HP 3 ("the next turn kills … the kill needs 3.7 turns", 28,301 and 28,351), refuses flight
Recall (#758), and the druid flees toward up stairs "at cost 34" and rests. The crow comes back
at 28,511; the druid quaffs a Cure Light Wounds at 6 HP (before contact), then fights with its
Whip (1d3): "Attack on sight: crow (fast-fragile)", 1.6 HP a turn against the crow's 7.1. Two
hits and a miss; HP 22 → 19 → 8 → −1; "You die." at 28,549, the crow at 2 HP. It still held
4 CLW and 6 Phase Door, 40 gold (found at 26,428), no flask since 19,232, and never reached
CL3 (25 XP), so no Stinking Cloud.

## For borg-zoo#589 (hypotheses)

- The kit leash cannot change a game before the kit is short in the dungeon, and for a druid
  that buys 27 flasks it is short only of the ranged item, late, by a few steps: a small leash
  change. In #840's dying cases the shortage is earlier (cures, Phase Door); whether the leash
  helps there is the zoo's question.
- `kit_leash_min` and `kit_money_first` were inert on this start (identical keys); arms that
  differ only by them may often play the control's or the leash arm's game exactly, which the
  pilot's "identical plays" column will show.
- `town_hunt` changes the opening in town, so the kit-money-hunt arm mixes two effects; a
  `town_hunt`-only arm would separate them.

## Files

- `arms.json`: per arm, overrides, outcome, full hashes, first divergence, counts.
- `arms.sh`: reproduces every arm (A–F, S0/S1 on main; Z0/Z1 on the specimen).
- `extracts/`: purchases, flask throws with targets, kit notes, gold/depth/CL changes, and the
  last 50 messages of each death. The raw run directories are not kept (they replay from
  `arms.sh` key for key).
