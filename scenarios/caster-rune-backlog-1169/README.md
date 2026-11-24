# Caster rune backlog (#1169)

These named replays use the shipped borg-rs core at
[`e34d04b788a5f6a9b600268231cfe6c4e260e820`](https://github.com/diegoami/borg-reborn-rs/commit/e34d04b788a5f6a9b600268231cfe6c4e260e820).
They start with fresh Borg memory and saved engine RNG. The original Mage input
is the unchanged [published CL17 save](../mage-overweight-cursed-kit-9221204/start.save.gz).
The control reproduces the prior replay's keys, messages, state and town plan
byte for byte. [Original replay](../mage-overweight-cursed-kit-9221204/replays/11214501-daggers)

## Mage

The constructed arm adds one copy of Attacks and Knowledge with Identify Rune
already learned. The original Mage had 24/24 SP, so the author did not
replenish it. The engine requires CL8 and 7 SP for the spell. The ordinary
Borg casts it after recovering in place on DL1. The trial grants no rune
knowledge. The book also lets the Borg study other spells, and the route
diverges before the first town visit.

| Original slot | Dagger | Rune or runes learned | Actual disposition |
| --- | --- | --- | --- |
| 11 | (+0,+0) [+20], known cursed | Air swing, 9,228,494 | Dropped at 9,229,281, shown as (−20,+0) after identification |
| 12 | (+4,+5) | Slay orcs, 9,224,494 | Dropped at 9,286,279, picked up at 9,286,301, dropped again at 9,286,311 |
| 13 | (+3,+2) | Slay demons via Mace, 9,222,514 | Dropped at 9,290,290 |
| 14 | (+2,+2) | Slay demons via Mace, 9,222,514 | Dropped at 9,287,031 |
| 15 | (+4,+1) | Demon summon, 9,225,154, and undead summon, 9,228,514 | Dropped at 9,229,253 |
| 16 | (+1,+1) | Slay giants, 9,225,814 | Dropped at 9,238,985 |

The six daggers started in six slots, at 1.2 lb each. All six original
slots were released before first town arrival in the book arm. The two
Slay Demon weapons became known from one cast on a different item. The
book arm had 14 free slots at the last town plan versus six for the
control. The actual stair turns were 9,340,413 and 9,231,654. The control
carried five original daggers weighing 6 lb at departure. The book arm
carried zero and had eight charges left in the Wand of Magic Missile
picked up at 9,292,223 and aimed twice. Its post-stair save inspection
shows the wand in pack slot 7. No mushroom was carried. The route, loot
and other pack dispositions changed, so this comparison does not isolate
the dagger slots as the reason for retaining the wand.

Counting game turns to full identification or permanent removal, or to
the first stair for survivors, the six original daggers occupied 62,411
unknown slot-turns in the control and 25,120 in the book arm. Fully
identified items still occupy slots until removed. The book arm found
other daggers later, including one whose slay trolls rune was learned at
9,318,978. Those items are outside the six-item accounting.

## Priest

The Dunadan Priest is an independent natural seed (399497898), captured at
turn 600,016, CL10, DL1, max DL3. The paired constructed inputs open and
light a room, clear monsters, add an unknown (+2,+0) Dagger with a
resist nexus rune, and set an equal pending Recall to town. The scroll
arm adds a stack of three known Identify Rune scrolls. The Priest spell
list offers no Identify Rune equivalent. The scroll arm learned resist
fire and slay trolls on the equipped War Hammer before learning resist
nexus from the Dagger, at 600,046, 600,056 and 600,066 respectively.

Both arms entered town at 600,661. The control left at 601,631 with the
unknown Dagger. The scroll arm sold it at 600,771 and left at 603,163
with an upgraded device stack. It bought one Wand of Light with 13
charges and merged it into its existing stack of two. A Treasure
Detection scroll also occupied a newly available slot. Both final town
plans had two slots free. The sale and purchase are observed. Differences
in actions and routes limit causal claims about the purchase. This is a
scroll-path demonstration on an early constructed Priest case.

## Proposed P9 change

Keep the existing protection for unidentified wearables. In a safe window
before returning or departing, reuse the existing Identify Rune action
when a learned spell can be cast with recoverable mana and unidentified
spares are blocking pack or weight headroom. Reobserve the entire pack
after each rune, since one rune can identify several objects. Then use
normal wear, swap and sale decisions on the refreshed kit. A zero swap
delta before identification gives no basis for disposal. For finite
scrolls, preserve the current target priorities and measure scroll cost
and the opportunity lost when worn gear takes priority.

The shipped action already handles the Mage's backlog when the book and
a safe window are available. Test earlier scheduling independently from
book acquisition. Compare unknown slot-turns, rune yield, useful upgrades
and swaps kept, and devices or mushrooms carried at departure in Zoo on
CL15–35 starts. The two named lives do not establish a class-wide buying,
junking or scroll threshold. Follow-up Home retrieval is #1170 and
throwing known surplus is #1200.

[Receipts](receipts.json) pin the exact inputs, build, resolved settings
and log streams. [Replay](replay.sh) uses files from this ordinary checkout.
