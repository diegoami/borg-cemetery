---
name: animate-death
description: Make an animated GIF of the last X game turns before a death in a borg-zoo run - screens from verified replays, with game messages and Borg notes. Use when the owner asks to animate, show or watch the last turns of a game/death from a zoo run, or types /animate-death.
---

# /animate-death

Arguments: the game and the number of turns, e.g. `/animate-death run 44051234567 seed 934061548 profile reborn-heal1-trip0-plan 1000`
or `/animate-death D-02cc 500`. The tool is `scripts/animate_death.py`;
README "Animate the last turns of a zoo death" documents it.

1. **Find the dossier.**
   - A case ID or prefix (`D-…`): use it directly.
   - A zoo run plus a game: open `runs/zoo-*-<RUN>/deaths.json` and pick the row
     by seed, and by profile or specimen if the seed played several arms. Its
     `case` is the dossier. If more than one row matches, list them and ask.
   - If the run has not been imported yet (no `runs/zoo-*-<RUN>/`), import it into a
     scratch registry so nothing in the repository changes:
     `BORG_DEATH_RECORDS_DIR=<scratch>/deaths python3 scripts/import_zoo_deaths.py --run <RUN>`,
     then use `<scratch>/deaths/<case>`. Say that the dossier is not in the cemetery yet.
   - A game whose row says `skipped`, or a game that did not die, cannot be
     animated. Report the reason from the run page.
2. **Turns.** X is in game turns, the unit of the dossier's death turn: at
   normal speed, one player turn is 10 game turns. If the owner says "player
   turns" or "moves", multiply by 10 and say so. Use 24 frames unless asked otherwise.
3. **Run it** under the shared lock, Pillow installed (`requirements-media.txt`):
   ```bash
   flock /tmp/angband-validation.lock python3 scripts/animate_death.py CASE --turns X [--frames N]
   ```
   The first use of a commit builds it into the cemetery cache, as the case's `./build.sh`
   would, which takes a few minutes. Use `--out <scratch>` when the dossier
   is in a scratch registry or the owner only wants to look.
   If it stops with "does not reproduce its recorded keys", do not retry with another build. Report it.
4. **Check and show.** Read the JSON receipt (`status`, `frames`, `dropped`). Extract
   two or three frames to PNG (Pillow `seek`) and look at them. Tell the owner
   what happens in the window: HP, depth, the monsters in the messages, and
   what the Borg notes say it was doing. Give the full GIF path.
5. **Publishing.** Adding it to the cemetery is a repository change. The GIF and
   receipt go in the dossier's `media/`; run
   `python3 scripts/register_deaths.py` so the death page embeds it, then
   commit and push on a branch with a PR (AGENTS.md Delivery). A GIF made in a
   scratch registry or with `--out` elsewhere is not published.

Frames are reruns of the same life, not new samples. Never present a dropped
frame or a partial animation as complete.
