# Druid seed 202: recovery ignores repeated unseen attacks

This natural death is retained, not discarded for failing a level-2 capture.
Original death and full three-stream hashes reproduce from birth using the
recipe in `reproduction/druid-seed202/`. Source/build identities are those in
`build.json`; the capture-off control has identical key/state/message streams.

At turn 7608 the log first says “Something touches you.” Repeated touches reduce
HP. The final two decision traces, turns 7804 and 7814, select `Rest(75)` with
`mode: recover`, rule “hurt and safe: recover”, and `expected`, `worst` and
`p_death` all zero. At 7814 the character has 1/13 HP and 2/2 mana. It dies at
7818 from a clear icky thing. The logs establish unsafe recovery while taking
unseen damage; they do not establish that a particular spell/escape would work.
The killer's actual identity is postmortem information, not information to give
the playing Borg.

The fast scenario `druid-unseen-contact-202` starts at turn7605, with13/13 HP
and2/2 SP, three engine ticks before first contact. It therefore exercises the
onset and the Borg's opportunity to respond, rather than starting at1 HP.
A fresh reborn Borg from that save still dies at7818, consistently across three
trials. Saved engine RNG is preserved; private Borg memory is not restored.
This is a local regression case, not a population finding or a completed fix.
