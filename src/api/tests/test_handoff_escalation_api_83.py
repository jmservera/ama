"""Focused HTTP API tests for Issue #83 BG-010 handoff visibility and escalation routes."""

import copy
import csv
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

import dataset as _dataset
from tests.test_mvp import DATA as _MVP_DATA
from zava_forward.core import change_provenance, projection
from zava_forward.core.sqlstore import SqlStore as _SqlStore

from zava_forward.api.server import App as _App
from zava_forward.api.server import make_handler as _make_handler

MVP_DATA: dict[str, Any] = _MVP_DATA
CHANGE_METADATA: Any = _dataset.change_metadata
SQL_STORE_CLS: Any = _SqlStore
APP_CLS: Any = _App
MAKE_HANDLER: Any = _make_handler

APPROVED_POLICY: dict[str, Any] = {
    "status": "Approved",
    "owner": "Pam Lead",
    "policy_id": "BG-010-v1",
    "acceptance_hours": 24,
    "urgent_acceptance_hours": 4,
    "escalation_role": "Retrofit Programme Manager",
}


class HandoffEscalationApi83Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data: dict[str, Any] = copy.deepcopy(MVP_DATA)
        data["as_of"] = "2026-10-18"
        data["handoff_policy"] = copy.deepcopy(APPROVED_POLICY)
        data["staff"].extend(
            [
                {
                    "code": "RLO-02",
                    "name": "Rae Other",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "RC-01",
                    "name": "Rex Coordinator",
                    "email": "rex@example.test",
                    "role": "Retrofit Coordinator",
                },
                {
                    "code": "RC-02",
                    "name": "Rory Coordinator",
                    "email": "rory@example.test",
                    "role": "Retrofit Coordinator",
                },
                {
                    "code": "PSO-01",
                    "name": "Pia Support",
                    "email": "pso@example.test",
                    "role": "Programme Support Officer",
                },
                {
                    "code": "QI-01",
                    "name": "Quinn Inspector",
                    "email": "quinn@example.test",
                    "role": "Quality Inspector",
                },
                {
                    "code": "CON-01",
                    "name": "Kim Builder",
                    "email": "kim@example.test",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
            ]
        )
        data["cases"][0]["stage"] = "Survey booked"
        data["cases"][0]["resident"]["name"] = "PRIVATE-RESIDENT"
        data["cases"][0]["home"]["address"] = "PRIVATE-ADDRESS"
        data["cases"][1]["stage"] = "Survey booked"
        path = Path(self.tmp.name) / "seed.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.store: Any = SQL_STORE_CLS(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app: Any = APP_CLS(self.store, "synthetic-test-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), MAKE_HANDLER(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self._shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def _shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def _cookie(self, actor: str) -> str:
        if actor not in self.cookies:
            req = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    {"email": f"{actor}@example.test", "password": "synthetic-test-password"}
                ).encode(),
            )
            with urllib.request.urlopen(req) as resp:
                self.cookies[actor] = resp.headers["Set-Cookie"].split(";")[0]
        return self.cookies[actor]

    def call_raw(self, actor: str, path: str, body: object = None) -> tuple[int, str]:
        req = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self._cookie(actor)},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, resp.read().decode("utf-8")
        except urllib.error.HTTPError as err:
            return err.code, err.read().decode("utf-8")

    def call(self, actor: str, path: str, body: object = None) -> tuple[int, Any]:
        code, raw = self.call_raw(actor, path, body)
        return code, json.loads(raw)

    def _offer_aged(
        self,
        actor: str,
        case_id: str,
        to_email: str,
        offered_at: str,
        *,
        urgency: str = "Routine",
        receive_actor: str | None = None,
    ) -> None:
        payload = {
            **CHANGE_METADATA(self.store, case_id),
            "to": to_email,
            "urgency": urgency,
            "note": "PRIVATE-NOTE",
            "next_action": "PRIVATE-NEXT",
        }
        code, _ = self.call(actor, f"/api/cases/{case_id}/offer-handoff", payload)
        self.assertEqual(code, 200)
        if receive_actor is not None:
            code, _ = self.call(receive_actor, f"/api/cases/{case_id}/receive-handoff", {})
            self.assertEqual(code, 200)
        sender_user = self.store.staff[f"{actor}@example.test"]
        with change_provenance.controlled(self.store, sender_user, case_id) as (c, who):
            c["handoff"]["offered_at"] = offered_at
            self.store._save_workflow(who, "test_age_handoff", case_id, offered_at)

    def test_unowned_and_escalated_routes_enforce_role_scope_validation_and_redaction(
        self,
    ) -> None:
        self._offer_aged(
            "sam",
            "ZF-1",
            "rex@example.test",
            "2026-10-15T08:00:00+00:00",
            receive_actor="rex",
        )
        self._offer_aged(
            "sam",
            "ZF-2",
            "rex@example.test",
            "2026-10-16T10:00:00+00:00",
        )
        query = "?as_of=2026-10-16T16:00:00Z"

        # Contractor is refused on all handoff routes.
        for route in ("/api/handoffs/unowned", "/api/handoffs/escalated"):
            self.assertEqual(self.call("kim", route)[0], 403)
            for bad in ("0", "-2", "abc", "nan", "inf", "1000000"):
                self.assertEqual(
                    self.call("sam", f"{route}?max_age_hours={bad}")[0], 400, (route, bad)
                )
            self.assertEqual(self.call("sam", f"{route}?as_of=2026-10-16T16:00:00")[0], 400, route)

        # Destination-role peer Rory sees both unowned handoffs overdue-first with notes held.
        code, rory_unowned = self.call("rory", f"/api/handoffs/unowned{query}")
        self.assertEqual(code, 200)
        self.assertEqual([r["case_id"] for r in rory_unowned], ["ZF-1", "ZF-2"])
        self.assertEqual(rory_unowned[0]["escalation_status"], "Overdue - escalation required")
        self.assertEqual(rory_unowned[0]["escalation_target"], "Pam Lead")
        self.assertEqual(rory_unowned[0]["accountable_owner"], "Sam Example")
        self.assertEqual(rory_unowned[0]["note"], projection.NOTE_HELD)
        self.assertEqual(rory_unowned[0]["next_action"], projection.NOTE_HELD)
        for canary in ("PRIVATE-RESIDENT", "PRIVATE-ADDRESS", "PRIVATE-NOTE", "PRIVATE-NEXT"):
            self.assertNotIn(canary, json.dumps(rory_unowned))

        # Unrelated Quality Inspector sees empty queues.
        self.assertEqual(self.call("quinn", f"/api/handoffs/unowned{query}"), (200, []))
        self.assertEqual(self.call("quinn", f"/api/handoffs/escalated{query}"), (200, []))

        # Escalated queue surfaces overdue ZF-1 to sender, receiver, role peer, PSO, and PM.
        for viewer in ("sam", "rex", "rory", "pso", "pam"):
            code, esc_rows = self.call(viewer, f"/api/handoffs/escalated{query}")
            self.assertEqual(code, 200)
            self.assertEqual([r["case_id"] for r in esc_rows], ["ZF-1"])

    def test_escalate_overdue_post_enforces_manager_gate_first_sweeps_and_preserves_csv_parity(
        self,
    ) -> None:
        self._offer_aged(
            "sam",
            "ZF-1",
            "rex@example.test",
            "2026-10-15T08:00:00+00:00",
        )
        self._offer_aged(
            "sam",
            "ZF-2",
            "rex@example.test",
            "2026-10-17T06:00:00+00:00",
            urgency="Urgent",
            receive_actor="rex",
        )

        # Non-managers receive 403 even when max_age_hours is invalid (role gate runs first).
        for actor in ("sam", "rex", "quinn", "kim"):
            code, _ = self.call(actor, "/api/handoffs/escalate-overdue", {"max_age_hours": -5})
            self.assertEqual(code, 403, actor)

        # Invalid payloads from a manager return 400.
        for bad_body in (
            {"max_age_hours": True},
            {"max_age_hours": 0},
            {"max_age_hours": "nan"},
            {"as_of": "2026-10-17T12:00:00"},
            {"as_of": 123},
        ):
            code, _ = self.call("pam", "/api/handoffs/escalate-overdue", bad_body)
            self.assertEqual(code, 400, bad_body)

        # PSO executes sweep; custom reason is held in PSO response and visible to PM on case card.
        code, swept = self.call(
            "pso",
            "/api/handoffs/escalate-overdue",
            {"as_of": "2026-10-17T12:00:00Z", "reason": "PRIVATE-SWEEP-REASON"},
        )
        self.assertEqual(code, 200)
        self.assertEqual(swept["escalated_case_ids"], ["ZF-1", "ZF-2"])
        self.assertEqual(swept["items"][0]["answer_note"], projection.NOTE_HELD)
        self.assertNotIn("PRIVATE-SWEEP-REASON", json.dumps(swept))

        code, detail = self.call("pam", "/api/cases/ZF-1")
        self.assertEqual(code, 200)
        self.assertEqual(detail["owner_code"], "RLO-01")
        self.assertEqual(detail["handoff"]["state"], "Escalated")
        self.assertEqual(detail["handoff"]["escalation_owner"], "Pam Lead")
        self.assertEqual(detail["handoff"]["answer_note"], "PRIVATE-SWEEP-REASON")

        # Repeat sweep is idempotent.
        code, again = self.call(
            "pam", "/api/handoffs/escalate-overdue", {"as_of": "2026-10-17T12:00:00Z"}
        )
        self.assertEqual(
            (code, again["escalated_count"], again["already_escalated_count"]), (200, 0, 2)
        )

        # 13-column /api/handoffs/unaccepted and .csv remain schema-compatible.
        code_json, json_rows = self.call("pam", "/api/handoffs/unaccepted")
        code_csv, csv_raw = self.call_raw("pam", "/api/handoffs/unaccepted.csv")
        self.assertEqual((code_json, code_csv), (200, 200))
        parsed_csv = list(csv.DictReader(io.StringIO(csv_raw)))
        self.assertEqual(len(parsed_csv), 2)
        self.assertEqual(len(parsed_csv[0]), 13)
        self.assertEqual(len(json_rows[0]), 13)
        self.assertTrue(all(r["escalated"] is True for r in json_rows))

    def test_manager_card_and_waiting_queues_agree_for_third_party_offer(self) -> None:
        self._offer_aged("sam", "ZF-1", "rex@example.test", "2026-10-15T08:00:00+00:00")
        code, card = self.call("pam", "/api/cases/ZF-1")
        self.assertEqual(code, 200)
        self.assertEqual(card["handoff"]["state"], "Offered")
        for route in ("/api/handoffs", "/api/handoffs/unaccepted", "/api/handoffs/unowned"):
            code, rows = self.call("pam", route)
            with self.subTest(route=route):
                self.assertEqual(code, 200)
                (row,) = [r for r in rows if r["case_id"] == "ZF-1"]
                self.assertEqual(row["proposed_receiver"], "Rex Coordinator")
                self.assertEqual(row["chase_owner"], card["handoff"]["from_name"])
        code, rows = self.call("quinn", "/api/handoffs/unaccepted")
        self.assertEqual((code, rows), (200, []))

    def test_offer_without_timezone_stays_listed_with_unknown_age(self) -> None:
        self._offer_aged("sam", "ZF-1", "rex@example.test", "2026-10-15T08:00")
        code, rows = self.call("pam", "/api/handoffs/unaccepted")
        self.assertEqual(code, 200)
        (row,) = [r for r in rows if r["case_id"] == "ZF-1"]
        self.assertIsNone(row["age_hours"])


if __name__ == "__main__":
    unittest.main()
