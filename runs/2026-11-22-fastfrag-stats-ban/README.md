# Fast-fragile stats-ban deaths, big tier (borg-zoo#596)

Source: borg-zoo run [44950087466](https://github.com/diegoami/borg-zoo/actions/runs/44950087466),
experiment `reborn-fast-fragile-big`, specimen `4.2.6-reborn-rust-fast-fragile-7f8c6b80`
(borg-reborn-rs `7f8c6b80`, PR #847, issue #842). Selection: every death of the arm
`reborn-fastfrag-stats-ban` (`fast_fragile_policy = 1`, `fast_fragile_by_stats = 1`,
`fast_fragile_no_heal = 1`) over classes-1800 starts 361-900, 100,000 game turns. The
import page is [zoo-reborn-fast-fragile-big-44950087466](../zoo-reborn-fast-fragile-big-44950087466/README.md).

Report with each death's last recorded screens: https://claude.ai/artifact/W3TpP3KAscneK31eGZDBnN (private until shared)

Play pack: `~/borg-play/fastfrag-stats-ban` (`./play.sh SEEDDIR --to TURN` replays the exact game).

| Dossier | Seed | Character | Cause | CL | DL | Turn | Control (`reborn-fastfrag-ctl`) |
|---|---:|---|---|---:|---:|---:|---|
| [D-764c60e2e79f](../../deaths/D-764c60e2e79fbe55e12f57fded00335994c58af3b7c6004f3a0e8029f85b0146/README.md) | 739186786 | Kobold Blackguard | a soldier | 2 | 1 | 4,315 | dies, same play |
| [D-63286be40892](../../deaths/D-63286be40892e5795d9c7ceca759a0d23c50f8c4eff3b7276c80a07a8eab7a6b/README.md) | 1512540769 | Human Priest | a white worm mass | 3 | 1 | 9,703 | dies, same play |
| [D-db67fee6d6ca](../../deaths/D-db67fee6d6caaf7d4a6bcbe3c4cebac13af9301eb0384f072ff195818b18c3e8/README.md) | 402790494 | Kobold Druid | a crow | 2 | 1 | 28,549 | dies to a crow (turn 26,206), different play |
| [D-c4a44a562f58](../../deaths/D-c4a44a562f58a485219d0d93ee1cb7cc9112a58e079dda4045ff16ca1b776985/README.md) | 138790139 | Human Ranger | a crow | 3 | 1 | 42,507 | dies, same play |
| [D-d97a18672a49](../../deaths/D-d97a18672a492587c9acbfede7f83106d2dbf6bca390faa93200127d89e4f46d/README.md) | 381988580 | Dunadan Rogue | a soldier | 4 | 2 | 62,965 | dies, same play |
| [D-af342fe11101](../../deaths/D-af342fe111018d78cd4dca016ffce4069371996a691ee9e598981e25dc15a1e7/README.md) | 2008390085 | High-Elf Rogue | a cave spider | 6 | 2 | 64,483 | lives |
| [D-85f1e458d8e9](../../deaths/D-85f1e458d8e94776e211db55dc21245ca194088014efe6f5734226c431fd9679/README.md) | 390305857 | Gnome Rogue | a blue yeek | 5 | 1 | 78,878 | dies, same play |
| [D-32621a9cd11c](../../deaths/D-32621a9cd11c6723f94706b2936a8745441f1889b901db6d67bd686d6dd7d9ea/README.md) | 798380952 | Half-Elf Necromancer | a fatal wound | 6 | 2 | 93,910 | lives |
| [D-87e4851831ce](../../deaths/D-87e4851831ce1b7c8ac10bf7f6714bf48a1487eda3f1e042c9ad5da080fb799f/README.md) | 829474344 | Half-Troll Ranger | poison | 8 | 2 | 96,820 | lives |

## Observations

The arm died 9 times out of 540 starts, the same number as the control. Paired by start: 6 die in both arms (5 with identical
key streams), 3 rescued (Druid 725188949, crow; Mage 896825692, crow; Druid 1247318324,
cutpurse) and 3 newly killed (seeds 2008390085, 798380952, 829474344), all after game
turn 64,000. Exact McNemar on 3 against 3: p = 1. Descriptive (RULES 14); the study pools
the small, medium and big tiers.

- 2008390085, High-Elf Rogue: cave spiders are fast-fragile by stats (speed +21, 9 HP).
  Three take HP 39 to 7 in four turns. At HP 7 the log says "No healing potion in contact
  with a fast-fragile attacker (#842)", and the rogue dies attacking with a Dagger (1d4).
- 798380952, Half-Elf Necromancer: attack on sight at an adjacent crow. One Nether Bolt,
  then four Flasks of oil that break without a hit message ("Guessing wall (49,120) near
  target (49,121)"). HP 33 to 0 in five turns; the Phase Door is read at HP 0.
- 829474344, Half-Troll Ranger: from turn 95,170 it steps back from a white jelly and the
  stair flow returns it next to the jelly. 132 touches and 4 Cure Light Wounds, no attack,
  dead of poison at 96,820. Not the policy.
- 402790494, Kobold Druid: the policy fires (6 Phase Doors at "the next turn kills", 11
  attacks on sight with a Whip (1d3); its kill rate is 1.6 HP per turn against the crow's
  7.1 damage per turn). The control's game died to a crow too, at 26,206.
- 390305857, Gnome Rogue (same play as the control): stunned by a blue yeek at 78,756.
  All 28 later hits "fail to harm" while the fight race says "1 turn to kill ... winning".
- 1512540769, Human Priest (same play): retreats and backs up from white worm masses
  ("32 > 1") until dead; compare borg-reborn-rs #876.

These are observations from the logs, not a diagnosis.
