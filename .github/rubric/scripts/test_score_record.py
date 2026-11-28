"""Integrity tests for the committed rubric score record (issue 198)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

RUBRIC_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = RUBRIC_DIR.parent.parent
RETIRED_ROOTS = ("mvp/", "prototype/", "prototypes/")
LOCATION_SUFFIX = re.compile(r":(?:\d|L\d|slide).*$")


def load(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((RUBRIC_DIR / name).read_text(encoding="utf-8"))
    return data


def evidence_paths(record: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        (cid, LOCATION_SUFFIX.sub("", str(cite)))
        for cid, entry in record["criteria"].items()
        for cite in entry["evidence"]
    ]


def test_given_score_record_when_summed_then_totals_match_criteria_and_sections() -> None:
    record = load("scores/latest.json")
    rubric = load("rubric.json")
    section_of = {c["id"]: c["section"] for c in rubric["criteria"]}
    sums: dict[str, int] = {}
    for cid, entry in record["criteria"].items():
        sums[section_of[cid]] = sums.get(section_of[cid], 0) + int(entry["score"])
    assert sums == record["sections"]
    assert sum(sums.values()) == record["total"]


def test_given_rubric_when_compared_then_every_criterion_has_a_recorded_score() -> None:
    record = load("scores/latest.json")
    rubric = load("rubric.json")
    assert {c["id"] for c in rubric["criteria"]} == set(record["criteria"])


def test_given_recorded_evidence_when_resolved_then_files_exist_outside_retired_roots() -> None:
    record = load("scores/latest.json")
    paths = evidence_paths(record)
    assert paths
    assert [(c, p) for c, p in paths if p.startswith(RETIRED_ROOTS)] == []
    assert [(c, p) for c, p in paths if not (REPO_ROOT / p).exists()] == []
