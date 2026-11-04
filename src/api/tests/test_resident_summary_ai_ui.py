"""Browser test of the resident AI case summary branches in demo.js showAi (#462)."""

from __future__ import annotations

import importlib.util
import json
import threading
import unittest
from datetime import timedelta
from typing import Any

from zava_forward.core import resident_showcase as rs

from test_resident_demo_api import FAKE_PASSWORD, KEY, NOW, Clock, FakeReader, make_row
from zava_forward.api.resident_demo import app as demo

HAS_PLAYWRIGHT = importlib.util.find_spec("playwright") is not None
RULES = "Summary by rules. Not an instruction."
AI_LABEL = "AI suggestion, not approved. Not an instruction."


@unittest.skipUnless(HAS_PLAYWRIGHT, "Playwright is not installed")
class ResidentSummaryAiUi(unittest.TestCase):
    def setUp(self) -> None:
        clock = Clock()
        reader = FakeReader([make_row("C-1", "one@example.com", stage="Survey booked")])
        expiry = NOW + timedelta(hours=6)
        self.app = demo.ResidentDemo(
            reader,
            rs.build_identity_map(reader.list_rows(), NOW),
            rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
            rs.SessionCodec(KEY, expiry, clock),
            rs.LoginLimiter(clock=clock),
            ("127.0.0.1",),
            expiry,
            port=0,
            clock=clock,
        )
        self.server = demo.serve(self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def test_ai_success_fallback_and_reduced_motion(self) -> None:
        from playwright.sync_api import Error, Route, expect, sync_playwright

        reply: dict[str, Any] = {}

        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except Error as exc:
                self.skipTest(f"Chromium is not available: {exc}")
            try:
                page = browser.new_page()

                def assistant(route: Route) -> None:
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=json.dumps(reply),
                    )

                page.route("**/demo/assistant", assistant)
                page.goto(f"http://127.0.0.1:{self.app.port}")
                page.get_by_label("Email address").fill("one@example.com")
                page.get_by_label("Password", exact=True).fill(FAKE_PASSWORD)
                page.get_by_role("button", name="Sign in", exact=True).click()
                summary = page.locator("#sec-summary")
                expect(summary).to_contain_text(RULES)
                generate = page.locator("#summary-ai-button")
                back = summary.get_by_role("button", name="Show rules summary instead")

                reply.update(
                    label="AI summary of your recorded facts",
                    answer="AI says the survey is booked.",
                    sources=["Stage: Survey booked"],
                )
                page.locator("#summary-ai-consent").check()
                generate.click()
                expect(summary).to_contain_text(AI_LABEL)
                expect(summary.locator(".status-badge.caution")).to_have_count(1)
                expect(summary).to_contain_text("AI says the survey is booked.")
                expect(summary).to_contain_text("AI-generated content may be incorrect")
                expect(summary).to_contain_text("Record facts the AI used:")
                expect(summary).to_contain_text("Stage: Survey booked")
                expect(summary).not_to_contain_text(RULES)
                expect(page.locator("#summary-status")).to_contain_text("AI summary ready")
                expect(back).to_be_visible()

                back.click()
                expect(summary).to_contain_text(RULES)
                expect(summary).not_to_contain_text(AI_LABEL)
                expect(summary).not_to_contain_text("AI-generated content may be incorrect")
                expect(back).to_be_hidden()
                expect(generate).to_be_focused()

                reply.update(label="Summary by rules because AI is not enabled", answer="x")
                generate.click()
                expect(page.locator("#summary-status")).to_contain_text(
                    "AI summary is not available right now"
                )
                expect(summary).to_contain_text(RULES)
                expect(summary).not_to_contain_text(AI_LABEL)
                expect(back).to_be_hidden()

                page.emulate_media(reduced_motion="reduce")
                page.evaluate(
                    "() => { const s = document.getElementById('status');"
                    " s.className = 'status loading-card'; }"
                )
                animation = page.evaluate(
                    "getComputedStyle(document.getElementById('status'), '::before').animationName"
                )
                self.assertEqual(animation, "none")
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
