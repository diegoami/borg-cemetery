# P6 reconciliation: local named-case and smoke evidence (#774)

Source PR borg-reborn-rs#783 synchronizes track-p e9670cab with exact accepted
main 4e9af99e. Runtime build 27700983, published candidate d0657712, engine
574b618c, donor8c5d000a. source-proof.json pins both parents and trees, confirms
the exact reviewed #680 modules and subtractive preservation of main's parser.
The only runtime delta against main is the reviewed neutral four-file P6 delta.
No extra donor carry, profile tuning or engine adoption is performed by this
reconciliation beyond preserving main's already accepted work.

**Local scope:** native borg-rs smoke is 3/3 identical for keys/messages/states
against retained main smoke-borg-rs references. One named #680 case (seed1001,
race1/class0/menu/cap100000) still demonstrates actual control: environment
ENCHANT_TOWN_MAX_TURNS=0 (full variable BORG_PARAM_ENCHANT_TOWN_MAX_TURNS)
changes key index10604 at turn80689. Trace think7928 goes from borg_enchanting
with read/select keys to borg_flow_shop_entry with key57. The parameter record
shows default3501, value0 and origin environment. Both named runs stop alive at
the cap. No natural deaths occurred in these five local checks.

The required new broader build comparison is **pending Zoo #520**. The source
now routes comparisons over sets of starts to Zoo (RULES20), so no new local
full45 cohort was run. The Zoo request pins both builds, requests its pilot
first and an owner-gated exact-native45 follow-up. Neither old #680 full45
nor local smoke is being relabelled as that result or a latest-main proof.

Checks: 505 release-core tests/4 ignored, fmt/clippy/workspace/vendor,
2264 citations, 39 script tests, 96 tool tests and 92 engine/contract tests
(4 skipped). The first engine test setup failed because a shared Zoo checkout
was not at the retained pin; a local shared-clone attempt also lacked cached
promisor blobs. A fresh direct clone at exact Zoo7b373a70 fixed the local test
input, without changing any source/pin or weakening a test. Failure and final
check logs are retained. Build is clean; smoke was run with documentation-only
checkout dirtiness during citation cleanup, inputs unchanged and overrides=none.

## Artifact map and reproduction

runs/smoke and smoke-reference retain both sides of the three-case smoke check.
runs/named-default and runs/named-override retain each **own** complete
trace/keys/messages/states plus original summaries/configs/effective parameters.
The standalone default trace is explicit, not inferred from the override.
build retains the exact executable (gzip; hash after decompression) and BUILD_ID;
inputs pins the receiving settings, suite, engine and native tools. receipt.json
records identities, results and first divergence. file-manifest.json hashes all
other retained files. Original captures are not edited to improve presentation.

Build the exact source with BORG_IMPL=rust harness/build.sh under the shared
lock. At the pinned tools and current receiving settings use BORG_CORE=borg-rs,
BORG_CORE_OVERRIDES=on, BORG_ERRAND=none, BORG_STOPSCARED=off and private
BORG_DEATH_RECORDS_DIR. Run harness/suite.sh smoke, then harness/diff --suite
smoke --expect-impl rust OUT harness/reference/smoke-borg-rs. The named runs
are harness/run.sh OUT 1001 1 0 100000 menu, once at defaults and once adding
BORG_PARAM_ENCHANT_TOWN_MAX_TURNS=0. No stale/unknown/incomplete switches.
Do not turn this named-case recipe into a local cohort; broader requests go
to Zoo. Capture local paths exactly and use the receipt's checkout/output roles.

## Additive clarification of earlier #773 evidence notes

The original default witness trace is already retained byte-for-byte at
[0529ff6f streams/full-0-warrior-1/trace-core.jsonl.xz](https://github.com/diegoami/borg-cemetery/blob/0529ff6f7208b197a5ee156be180395e7fbef38e/validation/borg-reborn-rs/enchant-decurse-680/streams/full-0-warrior-1/trace-core.jsonl.xz).
Its original comparison side is the paired suite case, not missing data.
The original checks/t680-native-override.log is empty because harness/run.sh
is quiet on success; the native transcript is in override/ and
checks/t680-override-diff.log of that same immutable bundle. The new local
bundle likewise retains stdout as captured and labels results explicitly.
No old bundle, hash, death identity or independent-life count is rewritten.

This is validation evidence, not owner acceptance of #774/P6 or authorization
to promote source main. The source PR remains gated on review, CI and Zoo
comparison disposition. No R carry, tuning or survival claim.
