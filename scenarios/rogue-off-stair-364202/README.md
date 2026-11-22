# Hobbit Rogue stair loop on dungeon level 5

[borg-reborn-rs #1052](https://github.com/diegoami/borg-reborn-rs/issues/1052) records the stall. At character level 12 and full health (89 HP), the Rogue made 430 moves between (78,40) and (77,41) from turn 359,902 to turn 364,202. Coordinates are (x,y). The terminal map placed the down staircase at (79,41), and the Borg had stood on it at turn 359,862. The owner interrupted the Borg and saved before moving. Frame 85,029 is the saved position.

At turn 359,882 the Rod of Light fired down the hallway. A radiation eye at (61,41) had 11 HP and was out of sight. The next frame dropped that eye from the engine's monster list and gained two experience points. It was the only monster removed in that frame, and the engine reported a scream of agony. At turn 359,892 the Borg interpreted the sound as a death message but tried to match it as a player ghost. It then reported the eye's old location and danger 115 at (77,41). That danger estimate and the down-stair decision recur whenever the Rogue returns to that tile. The recording shows the eye was already dead. The log does not break the aggregate risk score down by source.

- [Recorded positions](recorded-positions.tsv) include pre-loop context and every movement. Monster columns come from recorder diagnostics and were unavailable to the Borg.
- [Recorded messages](recorded-messages.tsv) include the Rod of Light, the death sound, and each alternating exploration and escape decision.
- [Save and runtime inputs](scenario.json) pin the exact commit, executable checksum, and settings from the recorder session. The session's original birth seed is unknown.
- [Same-build reload](reload-summary.json) played 212 keys and reached the global cap at turn 365,200. [Its positions](reload-positions.tsv) show the Rogue moved away from the staircase to (110,55), still on dungeon level 5. Loading restores the engine RNG but starts a fresh Borg. Use the uninterrupted trail to reproduce the decision pattern.

## Load the save

Decompress `start.save.gz` to a private Angband save directory and put the three captured settings files in your private user directory. Using the pinned executable and headless frontend, with the user directory set through the launcher's usual options:

```sh
angband -m borgh -- -load /absolute/path/to/save/load -keep-load-rng \
  -seed 1 -race 3 -class 6 -turns 365200 -keys 250 -menu-letters -exact-turns
```

The seed argument is a load request value. The engine's saved RNG is used for play.
