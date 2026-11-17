# Repeated execution of the six-case P1 pilot

This is additional execution evidence for Cemetery #5 / #7 and reborn #371 / #378,
not milestone acceptance or a new scenario suite. It reuses the existing bank.

- Cemetery runner/bank: `b55b07aed36eb4ad15acf9db5ee2a7cc7acc53e1`.
- Reborn runtime: `99473510940b8a7bd6e77ad61e3a2b00c72a6e6d`, clean inputs and checkout.
- Runtime input digest: `bf9a451c46a07142b59525a9c9c581287930e3b333baa4a81dda4816ed2a025a`.
- Rebuilt executable: `ba06d6fad667a51a25b644b62687a5b47f17cabe75fecce45638e7f4301b290b`.
- Toolchain: Rust 1.100.0, GCC 14.2.0, Debian 13; exact build receipt in results.
- Bank: seed 101, Human Warrior, starting depths 5/10/15, birth and observed-level-5
  character tiers, 5,000 engine turns and 30 wall seconds per case.

| Starting depth | Birth kit | Observed level-5 tier |
| --- | --- | --- |
| 5 | Survived to cap | Survived to cap |
| 10 | Died to a wolf | Died to a wolf |
| 15 | Died to an ochre jelly | Died to an ochre jelly |

Both executions completed all six cases: four deaths, two cap survivals, zero
stopped/failure/mismatch/timeout/unsupported cases. These are repeated attempts
of six scenarios, not twelve independent natural games. Each key/state/message
stream matches its repeat byte for byte: 18 matching stream pairs. Suite digest,
scenario IDs and terminal results match the original M2 evidence packet.
The rebuilt binary has its own hash; cross-toolchain binary equality is not claimed.

Qualified near-death coverage/count remains unavailable/null. Low-HP screens
are provisional. The level-5 tier is one observed character, normalized as the
catalog declares; it is not a population average. No improvement claim follows.

## Checks and retained evidence

- 54 cemetery runner tests and 50 native-tool tests passed before execution.
- The real synthetic-start engine test suite passed; its output is retained in
  `startup-tests.txt` (repeated starts, bad inputs and registry exclusion).
- Actual generated starts and two executions were checked against the suite's
  scenario, profile, source and binary identities by the existing runner.
- No input save was used. No scenario created a natural-registry guard directory.
- Reconciliation independently excluded all 12 synthetic attempts, with zero
  natural deaths or missing natural dossiers. Direct export of an actual
  synthetic death returned `not natural: synthetic start; no dossier` and
  created no registry. See the retained exclusion receipts.
- `verification.json` contains repeated gameplay-stream hashes.
- `results-first.json`, `results-repeat.json`, `scenarios.json` and `report.md`
  retain complete compact outputs; original reviewed evidence is unchanged.

Raw logs remain outside Git in the execution workspace (`work/pilot/run-1` and
`work/pilot/run-2`); those paths are not permanent public downloads. The existing
pinned CI workflow separately offers its own evidence artifacts with 14-day
retention. The compact records here persist independently of those logs.

## Reproduce

Use clean checkouts at the exact source and runner pins above. Build reborn
with Rust 1.100.0 and the documented native dependencies:

```sh
BORG_IMPL=rust flock /tmp/angband-validation.lock harness/build.sh
```

From the pinned Cemetery checkout, use two fresh output paths:

```sh
python3 scripts/synthetic_suite.py run --manifest synthetic/p1-warrior/suite.json --source /path/to/reborn --out /tmp/p1-first
python3 scripts/synthetic_suite.py run --manifest synthetic/p1-warrior/suite.json --source /path/to/reborn --out /tmp/p1-repeat
```

The runner takes the execution lock itself. Compare keys.log, state.log and
messages.log for every matching scenario ID. Keep P2/P3 and milestone acceptance
separate; this execution changes no game code, catalog or suite definition.
