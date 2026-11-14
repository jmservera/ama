"""Raw safeguarding items never leave the store on case detail, for any role."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from zava_forward.core import projection
from zava_forward.core.store import Store

from role_matrix_fixture import ROLES, MatrixServer, SqlStoreCase, build
from zava_forward.api.server import App, make_handler

CANARIES = ("SYN-SG-NOTE", "SYN-SG-OWNER", "SYN-SG-CLOSED", "2026-10-15T12:00Z")


def seed(data: dict[str, Any]) -> dict[str, Any]:
    data["cases"][0]["safeguarding_items"] = [
        dict(
            referred_at="2026-10-15T12:00Z",
            response_due_at="2026-10-17",
            owner=dict(name="SYN-SG-OWNER", role="Safeguarding lead"),
            note="SYN-SG-NOTE",
        ),
        dict(closed=True, note="SYN-SG-CLOSED", owner="SYN-SG-OWNER"),
    ]
    return data


def leaks(payload: str) -> list[str]:
    return [c for c in CANARIES if c in payload]


class DetailOverHttp(MatrixServer):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(seed(build())))
        cls.store = Store(str(p))
        app_factory: Any = App
        app = app_factory(cls.store, "zf-test")
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    def test_no_role_receives_raw_items_or_notes(self) -> None:
        case_id = self.store.cases and next(iter(self.store.cases))
        for i, role in enumerate(ROLES):
            if role == projection.CONTRACTOR:
                continue
            code, body = self.call(self.session(f"u{i}@example.test"), f"/api/cases/{case_id}")
            self.assertEqual(code, 200, role)
            detail = json.loads(body)
            self.assertNotIn("safeguarding_items", detail, role)
            self.assertNotIn("SYN-SG-NOTE", body, role)
            self.assertNotIn("SYN-SG-CLOSED", body, role)
            clocks = detail["work"]["safeguarding_clocks"]
            if projection.can_see_reason({"role": role}):
                self.assertEqual([c["owner"] for c in clocks], ["SYN-SG-OWNER"], role)
            else:
                self.assertEqual(clocks, [], role)
                self.assertEqual(leaks(body), [], role)


class DetailOnSqlStore(SqlStoreCase):
    def setUp(self) -> None:
        super().setUp()
        self.store.cases[next(iter(self.store.cases))].update(seed(dict(cases=[{}]))["cases"][0])

    def test_detail_matrix(self) -> None:
        case_id = next(iter(self.store.cases))
        for role, user in self.people.items():
            if role == projection.CONTRACTOR:
                continue
            detail = self.store.detail(case_id, user)
            text = json.dumps(detail)
            self.assertNotIn("safeguarding_items", detail, role)
            self.assertNotIn("SYN-SG-NOTE", text, role)
            if not projection.can_see_reason(user):
                self.assertEqual(leaks(text), [], role)


if __name__ == "__main__":
    unittest.main()
