# Disposition: landed fix verified; alternative not deployed

While the alternate P421 branch was validating, independent PR428 landed on
main at d3ebe3c0 (source6b3b9e99). It remembers a preparedness refusal across
a town trip and yields to native play if that trip did not change the refusal.
This work therefore closes alternative PR430 as superseded. The alternative
implementation in earlier receipts was not merged to track-p or main. Those
receipts remain intact, with their own measured source/build/lineage.

An independent clean build of exact d3ebe3c0 was checked against the short
constructed positive-loop regression and all three reported characters. All
finish alive at cap with zero turns at1000 or more keys: constructed peak39,
Half-Troll134, Half-Orc78, Warrior121. Exact commands, actual births, builds,
raw-file hashes and summaries are in LANDED-VERIFICATION.json. PR428's
required Rust, engine and recorder CI is green. No population/survival claim.

The canonical-ID migration landed concurrently in Cemetery. Existing
published paths and payload bytes are preserved as historical aliases;
additive death-id.json files and the regenerated alias catalogue record the
canonical D-SHA256 identities. The eight cases from this branch were already
published at d1ab0406 before that rule was incorporated; their old published
paths are retained, not used to allocate new numeric identities.
