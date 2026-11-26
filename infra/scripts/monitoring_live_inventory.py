"""Classify live Azure alert inventory against issue #146 criterion 1 (read-only, offline).

Input is the JSON from `az monitor metrics alert list` and `az monitor scheduled-query list`.
Only rule name, class and enabled flag are reported. Coverage is never `proven`: an installed,
enabled rule does not show that it fires or notifies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

CLASSES: dict[str, re.Pattern[str]] = {
    "job_failure": re.compile(r"^alert-job-.+-failed$"),
    "poison_queue": re.compile(r"^alert-.+-agent-tasks-poison$"),
    "ledger_digest": re.compile(r"^alert-.+-ledger-(digest-mismatch|verify-missing)$"),
    "iot_ingestion": re.compile(r"^alert-.+-iot-.+$"),
}


def classify(
    rules: Sequence[Mapping[str, Any]], jobs: Sequence[str] | None = None
) -> dict[str, Any]:
    classes: dict[str, Any] = {}
    for label, pattern in CLASSES.items():
        matched = [
            {"name": str(r["name"]), "enabled": r.get("enabled") is True}
            for r in rules
            if pattern.match(str(r.get("name", "")))
        ]
        if any(m["enabled"] for m in matched):
            status = "enabled"
        elif matched:
            status = "disabled"
        else:
            status = "missing"
        entry: dict[str, Any] = {
            "status": status,
            "rules": sorted(matched, key=lambda m: m["name"]),
        }
        if label == "job_failure" and jobs is not None:
            enabled_names = {m["name"] for m in matched if m["enabled"]}
            uncovered = sorted(j for j in jobs if f"alert-{j}-failed" not in enabled_names)
            entry["uncovered_jobs"] = uncovered
            if status == "enabled" and uncovered:
                entry["status"] = "partial"
        classes[label] = entry
    all_enabled = all(c["status"] == "enabled" for c in classes.values())
    return {
        "classes": classes,
        "coverage": "partial"
        if any(c["status"] in ("enabled", "partial") for c in classes.values())
        else "none",
        "all_classes_enabled": all_enabled,
        "firing_observed": False,
    }


def _load(path: Path) -> list[Mapping[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError(f"{path} must be a JSON list of rule objects")
    return data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metric-alerts", type=Path, required=True)
    parser.add_argument("--scheduled-queries", type=Path, required=True)
    parser.add_argument(
        "--jobs", type=Path, help="`az containerapp job list` JSON; reports jobs lacking a rule"
    )
    args = parser.parse_args(argv)
    try:
        rules = _load(args.metric_alerts) + _load(args.scheduled_queries)
        jobs = [str(j["name"]) for j in _load(args.jobs)] if args.jobs else None
    except (OSError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(classify(rules, jobs), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
