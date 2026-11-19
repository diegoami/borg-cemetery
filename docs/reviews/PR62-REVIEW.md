# Review: PR #62 "Support exact bounds and initial observations for configured saved trials"

- Repository: `diegoami/borg-cemetery`
- Branch: `task/paired-exact-saved-execution`
- First head reviewed: `af7bad6c35a3358e2a42ec19ecd33d8884261b42`
- Re-review head: `0f500d244bc391c9536f05edad8f88b93a5826f6`
- Reviewer model family: MiniMax (M3). Implementer family: MiniMax (M3), then Claude Opus 5.5.
  **Same family as the original implementation — the owner's "different family" rule for model
  review is not satisfied for the original commits. The re-review fix commit was authored by a
  different family.**
- Reviewer-verified environment: borg-reborn-rs `d09c4bc5`, engine upstream `42cd156a`,
  binary `a41f4bde…`, scenario `synthetic/fast-caster-encounters/mage-fang-102`.

## Verdict

**First review (`af7bad6c`): do not merge as-is.** Two of the three commits are sound and
useful; the middle commit implements a mechanism that cannot work in the configuration the PR
itself selects, and its stated purpose is not achieved.

**Re-review (`0f500d24`): the blocker is resolved.** F1, F3 and F5 are addressed and verified.
F4 remains open by the author's own choice, and is a receipt nit rather than a defect. The
branch merges cleanly and its full suite passes. The PR is ready for the owner's decision;
this review does not merge it.

| Commit | Subject | Verdict |
|---|---|---|
| `2463b03a` | Allow exact turn bounds for configured saved-state comparisons | **Good.** Works; keep. |
| `2586b5f6` | Retain explicit initial observation logging in configured trials | **Ineffective** (superseded — the pass-through was dropped in `0f500d24`). |
| `af7bad6c` | Keep configured trial input immutable when the engine autosaves | **Good and necessary.** Verified empirically. |
| `d82b697b` | Merge current `main` into the branch | Neutral. |
| `0f500d24` | Drop the ineffective observation-log pass-through and test `exact_turns` | **Good.** Resolves F1; adds F3 and F5 coverage. |

## Findings

### F1 (blocker) — `BORG_OBSERVATION_LOG` is never written when `BORG_CORE=borg-rs`

`scripts/scenario_config.py:66` hardcodes `BORG_CORE='borg-rs'` for the configured
adapter. In borg-reborn-rs, `BORG_CORE=borg-rs` selects the vendored borg-rs
decision core and **short-circuits reborn's own shell**:

- `borg-reborn-rs/src/engine.rs:255` — `do_cmd_borg()` calls `borg_rs::do_cmd_borg()`
  and `return`s when `core_is_borg_rs()` is true; `crate::borg::command()` (reborn's
  shell) is never reached.
- `borg-reborn-rs/src/borg.rs:466` — `observations: open_log("BORG_OBSERVATION_LOG")`
  lives inside `crate::borg::command()`. Unreachable in this configuration.
- `borg-core/src/` contains **no** `BORG_OBSERVATION_LOG` support at all
  (grep over the whole crate: zero hits; only `BORG_TOWN_PLAYER` is read).

So the env var the PR now propagates is silently ignored. Verified against the
real pinned binary:

```
[noexact] rc=0
[noexact] observations.jsonl exists=False size=0
[noexact] NO OBSERVATION LOG WRITTEN
[noexact] summary: dead=False stop_reason=turns game_turns=3611 loaded_turn=3402 exact_turns=False
[exact]   observations.jsonl exists=False size=0
[exact]   NO OBSERVATION LOG WRITTEN
[exact]   summary: dead=False stop_reason=turns game_turns=3602 loaded_turn=3402 exact_turns=True
```

Reproduced twice, identical result.

**The PR body claim is therefore not met.** It states the change "preserves its
explicit initial-observation log so Zoo can verify loaded equipment/resources."
No observation log is produced.

**It is also not needed by the Zoo.** `borg-zoo/zoo/paired_incidents.py:148-151`
reads `run/observations.jsonl` **only for the `baseline` arm**, which runs through
`run_scenario` on the **reborn** core (`zoo/paired_incidents.py:187`), where
`run_scenario.py:60` already sets the env var. The **candidate** arm — the one
that uses `run_configured` — is never asked for an observation log. The Zoo's
`validate()` (`zoo/paired_incidents.py:102-104`) checks `initial-coverage` under
`if arm['id']=='baseline'` only.

**Consequence:** commit `2586b5f6` is a no-op for its stated purpose. It adds an
env var that the selected core discards. It is harmless (no behaviour change,
no receipt claims it), but it must not be described as delivering an
initial-observation log, and nothing in Zoo may later be built on the assumption
that the candidate arm produces one.

**Suggested resolution:** either drop the `BORG_OBSERVATION_LOG` propagation and
correct the PR body, or — if the candidate arm genuinely needs an initial
observation — obtain it from a source that works under `BORG_CORE=borg-rs`
(e.g. `run/state.log`, which the Zoo already parses at
`zoo/paired_incidents.py:97,147` and which carries depth/HP/SP), and say
explicitly which mechanism is used.

### F2 (minor) — the PR body's validation numbers are measured against a stale base

The branch is **112 commits behind `main`**. The body reports:

- "109 Cemetery tests passed" — that is the count on the stale base. On current
  `main` the suite is **122 tests**; merged onto current `main` it is still 122
  and all pass (verified locally: `Ran 122 tests … OK`; native suite `Ran 69
  tests … OK`; `death_ids.py --check` → `Verified canonical IDs for 843 retained
  dossiers`).
- "642 retained dossier IDs checked" — current `main` has **843**.
- "7 configured-comparison tests passed" — `tests/test_encounter_comparison.py`
  does contain 7 test methods; that count is still accurate.

The numbers are not wrong *for the branch's base*, but they are not the
repository's current state. The PR body should state the base commit and be
refreshed, or the branch rebased so the reported numbers describe `main`.

### F3 (minor) — `exact_turns` has no test in this repository

`exact_turns` is a new public parameter of a cross-repo API. The only two
callers are in `borg-zoo` (`zoo/suite_runs.py:260`, `zoo/paired_incidents.py:189`,
both `exact_turns=True`), and both are outside this repository. There is no
Cemetery test asserting that the flag reaches the frontend, that the default is
unchanged, or that the horizon is exact.

The behaviour was verified by the reviewer directly and is correct — with
`exact_turns=True` the run stopped at `game_turns=3602` for a cap of
`start_turn(3402) + 200`; without it, at `3611`. The frontend flag is real
(`borg-rs/docs/harness.md:557`) and the summary records `exact_turns: true`.

A regression test asserting both arms would close the gap.

### F4 (nit) — no receipt for the execution save copy

`af7bad6c` copies the scenario save to `raw/save/input.save` and loads from
there. The original `dest/input.save` is correctly left untouched and
`config['save_sha256']` still hashes the original (`scripts/scenario_config.py:85`),
so the Zoo's `validate()` check `cfg.get('save_sha256') == s['save_sha256']`
(`zoo/paired_incidents.py:106`) still holds.

However, the *copy* that was actually loaded has no recorded pre-execution hash.
The engine overwrites that file in place on death (`angband/src/ui-game.c:1153`
→ `savefile_save(savefile)` → `angband/src/savefile.c:429-437` moves the old file
aside and renames the new one into place), so after a run the copy's bytes
differ from the input. Verified:

```
[long-run] rc=0
[long-run] summary: dead=False stop=turns turns=5411
[long-run] original dest/input.save sha=2883cc50b041337b unchanged=True
[long-run] execution copy raw/save/input.save sha=bd2c805e2d86f26b matches_original=False
```

This is not a correctness problem for the current consumers — the Zoo reads only
`keys.log`, `state.log`, `messages.log` (`zoo/paired_incidents.py:154`) and the
Cemetery death export collects `keys.log`/`messages.log`/`state.log`/`summary.json`/
`config.txt`/`params*.json` (`scripts/native/export-death.py:104,139`), never the
save. But recording the loaded copy's pre-execution hash (e.g. a
`loaded_save_sha256` next to `save_sha256`) would make the executed input
auditable rather than merely consistent.

### F5 (nit) — the copy lands inside the engine's own save directory

`raw/save` is also `-d save=`, i.e. `ANGBAND_DIR_SAVE`. Placing `input.save`
there is behaviourally inert in this headless frontend — `ANGBAND_DIR_SAVE` is
only consulted by the interactive save-file menu
(`angband/src/ui-game.c:905,1012`, `angband/src/main-win.c:3534`), which
`-mborgh` with `-load` never reaches. Worth a one-line comment, since the
co-location looks accidental otherwise.

## What is confirmed good

1. **`exact_turns` works and is correctly defaulted.** `-exact-turns` is a real
   borg-rs frontend flag (`borg-rs/docs/harness.md:557`), the parameter defaults
   to `False`, `compare_encounters.py:242` is unchanged, and no existing caller's
   behaviour changes. Verified: exact arm stopped at 3602 (cap 3602), non-exact
   at 3611.

2. **The exact-bound change is required by the Zoo and matches its call
   signature.** `run_configured(source, scenario, out, template, plan, turns,
   wall_seconds, exact_turns=True)` — the Zoo's positional/keyword usage at
   `zoo/suite_runs.py:260` and `zoo/paired_incidents.py:189` matches the new
   signature exactly. The parameter is not dead code; it is consumed cross-repo.

3. **The save-immutability fix is real and needed.** The claim "the engine may
   autosave the loaded file" is confirmed in the engine source
   (`angband/src/ui-game.c:1153`, `angband/src/savefile.c:429-437`). Without the
   fix, the scenario's input save would be overwritten by the run. With it, the
   original is provably unchanged (sha identical) and only the private copy
   mutates. The Zoo's `save_sha256` check and the Cemetery's death export are
   unaffected.

4. **Defaults and scope are respected.** No Borg policy, engine or saved input
   changed. The diff is 13 insertions / 6 deletions in one file.

5. **It merges cleanly** onto current `main` with no conflict, and the merged
   tree passes 122 + 69 tests, `death_ids.py --check`, and
   `build_statistics.py --check`.

## Recommended disposition

1. Resolve **F1**: drop the `BORG_OBSERVATION_LOG` propagation or replace it with
   a mechanism that works under `BORG_CORE=borg-rs`; correct the PR body either
   way. Do not merge a body that claims a log that is never produced.
2. Refresh the PR body against current `main` (**F2**), or rebase the branch.
3. Add a regression test for `exact_turns` (**F3**).
4. Optionally record the loaded copy's pre-execution hash (**F4**) and comment
   the save-directory co-location (**F5**).

`2463b03a` and `af7bad6c` are ready to keep as they are.

**All of the above are addressed at `0f500d24` except F4, which the author left
open by choice; see the re-review below.**

---

# Re-review: head `0f500d24`

The author addressed the findings at `0f500d24` ("Drop the ineffective observation-log
pass-through and test `exact_turns`"), after merging current `main` in at `d82b697b`.

## Disposition of each finding

| Finding | Status | Evidence |
|---|---|---|
| **F1** (blocker) — observation log never written | **Resolved** | The pass-through is removed from `scripts/scenario_config.py`, with a comment stating why: "with `BORG_CORE=borg-rs` the reborn shell that writes it never runs, so no log would appear." The new test asserts `BORG_OBSERVATION_LOG` is not in the child env. |
| **F2** (minor) — stale validation numbers | **Resolved** | `d82b697b` merges current `main`. The branch is now 5 commits behind `main` and 0 ahead, with no conflict. |
| **F3** (minor) — no test for `exact_turns` | **Resolved** | New `tests/test_configured_exact_turns.py` (62 lines, 3 test methods). |
| **F4** (nit) — no receipt for the executed save copy | **Open, by choice** | The author states no consumer reads the executed copy's hash. Verified: neither the Zoo (`zoo/paired_incidents.py:154`) nor the death export (`scripts/native/export-death.py:104,139`) reads it. Recorded as a known limitation rather than a defect. |
| **F5** (nit) — copy sits in the engine's save directory | **Resolved** | A comment now explains that the private `-dsave` directory is never read by `-mborgh` with `-load`, only by the interactive save menu. |

## Verification of the fix commit

**New tests** (`tests/test_configured_exact_turns.py`) mock `scenario_config.command` and
assert the constructed argv and environment:

- `test_default_has_no_exact_turns` — the default argv has no `-exact-turns`; `-turns 300`
  is present with the right value; `-load` points at `raw/save/input.save`.
- `test_exact_turns_reaches_frontend` — with `exact_turns=True`, `-exact-turns` appears
  exactly once in the argv.
- `test_environment` — `BORG_CORE` is `borg-rs`, `BORG_CEMETERY_DIR` is passed through, and
  `BORG_OBSERVATION_LOG` is **not** in the child env.

The harness also simulates the engine's autosave (`(raw / 'save/input.save').write_bytes(b'autosaved')`)
and asserts the original `save` still reads `b'original save'` — so the F4-adjacent
immutability property is now regression-tested too, and `config.txt` still records
`save_sha256=` of the **original**, which is what the Zoo checks at
`zoo/paired_incidents.py:106`.

**Suite results on `0f500d24`:**

```
python3 -m unittest discover -s tests                → Ran 125 tests … OK
python3 -m unittest discover -s scripts/native/tests → Ran 69 tests … OK
python3 scripts/death_ids.py --check                 → Verified canonical IDs for 853 retained dossiers
python3 scripts/build_statistics.py --check          → Statistics: 138 reports checked/generated
```

125 tests (up from 122 on `main`: the 3 new methods). CI is green on the PR.

Note on the dossier count: the author's comment says 844; the reviewer measured **853** on
current `main` at `a4c76ac5`. The number moves with `main`, so any figure quoted in the PR
body should be read as "at the time of the run".

## Revised verdict

**The blocker is cleared.** The branch now does exactly what it claims: it adds an opt-in
exact turn bound, keeps the scenario's input save immutable against the engine's autosave,
and no longer advertises an observation log it cannot produce. The remaining open item (F4)
is a receipt nicety with no consumer today, and is disclosed in the author's own reply.

This review does **not** merge the PR, mark any milestone accepted, or advance the
`reviewed` boundary — those remain the owner's decisions.

## Reproduction (re-review)

```bash
cd /home/diego/projects/angband/borg-cemetery
git checkout -B review/pr62-rereview origin/task/paired-exact-saved-execution
python3 -m unittest discover -s tests                  # Ran 125 tests … OK
python3 -m unittest discover -s scripts/native/tests   # Ran 69 tests … OK
python3 scripts/death_ids.py --check                   # 853 retained dossiers
python3 scripts/build_statistics.py --check            # 138 reports
```

## Reproduction (original review)

```bash
cd /home/diego/projects/angband/borg-cemetery
git checkout -B review/pr62 origin/task/paired-exact-saved-execution
git checkout main && git merge --no-commit --no-ff origin/task/paired-exact-saved-execution
python3 -m unittest discover -s tests          # Ran 122 tests … OK
python3 -m unittest discover -s scripts/native/tests   # Ran 69 tests … OK
python3 scripts/death_ids.py --check           # 843 retained dossiers
```

The observation-log probe used the real pinned borg-reborn-rs binary
(`d09c4bc5`, engine `42cd156a`) against
`synthetic/fast-caster-encounters/mage-fang-102` with
`studies/fast-caster-config/base-borg.txt`, invoking
`scenario_config.configured_adapter` directly with
`BORG_OBSERVATION_LOG` set in the inherited environment.
