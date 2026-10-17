"""Authenticated local grant/application evidence and changed browser behavior."""

import copy
import json
import os
import unittest
from typing import Any

from test_grant_lifecycle_controls import designate

import test_finance_match_api as fixture


class GrantLifecycleApi(unittest.TestCase):
    setUp = fixture.FinanceMatchApi.setUp
    call = fixture.FinanceMatchApi.call

    def prepare(self: Any) -> None:
        self.a = designate(self.a)
        self.b = designate(self.b)
        for user in (self.a, self.b):
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(user), user["email"])
            )
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["funding"].update(route="SYN-95", status="Draft ready", draft="SYN draft")
            self.store.save()

    def grant(self: Any, user: dict[str, Any], action: str, **body: Any) -> tuple[int, Any]:
        status, result = self.call(user, "/api/cases/ZF-1/grant", dict(action=action, **body))
        return status, result

    def test_http_denial_designated_success_and_mixed_state_projection(self: Any) -> None:
        self.assertEqual(
            self.grant(
                self.a,
                "grant_open",
                scheme="SYN-95",
                source="Unverified opportunity",
                amount=40_000_000,
            )[0],
            200,
        )
        self.assertEqual(self.grant(self.b, "grant_approve", id="GR-1")[0], 403)
        self.prepare()
        self.assertEqual(self.grant(self.b, "grant_approve", id="GR-1")[0], 200)
        self.assertEqual(
            self.grant(
                self.alias,
                "grant_propose",
                id="GR-1",
                to="Cash received",
                source="Invalid leap",
                amount=1,
            )[0],
            400,
        )
        before = copy.deepcopy(self.store.cases["ZF-1"]["grants"])
        # The existing evidence gate is separately covered; this fixture is a reviewed application.
        with self.store.lock:
            self.store._case("ZF-1")["funding"]["status"] = "Approved"
            self.store.save()
        for action in ("submit", "confirm"):
            self.assertEqual(
                self.call(self.b, "/api/cases/ZF-1/funding", dict(action=action, text=""))[0], 400
            )
            status, detail = self.call(
                self.b, "/api/cases/ZF-1/funding", dict(action=action, text="SYN " + action)
            )
            self.assertEqual(status, 200, detail)
        self.assertEqual(detail["grants"], before)
        self.assertEqual(detail["grants"][0]["state"], "Opportunity")
        self.assertEqual(detail["funding"]["status"], "Confirmed")
        self.assertNotIn("finance", detail)
        # Designation-only revocation, unchanged case sequence and authenticated cookie.
        revoked = copy.deepcopy(self.b)
        revoked["financial_authority"]["status"] = "Revoked"
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(revoked), self.b["email"])
        )
        self.assertEqual(
            self.grant(
                self.a, "grant_propose", id="GR-1", to="Award", source="SYN award", amount=1
            )[0],
            200,
        )
        self.assertEqual(self.grant(self.b, "grant_approve", id="GR-1")[0], 403)
        self.assertTrue(self.store.verify_audit())

    @unittest.skipUnless(os.environ.get("ZF_GRANT_BROWSER") == "1", "opt-in local Playwright")
    def test_browser_application_confirmation_is_not_an_award(self: Any) -> None:
        from playwright.sync_api import sync_playwright

        self.prepare()
        self.assertEqual(
            self.grant(
                self.a,
                "grant_open",
                scheme="SYN-95",
                source="Unverified opportunity",
                amount=40_000_000,
            )[0],
            200,
        )
        self.assertEqual(self.grant(self.b, "grant_approve", id="GR-1")[0], 200)
        with self.store.lock:
            self.store._case("ZF-1")["funding"]["status"] = "Submitted"
            self.store.save()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            response = page.request.post(
                self.base + "/api/login",
                data=dict(email=self.b["email"], password="synthetic-finance-test"),
            )
            self.assertEqual(response.status, 200)
            page.goto(self.base + "/app#/case/ZF-1")
            button = page.get_by_role("button", name="Record application confirmation", exact=True)
            button.wait_for()
            button.click()
            page.get_by_text(
                "Enter the evidence reference for this application event", exact=False
            ).wait_for()
            page.get_by_role("textbox", name="Application event evidence reference").fill(
                "SYN browser confirmation"
            )
            button.click()
            page.get_by_text("Application confirmation recorded.", exact=False).wait_for()
            self.assertEqual(page.get_by_text("Funder confirmed the award", exact=True).count(), 0)
            self.assertIn("Now: Opportunity.", page.locator("main").inner_text())
            grant = self.store.detail("ZF-1")["grants"][0]
            self.assertEqual(
                (grant["state"], grant["history"][0]["amount"]), ("Opportunity", 40_000_000)
            )
            self.assertEqual(
                self.store.detail("ZF-1")["funding"]["history"][-1]["source"],
                "SYN browser confirmation",
            )
            browser.close()


if __name__ == "__main__":
    unittest.main()
