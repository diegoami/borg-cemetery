# D0007 bounded parameter results — 2026-11-15

Five diagnostic processes used the **same S0003 save**, saved engine RNG,
fresh Borg memory, the exact original reborn source `e9a6a521f3ac` and the
same executable. Each requested 1000 engine turns beyond saved turn 3402,
so the cap was 4402. Effective parameters were checked: every candidate
differs from the control in exactly its declared single key.

The control's complete terminal summary, including engine RNG, matches the
previously retained original-version S0003 trial except elapsed wall time.
These are one starting condition and its continuations, **not five independent
births**, a held-out test, or a population survival estimate.

| Arm | Result | End turn | End HP | Recorded grids/depth pairs | Trace violations |
| --- | --- | --- | --- | --- | --- |
| Control | Died to Fang | 3640 | −2 | 5 | 0 |
| Threat horizon 2 | Alive at cap | 4402 | 9/9 | 16 | 0 |
| Threat horizon 3 | Died to Fang | 3650 | −4 | 13 | 0 |
| Risk aversion 75 | Died to Fang | 3640 | −2 | 5 | 0 |
| Rest duration 1 | Alive at cap, with refused rests | 4402 | 9/9 | 77 | 4 |

All arms remained character level 1, deepest level 1. Distinct positions are
a limited movement measure, not proof of useful mapping or long-term progress.
Both survivors are exploring in the trace at the cap; neither establishes
eventual survival or success at a harder encounter.

## Interpretation

**Horizon 2 is a useful candidate for confirmation.** It retreats earlier
during the first recovery, takes a different sequence of steps, and spends its
second Phase at 3522 rather than 3532. After that landing it rests from 3532
to 4282, reaches full HP and resumes exploration. This supports testing
pursuer/recovery timing; it does not prove that a longer horizon always helps.
The next horizon, 3, dies at 3650. Action and RNG paths diverge after the
parameter changes, so each is an observed branch, not an unchanged-dice shadow.

**Risk aversion 75 has no observed benefit here.** Its death and decision
sequence reproduce the control. The source's threat-removal credit explains
why a more pessimistic risk weight need not choose a cure over a spell.

**Rest duration 1 is not a clean tuning success.** There are four refusal violations. The first, at turn 3452, says:
“the action took no game time: the game refused it.” Recover is cooled, and
Explore immediately chooses northwest at the same engine turn. The survival
therefore includes a refused-action/cooldown mechanism, not simply more careful
one-turn resting. This parameter also changes Recover's stall budget. Do not
promote it as an improved rest policy. Test the executor's short-rest semantics
and a deliberate post-escape movement policy separately, with no-new-refusal
acceptance criteria.

## Evidence and next test

Each arm directory retains its original summary, effective parameters,
configuration, process/trial receipt and compressed key/message/state/decision
logs with hashes. No game binary or duplicate source save is committed. Some
load-time messages have key/turn zero and replay stored history; they are **not
new purchases or resource use during the trial**.

Confirm the unchanged control, then test horizon 2 on the two earlier saved
risk candidates and on other prespecified starts, including encounters where
the original horizon succeeds. Keep newly killed cases, refusals, stalls,
resource use and progress alongside survival. A native timing fixture should
still assess the movement penalty and candidate-outcome hypotheses before
changing those algorithms. No Borg source or default profile was changed.

[Analysis and hypotheses](../analysis.md) · [Frozen profiles](../analysis-profiles/README.md)
