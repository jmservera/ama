#!/usr/bin/env python3
"""Deterministic offline region and quota preflight for an environment parameter set (issue 137).

Reads a .bicepparam file and, optionally, a JSON check record, and reports whether the region and
quota choices are explicit and covered by a recorded check. It never calls Azure, never reads
secrets and never approves a deployment: a human verifies the record's contents and freshness.

Record schema (JSON object): {"checked_on": "YYYY-MM-DD", "regions": ["uksouth"],
"quotas": [{"name": "...", "region": "...", "limit": 50, "used": 2, "requested": 30}]}

Exit code 0 only when every check passes; 1 otherwise.

Example:
  python3 infra/scripts/region_quota_preflight.py infra/main.test.bicepparam --record check.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LOCATION_PARAMS = ("location", "sqlLocation", "aiModelLocation")
REQUIRED_PARAMS = (
    *LOCATION_PARAMS,
    "modelCapacityBudget",
    "regionCheckReference",
    "quotaCheckReference",
)
PARAM_LINE = re.compile(r"^param\s+(\w+)\s*=\s*(?:'([^']*)'|(-?\d+)|(true|false))", re.MULTILINE)


def read_params(text: str) -> dict[str, str | int | bool]:
    params: dict[str, str | int | bool] = {}
    for name, string, number, boolean in PARAM_LINE.findall(text):
        if number:
            params[name] = int(number)
        elif boolean:
            params[name] = boolean == "true"
        else:
            params[name] = string
    return params


def read_capacity(text: str) -> list[int] | None:
    """Capacity units the parameter file requests: modelDeployments entries, else chatModelCapacity.

    Returns None when modelDeployments is set but a capacity is not an integer literal.
    """
    match = re.search(r"^param\s+modelDeployments\s*=\s*\[", text, re.MULTILINE)
    if match:
        depth, end = 1, match.end()
        while end < len(text) and depth:
            depth += {"[": 1, "]": -1}.get(text[end], 0)
            end += 1
        block = text[match.end() : end - 1]
        capacities = [int(c) for c in re.findall(r"\bcapacity\s*[:=]\s*(\d+)\s*(?=[,}\n])", block)]
        return capacities if capacities and len(capacities) == block.count("{") else None
    chat = re.search(r"^param\s+chatModelCapacity\s*=\s*(\d+)", text, re.MULTILINE)
    return [int(chat.group(1)) if chat else 1]


def evaluate(
    params: dict[str, str | int | bool],
    record: dict | None = None,
    capacities: list[int] | None = None,
) -> list[dict]:
    """Return an ordered list of {check, status, detail}; status is pass, fail or blocked."""
    results: list[dict] = []

    def add(check: str, status: str, detail: str) -> None:
        results.append({"check": check, "status": status, "detail": detail})

    missing = [name for name in REQUIRED_PARAMS if name not in params]
    add(
        "parameters-explicit",
        "fail" if missing else "pass",
        f"missing: {', '.join(missing)}" if missing else "all region and quota parameters set",
    )
    for name in LOCATION_PARAMS:
        value = params.get(name)
        add(
            f"{name}-selected",
            "pass" if value else "blocked",
            f"{name}={value}" if value else f"{name} is an unresolved placeholder",
        )
    fallback = params.get("aiModelFallbackLocation", "")
    if fallback and fallback == params.get("aiModelLocation"):
        add("fallback-differs", "fail", "aiModelFallbackLocation equals aiModelLocation")
    for name in ("regionCheckReference", "quotaCheckReference"):
        add(
            f"{name}-recorded",
            "pass" if params.get(name) else "blocked",
            "reference present" if params.get(name) else f"{name} is empty; deployment is blocked",
        )
    budget = params.get("modelCapacityBudget")
    param_total = sum(capacities) if capacities else 0
    if capacities is not None and isinstance(budget, int):
        add(
            "parameter-capacity-budget",
            "fail" if param_total > budget else "pass",
            f"parameterised capacity {param_total} vs modelCapacityBudget {budget}",
        )
    if record is None:
        add("check-record", "blocked", "no check record supplied")
        return results
    regions = set(record.get("regions", []))
    wanted = {params.get(n) for n in (*LOCATION_PARAMS, "aiModelFallbackLocation") if params.get(n)}
    uncovered = sorted(str(r) for r in wanted - regions)
    add(
        "regions-covered",
        "fail" if uncovered else "pass",
        f"not in record: {', '.join(uncovered)}" if uncovered else "every selected region recorded",
    )
    add(
        "record-dated",
        "pass" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("checked_on", ""))) else "fail",
        f"checked_on={record.get('checked_on')}",
    )
    for quota in record.get("quotas", []):
        try:
            headroom = int(quota["limit"]) - int(quota["used"]) - int(quota["requested"])
        except (KeyError, TypeError, ValueError):
            add(f"quota-{quota.get('name')}", "fail", "limit, used and requested must be integers")
            continue
        add(
            f"quota-{quota.get('name')}",
            "pass" if headroom >= 0 else "fail",
            f"headroom={headroom} in {quota.get('region')}",
        )
    if not record.get("quotas"):
        add("quota-records", "fail", "record has no quota entries")
    requested = sum(
        int(q.get("requested", 0))
        for q in record.get("quotas", [])
        if str(q.get("name", "")).startswith("model")
    )
    if isinstance(budget, int) and requested > budget:
        add("model-budget", "fail", f"requested {requested} exceeds modelCapacityBudget {budget}")
    if capacities is not None:
        add(
            "record-covers-parameter-capacity",
            "pass" if requested >= param_total else "fail",
            f"recorded model requests {requested} vs parameterised capacity {param_total}",
        )
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("param_file", type=Path, nargs="?", help=".bicepparam file")
    parser.add_argument("--bicepparam", type=Path, help="same as the positional .bicepparam file")
    parser.add_argument("--record", type=Path, help="JSON check record")
    args = parser.parse_args(argv)
    param_file = args.bicepparam or args.param_file
    if param_file is None:
        parser.error("a .bicepparam file is required")
    text = param_file.read_text(encoding="utf-8")
    params = read_params(text)
    capacities = read_capacity(text)
    record = json.loads(args.record.read_text(encoding="utf-8")) if args.record else None
    results = evaluate(params, record, capacities)
    if capacities is None:
        results.append(
            {
                "check": "parameter-capacity-parsed",
                "status": "fail",
                "detail": "modelDeployments capacity is not an integer literal in the file",
            }
        )
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if all(r["status"] == "pass" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
