# Mage stalled at passable rubble

[Targeting issue #979](https://github.com/diegoami/borg-reborn-rs/issues/979) ·
[Restore Life Levels issue #978](https://github.com/diegoami/borg-reborn-rs/issues/978)

The owner used Ctrl+S at turn 10,815,143 after stopping the Borg and
before moving. The saved CL37 Gnome Mage is at (133,56) on DL1 with
386/386 HP and 255/297 SP. Passable rubble at (127,56) separates the
Mage from the wild dog at (126,56). The preceding recording shows
7,856 Acid Spray attempts aimed there. The dog remains at 3 HP.

The native reload on the original executable confirms the character,
depth and save turn. The bounded headless verification produced zero
game inputs and stopped at the saved turn. A fresh Borg starts with
new decision memory. The original recording establishes the stall.

The [compressed save](start.save.gz) is accompanied by its game and
settings checksums in [scenario.json](scenario.json). Use a private
directory for each reload. From here, run the recorded executable with
its original data directory as the working directory:

```sh
fixture="$PWD"
trial="$(mktemp -d)"
mkdir -p "$trial"/{user,save,archive,panic,scores}
cp "$fixture"/{borg.txt,errands_plan.txt,scary_monsters.txt} "$trial/user/"
gzip -dc "$fixture/start.save.gz" >"$trial/save/RubbleMage"
cd /home/diego/angband-builds/borg-reborn-rs-recording-4b2c2fcf/launcher/game
./angband -mx11 -duser="$trial/user" -dsave="$trial/save" \
  -darchive="$trial/archive" -dpanic="$trial/panic" -dscores="$trial/scores" \
  -uRubbleMage
```

## Restore Life Levels

At the save the Mage has 711,985 XP, below the 713,458 observed directly
before the recorded non-permanent drain. It has no Restore Life Levels
potion and carries 787,811 gold. This is a candidate for a controlled
drained-state test with a potion in the pack or an affordable Alchemist
offer. Evidence of earlier stock destruction and no-benefit quaffs is
recorded separately in [Cemetery PR #123](https://github.com/diegoami/borg-cemetery/pull/123).
