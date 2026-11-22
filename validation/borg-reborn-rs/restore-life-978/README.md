# Restore Life Levels used and discarded as junk

[borg-reborn-rs #978](https://github.com/diegoami/borg-reborn-rs/issues/978)

Live Gnome Mage recording `20261122-142315-1.JptJU1/native` on
Track P `4b2c2fcf913e352ebd7bef5f16a531e8fc50d92a`.
The recorder's executable SHA-256 was
`3a298a35a53bd6e1ba43fe25295ea0c522501a03ae43f724826e02942eb7cf62`.

| Game turn | Evidence |
| ---: | --- |
| 4,981,588 | Town plan sale at the Alchemist. The sale removes the single Restore Life Levels potion. |
| 7,315,201 | Full-pack junk action drinks the first of two potions. The before and after frames show 365,281 XP. |
| 7,315,206 | The remaining potion is inscribed as junk, dropped and subsequently destroyed. |
| 7,832,293 | The full-pack junk action repeats after two more potions are picked up. Before and after frames show 461,802 XP. |
| 7,832,300 | The spare is discarded, leaving none. |
| 10,076,838 | CL37 Mage loses 14,310 XP to a non-permanent drain. Frames around the event show XP falling from 713,458 to 699,148. |
| 10,472,678 | Alchemist visit, 711,478 XP, 787,466 gold before buying one Word of Recall. No Restore Life Levels in the pack. |
| 10,595,479 | Latest frame in the checked range. 711,985 XP, still below the observed pre-drain XP, with no potion in the carried gear. |

The complete message stream through the checked turn contains two junk
quaffs, zero Restore Life Levels purchases, and no message from a
successful restoration. There are 62 logged Alchemist entries from the
last drain through the captured message endpoint. The Borg's internal
shop visits do not expose a reliable shop inventory in these terminal
frames, so availability at those visits remains unverified. The potion
is rotating Alchemist stock in the engine's `store.txt`.

The first two quaffs are immediately preceded by the full-pack junk
decision. The engine only increases experience for Restore Life Levels
when `exp < max_exp` (`effect-handler-general.c:effect_handler_RESTORE_EXP`).
The normal quaff decision requires that condition. The junk quaff list
has no such condition, and the town capability curve assigns experience
restoration no value before drain. These paths can remove the only
carried reserve before later drain occurs.

[Relevant recorded messages](messages.tsv) · [Frame receipts](frames.tsv)
