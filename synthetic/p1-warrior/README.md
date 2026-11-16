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
