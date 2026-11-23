# Tools

Scripts used for this study. They run from a work directory laid out as follows:

- `cells.jsonl`: `git show origin/results:results/reborn-bfs-full/45121432449-1/cells.jsonl` from borg-zoo.
- `D/<seed>_<ctl|bfs0>/`: one link per death bundle. Fetch the bundles with `gh run download 45121432449 -R diegoami/borg-zoo -p 'deaths-*'`.
- A recorder build of borg-reborn-rs 1c071812. borg-zoo's `.claude/skills/death-report/scripts/record.py` builds `build/recorder/game/angband`.

| script | what it does |
|---|---|
| `poison_episode.py SEED_ARM` | The last poisoning episode from `state.log` (timed index 7 = `TMD_POISONED`): turn, depth, HP, counter, gold. |
| `cf.py ARMS JOBS OUT --game DIR --work DIR [-j N]` | Plays each job (seed, race, class, the bundle's `user/` files) from birth under each arm's `borg_param_*` overrides, writing one JSON line per game with the engine summary. `same_play` says whether `keys.log` hashes to the zoo cell's `play_sha256`. Results already in `OUT` are skipped. |
| `div2.py OUT...` | For each changed death game, the first key where it departs from the original `keys.log`, and whether that is within 2,000 game turns of the death (near) or earlier. |
| `matrix.py` | The per-death × per-arm table in `../evidence/matrix.md`. |

Inputs used are in `../evidence/`:

- `arms.json`;
- `jobs-deaths.json` and `jobs-survivors.json` (the template is each death's own bundle `user/`; survivors use a death bundle of the same arm with `borg_respawn_race`/`borg_respawn_class` rewritten, the only lines that differ between cells of an arm).

Results:

- `cf-deaths.jsonl` (9 arms × 25 deaths) and `cf-prep-deaths.jsonl` (`town_prepared_percent` 25 and 50 × 25 deaths);
- `cf-survivors.jsonl` (6 arms × 18 survivors, including the unchanged `base`) and `cf-prep-survivors.jsonl` (2 arms × 18 survivors).
