# Historical controller and parameter replay validation

Two configurations of seed 102, Elf Mage, were executed and replayed on clean
reborn source `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d` using its already-built
executable. Both replays matched their original endpoint and all three
key/state/message hashes, with `reproduction_verified: true`.

| Configuration | Original input | Death endpoint | Replay |
| --- | --- | --- | --- |
| Native borg-rs | `BORG_CORE=borg-rs`, `BORG_CORE_OVERRIDES=off`, `BORG_PARAM_CAUTION_CLW_MIN_LOSS=20` (default 30) | Grip, turn 23324; CL2, DL1, max DL2 | Same binary, parameter bytes/origins and all three streams |
| Historical reborn | No BORG_CORE variable and no borg_core config entry | Grip, turn 3640; CL1, DL1 | Explicit historical reborn selection; same binary, configuration, endpoint and all three streams |

The native replay inherited `BORG_CORE=reborn`,
`BORG_PARAM_CAUTION_CLW_MIN_LOSS=99` and unknown `BORG_PARAM_UNKNOWN=1`.
It restored 20 from the receipt and cleared the unknown setting. The historical
run's unmodified config genuinely predates mandatory controller recording; it
was not edited to simulate a missing key. Regression tests separately exercise
an ambient native controller against that fallback and class-specific origins.

These are correlated configurations of the same seed/race/class, followed by
their reproductions. Four executions are not four independent lives or a
population/policy comparison. All natural deaths are retained, including CL1.
No gameplay policy, runtime or prior milestone evidence changed. These are
birth runs without input saves, not fresh-Borg saved-scenario continuations.

## Identities and retained bytes

`BUILD_ID` retains source digest
`bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a` and executable
digest `68ed3ed7108a2d675efb94de2206ab8ea24a5ad46e40009813d24f7f7e55187d`.
That executable was reused; bit-identical rebuilding is not claimed.
`validation.json` records runtime game-data hashes, the validated tool hash,
original environments, endpoints and archive hashes. `reborn-default.txt` is
the exact profile read in both configurations.

Each controller directory contains the original D-SHA256 dossier with unchanged
record/payload bytes and additive ID, reproduction receipt and launcher output.
Its `streams.tgz` retains the complete original and replay output: input
borg.txt, configuration/parameters, gameplay streams, native trace or reborn
observation/world/knowledge logs, and process diagnostics. Repeated exported
dossiers under `not-exported` are omitted as duplicate evidence of the same life;
their game streams and original canonical dossiers are retained.

Existing dossier raw_directory paths name the execution workspace, not another
authoritative store. Recover the bytes from these checked archives after temp
workspaces disappear. Reproduction receipts bind each original record hash;
`validation.json` binds records and archives. Both source/build configurations
and their expected outcomes/streams are retained without recorder dependency.

## Re-run

Use a source checkout/build matching the recorded executable and game data.
A differently rebuilt binary is diagnostic only. From Cemetery, substitute
the exact case path in `validation.json`, a fresh output and the exact source:

```sh
flock /tmp/angband-validation.lock python3 scripts/native/rerun-death.py \
  validation/borg-reborn-rs/historical-replay-settings/CONTROLLER/death/D-ID \
  /tmp/fresh-death-rerun --source-root /path/to/exact/borg-reborn-rs
```

The source consumer pin is adopted separately. These actual checks used the
older runtime's API-1 forwarding support with an explicit toolkit directory;
they do not qualify current-source gameplay policy. Historical binaries and
native tool receipts stay bound to their original source/configuration.
