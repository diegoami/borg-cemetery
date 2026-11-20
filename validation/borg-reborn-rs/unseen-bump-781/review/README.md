# Review follow-up for reborn #782

Implementation pin: `5d53f8b571f1b9c96cc73bf3185af5b8d6642b69`, synchronized
through main `d7e58cdf`. Initial review-fix runs use `a678c329` on main
`fcaecf2b`, identified separately in `builds.json`. The historical reconstruction
is upstream source `09a70906` plus `historical-review.patch`. The preserved
pre-review executable is the earlier historical-final build (`2e28b05f…`
source identity), whose exact patch remains in the parent case.

All16 newly attempted games/process launches are retained here. They replay
the same one Druid seed and three smoke identity seeds; they are not
independent lives. Six attempts ran games successfully but failed afterwards
because the local default Cemetery tools did not match main's newly adopted
pin. These are `exporter_pin_mismatch`, not successful harness attempts. One
copied-executable launch failed before starting a game because its relative
`lib/screens/news.txt` was absent; that is `missing_game_data`, not a death or
survival. After providing the exact pinned tools/game data, the reruns passed.
No attempt was overwritten or excluded. The final local duplicate smoke was
cancelled while queued behind another session's shared lock, before any game
started; no final local game outcome is claimed. Latest-head CI supplies that
smoke receipt. The clean final executable/build identity is retained too.

## Findings and changes

The original review's F1 runtime premise was not reproduced. In
`generate_keypress`, messages are parsed and queued keys/directions returned
before calling `borg_think`/`borg_update`. Its cited second throw follows a
miss, then kills. In the original preserved current-main stream, the sequence
at62584/62594/62604 is: miss, second throw kills, next think walks. Likewise
the three misses at69691/69701/69711 are not throws after a confirmed kill.
The old kill confirmation did work on this ordinary command ordering.

The implementation is nevertheless hardened to support the requested
intermediate-update ordering. An unresolved shot now survives such an update,
then clears on death confirmation, the oil-break resolution, cancellation,
expiry or entry into its grid. Miss completion cannot carry attribution into
an unrelated later death. New tests cover each boundary and the review's
synthetic delayed-feedback case. Queueing reserves one attempt of the grid's
budget, including cancelled attempts; one command is queued per response.
A nonlethal hit correctly leaves the observed occupant in place.

Other review changes: the response follows ordinary healing, defence, Recall
and food; detection reuses existing danger/darkness gates; the independent
cure's deliberate bypass of both danger gates is explicit; bump phases keep
emergency landing tests and increment ordinary level escape accounting;
twitch movement supplies the same evidence and refuses a remembered occupied
grid before queueing a prefix. `caution_escape_limit` triggers leaving rather
than forbidding subsequent escape actions. Historical section counts stay
historical; the current registry has2270 parameters, four beyond main. The
Phase Door table includes the site, and source documentation links are pinned.

The original cure calculation also checks out directly: of110 final caution
rows,70 meet the30% wound gate. The first is turn37069, HP29/44, danger76.
All70 fail BOTH `danger < HP+20` and `20 > danger/3`. The investigation's
original description of non-overlapping gates is accurate, rather than a
zero-danger explanation. The source handover now supplies those exact counts.

## Bounded observations

| Reconstruction/check | Result at100,000 | Oil attempts | Explicit kill clears |
| --- | --- | ---: | ---: |
| Historical pre-review, memory200/response1/cure50 | alive, CL7/maxDL2 | 13 | old implementation had no clear log |
| Historical combined review changes, same settings | alive, CL7/maxDL2 | 7 | 3 |
| Main fcaecf2b control | alive, CL9/maxDL2 | 0 | 0 |
| Review a678c329 disabled, same main | identical control keys (`2e18e8eb7ace7b78…`) | 0 | 0 |
| Review a678c329 enabled, memory200/response1/cure50 | alive, CL8/maxDL3 | 8 | 4 |

The historical disabled review reconstruction again dies at37759, clear icky
thing, with the exact original key SHA-256 `8b21c6b94e80e969…`.
Multiple review policies changed, so the reduction13→7 is not attributed to
one fix or called six wasted flasks saved. No population comparison or
recommendation follows. The new Detect Invisible call remains unexercised by
these seeded games. A kill-clear note establishes processing of the actual
kill feedback; a later throw following a miss is not classified as waste.

Local fmt/clippy/workspace checks,540 release-core tests,39 script tests,
96 tool tests, parameter citations and vendor integrity pass. The clean
review-fix smoke at a678c329 matches3/3 keys/messages/states against its main's
reference. The final head builds clean; its CI receipt is retained alongside
these records. No population experiment was dispatched; all new switches
remain compiled/shipped0. Both source/evidence PRs remain subject to owner
review disposition.

`receipts.json` hashes decompressed original bytes. `verify.py` checks custody
and process identity while retaining the expected operational failures.
`deaths/` preserves the newly exported historical control package unchanged;
it shares the original start/key stream and is another replay of that life.
