#!/usr/bin/env python3
"""Derive monthly temperature statistics from a local Met Office historic station file."""

import argparse
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re


def _temperature(token: str) -> tuple[float | None, str]:
    if token == "---":
        return None, "missing"
    if not re.fullmatch(r"-?\d+(?:\.\d+)?\*?", token):
        raise ValueError(f"Unrecognized temperature token: {token!r}")
    value = float(token.rstrip("*"))
    if not math.isfinite(value):
        raise ValueError("Nonfinite temperature")
    return value, "estimated" if token.endswith("*") else "valid"


def _summary(samples: list[dict], counts: dict[str, int], definition: str) -> dict:
    result = {
        "definition": definition,
        "unit": "degC",
        "status": "available" if samples else "unavailable",
        "counts": counts,
        "minimum": None,
        "maximum": None,
    }
    if samples:
        for label, value in (("minimum", min(s["value"] for s in samples)),
                             ("maximum", max(s["value"] for s in samples))):
            result[label] = {
                "value": value,
                "occurrences": [
                    {"month": s["month"], "source_line": s["source_line"]}
                    for s in samples if s["value"] == value
                ],
            }
    return result


def analyze(raw: bytes, *, source_url: str, retrieved_on: str,
            expected_sha256: str, start_year: int, end_year: int) -> dict:
    """Analyze one calendar window without network access, filling or RH inference."""
    if not 1 <= start_year <= end_year <= 9999:
        raise ValueError("Require 1 <= start-year <= end-year <= 9999")
    if date.fromisoformat(retrieved_on).isoformat() != retrieved_on:
        raise ValueError("retrieved-on must be YYYY-MM-DD")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"Input SHA-256 mismatch: got {digest}")
    if not source_url.startswith("https://"):
        raise ValueError("Source URL must use HTTPS")
    lines = raw.decode("utf-8").splitlines()
    header = "yyyy mm tmax tmin af rain sun"
    indexes = [i for i, line in enumerate(lines) if " ".join(line.split()) == header]
    if len(indexes) != 1 or indexes[0] < 2:
        raise ValueError("Expected one historic-station monthly schema header")
    start = indexes[0]
    if start + 1 >= len(lines) or lines[start + 1].split() != [
        "degC", "degC", "days", "mm", "hours"
    ]:
        raise ValueError("Unexpected station units")
    if not lines[1].startswith("Location:"):
        raise ValueError("Missing station location metadata")

    samples: dict[str, list[dict]] = {"tmax": [], "tmin": [], "midpoint": []}
    counts = {
        key: dict.fromkeys(("valid", "provisional", "missing", "estimated"), 0)
        for key in ("tmax", "tmin")
    }
    seen: set[str] = set()
    selected: set[str] = set()
    outside = 0
    for line_number, line in enumerate(lines[start + 2:], start=start + 3):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) not in (7, 8) or (
            len(fields) == 8 and fields[7] != "Provisional"
        ):
            raise ValueError(f"Malformed row at line {line_number}")
        try:
            year, month = int(fields[0]), int(fields[1])
            date(year, month, 1)
            values = [_temperature(t) for t in fields[2:4]]
        except ValueError as exc:
            raise ValueError(f"Invalid row at line {line_number}: {exc}") from exc
        key = f"{year:04}-{month:02}"
        if key in seen:
            raise ValueError(f"Duplicate month: {key}")
        seen.add(key)
        if not start_year <= year <= end_year:
            outside += 1
            continue
        selected.add(key)
        accepted: dict[str, float] = {}
        for variable, (value, quality) in zip(("tmax", "tmin"), values):
            category = "provisional" if len(fields) == 8 else quality
            counts[variable][category] += 1
            if category == "valid":
                assert value is not None
                accepted[variable] = value
                samples[variable].append(
                    {"value": value, "month": key, "source_line": line_number}
                )
        if len(accepted) == 2:
            if accepted["tmin"] > accepted["tmax"]:
                raise ValueError(f"tmin exceeds tmax at {key}")
            samples["midpoint"].append({
                "value": round((accepted["tmax"] + accepted["tmin"]) / 2, 2),
                "month": key, "source_line": line_number,
            })
    if not selected:
        raise ValueError("No records in selected window")
    expected = [
        f"{year:04}-{month:02}"
        for year in range(start_year, end_year + 1) for month in range(1, 13)
    ]
    return {
        "analysis_version": "historic-station-monthly-bounds-v1",
        "source": {
            "url": source_url, "retrieved_on": retrieved_on,
            "sha256": digest, "bytes": len(raw),
            "station": lines[0], "location": lines[1],
        },
        "window": {
            "start": expected[0], "end": expected[-1],
            "expected_months": len(expected), "present_months": len(selected),
            "absent_months": [key for key in expected if key not in selected],
            "calendar_complete": len(selected) == len(expected),
            "outside_window_rows": outside,
        },
        "quality_policy": "Exclude provisional rows, then missing, then estimated "
                          "values per field; categories are mutually exclusive.",
        "temperature": {
            "tmax": _summary(samples["tmax"], counts["tmax"],
                             "Monthly average of daily maximum air temperature"),
            "tmin": _summary(samples["tmin"], counts["tmin"],
                             "Monthly average of daily minimum air temperature"),
            "midpoint": _summary(samples["midpoint"], {
                "valid": len(samples["midpoint"]),
                "excluded": len(selected) - len(samples["midpoint"]),
            }, "Arithmetic (tmax+tmin)/2, same-month accepted pairs only"),
        },
        "humidity": {
            "status": "unavailable",
            "reason": "No relative humidity field in this source; not inferred",
        },
        "interpretation": "Monthly sample statistics, not instantaneous extremes, "
                          "region-wide bounds, replay limits or safety thresholds.",
        "owner_reuse_approval": "UNMET",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--retrieved-on", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    args = parser.parse_args()
    try:
        report = analyze(
            args.input.read_bytes(), source_url=args.source_url,
            retrieved_on=args.retrieved_on, expected_sha256=args.expected_sha256,
            start_year=args.start_year, end_year=args.end_year,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
