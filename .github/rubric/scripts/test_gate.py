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


def test_given_seed_baseline_when_summed_then_total_is_66():
    # Arrange
    scores = seed_scores()

    # Act
    total = sum(scores.values())

    # Assert
    assert total == SEED["total"] == 66


def test_given_equal_scores_when_evaluated_then_passes():
    # Arrange
    items = scorecard_items(seed_scores())

    # Act
    result = run(workflow_baseline(), items)

    # Assert
    assert (result["passed"], result["total"]) == (True, 66)


def test_given_unknown_criterion_when_evaluated_then_fails_with_actionable_error():
    # Arrange
    criteria = seed_scores()
    criteria["A1_unused"] = None
    items = scorecard_items(criteria)

    # Act
    result = run(workflow_baseline(), items)

    # Assert
    assert result["valid"] is False
    assert result["error"] == "unknown criteria: A1_unused"


def test_given_missing_criterion_when_evaluated_then_fails_with_actionable_error():
    criteria = seed_scores()
    del criteria["A2"]

    result = run(workflow_baseline(), scorecard_items(criteria))

    assert result["valid"] is False
    assert result["error"] == "criterion A2 is missing"


def test_given_unscored_template_placeholder_when_evaluated_then_fails_closed():
    criteria = seed_scores()
    criteria["A2"] = None
    items = [{"type": gate.TOOL_TYPE, "scorecard": json.dumps({"criteria": {
        **{cid: {"score": score, "evidence": [], "rationale": "r"} for cid, score in criteria.items() if score is not None},
        "A2": {"score": None, "evidence": [], "rationale": "UNSCORED"},
    }})}]

    result = run(workflow_baseline(), items)

    assert result["valid"] is False
    assert result["error"] == "criterion A2 score must be an integer from 1 to 5"


def test_given_supported_drop_when_evaluated_then_fails_with_warning():
    # Arrange
    scores = seed_scores() | {"A2": 4}
    items = scorecard_items(scores, [f"{BRD}:312"])

    # Act
    result = run(workflow_baseline(), items, changed=[BRD])

    # Assert
    assert (result["passed"], result["total"], result["drops"]) == (False, 65, ["A2"])


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
    assert (result["passed"], result["total"]) == (False, 64)


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


@pytest.mark.parametrize("slide", [1, 5, 7, 14, 17])
def test_given_pptx_slide_reference_when_normalised_then_repository_path(slide):
    deck = "docs/capstone/deck/proper-warm-executive-draft.pptx"

    assert gate.evidence_path(f"{deck}:slide{slide}") == deck


def test_given_changed_deck_with_slide_citations_when_scored_then_deck_scores_are_recorded():
    deck = "docs/capstone/deck/proper-warm-executive-draft.pptx"
    baseline = workflow_baseline()
    for cid in ("B1", "B2", "B7"):
        baseline["criteria"][cid]["score"] = 0
    baseline["criteria"]["B6"]["score"] = 3
    baseline["total"] = sum(entry["score"] for entry in baseline["criteria"].values())
    scores = {cid: entry["score"] or 1 for cid, entry in baseline["criteria"].items()}
    scores.update({"B1": 4, "B2": 3, "B6": 4, "B7": 4})
    items = scorecard_items(scores, [f"{deck}:slide1", f"{deck}:slide17"])
    counts = {"capstone-deck": 1, "pitch": 0, "thought-leadership": 0}

    result = gate.evaluate(
        RUBRIC, baseline, False, ["B1", "B2", "B6", "B7"], [deck],
        items, "success", "success", artifact_counts=counts,
    )

    assert {cid: result["criteria"][cid]["score"] for cid in ("B1", "B2", "B6", "B7")} == {
        "B1": 4, "B2": 3, "B6": 4, "B7": 4,
    }
    assert not any("evidence cites no changed file" in warning for warning in result["warnings"])
    assert result["criteria"]["B3"]["score"] == 0
    assert result["criteria"]["D1"]["score"] == 0


@pytest.mark.parametrize(
    "reference",
    [
        f"{BRD}:slide1",
        "docs/capstone/deck/a.pptx:slide0",
        "docs/capstone/deck/a.pptx:slide-1",
        "docs/capstone/deck/a.pptx:slideone",
        "docs/capstone/deck/a.pptx:slide1-extra",
    ],
)
def test_given_unsupported_slide_anchor_when_normalised_then_not_accepted_as_file(reference):
    assert gate.evidence_path(reference) == reference


def test_given_unchanged_deck_slide_citation_when_scored_then_increase_is_rejected():
    deck = "docs/capstone/deck/proper-warm-executive-draft.pptx"
    baseline = workflow_baseline()
    baseline["criteria"]["B1"]["score"] = 2
    scores = {cid: entry["score"] or 1 for cid, entry in baseline["criteria"].items()}

    result = run(
        baseline, scorecard_items(scores | {"B1": 4}, [f"{deck}:slide1"]),
        open_criteria=["B1"], changed=[BRD],
    )

    assert result["criteria"]["B1"]["score"] == 2
    assert "B1: change ignored, evidence cites no changed file" in result["warnings"]


def test_given_no_pitch_or_thought_leadership_when_scored_then_gate_forces_zero():
    # Arrange
    scores = {cid: 4 for cid in IDS}
    counts = {"brd": 1, "prd": 1, "capstone-deck": 0, "pitch": 0, "thought-leadership": 0}

    # Act
    result = gate.evaluate(RUBRIC, None, True, IDS, [], scorecard_items(scores), "success", "success", [], False, counts)

    # Assert
    zeroed = {cid for cid, entry in result["criteria"].items() if entry["score"] == 0}
    assert zeroed == {"B1", "B2", "B3", "B4", "B5", "B7", "C2", "C3", "D1", "D2", "D3"}
    assert result["criteria"]["B6"]["score"] == 3
    assert result["sections"]["D"] == 0
    assert result["floors_met"] is False
    assert result["outcome"] == RUBRIC["submission_required"]["outcome"]


def test_given_deck_only_when_scored_then_pitch_criteria_stay_zero_and_deck_criteria_count():
    # Arrange
    scores = {cid: 4 for cid in IDS}
    counts = {"brd": 1, "capstone-deck": 1, "pitch": 0, "thought-leadership": 1}

    # Act
    result = gate.evaluate(RUBRIC, None, True, IDS, [], scorecard_items(scores), "success", "success", [], False, counts)

    # Assert
    assert [cid for cid in ("B1", "B2", "B3", "B4", "B5", "B7", "C2", "C3") if result["criteria"][cid]["score"] == 0] == ["B3", "B4", "B5", "C2", "C3"]
    assert result["criteria"]["B6"]["score"] == 4
    assert result["sections"]["D"] == 12


def test_given_scores_when_badge_rendered_then_svg_shows_total_and_escapes_text():
    # Arrange
    scores = {"total": 34, "outcome": "Not Yet Met (floor) <x>"}

    # Act
    svg = gate.render_badge(scores)

    # Assert
    assert svg.startswith("<svg") and ">34/100<" in svg and "<x>" not in svg and "#e05d44" in svg
