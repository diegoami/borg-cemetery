# P8 exploration deaths

[Download the interactive Zoo-style report](index.html) and open it in a browser to step through the last 50 changed screens of each fatal play. The report covers [Zoo #754](https://github.com/diegoami/borg-zoo/issues/754) at `c5501d3c` in the normal world.

| Arm | Small deaths | Medium deaths | Big deaths | All deaths | CL5 by 100,000 turns |
| --- | ---: | ---: | ---: | ---: | ---: |
| Shipped | 0/90 | 0/270 | 2/540 | 2/900 | 681/900 |
| BFS off | 0/90 | 2/270 | 2/540 | 4/900 | 829/900 |
| Mixed off | 0/90 | 0/270 | 2/540 | 2/900 | 685/900 |

The 54 pilot cells had zero deaths and are excluded from the decision-tier totals. All eight death outcomes occurred on DL1, before CL5. The Druid and Rogue each died with the same key stream in shipped and mixed off. The viewer shows six distinct fatal plays and the run manifests retain all eight outcomes with their original configurations. Each viewer stream reproduces its archived key hash.

- [Medium run dossiers and Ranger stair counterfactual](../zoo-reborn-p8-exploration-medium-45456422005/README.md)
- [Big run dossiers](../zoo-reborn-p8-exploration-big-45492520011/README.md)

The X11 play pack on the analysis machine is `~/borg-play/p8-exploration-deaths`. Run `./play.sh` there to see the saves or `./play.sh NAME --to TURN` to replay from birth to a point in the exact game.
