# Two stair routes reverse a live Borg (#807)

Source task: [borg-reborn-rs#807](https://github.com/diegoami/borg-reborn-rs/issues/807).
The recording is an observed X11 game on `2801ba188b1f46ddfdd32eeb7ae7c58330b0fd30`,
with the v0.2.0 recorder. Dunadan Warrior DBorg, CL14, on DL3. The session
was stopped by the player, alive. This case reports a path loop, not a death.

`actions.txt` and `messages.jsonl` excerpt the original recorder streams.
`positions.jsonl` projects command frames onto their turn, grid, depth and HP.
The final uninterrupted suffix uses southwest/northeast movement keys (`1`,
`9`) for 388 actions, turns 382115 to 385985. At turn 385995 the user aborts.
The positions are `(77,16)` and `(76,17)` with 188/188 HP. The logs alternate
between a 118-move up-stair route from the desperate scary-level rule and a
21-move route from ordinary flight to any stair. A food action interrupted
an earlier stretch of the same alternating route. These are excerpts from a
live recording. They do not certify byte-for-byte X11 re-execution.

The desperate rule's '<20' gate measures proximity across the dungeon,
while the weighted stair router allowed a walk of up to 249 moves. Source
commit `006aa179` passes the desperate limit into the weighted search, also
for clean detours. Its regression model builds the observed pair of opposing
routes with the same 118 and 21 move counts. The up route is refused with a
19-move cap, and the ordinary search proceeds to the other staircase.
The model is a constructed corridor layout, not a reconstruction of the
recorded dungeon. The three shipped Borg smoke games match the refreshed
reference. The Warrior's key stream changes, and the other two match their
previous key, message and state streams. No smoke game died.

A bounded load of a copy of the turn-385995 native fingerprint save ran on
both the installed recording executable and the patched headless executable.
Both restarted with fresh Borg memory and retained the save's engine RNG.
Neither recovered the original scare and map knowledge. The 45-key stream
was identical (`0bd1479178f20e13e37f89a4cf60e16f437a08414461588af31d4c873ecf75fc`)
and both stopped alive on DL3, 188 HP, at turn 386150. The save hash is
`b021493c9ea63c51cab746cb760330a1bb91a73184649ea460f1c5d566362367`.
The owner retains the original recording and save locally. These short
loads are diagnostics from the same recorded life, not independent runs.
