# CL37 Gnome Mage rubble and restoration trials

The [owner-saved checkpoint and settings](https://github.com/diegoami/borg-cemetery/tree/aa15e7df8cf2226beab29e93094b7d7c8b8f4d40/scenarios/mage-rubble-10815143) are from turn 10,815,143. The native recording is the reproduction evidence for the 7,856 failed sprays and the [recorded potion losses](https://github.com/diegoami/borg-cemetery/pull/123). Alchemist stock in that recording remains unknown.

## Acid Spray and movement

Candidate source [5d1319b2962a59e2f9c4e612ebdc0c8d542c9ac8](https://github.com/diegoami/borg-reborn-rs/commit/5d1319b2962a59e2f9c4e612ebdc0c8d542c9ac8). The ordinary headless frontend reloaded at the correct turn and stopped with zero keys. Its startup script delivered the Borg toggle into a pending load message. A trial executable acknowledges that prompt before starting the Borg. The original checkpoint and saved engine RNG are used, with newly initialized Borg memory.

The first eligible combat decision scored Acid Spray below zero and chose movement. With just the scoring fix, the Mage moved five squares and began repeatedly waiting east of the rubble. With the combat-wait check fixed too, it stood on the rubble at (127,56), killed the original dog with its axe activation at 10,815,215 and resumed exploration. At the 10,815,343 cap the Mage was alive at (118,55), with 107 logged keys and zero new Acid Spray casts. The three default smoke games matched their references.

A second trial carved a short lane and added a wild dog at (126,54) with the original dog and rubble still present. The Borg recorded the added dog on initialization and Acid Spray scored +43 at turn 10,815,179 after two steps west. It chose Fire Ball. This is a constructed variant of the same encounter.

## Restore Life Levels

Candidate source [6a80619a764cecb6f6967c428bb791a2a676dc86](https://github.com/diegoami/borg-reborn-rs/commit/6a80619a764cecb6f6967c428bb791a2a676dc86). An initial trial added one known potion to the checkpoint, but the unresolved combat from the independent base continued to take priority during the 200-turn window. For the controlled recovery trial, the setup also removed the level's monsters. The Mage started at 711,985/714,369 XP. At turn 10,815,161 the Borg quaffed Restore Life Levels. Angband printed “You feel your life energies returning” and XP reached 714,369. The 713,458 XP figure in the original report was the pre-drain reading, while 714,369 is the saved maximum verified in this trial.

The source regression uses the live town decision solver with an Alchemist offer priced at 400. It chooses Buy when drained at both 400 and 787,811 gold, and when healthy with a one-copy reserve enabled. It leaves when the offer is absent or unaffordable. A healthy Mage with one carried copy sells it with the reserve off and keeps it with the reserve on. Dungeon junking covers one-copy drops, whole-stack drops, and the desperate full-pack fallback. These are controlled tests. The original shop visits did not establish offer availability.

## Reproduction

Build the cited source with `BORG_IMPL=rust harness/build.sh` on x86-64 GCC under the validation lock. Run `python3 build-trial.py SOURCE OUT` for the untouched encounter, adding `mixed-dog.c.inc` or `carried-potion.c.inc` as a third argument for the corresponding constructed trial. The script recompiles the local headless frontend object and links an isolated binary.

Verify and unzip the pinned save into `OUT/start.save`. Copy the pinned `borg.txt`, `errands_plan.txt` and `scary_monsters.txt` into `OUT/user`; create `save`, `archive`, `panic`, `scores` and `diagnostics` under OUT. Use absolute paths and run from the build's game directory.

```sh
BORG_CORE=borg-rs BORG_RUN_DIR="$out/diagnostics" \
BORG_ERRANDS_PLAN="$out/user/errands_plan.txt" \
"$out/angband" -mborgh "-duser=$out/user" "-dsave=$out/save" \
  "-darchive=$out/archive" "-dpanic=$out/panic" "-dscores=$out/scores" \
  -uRubble -- -seed 1 -race 4 -class 1 -load "$out/start.save" -keep-load-rng \
  -turns 10815343 -keys 1000 -menu-letters -summary "$out/summary.json" \
  -msglog "$out/messages.log" -statelog "$out/state.log"
```

Saved message history has turn zero in the exported logs. Assess trial behavior only on messages with turns at or after 10,815,143 and the matching Borg decision trace. All branches share one starting life.

## Validation receipts

The unchanged default borg-rs smoke references matched all three runs for
each candidate. An intermediate restoration candidate applied split quantities
to every town drop. The Warrior differed at turn 4,648 when it dropped one
Potion of Confusion instead of a stack of four. The final candidate limits
the split to the enabled restoration reserve, and all three logs match again.

| Trial | Isolated binary SHA-256 | State log SHA-256 |
| --- | --- | --- |
| Checkpoint with startup acknowledgment | `c06154e92cba8b6362f50fc6e92306d05414791eb3fd8839204d13b42fa541b3` | `4385d75b8d26af80af01d08957ad076053005b98d25adf248c858316383ce711` |
| Constructed clear dog | `ec2ba70fa7fcbbd94ffd06a8a3240a3c29b9a9644d3bbb1a40628c3e85e4cc74` | `efdf691e64952a6343671652fad7ae40bf2357f4b914cb8b8279081f57518dec` |
| Constructed carried potion | `e438c85dada0fd147381b1ebdc48b31eb22c800a79ee6ea51fcfce95d0fd7e1d` | `172506a0ec49d2c0dd8075a394962cdba7ab36c3f99db87be63a0b91f2533ca0` |
