# The two deaths of the reborn-bfs-pilot bfs0 arm (track-p 1c071812)

Source: borg-zoo#730 (does breadth-first exploration lower early deaths on borg-reborn-rs track-p `1c071812`?), run [45118195112](https://github.com/diegoami/borg-zoo/actions/runs/45118195112), attempt 1, suite classes-18, 100,000 turns, 18 seeds per arm. Both deaths are in the `reborn-bfs-bfs0` arm (`explore_breadth_first 0`); the control arm (shipped, breadth-first) had none. Both were replayed from birth with the commit's own build and their key logs match the zoo cells' `play_sha256`. The dossiers are listed in [zoo-reborn-bfs-pilot-45118195112](../zoo-reborn-bfs-pilot-45118195112/README.md).

Report with each death's last 100 recorded screens: https://claude.ai/artifact/J82fh2AgLfFHixe7f8mKyJ
Play pack: `~/borg-play/bfs-pilot-deaths` (`./play.sh`).

| Dossier | Seed | Character | Killed by | Turn | CL / DL | Control (same seed) |
| --- | --- | --- | --- | ---: | --- | --- |
| [D-a237f629e42e](../../deaths/D-a237f629e42e33713941f40454bb4a12a987ba164299baacadf6405e69d4b187/README.md) | 1548306106 | Human Mage | a floating eye | 14,483 | 2 / 1 | alive at the cap, CL5, max DL2 |
| [D-153403b2c90a](../../deaths/D-153403b2c90aa3e19d764446fb335f049a107aef815b8ac8688f331bb03828d9/README.md) | 226104090 | Human Ranger | a soldier ant | 17,368 | 3 / 1 | alive at the cap, CL5, max DL2 |

## Observations

- Both deaths are floating-eye paralysis chains on a freshly entered DL1. Each Borg logged `Flowing toward dark-2 at cost 2` for a few steps after the stairs and an eye then gazed at it. The Mage was gazed at 21 times (6 paralysed, 4 resisted, 5 recoveries), the Ranger 15 times (4 paralysed, 7 resisted, 3 recoveries). Between the first gaze and death neither pressed anything but space.
- The Mage (14 HP) logged `Attack on sight: floating eye ... 0.0 damage a turn against HP 14 (#878)` at turn 14,256 and threw one Flask of oil, which hit but did not kill. It died with 5 Cure Light Wounds, 5 Phase Door and 8 flasks.
- The Ranger (25 HP) has no tracking note for an eye before the first gaze at 17,215. A soldier ant woke at 17,257 and bit it nine times (one miss) while it was held. It died with 13 Cure Light Wounds, 8 Phase Door and 15 arrows. The same game had met an eye after the same flow step at 12,739 (one paralysis) and survived it.
- The first differing key against the control is at game turn 1,511 (Mage) and 1,130 (Ranger). The control flows with `dark-bfs`, the bfs0 arm with `dark-1` to `dark-5`, so the later games differ throughout. The control met eyes too (Mage control: 5 gazes, 1 paralysis; Ranger control: 1 gaze, 1 paralysis) and lived.
- On the 18 pilot seeds the zoo page shows 0 rescued and 2 newly killed for bfs0, exact McNemar p = 0.500. One game per seed and arm; these are two lives, not a rate.

## Not checked

- How `fight_incoming_with` treats a paralysing gaze: `borg_lone_target.rs` rates the eye by `hp_per_turn`, and I did not read that function.
- Why the Ranger's eye was not tracked before it gazed.
- No counterfactual replays were run, and no save was loaded into a fresh Borg.

The control cells come from the run's `raw-4.2.6-reborn-rust-trackp-1c071812-1` artifact (tarball sha256 `a13f3f0142049e5845a45fb2205f783b64ebe297905d5d85e63db60a826fa758`).
