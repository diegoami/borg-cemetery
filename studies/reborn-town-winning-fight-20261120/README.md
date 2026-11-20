# Town winning-fight policy: selected validation

Source task [reborn#788](https://github.com/diegoami/borg-reborn-rs/issues/788). Baseline `d7e58cdf1d9bc47655d4e476ab452816ff418935` includes accepted weighted-flight and Paladin-reserve changes; candidate `5f41b563be3f3e2d10345c255cbd4d208757ac04` adds the shared town policy. Frozen binary/profile identities and per-attempt applied parameters are recorded in [validation.json](validation.json), [control BUILD_ID](control-BUILD_ID) and [candidate BUILD_ID](candidate-BUILD_ID).

Twelve fresh named attempts at100000 engine turns, each under `/tmp/angband-validation.lock`: Warrior101 (race0,class0), Mage102 (2,1), and the previously named Ranger807683971 (0,7). No local population arm. All12 reach the cap alive, with no game/harness failures and no natural deaths to export. Three separate default borg-rs smoke games reach their20000 caps alive and match accepted main keys/states/messages3/3; no smoke reference change.

| Start | baseline mode0 | candidate0 | candidate2 | baseline1 | candidate1 |
|---|---:|---:|---:|---:|---:|
| 101 | 6 | 6 | 6 | 8 | 9 |
| 102 | 5 | 5 | 5 | 6 | 6 |
| 807683971 | not run | not run | not run | 6 | 6 |

Table values are maxCL, not independent samples or evidence of population improvement. Mode0 and diagnostic mode2 each preserve the exact baseline mode0 key/state streams on both101 and102. The enabled Warrior/Mage paths change; the Ranger key, state and message streams remain byte-identical. See individual stream hashes for equality rather than inferring identical lives from terminal CL.

The enabled logs contain 9 new-policy notes, all hunt refusals without a current certificate. **No positive `Town attack on sight` priority action was observed in these named games.** Winning/losing/tied certificates, shared resources, unknown threats, harmless bystanders, approach/healing cost, plain-step versus bump/door/trap/web/shop gating, and list/class/scare semantics are covered by production-helper unit tests. The actual positive town priority/wand path and the full range of safe approaches are not runtime-validated here. This boundary must remain visible to the reviewer and any Zoo measurement.

The initial integrated source build failed before games because an automatically merged town guard referenced the direction-index interface retired by the accepted weighted-flow refactor. It was corrected to consume the selected location. Final local required Rust/vendor/citation checks pass:537 core tests,4 ignored;2266 parameter citations,0wrong/0CAL disagreements. This build failure is retained separately from the15 successful game attempts.

The policy uses existing compiled0/shipped1 `caution_winning_fight`; list membership also requires `attack_on_sight=1`. Town rows keep ordinary scares for losing/unknown fights and have reasons for mercenary/veteran melee danger and rogue/urchin theft. Theft remains unmodelled and never forces a certificate. All remaining walk steps and healing during approach are charged; unknown future melee and interaction steps cannot borrow a winning attack. This is deliberately conservative, not a lethality or improvement claim.

Reproduction: build either exact source commit with its default borg-rs harness under the validation lock, then invoke retained `zrun.py GAME HARNESS FRESH_OUT SEED RACE CLASS 100000 borg_param_caution_winning_fight=MODE`. Use a **fresh output directory**: this low-level adapter replaces its output directory; the retained named runner rejects existing trial roots. The shipped profiles/scary lists are those of each exact source commit. Both main changes were integrated before freezing, so comparisons do not substitute the earlier f827 specimen.

The source PR supplies its own handover and reviewer checklist. Existing Zoo#511/#528 remain pinned to their older specimen; this evidence must not be silently folded into those requests. No workflow dispatch or population claim.


First visible enabled key differences are retained with state/message context: Warrior101 at54856 onDL2 (cure timing after a pit), Mage102 at76792 in town. The earlier Town refusal notes need not immediately change a key; subsequent internal goals/random flow choices may diverge later. These are full birth trajectories, not saved-state counterfactuals or proven direct effects on the terminal encounter. Ranger807683971 has no key/state/message difference.
