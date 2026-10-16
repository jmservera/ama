"""Run only constructed local evaluation data. Requires the documented absolute test paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from regulatory_gate_fixture import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--homes", type=int, default=60000)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    report = run(args.homes)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.write_text(text)
    print(text, end="")
    # Exit status is process execution, not an aggregate evaluation verdict.
    # Each check and the cards-only recommendation remain in the report.


if __name__ == "__main__":
    main()
