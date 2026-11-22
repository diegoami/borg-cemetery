# Priest repeatedly spends Detect Invisible staff charges

[Source issue #1016](https://github.com/diegoami/borg-reborn-rs/issues/1016)
· [Hallway Light Beam issue #995](https://github.com/diegoami/borg-reborn-rs/issues/995)

FreshBorg, CL22 Priest, recorder session
`20261122-170630-FreshBorg.F1wUCv/native`, Track P build
`4b2c2fcf913e352ebd7bef5f16a531e8fc50d92a`. The recorded executable
SHA-256 was
`3a298a35a53bd6e1ba43fe25295ea0c522501a03ae43f724826e02942eb7cf62`.

From turn 11,343,820 through 11,359,751, the Priest successfully used
Detect Invisible from the same stack 30 times on DL14 and DL15. Its
charge count fell from 39 to 9. Twenty-one uses returned “You sense no
invisible creatures.” Nine reported a presence.

The uninterrupted run of twelve empty results starts at 11,349,051
on DL15. The Priest uses the staff every 30 game turns up to
11,349,381, depleting the stack from 34 to 22 charges. The DL14 entries
show the Phase Door decision trying an ordinary defence while walking
toward the stairs. Several of those turns have one or two SP, but these
detections spend staff charges.

The log establishes the expenditure and result, as opposed to the
reason for every activation. The source's unseen-attacker timestamp
and short see-invisible timeout are the starting points for a controlled
regression. A fresh reason to detect can still justify a new use.

[Exact staff actions and results](staff-uses.tsv)
