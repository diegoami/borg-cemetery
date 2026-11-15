# D0007 analysis evidence qualification

The original decision scores and choices come from the retained reborn
`e9a6a521f3ac` trace. Additional monster HP was read from the already verified,
recorder-enabled S0003 saved-position diagnostic. Its keys, messages and state
logs matched the earlier original-version S0003 trial byte-for-byte. This is
supplemental observation of that replay, not an assertion of original binary,
whole-private-memory or all original frame equality.

| Diagnostic frame | Engine turn | Player HP / mana | Visible Fang HP |
| --- | --- | --- | --- |
| 88 | 3612 | 6 / 2 | 25 / 25 |
| 96 | 3632 | 4 / 1 | 16 / 25 |

Both anchors record Fang visible. The supplemental frame stream, executable
and recorder identities are retained in the adjacent machine evidence receipt.
The full local session was under `/tmp/S0003-recorder-session`; that temporary
path is not a portable recording download or a requirement to understand the
facts above. Use the case launchers to reproduce its saved-position run.

## Reproduced terminal score arithmetic

Actual risk aversion is 50; expected risk 5.4625 and worst 9.2 give composite
risk 7.33125. Magic Missile is 3d4, with native failure 14%, so its mean credited
damage is 6.45. Against the observed 16 HP, the source's share is 0.403125.
The tactical ladder gives the spell `2 × 7.33125 × 0.403125 − 7.33125`, or
**−1.4204297**. The cure restores missing HP only: `5 − 7.33125`, or
**−2.33125**. These agree with the original recorded choices/scores.

Failure is already discounted in expected damage. A spell cannot kill that
16-HP target in one 3d4 hit, but the engine can induce fear on nonlethal damage;
that possibility must remain part of a corrected action-outcome model.
