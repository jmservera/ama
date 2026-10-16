"""Running synthetic HTTP app, human authority and rendered comparison evidence."""

import copy
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class StockApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["cases"][0]["resident"].pop("priority_support")
        data["cases"][0]["resident"]["adjustment"] = None
        data["staff"].extend(
            [
                dict(
                    code="RC-2",
                    name="Synthetic Designer",
                    email="rex2@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="RC-1",
                    name="Synthetic Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Synthetic Contractor",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        path = Path(self.tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app = App(self.store, "synthetic-test-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, actor: str, path: str, body: object = None) -> tuple[int, Any]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-test-password")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    @staticmethod
    def query() -> dict[str, Any]:
        return dict(
            field="epc",
            query_owner="sam@example.test",
            left=dict(
                value="D",
                source_id="SYN-REGISTER-84",
                date="2026-01-01",
                version="1",
                validation_state="Unvalidated",
            ),
            right=dict(
                value="E",
                source_id="SYN-SURVEY-84",
                date="2026-02-01",
                version="2",
                validation_state="Disputed",
            ),
        )

    def test_local_app_comparison_unknowns_and_ai_capability_remain_available(self) -> None:
        for path in ("/", "/healthz", "/app.js", "/panels.js"):
            with urllib.request.urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
        code, detail = self.call("sam", "/api/cases/ZF-1/stock-reconciliation", self.query())
        self.assertEqual(code, 200, detail)
        query = detail["stock_reconciliation"][0]
        self.assertEqual(query["left"]["value"], "D")
        self.assertEqual(query["right"]["value"], "E")
        self.assertEqual(query["query_owner"]["name"], "Sam Example")
        self.assertEqual(detail["support_status"], "Unknown")
        self.assertEqual(detail["support_coverage"], "Unknown")
        self.assertEqual(query["eligibility"], "Unknown")
        self.assertIn("SQ-1", " ".join(detail["gate"]))
        self.assertEqual(self.call("sam", "/api/assistants")[0], 200)
        self.assertNotIn("stock_reconciliation", json.dumps(self.call("kim", "/api/cases/ZF-1")[1]))
        second = self.call("sam", "/api/cases/ZF-2")[1]
        self.assertEqual(second["stock_reconciliation"], [])
        self.assertEqual(self.call("rex", "/api/cases/ZF-1")[1]["support_status"], "Unknown")
        self.assertEqual(
            self.call("rex", "/api/cases/ZF-1")[1]["resident"]["adjustment"], "Unknown"
        )
        self.assertTrue(self.store.verify_audit())

    def test_auth_validation_and_no_client_approval_authority(self) -> None:
        path = "/api/cases/ZF-1/stock-reconciliation"
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(urllib.request.Request(self.base + path, b"{}"))
        self.assertEqual(caught.exception.code, 401)
        self.assertEqual(self.call("kim", path, self.query())[0], 403)
        mutations: list[dict[str, object]] = [
            {"field": "resident"},
            {"query_owner": "kim@example.test"},
            {"authority": "Validated"},
            {"recorded_by": "someone"},
            {"left": {}},
            {"ids": ["ZF-1", "ZF-2"]},
        ]
        for mutation in mutations:
            result = self.call("sam", path, dict(self.query(), **mutation))
            self.assertIn(result[0], (400, 403), result)
        self.assertEqual(self.call("sam", "/api/cases/ZF-1")[1]["stock_reconciliation"], [])
        technical = "/api/cases/ZF-1/technical"
        self.assertEqual(
            self.call(
                "rex",
                technical,
                dict(action="design_submit", note="Synthetic design", design_by="agent"),
            )[0],
            200,
        )
        self.assertEqual(
            self.call(
                "rex",
                technical,
                dict(action="signoff_give", type="design", approved_by="sam@example.test"),
            )[0],
            403,
        )
        self.assertEqual(
            self.call("kim", technical, dict(action="signoff_give", type="assessment"))[0], 403
        )
        design = self.call("sam", "/api/cases/ZF-1")[1]["technical"]
        self.assertEqual(design["design_by"], "rex@example.test")
        self.assertEqual(design["signoffs"], {})

    def test_withdraw_unblocks_http_signoff_and_retains_audit(self) -> None:
        path = "/api/cases/ZF-1"
        self.assertEqual(
            self.call(
                "rex2",
                path + "/technical",
                dict(
                    action="design_submit",
                    note="Synthetic design",
                ),
            )[0],
            200,
        )
        self.assertEqual(self.call("sam", path + "/stock-reconciliation", self.query())[0], 200)
        signoff = dict(action="signoff_give", type="design")
        self.assertEqual(self.call("rex", path + "/technical", signoff)[0], 409)
        event = dict(query_id="SQ-1", action="withdraw", reason="Duplicate query")
        self.assertEqual(self.call("rex", path + "/stock-query-event", event)[0], 403)
        code, detail = self.call("sam", path + "/stock-query-event", event)
        self.assertEqual(code, 200, detail)
        self.assertEqual(detail["stock_reconciliation"][0]["status"], "Withdrawn")
        self.assertEqual(
            detail["stock_reconciliation_events"][0]["recorded_by"]["email"], "sam@example.test"
        )
        self.assertEqual(self.call("rex", path + "/technical", signoff)[0], 200)
        self.assertEqual(self.call("rex2", path + "/technical", signoff)[0], 403)
        self.assertEqual(self.call("sam", path + "/stock-query-event", event)[0], 400)
        self.assertTrue(self.store.verify_audit())

    def test_http_case_responsibility_and_human_resolution(self) -> None:
        path = "/api/cases/ZF-1"
        self.assertEqual(self.call("rex", path + "/stock-reconciliation", self.query())[0], 403)
        self.assertEqual(
            self.call("sam", "/api/cases/ZF-5/stock-reconciliation", self.query())[0], 403
        )
        self.assertEqual(self.call("sam", path + "/stock-reconciliation", self.query())[0], 200)
        body = dict(
            query_id="SQ-1", action="resolve", reason="Human attestation", evidence="SYN-REVIEW"
        )
        self.assertEqual(self.call("sam", path + "/stock-query-event", body)[0], 403)
        self.assertEqual(self.call("kim", path + "/stock-query-event", body)[0], 403)
        self.assertEqual(
            self.call("pam", path + "/stock-query-event", dict(body, recorded_by="agent"))[0], 400
        )
        code, detail = self.call("pam", path + "/stock-query-event", body)
        self.assertEqual(code, 200, detail)
        self.assertEqual(detail["stock_reconciliation"][0]["status"], "Reconciled")
        self.assertEqual(detail["stock_reconciliation"][0]["authority"], "Unknown")
        self.assertEqual(
            detail["stock_reconciliation_events"][0]["recorded_by"]["name"], "Pam Lead"
        )
        self.assertEqual(self.call("sam", "/api/cases/ZF-2")[1]["stock_reconciliation"], [])

    @unittest.skipUnless(
        os.environ.get("ZF_STOCK_BROWSER") == "1",
        "Opt-in rendered check requires local Playwright browser.",
    )
    def test_rendered_comparison_and_case_switch(self) -> None:
        from playwright.sync_api import sync_playwright

        self.assertEqual(
            self.call("sam", "/api/cases/ZF-1/stock-reconciliation", self.query())[0], 200
        )
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.context.add_cookies(
                    [
                        dict(
                            name="zf_session",
                            value=self.cookies["sam"].split("=", 1)[1],
                            url=self.base,
                        )
                    ]
                )
                page.goto(self.base + "/app#/case/ZF-1")
                panel = page.get_by_role("region", name="Stock source comparisons")
                panel.wait_for()
                text = panel.inner_text()
                for value in (
                    "SYN-REGISTER-84",
                    "SYN-SURVEY-84",
                    "Sam Example",
                    "2026-01-01",
                    "2026-02-01",
                    "Unvalidated",
                    "Disputed",
                    "Authority: Unknown",
                    "Resolution: Unknown",
                    "Eligibility: Unknown",
                ):
                    self.assertIn(value, text)
                for value in ("D", "E"):
                    self.assertEqual(panel.get_by_text(value, exact=True).count(), 1)
                self.assertEqual(panel.get_by_role("heading", level=2).count(), 1)
                page.keyboard.press("Tab")
                self.assertTrue(page.evaluate("document.activeElement !== document.body"))
                self.assertIn("Support flag coverage", page.locator("main").inner_text())
                self.assertEqual(
                    page.locator("dt")
                    .filter(has_text="Support needs")
                    .locator("+ dd")
                    .inner_text(),
                    "Unknown",
                )
                self.assertEqual(
                    self.call(
                        "sam",
                        "/api/cases/ZF-1/stock-query-event",
                        dict(
                            query_id="SQ-1",
                            action="withdraw",
                            reason="Synthetic duplicate",
                        ),
                    )[0],
                    200,
                )
                page.reload()
                panel = page.get_by_role("region", name="Stock source comparisons")
                panel.get_by_text("SQ-1: epc. Withdrawn", exact=True).wait_for()
                self.assertIn("SQE-1: Withdrawn, recorded by Sam Example", panel.inner_text())
                self.assertIn("Synthetic duplicate", panel.inner_text())
                self.assertIn("SYN-REGISTER-84", panel.inner_text())
                page.goto(self.base + "/app#/case/ZF-2")
                page.get_by_text("No comparison recorded.", exact=False).wait_for()
                self.assertNotIn("SYN-REGISTER-84", page.locator("main").inner_text())
            finally:
                browser.close()
