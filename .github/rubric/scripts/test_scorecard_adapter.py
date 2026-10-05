"""Strict adapter tests, including canonical gate and scaffold boundaries."""

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate
import prepare
import scorecard_adapter as adapter

ROOT = Path(__file__).resolve().parent.parent
RUBRIC = json.loads((ROOT / "rubric.json").read_text(encoding="utf-8"))
BASELINE = json.loads((ROOT / "scores/latest.json").read_text(encoding="utf-8"))
IDS = [criterion["id"] for criterion in RUBRIC["criteria"]]


def card():
    result = prepare.build_scorecard_template(RUBRIC, BASELINE, False, False)
    for cid in IDS:
        result["criteria"][cid]["change_reason"] = f"Reason for {cid}"
    result["summary"] = "Exact summary"
    return result


def test_complete_card_round_trips_without_mutating_baseline():
    before = copy.deepcopy(BASELINE)
    canonical = card()
    inputs = adapter.to_inputs(canonical, IDS)
    assert set(inputs) == {f"{cid}_score" for cid in IDS} | {"details", "summary"}
    assert adapter.from_inputs(inputs, IDS) == canonical
    parsed, error = gate.parse_scorecard([{"type": gate.TOOL_TYPE, **inputs}], IDS)
    assert error is None
    assert parsed == canonical
    assert BASELINE == before


@pytest.mark.parametrize("mutation", ["missing", "extra", "number", "boolean", "null", "range", "coercion", "details-type", "summary-type"])
def test_malformed_inputs_fail_explicitly(mutation):
    inputs = adapter.to_inputs(card(), IDS)
    if mutation == "missing":
        del inputs["A2_score"]
    elif mutation == "extra":
        inputs["A8_score"] = "3"
    else:
        key, value = {
            "number": ("A2_score", 3),
            "boolean": ("A2_score", True),
            "null": ("A2_score", None),
            "range": ("A2_score", "6"),
            "coercion": ("A2_score", " 3"),
            "details-type": ("details", {}),
            "summary-type": ("summary", None),
        }[mutation]
        inputs[key] = value
    with pytest.raises(ValueError):
        adapter.from_inputs(inputs, IDS)
    parsed, error = gate.parse_scorecard([{"type": gate.TOOL_TYPE, **inputs}], IDS)
    assert parsed is None and error


@pytest.mark.parametrize("mutation", [
    "invalid-json", "array", "missing-id", "extra-id", "entry-type",
    "missing-field", "extra-field", "evidence-object", "evidence-number",
    "rationale-number", "reason-null", "duplicate-id", "duplicate-field",
])
def test_malformed_details_fail_without_defaults(mutation):
    inputs = adapter.to_inputs(card(), IDS)
    details = json.loads(inputs["details"])
    if mutation == "invalid-json":
        raw = "{"
    elif mutation == "array":
        raw = "[]"
    elif mutation == "duplicate-id":
        raw = inputs["details"][:-1] + ', "A2": {}}'
    elif mutation == "duplicate-field":
        raw = inputs["details"].replace('"evidence":', '"evidence": [], "evidence":', 1)
    else:
        if mutation == "missing-id":
            del details["A2"]
        elif mutation == "extra-id":
            details["A8"] = details["A2"]
        elif mutation == "entry-type":
            details["A2"] = None
        elif mutation == "missing-field":
            del details["A2"]["change_reason"]
        elif mutation == "extra-field":
            details["A2"]["score"] = 3
        else:
            field, value = {
                "evidence-object": ("evidence", {}),
                "evidence-number": ("evidence", [1]),
                "rationale-number": ("rationale", 42),
                "reason-null": ("change_reason", None),
            }[mutation]
            details["A2"][field] = value
        raw = json.dumps(details)
    inputs["details"] = raw
    with pytest.raises(ValueError):
        adapter.from_inputs(inputs, IDS)


@pytest.mark.parametrize(("bootstrap", "calibration"), [(True, False), (False, True)])
def test_unscored_scaffold_is_not_a_submittable_grade(bootstrap, calibration):
    canonical = prepare.build_scorecard_template(RUBRIC, BASELINE, bootstrap, calibration)
    inputs = adapter.to_inputs(canonical, IDS)
    assert all(inputs[f"{cid}_score"] is None for cid in IDS)
    assert all("UNSCORED" in detail["rationale"] for detail in json.loads(inputs["details"]).values())
    with pytest.raises(ValueError):
        adapter.from_inputs(inputs, IDS)


def test_gate_incremental_carry_forward_and_calibration_leave_baseline_unchanged():
    before = copy.deepcopy(BASELINE)
    canonical = card()
    canonical["criteria"]["B1"]["score"] = 5
    items = [{"type": gate.TOOL_TYPE, **adapter.to_inputs(canonical, IDS)}]
    incremental = gate.evaluate(RUBRIC, BASELINE, False, ["A1"], [], items, "success", "success")
    assert incremental["valid"]
    assert incremental["criteria"]["B1"] == BASELINE["criteria"]["B1"]
    calibration = gate.evaluate(RUBRIC, BASELINE, False, IDS, [], items, "success", "success", calibration=True)
    assert calibration["valid"] and calibration["calibration"]
    assert calibration["criteria"]["B1"]["score"] == 5
    assert BASELINE == before


@pytest.mark.parametrize(("bootstrap", "calibration"), [(False, False), (True, False), (False, True)])
def test_written_context_has_complete_tool_template_and_withholds_unscored_baseline(tmp_path, bootstrap, calibration):
    state = {
        "artifacts": {}, "removed_files": [], "changed_files": [], "diff_args": [],
        "force": calibration, "bootstrap": bootstrap, "baseline": BASELINE,
        "rubric": RUBRIC, "event": "workflow_dispatch", "instrument_changed": False,
        "reasons": [], "open_criteria": IDS, "changed_artifacts": [],
    }
    context = json.loads(prepare.write_context(tmp_path, state, tmp_path / "context").read_text())
    template = context["tool_inputs_template"]
    assert set(template) == {f"{cid}_score" for cid in IDS} | {"details", "summary"}
    if bootstrap or calibration:
        assert context["baseline"]["criteria"] == {}
        assert all(template[f"{cid}_score"] is None for cid in IDS)
    else:
        assert adapter.from_inputs(template, IDS) == context["scorecard_template"]


def test_adapter_is_a_scoring_instrument():
    assert ".github/rubric/scripts/scorecard_adapter.py" in prepare.INSTRUMENT_PATHS


def test_prompt_example_is_complete_and_accepted_by_adapter():
    workflow = (ROOT.parent / "workflows/rubric-score.md").read_text(encoding="utf-8")
    example = workflow.split("```json\n", 1)[1].split("```", 1)[0]
    parsed = adapter.from_inputs(json.loads(example), IDS)
    assert list(parsed["criteria"]) == IDS
