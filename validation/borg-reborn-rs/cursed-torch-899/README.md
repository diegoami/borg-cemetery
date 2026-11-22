# Cursed torch take-off loop validation

[Source fix](https://github.com/diegoami/borg-reborn-rs/pull/900) ·
[Original zoo finding](https://github.com/diegoami/borg-zoo/issues/609#issuecomment-7070855811) ·
[Replication on f57499d0](https://github.com/diegoami/borg-zoo/issues/623)

Both controls were replayed from birth with the `ab775d48` executable and
per-start settings in `~/borg-play/main-ab775d48-newly-killed`. Their full
key streams matched the preserved play pack. The control games are already
registered in the [original run](../../../runs/2026-11-22-tonight-ab775d48-newly-killed/README.md).

| Start | Curse learned | First take-off | Control | Fixed |
| --- | ---: | ---: | --- | --- |
| Elf Blackguard 1965910635 | 43,310 | 43,382 | 1,422 removals, scrawny cat at 64,969 | Alive at 100,000, CL5, max DL2 |
| Kobold Druid 653243095 | 71,580 | 71,694 | 367 removals, scrawny cat at 77,418 | Alive at 100,000, CL8, max DL3 |

Each fixed key stream matched its control through the key immediately
before the first take-off command. At that turn, each fixed game sent
`w` and equipped an uncursed 5,000-turn Wooden Torch directly. Neither
fixed game logged a cursed-torch take-off. The original commands and the
changed command occur at key 6,255 for the Blackguard and 8,797 for the
Druid. Both had a clean spare already. The source unit regression
separately tests the case without a usable spare.

## Candidate replay

On x86-64 GCC with right-to-left C argument evaluation, check out
`diegoami/borg-reborn-rs@a6e30cd1d71a405cebf0c697c963027424d992bb`.
Use the shipped settings and default borg-rs core, a natural birth, and
the exact cap.

```sh
BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
flock /tmp/angband-validation.lock harness/run.sh /tmp/torch-blackguard 1965910635 2 8 100000 menu,exact
flock /tmp/angband-validation.lock harness/run.sh /tmp/torch-druid 653243095 10 2 100000 menu,exact
```

The local candidate build used GCC 15.2.0 and Rust 1.98.1. SHA-256 receipts:

| Input | SHA-256 |
| --- | --- |
| Candidate source | `f40fe8e8b8e888db4e86bef51a9764ee2da7a67480a3a4725951259a7a9fd4ef` |
| Candidate binary | `4f77e695d9111b99cec3e39a1f403717f5c19480c2b8b5cbe8beee6eeb1ee2d3` |
| Control binary | `28ec8c027a93303329c3af126315603f131dffafe078f75c224f8fcdcd854339` |
| Shipped borg.txt | `dd21cc3e95f5ac0dc504d1f821f148befe356df74d4eb69b17d3b549edc4e046` |
| Shipped scary list | `e0e293814e8ed9c2f3a5f0af809f479e854878e5d0eaedea37b671dd1b20f5a8` |

| Candidate log | Blackguard | Druid |
| --- | --- | --- |
| keys.log | `0c96a44aca6fbcd891bd4717abcd00b1f22acc6ebc65cab90e47d37dd640d7ff` | `73f1c85e9b995ae2d364a14ea07df5e1a2eb674d6c6d63735bdf878bb1e380b9` |
| messages.log | `ebdc7ab61145f68e3916e44b4732eca4c712a0b8f1c23a8d7d78372a142f60e5` | `4543f128241186da466d3b554a1ced11c87b112f53316163f4fceefdf3f80568` |
| state.log | `5b0ea5486f012213f45a27a9eba7ebbd3bd3f5b0a42073fb76664e29c6e4a69f` | `b02bc61d8995ad58e018c44bc7c3431f5e20178dce6175e6628ffbb443810ac4` |

The two paired starts were selected because they reproduced the defect.
All three shipped smoke games matched their key, message and state
references. Population measurement is a separate Zoo pilot.
