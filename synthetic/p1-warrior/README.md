# P1 Human Warrior bank

This bank generates six new games: seed 101 × starting depths 5/10/15 × birth
and the observed level-5 tier. It contains no run or save bytes. The native
record is a compact declarative projection from a real ordinary run, not a save.

The level-5 Human Warrior was observed at turn 18057 with 58/72 HP. Its tier uses
its observed natural stats, rolled HP progression, gold, mundane equipment and
consumables, charges/fuel and carried-kind awareness. It starts synthetically
at full HP (72), with a fresh Borg and explicitly un-restored historical state.
`catalog.json` binds exact clean source/binary, process/capture and log hashes.
One observation is not a population average or evidence that this kit is common.

The manifest pins the exact engine/Borg source, both character definitions and
all profile/catalog/record bytes. Its required @2 startup verifies the actual
cave before activating either Borg. Generic low-HP and refused-action messages
are diagnostics, not qualified near-deaths or survival improvements.

See `docs/synthetic-suite.md` for the schema, work budget, failure semantics and
commands, and `docs/reviews/M2/` for the milestone evidence/reviewer packet.

P1 birth-tier normalization: `start_build=birth` retains the ordinary,
option-default Warrior birth kit, then applies one-way options. It is **not**
the kit from a native birth performed with `birth_no_recall` already enabled.
At the pinned engine, `lib/gamedata/class.txt:157` conditions the Word of Recall
scroll on that option; a native one-way birth omits it. These three constructed
birth cells keep the scroll and each consumes it at turn 3 with “Nothing
happens.” This declared difference preserves the reviewed P1 streams and is
part of the experiment's limitation, not evidence for native one-way kit play.
The observed tier separately retains its recorded ordinary-source inventory.

The native record's pval ceiling is currently 32767, without a per-kind charge
cap. The fixed observed kit has no wands/staves and every recorded pval is zero;
this bank does not qualify charged/recharged builds. Wider item validation needs
a separate source-side change and new qualification before extending the bank.
