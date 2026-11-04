"""Loopback proof that GET /api/finance/exposure serves the read-only pause signal (#99)."""

import copy
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import date
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest import mock

import dataset
from test_finance_signoffs import STAFF, person
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class FinanceExposureApi(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "seed.json"
        data = copy.deepcopy(dataset.DATA)
        self.a = person("PM-A", "Retrofit Programme Manager", oid="synthetic-a")
        self.b = person("PM-B", "Retrofit Programme Manager", oid="synthetic-b")
        self.alias = person("PM-ALIAS", "Retrofit Programme Manager", oid="synthetic-a")
        data["staff"] = [*copy.deepcopy(STAFF), self.a, self.b, self.alias]
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(App(self.store, "synthetic-finance-test"))
        )
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()

        def shutdown() -> None:
            self.httpd.shutdown()
            self.httpd.server_close()
            thread.join(timeout=5)

        self.addCleanup(shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}
        with urllib.request.urlopen(self.base + "/healthz") as response:
            self.assertEqual(response.status, 200)

    def call(self, user: dict[str, Any], path: str, body: object = None) -> tuple[int, Any]:
        email = user["email"]
        if email not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(dict(email=email, password="synthetic-finance-test")).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[email] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[email]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def fin(self, user: dict[str, Any], action: str, **body: Any) -> tuple[int, Any]:
        return self.call(user, "/api/cases/ZF-1/finance", dict(action=action, **body))

    def limits(self, committed_cap: float) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "approved-limits.json"
        path.write_text(
            json.dumps(
                dict(
                    approval=dict(
                        approver="Synthetic Board",
                        role="Board",
                        approved_on=date.today().isoformat(),
                        evidence_ref="SYN-MINUTE",
                        restart_owner="Synthetic Board",
                    ),
                    envelope=dict(amount=committed_cap, currency="GBP", period="test year"),
                    tolerances=dict(safety=dict(maximum=0, unit="count")),
                )
            )
        )
        patch = mock.patch.dict(os.environ, {"ZF_APPROVED_LIMITS": str(path)})
        patch.start()
        self.addCleanup(patch.stop)

    def test_no_approved_limits_is_held_not_within(self) -> None:
        with mock.patch.dict(os.environ, {"ZF_APPROVED_LIMITS": "/nonexistent/limits.json"}):
            status, body = self.call(self.a, "/api/finance/exposure")
        self.assertEqual(status, 200)
        self.assertEqual((body["status"], body["signal"]), ("Held", "Pause for human decision"))

    def test_breach_signal_for_a_human_and_unchanged_records(self) -> None:
        self.assertEqual(self.fin(self.a, "budget_propose", amount=100)[0], 200)
        self.assertEqual(self.fin(self.b, "budget_approve")[0], 200)
        raised = self.fin(
            self.a,
            "commit_raise",
            supplier="Fiction Ltd",
            contract="SYN-C",
            work_order="SYN-W",
            measure="Loft insulation",
            amount=100,
            quantity=10,
        )
        self.assertEqual(raised[0], 200, raised[1])
        before = copy.deepcopy(self.store.cases["ZF-1"]["finance"])
        self.limits(50)
        status, body = self.call(self.a, "/api/finance/exposure")
        self.assertEqual(status, 200)
        self.assertEqual((body["status"], body["signal"]), ("Breach", "Pause for human decision"))
        self.assertIn("does not approve", body["notice"])
        self.assertEqual(self.store.cases["ZF-1"]["finance"], before)

    def test_within_limits_gives_no_pause_but_unknown_tolerance_still_pauses(self) -> None:
        self.limits(1000)
        status, body = self.call(self.a, "/api/finance/exposure")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "Unknown")
        self.assertEqual(body["signal"], "Pause for human decision")

    def test_roles_without_finance_view_are_refused(self) -> None:
        contractor = next(s for s in self.store.data["staff"] if s["role"] == "Contractor")
        self.assertEqual(self.call(contractor, "/api/finance/exposure")[0], 403)
