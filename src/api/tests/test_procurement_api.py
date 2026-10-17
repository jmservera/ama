"""Exact #90 HTTP controls using only temporary fictional source bytes."""

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

from dataset import DATA, RESIDENT_BINDINGS, supplied_contract_fixture, supplied_resident_fixture
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api import server


class ProcurementApi(unittest.TestCase):
    sql = True

    def make_store(self, path: Path) -> Any:
        factory: Any = SqlStore if self.sql else Store
        return (
            factory(str(path), str(path.with_suffix(".sqlite"))) if self.sql else factory(str(path))
        )

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        for case in data["cases"]:
            supplied_resident_fixture(case)
        data["cases"][1]["contractor"]["name"] = "Other Ltd"
        data["staff"].extend(
            [
                dict(
                    code=code,
                    name=name,
                    email=email,
                    role="Contractor",
                    contractor=contractor,
                )
                for code, name, email, contractor in (
                    ("CON-1", "Kim Fiction", "kim@example.test", "Test Ltd"),
                    ("CON-2", "Kai Fiction", "kai@example.test", "Other Ltd"),
                )
            ]
        )
        self.manager = data["staff"][1]
        self.path.write_text(json.dumps(data))
        self.store = self.make_store(self.path)
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        self.pid = self.store.create_package(
            self.manager, "Synthetic package", "2026-01-01", "2099-12-31", "Loft", "SYN"
        )
        self.details = supplied_contract_fixture(self.store, self.pid, self.manager)
        self.other_details = supplied_contract_fixture(
            self.store, self.pid, self.manager, "Other Ltd"
        )
        app_factory: Any = server.App
        handler_factory: Any = server.make_handler
        self.app = app_factory(self.store, "synthetic-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, path: str, body: object = None, actor: str = "pam") -> tuple[int, Any]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-password")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            None if body is None else json.dumps(body).encode(),
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def capacity(self, contractor: str = "Test Ltd") -> dict[str, Any]:
        return dict(
            contractor=contractor,
            offered=9,
            committed=1,
            evidence="SYN accepted commitment",
            details=self.details if contractor == "Test Ltd" else self.other_details,
        )

    def issue(self, cid: str = "ZF-1") -> dict[str, Any]:
        return dict(package=self.pid, case_id=cid, resident_bindings=RESIDENT_BINDINGS)

    def test_capacity_http_exact_threshold_and_source_inputs(self) -> None:
        path = f"/api/packages/{self.pid}/capacity"
        self.assertEqual(self.call(path, dict(self.capacity(), details=None))[0], 400)
        self.assertEqual(self.call(path, self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 400)
        self.assertEqual(
            self.call(
                "/api/workorders/WO-0001/appointment", dict(outcome="Booked", date="2100-01-01")
            )[0],
            400,
        )
        self.assertEqual(self.call("/api/cases/ZF-3/advance", {})[0], 400)

    def test_contractors_own_orders_only_and_all_writes_denied(self) -> None:
        path = f"/api/packages/{self.pid}/capacity"
        for contractor, cid in (("Test Ltd", "ZF-1"), ("Other Ltd", "ZF-2")):
            self.assertEqual(self.call(path, self.capacity(contractor))[0], 200)
            self.assertEqual(self.call("/api/workorders", self.issue(cid))[0], 200)
        for actor, own, foreign in (("kim", "ZF-1", "ZF-2"), ("kai", "ZF-2", "ZF-1")):
            code, rows = self.call("/api/workorders", actor=actor)
            self.assertEqual(code, 200)
            self.assertEqual([row["case_id"] for row in rows], [own])
            self.assertEqual(self.call(f"/api/workorders?case={foreign}", actor=actor), (200, []))
            self.assertEqual(self.call("/api/packages", actor=actor)[0], 403)
            for route, body in [
                ("/api/workorders", self.issue()),
                ("/api/packages", dict(name="SYN")),
                (path, self.capacity()),
                (f"/api/packages/{self.pid}/rescope", dict(scope="SYN", reason="SYN")),
            ] + [
                (f"/api/workorders/WO-0001/{action}", {})
                for action in ("reissue", "appointment", "complete", "correct", "withdraw")
            ]:
                self.assertEqual(self.call(route, body, actor)[0], 403, (actor, route))
            with self.assertRaises(PermissionError):
                self.store.list_packages(self.store.staff[f"{actor}@example.test"])

    def test_lifecycle_http_has_issuer_for_every_change(self) -> None:
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 200)
        route = "/api/workorders/WO-0001/"
        for action, body in (
            ("appointment", dict(outcome="Booked", date="2099-01-01")),
            ("appointment", dict(outcome="No access")),
            ("appointment", dict(outcome="Booked", date="2099-01-02")),
            ("reissue", dict(scope="Loft", reason="SYN", resident_bindings=RESIDENT_BINDINGS)),
            ("complete", dict(note="SYN")),
            ("correct", dict(reason="SYN", resident_bindings=RESIDENT_BINDINGS)),
            ("withdraw", dict(reason="SYN")),
        ):
            self.assertEqual(self.call(route + action, body)[0], 200, action)
        versions = self.call("/api/workorders")[1][0]["versions"]
        self.assertEqual([row["version"] for row in versions], list(range(1, 9)))
        self.assertTrue(all(row["issuer_email"] == self.manager["email"] for row in versions))
        self.assertEqual(versions[0]["appointments"], [])
        self.assertTrue(self.store.verify_audit())


class JsonProcurementApi(ProcurementApi):
    sql = False
