"""Specialist hosts describe navigation, never extend server authority."""

import unittest
from pathlib import Path

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

    def test_engagement_retains_measure_version_and_separate_contact_boundary(self) -> None:
        source = (WEB / "screen-engagement.js").read_text()
        for field in ("m.context?.design_version", "answer.context_revision",
                      "update.safe_contact_ref", "request.remedy?.status"):
            self.assertIn(field, source)
        self.assertIn("Paused and Withdrawn", source)
        self.assertNotIn("caseApi(", source)
        self.assertNotIn('href: `tel:', source)
