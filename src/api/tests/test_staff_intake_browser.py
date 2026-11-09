"""Actual browser capture of the staff intake screen on synthetic data (#132).
Opt-in: ZF_STAFF_INTAKE_BROWSER=1.

Needs Playwright and the pinned axe-core 4.10.3 (ZF_AXE_PATH).
Run under the shared heavy-resource lock.
"""

import hashlib
import json
import os
import unittest
from pathlib import Path
from typing import Any

from dataset import supplied_appointment_fixture

from test_procurement_api import ProcurementApiFixture

AXE_SHA256 = "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
WORKER = "Wren Fictional"
URL = "/app#/screens?screen=staff-job-pack-intake&case=ZF-3"


@unittest.skipUnless(
    os.environ.get("ZF_STAFF_INTAKE_BROWSER") == "1" and os.environ.get("ZF_AXE_PATH"),
    "needs ZF_STAFF_INTAKE_BROWSER=1 and ZF_AXE_PATH",
)
class StaffIntakeBrowser(ProcurementApiFixture):
    sql = True

    def setUp(self) -> None:
        super().setUp()
        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue("ZF-3"))
        supplied_appointment_fixture(self.store, self.manager, "WO-0001", "2099-01-01")
        self.call("/api/workorders/WO-0001/appointment", dict(outcome="Booked", date="2099-01-01"))

    def scan(self, page: Any, state: str) -> None:
        raw = Path(os.environ["ZF_AXE_PATH"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), AXE_SHA256)
        page.evaluate(raw.decode())
        result = page.evaluate(
            """async () => await axe.run(document.querySelector('#app'), {
              runOnly: {type: 'tag',
                         values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}})"""
        )
        print(json.dumps(dict(state=state, violations=result["violations"])), flush=True)
        self.assertEqual(result["violations"], [], state)

    def open(self, browser: Any, email: str) -> Any:
        context = browser.new_context()
        login = context.request.post(
            self.base + "/api/login", data=dict(email=email, password="synthetic-password")
        )
        self.assertTrue(login.ok)
        page = context.new_page()
        page.goto(self.base + URL)
        page.reload()
        page.get_by_role("heading", name="Job pack and worker evidence intake").wait_for()
        return page

    def test_capture_acknowledge_readback_and_review_handoff(self) -> None:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = self.open(browser, "sam@example.test")
            page.get_by_text("Work order WO-0001").first.wait_for()
            self.scan(page, "pack open, nothing recorded")
            page.get_by_role("button", name="Record worker evidence").click()
            page.locator("#app [role=alert]").first.wait_for()
            self.assertEqual(self.store.cases["ZF-3"].get("quality") or [], [])
            self.scan(page, "rejected capture shows inline error")
            for i in range(5):
                page.locator(f"#intake-note-{i}").fill(f"Seen on site {i}")
            page.get_by_label("Worker's name").fill(WORKER)
            page.get_by_label("The worker confirms these notes are their own").check()
            page.get_by_role("button", name="Record worker evidence").click()
            page.get_by_text("Receipt SYN-").first.wait_for()
            text = page.inner_text("#app")
            self.assertIn("Submitted by worker - awaiting independent review", text)
            self.assertIn("Not yet acknowledged", text)
            self.assertIn("Acknowledging a receipt is not acceptance", text)
            self.assertIn("Unknown - not configured", text)
            self.scan(page, "recorded, not acknowledged")
            self.assertEqual(self.store.cases["ZF-3"]["quality"][0]["state"], "Submitted")
            page.close()
            other = self.open(browser, "pam@example.test")
            other.get_by_text("Receipt SYN-").first.wait_for()
            self.assertIn("Seen on site 0", other.inner_text("#app"))
            other.get_by_role("button", name="Acknowledge receipt").click()
            other.get_by_text("Receipt acknowledged - not accepted").first.wait_for()
            shown = other.inner_text("#app")
            self.assertIn("Pam Lead", shown)
            self.assertEqual(other.get_by_role("button", name="Acknowledge receipt").count(), 0)
            self.assertEqual(other.get_by_role("button", name="Record correction").count(), 0)
            self.assertEqual(self.store.cases["ZF-3"]["quality"][0]["state"], "Submitted")
            self.scan(other, "acknowledged")
            browser.close()


if __name__ == "__main__":
    unittest.main()
