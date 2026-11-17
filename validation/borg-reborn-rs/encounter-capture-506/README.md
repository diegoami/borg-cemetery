# Optional encounter capture validation (#506)

Source: borg-reborn-rs `ba26c2abc378302c7d37d4337775d3bd5fe5ad30`, a clean candidate based on main `28360152`, source PR #508. This is a bounded capture identity check, not a population comparison or a milestone acceptance.

The native archive retains all 13 executions: four unique birth starts (Mage and Warrior on each controller), their logging-on/off repetitions, four fresh-Borg saved-start loads, and one full-observation comparison. These are correlated repetitions, not 13 independent lives. No natural death occurred.

Complete key, state and message streams and terminal engine RNG are identical with capture on/off. Native compact channels match the full observation reader, initial frames include level-1 gear/status, and each saved-start first frame is exactly at the saved turn. `validation.json` retains the clean source/build/binary identity, raw archive digest and per-execution streams/RNG. The source test is `engine/tests/test_encounter_capture.py`.

This verifies recording identity on these cases. It does not establish gameplay improvement, counterfactual lethality, or completion of the new Suite 2 bank. Zoo #184 owns that harvest and bank validation, through Zoo PR #202 and Cemetery PR #68.
