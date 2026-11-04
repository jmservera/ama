"""Shared typed fixtures for role-scoped API tests. Not a test module."""

import copy
import json
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any, ClassVar

from dataset import DATA
from zava_forward.core import projection
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler

REASON = "SEEDED-REASON-dementia-and-hearing-loss"
PHONE = "01999 888777"
RESIDENT = "Quentin Residentname"
ROLES = list(projection.STAFF_ROLES) + [projection.CONTRACTOR]


def build() -> dict[str, Any]:
    d: dict[str, Any] = copy.deepcopy(DATA)
    d["staff"] = [
        dict(code=f"U{i}", name=f"User {i}", email=f"u{i}@example.test", role=r)
        for i, r in enumerate(ROLES)
    ]
    d["staff"][-1]["contractor"] = "Test Ltd"
    d["staff"].append(
        dict(
            code="U99",
            name="Other Contractor",
            email="other@example.test",
            role=projection.CONTRACTOR,
            contractor="Other Ltd",
        )
    )
    for c in d["cases"]:
        c["owner_code"] = "U1"
        c["owner"] = "User 1"
    c = d["cases"][0]
    c["resident"].update(
        adjustment=REASON,
        priority_support=True,
        phone=PHONE,
        name=RESIDENT,
        email="q@example.test",
    )
    c["contacts"].append(
        dict(
            at="2026-01-01T10:00",
            purpose="Update",
            channel="Phone",
            direction="Outbound",
            outcome="Spoke",
            note="private note",
            by="User 1",
        )
    )
    c["appointments"].append(
        dict(
            type="Survey",
            date="2099-01-01",
            slot="AM",
            outcome="Booked",
            note="private appointment note",
            who="Test Ltd",
            person="Kim Builder",
        )
    )
    d["cases"][1]["contractor"]["name"] = "Other Ltd"
    return d


class MatrixServer(unittest.TestCase):
    """Real HTTP server over a fictional seeded store, one per test class."""

    tmp: ClassVar[tempfile.TemporaryDirectory[str]]
    store: ClassVar[Any]
    httpd: ClassVar[ThreadingHTTPServer]
    base: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(build()))
        cls.store = Store(str(p))
        app_factory: Any = App
        app = app_factory(cls.store, "zf-test")
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    def session(self, email: str) -> str:
        body = json.dumps({"email": email, "password": "zf-test"}).encode()
        req = urllib.request.Request(self.base + "/api/login", body)
        return str(urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0])

    def call(self, ck: str, path: str, body: Any = None) -> tuple[int, str]:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data, headers={"Cookie": ck})
        try:
            with urllib.request.urlopen(req) as r:
                return int(r.status), str(r.read().decode())
        except urllib.error.HTTPError as e:
            return int(e.code), str(e.read().decode())


class SqlStoreCase(unittest.TestCase):
    """Fictional staff and a SQLite store opened over the shared dataset."""

    people: dict[str, dict[str, str]]
    pm: dict[str, str]
    store: Any

    def setUp(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="register-test-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        data: dict[str, Any] = copy.deepcopy(DATA)
        self.people = {}
        for i, role in enumerate(projection.STAFF_ROLES + ("Contractor", "Unknown")):
            self.people[role] = dict(
                code=f"ROLE-{i}", name=f"Human {i}", email=f"human{i}@example.test", role=role
            )
        data["staff"] = list(self.people.values())
        self.pm = self.people["Retrofit Programme Manager"]
        seed = root / "seed.json"
        seed.write_text(json.dumps(data))
        self.store = SqlStore(str(seed), str(root / "cases.sqlite"))
        self.addCleanup(self.store.db.close)
