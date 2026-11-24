# Late inventory and Home on a Gnome Mage

This bank contains four constructed starts and two living continuations for Track P [quiver headroom #1168](https://github.com/diegoami/borg-reborn-rs/issues/1168) and [Zoo #764](https://github.com/diegoami/borg-zoo/issues/764). All six files derive from one [observed CL37 Mage save at turn 10815143](../mage-rubble-10815143). Each replay starts with fresh Borg memory and saved engine RNG.

[Receipts](receipts.json) identify the source, build, save bytes, effective configurations and stream hashes. Trials used the shipped borg-rs core at `c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894`, live town planning and no errands.

## Same town, different quiver load

Using the pinned engine's native level transition, move a private copy of the observed save to town at the saved turn. Enable `auto_more` in the private input to work around the pending-message startup bug. Save once with all 300 Rounded Pebbles, then use the native gear removal routine to remove 260 and save again. The native save's RNG, options, stores and player blocks match. Only the gear and messages blocks differ. The source character stats, other gear, Home and store offers start the same.

| Town fixture | Shots at start | First departure | Weight above allowance | Free pack slots |
| --- | ---: | ---: | ---: | ---: |
| `mage-quiver-300-town` | 300 | 10815783 | 131.2 lb | 3 |
| `mage-quiver-40-town` | 40 | 10815548 | 27.2 lb | 10 |

Both runs reached their 3,000-turn cap alive. Removing 260 shots recovered exactly 104 lb. Both first visits sold Restore Mana and bought no devices. This is a named headroom test. Store observations after divergence may differ.

## Equipped CL45 starts

In the private engine before Borg activation, advance the observed Mage to CL45 by engine experience gain, set base/current STR to 18/100 and max and Recall depth to DL45, clear a pending Recall, and restore HP and SP. Keep the original full Home and wearable equipment. Trim only the ordinary shots to 40, then add a Healing rod, six-charge Teleport Other wand, five-charge Teleportation staff, one-charge Speed staff, empty Annihilation wand, unaware Drain Life rod and two each of Vigor and Emergency. Put four Recharging scrolls in the Alchemist and eligible offers of a charged Speed staff and three Restore Mana potions in the Black Market using the native stocking function. Save in town. Use the native level transition to generate the separate DL45 start from that kit. Both start with 21 of 23 pack slots occupied. Ascent and Recall remain available.

- **Town, first 10,000 turns.** Both device settings sold the unaware rod and the mushrooms. Shipped kept the recharged Annihilation wand, attempted 17 shots and bought three Black Market Restore Mana at 1,050 gold each. Rows off sold the three-charge wand and attempted four shots before sale. Both reached their cap alive. The town fixtures share one lineage with the deep fixture.
- **DL45, first 20,000 turns.** Shipped used both staves, attempted 21 Annihilation shots and recharged by spell. The Healing rod raised HP from 214 to 461. The Mage reached DL46 and ended on DL43 alive.

The two `after` files are living saves from the shipped CL45 runs. The town continuation is at CL45/DL0, turn 10825146. The deep continuation is at CL45/DL43, turn 10835144, with max DL46. Restart them with a turn cap greater than their saved turn. The Borg can reset `auto_more` during play. On builds with #1154, use [prepare-resume.py](prepare-resume.py) to enable it in a new private copy if startup stops at a pending message. They provide later checkpoints of the same constructed life.

## Run a private copy

Use a clean build from the pinned source. Run this from that checkout, with `fixture` pointing to this case directory and `trial` pointing to a new private scratch directory.

```sh
mkdir -p "$trial/saves"
gzip -dc "$fixture/late-mage-deep-fit.save.gz" > "$trial/saves/late-mage-deep-fit.save"
SAVE_ROOT="$trial/saves" RUN_TIMEOUT_SECONDS=90 \
BORG_TOWN_PLAN_RECORD="$trial/town-plan.jsonl" \
flock /tmp/angband-validation.lock harness/run.sh "$trial/run" 1 4 1 10835143 \
  menu,keep-load-rng,save=late-mage-deep-fit.save,living-save
```

For the late town pair use `late-mage-town-fit.save` and cap `10825143`. On a separate output path, set `BORG_TXT_SET=borg_param_town_device_percent=0` for the rows-off arm. Keep separate scratch death storage if extending these horizons.
