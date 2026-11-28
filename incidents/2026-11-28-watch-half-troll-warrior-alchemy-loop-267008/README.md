# Half-Troll Warrior loops on the Alchemy Shop entrance

The level 10 Half-Troll Warrior `Borg261128034455` was alive in town at 128/128 HP on P-Borg recorder build `cae077d67c6fadeb49ff1603acc68aca1a1f5c04` (borg-reborn-rs PR #1392). At turn **267,008**, the live trace shows 1,320 visits to the Alchemy Shop with zero game turns elapsed. Each `borg_flow_shop_entry` decision queues `5`, and each `borg_think_store` decision queues Escapes without a transaction. The Borg ultimately abandoned shopping and entered DL1. This is a nonfatal incident supporting [borg-reborn-rs #1395](https://github.com/diegoami/borg-reborn-rs/issues/1395).

The Borg map captures turn 267,008. The case preserves original saves from turns 266,801 and 267,047 and the trace between them. An exact-turn save was loaded with fresh Borg memory and saved engine RNG. The continuation sold Cure Light Wounds and advanced to 267,108. The game overwrote the working copy during that trial. The archive retains the post-reload save, replay logs, and planner records. Old messages restored from the save appear at turn zero in that log.

The original recording has not been reexecuted. The live shop goal is unavailable in a save, and the specific action rejected at the shop boundary remains unknown. The local pack-slack value was `-1`. This case does not establish that setting as the cause.

The [evidence archive](borg-warrior-alchemy-loop.tar.gz) contains the original saves, Borg map, exact recording settings, live trace excerpts, and the fresh-memory comparison. The [archive checksum](SHA256SUMS) and the manifest inside the archive cover the retained bytes.
