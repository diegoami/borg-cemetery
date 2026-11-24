"""Verify the bounded #1132 replay and its aim handoff."""

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "keys.log": "94d261a25ab26a759e193dd1d19130b4dbafa2b5b303aa53b9cea07f04f5ed1c",
    "messages.log": "c367b7a84f25daf27475fcac81a6ac7727e045f4c9d7fce9737d55a9b4e46c4d",
    "state.log": "088f9c85fd746142d6e8abaec08040866ae183b20af9633ae587430741384bd7",
}


def check(run):
    for name, expected in EXPECTED.items():
        actual = hashlib.sha256((run / name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"{name} hash changed: {actual}")
    summary = json.loads((run / "summary.json").read_text())
    if (summary["stop_reason"], summary["game_turns"]) != ("turns", 77500):
        raise SystemExit("expected the bounded replay to reach turn 77500")
    trace = (run / "stderr.log").read_text()
    expected_trace = Path(__file__).with_name("trace.txt").read_text()
    if trace != expected_trace:
        raise SystemExit("aim handoff trace changed")
    print("verified the 77,500-turn replay and aim trace")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    check(parser.parse_args().run)
