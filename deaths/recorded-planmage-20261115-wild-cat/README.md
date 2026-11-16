# Recorded PlanMage wild-cat death

**Canonical incident and scenario home: Borg Cemetery.** Original human/Borg
recordings and working play state remain in player-cemetery; source repositories
contain code/tests and links, not duplicate gameplay reports.

Level5 Gnome Mage, DL1, death at411674. The original full replay verifies;
four nearby native saves match its world fingerprints. The original source
fails all four saved-position trials; #355 survives its bounded checks.
These are repeated starts from one life, with fresh Borg memory after reload.

- [Incident report](report.md)
- [Four-step death sequence](trace-final.jsonl)
- [Original versus #355 comparisons](fix-350/README.md)
- [Observed attack scores: melee25, Magic Missile17](magic-missile-scores.json)
- [Play at26 HP](../../scenarios/planmage-wild-cat-411638/README.md)
- [Play at19 HP](../../scenarios/planmage-wild-cat-411648/README.md)
- [Play at14 HP, two player actions before death](../../scenarios/planmage-wild-cat-411658/README.md)
- [Play at4 HP, final decision](../../scenarios/planmage-wild-cat-411668/README.md)

Post-merge review and owner-requested improvements are tracked in
[borg-reborn-rs#369](https://github.com/diegoami/borg-reborn-rs/issues/369).
Known landing danger, healing-before-escape, heal parameters, fight-through,
Magic Missile scoring and missing scroll reserves are being investigated.
The zoo comparison is paused until those improvements are tested.

Historical reports copied verbatim into history/ preserve their earlier
wording and provenance. They are not claims that subsequent findings were
already known. Original recording hashes and published export history stay
unchanged; current source/player report locations will redirect here.
