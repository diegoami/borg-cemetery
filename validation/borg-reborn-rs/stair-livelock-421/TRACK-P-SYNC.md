# Final source synchronization for #421

Track-p advanced through #426 to50c92ba0 during task validation. Preserve its winning raw/weighted diagnostic and status changes. The first merged build0c5ad8f7/sourcec5d12fc5 keeps the earlier stair fix; its constructed/Troll controls have byte-identical keys and state to the earlierd012 source. Messages match after replacing only the per-run directory in the plan diagnostic.

The final build9289dbc5/source69f3c872 further restricts stale-flow cleanup to GOAL_FLEE. Existing native loot/combat/exploration flows remain owned by the core. Both the short positive-loop regression and all reported-character checks have zero threshold bursts. Warrior trip-policy0/1 keys match each other. Native preparedness/retreat remain authoritative, with no change to engine time/RNG or town-ended/one-shot refusal behavior.

| Trial | Source | Actual race/class | Keys | Peak keys/turn | Burst turns≥1000 |
| --- | --- | --- | --- | --- | --- |
| p421-note-sync-constructed | c5d12fc5 | Half-Elf Warrior | 727 | 39 | 0 |
| p421-note-sync-troll | c5d12fc5 | Half-Troll Rogue | 16758 | 248 | 0 |
| p421-final-constructed | 69f3c872 | Half-Elf Warrior | 751 | 39 | 0 |
| p421-final-warrior | 69f3c872 | Half-Elf Warrior | 15393 | 138 | 0 |
| p421-final-warrior-trip | 69f3c872 | Half-Elf Warrior | 15393 | 138 | 0 |
| p421-final-troll | 69f3c872 | Half-Troll Rogue | 14299 | 345 | 0 |
| p421-final-orc | 69f3c872 | Half-Orc Rogue | 13145 | 78 | 0 |

All seven bounded trials finish alive at cap; no population or survival claim. The old14-trial report/receipts are unchanged and remain with their original epochs. Eight natural control packets (ordinary3+weighted1 for each new epoch) are separately retained and reconciled against independent canonical registries. Exact identities, raw-file hashes, diagnostics normalization and package maps are in TRACK-P-SYNC.json. Raw logs/builds remain outside Git.

The native engine suite passes76 tests with two local environment skips; required Rust checks pass. Full CI on the final source/head is required before integration into track-p, and this is not owner acceptance for main promotion.
