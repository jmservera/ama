"""Issue #76: hazard and safeguarding items show a clock and an accountable owner."""

import copy
import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import ranking, taskqueues

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

CASE: dict[str, Any] = dict(
    id="ZF-76",
    stage="Contacting resident",
    stage_since="2026-10-01",
    owner="Sam Example",
    funding_ok=True,
    closed=False,
    hazards=[],
)


def clocks(*hazards: dict[str, Any]) -> list[dict[str, Any]]:
    case = copy.deepcopy(CASE)
    case["hazards"] = list(hazards)
    work = taskqueues.context(
        case,
        as_of="2026-10-16T12:00:00Z",
        reason_ok=True,
        policy=ranking.CURRENT,
        stock_queries=[],
        building_reasons=[],
        resident_reasons=[],
        technical_missing=[],
        handoff=None,
    )
    return list(work["hazard_clocks"])


def render(work: dict[str, Any]) -> str:
    script = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const app = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const work = JSON.parse(process.argv[2]);
const h = (tag, attrs, ...kids) => ({kids: kids.flat(Infinity).filter(k => k)});
const text = (n) => typeof n === "object" ? n.kids.map(text).join(" ") : String(n);
const ctx = vm.createContext({h});
vm.runInContext(app.slice(app.indexOf("function workSummary("),
  app.indexOf("function workSteps(")), ctx);
console.log(text(vm.runInContext("workSummary", ctx)(work)));
"""
    done = subprocess.run(
        ["node", "-e", script, str(WEB), json.dumps(work)],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return done.stdout


def work_for(items: list[dict[str, Any]]) -> dict[str, Any]:
    return dict(
        owner="Case owner",
        reason="r",
        next_action="n",
        source="s",
        evidence="e",
        version=1,
        recorded_at="x",
        as_of="y",
        handoff=None,
        hazard_clocks=items,
    )


class HazardClockOwner(unittest.TestCase):
    def test_named_hazard_shows_elapsed_clock_window_and_owner_in_text(self) -> None:
        (clock,) = clocks(
            dict(
                category="Damp",
                aware_at="2026-10-15T12:00:00Z",
                response_due_at="2026-10-17T12:00:00Z",
                owner="Bea Safe",
            )
        )
        self.assertEqual(clock["accountable_owner"], "Bea Safe")
        self.assertIn("Hazard clock: 24 hours elapsed", clock["clock_text"])
        self.assertIn("service response due 2026-10-17T12:00:00Z", clock["clock_text"])
        shown = render(work_for([clock]))
        self.assertIn("Accountable owner: Bea Safe", shown)
        self.assertIn("24 hours elapsed", shown)

    def test_safeguarding_item_is_labelled_and_never_anonymous(self) -> None:
        (clock,) = clocks(dict(category="Safeguarding concern", aware_at="2026-10-16T00:00:00Z"))
        self.assertEqual(clock["kind"], "Safeguarding")
        self.assertEqual(clock["accountable_owner"], taskqueues.ESCALATION_OWNER)
        self.assertIn("no response target window recorded", clock["clock_text"])
        shown = render(work_for([clock]))
        self.assertIn("Safeguarding clock: 12 hours elapsed", shown)
        self.assertIn(f"Accountable owner: {taskqueues.ESCALATION_OWNER}", shown)

    def test_unknown_awareness_is_stated_and_owner_falls_back_to_escalation(self) -> None:
        (clock,) = clocks(dict(category="Mould", response_due_at="2026-10-10"))
        self.assertIsNone(clock["elapsed_hours"])
        self.assertIn("elapsed time unknown", clock["clock_text"])
        self.assertIn("response overdue", clock["clock_text"])
        self.assertNotIn(clock["accountable_owner"], ("", "Unknown", None))

    def test_every_open_item_gets_its_own_clock_and_owner(self) -> None:
        items = clocks(
            dict(category="Damp", owner="Bea Safe", aware_at="2026-10-16T00:00:00Z"),
            dict(category="Safeguarding", aware_at="2026-10-16T06:00:00Z"),
        )
        self.assertEqual([c["kind"] for c in items], ["Hazard", "Safeguarding"])
        for item in items:
            self.assertTrue(item["clock_text"])
            self.assertTrue(item["accountable_owner"])

    def test_queue_clock_shows_time_remaining_overdue_or_missing_awareness(self) -> None:
        running, overdue, missing = clocks(
            dict(
                category="Damp",
                priority="Emergency",
                aware_at="2026-10-16T06:00:00Z",
                owner="Bea Safe",
            ),
            dict(
                category="Mould",
                priority="Significant",
                aware_at="2026-10-01T00:00:00Z",
                owner="Bea Safe",
            ),
            dict(category="Mould", priority="Significant", noticed="2025-12-21", owner="Bea Safe"),
        )
        self.assertEqual(running["clock_status"], "running")
        self.assertEqual(overdue["clock_status"], "overdue")
        self.assertEqual(missing["clock_status"], "fail_closed_missing_timestamp")
        self.assertIn("18 hours remaining until the target", render(work_for([running])))
        shown = render(work_for([overdue]))
        self.assertIn("Overdue by 204 hours", shown)
        self.assertNotIn("-204", shown)
        shown = render(work_for([missing]))
        self.assertIn("Time remaining unknown", shown)
        self.assertIn("Next action: record it", shown)
        self.assertIn("Accountable owner: Bea Safe", shown)

    def test_safeguarding_queue_clock_has_target_and_owner(self) -> None:
        case = copy.deepcopy(CASE)
        case["safeguarding_items"] = [
            dict(
                category="Safeguarding",
                priority="Significant",
                referred_at="2026-10-14T09:00:00Z",
                response_due_at="2026-10-17T09:00:00Z",
                owner=dict(name="Sam Lead", role="Safeguarding lead"),
            )
        ]
        work = taskqueues.context(
            case,
            as_of="2026-10-16T12:00:00Z",
            reason_ok=True,
            policy=ranking.CURRENT,
            stock_queries=[],
            building_reasons=[],
            resident_reasons=[],
            technical_missing=[],
            handoff=None,
        )
        (clock,) = work["safeguarding_clocks"]
        self.assertEqual(clock["clock_status"], "running")
        self.assertEqual(clock["clock_remaining_hours"], 21.0)
        self.assertEqual(clock["owner"], "Sam Lead")
        self.assertIn("21 hours remaining", render(dict(work, hazard_clocks=[])))

    def test_safeguarding_label_is_redacted_without_reason_visibility(self) -> None:
        case = copy.deepcopy(CASE)
        case["hazards"] = [
            dict(category="Safeguarding", priority="Routine", aware_at="2026-10-16T00:00:00Z")
        ]
        work = taskqueues.context(
            case,
            as_of="2026-10-16T12:00:00Z",
            reason_ok=False,
            policy=ranking.CURRENT,
            stock_queries=[],
            building_reasons=[],
            resident_reasons=[],
            technical_missing=[],
            handoff=None,
        )
        (clock,) = work["hazard_clocks"]
        self.assertEqual(clock["clock_label"], "Safety review clock")
        self.assertNotIn("afeguard", json.dumps(clock))

    def test_ui_falls_back_when_owner_missing_from_payload(self) -> None:
        shown = render(work_for([dict(owner="Unknown", elapsed_hours=None)]))
        self.assertIn("Accountable owner: Building Safety lead (escalation owner)", shown)


if __name__ == "__main__":
    unittest.main()
