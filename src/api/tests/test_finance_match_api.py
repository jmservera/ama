"""Authenticated loopback proof of the exact record-only finance criteria."""

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

import dataset
from test_finance_signoffs import STAFF, lines, person
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class FinanceMatchApi(unittest.TestCase):
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

    def test_exact_criteria_through_authenticated_finance_route(self) -> None:
        self.assertEqual(self.fin(self.a, "budget_propose", amount=100)[0], 200)
        self.assertEqual(self.fin(self.a, "budget_approve")[0], 403)
        self.assertEqual(self.fin(self.alias, "budget_approve")[0], 403)
        self.assertEqual(self.fin(self.b, "budget_approve")[0], 200)
        status, detail = self.fin(
            self.a,
            "commit_raise",
            supplier="Fiction Ltd",
            contract="SYN-C",
            work_order="SYN-W",
            measure="Loft insulation",
            amount=100,
            quantity=10,
        )
        self.assertEqual(status, 200, detail)
        self.assertEqual(self.fin(self.alias, "commit_approve", id="COM-1")[0], 403)
        self.assertEqual(self.fin(self.b, "commit_approve", id="COM-1")[0], 200)
        approved = copy.deepcopy(self.store.cases["ZF-1"]["finance"])
        grants = copy.deepcopy(self.store.cases["ZF-1"].get("grants"))
        self.assertEqual(
            self.fin(
                self.a,
                "invoice_receive",
                supplier="Fiction Ltd",
                work_order="SYN-W",
                ref="SYN-UNKNOWN",
                lines=lines(qty=1, amount=1, ms=""),
            )[0],
            200,
        )
        status, detail = self.fin(self.a, "invoice_match", id="INV-1")
        self.assertEqual(status, 200)
        self.assertEqual(detail["finance"]["invoices"][0]["exceptions"][0]["line"], 0)
        self.assertEqual(
            self.fin(
                self.b,
                "disposition",
                id="INV-1",
                decision="Accept for payment",
                note="Unknown",
            )[0],
            400,
        )
        status, queue = self.call(self.b, "/api/finance")
        self.assertEqual(status, 200)
        self.assertEqual(queue[0]["invoice"], "INV-1")
        self.assertEqual(
            self.fin(
                self.a,
                "invoice_receive",
                supplier="Fiction Ltd",
                work_order="SYN-W",
                ref="SYN-CLEAN",
                lines=lines(qty=1, amount=10),
            )[0],
            200,
        )
        self.assertEqual(self.fin(self.a, "invoice_match", id="INV-2")[0], 200)
        self.assertEqual(
            self.fin(
                self.alias,
                "disposition",
                id="INV-2",
                decision="Accept for payment",
                note="x",
            )[0],
            403,
        )
        self.assertEqual(self.fin(self.a, "hold_place", id="INV-2", reason="Query")[0], 200)
        self.assertEqual(self.fin(self.alias, "hold_release", id="INV-2", note="x")[0], 403)
        self.assertEqual(
            self.fin(
                self.b,
                "disposition",
                id="INV-2",
                decision="Keep on hold",
                note="Review",
            )[0],
            200,
        )
        self.assertEqual(
            self.fin(
                self.b,
                "disposition",
                id="INV-2",
                decision="Accept for payment",
                note="Held",
            )[0],
            400,
        )
        self.assertEqual(
            self.fin(
                self.a,
                "payment_status",
                id="INV-2",
                status="Paid outside this system",
            )[0],
            400,
        )
        reopened = SqlStore("unused-seed", self.store.db_path)
        self.addCleanup(reopened.db.close)
        held = reopened.cases["ZF-1"]["finance"]["invoices"][1]
        self.assertIsNotNone(held["hold"])
        self.assertEqual(held["disposition"], "Keep on hold")
        self.assertEqual(self.fin(self.b, "hold_release", id="INV-2", note="Resolved")[0], 200)
        self.assertEqual(
            self.fin(
                self.b,
                "disposition",
                id="INV-2",
                decision="Accept for payment",
                note="Checked",
            )[0],
            200,
        )
        self.assertEqual(
            self.fin(
                self.b,
                "payment_status",
                id="INV-2",
                status="Paid outside this system",
            )[0],
            403,
        )
        for payment in ("Awaiting payment run", "Paid outside this system"):
            self.assertEqual(self.fin(self.a, "payment_status", id="INV-2", status=payment)[0], 200)
        with reopened.lock:
            case = reopened._case("ZF-1")
            self.assertEqual(case["finance"]["budget"], approved["budget"])
            self.assertEqual(case["finance"]["commitments"], approved["commitments"])
            self.assertEqual(case.get("grants"), grants)
            self.assertEqual(
                case["finance"]["invoices"][1]["payment_status"], "Paid outside this system"
            )
        self.assertTrue(reopened.verify_audit())
