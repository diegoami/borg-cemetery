# Dwarf Priest repeatedly swaps a shovel and a dagger on the upstairs

The level 27 Dwarf Priest `Borg261127181053` was alive at DL5 on Track P P-Borg build `f51625f87123daf05b499bc5336664f98f3109cb`. Between game turns 5,131,391 and 5,153,067, the recorder shows 2,026 successful wield commands alternating Narthanc and a Shovel of Earthquakes. The Priest stayed on the upstairs. At the final decision he had 219 HP, 95 SP, and zero estimated danger. This incident concerns [borg-reborn-rs #1361](https://github.com/diegoami/borg-reborn-rs/issues/1361).

The [evidence archive](borg-priest-shovel-swap-loop.tar.gz) contains the original native save, the exported Borg map, settings, turn-bounded live combat and decision streams, and the bounded reload output. Its two named saves have identical bytes and are both from turn 5,153,079. The [archive checksum](SHA256SUMS) and the manifest inside it cover the retained bytes. The complete recording stays on the originating machine.

## Reproduce from the saved position

Use the headless game from the pinned revision. Extract the archive, verify its internal checksums from the extraction directory, and run the binary from its game directory (where its `lib/` lives). `evidence` is the absolute path to the extracted directory.

```sh
evidence=/absolute/path/to/extracted/evidence
run=$(mktemp -d)
mkdir "$run"/{user,save,archive,panic,scores}
cp "$evidence/borg-settings/"* "$run/user/"
cp "$evidence/repro.save" "$run/save/Priest"
TZ=UTC LC_ALL=C.UTF-8 flock /tmp/angband-validation.lock ./angband -mborgh \
  -duser="$run/user" -dsave="$run/save" -darchive="$run/archive" \
  -dpanic="$run/panic" -dscores="$run/scores" -- \
  -seed 1 -race 5 -class 3 -load "$run/save/Priest" -keep-load-rng \
  -exact-turns -turns 5153379 -msglog "$run/messages.log" \
  -summary "$run/summary.json"
```

The bounded reproduction on that revision repeatedly wielded both pieces and reached turn 5,153,379 on DL5. It started with fresh Borg memory and preserved the engine RNG stored in the save. The seed argument satisfies the harness and is not the original birth seed. This reproduction exercises the loop from a native checkpoint. It does not reexecute the full live recording.
