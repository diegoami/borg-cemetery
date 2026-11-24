# Track P loop breaker comparison for seed 453254028

Both starts used the default `borg-rs` core from Track P
`c5501d3c5aeac2449fc47ed6ca6efe2fbafdd894` in the normal world, with
`harness/run.sh OUT 453254028 1 4 100000 menu,exact`. The
[shipped arm](loop-on/summary.json) resolved `loop_breaker=1`.
The [override arm](loop-off/summary.json) used only
`BORG_TXT_SET=borg_param_loop_breaker=0` and resolved `loop_breaker=0`.

The configurations below are the exact `user/borg.txt` files from the
two runs. They differ only in `borg_param_loop_breaker`.

| Run configuration | `borg_txt_sha256` |
|---|---|
| [Shipped `borg.txt`](loop-on/borg.txt) | `0cac99702aea4f46a3555b710bfcb4cacf7319203f862f6557704c04607272db` |
| [Override `borg.txt`](loop-off/borg.txt) | `94b1d1c8b9ac8eda427b008ea87a9e258ff7e867f3cbc3b86d8fb861d302b8b6` |

Both reached the 100,000-game-turn cap at CL5, DL2. The two runs have
the same SHA-256 for each game stream.

| Stream | SHA-256 in both arms |
|---|---|
| `keys.log` | `514113e9663b472d6077dbe3738ede75729a8a70f0ecc0d2e91631214b3f126c` |
| `messages.log` | `f9e2aba09a5d6ea7f8720eb4e45e714a51882caa8d57360cad195f3ff9939305` |
| `state.log` | `f7de0273d3ad766805dde6071939d2e0760b114b1c261dc7864b0bea92a981d6` |

This is a paired result for one named start.
