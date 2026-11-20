# P6 enchant/decurse validation (#680 / source PR #773)

Default extraction at source 710ba18f versus receiving track-p 760fae80:
**45/45 strict harness comparisons pass** for keys/messages/states, with all
45 complete trace@2 streams equal. Suite SHA-256 is in receipt.json. Both
builds are clean and preserve engine 42cd156ac and donor 8c5d000a; this does
not validate newer main or a donor/engine carry.

Override `BORG_PARAM_ENCHANT_TOWN_MAX_TURNS=0` on candidate seed 1001,
race index 1, class index 0, `menu`, cap 100000 changes the first command at
turn 23238/key index 3138: trace think 2210 changes from borg_enchanting to
borg_flow_shop_entry. params-core.json records value 0, origin environment,
default 3501. The key comparison is expected to fail (exit 1); it is a control
witness, not a performance or survival-improvement claim.

The clean baseline and candidate suites each completed 45 runs. These are 45
paired starts, not 90 independent lives. The override reuses one start.
Two source-qualified natural-death packages (baseline/candidate) are retained
byte-for-byte under dossiers; they are paired observations, not two independent
lives. Their IDs/record bytes are not rewritten to force identity agreement.

The initial baseline attempt exhausted disk and then hit missing bc (exit
127). It remains failed; available logs, partial run receipts and missing-case
limits are retained. A clean full retry used locally extracted Debian bc and
compressed completed logs. A post-suite rename raced xz cleanup; the baseline
suite had DONE/result OK, the wrapper reported exit 1, and duplicate raw/xz
bytes were verified before removing redundant raw files. Candidate's wrapper
handled the same warning. No gameplay result was changed or rerun for cleanup.

## Contents and reproduction

receipt.json pins both commits, suite, build artifacts, full per-run receipts,
stream hashes, first override divergence and failures. builds retains exact
binaries compressed with gzip (decompress before hashing/executing), plus
original BUILD_ID. attempts retains each control's original config, effective
parameter/provenance JSON and summary. All equal keys/messages/states/traces
are retained once under streams and hashed for both attempts; this is shared
validation artifact storage, not a reference-only native dossier format.
Native death packages keep every original payload intact. override retains
its differing streams. file-manifest.json hashes every retained file.

In clean receiving checkouts at each exact commit, build using
`BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh`.
Use Cemetery tools at the pinned receipt revision. Run `harness/suite.sh full`
under the shared lock with BORG_CORE=borg-rs, BORG_CORE_OVERRIDES=on,
BORG_ERRAND=none, BORG_STOPSCARED=off, JOBS=2 and private
BORG_DEATH_RECORDS_DIR. No permissive stale/unknown/incomplete switches.
After both complete, `harness/diff --suite full --expect-impl rust BASE CAND`
produces the retained strict result. For the override use the candidate build
and the same environment plus BORG_PARAM_ENCHANT_TOWN_MAX_TURNS=0:
`harness/run.sh OUT 1001 1 0 100000 menu`. Paths are checkout/output roles;
original local paths remain unchanged in captured provenance.

No new fixtures, born-state synthesis, population runs, tuning values or
runtime mutation of published evidence. The source PR remains owner-reviewed
before integration; this evidence publication does not accept the P6 milestone.
