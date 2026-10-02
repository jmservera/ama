"""Tests for the deterministic rubric gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate  # noqa: E402

RUBRIC_DIR = Path(__file__).resolve().parent.parent
RUBRIC = json.loads((RUBRIC_DIR / "rubric.json").read_text(encoding="utf-8"))
SEED = json.loads((RUBRIC_DIR / "scores" / "latest.json").read_text(encoding="utf-8"))
IDS = [criterion["id"] for criterion in RUBRIC["criteria"]]
BRD = "docs/brds/agentic-retrofit-programme-brd.md"


def workflow_baseline() -> dict:
    baseline = json.loads(json.dumps(SEED))
    baseline["source"] = "workflow"
    return baseline


def scorecard_items(scores: dict[str, int], evidence: list[str] | None = None) -> list[dict]:
    criteria = {cid: {"score": score, "evidence": evidence or [], "rationale": "r"} for cid, score in scores.items()}
    return [{"type": gate.TOOL_TYPE, "scorecard": json.dumps({"criteria": criteria, "summary": "s"})}]


def seed_scores() -> dict[str, int]:
    return {cid: entry["score"] for cid, entry in SEED["criteria"].items()}


def run(baseline: dict, items: list[dict], *, bootstrap: bool = False, open_criteria=None, changed=None, removed=None, agent="success", detection="success", calibration=False) -> dict:
    removed = removed or []
    changed = (changed or []) + removed
    return gate.evaluate(RUBRIC, baseline, bootstrap, IDS if open_criteria is None else open_criteria, changed, items, agent, detection, removed, calibration)


def test_given_seed_baseline_when_summed_then_total_is_61():
    # Arrange
    scores = seed_scores()

    # Act
    total = sum(scores.values())

    # Assert
    assert total == SEED["total"] == 61


def test_given_equal_scores_when_evaluated_then_passes():
    # Arrange
    items = scorecard_items(seed_scores())

    # Act
    result = run(workflow_baseline(), items)

    # Assert
    assert (result["passed"], result["total"]) == (True, 61)


def test_given_supported_drop_when_evaluated_then_fails_with_warning():
    # Arrange
    scores = seed_scores() | {"A2": 4}
    items = scorecard_items(scores, [f"{BRD}:312"])

    # Act
    result = run(workflow_baseline(), items, changed=[BRD])

    # Assert
    assert (result["passed"], result["total"], result["drops"]) == (False, 60, ["A2"])


def test_given_change_without_changed_evidence_when_evaluated_then_baseline_kept():
    # Arrange
    items = scorecard_items(seed_scores() | {"A2": 4}, ["docs/other.md:1"])

    # Act
    result = run(workflow_baseline(), items, changed=[BRD])

    # Assert
    assert (result["passed"], result["criteria"]["A2"]["score"]) == (True, 5)


def test_given_closed_criterion_when_agent_changes_it_then_carried_forward():
    # Arrange
    items = scorecard_items(seed_scores() | {"B3": 5}, [f"{BRD}:1"])

    # Act
    result = run(workflow_baseline(), items, open_criteria=["A1"], changed=[BRD])

    # Assert
    assert result["criteria"]["B3"]["score"] == 1


def test_given_bootstrap_when_score_is_lower_then_passes():
    # Arrange
    items = scorecard_items({cid: 2 for cid in IDS})

    # Act
    result = run(SEED, items, bootstrap=True)

    # Assert
    assert (result["passed"], result["total"]) == (True, 40)


def test_given_drop_citing_removed_file_when_evaluated_then_fails():
    # Arrange
    items = scorecard_items(seed_scores() | {"A2": 3}, [f"{BRD}:312"])

    # Act
    result = run(workflow_baseline(), items, removed=[BRD])

    # Assert
    assert (result["passed"], result["total"]) == (False, 59)


def test_given_increase_citing_removed_file_when_evaluated_then_baseline_kept():
    # Arrange
    items = scorecard_items(seed_scores() | {"A4": 3}, [f"{BRD}:1"])

    # Act
    result = run(workflow_baseline(), items, removed=[BRD])

    # Assert
    assert result["criteria"]["A4"]["score"] == 1


def test_given_calibration_when_score_is_lower_then_reported_without_failing():
    # Arrange
    items = scorecard_items({cid: 2 for cid in IDS})

    # Act
    result = run(workflow_baseline(), items, calibration=True)

    # Assert
    assert (result["passed"], result["calibration"], result["total"]) == (True, True, 40)


@pytest.mark.parametrize(
    ("items", "agent", "detection"),
    [
        ([], "success", "success"),
        (scorecard_items(seed_scores()) * 2, "success", "success"),
        ([{"type": gate.TOOL_TYPE, "scorecard": "not json"}], "success", "success"),
        (scorecard_items(seed_scores() | {"A1": 6}), "success", "success"),
        (scorecard_items(seed_scores()), "failure", "success"),
        (scorecard_items(seed_scores()), "success", "failure"),
    ],
)
def test_given_invalid_run_when_evaluated_then_fails_closed(items, agent, detection):
    # Act
    result = run(workflow_baseline(), items, agent=agent, detection=detection)

    # Assert
    assert (result["valid"], result["passed"]) == (False, False)


def test_given_agent_text_with_markup_when_sanitized_then_neutralised():
    # Act
    value = gate.sanitize("@owner <script>|x")

    # Assert
    assert "<" not in value and "@owner" not in value and "\\|" in value


def test_given_links_and_references_when_cleaned_twice_then_neutralised_and_stable():
    # Arrange
    text = "see [x](https://evil.example) ![i](u) @owner #12 www.evil.example GH-7 deadbeef1234\x07"

    # Act
    once = gate.clean_text(text)

    # Assert
    assert (
        "](" not in once,
        "![" not in once,
        "://" not in once,
        "www." not in once,
        "GH-7" not in once,
        "deadbeef1234" not in once,
        "\x07" not in once,
        gate.clean_text(once),
    ) == (True, True, True, True, True, True, True, once)


@pytest.mark.parametrize(
    "reference",
    [
        f"{BRD}:12",
        f"{BRD}:L12-L20",
        f"{BRD}#L12",
        f"./{BRD}",
        f"/{BRD}",
        BRD.replace("/", "\\") + ":3",
    ],
)
def test_given_evidence_reference_variant_when_normalised_then_repository_path(reference):
    # Act
    path = gate.evidence_path(reference)

    # Assert
    assert path == BRD
