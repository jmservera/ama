"""Running local app exercise with synthetic resident decisions and authority."""

import copy
import json
import os
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class ResidentApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                dict(
                    code="RLO-2",
                    name="Rae Reviewer",
                    email="rae@example.test",
                    role="Resident Liaison Officer",
                ),
                dict(
                    code="CON-1",
                    name="Kim Contractor",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
            ]
        )
        self.path.write_text(json.dumps(data))
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app = App(self.store, "synthetic-only")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def call(self, path: str, actor: str = "", body: object = None) -> tuple[int, Any]:
        if actor and actor not in self.cookies:
            req = Request(
                self.base + "/api/login",
                json.dumps(dict(email=f"{actor}@example.test", password="synthetic-only")).encode(),
            )
            with urlopen(req, timeout=5) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies.get(actor, ""), "Content-Type": "application/json"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                raw = response.read()
                return response.status, (
                    json.loads(raw)
                    if "application/json" in response.headers.get("Content-Type", "")
                    else raw.decode()
                )
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def action(self, action: str, actor: str = "sam", **kw: Any) -> tuple[int, Any]:
        return self.call("/api/cases/ZF-1/resident", actor, dict(action=action, **kw))

    def context(self) -> None:
        self.assertEqual(
            self.call(
                "/api/cases/ZF-1/technical",
                "pam",
                dict(action="design_submit", note="Synthetic design"),
            )[0],
            200,
        )
        code, detail = self.action(
            "scope_record",
            measure="Loft insulation",
            design_version=1,
            scope="SYN-SCOPE",
            source="SYN-SCOPE-SOURCE",
        )
        self.assertEqual(code, 200, detail)

    def commitment(self, **kw: Any) -> tuple[int, Any]:
        return self.action(
            "update_record",
            **dict(
                dict(
                    expected_version=0,
                    purpose="SYN commitment",
                    owner="sam@example.test",
                    due_at="2099-01-01T12:00:00Z",
                    basis="SYN fixture basis",
                    status="Outstanding",
                    safe_contact_ref="SYN-SAFE-88",
                ),
                **kw,
            ),
        )

    def test_http_commitment_and_independent_closure_restart(self) -> None:
        self.assertEqual(self.commitment(basis="")[0], 400)
        self.assertEqual(self.commitment(owner="kim@example.test")[0], 400)
        code, detail = self.commitment()
        self.assertEqual(code, 200, detail)
        self.assertEqual(detail["resident_update"]["owner_identity"]["email"], "sam@example.test")
        self.assertEqual(self.commitment()[0], 409)
        service = dict(
            summary="SYN complaint",
            desired_outcome="SYN remedy",
            service_owner="sam@example.test",
            redress_owner="rae@example.test",
            next_update="2099-01-01",
        )
        for route in ("Complaint", "Defect", "Charge query"):
            self.assertEqual(self.action("service_open", route=route, **service)[0], 200)
        self.assertEqual(
            self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")[
                0
            ],
            200,
        )
        self.assertEqual(
            self.action("service_close", "rae", id="SR-1", note="SYN response")[0], 200
        )
        code, detail = self.call("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        self.assertEqual(detail["service_requests"][0]["status"], "Closed")
        self.assertEqual(detail["service_requests"][0]["remedy"]["status"], "Open")
        self.assertEqual(detail["service_requests"][1]["status"], "Open")
        self.assertEqual(detail["service_requests"][2]["status"], "Open")
        self.assertEqual(
            self.action(
                "remedy_update",
                "sam",
                id="SR-1",
                expected_version=1,
                status="Resolved",
                note="SYN wrong owner",
            )[0],
            403,
        )
        self.assertEqual(
            self.action(
                "remedy_update",
                "rae",
                id="SR-1",
                expected_version=1,
                status="Resolved",
                note="SYN remedy",
            )[0],
            200,
        )
        for actor in ("kim",):
            projected = self.call("/api/cases/ZF-1", actor)[1]
            self.assertNotIn("SYN-SAFE-88", json.dumps(projected))
            self.assertNotIn("service_requests", projected)
        again = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(again.db.close)
        self.assertEqual(again.cases["ZF-1"]["service_requests"][0]["status"], "Closed")
        self.assertTrue(again.verify_audit())

    def test_http_postcommit_sync_and_projection_outcomes_are_truthful(self) -> None:
        other = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(other.db.close)
        save, sync = self.store.save, self.store._sync
        armed = False

        def interleave() -> None:
            nonlocal armed
            other.log_call(other.staff["sam@example.test"], "ZF-2", "SYN", "SYN unrelated write")
            armed = True
            save()

        def fail_sync() -> None:
            if armed:
                raise OSError("SYN postcommit synchronization")
            sync()

        with (
            patch.object(self.store, "save", side_effect=interleave),
            patch.object(self.store, "_sync", side_effect=fail_sync),
            self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
        ):
            code, detail = self.commitment()
        self.assertEqual(code, 409)
        self.assertEqual(detail["outcome"], "committed")
        self.assertIn("recorded", detail["error"])
        self.assertIn("Reload", detail["error"])
        with (
            patch.object(self.store, "detail", side_effect=OSError("SYN projection fault")),
            self.assertLogs("zava_forward.api.server", level="ERROR"),
        ):
            code, detail = self.commitment(expected_version=1)
        self.assertEqual(code, 409)
        self.assertEqual(detail["outcome"], "committed")
        code, refused = self.commitment(expected_version=1)
        self.assertEqual(code, 409)
        self.assertNotIn("outcome", refused)
        again = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(again.db.close)
        self.assertEqual(again.cases["ZF-1"]["resident_update"]["version"], 2)
        audit = list(again.audit_entries())
        self.assertEqual(sum(e["action"] == "resident_update_record" for e in audit), 2)
        self.store.save()
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertTrue(again.verify_audit())

    @unittest.skipUnless(os.environ.get("ZF_RESIDENT_BROWSER") == "1", "opt-in local browser")
    def test_browser_commitment_reassignment_response_closure_and_remedy_reopen(self) -> None:
        from playwright.sync_api import sync_playwright

        self.assertEqual(
            self.action(
                "service_open",
                route="Complaint",
                summary="SYN browser complaint",
                desired_outcome="SYN remedy",
                service_owner="sam@example.test",
                redress_owner="rae@example.test",
                next_update="2099-01-01",
            )[0],
            200,
        )
        self.assertEqual(
            self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")[
                0
            ],
            200,
        )
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(
                viewport={"width": 1280, "height": 900}, reduced_motion="reduce"
            )
            context.route(
                "**/*",
                lambda route: (
                    route.continue_()
                    if route.request.url.startswith(self.base + "/")
                    else route.abort()
                ),
            )
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))

            def login(actor: str) -> None:
                context.clear_cookies()
                page.goto(self.base + "/app")
                page.locator("#email").fill(f"{actor}@example.test")
                page.locator("#pw").fill("synthetic-only")
                page.locator("button[type=submit]").click()
                page.locator("#account").wait_for()
                page.goto(self.base + "/app#/case/ZF-1")
                page.get_by_role(
                    "heading", name="Resident-update commitment", exact=True
                ).wait_for()

            def fill_update() -> None:
                page.locator("#ru-record-purpose").fill("SYN browser update")
                page.locator("#ru-record-due_at").fill("2099-01-01T12:00")
                page.locator("#ru-record-basis").fill("SYN selected fixture basis")

            login("sam")
            page.get_by_text("Record or reassign update commitment", exact=True).first.click()
            page.locator("#ru-record-purpose").fill("SYN incomplete")
            page.locator("#ru-record-purpose").press("Enter")
            page.locator("#ru-record-feedback").get_by_text("Enter", exact=False).wait_for()
            self.assertNotIn("resident_update", self.store.cases["ZF-1"])
            self.assertEqual(page.locator("#ru-record-purpose").input_value(), "SYN incomplete")
            fill_update()
            page.locator("#ru-record-basis").press("Enter")
            page.get_by_text("SYN browser update", exact=False).first.wait_for()
            page.get_by_text("Record or reassign update commitment", exact=True).first.click()
            fill_update()
            page.locator("#ru-record-owner").select_option("rae@example.test")
            page.locator("#ru-record-basis").press("Enter")
            page.get_by_text("Version 2.", exact=False).first.wait_for()
            login("rae")
            page.get_by_text("Close a request response", exact=True).click()
            page.get_by_label("Response outcome (remedy stays separate)", exact=True).fill(
                "SYN response"
            )
            page.get_by_role("button", name="Close response", exact=True).click()
            page.get_by_text("Response: Closed.", exact=False).wait_for()
            page.get_by_text("Remedy: Open.", exact=False).wait_for()
            for version, status in ((1, "Resolved"), (2, "Closed"), (3, "Open")):
                page.get_by_text("Record remedy progress for SR-1", exact=True).first.click()
                page.locator("#remedy-SR-1-status").select_option(status)
                page.locator("#remedy-SR-1-note").fill("SYN remedy evidence")
                page.locator("#remedy-SR-1-note").press("Enter")
                page.get_by_text(f"Remedy: {status}.", exact=False).wait_for()
                self.assertEqual(
                    self.store.cases["ZF-1"]["service_requests"][0]["remedy"]["version"],
                    version + 1,
                )
            page.get_by_text("Reopen response for SR-1", exact=True).first.click()
            page.locator("#response-SR-1-note").fill("SYN response reopening")
            page.locator("#response-SR-1-note").press("Enter")
            page.get_by_text("Response: Open.", exact=False).wait_for()
            for width in (320, 390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                self.assertTrue(
                    page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                )
            self.assertEqual(errors, [])
            browser.close()

    def test_live_local_http_decision_pause_redress_and_restart(self) -> None:
        self.assertEqual(self.call("/healthz")[0], 200)
        self.assertEqual(self.call("/app")[0], 200)
        script = self.call("/panels.js")[1]
        self.assertIn("Current scope revision", script)
        self.assertIn("Request independent human review", script)
        self.assertIn('options: ["", "Waiting", "Accepted"', script)
        detail = self.call("/api/cases/ZF-1", "sam")[1]
        self.assertEqual(detail["measure_decisions"][0]["status"], "Not recorded")
        self.context()
        body: dict[str, Any] = dict(
            measure="Loft insulation",
            context_revision=1,
            status="Accepted",
            answered_by="The resident",
            source="SYN-STATEMENT",
            recorded_by_email="forged@example.test",
        )
        self.assertEqual(self.action("decision_record", **body)[0], 200)
        code, detail = self.action(
            "decision_record", **dict(body, status="Withdrawn", note="The resident asked to stop")
        )
        self.assertEqual(code, 200)
        answer = detail["measure_decisions"][0]["versions"][-1]
        self.assertEqual(answer["recorded_by_email"], "sam@example.test")
        self.assertEqual(detail["measure_decisions"][0]["review"]["status"], "Needs human review")
        choices = copy.deepcopy(detail["measure_decisions"])
        service = dict(
            summary="Synthetic review request",
            desired_outcome="Independent human review",
            service_owner="sam@example.test",
            redress_owner="rae@example.test",
            next_update="2099-01-01",
        )
        self.assertEqual(
            self.action(
                "service_open",
                route="Independent review",
                review_measure="Loft insulation",
                review_decision_version=2,
                review_reference="SYN-REVIEW",
                **service,
            )[0],
            200,
        )
        self.assertEqual(
            self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")[
                0
            ],
            403,
        )
        self.assertEqual(
            self.action(
                "service_update", "rae", id="SR-1", status="Resolved", next_update="2099-01-01"
            )[0],
            200,
        )
        self.assertEqual(
            self.action("service_close", "rae", id="SR-1", note="Synthetic explanation")[0], 200
        )
        self.assertEqual(self.action("service_open", route="Complaint", **service)[0], 200)
        self.assertEqual(self.call("/api/cases/ZF-1", "sam")[1]["measure_decisions"], choices)
        self.assertEqual(self.action("decision_record", **body)[0], 400)
        self.assertEqual(
            self.action("decision_record", **dict(body, review_ref="SYN-HUMAN-REVIEW"))[0], 200
        )
        again = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(again.db.close)
        self.assertEqual(again.detail("ZF-1")["measure_decisions"][0]["status"], "Accepted")
        self.assertTrue(again.verify_audit())
        self.assertEqual(self.call("/api/assistants", "sam")[0], 200)

    def test_roles_authority_disclosure_and_no_failure_mutation(self) -> None:
        self.context()
        self.assertEqual(self.action("decision_record", actor="")[0], 401)
        self.assertEqual(self.action("decision_record", actor="kim")[0], 403)
        self.assertEqual(
            self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")[0],
            200,
        )
        authority: dict[str, Any] = dict(
            measure="Loft insulation",
            context_revision=1,
            representative_ref="SYN-REP",
            tasks=["Works decision", "Receive information"],
            status="Confirmed",
            authority_date="2026-01-01",
            review_date="2099-01-01",
            safe_contact_ref="SYN-SAFE-CANARY",
            source="SYN-AUTH-CANARY",
            resident_wishes="SYN-WISHES-CANARY",
        )
        self.assertEqual(self.action("representative_record", **authority)[0], 200)
        self.assertEqual(
            self.action(
                "disclosure_check",
                measure="Loft insulation",
                context_revision=1,
                representative_ref="SYN-REP",
                task="Receive information",
            )[0],
            200,
        )
        self.assertEqual(
            self.action("representative_record", **dict(authority, status="Disputed"))[0], 200
        )
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        self.assertEqual(
            self.action(
                "decision_record",
                measure="Loft insulation",
                context_revision=1,
                status="Accepted",
                answered_by="Their representative",
                representative_ref="SYN-REP",
                source="SYN",
            )[0],
            400,
        )
        for actor in ("rex", "pam"):
            text = json.dumps(self.call("/api/cases/ZF-1", actor)[1])
            for canary in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SAFE-CANARY"):
                self.assertIn(canary, text)
        for actor in ("kim",):
            text = json.dumps(self.call("/api/cases/ZF-1", actor)[1])
            for canary in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SAFE-CANARY"):
                self.assertNotIn(canary, text)
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_manager_read_only_coordinator_records_and_contractor_flags(self) -> None:
        self.context()
        self.assertEqual(
            self.action("safe_contact_record", "rex", safe_contact_ref="SYN-SAFE", source="SYN")[0],
            200,
        )
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for path, body in (
            (
                "/api/cases/ZF-1/resident",
                dict(action="safe_contact_record", safe_contact_ref="FORGED", source="FORGED"),
            ),
            ("/api/cases/ZF-1/decision", dict(status="Accepted")),
        ):
            self.assertEqual(self.call(path, "pam", body)[0], 403)
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertFalse(self.call("/api/cases/ZF-1", "pam")[1]["can_record_resident"])
        self.assertEqual(
            self.call("/api/cases/ZF-1", "kim")[1]["resident_readiness"],
            [dict(measure="Loft insulation", flag="Hold")],
        )
