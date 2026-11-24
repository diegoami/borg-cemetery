# Six spare daggers on current Track P

Replay of the original [CL17 Mage save](../../start.save.gz) on
borg-reborn-rs `11214501638b3d172113d41c10a304932c925f51`, with shipped
borg-rs and the engine RNG preserved. The [recorded live inventory](../../inventory-screen.txt)
has six daggers in distinct pack slots, 7.2 lb total.

The first town plan at turn 9,230,469 classified all six as unknown
wearables. The Mage dropped the known-cursed dagger at turn 9,231,365.
At departure, turn 9,231,544, the five other daggers still occupied
five slots and weighed 6.0 lb. Each had zero swap-power gain in the
planner and a keep disposition. The run recorded no identification
attempt. One book with Identify Rune is [Attacks and Knowledge].
The live pack inspection shows [First Spells].

The native Dagger kind has the THROWING flag. The shipped Borg's throw
chooser excludes objects with a wield slot, including daggers. Unknown
wearable retention is tracked in
[#1169](https://github.com/diegoami/borg-reborn-rs/issues/1169).
Using known surplus objects as attacks is tracked in
[#1200](https://github.com/diegoami/borg-reborn-rs/issues/1200).

[Receipts](receipts.json) pin the save, build and settings and record the
town observations. The messages and plan are compressed alongside them.
This is one recorded Mage life. It gives no direct Priest population
evidence.

To replay from the pinned source checkout, decompress the input into a
private save directory and pass that directory as `SAVE_ROOT`.

```sh
BORG_TOWN_PLAN_RECORD="$trial/town-plan.jsonl" \
  flock /tmp/angband-validation.lock harness/run.sh "$trial/run" 1 4 1 9241204 \
  menu,finalsave,keep-load-rng,save=recorded-mage.save
```
