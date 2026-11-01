"""Technical and quality reader screens block readiness on missing or stale evidence."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Quality Inspector"}},
  api: async () => ({total: 1, items: []}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__r = roleScreens;", context);
(async () => {
  const input = JSON.parse(process.argv[3]);
  const screen = context.__r.get(process.argv[2]);
  console.log(JSON.stringify({roles: screen.roles, tree: await screen.render(input)}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""


def render(screen: str, case: dict[str, Any]) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), screen, json.dumps(case)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


def signed(version: int, by: str = "Person") -> dict[str, Any]:
    return {"status": "Signed off", "version": version, "by": by, "history": []}


def tech_case(**changes: Any) -> dict[str, Any]:
    side = {
        "value": "D",
        "source_id": "S-A",
        "version": "1",
        "date": "2020-01-01",
        "validation_state": "Unvalidated",
    }
    case: dict[str, Any] = {
        "id": "C-1",
        "stock_reconciliation": [
            {
                "id": "SQ-1",
                "field": "epc",
                "left": side,
                "right": side,
                "query_owner": {"name": "Query Owner"},
            }
        ],
        "stock_reconciliation_events": [],
        "technical": {
            "design_version": 2,
            "design_name": "Designer",
            "versions": [{"note": "Changed"}],
            "signoffs": {
                k: signed(2) for k in ("assessment", "design", "building", "coordination")
            },
        },
        "technical_missing": [],
    }
    case.update(changes)
    return case


class TechnicalQueue(unittest.TestCase):
    def test_complete_evidence_shows_ready_text_and_no_controls(self) -> None:
        out = render("technical-queue", tech_case())
        text = json.dumps(out["tree"])
        self.assertIn("Recorded evidence is complete", text)
        self.assertIn("does not approve", text)
        self.assertIn("Signed off on design version 2", text)
        self.assertIn("S-A v1", text)
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(out["tree"]))
        self.assertIn("Quality Inspector", out["roles"])
        self.assertNotIn("Resident Liaison Officer", out["roles"])

    def test_reassessment_signoff_cannot_show_readiness(self) -> None:
        case = tech_case()
        case["technical"]["signoffs"]["building"] = {
            "status": "Needs reassessment",
            "reason": "Design changed",
            "history": [],
        }
        text = json.dumps(render("technical-queue", case)["tree"])
        self.assertNotIn("Recorded evidence is complete", text)
        self.assertIn("Cannot confirm readiness", text)

    def test_unaffected_older_signoffs_and_no_conflicts_stay_ready(self) -> None:
        case = tech_case(stock_reconciliation=[])
        case["technical"]["signoffs"]["assessment"] = signed(1)
        text = json.dumps(render("technical-queue", case)["tree"])
        self.assertIn("Recorded evidence is complete", text)
        self.assertIn("Signed off on design version 1", text)

    def test_missing_references_and_no_design_block(self) -> None:
        case = tech_case(
            technical_missing=[
                {"item": "Evidence: EPC", "assigned_to": "Grants and Evidence Officer"}
            ]
        )
        text = json.dumps(render("technical-queue", case)["tree"])
        self.assertNotIn("Recorded evidence is complete", text)
        self.assertIn("Evidence: EPC", text)
        self.assertIn("Grants and Evidence Officer", text)
        empty = json.dumps(render("technical-queue", {"id": "C-2"})["tree"])
        self.assertIn("Cannot confirm readiness", empty)
        self.assertIn("No design is recorded", empty)
        self.assertIn("Missing references are not supplied", empty)
        self.assertNotIn("Recorded evidence is complete", empty)

    def test_return_routes_to_competent_role(self) -> None:
        case = tech_case()
        case["technical"]["signoffs"]["building"] = {
            "status": "Returned",
            "reason": "Ventilation unclear",
            "history": [{"status": "Returned", "by": "Reviewer One"}],
        }
        text = json.dumps(render("technical-queue", case)["tree"])
        self.assertIn(
            "Building Safety Liaison (competent reviewer for this sign-off, not a generic",
            text,
        )
        self.assertIn("Ventilation unclear", text)
        self.assertIn("Reviewer One", text)


def record(state: str, **changes: Any) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "measure": "Loft insulation",
        "state": state,
        "checklist": "Loft insulation",
        "checklist_version": "QC-LOFT v1",
        "evidence_version": 1,
        "source": "Installer",
        "submitted_by": "Installer Ltd",
        "defect": None,
        "items": [{"label": "Depth measured", "evidence": "270mm photo"}],
    }
    rec.update(changes)
    return rec


class QualityQueue(unittest.TestCase):
    def test_accepted_measure_shows_positive_evidence_and_readiness_text(self) -> None:
        case = {
            "id": "C-1",
            "measures": "Loft insulation",
            "quality": [record("Accepted", accepted_by="Inspector")],
            "quality_handover_blockers": [],
        }
        out = render("quality-queue", case)
        text = json.dumps(out["tree"])
        self.assertIn("Evidence noted", text)
        self.assertIn("270mm photo", text)
        self.assertIn("Every measure has accepted evidence", text)
        self.assertIn("accepts, returns and hands over nothing", text)
        self.assertEqual(out["roles"][0], "Quality Inspector")
        self.assertNotIn("Building Safety Liaison", out["roles"])
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(out["tree"]))

    def test_incomplete_evidence_blocks_handover(self) -> None:
        cases: dict[str, dict[str, Any]] = {
            "unrecorded": {
                "id": "C",
                "measures": ["Loft insulation", "Heat pump"],
                "quality": [record("Accepted")],
                "quality_handover_blockers": [],
            },
            "pending": {"id": "C", "measures": "Loft insulation", "quality": [record("Submitted")]},
            "blank": {
                "id": "C",
                "measures": "Loft insulation",
                "quality": [record("Accepted", items=[{"label": "Depth", "evidence": " "}])],
            },
            "none": {"id": "C", "measures": ""},
            "not supplied": {
                "id": "C",
                "measures": "Loft insulation",
                "quality": [record("Accepted")],
            },
            "partial checklist": {
                "id": "C",
                "measures": "Loft insulation",
                "quality": [record("Accepted")],
                "quality_handover_blockers": [
                    {"measure": "Loft insulation", "reason": "Checks without evidence: Hatch."}
                ],
            },
            "stale scope or safety": {
                "id": "C",
                "measures": "Loft insulation",
                "quality": [record("Accepted")],
                "quality_handover_blockers": [
                    {"measure": "Loft insulation", "reason": "Resident scope is unknown."}
                ],
            },
        }
        for name, case in cases.items():
            with self.subTest(name):
                text = json.dumps(render("quality-queue", case)["tree"])
                self.assertIn("Cannot confirm readiness", text)
                self.assertNotIn("Every measure has accepted evidence", text)

    def test_defect_owner_return_and_reinspection(self) -> None:
        defect = {
            "description": "Gap at eaves",
            "reason": "Ventilation blocked",
            "owner": "Installer Ltd",
            "raised_by": "Inspector",
            "fixed_by": "Fitter",
            "remediation_evidence": "Photo 4",
        }
        case = {
            "id": "C",
            "measures": "Loft insulation",
            "quality": [
                record("Fixed, awaiting reinspection", defect=defect),
                record("Superseded", items=[{"label": "Old", "evidence": "old"}]),
            ],
        }
        text = json.dumps(render("quality-queue", case)["tree"])
        self.assertIn("Defect owner", text)
        self.assertIn("Installer Ltd", text)
        self.assertIn("Awaiting independent reinspection", text)
        self.assertIn("Independent reinspection by a Quality Inspector not involved", text)
        self.assertNotIn("Every measure has accepted evidence", text)
        self.assertNotIn('"old"', text)

    def test_handed_over_after_fix_keeps_passed_reinspection(self) -> None:
        defect = {
            "description": "Gap",
            "reason": "Why",
            "owner": "Owner Co",
            "raised_by": "Inspector",
        }
        case = {
            "id": "C",
            "measures": "Loft insulation",
            "quality": [
                record("Handed over", defect=defect, handover={"by": "Officer", "at": "2026-01-01"})
            ],
            "quality_handover_blockers": [],
        }
        text = json.dumps(render("quality-queue", case)["tree"])
        self.assertIn('"Passed"', text)
        self.assertNotIn("Not yet possible", text)

    def test_returned_names_owner_next_action(self) -> None:
        defect = {
            "description": "Gap",
            "reason": "Why",
            "owner": "Owner Co",
            "raised_by": "Inspector",
        }
        case = {
            "id": "C",
            "measures": "Loft insulation",
            "quality": [record("Returned", defect=defect)],
        }
        text = json.dumps(render("quality-queue", case)["tree"])
        self.assertIn("Defect owner Owner Co to correct", text)
        self.assertIn("Not yet fixed", text)


if __name__ == "__main__":
    unittest.main()
