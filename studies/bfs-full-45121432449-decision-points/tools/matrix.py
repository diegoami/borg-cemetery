"""Render the per-death matrix from the Zoo cells and replay results."""

import argparse
from collections import Counter
import json
from pathlib import Path

from div2 import divergence

ARM_NAMES = ("p934", "flee100", "flee1", "osc", "bundle", "conf", "phase50", "phasefear", "recall0")
OUTCOME_CODES = {
    "near lives": "**L**",
    "near dies": "D",
    "early lives": "l",
    "early dies": "d",
    "identical": "=",
    "failed": "!",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=Path, default=Path("cells.jsonl"))
    parser.add_argument("--results", type=Path,
                        default=Path(__file__).resolve().parents[1] / "evidence" / "cf-deaths.jsonl")
    parser.add_argument("--deaths", type=Path, default=Path("D"))
    parser.add_argument("--work", type=Path, default=Path("cfw"))
    args = parser.parse_args()

    cells = (json.loads(line) for line in args.cells.read_text().splitlines())
    deaths = sorted(
        (cell for cell in cells if cell["outcome"] == "death"),
        key=lambda cell: (cell["cause"] != "poison", cell["profile"], cell["seed"]),
    )
    results = {}
    for line in args.results.read_text().splitlines():
        row = json.loads(line)
        key = (row["arm"], row["profile"], row["seed"])
        if key in results:
            parser.error(f"duplicate result for {key}")
        results[key] = row

    print("| seed | arm | killer | " + " | ".join(ARM_NAMES) + " |")
    print("|---:|---|---|" + "|".join(":-:" for _ in ARM_NAMES) + "|")
    totals = Counter()
    for death in deaths:
        seed, profile = death["seed"], death["profile"]
        codes = []
        for arm in ARM_NAMES:
            row = results.get((arm, profile, seed))
            if row is None:
                code = "?"
            else:
                outcome, _, _ = divergence(row, args.deaths, args.work)
                code = OUTCOME_CODES[outcome]
            codes.append(code)
            totals[arm, code] += 1
        tag = profile.removeprefix("reborn-bfs-")
        print(f"| {seed} | {tag} | {death['cause']} | " + " | ".join(codes) + " |")

    legend = (
        ("**L**", "lives, diverged ≤ 2,000 game turns before the last original key"),
        ("D", "still dies, diverged near"),
        ("l", "lives, diverged earlier"),
        ("d", "dies, diverged earlier"),
        ("=", "identical play"),
        ("!", "failed replay or missing/invalid key evidence"),
        ("?", "missing replay result"),
    )
    for code, label in legend:
        counts = [totals[arm, code] for arm in ARM_NAMES]
        if code in {"!", "?"} and not any(counts):
            continue
        print(f"| {code} | | {label} | " + " | ".join(map(str, counts)) + " |")


if __name__ == "__main__":
    main()
