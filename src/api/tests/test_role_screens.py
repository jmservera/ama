"""Specialist hosts describe navigation, never extend server authority."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.signoffs import SignoffMixin

from zava_forward.api.workbench import navigation

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class RoleScreens(unittest.TestCase):
    def test_staff_and_contractor_navigation_retains_scoped_screen_link(self) -> None:
        for role in ("Resident Liaison Officer", "Retrofit Programme Manager", "Contractor"):
            links = navigation({"role": role})
            self.assertEqual(links[-1]["href"], "#/screens")
            self.assertTrue(links[-1]["scope"])
        self.assertEqual(navigation({"role": "Asset Executive"}), [])

    def test_host_reads_existing_scoped_endpoints_without_post(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        self.assertIn("/api/cases?view=all&limit=20&offset=", source)
        self.assertIn("encodeURIComponent(caseId)", source)
        self.assertNotIn('"POST"', source)
        self.assertNotIn("innerHTML", source)

    def test_route_supports_contractor_screens_before_contractor_case_dispatch(self) -> None:
        source = (WEB / "app.js").read_text()
        self.assertLess(
            source.index("return await roleScreensView()"),
            source.index("return await (m ? contractorCaseView"),
        )
        self.assertIn('src="/role-screens.js"', (WEB / "index.html").read_text())

    def test_host_requires_explicit_selection_and_retains_abort_boundary(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        self.assertIn("No home selected", source)
        self.assertIn("signal.throwIfAborted()", source)
        self.assertIn('"aria-current"', source)
        self.assertIn("Reset screen view", source)

    def test_technical_preserves_selective_review_invalidation_and_quality_evidence(self) -> None:
        source = (WEB / "screen-technical.js").read_text()
        for field in ("record.defect?.owner", "record.items", "record.handover?.note"):
            self.assertIn(field, source)
        self.assertIn("Missing or stale evidence cannot establish readiness", source)
        self.assertNotIn("post(", source)

        def render_reviews(case: dict[str, Any]) -> list[list[Any]]:
            result = subprocess.run(
                [
                    "node",
                    "-e",
                    """
const fs = require("node:fs");
const vm = require("node:vm");
const tables = {};
let screen;
const context = {
  registerRoleScreen: value => { screen = value; }, screenManagers: [],
  h: () => null, screenFields: () => null, screenUnknown: () => null,
  screenPanel: () => null,
  screenTable: (caption, columns, rows) => { tables[caption] = rows; }
};
vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), context);
screen.render(JSON.parse(fs.readFileSync(0, "utf8")));
console.log(JSON.stringify(tables["Independent technical reviews"]));
""",
                    str(WEB / "screen-technical.js"),
                ],
                input=json.dumps(case),
                text=True,
                capture_output=True,
                check=True,
                timeout=10,
            )
            rows: list[list[Any]] = json.loads(result.stdout)
            return rows

        case: dict[str, Any] = {
            "technical": {
                "design_version": 1,
                "versions": [],
                "signoffs": {
                    key: {"status": "Signed off", "version": 1, "by": f"SYN {key}", "history": []}
                    for key in ("assessment", "design", "building", "coordination")
                },
            }
        }
        SignoffMixin()._tech_design_change(
            {"role": "Retrofit Programme Manager", "email": "sam@example.test", "name": "SYN Sam"},
            case,
            {"affects": ["coordination"], "note": "SYN coordination change"},
        )
        rows = render_reviews(case)
        for row in rows[:3]:
            with self.subTest(unaffected=row[0]):
                self.assertEqual(row[1:3], ["Signed off", 1])
                self.assertEqual(row[-1], "Recorded sign-off; verify professional evidence")
                self.assertNotIn("stale", row[-1].lower())
        self.assertEqual(rows[3][1:3], ["Needs reassessment", 1])
        self.assertIn("Design changed to version 2", rows[3][-2])
        self.assertEqual(rows[3][-1], "Not signed off; follow the source review decision")
        self.assertNotIn("Signed off", rows[3])

        signoffs = case["technical"]["signoffs"]
        signoffs["assessment"]["version"] = None
        signoffs["design"].update(status="Returned", version=2, reason="SYN return")
        del signoffs["building"]
        signoffs["coordination"].update(status="Signed off", version=2)
        rows = render_reviews(case)
        self.assertEqual(rows[0][-1], "Missing sign-off or version; cannot establish readiness")
        self.assertEqual(rows[1][1], "Returned")
        self.assertEqual(
            rows[1][-2:], ["SYN return", "Not signed off; follow the source review decision"]
        )
        self.assertEqual(rows[2][-1], "Missing sign-off or version; cannot establish readiness")
        self.assertEqual(rows[3][-1], "Recorded sign-off; verify professional evidence")
