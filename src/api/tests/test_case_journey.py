"""Case journey semantics execute the shipped JavaScript, not a Python copy."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.insights import STAGE_ORDER

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


def evaluate(expression: str) -> Any:
    source = (WEB / "case-workspace.js").read_text()
    result = subprocess.run(
        ["node", "-e", source + f"\nconsole.log(JSON.stringify({expression}));"],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def journey(**overrides: Any) -> list[dict[str, Any]]:
    case = dict(
        stage="Works under way",
        closed=False,
        work={"blockers": []},
        funding={"status": "Confirmed"},
        decision={"status": "Accepted"},
    )
    case.update(overrides)
    return list(evaluate(f"CaseWorkspace.journey({json.dumps(case)})"))


class CaseJourney(unittest.TestCase):
    def test_all_stages_mapped_once_in_shipped_module(self) -> None:
        stages = evaluate("CaseWorkspace.steps.flatMap(step => step.stages)")
        self.assertEqual(len(stages), len(set(stages)))
        self.assertEqual(set(stages), set(STAGE_ORDER))
        for stage in STAGE_ORDER:
            with self.subTest(stage=stage):
                current = [step for step in journey(stage=stage) if step["current"]]
                self.assertEqual(len(current), 1)

    def test_fixed_slide_order_and_evidence_exceptions(self) -> None:
        states = journey(funding={"status": "Submitted"}, decision={"status": "Asked"})
        self.assertEqual(
            [step["name"] for step in states],
            [
                "Survey",
                "Assessment",
                "Funding",
                "Resident agreement",
                "Contractor",
                "Quality and handover",
            ],
        )
        for index in (2, 3):
            self.assertEqual(states[index]["state"], "upcoming")
            self.assertEqual(states[index]["text"], "Earlier step not confirmed")
        self.assertEqual(journey()[2]["state"], "done")
        self.assertEqual(journey()[3]["state"], "done")
        self.assertNotEqual(
            journey(stage="Waiting for resident decision", funding={"status": "Draft ready"})[2][
                "state"
            ],
            "done",
        )

    def test_blocker_mapping_current_and_unknown(self) -> None:
        for label, index in (
            ("Final checks: funding", 2),
            ("Final checks: resident decision", 3),
            ("Final checks: technical review", 1),
            ("Stock review", 1),
            ("Safety review", 4),
            ("Shared building review", 4),
            ("Unknown blocker", 4),
        ):
            with self.subTest(label=label):
                states = journey(work={"blockers": [{"step": label, "reason": "Check evidence"}]})
                self.assertEqual(states[index]["state"], "blocked")
                self.assertIn("Check evidence", states[index]["text"])
                self.assertEqual(sum(bool(step["current"]) for step in states), 1)
                self.assertTrue(states[4]["current"])
                self.assertNotEqual(states[0]["state"], "blocked")

    def test_closed_overrides_blockers_unknown_stage_does_not_invent_step(self) -> None:
        states = journey(
            closed=True, work={"blockers": [{"step": "Safety review", "reason": "Check"}]}
        )
        self.assertTrue(all(step["state"] == "done" for step in states))
        self.assertFalse(any(step["current"] for step in states))
        self.assertFalse(any(step["current"] for step in journey(stage="Unknown")))

    def test_summary_empty_values_handoff_and_overdue(self) -> None:
        empty = evaluate("CaseWorkspace.summary({work: {}})")
        self.assertEqual(empty["owner"], "Unknown")
        self.assertEqual(empty["blockers"], "No recorded blockers.")
        self.assertEqual(empty["step"], "Step unknown")
        case = {
            "owner": "Sam",
            "owner_role": "Officer",
            "handoff": {"state": "Received", "proposed_receiver": "Pam"},
            "work": {
                "next_action": "Check the evidence.",
                "blockers": [
                    {"reason": "Missing source.", "owner": "Unknown", "next_action": "Ask Sam."}
                ],
                "overdue": [{"task": "Call"}],
            },
        }
        summary = evaluate(f"CaseWorkspace.summary({json.dumps(case)})")
        self.assertIn("Offered to Pam, not yet confirmed", summary["owner"])
        self.assertIn("Owner: Unknown. Next action: Ask Sam.", summary["blockers"])
        self.assertEqual(summary["overdue"], 1)

    def test_reviewable_count_states(self) -> None:
        for state, output, stale, expected in (
            ("ready", {}, False, True),
            ("ready", {}, True, False),
            ("queued", None, False, False),
            ("running", None, False, False),
            ("failed", None, False, False),
            ("accepted", {}, False, False),
            ("rejected", {}, False, False),
        ):
            proposal: dict[str, Any] = {"state": state, "output": output, "stale": stale}
            self.assertEqual(evaluate(f"CaseWorkspace.waiting({json.dumps(proposal)})"), expected)

    def test_summary_jump_targets_record_actions(self) -> None:
        for case, expected in (
            ({"stage": "Contacting resident", "work": {}}, "resident"),
            ({"stage": "Final checks before ordering", "can_advance": True}, "overview"),
            ({"work": {"source": "case:ZF-1/handoff"}}, "quality"),
            ({"work": {"blockers": [{"current_stop": True}]}}, "blockers"),
        ):
            self.assertEqual(evaluate(f"CaseWorkspace.nextTab({json.dumps(case)})"), expected)

    def test_panels_mounted_once_and_tab_only_navigation_precedes_guard(self) -> None:
        app = (WEB / "app.js").read_text()
        case = app.split("async function caseView(id) {", 1)[1].split(
            "async function buildingView", 1
        )[0]
        for panel in (
            "workSteps",
            "safetyPanel",
            "regulatoryAlertsPanel",
            "returnPanel",
            "stockPanel",
            "technicalPanel",
            "documentsPanel",
            "fundingPanel",
            "financePanel",
            "grantPanel",
            "residentPanel",
            "affectedChallengePanel",
            "qualityPanel",
            "handoffPanel",
            "assistantCasePanel",
            "chatCasePanel",
        ):
            self.assertEqual(case.count(panel + "("), 1, panel)
        route = app.split("async function route() {", 1)[1]
        self.assertLess(route.index("controller.select"), route.index("window.confirm"))
        self.assertIn('draftBox: h("div", { id: "resident-draft-output" })', app)
        self.assertIn('data-case-dirty="true"', app)


if __name__ == "__main__":
    unittest.main()
