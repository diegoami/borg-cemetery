# Scenario screening

Seed: 102; source: `e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71`.

1 candidate events; 3 structured decisions in their windows. See scenarios.json for original state/trace line numbers.

Windows: 10, 20, 30 engine turns. Calibrate their useful context against player actions and Borg decisions before adopting a standard horizon.

Investigation queue (hypotheses requiring evidence):

- Stair retreat: establish known stairs, path legality, travel cost and danger along the path.
- Fight or disengage: compare the scored alternatives, threat, mode and goal timing.
- Potions and objects: establish known inventory, usability and the cost of spending a turn.
- Spells: establish knowledge, mana, failure chance and legal targets.

No parameter change is proposed automatically from low HP or a death alone. Missing decision traces remain missing evidence. The next report must name the actual parameter, current/candidate values, cited observations and a testable prediction.
