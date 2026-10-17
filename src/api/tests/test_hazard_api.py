"""Loopback synthetic app exercise for hazard evidence and home retrofit holds."""

import copy
import json
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


class HazardApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                dict(
                    code="BS-2",
                    name="Bo Safe",
                    email="bo@example.test",
                    role="Building Safety Liaison",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Kim Builder",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        data["cases"][0].update(closed=True, stage="Completed")
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(data))
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
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

    def post(self, actor: str, action: str, body: object) -> tuple[int, Any]:
        return self.call(actor, f"/api/cases/ZF-1/{action}", body)

    def report(self) -> None:
        code, detail = self.post(
            "sam",
            "hazard-raise",
            dict(
                category="Damp and mould",
                priority="Emergency",
                note="SYN-NOTE-CANARY",
                source="SYN-SOURCE-CANARY",
                aware_at="2026-01-01T10:00:00Z",
                raised_by_email="forged@example.test",
                hold={"scope": "Building"},
            ),
        )
        self.assertEqual(code, 200)
        h = detail["hazards"][0]
        self.assertEqual(h["sender"]["email"], "sam@example.test")
        self.assertEqual(h["hold"]["scope"], "Home")

    def refer(self) -> None:
        result = self.post(
            "sam",
            "hazard-refer",
            dict(index=0, to="bea@example.test", job="SYN-JOB-CANARY", evidence="SYN-SENT-CANARY"),
        )
        self.assertEqual(result[0], 200, result[1])

    def test_running_synthetic_app_lifecycle_and_persistence(self) -> None:
        for path in ("/", "/healthz"):
            with urllib.request.urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
        with urllib.request.urlopen(self.base + "/app.js") as response:
            script = response.read().decode()
        self.assertIn("also available after retrofit closure", script)
        self.assertIn("External evidence reference", script)
        self.assertIn("Unknown (external service owns timing)", script)
        before = self.call("sam", "/api/cases/ZF-1")[1]
        self.report()
        self.refer()
        self.assertEqual(
            self.post("bea", "hazard-accept", dict(index=0, evidence="Too soon"))[0], 400
        )
        for action, expected in (("hazard-receive", "Received"), ("hazard-accept", "Accepted")):
            code, detail = self.post("bea", action, dict(index=0, evidence=f"SYN-{action}"))
            self.assertEqual((code, detail["hazards"][0]["state"]), (200, expected))
        self.assertEqual(
            self.post(
                "bea",
                "hazard-times",
                dict(
                    index=0,
                    evidence="SYN-TIMES",
                    response_due_at="2026-01-02T10:00:00Z",
                    responded_at="2026-01-02T09:00:00Z",
                    resident_update_due_at="2026-01-03T10:00:00Z",
                    resident_updated_at="2026-01-03T09:00:00Z",
                ),
            )[0],
            200,
        )
        self.assertEqual(
            self.post("bea", "hazard-repaired", dict(index=0, evidence="SYN-REPAIR-CANARY"))[0], 200
        )
        self.assertEqual(
            self.post("bea", "hazard-release", dict(index=0, note="Reason", evidence="SYN-CLEAR"))[
                0
            ],
            403,
        )
        code, detail = self.post(
            "bo", "hazard-release", dict(index=0, note="Independent check", evidence="SYN-CLEAR")
        )
        self.assertEqual((code, detail["hazards"][0]["state"]), (200, "Retrofit hold released"))
        for key in ("closed", "stage", "decision", "owner_code"):
            self.assertEqual(detail[key], before[key])
        reopened = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(reopened.db.close)
        self.assertEqual(reopened.detail("ZF-1")["hazards"], detail["hazards"])
        self.assertTrue(reopened.verify_audit())
        self.assertEqual(self.call("sam", "/api/assistants")[0], 200)
        self.assertEqual(self.post("sam", "hazard-close", dict(index=0))[0], 404)
        self.assertEqual(self.post("sam", "hazard-reset-clock", dict(index=0))[0], 404)

    def test_roles_missing_evidence_and_unauthenticated_requests(self) -> None:
        request = urllib.request.Request(self.base + "/api/cases/ZF-1/hazard-raise", b"{}")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code, 401)
        self.assertEqual(
            self.post("sam", "hazard-raise", dict(category="Electrical", priority="Routine"))[0],
            400,
        )
        self.report()
        self.refer()
        for action in (
            "hazard-receive",
            "hazard-accept",
            "hazard-times",
            "hazard-repaired",
            "hazard-release",
            "hazard-refer",
        ):
            body = dict(index=0, evidence="SYN", note="Reason", to="bea@example.test", job="SYN")
            self.assertEqual(self.post("kim", action, body)[0], 403)
        self.assertEqual(
            self.post(
                "bo",
                "hazard-receive",
                dict(index=0, evidence="SYN", received_by="bea@example.test"),
            )[0],
            403,
        )
        self.assertEqual(self.post("bea", "hazard-receive", dict(index=0))[0], 400)
        self.assertEqual(self.post("bea", "hazard-receive", dict(index=-1, evidence="SYN"))[0], 400)
        no_need = json.dumps(self.call("rex", "/api/cases/ZF-1")[1])
        for text in ("SYN-SOURCE-CANARY", "SYN-SENT-CANARY", "SYN-JOB-CANARY", "SYN-NOTE-CANARY"):
            self.assertNotIn(text, no_need)
        self.assertNotIn("hazards", self.call("kim", "/api/cases/ZF-1")[1])

    def test_legacy_referral_binding_is_prospective_over_http(self) -> None:
        with self.store.lock:
            self.store._case("ZF-1")["hazards"] = [
                dict(
                    category="Damp",
                    priority="P1",
                    noticed="2025-01-01",
                    referred="2025-01-02",
                    repaired="2025-01-03",
                    released=False,
                    job="OLD",
                    owner="Unknown receiver",
                )
            ]
            self.store.save()
        self.assertEqual(self.post("bea", "hazard-repaired", dict(index=0, evidence="SYN"))[0], 400)
        self.refer()
        detail = self.call("sam", "/api/cases/ZF-1")[1]
        h = detail["hazards"][0]
        self.assertIsNone(h["aware_at"])
        self.assertIsNone(h["received_at"])
        self.assertIsNone(h["accepted_at"])
        self.assertIsNone(h["repaired"])
        self.assertEqual(h["legacy_record"]["job"], "OLD")
        self.assertEqual(len(h["history"]), 1)

    def test_cached_session_cannot_record_after_staff_authority_changes(self) -> None:
        self.report()
        self.refer()
        self.call("bea", "/api/cases/ZF-1")
        before = self.store.detail("ZF-1")["hazards"]
        audit = list(self.store.audit_entries())
        row = self.store.db.execute(
            "SELECT body FROM staff WHERE email=?", ("bea@example.test",)
        ).fetchone()
        original = json.loads(row[0])
        for field, value in (("role", "Contractor"), ("oid", "SYN-REPLACED")):
            changed = dict(original, **{field: value})
            with self.store.dblock:
                self.store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?",
                    (json.dumps(changed), "bea@example.test"),
                )
            code, _ = self.post("bea", "hazard-receive", dict(index=0, evidence="SYN-RECEIPT"))
            self.assertEqual(code, 403)
            self.assertEqual(self.store.detail("ZF-1")["hazards"], before)
            self.assertEqual(list(self.store.audit_entries()), audit)
        with self.store.dblock:
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(original), "bea@example.test"),
            )
        self.assertEqual(
            self.post("bea", "hazard-receive", dict(index=0, evidence="SYN-RECEIPT"))[0], 200
        )
