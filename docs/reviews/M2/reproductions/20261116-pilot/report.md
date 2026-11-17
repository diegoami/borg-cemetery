# Synthetic suite p1-warrior revision 1

Attempted 6 / 6 scenarios. Deaths: 4; survived to cap: 2; stopped: 0; failures/mismatches/timeouts/unsupported: 0.

Qualified near-death coverage is unavailable; count is unknown. Low-HP screens are provisional.

| Scenario | Depth | Character tier | Outcome | Min living HP observed | Candidate sampled turns | Nothing happens messages | Death cause / reason |
|---|---:|---|---|---:|---:|---:|---|
| p1-warrior-58049e87970571527e48fe74 | 5 | birth | survived_to_cap | 9 | 0 | 1 |  |
| p1-warrior-e13f8633d330da903304278c | 5 | observed-level5 | survived_to_cap | 54 | 0 | 0 |  |
| p1-warrior-80745bce983fbadfef1163fd | 10 | birth | death | 5 | 0 | 1 | a wolf |
| p1-warrior-227b3d5a4a28b149c71d2599 | 10 | observed-level5 | death | 0 | 3 | 0 | a wolf |
| p1-warrior-ca82babc75c232d09ab1512f | 15 | birth | death | 0 | 1 | 1 | an ochre jelly |
| p1-warrior-6a9113b2647a4fad82a6c205 | 15 | observed-level5 | death | 5 | 0 | 0 | an ochre jelly |

| Depth | Character tier | Total denominator | Death | Survived | Stopped | Invalid |
|---:|---|---:|---:|---:|---:|---:|
| 5 | birth | 1 | 0 | 1 | 0 | 0 |
| 5 | observed-level5 | 1 | 0 | 1 | 0 | 0 |
| 10 | birth | 1 | 1 | 0 | 0 | 0 |
| 10 | observed-level5 | 1 | 1 | 0 | 0 | 0 |
| 15 | birth | 1 | 1 | 0 | 0 | 0 |
| 15 | observed-level5 | 1 | 1 | 0 | 0 | 0 |

These are synthetic starting-condition experiments, not historical replays or population improvement evidence.
Character catalog provenance and sampling/normalization limits are part of each scenario definition.
Minimum HP describes sampled pre-key states; it is not a complete decision-state distribution.

Death causes: {"a wolf": 2, "an ochre jelly": 2}
Sampled minimum living HP distribution: {"0": 2, "5": 2, "54": 1, "9": 1}
Scenarios with missing evidence: 0.
