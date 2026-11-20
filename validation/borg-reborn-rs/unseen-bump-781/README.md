# Unseen monster on the escape step: reborn #781

Source task: [reborn #781](https://github.com/diegoami/borg-reborn-rs/issues/781).
Implementation: [PR #782](https://github.com/diegoami/borg-reborn-rs/pull/782),
initial head `155943c0c7a2fbfc7e31662a4fb3f0960c653f71`, final delivery
`f1d3c576d2b92f9dc13656318f92eb51a4f6e2ac`. Engine: upstream `574b618c`,
unchanged. Default borg-rs core, Human Druid, seed **102023799**.

These are bounded regression checks of one seeded life, with alternative
policies and repeated controls. They are not independent lives, a population
experiment, or evidence for changing shipped values. The three smoke seeds
were each repeated for identity checks. No attempted game was dropped.

## The original failure and why cures did not fire

At historical main `09a7090650bf837702d5ab3345a7401532114cf8`, the control
matches the reported key SHA-256 exactly:
`8b21c6b94e80e9692c45c4dcf88352d351c3f88db19bc11c189a2330cf613124`.
It dies at game turn **37,759**, CL4/DL1, to a clear icky thing.
From turn 36,669 it stays at (y40,x35), attempting north toward the upstairs.
Player melee messages report “You fail to harm something.” The walk neither
recognizes occupancy nor progresses. Its incoming blows supply regional fear
without a located monster.

The preserved core trace contains **110 caution decisions** from turn 36,669.
The first has HP41/44 and danger24; by turn37,189, HP21/44 and danger99; by
turn37,709, HP3/44 and danger162; danger reaches170. Thus the problem is **not
zero reported danger**. `borg_heal` runs before stair desperation even while
fleeing, but CLW requires wound percentage≥30, `danger < HP + 20`, and
`20 > danger/3` at the recorded settings. No one of those 110 decisions passes
all three. The initial small wound fails the percentage gate; by the time it
qualifies, accumulated fear makes the survivable-healing gate fail. The
additional random healing skips can only reject more decisions.
The recover-unseen switches were both0, and recovery is downstream of the
successful desperate walk anyway. Incoming “Something touches you” locates no
specific square and is insufficient evidence for the new occupied-grid memory.

## Change and observations

A queued unimpaired step plus outgoing unseen melee feedback plus an unchanged
observed position marks the destination occupied. All flow seeds, spreads,
old-flow steps, stair-distance calculations and resulting stair-path costs
respect the memory. It expires in game turns, resets on level change and
clears on successful entry. This does not invent a race, HP, AC or monster
index. Normal visible monster handling remains available after detection.

An optional caution response, before the desperate walk, tries a carried
Detect Invisible scroll once, bounded oil throws into the adjacent direction
under the existing fuel reserve, then Phase Door. A separate HP threshold
allows a known cure before the walk without requiring danger to fit the
unknown monster. This Phase Door site uses confirmed bump evidence instead
of the known-race-only adjacent fight test; it does not establish landing
safety or that the unknown fight is lost. Both are limitations for measurement.
All behavior remains compiled and shipped off.

The enabled game diverges **earlier** than the terminal staircase: at turn
10,703 it infers an unseen occupant east of (y30,x77). Oil kills that unseen
monster. This changes later play, so survival does not prove an alternative
at the exact old terminal position. A preliminary implementation kept the
grid occupied after “It dies.” and wasted two further throws and a Phase Door;
that full attempt is retained. The final implementation associates the
single-target directional throw's death feedback with its grid, clears it,
and does not feed directional throws into target-wall guessing.

Historical final responses (100-turn memory, response1, cure threshold50,
three throws) survive to100,000, CL7/maxDL2. Occupancy/cure-only (response0)
also survives, without needing the new cure. Zero throws exercises five
Phase Doors and survives, CL6/maxDL1. The explicit cure-threshold100 probe
exercises the new cure priority and survives, CL5/maxDL2. Threshold100 is a
coverage probe, not a recommended setting. The threshold50 runs do not
exercise this cure call. No run exercised the new Detect Invisible call;
finding or buying that scroll is not counted as exercising it.

Current main `4e9af99e` already survives after #768: CL8/maxDL2 to100,000,
key SHA-256 `4cb7bb4376932733cbf11100e7a3c60f8694392e43c88c30fb93f1781699cc74`.
The disabled patched run is identical. Clean delivery head's enabled run
survives to100,000, CL8/maxDL3. These descriptive endpoints do not establish
an improvement. The 100-game-turn memory, three-throw budget and50%-HP cure
threshold are hypotheses only, and the behavior switches remain0.

## Reproduce and verify

`receipts.json` lists every attempt, exact configuration, original raw file
hashes, process result, executable hash and event counts. Files over100kB are
gzipped; hashes in the receipt refer to **decompressed bytes**. `builds.json`
retains build identities. `deaths/` retains all three exporter-created
packages, without changing IDs or published payloads. All three deaths have
the same original start/key stream, so they are repeats of one life despite
the configuration/provenance-specific exporter IDs. They do not count as three
distinct deaths. None of the enabled attempts died. `verify.py` checks file
custody, process results and binary identity against the receipts.

The historical builds use the retained patch on top of `09a70906`, not current
main with its changed dive gates. The preliminary source patch was reconstructed
and its input SHA-256 verified against its contemporaneous death build receipt.
The intermediate current-main patch omits the final glyph-step hook, and its
source hash is independently verified against the contemporaneous smoke
manifest. Final historical patch source hash is in `builds.json`; it predates
only the glyph-step hook added for final delivery. Source hashes and compiler
versions, rather than local directory names or binary reproducibility across
compilers, identify these builds.

```sh
git clone https://github.com/diegoami/borg-reborn-rs SOURCE
cd SOURCE
git checkout --detach 09a7090650bf837702d5ab3345a7401532114cf8
# CASE is the absolute path to this Cemetery directory.
git apply --check "$CASE/historical-final.patch"
git apply "$CASE/historical-final.patch"
bash scripts/setup.sh
BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
# Disabled: exact original death and key hash.
BORG_DEATH_RECORDS_DIR="$PWD/validation-deaths" \
  flock /tmp/angband-validation.lock harness/run.sh OUT-OFF 102023799 0 2 100000 exact,menu
# Enabled: bounded alternate play from birth, not a restored Borg memory.
BORG_DEATH_RECORDS_DIR="$PWD/validation-deaths" \
  BORG_TXT_SET='borg_param_caution_unseen_bump_turns=100;borg_param_caution_unseen_bump_response=1;borg_param_caution_unseen_bump_heal_hp_percent=50' \
  flock /tmp/angband-validation.lock harness/run.sh OUT-ON 102023799 0 2 100000 exact,menu
```

The normal exporter needs the Cemetery checkout at `death-tools-pin.txt`
(or a checkout whose native-tool bytes match). The three historical patch
files are audit inputs, not an adopted fork or a source pin update.
To check the shipped identity, build clean delivery commit155943c0 and run
`harness/suite.sh smoke`, then `harness/diff --suite smoke --expect-impl rust
OUT harness/reference/smoke-borg-rs`: retained clean-build result is3/3 exact
keys/messages/states. Workspace fmt/clippy/tests,510 release borg-core tests,
39 script tests,96 tool tests, vendor/citation checks pass. Reborn-core full
suites and population comparisons were not run.


## Delivery refinement: all engine melee verbs

Final delivery f1d3c576 additionally recognizes every brand/slay/shape melee
verb at the pinned engine (including smite/burn/freeze), with a corpus test
against brand.txt, slay.txt and shape.txt. Directional oil also clears an
unseen nonliving victim on "It is destroyed.". This extends coverage beyond
the initial hit/miss/fail-to-harm case without changing the switches or shipped
values. Release tests:511 passed,4 ignored; workspace clippy and parameter
citations pass. The clean final smoke again matches3/3. Final enabled Druid
keys are identical to the previous current-main enabled run:
`949307338b60b03e6df33e25a0a314eeeb8d498a69407b3694d23637bcabf355`.
The four additional attempts are retained, bringing this case to22 attempts:
13 plays of the one Druid life and nine repeated smoke identity checks.
No additional death occurred, and no new runtime detection coverage is claimed.
