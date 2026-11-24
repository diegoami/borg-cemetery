"""Classify counterfactual outcomes and their timing relative to the last original key."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

CAP = 100_000
NEAR = 2_000


def replay_outcome(summary):
    if summary.get("stop_reason") == "death":
        return "dies"
    if summary.get("stop_reason") == "turns" and summary.get("game_turns") == CAP:
        return "lives"
    return "failed"


def divergence(row, deaths, work):
    outcome = replay_outcome(row["summary"])
    if row.get("error") or outcome == "failed":
        return "failed", None, None
    if row["same_play"]:
        return "identical", None, None

    profile = row["profile"]
    seed = row["seed"]
    original = deaths / f"{seed}_{profile.removeprefix('reborn-bfs-')}" / "keys.log"
    changed = work / row["arm"] / f"{profile}-{seed}" / "keys.log"
    try:
        original_keys = original.read_text().splitlines()
        changed_keys = changed.read_text().splitlines()
        if not original_keys or not changed_keys or original_keys == changed_keys:
            return "failed", None, None
        first_diff = next(
            (index for index, (left, right) in enumerate(zip(original_keys, changed_keys))
             if left != right),
            min(len(original_keys), len(changed_keys)),
        )
        turn = int(original_keys[min(first_diff, len(original_keys) - 1)].split()[0])
        last_turn = int(original_keys[-1].split()[0])
    except (OSError, ValueError, IndexError):
        return "failed", None, None

    timing = "near" if last_turn - turn <= NEAR else "early"
    return f"{timing} {outcome}", turn, last_turn


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="+", type=Path)
    parser.add_argument("--deaths", type=Path, default=Path("D"))
    parser.add_argument("--work", type=Path, default=Path("cfw"))
    args = parser.parse_args()
    counts = defaultdict(Counter)
    for path in args.results:
        for line in path.read_text().splitlines():
            row = json.loads(line)
            outcome, turn, last_turn = divergence(row, args.deaths, args.work)
            timing = f" t{turn} → t{last_turn}" if turn is not None else ""
            print(f"{row['arm']} {row['seed']} {row['profile']}: {outcome}{timing}")
            counts[row["arm"]][outcome] += 1
    for arm, outcomes in counts.items():
        print(arm, dict(outcomes))


if __name__ == "__main__":
    main()
