# Priest repeats Light Beam and rests for mana

[Source issue #995](https://github.com/diegoami/borg-reborn-rs/issues/995)

FreshBorg, a Priest in recorder session
`20261122-170630-FreshBorg.F1wUCv/native`, used Track P build
`4b2c2fcf913e352ebd7bef5f16a531e8fc50d92a`. The recorded executable
SHA-256 is
`3a298a35a53bd6e1ba43fe25295ea0c522501a03ae43f724826e02942eb7cf62`.

The message “A line of shimmering blue light appears” is from the
Rod of Light. The selected defence repeatedly cast Spear of Light,
then zapped the rod and rested for mana. The recording shows four
stationary positions for which every hallway beam used the same
direction.

| First turn | Next position or level | DL | CL | Grid (x,y) | Direction | Beams attempted | Rod zaps | Rests |
| ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |
| 7,026,343 | 7,245,231 | 5 | 18 | (117,22) | North | 943 | 165 | 165 |
| 7,697,664 | 7,862,744 | 3 | 20 | (16,8) | South | 759 | 114 | 114 |
| 7,866,046 | 7,982,776 | 2 | 20 | (95,46) | South | 544 | 79 | 78 |
| 7,984,729 | 8,012,780 | 2 | 20 | (130,46) | North | 136 | 20 | 19 |

The longest episode contains 778 Spear of Light attempts alongside the
165 rod uses. At turn 7,245,043 the Priest decides to restock food and
reads Word of Recall. It is back in town at turn 7,245,231. In the last
listed episode the Priest runs short of food and advances after a few
wall bumps. The user interrupts automation later, at turn 8,013,720.

The recorded settings have `recover_rest_arms_see_invis=0` and
`cave_light_engine_radius=0`. The loop is observed live. A native save
from the start of an episode and a controlled replay remain to be
obtained. The evidence below identifies the attack and rest actions,
their location and key directions, and the first transition after
each episode.

[Episode receipts](episodes.tsv) · [Selected messages](messages.tsv)
