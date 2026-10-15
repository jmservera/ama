"""Running local app exercise with synthetic resident decisions and authority."""

import copy
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
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
        for actor in ("rex", "kim"):
            text = json.dumps(self.call("/api/cases/ZF-1", actor)[1])
            for canary in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SAFE-CANARY"):
                self.assertNotIn(canary, text)
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)
