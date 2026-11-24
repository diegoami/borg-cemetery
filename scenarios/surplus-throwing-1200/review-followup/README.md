# Review follow-up for #1200

The tested code is `31ca4dfc4d633d091141505d13436fe750c37f37`, synced
with Track P `20ac7d1903b9a018d0c81fe67d5441a36b483062`. With surplus
throwing enabled, ordinary throws and spare weapons now use native range
and the same throw damage and hit scoring. The spare-weapon value cap is
independently configured at 100 gold.

All four shipped smoke starts matched the current references. All 15
original named replays reproduced keys, messages, state and core traces.
The added CL17 Mage case carries three flasks and a spare dagger, and
sees a kobold at nine tiles while wearing no launcher. Both arms use
`attack_throw_as_melee=0`. At surplus flag 0 there is no throw during the
21-turn run under the historical six-tile limit. At flag 1 the Mage
throws oil from nine tiles, then throws again and hits for 36 damage.
A companion fixture retaining a launcher threw oil in both arms, since
that launcher already puts nine tiles inside the legacy aiming limit.

[Receipts](receipts.json) pin the current build and all arms. [Replay](replay.sh)
runs the comparison from that build. The [author code](fixture.inc)
adds the oil and constructs the two launcher states from the Mage save.
