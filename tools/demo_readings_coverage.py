"""Measure the share of demo homes with sensor readings from saved map snapshots (issue 2202).

`/api/map?sensors=1` loads sensor states for at most 100 homes per call, so a whole-estate answer
needs several bbox tiles. Merge them here: the result is a lower bound, because homes whose state
was not loaded are never assumed to have readings.

Usage:
    python tools/demo_readings_coverage.py SNAPSHOT.json [SNAPSHOT.json ...]
Each file holds the JSON body of /api/map (an object with `items`). Exit 0 when at least half of
all homes are known to have readings, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from typing import Any

WITH_READINGS = ("fresh", "stale", "offline")
UNMEASURED = ("not-loaded", "unavailable", "restricted", "not-connected")
SHARE = 0.5


def coverage(snapshots: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Merge snapshots by home id, preferring a measured state over an unmeasured one."""
    homes: dict[str, str] = {}
    for snap in snapshots:
        for item in snap.get("items", []):
            state = (item.get("sensor") or {}).get("state", "not-loaded")
            old = homes.get(item["id"])
            if old is None or (old in UNMEASURED and state not in UNMEASURED):
                homes[item["id"]] = state
    states: dict[str, int] = {}
    for state in homes.values():
        states[state] = states.get(state, 0) + 1
    total = len(homes)
    with_readings = sum(states.get(s, 0) for s in WITH_READINGS)
    unmeasured = sum(states.get(s, 0) for s in UNMEASURED)
    return {
        "total": total,
        "states": dict(sorted(states.items())),
        "with_readings": with_readings,
        "recent": states.get("fresh", 0),
        "unmeasured": unmeasured,
        "with_readings_share": with_readings / total if total else 0.0,
        "recent_share": states.get("fresh", 0) / total if total else 0.0,
        "complete": total > 0 and unmeasured == 0,
    }


def meets(result: dict[str, Any], share: float = SHARE) -> bool:
    return bool(result["total"]) and result["with_readings_share"] >= share


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    snaps = []
    for path in argv:
        with open(path, encoding="utf-8") as fh:
            snaps.append(json.load(fh))
    result = coverage(snaps)
    result["meets_half"] = meets(result)
    print(json.dumps(result, indent=1))
    return 0 if result["meets_half"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
