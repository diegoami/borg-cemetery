# Alternative human play — survived beyond the original death

The owner played from S0003's retained save at turn **3402**, with its saved
engine RNG and the Borg initially off. The recording contains 56 terminal
input events and **no Borg inputs**. Replay verification passed.

The character reached **turn 4873 alive, level 2, with 15/15 HP**. The original
Borg died to Fang at **3640**. This continuation therefore remained alive
**1233 engine ticks beyond the original death**.

## Comparison with the original death

**Survived beyond the original death turn 3640: the continuation was last observed alive at 4873, 1233 engine ticks later, with 15/15 HP at level 2.**

| Observation | Result |
| --- | --- |
| Retained starting save | Turn 3402 |
| Original Borg death | Turn 3640 |
| Last recorded continuation | Turn 4873; HP 15/15; level 2 |
| Original save bytes captured | Yes |
| Recorder replay verification | Passed |
| Continuous ordinary-play observations through comparison | Yes |

Fang, Farmer Maggot's Dog was never recorded as visible in this continuation. This shows survival from the saved situation; it does not demonstrate defeating that enemy in a direct fight.

The identified human-play runtime and chosen route may differ from the original Borg run. This is one alternative from the retained starting position, not a general policy improvement, an exact restoration of original private Borg memory, or an additional independent life.

## Watch or reverify this continuation

From the death directory:

```bash
./watch.sh --alternative 20261115T004527-7541a0
./watch.sh --alternative 20261115T004527-7541a0 --verify-only
```

[Download the retained recorder input recording](recording.tar.xz).
Recorded game source: `2e648118eedc31904dcaed056db52e14acda2a07`, the separately
identified recorder-enabled runtime. Exact reverification needs its matching
cached executable; recorded-frame viewing remains available otherwise.

The archive's original capture hash was checked, and the recorded file inputs
contain the original starting-save bytes. The original recording and capture
metadata are preserved; this written comparison is added beside them.
