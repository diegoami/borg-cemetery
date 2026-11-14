# Local pipeline validation, 2026-11-14

Original natural-death evidence from `borg-reborn-rs` commit
`e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71`, seed **102**, Elf Mage
(birth menu race 2/class 1), default profile, cap 100000 engine turns.
The run died to Fang at engine turn 3640. `native-dossier/` is the
upstream export, preserved as written. Its `D0001` identifier is local to
the isolated validation registry, not the cemetery's historical D0001.

`analysis/` was extracted from this run's original state/decision streams.
It contains one death event and three structured decisions in the selected
windows. It is not a qualified rewind or tuning experiment. This selected
validation run is not a survival-rate cohort.

The raw local evidence was written to
`/tmp/cemetery-reborn-death-validation-20261114`; raw streams/saves are not
copied here. Their hashes are retained by the native dossier. The pipeline
was also smoke-checked against `borg-rs` commit
`122185ba36c352bdbec455bd6c7c7e2dca3823fb`, Human Warrior seed 8400,
alive at the 1000-turn cap (observed engine turn 1001), and reborn Human
Mage seed 102, alive at a 5000-turn cap. These are different births from
the Elf Mage death retained here.

## Sequence report and saved-position trial

The later `sequence-analysis-v2/` adds an adaptive chronology and an actual
compressed starting save. A repeat of this same seeded birth with checkpoint
capture produced a byte-identical key stream; it is not another independent
life. The inferred stable boundary is turn 3432 and the selected save is from
turn 3402, before the decline and Fang death at 3640. See the
[sequence report](sequence-analysis-v2/event-1/report.md).

Both original reborn `e9a6a521f3ac2fc631aed2c2e3d6c595dde9ab71` and alternative
borg-rs `122185ba36c352bdbec455bd6c7c7e2dca3823fb` loaded that same save at turn
3402 with saved engine RNG and fresh Borg memory. Reborn died at 3640; borg-rs
survived the 1000-engine-turn target horizon, stopping at 4411 (cap 4402; the
native frontend stops at its next boundary). The compact trial receipts and
comparison are retained beside the report. These builds contain different
engine/Borg implementations, so this compares complete versions from one saved
position; it does not isolate a particular policy or establish general benefit.

## Inventory and screenshot animation

The additive `episode-media-v3/` includes the
[inventory and chronological report](episode-media-v3/event-3/report.md) and a
[23-frame screenshot GIF](episode-media-v3/event-3/media/episode.gif), under 1 MB.
The death episode runs from the inferred stable state at turn 3432 to death at
3640 and retains the checkpoint at 3402. Two earlier near-death candidates that
recovered have their own reports, inventories and shorter GIFs under `event-1/`
and `event-2/`.

Inventory was recovered by a same-source, same-birth observation-logging rerun
whose complete key and state streams matched the original byte-for-byte. Each
sampled terminal screen was captured by replaying to a verified key/state prefix;
the terminal death screen comes from the original run. The GIF uses monochrome
terminal glyphs, with observed item quantities and the last Borg decision in a
side panel. `media/media.json` retains screenshot/provenance hashes. Earlier
reports and the saved-position comparison above are preserved as written.
