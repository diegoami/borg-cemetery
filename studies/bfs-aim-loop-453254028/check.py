"""Verify the #1132 death replay, its bounded prefix and the aim handoff."""

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "keys.log": "94d261a25ab26a759e193dd1d19130b4dbafa2b5b303aa53b9cea07f04f5ed1c",
    "messages.log": "c367b7a84f25daf27475fcac81a6ac7727e045f4c9d7fce9737d55a9b4e46c4d",
    "state.log": "088f9c85fd746142d6e8abaec08040866ae183b20af9633ae587430741384bd7",
}
STUDY = Path(__file__).resolve().parent
DOSSIER = STUDY.parents[1] / "deaths" / (
    "D-88768638033650b62916128147e2e9ee8ce6e53590c6d119d2d538df88f09e08"
)


def verify_hash(data, expected, label):
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SystemExit(f"{label} hash changed: {actual}")


def read_summary(run):
    summary = json.loads((run / "summary.json").read_text())
    if (summary["seed"], summary["race_idx"], summary["class_idx"], summary["loaded"]) != (
        453254028, 1, 4, False
    ):
        raise SystemExit(f"{run} is not the Half-Elf Necromancer birth run")
    return summary


def check(baseline, probe):
    death = read_summary(baseline)
    if (death["stop_reason"], death["game_turns"], death["death_cause"]) != (
        "death", 77923, "a floating eye"
    ):
        raise SystemExit("expected the unmodified replay to die to a floating eye at turn 77923")
    summary = read_summary(probe)
    if (summary["stop_reason"], summary["game_turns"]) != ("turns", 77500):
        raise SystemExit("expected the bounded replay to reach turn 77500")

    dossier = json.loads((DOSSIER / "record.json").read_text())
    death_hashes = dossier["attempts"][0]["raw_sha256"]
    for name, expected in EXPECTED.items():
        original = (baseline / name).read_bytes()
        bounded = (probe / name).read_bytes()
        verify_hash(original, death_hashes[name], f"baseline {name}")
        verify_hash(bounded, expected, f"probe {name}")
        if not original.startswith(bounded):
            raise SystemExit(f"probe {name} differs from the unmodified run before the cap")

    trace = (probe / "stderr.log").read_text()
    expected_trace = (STUDY / "trace.txt").read_text()
    if trace != expected_trace:
        raise SystemExit("aim handoff trace changed")
    print("verified the dossier death, all three 77,500-turn stream prefixes, and the aim trace")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path, help="unmodified death replay")
    parser.add_argument("probe", type=Path, help="bounded replay with the aim trace")
    args = parser.parse_args()
    check(args.baseline, args.probe)
