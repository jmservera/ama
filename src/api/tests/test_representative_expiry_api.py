"""HTTP representative view projection and session/request-time expiry tests (#154 C3).

Exercises both HTTP surfaces over real loopback sockets:
1. ResidentDemo (`/demo/login`, `/demo/session`, `/demo/view`, `/demo/assistant`, `/demo/agenda`)
2. Workbench case API (`/api/cases/<id>/representative-view` GET and POST)
"""

import copy
import json
import tempfile
import threading
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dataset import DATA
from zava_forward.core import controls
from zava_forward.core import resident_journey_design as rjd
from zava_forward.core import resident_showcase as rs
from zava_forward.core.resident_documents import DocumentFacts, DocumentRequest
from zava_forward.core.sqlstore import SqlStore

from test_resident_demo_api import FAKE_PASSWORD, HOST, KEY, NOW, Client, Clock, make_row
from zava_forward.api.resident_demo import app as demo
from zava_forward.api.resident_demo.agenda import Agenda
from zava_forward.api.server import App, make_handler

RESIDENT_DOC_CANARY = "RESIDENT-PRIVATE-DOCUMENT-ACTION-CANARY"
HOUSEHOLD_CANARY = "HOUSEHOLD-SAFEGUARDING-NOTE-CANARY"


class FakeGrantReader:
    def __init__(
        self,
        rows: list[rs.ShowcaseRow],
        grants: list[rs.RepresentativeShowcaseGrant],
    ) -> None:
        self.rows = {r.case_id: r for r in rows}
        self.grants = list(grants)

    def list_rows(self) -> list[rs.ShowcaseRow]:
        return list(self.rows.values())

    def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None:
        return self.rows.get(case_id)

    def list_representative_grants(self) -> list[rs.RepresentativeShowcaseGrant]:
        return list(self.grants)


class ResidentDemoRepresentativeExpiryApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = Clock()
        self.expires_at = NOW + timedelta(minutes=15)
        self.row = make_row(
            "SYN-REP-01",
            "resident.01@example.com",
            address="10 Private Resident Walk",
            postcode="NB9 9PR",
            measures=("Loft insulation", "Cavity wall"),
            documents=DocumentFacts(
                requests=(
                    DocumentRequest(
                        id="REQ-LEASE-1",
                        kind="Lease",
                        how_to_provide=RESIDENT_DOC_CANARY,
                    ),
                )
            ),
        )
        self.info_grant = rs.RepresentativeShowcaseGrant(
            case_id="SYN-REP-01",
            email="rep.info@example.com",
            representative_ref="REP-INFO-1",
            measure="Loft insulation",
            tasks=("Receive information",),
            valid_from=NOW - timedelta(hours=1),
            expires_at=self.expires_at,
        )
        self.comm_grant = rs.RepresentativeShowcaseGrant(
            case_id="SYN-REP-01",
            email="rep.comm@example.com",
            representative_ref="REP-COMM-1",
            measure="Loft insulation",
            tasks=("Receive information", "Communicate"),
            valid_from=NOW - timedelta(hours=1),
            expires_at=self.expires_at,
        )
        self.expired_grant = rs.RepresentativeShowcaseGrant(
            case_id="SYN-REP-01",
            email="rep.expired@example.com",
            representative_ref="REP-EXPIRED-1",
            measure="Loft insulation",
            tasks=("Receive information",),
            valid_from=NOW - timedelta(hours=3),
            expires_at=NOW - timedelta(seconds=1),
        )
        self.reader = FakeGrantReader(
            [self.row],
            [self.info_grant, self.comm_grant, self.expired_grant],
        )
        slot_start = NOW + timedelta(days=1)
        agenda = Agenda.create(
            Path(self.tmp.name) / "agenda.sqlite",
            [(slot_start, slot_start + timedelta(minutes=30))],
        )
        identity = rs.build_identity_map(self.reader.list_rows(), NOW)
        codec = rs.SessionCodec(KEY, NOW + timedelta(hours=6), self.clock)
        limiter = rs.LoginLimiter(clock=self.clock)
        self.demo_app = demo.ResidentDemo(
            self.reader,
            identity,
            rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
            codec,
            limiter,
            (HOST,),
            NOW + timedelta(hours=6),
            "127.0.0.1",
            0,
            self.clock,
            agenda=agenda,
            representative_grants=tuple(self.reader.list_representative_grants()),
        )
        self.server = demo.serve(self.demo_app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self._stop)

    def _stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def client(self) -> Client:
        return Client(self.demo_app.port)

    def test_task_limited_projection_scopes_view_assistant_and_agenda_isolation(self) -> None:
        rep = self.client()
        self.assertEqual(rep.login("rep.info@example.com"), 200)

        code, session_body, _ = rep.call("GET", "/demo/session")
        self.assertEqual(code, 200)
        self.assertTrue(session_body["authenticated"])
        self.assertEqual(session_body["principal_kind"], "representative")
        self.assertEqual(session_body["state"], "active")
        self.assertEqual(session_body["expires_at"], rjd.format_iso_utc(self.expires_at))
        self.assertNotIn("@example.com", json.dumps(session_body))

        code, view, _ = rep.call("GET", "/demo/view")
        self.assertEqual(code, 200)
        self.assertTrue(view["active"])
        self.assertEqual(view["journey_stages"], ["R1", "J4"])
        self.assertEqual(view["permitted_actions"], ["view_task_briefing"])
        self.assertEqual([m["measure"] for m in view["measures"]], ["Loft insulation"])
        serialized_view = json.dumps(view)
        for forbidden in (
            "Cavity wall",
            "10 Private Resident Walk",
            "NB9 9PR",
            "SYN-REP-01",
            RESIDENT_DOC_CANARY,
        ):
            self.assertNotIn(forbidden, serialized_view)

        # Allowed assistant topic ("status") sees only Loft insulation and empty grant documents.
        code, ans, _ = rep.call("POST", "/demo/assistant", {"topic": "status", "use_record": True})
        self.assertEqual(code, 200)
        self.assertNotIn("Cavity wall", json.dumps(ans))
        self.assertNotIn(RESIDENT_DOC_CANARY, json.dumps(ans))

        # Out-of-scope assistant topics and agenda writes are denied with 403.
        for forbidden_topic in ("consents", "appointments", "home", "documents"):
            code, denied, _ = rep.call(
                "POST", "/demo/assistant", {"topic": forbidden_topic, "use_record": True}
            )
            self.assertEqual(code, 403, forbidden_topic)
            self.assertEqual(denied["reason"], "task_out_of_scope")
        code, agenda_denied, _ = rep.call(
            "POST", "/demo/agenda", {"action": "list", "use_record": True}
        )
        self.assertEqual(code, 403)
        self.assertEqual(agenda_denied["reason"], "task_out_of_scope")

        # "Communicate" representative can book a callback slot without touching resident state.
        comm = self.client()
        self.assertEqual(comm.login("rep.comm@example.com"), 200)
        code, found_slots, _ = comm.call(
            "POST",
            "/demo/agenda",
            {"action": "find", "use_record": True, "earliest": "2026-10-25", "period": "any"},
        )
        self.assertEqual(code, 200)
        proposal = found_slots["proposals"][0]["proposal"]
        code, booked_body, _ = comm.call(
            "POST",
            "/demo/agenda",
            {"action": "book", "use_record": True, "proposal": proposal, "confirmed": True},
        )
        self.assertEqual(code, 200)
        self.assertEqual(len(booked_body["bookings"]), 1)

        resident = self.client()
        self.assertEqual(resident.login("resident.01@example.com"), 200)
        code, res_agenda, _ = resident.call(
            "POST", "/demo/agenda", {"action": "list", "use_record": True}
        )
        self.assertEqual(code, 200)
        self.assertEqual(res_agenda["bookings"], [])

    def test_mid_session_expiry_and_revocation_transition_open_session_and_block_actions(
        self,
    ) -> None:
        # Already-expired grant cannot sign in.
        expired_client = self.client()
        self.assertEqual(expired_client.login("rep.expired@example.com"), 401)

        # Active "Communicate" representative signs in 15 minutes before recorded expires_at.
        comm = self.client()
        self.assertEqual(comm.login("rep.comm@example.com"), 200)
        code, initial_view, _ = comm.call("GET", "/demo/view")
        self.assertEqual(code, 200)
        self.assertTrue(initial_view["active"])

        # Advance clock to exact recorded expires_at (15m < 30m HTTP session TTL).
        self.clock.now = self.expires_at.timestamp()
        expected_iso = rjd.format_iso_utc(self.expires_at)

        code, sess, _ = comm.call("GET", "/demo/session")
        self.assertEqual(code, 200)
        self.assertTrue(sess["authenticated"])
        self.assertFalse(sess["active"])
        self.assertEqual(sess["state"], "expired")
        self.assertEqual(sess["reason"], "expired")
        self.assertEqual(sess["expires_at"], expected_iso)
        self.assertEqual(sess["renewal_route"]["recorded_expires_at"], expected_iso)
        self.assertTrue(sess["renewal_route"]["non_digital_supported"])

        for method, path, payload in (
            ("GET", "/demo/view", None),
            ("POST", "/demo/assistant", {"topic": "status", "use_record": True}),
            ("POST", "/demo/agenda", {"action": "list", "use_record": True}),
            (
                "POST",
                "/demo/agenda",
                {"action": "find", "use_record": True, "earliest": "2026-10-25", "period": "any"},
            ),
        ):
            code, blocked, _ = comm.call(method, path, payload)
            self.assertEqual(code, 403, (method, path))
            self.assertEqual(blocked["state"], "expired")
            self.assertEqual(blocked["expires_at"], expected_iso)
            self.assertEqual(blocked["renewal_route"]["recorded_expires_at"], expected_iso)
            self.assertNotIn("Loft insulation", json.dumps(blocked))
            self.assertNotIn("10 Private Resident Walk", json.dumps(blocked))

        # Reset clock back to active window and verify mid-session revocation transitions to held.
        self.clock.now = NOW.timestamp()
        info = self.client()
        self.assertEqual(info.login("rep.info@example.com"), 200)
        self.reader.grants = [
            replace(self.info_grant, revoked=True, status="Revoked"),
            self.comm_grant,
        ]
        code, held_view, _ = info.call("GET", "/demo/view")
        self.assertEqual(code, 403)
        self.assertEqual(held_view["state"], "held")
        self.assertEqual(held_view["reason"], "revoked")
        self.assertEqual(held_view["expires_at"], expected_iso)
        self.assertEqual(held_view["renewal_route"]["recorded_expires_at"], expected_iso)


class CaseRepresentativeViewApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                {
                    "code": "RLO-2",
                    "name": "Rae Reviewer",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "CON-1",
                    "name": "Kim Contractor",
                    "email": "kim@example.test",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
            ]
        )
        # Ensure ZF-1 has two measures and sensitive household notes to verify redaction.
        zf1 = next(c for c in data["cases"] if c["id"] == "ZF-1")
        zf1["measures"] = ["Loft insulation", "Cavity wall"]
        zf1["contacts"].append(
            {
                "at": "2026-04-01T09:00",
                "by": "HO-1",
                "channel": "Phone",
                "outcome": HOUSEHOLD_CANARY,
                "note": HOUSEHOLD_CANARY,
            }
        )
        self.path.write_text(json.dumps(data), encoding="utf-8")
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

    def call(self, path: str, actor: str, body: object = None) -> tuple[int, Any]:
        if actor not in self.cookies:
            login_req = Request(
                self.base + "/api/login",
                json.dumps(
                    {"email": f"{actor}@example.test", "password": "synthetic-only"}
                ).encode(),
            )
            with urlopen(login_req, timeout=5) as resp:
                self.cookies[actor] = resp.headers["Set-Cookie"].split(";")[0]
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[actor], "Content-Type": "application/json"},
        )
        try:
            with urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read())
        except HTTPError as err:
            return err.code, json.loads(err.read())

    def test_case_representative_view_enforces_role_scope_and_recorded_expiry(self) -> None:
        # Contractor is denied on both existing and unknown case IDs (no existence oracle).
        for cid in ("ZF-1", "ZF-DOES-NOT-EXIST"):
            code_get, _ = self.call(
                f"/api/cases/{cid}/representative-view?representative_ref=REP-API-1", "kim"
            )
            code_post, _ = self.call(
                f"/api/cases/{cid}/representative-view",
                "kim",
                {"representative_ref": "REP-API-1", "action": "view_task_briefing"},
            )
            self.assertEqual(code_get, 403)
            self.assertEqual(code_post, 403)

        c0, _ = self.call(
            "/api/cases/ZF-1/technical",
            "pam",
            {"action": "design_submit", "note": "Synthetic design"},
        )
        self.assertEqual(c0, 200)
        with patch.object(controls, "today", return_value="2026-04-01"):
            c1, _ = self.call(
                "/api/cases/ZF-1/resident",
                "rae",
                {
                    "action": "scope_record",
                    "measure": "Loft insulation",
                    "scope": "Loft 270mm",
                    "design_version": 1,
                    "source": "SYN-SCOPE-1",
                },
            )
            c2, _ = self.call(
                "/api/cases/ZF-1/resident",
                "rae",
                {
                    "action": "safe_contact_record",
                    "safe_contact_ref": "SYN-SAFE-1",
                    "source": "SYN-SAFE-SRC",
                },
            )
            c3, _ = self.call(
                "/api/cases/ZF-1/resident",
                "rae",
                {
                    "action": "representative_record",
                    "measure": "Loft insulation",
                    "context_revision": 1,
                    "representative_ref": "REP-API-1",
                    "status": "Confirmed",
                    "tasks": ["Receive information", "Works decision"],
                    "authority_date": "2026-04-01",
                    "review_date": "2026-04-10",
                    "expires_at": "2026-04-05T14:00:00Z",
                    "safe_contact_ref": "SYN-SAFE-1",
                    "source": "SYN-AUTH-1",
                    "resident_wishes": "Loft decision support only",
                },
            )
            self.assertEqual((c1, c2, c3), (200, 200, 200))

        before_exp = datetime(2026, 4, 5, 13, 59, 59, tzinfo=UTC)
        with (
            patch.object(controls, "today", return_value="2026-04-05"),
            patch.object(rjd, "utc_now", return_value=before_exp),
        ):
            code, active_view = self.call(
                "/api/cases/ZF-1/representative-view?representative_ref=REP-API-1&session_id=S-1",
                "rae",
            )
            self.assertEqual(code, 200)
            self.assertTrue(active_view["active"])
            self.assertEqual(active_view["state"], "active")
            self.assertEqual(active_view["expires_at"], "2026-04-05T14:00:00Z")
            self.assertEqual(active_view["journey_stages"], ["R1", "J1", "J2", "J4"])
            self.assertEqual([m["measure"] for m in active_view["measures"]], ["Loft insulation"])
            self.assertNotIn("Cavity wall", json.dumps(active_view))
            self.assertNotIn(HOUSEHOLD_CANARY, json.dumps(active_view))

            ok_code, ok_act = self.call(
                "/api/cases/ZF-1/representative-view",
                "rae",
                {
                    "representative_ref": "REP-API-1",
                    "session_id": "S-1",
                    "action": "submit_measure_decision",
                    "measure": "Loft insulation",
                },
            )
            self.assertEqual(ok_code, 200)
            self.assertTrue(ok_act["allowed"])

            scope_code, scope_err = self.call(
                "/api/cases/ZF-1/representative-view",
                "rae",
                {
                    "representative_ref": "REP-API-1",
                    "session_id": "S-1",
                    "action": "submit_measure_decision",
                    "measure": "Cavity wall",
                },
            )
            self.assertEqual(scope_code, 403)
            self.assertEqual(scope_err["reason"], "task_out_of_scope")

        # Advance to exact recorded expires_at: open session S-1 transitions immediately.
        at_exp = datetime(2026, 4, 5, 14, 0, 0, tzinfo=UTC)
        with (
            patch.object(controls, "today", return_value="2026-04-05"),
            patch.object(rjd, "utc_now", return_value=at_exp),
        ):
            exp_get_code, exp_view = self.call(
                "/api/cases/ZF-1/representative-view?representative_ref=REP-API-1&session_id=S-1",
                "rae",
            )
            self.assertEqual(exp_get_code, 200)
            self.assertFalse(exp_view["active"])
            self.assertEqual(exp_view["state"], "expired")
            self.assertEqual(exp_view["expires_at"], "2026-04-05T14:00:00Z")
            self.assertEqual(
                exp_view["renewal_route"]["recorded_expires_at"], "2026-04-05T14:00:00Z"
            )
            self.assertNotIn("measures", exp_view)
            self.assertNotIn(HOUSEHOLD_CANARY, json.dumps(exp_view))

            exp_post_code, exp_post = self.call(
                "/api/cases/ZF-1/representative-view",
                "rae",
                {
                    "representative_ref": "REP-API-1",
                    "session_id": "S-1",
                    "action": "submit_measure_decision",
                    "measure": "Loft insulation",
                },
            )
            self.assertEqual(exp_post_code, 403)
            self.assertEqual(exp_post["state"], "expired")
            self.assertEqual(exp_post["expires_at"], "2026-04-05T14:00:00Z")
            self.assertEqual(
                exp_post["renewal_route"]["recorded_expires_at"], "2026-04-05T14:00:00Z"
            )


if __name__ == "__main__":
    unittest.main()
