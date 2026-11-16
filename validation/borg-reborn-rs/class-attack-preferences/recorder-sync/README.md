# Synchronization with the recorder v0.2.0 review baseline

Track-p advanced through recorder adoption #393 to46d5f2ae while preference
validation ran. Its review #407 freezes that integration head. The preference
branch merges it as25e89494, retaining all recorder files and both handovers;
it does not move the frozen target or claim recorder milestone acceptance.

Fresh clean25e89494 versus clean46d5f2ae passes strict full45/45 keys/messages/
states parity with no stale-build override. Actual source/binary/config identities
and per-run hashes are retained here. The candidate's recorder-off executable
hash is identical to the earlier pre-sync candidate, but source identity changes
because the full build-input contract includes the recorder pin/vendor/adapter.
Earlier exact-build evidence remains historical and unmodified.

336 native tests (four existing ignored),165 workspace tests, formatting and
Clippy pass again. All70 engine tests pass with two local skips, with the pinned
zoo profile and four saved-position incident checks required. The actual weighted
Mage selection still changes; its observed candidate row is retained. Non-neutral
native validation uses a separate retained/reconciled registry, leaving the
original-core observation replay in its own registry. A real original-core Fang
smoke death reproduces exactly through the existing replay tool (50491fa13924...).
Native calibration restoration is a separate tooling gap tracked in Cemetery#13.

This is recorder-off compatibility/mechanism validation, not a new survival or
population claim. Repeated controls and source-qualified packages are not
independent life counts. R carry and P promotion remain behind owner review.
