## Why the aim flow reversed before the floating-eye death

This is one diagnostic replay of the Half-Elf Necromancer `453254028`
in [D-88768638](../../deaths/D-88768638033650b62916128147e2e9ee8ce6e53590c6d119d2d538df88f09e08/analysis.md).
It answers the handoff question in [borg-reborn-rs #1132](https://github.com/diegoami/borg-reborn-rs/issues/1132).
Coordinates below are `(x,y)`.

An unmodified build at
[`d8b55d647ec941676ac2449ad97a786ecf8f235f`](https://github.com/diegoami/borg-reborn-rs/commit/d8b55d647ec941676ac2449ad97a786ecf8f235f)
reproduced the death at turn 77,923. Its keys, messages and states matched
the dossier. The diagnostic build added only the stderr observations in
[trace.patch](trace.patch). It ended at turn 77,500, with its three game
streams byte-for-byte prefixes of the unmodified run. Both builds used
Angband `574b618c3bfec595f3503a58f8e488b1c4ae3a46`, GCC 14.2 on x86-64
(right-to-left argument evaluation), and rustc 1.100.0.

| Turn | Borg grid | Decision |
|---:|---|---|
| 77,029 | (90,39) | The old aim flow has reached cost zero and the ordinary attack has no targets. Dark BFS moves south to (90,40). |
| 77,039 | (90,40) | Aim simulation accepts (88,40) with one target, even though that grid is known granite. The committed route starts southwest to (89,41). |
| 77,049 | (89,41) | The old flow selects the granite grid. The ordinary step refuses it because the Borg cannot dig it. A new aim search starts northeast to (90,40). |
| 77,059 | (90,40) | The new aim route continues north to (90,39). |
| 77,069 | (90,39) | Aim has reached cost zero and the attack has no targets. Dark BFS takes the south step again. |

The granite aim destination and the lack of a target on arrival at the
second destination give exploration its turn back. The same pattern is
visible forty game turns later in [trace.txt](trace.txt). It eventually
raises the bounce count to the reset that forgets the eye. This is one
historical start. At shipped Track P `c5501d3c` the same seed reached the
100,000-turn cap with the loop breaker [on](evidence/loop-on/summary.json)
and [off](evidence/loop-off/summary.json). The calls and outcomes are
recorded in the [paired receipts](evidence/README.md). These two runs had
identical game streams and neither reproduced the historical death.

### Replay

Use a clean scratch checkout of `borg-reborn-rs` at the commit above.
Install CMake, GCC on x86-64, Rust, Python 3 and `flock`. Run the checkout's
`scripts/setup.sh` to fetch its pinned vendor sources and native Cemetery
tools (`death-tools-pin.txt` at `4697893660942ed142744306c634583ec630f88a`).
Use unused output directories for the two runs.

```sh
study=/path/to/borg-cemetery/studies/bfs-aim-loop-453254028
bash scripts/setup.sh
CC=gcc BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
flock /tmp/angband-validation.lock harness/run.sh /tmp/aim-loop-original 453254028 1 4 100000 menu,exact
git apply --unidiff-zero "$study/trace.patch"
CC=gcc BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
flock /tmp/angband-validation.lock harness/run.sh /tmp/aim-loop-probe 453254028 1 4 77500 menu,exact
python3 "$study/check.py" /tmp/aim-loop-original /tmp/aim-loop-probe
```

The verifier checks the unmodified death against the dossier's three
full stream hashes. It then checks the bounded hashes, byte prefixes and
aim trace against the diagnostic run.

The next production test should require a walkable aim destination and a
target that the normal attack evaluator can see on arrival. The diagnostic
patch can verify both symptoms before testing a change in policy.
