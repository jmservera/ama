"""Run only constructed local evaluation data. Requires the documented absolute test paths."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from pathlib import Path
from typing import Any, NoReturn

from regulatory_fixture import NOW

from regulatory_gate_fixture import run
from zava_forward.agents.paired_trial import (
    BOOLS,
    SECONDS,
    evaluate_paired_trial,
    valid_observation,
)

OPTION = "--constructed-paired-observations"
SCHEMA = "constructed-paired-observations-v1"
MAX_BYTES = 256 * 1024
MAX_OBSERVATIONS = 1000
MAX_SECONDS = 365 * 24 * 3600
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
ENVELOPE_KEYS = {"schema", "observations"}
OBSERVATION_KEYS = {"participant", "task", "role", "arm", *BOOLS, *SECONDS}
QUALIFICATION = (
    "This section holds caller-declared constructed observations. Independent human "
    "participation, synthetic origin, pseudonymity and the supplied accepted flags are "
    "unverified. It is not a staff trial, not human acceptance and not owner-agreed, no "
    "threshold, price, budget or authority was supplied, and it is not merged with any other "
    "dataset or with the structural comparison and not_evaluated staff checks."
)


def refuse(message: str) -> NoReturn:
    raise SystemExit(f"{OPTION}: {message}")


def _non_finite(constant: str) -> NoReturn:
    refuse(f"non-finite number {constant} is not allowed")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    if len({key for key, _ in pairs}) != len(pairs):
        refuse("duplicate key in a JSON object")
    return dict(pairs)


def _read_bounded(path: Path) -> bytes:
    try:
        mode = path.stat().st_mode
    except OSError as error:
        refuse(f"cannot read {path}: {error.strerror}")
    if not stat.S_ISREG(mode):
        refuse(f"{path} must be a regular file")
    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError as error:
        refuse(f"cannot read {path}: {error.strerror}")
    if len(data) > MAX_BYTES:
        refuse(f"input is larger than {MAX_BYTES} bytes")
    return data


def _check_observation(index: int, row: Any) -> None:
    if not isinstance(row, dict):
        refuse(f"observation {index} must be an object")
    if set(row) != OBSERVATION_KEYS:
        refuse(f"observation {index} must have exactly the keys {sorted(OBSERVATION_KEYS)}")
    for key in ("participant", "task"):
        value = row[key]
        if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
            refuse(
                f"observation {index}: {key} must be a pseudonymous id "
                "(letters, digits, '.', '_' or '-', at most 64 characters)"
            )
    for key in SECONDS:
        value = row[key]
        if isinstance(value, int | float) and not isinstance(value, bool) and value > MAX_SECONDS:
            refuse(f"observation {index}: {key} exceeds {MAX_SECONDS} seconds")
    reason = valid_observation(row)
    if reason:
        refuse(f"observation {index}: {reason}")


def load_constructed_observations(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return validated observations and the input identity, or exit with the reason."""
    data = _read_bounded(path)
    try:
        document = json.loads(
            data.decode("utf-8"), parse_constant=_non_finite, object_pairs_hook=_no_duplicates
        )
    except UnicodeDecodeError:
        refuse("input is not valid UTF-8")
    except RecursionError:
        refuse("input is too deeply nested")
    except ValueError as error:
        refuse(f"input is not valid JSON: {error}")
    if not isinstance(document, dict):
        refuse("input must be a JSON object")
    if set(document) != ENVELOPE_KEYS:
        refuse(f"envelope must have exactly the keys {sorted(ENVELOPE_KEYS)}")
    if document["schema"] != SCHEMA:
        refuse(f"schema must be {SCHEMA}")
    rows = document["observations"]
    if not isinstance(rows, list):
        refuse("observations must be a list")
    if len(rows) > MAX_OBSERVATIONS:
        refuse(f"input has more than {MAX_OBSERVATIONS} observations")
    for index, row in enumerate(rows):
        _check_observation(index, row)
    info = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), observations=len(rows))
    return rows, info


def constructed_section(rows: list[dict[str, Any]], info: dict[str, Any]) -> dict[str, Any]:
    return dict(
        schema=SCHEMA,
        input=info,
        qualification=QUALIFICATION,
        result=evaluate_paired_trial(rows, thresholds=None, cost_inputs=None, now=NOW),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--homes", type=int, default=60000)
    parser.add_argument("--record", type=Path)
    parser.add_argument(
        OPTION,
        dest="constructed",
        type=Path,
        metavar="PATH",
        help=f"bounded local JSON of caller-declared constructed observations ({SCHEMA})",
    )
    args = parser.parse_args()
    constructed = (
        None if args.constructed is None else load_constructed_observations(args.constructed)
    )
    report = run(args.homes)
    if constructed is not None:
        report["constructed_paired_observations"] = constructed_section(*constructed)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.write_text(text)
    print(text, end="")
    # Exit status is process execution, not an aggregate evaluation verdict.
    # Each check and the cards-only recommendation remain in the report.


if __name__ == "__main__":
    main()
