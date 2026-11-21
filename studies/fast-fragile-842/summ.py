#!/usr/bin/env python3
"""usage: summ.py OUTDIR ARM... -> a table of the 8 crow cases per arm."""
import json, re, sys
from pathlib import Path

out = Path(sys.argv[1])
arms = sys.argv[2:]
cases = [("Dwarf Mage", 896890415), ("Human Ranger", 526144893), ("Gnome Druid", 1311931798),
         ("Kobold Priest", 994753489), ("Dunadan Priest", 1309976551),
         ("H-Troll Necro", 1705507033), ("Half-Elf Druid", 733550937), ("Dwarf Necro", 258108142)]
print("| case | " + " | ".join(arms) + " |")
print("|---|" + "---|" * len(arms))
tot = {a: dict(dead=0, crow=0, clw=0, oil=0, phase=0, stairs=0, ff=0) for a in arms}
for name, seed in cases:
    row = []
    for a in arms:
        run = out / a / f"run-{seed}" / "run"
        try:
            s = json.load(open(run / "summary.json"))
        except Exception:
            row.append("n/a"); continue
        msgs = (run / "messages.log").read_text(errors="replace")
        clw = len(re.findall(r"# Healing Level|# Healing \(outmatched\)", msgs))
        oil = len(re.findall(r"# Throwing painful object 'Flask", msgs))
        ph = len(re.findall(r"Fast-fragile: .*Phase Door", msgs))
        st = len(re.findall(r"Fast-fragile: .*stairs underfoot", msgs))
        ff = len(re.findall(r"# Fast-fragile \(", msgs))
        t = tot[a]
        if s["dead"]:
            t["dead"] += 1
            if "crow" in s["death_cause"] or "cat" in s["death_cause"]:
                t["crow"] += 1
        t["clw"] += clw; t["oil"] += oil; t["phase"] += ph; t["stairs"] += st; t["ff"] += ff
        end = f"died ({s['death_cause']}) CL{s['clevel']} DL{s['depth']} t{s['game_turns']}" if s["dead"] else f"alive CL{s['clevel']} maxDL{s['max_depth']} t{s['game_turns']}"
        row.append(f"{end}; heals {clw}, oil {oil}, phase {ph}, stairs {st}")
    print(f"| {name} {seed} | " + " | ".join(row) + " |")
print()
for a in arms:
    t = tot[a]
    print(f"{a}: dead {t['dead']}/8, to crow/cat {t['crow']}, heals {t['clw']}, oil {t['oil']}, phase {t['phase']}, stairs {t['stairs']}, ff-notes {t['ff']}")
