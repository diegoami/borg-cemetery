# Flight Recall among white worm masses: the CL6 priest of borg-zoo run 44924461733

Investigation for [borg-reborn-rs#876](https://github.com/diegoami/borg-reborn-rs/issues/876)
("don't refuse flight Recall when the attacking monsters are breeders"). One named
case, one life: the replays below are branches of the same game, not samples
(borg-reborn-rs RULES 12, 14).

**Result: the issue's premise does not hold for this game.** From game turn 45022
until its death the priest had **no Word of Recall to read**. Every "Refusing flight
Recall" note after that turn was printed by a check that runs before anyone looks
for a scroll. When that check is forced to allow Recall, the game is the same key for
key and ends in the same death. Recall was never the way out of the worm pocket.

## The case

| | |
|---|---|
| zoo run | [44924461733](https://github.com/diegoami/borg-zoo/actions/runs/44924461733) (`reborn-confusion-837-small`, suite `classes-1800-small`, start 76 of `toolkit/originals-20261108/starts.json`) |
| specimen | `4.2.6-reborn-rust-confusion-da097a76`, borg-reborn-rs `da097a764239c64cdcdd0fb469d5a05577a6823e`, borg-rs core |
| arms that died | `reborn-confusion-csw` and `reborn-confusion-clw_walk`: same play hash, same game. `ctl` and `stuck` reached the turn cap alive |
| character | Dunadan Priest, seed 399497898, race 8, class 3, menu letters, cap 100,000 game turns, exact turns |
| arm settings | `borg_param_caution_confused_clw_cure=1`, `borg_param_town_confusion_cure_reserve=1` (csw; `evidence/zoo-config.txt`) |
| death | game turn 66588, key 6212, CL6, max HP 59, dungeon level 1, "a white worm mass" |
| play hash | `dde95ceb4cce4cb57309baa4c1aea2281d496c9f78b06b76a5c9c6169d17a4e9` (sha256 of `keys.log`) |

The issue gives run 44936494812, but that is the **medium** tier (starts 91–360) and
has no seed 399497898. The death is in the small tier, run 44924461733: artifacts
`deaths-…-1` (csw) and `deaths-…-5` (clw_walk).

## Rebuilding the exact game

`reproduce.sh` builds da097a76 (`harness/build.sh`, rust) and plays the start from
birth with the arm's settings (`harness/run.sh … 399497898 8 3 100000 exact,menu`).
It does not load a save. The game RNG, the Borg (which uses no RNG of its own
here, `summary.json: borg_rng 0`) and the build decide every key. The result is the
zoo's game:

- `keys.log`, `messages.log` and `state.log` are byte-identical to the zoo
  artifact's (`evidence/hashes.txt`);
- the run's `borg.txt` differs from the zoo's only in where the scary-list line sits
  (the zoo adapter puts it inline, `run.sh` appends it with its hash); same values.

The local binary's sha256 (`18ca455b…`) differs from the zoo's (`d6a70762…`):
another machine and toolchain path. The streams are what we compare.

## Step 1: why the check refuses (verified)

Code: borg-reborn-rs `borg-core/src/borg_caution.rs`, same lines at da097a76 and at
`track-p` c432b786.

- Every white worm mass counts as an "unmodelled spell/status risk" **because of its
  poison blow**: `fight_incoming_with` sets
  `out.unknown_damage |= !modelled_blow(effect)` (:2400), and `modelled_blow`
  (:2366) accepts only `HURT | ACID | ELEC | FIRE | COLD | NONE`. The worm has no
  spells: in every forecast `ranged_risk=false`, so this is the blow alone
  (`evidence/monsters-at-issue-turns.txt`, 53 monsters, all
  `unknown_damage=true ranged_risk=false multiply=true`). `flight_recall_survivable`
  (:2256) then counts it (`unknown_risks += 1`, :2292) and `recall_forecast_allows`
  (:2236-2237) refuses on any `unknown_risks > 0`.
- **The contact HP refuses too.** At turn 64022 the sum is 193.53 HP against
  55 HP, so the check would still refuse with the poison blow modelled.
  Exempting the blow is not enough: breeders' contact HP would also have to be
  left out, or capped.

The engine (574b618c):

| fact | value | where |
|---|---|---|
| white worm mass speed | 100 (−10), energy 5 per game turn vs 10 at normal speed: one action per two player turns | `lib/gamedata/monster.txt:680`, `src/game-world.c:68-81,138` |
| HP / blow | 10 HP; `CRAWL:POISON:1d2` | `monster.txt:681,688` |
| flags | `MULTIPLY`, `RAND_25 \| RAND_50` (75% of moves are random steps), `STUPID` | `monster.txt:689-690`; `src/mon-move.c:1087-1103,1571-1585` |
| breeding | tried before any attack or move, can use the turn; fewer than 4 neighbours; at most 100 breeders on a level; rate 8 | `mon-move.c:1024-1063,1563-1565`; `constants.txt:30,52` |
| poison blow | element damage, then `TMD_POISONED` + (5 + 1d rlev) | `src/mon-blows.c:674-690` |
| poison status | 1 HP per world tick while poisoned, **one status however many worms** | `src/game-world.c:513-519` |
| Recall's delay | `15 + randint0(20)` = 15..34 world ticks; counted down once per world tick (every 10 game turns) | `src/effect-handler-general.c:1145`; `game-world.c:709-711,1080-1081` |
| Recall scroll | 125 gold, sold always by the Alchemist | `object.txt:2865`; `store.txt:160` |
| Priest's Recall prayer | level 25 | `class.txt:840` |

`caution_recall_survival_delay` = 34 world ticks = 340 game turns = 34 player turns
at normal speed: the engine's longest delay, a cautious bound (`params.rs:43`). In
that time a worm gets 17 actions. `recall_exposure` (:2230-2234) counts
`hp_per_turn × (34 − 2·steps)` for each worm. At 0.658 HP per player turn, one
adjacent worm is 22.38 HP and one 9 steps away is 10.53 HP.

**The contact sum overstates what can reach the Borg.** It sums every reachable worm
for the whole delay (11 at 64022, 24 at 64932, 18 at 66582). At most 8 can be
adjacent. 75% of a worm's moves are random, and a breeding turn is not an attack.
The poison status is one 1-HP-per-tick status, so it adds at most 34 HP over the
delay; it is not a per-worm unknown. Measured over a 340-game-turn window in the
real game (the priest was meleeing and healing, so these are net figures):

| window | reachable | modelled contact HP | worm hits | HP at start → end |
|---|---|---|---|---|
| 64022–64362 | 11 | 193.53 | 7 | 55 → 49 |
| 64932–65272 | 24 | 442.36 | 7 | 43 → 48 |
| 66242–66582 | 18 | 346.25 (at 66582) | 12 | 37 → 2 |

## Step 2: the counterfactual (contradicts the issue)

**There was no Recall to read.** `evidence/forecasts.txt` logs every one of the 147
flight-Recall forecasts with `BI_RECALL`, the Borg's count of Recall sources:

- turns 44932–45012: 9 refusals **with** one scroll (1 sleeping monster, HP 39/39).
  At 45022 the forecast allows it, and the priest reads its last scroll (key 3641):
  "You have no more Scrolls of Word of Recall (m)" (key 3646);
- turn 45340: yanked to town with **117 gold**. `birth_no_selling`: what it sells
  brings nothing. It buys Remove Curse for 100 gold (a steelskin curse) and 5 flasks
  of oil for 15. That leaves 2 gold, and a Recall costs 125. It takes the down stair
  at 46411 with no Recall;
- turns 46802–66582: **137 refusals, all with `BI_RECALL=0`**, including the three
  the issue quotes (64022 HP 55, 64932 HP 43, 66582 HP 1). The two scrolls picked up
  later are unknown flavours ("miter pafficus", key 4610; "creffido tuder",
  key 5312). Recall's flavour has been known since 45022, so neither can be Recall.
  The priest has no Recall prayer before CL25. At 64022 it has 537 gold but no
  route to town.

`borg_recall_for_flight` (`borg_escape.rs:102-107`) evaluates
`flight_recall_survivable(st) && borg_recall(st)`: the forecast, and its
"Refusing flight Recall" note, come **before** `borg_recall` looks for a rod, an
activation, the spell or a scroll (`borg_escape.rs:110-118`).

**Forced allow, same game.** `diagnostic.patch` adds `BORG_CF_ALLOW_FROM_TURN=N`:
from game turn N on, `flight_recall_survivable` returns true. Every key before
the first forced call is the original's.

| branch | forced allows | key stream | end |
|---|---|---|---|
| original (da097a76) | none | `dde95ceb…` | dies 66588, key 6212 |
| diagnostics only (`BORG_CF_DEBUG=1`) | none | `dde95ceb…` | dies 66588 |
| allow from 46802 (first refusal without a scroll) | 137 | `dde95ceb…` | dies 66588 |
| allow from 64022 (key 5602, HP 55/59) | 91 | `dde95ceb…` | dies 66588 |

Allowing Recall changes nothing, because `borg_recall` finds nothing to read.
"The last turn Recall still saves it" therefore has no answer in this game. The
only Recall it had was read at 45022 and did reach town (45340, HP 39/39). The
requested 64022/64932 counterfactual would need a scroll the game does not
contain. That is a constructed scenario, not this death, and was not run.

## What does explain the death (leads, not measured)

1. **It went down again without Recall.** Its 117 gold could not buy a 125-gold scroll
   even before Remove Curse, and it left town with 2 gold.
2. **On DL1 it knew no up stair** (the stair to town). From 63000 on: 82 × "Looking
   for any stair", 40 × "Looking for Up Stair", 10 × "no up stairs found, exploring
   for them (rising)", 31 × "Flowing toward down-stairs", 5 × "no up stairs found,
   going down", but it never takes a stair. borg-reborn-rs #862 (422246f5) and #871
   (bc12891d), both on `main`, change stair flight. Neither is in da097a76 or in
   `track-p` c432b786.
3. It meleed worms from 64022 to its death (68 killed; 73 since 63000) while they
   bred, and died at 1 HP with poison running. It stayed on DL1 all that time: no
   level change after turn 63000 (`state.log`).

## Files

- `reproduce.sh`: build, the original replay, the diagnostic branches; checks
  `forecasts.txt`;
- `diagnostic.patch`: the scratch patch on da097a76 (stderr diagnostics, the
  forced allow). It was never pushed to any borg-reborn-rs branch;
- `evidence/forecasts.txt`: all 147 forecasts (turn, HP, `recall_sources` =
  `BI_RECALL`, exposure, unknown, reachable, position);
- `evidence/monsters-at-issue-turns.txt`: each monster's terms at 64022, 64932 and 66582;
- `evidence/hashes.txt`: sha256 of the zoo's and the local streams;
- `evidence/zoo-config.txt`, `evidence/zoo-BUILD_ID`: the zoo cell's own records.

The raw logs (keys, messages, state, trace) are in the zoo artifact
`deaths-4.2.6-reborn-rust-confusion-da097a76-1` of run 44924461733 and are not
copied here. This natural death has not been imported as a Cemetery death
dossier (`D-<sha>`) yet. That is left to the zoo-death import.
