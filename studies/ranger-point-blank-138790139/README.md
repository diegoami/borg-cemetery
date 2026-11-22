# Ranger point-blank divisor 1: the Human Ranger 138790139 and the crow

What the owner asked: on the Human Ranger of borg-zoo run
[44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466), does the
Ranger shoot the crow instead of meleeing it if a shot at an adjacent monster has no
point-blank penalty, and does it live? The death is
[D-c4a44a562f58](../../deaths/D-c4a44a562f58a485219d0d93ee1cb7cc9112a58e079dda4045ff16ca1b776985/README.md)
(runs/2026-11-22-fastfrag-stats-ban, borg-cemetery#109). The setting is
`attack_arrow_point_blank_divisor`, set per class by
[borg-reborn-rs#485](https://github.com/diegoami/borg-reborn-rs/issues/485).

**One start, one game per arm.** This is an anecdote, not a rate
(borg-reborn-rs RULES 14, 20). Any general statement below is a hypothesis for a borg-zoo
request.

## Answer

**No, on this start.** The divisor never reaches the crow decision:

- Every crow attack in every arm is made by attack-on-sight. At 7f8c6b80 the control's
  path is `#760` and the stats-ban arm's is `#842`. Both pick their attack with the
  focused planner, `focused_attack` (`borg-core/src/borg_fight_attack.rs:5362`).
- For a shot, the planner's damage function `borg_launch_damage_one` returns through
  `focused_launch_damage` (`borg_fight_attack.rs:964-965`) before the point-blank
  divisor is applied (lines 1029-1031).
- Its own comment says why: "the native planner's targeting bonuses, missile
  conservation and point-blank preferences are not damage" (line 5143).
- So the planner compares melee and arrows by expected HP per turn, with no divisor.

**The death game, on its own build (7f8c6b80):** with the Ranger's divisor at 1, the key
stream is byte-identical to the death in both the control and the stats-ban settings. It
dies to the crow at game turn 42,507, CL3, as the zoo recorded. The keys' sha256 is
`b9e7f2f8…`, the same as the dossier's `result_sha256`.

**On main (47b9bbb6):** the game no longer meets that crow. All three arms live to the cap.
The divisor changes the game at turn 45,482 through the native planner. There an adjacent
apprentice gets an arrow instead of a stab. Crows are not involved.

**On track-p (e2d8919e, 105 commits ahead of main, which it contains):** neither game meets
a crow at all. All three arms live to the cap. The divisor changes the game at turn 46,028,
inside a wild-dog pack, where the Borg shoots a different dog (see *Track-p*). Track-p
keeps the same code path: the focused planner returns at `borg_fight_attack.rs:1069-1070`,
before the arrow divisor at line 1137.

## Settings checked (main 47b9bbb6)

- `attack_arrow_point_blank_divisor`: default 5, range 1..=1000 (`params.rs:933`).
  `harness/borg.txt:552` ships 5.
- For a Ranger, `borg.txt:1628` ships `borg_param_attack_arrow_point_blank_divisor_ranger
  = 2`, folded in from `harness/borg_ranger.txt:6`.
- The `_ranger` name is an alias of `attack_arrow_point_blank_divisor@ranger`. Its
  sentinel is 0 (`params.rs:2524`, `legacy_alias`), and a value at the sentinel "sets no
  class value" (`params.rs:2651-2654`). So **0 means "use the general divisor" (5), not
  "no penalty"**.
- **1 is allowed and means no penalty.** It is what this study used.
- Environment overrides beat borg.txt, class value against class value
  (`params.rs:2646-2648`). Each arm's `settings-resolved.json` confirms the value it ran
  with (the "divisor" column below).
- The fast-fragile flags on main: `fast_fragile_policy = 1` and `fast_fragile_no_heal = 1`
  are shipped (`borg.txt:1291-1293`); `fast_fragile_by_stats = 0` is not. So arm C adds
  only `BORG_PARAM_FAST_FRAGILE_BY_STATS=1`.

## Arms

Start: seed 138790139, race 0 (Human), class 7 (Ranger), 100,000 game turns, `menu,exact`,
default core (borg-rs). Engine built with `BORG_IMPL=rust harness/build.sh`.
[arms.sh](arms.sh) has the exact commands.

| arm | build | overrides | divisor | ff policy / by_stats / no_heal | keys |
|---|---|---|---|---|---|
| A | main 47b9bbb6 | none | 2 | 1 / 0 / 1 | own game |
| B | main 47b9bbb6 | `BORG_PARAM_ATTACK_ARROW_POINT_BLANK_DIVISOR__RANGER=1` | 1 | 1 / 0 / 1 | differs from A at 45,482 |
| C | main 47b9bbb6 | B + `BORG_PARAM_FAST_FRAGILE_BY_STATS=1` | 1 | 1 / 1 / 1 | identical to B |
| old-ctl | 7f8c6b80 | none | 2 | 0 / 0 / 0 | the zoo's death game |
| old-ctl-div1 | 7f8c6b80 | `…DIVISOR__RANGER=1` | 1 | 0 / 0 / 0 | identical to old-ctl |
| old-ban | 7f8c6b80 | the zoo arm's three flags | 2 | 1 / 1 / 1 | identical to old-ctl |
| old-ban-div1 | 7f8c6b80 | old-ban + `…DIVISOR__RANGER=1` | 1 | 1 / 1 / 1 | identical to old-ctl |

Each arm's configuration hash (`params_core_sha256`) and key hash are under *Hashes*.

Every run's `borg_txt_sha256` is `8d772f96…` on main and `690245b4…` on 7f8c6b80; the
settings came through the environment. The zoo's borg.txt with the appended lines hashes
`32508ae3…`, but it plays the same keys. The cemetery death tools are at
`4697893660942ed142744306c634583ec630f88a` (`death-tools-pin.txt`).

## Outcomes

| arm | outcome | turn | CL / max CL | max DL (first turn there) | keys |
|---|---|---|---|---|---|
| A | alive at the cap | 100,000 | 6 / 6 | 4 (DL3 at 46,412, DL4 at 95,975) | 15,682 |
| B | alive at the cap | 100,000 | 7 / 7 | 3 (DL3 at 56,428) | 17,346 |
| C | alive at the cap, same game as B | 100,000 | 7 / 7 | 3 | 17,346 |
| old-* (all four) | dead, a crow | 42,507 | 3 / 3 | 2 | 6,452 |

## Crow fights

### The death game (7f8c6b80, all four arms identical)

The Borg arrives on DL1 by a down staircase. It shoots the giant green frog twice (attack
type 3, LAUNCH 4/8 and 8/16; no melee candidate at distance 5 and 4). From 42,462 it picks
a lock, and the crow bites it.

| turn | HP before → after | decision | attack | result |
|---|---|---|---|---|
| 42,492 | 16/22 → 12/22 | "Fast-fragile (named): crow (speed +12 vs +0, 11 HP vs 5.0 per turn, 6.6 damage/turn = 41% of HP 16)"; "Attack on sight: crow (fast-fragile), 10 HP, attack 1" | melee, Main Gauche (1d5) | hit; 3 bites, 1 miss |
| 42,501 | 10/22 → dead | "… 8 HP vs 5.0 per turn … 66% of HP 10"; "attack 1" | melee | miss; 4 bites, dead at 42,507 |

No shot is fired at the crow, so there are no shot hits. The focused planner's choice is
logged only as the attack number. Its "5.0 per turn" is the best attack's HP per turn
(`focused_attack`, `borg_fast_fragile.rs:133-136`), and the arrows' figure is not logged. In the old-ctl arm the same
decision is logged as `(#760)`.

### Main, arm A (shipped)

| turn | HP | what the Borg did |
|---|---|---|
| 44,578 | 36/36 | attack on sight, melee (attack 1): hit, the crow flees |
| 44,767 | 36/36 | melee: hit, the crow flees |
| 44,881 | 9/36 | not attacked; flees ("scaryguy"); Phase Door rule |
| 45,059-45,069 | 6/36 | "Fight race … not winning"; no cure ("No healing potion in contact with a fast-fragile attacker"); Phase Door read at HP 6 |
| 45,129-45,278 | 27 → 19 | crow bites while the Borg flees to a stair; no attack on sight logged |
| 45,345 | 21 → 16 | melee: hit; 3 bites |
| 45,354 | 13 → 14 | melee: crow slain |
| 93,271 | 49/52 | attack on sight, **attack 3 (shot)** at distance 1: hit, the crow dies |

The lowest dungeon HP of the game is 4/36 at 44,931. That is in the same stretch, before
any divergence, and it is the same in all three arms.

### Main, arm B (divisor 1)

Identical to A up to 45,482, with the same four melee attacks at 44,578-45,354. Later:

| turn | HP | what the Borg did |
|---|---|---|
| 59,728 | 39 → 38 /48 | attack on sight, melee: hit |
| 59,737 | 35 → 36 /48 | melee: crow slain |
| 67,640 | 52/52 | attack on sight, attack 3, shot at distance 2: no hit message |
| 67,649 | 48/52 | shot at distance 1: hit |
| 67,657 | 44/52 | shot at distance 1: hit, the crow flees |

The attack-on-sight choice moves from melee to arrows as the character levels: at CL6-7
"5.3 per turn" is the arrows' figure. That happens in A (93,271) as well as B, so it is
the character's growth, not the divisor. Per-attack rows are in
[data/attacks-A.tsv](data/attacks-A.tsv) and [data/attacks-B.tsv](data/attacks-B.tsv);
every crow-related key is in [data/crow-A.txt](data/crow-A.txt) and
[data/crow-B.txt](data/crow-B.txt).

## Where B first plays differently from A

At `keys.log` line 6,778, game turn 45,482, DL2, HP 32/36: the Borg is fleeing a
"scaryguy" level, adjacent to an apprentice with 3 HP. This is the native planner
(`borg_attack`), the only place the divisor acts:

| arm | melee (raw / weighted) | launch (raw / weighted, ×2000‰) | chosen |
|---|---|---|---|
| A | 30 / 30 | 13 / 26 | melee, the 3rd stab in a row |
| B | 30 / 30 | 19 / 38 | arrow: "hits the apprentice. The apprentice dies." |

## What else the divisor changes on main

| over the game | A | B |
|---|---|---|
| shots fired (distance 1 / farther) | 244 (56 / 188) | 272 (64 / 208) |
| shots after the divergence (distance 1) | 178 (43) | 206 (51) |
| melee attacks | 86 | 75 |
| arrow hit messages / arrows broken | 205 / 70 | 244 / 78 |
| kill messages | 130 | 172 |
| Cure Light Wounds quaffed / Phase Door read | 8 / 10 | 14 / 9 |
| lowest HP after the divergence | 15/36 (46,153) | 11/36 (56,018) |
| arrows bought after the divergence | 26 | 152 (9 purchases) |
| arrows at the end | 18 | 116 |
| CL at the end, max DL | 6, DL4 | 7, DL3 |

Adjacent shots in B go mostly to wild dogs (16), fruit bats (8), acolytes (7) and
salamanders (5). In A they go to acolytes (11), Fang (9), white worm masses (8) and giant
white centipedes (7): after the divergence the two games meet different monsters.

Nothing is clearly worse in B. It levels one CL higher and ends with more arrows, because
it bought more. It quaffs 6 more cures and goes no deeper than DL3, while A reaches DL4
at 95,975. Its lowest HP after the divergence is lower (11 against 15 of 36). These are
two games that split at one decision; none of these differences is a measured effect.

The `dist` column comes from `state.log` positions. About 13-15 melee rows show a
distance above 1; they are town urchins whose logged coordinates do not match. This was
not investigated.

## Track-p (e2d8919e)

Added after the owner's follow-up ("Main was many commits behind ... repeat on
track-p"). The build is borg-reborn-rs `e2d8919e8aa314b8a3622b90bf0b1be7958bdfd4`, source
hash `453451d4b8a44259…`. `harness/borg.txt` sha256 is `e4bd2b87…`; its run copy hashes
`3c0c9d8b…`. Smoke is 3/3 identical to `smoke-borg-rs`.

What track-p ships that matters here:
- the same arrow divisors (5, Rogue 3, Ranger 2; `borg.txt:634`, `1783`);
- `fast_fragile_policy = 1`, `by_stats = 0`, `no_heal = 1` (`1405-1407`);
- #870's `attack_throw_point_blank_divisor = 1` (`715`), which no arm changes.

| arm | overrides | outcome | CL | max DL (first turn) | keys | params_core_sha256 | keys sha256 |
|---|---|---|---|---|---|---|---|
| tp-A | none | alive at the cap | 8 | 5 (DL3 63,987; DL5 67,322) | 20,433 | `21a3f54b2b66ed61ae5630046933d412ae1aeacb7bdee43f570ef57da8638d31` | `f01f7fdf4521ccfcb3333f4f1ba79fe081e60a2eacc23a31b90f2b35e7e06816` |
| tp-B | Ranger divisor 1 | alive at the cap | 7 | 4 (DL3 72,456; DL4 73,640) | 19,438 | `06a17b7ec16562775e4121e236332e6df222680636c6635a5838b5b90165078c` | `0ac863bf4405915577bc2f79bbeed8072000d13da2f9ce650bd10fc003cf0556` |
| tp-C | B + `by_stats=1` | identical to B | 7 | 4 | 19,438 | `3d75da444dec80f1bdcc45a9b9ce89e7c8be18d29d770a401de4a0860df9a072` | = B |

**Crows:** none in either game. No crow is created in view, so the owner's question has no
crow fight to answer on this head.

**First difference:** `keys.log` line 8,416, game turn 46,028, DL2, a pack of wild dogs at
3 HP each.

| arm | melee | launch, as chosen | target |
|---|---|---|---|
| tp-A | 6 / 6 | 8 / 16 | the dog at distance 2, (43,40) |
| tp-B | 6 / 6 | 10 / 20 | the adjacent dog, (43,42) |

Both arms shoot. The divisor raised the adjacent dog's value until it became the best
target. One turn earlier (46,019) both arms had already shot an adjacent dog: at divisor 2
the arrow, 4/8, beat the stab, 6/6, because of the projectile weight 2000‰.

**Over the game:**

| | tp-A | tp-B |
|---|---|---|
| shots (distance 1 / farther) | 298 (85 / 213) | 308 (80 / 228) |
| melee attacks | 81 | 66 |
| arrow hit messages / broken | 250 / 91 | 250 / 84 |
| kill messages | 143 | 153 |
| Cure Light Wounds / Phase Door | 10 / 3 | 7 / 3 |
| lowest HP after the split | 12/48 (51,984) | 39/52 (68,329) |
| arrows bought after the split / at the end | 87 / 110 | 76 / 64 |
| CL, max DL | 8, DL5 | 7, DL4 |

The lowest HP of the game, 3/22 at 31,794, comes before the split and is the same in both
arms. Here divisor 1 ends a level lower and a level shallower; on main it ended a level
higher. Per-attack rows: [data/attacks-trackp-A.tsv](data/attacks-trackp-A.tsv),
[data/attacks-trackp-B.tsv](data/attacks-trackp-B.tsv).

## Would shooting the crow have saved it? (7f8c6b80, a scratch probe)

Added at the owner's request. The probe lives in a scratch build of 7f8c6b80 and is not
committed to borg-reborn-rs: [probe-7f8c6b80.diff](probe-7f8c6b80.diff). It adds two
things to `focused_attack_ranked`:
- a note with each focused candidate's rating, which does not change play: with the probe
  built and its switch unset, the keys are the death's, `b9e7f2f8…`;
- a switch, `PROBE_FAVOR_LAUNCH_FROM=<game turn>`, that multiplies the arrows' rating by 1.1
  from that game turn on.

**The planner's ratings** (HP per Borg turn, from the death game, stats-ban settings):

| turn | melee, Main Gauche | arrows, Short Bow (1.1 shots per turn, quiver 117) | chosen |
|---|---|---|---|
| 42,492 | **4.997** | 4.768 | melee |
| 42,501 | **4.997** | 4.768 | melee |

The arrows lose by 4.6%. The divisor is not in either number.

**The counterfactual:**
- **Arrows favoured from turn 42,490.** The game is the death game key for key up to
  `keys.log` line 6,444, the first crow decision. From there:
  - 42,492: the shot hits (crow 10 → 3 HP); "The crow flees in terror!";
  - 42,501 to 42,519: three more shots at the fleeing crow at distance 3-7, two hits;
    "The crow dies.";
  - the Borg takes no damage after the first decision (HP 16/22 throughout);
  - **alive at the cap: CL7, max DL4** (DL3 at 90,639).
  - The stats-ban and control settings give the same keys (`d346bcba…`;
    params_core `0cc8a206…` and `1c544a18…`).
- **Arrows favoured from turn 0** (control for the gate). The game splits at 29,588, long
  before the crow, and never meets it. It lives (CL6, DL3, keys `553520d6…`), but that is
  another game and is not evidence about the crow.

**Reading (one start, one roll of the dice):**
- The melee hit did 3 damage, and the crow kept biting.
- The arrow (1d4 × 2) did 7, and the crow fled. A fleeing crow can still be shot; it
  cannot be stabbed.
- On this start the choice of arrows decides the game. That is partly the roll: the fear
  came from the bigger first hit.

**Hypothesis H3, for a zoo request:** at early CL, against a fast-fragile monster the
focused planner's near-tie between melee and arrows should go to the arrows (or to a
ranged attack in general). That would take a code change: a preference or tie margin in
the focused planner. It is not a setting today, and the point-blank divisor does not reach
it. Not measured.

## Hypotheses for a borg-zoo request (RULES 14, 20)

1. **H1: on the shipped settings, the Ranger's point-blank divisor does not affect fights
   with fast-fragile monsters.** The attack-on-sight and fast-fragile paths use the
   focused planner, which ignores it. This is a property of the code (cited above), not a
   measurement. A zoo arm is needed only to size the indirect effect (H2).
2. **H2: Ranger divisor 1 against the shipped 2** changes Ranger games through the native
   planner. On this start that meant more adjacent shots, more arrows used and bought, and
   a higher CL; on track-p, a different target and a lower CL. The zoo has measured this
   before.
   - [borg-zoo#290](https://github.com/diegoami/borg-zoo/issues/290), on main f660aecc:
     development 11 against 18 deaths over the 200 classes-1800 Rangers (p 0.12), then
     confirmation 12 against 15 over the 200 classes-1800-b Rangers (p 0.58, not
     confirmed). Binned neutral.
   - Re-measure on track-p e2d8919e:
     [borg-zoo#651](https://github.com/diegoami/borg-zoo/issues/651). Arm `lo`:
     `borg_param_attack_arrow_point_blank_divisor__ranger = 1` against the shipped
     `harness/borg.txt`, on the 200 classes-1800 Ranger starts. Any confirmation goes to the
     Ranger starts of classes-1800-fresh.
   - Endpoints: deaths, max CL, max DL, arrows fired and bought.
3. To make a *crow* fight use arrows, the lever is the focused planner's comparison
   (melee against arrows by HP per turn), not this divisor. On the death game the planner
   rated the Main Gauche at 5.0 HP per turn against a 10-11 HP crow. Any such change is
   code, not a setting, and is outside this study.
   - [borg-reborn-rs#870](https://github.com/diegoami/borg-reborn-rs/issues/870) (a
     separate point-blank divisor for thrown oil) is merged on track-p and shipped at 1.
     Its `borg.txt` comment says "Attack on sight already bypasses it", the same as
     the arrow divisor.

## Hashes

| run | params_core_sha256 | keys.log sha256 |
|---|---|---|
| A | 236784febb27f7f09c9df67729ff1aeb38bda471d56522b708f8b358bb90ade3 | abe1e46400f97d4d490087a3183e5186214ffde1e22a471b6f5605c9211812d2 |
| B | e89106fa3e508127927ecca562fdcc6208300ad7159e7b5d3c9d04a046f093c9 | f381a4a344e5d01d13e36ccebaeeed34dc8f3147f8d4c0a02909a260e362cca0 |
| C | 91b00e469f186a9a94c98dfa825a0e37a27077997dbdf09e18d7bd8aeba3319e | f381a4a344e5d01d13e36ccebaeeed34dc8f3147f8d4c0a02909a260e362cca0 |
| old-ctl | 1c544a18627156cecd086bf16500d3c7aba62e681f5320f0b03d51355985e398 | b9e7f2f85eff2c89513728c398e345fe3e09226c9cb84724e6df4290b178b0d9 |
| old-ctl-div1 | 342a81fea920647934474520bb5d60aec8f3cc99f70e9b87bedb34a9ba73e205 | b9e7f2f85eff2c89513728c398e345fe3e09226c9cb84724e6df4290b178b0d9 |
| old-ban | 0cc8a206df9634864493cb69ce2e78c8d6e2bdeb53ae81eccebfb1b546260460 | b9e7f2f85eff2c89513728c398e345fe3e09226c9cb84724e6df4290b178b0d9 |
| old-ban-div1 | 65df97561eb6f1509a9bb7a07508f681e7b88ee13bff33adc83dcc943c828c0d | b9e7f2f85eff2c89513728c398e345fe3e09226c9cb84724e6df4290b178b0d9 |

Shared by all main arms: `borg_txt_sha256` 8d772f96ab2780d512dfb00d8950c688135b5b59088a1d61d02d2ac70511b161,
scary list e0e293814e8ed9c2f3a5f0af809f479e854878e5d0eaedea37b671dd1b20f5a8. On 7f8c6b80:
`borg_txt_sha256` 690245b4dce8f440dea032285592a632b5091455b459e45646f16cb0f1839eec.

## Death records

The four 7f8c6b80 runs play the same start with the same keys as D-c4a44a562f58 (sha256
`b9e7f2f8…`). They are that death, KNOWN, and need no new record (RULES 12, owner #464).
The main and track-p arms did not die. The raw run directories are not committed.
