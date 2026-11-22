# Rests at danger 0: an unseen archer and a crow out of view (borg-reborn-rs #981, #982)

A study of two deaths from borg-zoo run 45028029063 (track-p `9085c266`, full tier), replayed on track-p `4b2c2fcf` and on the fix branches. The Borg rests because the attacker's danger is 0, and no rule drinks a potion at danger 0. Both runs use the borg-rs core (the default).

| start | dossier | issue | fix PR |
|---|---|---|---|
| Elf Warrior 1312323730 (`-race 2 -class 0`) | [D-6a839b1e](../../deaths/D-6a839b1e5c716242230f684e6b2206174544302289422dcd8b76e7c4474a8b6b/) | [#981](https://github.com/diegoami/borg-reborn-rs/issues/981) | [#998](https://github.com/diegoami/borg-reborn-rs/pull/998) |
| Half-Troll Necromancer 2125189042 (`-race 7 -class 4`) | [D-a61ab469](../../deaths/D-a61ab469b8a6a61bcd46066b2498d0d74bb79e9c158e36ac70a43f5c110858d9/) | [#982](https://github.com/diegoami/borg-reborn-rs/issues/982) | [#999](https://github.com/diegoami/borg-reborn-rs/pull/999) (stacked on #998) |

The dossiers are imported with the whole run in the Cemetery PR that adds `runs/zoo-reborn-trackp-9085c266-full-45028029063/`.

Each arm here is **one replay of one start**: a lead, not a measurement. The arms are alternative continuations of the same life, not independent samples. The measurement is [borg-zoo#671](https://github.com/diegoami/borg-zoo/issues/671).

## Warrior 1312323730: rests 18 times under an unseen kobold archer

**Cause.** "You are hit by something sharp!" is the engine's message for a projection from a monster the player cannot see, or for any projection while the player is blind (`project-player.c:798-799, 840-842, 886-888`). The archer was out of the light, not invisible. The Borg reads the arrow's "You hear a soft twang." as `SPELL_005:Something`, which creates no monster, so the danger is 0. The #697/#831 unseen-attacker mode is fed only by blows, so the hit never entered it: the off replay has no `# Mode:` line.

| arm | build | setting | keys sha256 | outcome |
|---|---|---|---|---|
| `off` | `f07b17f9` (#998), shipped settings | `recover_unseen_shot = 0` | `7243fba61d12f4b2` (= the zoo game, = `4b2c2fcf`) | dies at 24984 to the kobold archer, CL5 |
| `on` | `f07b17f9` | `recover_unseen_shot = 1` | `496861d1cf5d1a71` | mode entered at 24792; Detect Invisible ×2 (nothing); walks away while hit; rests; sees the archer at 24992 and kills it; alive at the 100,000-turn cap, CL7, DL5 |

## Necromancer 2125189042: rests at 2/17 HP with 12 CLW

**Cause.** No HP floor makes `borg_recover` use a potion the Borg has:
- `borg_heal` returns at once at danger 0;
- the recovery heal drinks Cure Serious or Critical Wounds, never Cure Light;
- the crow (speed +10) was known, awake and 9 grids away, out of view, so it was worth 0 at a one-turn horizon;
- `borg_check_rest` ignores awake monsters at 5 or more grids;
- the #615 hold is shipped off.

| arm | build | setting | keys sha256 | outcome |
|---|---|---|---|---|
| `off` | `ed6c7ab8` (#999), shipped settings | `recover_rest_cure_hp_percent = 0` | `6f2825472c67b78f` (= the zoo game, = `4b2c2fcf`) | rests at 8342, killed by the crow at 8350, CL2 |
| `on` | `ed6c7ab8` | `recover_rest_cure_hp_percent = 50` (distance 20, edge 1) | `aee7bb2ee27e5831` | 8342: "Cure before rest: HP 2/17, a fast awake crow (speed +10 over the Borg) known 9 grids away, out of view"; drinks one CLW, fights the crow and phases, drinks again at 7/17; alive at the cap, CL6, DL2 |

## Contents

- `*/arms/<arm>/`: the arm's applied `borg.txt` (shipped plus the replay overrides), `keys.log.gz`, `keys.sha256` and `summary.json`.
- `evidence/`: message excerpts for both arms and the off arm's `trace-core` excerpt, around the rests.
- `tools/replay.sh WORKTREE OUT SEED RACE CLASS [borg.txt overrides...]`: the replay. It uses the zoo report's command (borg-zoo#668's reproduction section) on a `BORG_IMPL=rust harness/build.sh` build of the named commit. `sha256sum keys.log` must equal the arm's `keys.sha256`.

## Not done

Both switches ship 0 on the fix branches, and `smoke-borg-rs` is identical. Whether either helps a population is for borg-zoo#671.
