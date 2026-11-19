games 108, deaths 4, rests 13425

### By kind
| kind | rests | interrupted | attacked | monster | stopped short | level change | median game turns to interruption |
|---|---:|---:|---:|---:|---:|---:|---:|
| hp | 9454 | 984 (10%) | 389 | 595 | 5617 | 4 | 10.0 |
| mana | 3748 | 428 (11%) | 214 | 214 | 2236 | 1 | 10.0 |
| recall | 217 | 56 (26%) | 29 | 27 | 0 | 64 | 10.0 |
| other | 6 | 0 (0%) | 0 | 0 | 0 | 1 | - |

### By grid (dungeon rests only, depth > 0)
| grid | rests | interrupted | attacked |
|---|---:|---:|---:|
| stairs | 1185 | 146 (12%) | 75 (6%) |
| dead end | 27 | 3 (11%) | 0 (0%) |
| corridor | 1629 | 258 (16%) | 100 (6%) |
| room edge/junction | 1574 | 236 (15%) | 109 (7%) |
| open room | 1577 | 272 (17%) | 96 (6%) |
| *next to unknown grids* | 3 | 0 (0%) | 0 |
| *next to a door* | 597 | 88 (15%) | 41 |
| *on a scary level* | 395 | 120 (30%) | 32 |
| *fleeing* | 808 | 204 (25%) | 66 |

### Awake monster seen recently (Borg-time age of the youngest awake known monster)
| last seen | rests | interrupted | attacked |
|---|---:|---:|---:|
| 0-5 | 1444 | 339 (23%) | 92 |
| 6-20 | 165 | 40 (24%) | 19 |
| 21-50 | 160 | 26 (16%) | 12 |
| 51-200 | 161 | 17 (11%) | 6 |
| >200 or none | 4062 | 493 (12%) | 251 |

### Deaths and their last rest (window 2000 game turns)
| game | class | died at | last rest | kind | grid | outcome | turns before death |
|---|---|---:|---:|---|---|---|---:|
| 1199401383 | Necromancer | 88127 | 83682 | mana | open room (scary) | complete  | 4445 |
| 1516096046 | Druid | 3400 | 2931 | hp | room edge/junction | complete  | 469 |
| 1569794094 | Priest | 8158 | 8062 | hp | room edge/junction | complete  | 96 |
| 300461652 | Mage | 3211 | 1131 | hp | stairs | complete  | 2080 |

deaths with an interrupted rest within 2000 turns before: 1

### Candidate rules: rests they would touch (dungeon)
| rule | rests touched | of them interrupted | attacked | deaths within window after a touched rest |
|---|---:|---:|---:|---:|
| where: not in an open room (walk to stairs/corridor) | 3151 | 508 (16%) | 205 | 2 |
| where: not next to unknown grids | 3 | 0 (0%) | 0 | 0 |
| when: scary level, not on stairs | 377 | 112 (30%) | 28 | 0 |
| when: an awake monster seen within 20 | 1609 | 379 (24%) | 111 | 1 |
| when: an awake monster seen within 50 | 1769 | 405 (23%) | 123 | 1 |
| when: after two interruptions on one grid | 468 | 100 (21%) | 35 | 0 |
| (all dungeon rests) | 5992 | 915 (15%) | 380 | 2 |
