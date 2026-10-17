"""Loopback HTTP exercise for the issue 83 staff workflow, using synthetic data only."""

import base64
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

from dataset import change_metadata
from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class HandoffApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                dict(
                    code="RLO-02",
                    name="Rae Other",
                    email="rae@example.test",
                    role="Resident Liaison Officer",
                ),
                dict(
                    code="RC-01",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-01",
                    name="Kim Builder",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        data["cases"][0]["stage"] = "Install booked"
        data["cases"][1].update(stage="Completed", closed=True)
        path = Path(self.tmp.name) / "seed.json"
        path.write_text(json.dumps(data))
        self.store = self.make_store(path)
        self.addCleanup(self.store.db.close)
        self.app = App(self.store, "synthetic-test-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def make_store(self, path: Path) -> SqlStore:
        return SqlStore(str(path), str(path.with_suffix(".sqlite")))

    def reopen_store(self) -> SqlStore:
        return SqlStore("nonexistent-seed-is-not-read", self.store.db_path)

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(
        self,
        actor: str,
        path: str,
        body: object = None,
    ) -> tuple[int, Any]:
        """JSON boundary: responses include heterogeneous legacy case records."""
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

    def post(self, actor: str, action: str, body: object = None) -> tuple[int, Any]:
        if action in ("offer-handoff", "accept-handoff", "handover"):
            body = {**change_metadata(self.store), **(body if isinstance(body, dict) else {})}
        return self.call(actor, f"/api/cases/ZF-1/{action}", {} if body is None else body)

    def test_explicit_change_sources_are_required_and_reopen_from_http(self) -> None:
        upload = dict(
            name="supplied.txt", kind="Other", data=base64.b64encode(b"SYN text").decode()
        )
        for action, body in (("upload", upload), ("offer-handoff", dict(to="rae@example.test"))):
            code, result = self.call("sam", f"/api/cases/ZF-1/{action}", body)
            self.assertEqual(code, 400, result)
            self.assertIn("source", result["error"])
        code, result = self.call(
            "sam", "/api/cases/ZF-1/upload", {**upload, **change_metadata(self.store)}
        )
        self.assertEqual(code, 200, result)
        self.assertEqual(self.post("sam", "offer-handoff", dict(to="rae@example.test"))[0], 200)
        self.assertEqual(self.call("rae", "/api/cases/ZF-1/accept-handoff", {})[0], 400)
        stale = {**change_metadata(self.store), "handoff_version": 0}
        self.assertEqual(self.call("rae", "/api/cases/ZF-1/accept-handoff", stale)[0], 409)
        self.assertEqual(self.post("sam", "accept-handoff")[0], 403)
        code, detail = self.post("rae", "accept-handoff")
        self.assertEqual(code, 200, detail)
        reopened = self.reopen_store()
        self.addCleanup(reopened.db.close)
        case = reopened.cases["ZF-1"]
        for history, action in (
            ("document_history", "upload_document"),
            ("handoff_history", "handoff_accepted"),
        ):
            event = case[history][-1]
            self.assertEqual(event["source_version"], "fixture-1")
            audit = next(e for e in reopened.audit_entries() if e["action"] == action)
            self.assertEqual(json.loads(audit["detail"]), event)
        self.assertEqual(case["owner_code"], "RLO-02")
        self.assertTrue(reopened.verify_audit())

    def test_synthetic_app_states_sender_receiver_manager_views(self) -> None:
        with urllib.request.urlopen(self.base + "/") as response:
            self.assertEqual(response.status, 200)
        self.assertEqual(
            self.post(
                "sam",
                "offer-handoff",
                dict(
                    to="rae@example.test",
                    urgency="Urgent",
                    next_action="PRIVATE-NEXT",
                    note="PRIVATE-NOTE",
                    due_at="2026-10-16T12:00:00Z",
                ),
            )[0],
            200,
        )
        for actor in ("sam", "rae", "pam"):
            code, rows = self.call(actor, "/api/handoffs")
            self.assertEqual(code, 200)
            self.assertEqual(rows[0]["status"], "Sent")
            self.assertEqual(rows[0]["accountable_owner"], "Sam Example")
            self.assertIsNone(rows[0]["confirmed_receiver"])
        self.assertEqual(self.post("sam", "receive-handoff")[0], 403)
        self.assertEqual(self.post("rae", "receive-handoff")[1]["handoff"]["status"], "Received")
        self.assertEqual(self.post("rae", "receive-handoff")[0], 400)
        self.assertEqual(
            self.post(
                "sam",
                "escalate-handoff",
                dict(to="pam@example.test", reason="Waiting for acceptance"),
            )[1]["handoff"]["status"],
            "Escalated",
        )
        self.assertEqual(self.post("sam", "complete-handoff", {"note": "Too soon"})[0], 400)
        code, detail = self.post("rae", "accept-handoff")
        self.assertEqual((code, detail["owner"]), (200, "Rae Other"))
        self.assertEqual(detail["handoff"]["confirmed_receiver"], "Rae Other")
        self.assertEqual(self.call("sam", "/api/handoffs")[1], [])
        self.assertEqual(self.post("pam", "complete-handoff", {"note": "Wrong owner"})[0], 403)
        code, detail = self.post("rae", "complete-handoff", {"note": "Reviewed"})
        self.assertEqual((code, detail["handoff"]["status"]), (200, "Completed"))
        self.assertEqual(
            [event["status"] for event in detail["handoff_history"]],
            ["Sent", "Received", "Escalated", "Accepted", "Completed"],
        )
        self.assertTrue(self.store.verify_audit())

    def test_return_reopen_require_provenance_and_use_authenticated_authority(self) -> None:
        for action, cid, actor in (("return", "ZF-1", "sam"), ("reopen", "ZF-2", "pam")):
            path = f"/api/cases/{cid}/{action}"
            body: dict[str, object] = dict(reason="Synthetic change", to_stage="Funding check")
            self.assertEqual(self.call(actor, path, body)[0], 400)
            body.update(
                source="Synthetic report 83",
                next_action="Review evidence",
                receiving_owner="rae@example.test",
                initiating_authority={"role": "Invented authority"},
            )
            code, detail = self.call(actor, path, body)
            self.assertEqual(code, 200)
            rec = detail["returns"][-1]
            self.assertEqual(rec["initiating_authority"]["email"], f"{actor}@example.test")
            self.assertEqual(rec["receiving_owner"]["name"], "Sam Example")
            self.assertEqual(detail["owner"], "Sam Example")
        self.assertEqual(self.post("sam", "handover", {"to": "rae@example.test"})[0], 200)
        self.assertEqual(self.call("sam", "/api/cases/ZF-1")[1]["owner"], "Sam Example")
        self.assertEqual(self.post("rae", "accept-handoff")[1]["owner"], "Rae Other")

    def test_new_actions_are_denied_to_contractors_and_wrong_staff(self) -> None:
        self.post("sam", "offer-handoff", {"to": "rae@example.test"})
        for action, body in (
            ("receive-handoff", {}),
            ("accept-handoff", {}),
            ("decline-handoff", {"reason": "No"}),
            ("withdraw-handoff", {}),
            ("escalate-handoff", {"to": "pam@example.test", "reason": "No"}),
            ("complete-handoff", {"note": "No"}),
        ):
            self.assertEqual(self.post("kim", action, body)[0], 403)
            self.assertEqual(
                self.post("rex", action, body)[0],
                403 if action != "complete-handoff" else 400,
            )
        self.assertEqual(self.call("kim", "/api/handoffs")[0], 403)
        self.assertNotIn("handoff", self.call("kim", "/api/cases/ZF-1")[1])
        self.assertEqual(self.post("sam", "receive-handoff", [1, 2])[0], 400)

    def test_queue_and_detail_hold_notes_for_roles_without_need(self) -> None:
        self.post(
            "sam",
            "offer-handoff",
            dict(to="rex@example.test", note="PRIVATE-NOTE", next_action="PRIVATE-NEXT"),
        )
        for path in ("/api/handoffs", "/api/cases/ZF-1"):
            code, detail = self.call("rex", path)
            self.assertEqual(code, 200)
            self.assertNotIn("PRIVATE", json.dumps(detail))
            self.assertIn("Held for roles with a recorded need", json.dumps(detail))

    def test_rejection_withdrawal_and_escalation_permissions_over_http(self) -> None:
        for action in ("decline-handoff", "withdraw-handoff"):
            self.post("sam", "offer-handoff", {"to": "rae@example.test"})
            self.post("rae", "receive-handoff")
            self.assertEqual(
                self.post(
                    "sam",
                    "escalate-handoff",
                    {"to": "rex@example.test", "reason": "Not manager"},
                )[0],
                400,
            )
            self.assertEqual(
                self.post(
                    "pam",
                    "escalate-handoff",
                    {"to": "pam@example.test", "reason": "Manual chase"},
                )[0],
                200,
            )
            actor = "rae" if action == "decline-handoff" else "sam"
            code, detail = self.post(actor, action, {"reason": "No capacity"})
            self.assertEqual(code, 200)
            self.assertEqual(detail["owner"], "Sam Example")
            self.assertEqual(self.post("rae", "accept-handoff")[0], 400)
