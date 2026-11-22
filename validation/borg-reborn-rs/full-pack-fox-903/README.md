# Full-pack abort in Fox Form

[Borg issue #903](https://github.com/diegoami/borg-reborn-rs/issues/903) ·
[Zoo #612 stop evidence](https://github.com/diegoami/borg-zoo/issues/612#issuecomment-7072804621) ·
[Original run 44950482392](https://github.com/diegoami/borg-zoo/actions/runs/44950482392)

Half-Elf Druid seed 934061548, native birth, exact 300,000-engine-turn cap.
The original build was `c7ea18dff9f1865bddfebbd5651ca2ad1a533107`.
Both original affected arms re-executed with the original archived binary
and their archived `user/borg.txt` and `user/scary_monsters.txt`. Both key,
message and state logs matched the retained Zoo cell byte for byte.

At turn 78,481 the Druid assumed Fox Form. At 79,360 four Potions of
Slime Mold Juice filled the pack. The junk choice at 79,361 was the older
stack of six ordinary Slime Molds in slot `c`. Eating has no return-to-normal
prompt and the engine's item selector hides the pack while shapechanged.
The rejected `E` leaves `c` at the command prompt. The game interprets it
as Close, consumes a subsequent input as a direction the first time, and
stops on the second direction prompt. The player is alive at 62/62 HP.

The candidate is [7f3d0d61](https://github.com/diegoami/borg-reborn-rs/commit/7f3d0d61b354ae911f131126781b4e4482e09290),
the original pilot plus only the fix. Both candidate streams match the
original up to the 9,722nd key at 79,361, when inscribe (`{`) replaces
eat (`E`). Angband prompts to change back. The Borg resumes normal
shape, marks the food and drops all six Slime Molds. No direction
abort follows.

| Arm | Original | Candidate |
| --- | --- | --- |
| room | borg_stopped at 79,361, CL7 | alive at 300,000, CL9, max DL3 |
| shipped | borg_stopped at 79,361, CL7 | alive at 300,000, CL10, max DL3 |

The original `ctl` and `recall` arms also reached the cap in the retained
Zoo cells. Both candidate starts above are reruns of the same start with
different settings. Neither died.

## Reproduction receipts

Download the build and raw artifacts for run 44950482392. In the raw
archives, find `classes-18-300k/*/reborn-room-{room,shipped}/934061548`.
Copy the two configuration files into a fresh per-arm user directory.
From each build's `game` directory, use `TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8`
and the following arguments with separate directories for all outputs.

```sh
./angband -mborgh -n -uBorg -duser="$out/user" -dsave="$out/save" \
  -darchive="$out/archive" -dpanic="$out/panic" -dscores="$out/scores" \
  -- -seed 934061548 -race 1 -class 2 -turns 300000 \
  -menu-letters -exact-turns -keylog "$out/keys.log" \
  -statelog "$out/state.log" -msglog "$out/messages.log" -summary "$out/summary.json"
```

Use the Zoo binary for the control. For the candidate, use the source pin
above and `BORG_IMPL=rust harness/build.sh` on x86-64 GCC. The local
candidate used GCC 15.2.0 and Rust 1.98.1. Each archived config is used
unchanged on the control and candidate.

| Receipt | SHA-256 |
| --- | --- |
| Original binary | `ac34253303194b39d68e26fec97a249483408a12c96fd27f616fb36ac3c90b19` |
| Candidate source | `f2215654b873033c8b65fa3de2f5c10dbb689f7f87977c45b10acd4451026a67` |
| Candidate binary | `2e144b7d9fccf55633b65f7476864c865611edab2076abf9d3f7f47e8b11d5ff` |
| Room borg.txt | `45ad308a1fb5e41fa657442835771d095b57799093a6273de9844e9374b1e457` |
| Shipped borg.txt | `4141f63a394b49946e5333e82ac01cf9a80f0e7e644a428aaedadb8c65f94646` |
| Original keys, both arms | `77965f45c88a168da2d2b8d02c8c2e6b3003d65f6a6c02f0e8313b4e3b754090` |
| Candidate room keys | `fa8d4a115addf169ebf86f175bd0267b65ee9bda3bc3afc4ee96122b02259844` |
| Candidate shipped keys | `bdce3376408359d96f73900cd4d1c010ec8ccb1e7668bebc96632554d6912e9c` |
