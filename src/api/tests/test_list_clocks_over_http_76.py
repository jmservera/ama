"""Issue #76: list rows and detail carry hazard and safeguarding clocks and a named owner."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from zava_forward.core import projection
from zava_forward.core.store import Store

from role_matrix_fixture import ROLES, MatrixServer, build
from zava_forward.api.server import App, make_handler


def seed(data: dict[str, Any]) -> dict[str, Any]:
    case = data["cases"][0]
    case["hazards"] = [
        dict(
            category="Damp and mould",
            priority="Emergency",
            aware_at="2026-10-15T06:00:00Z",
            owner="SYN-HZ-OWNER",
        )
    ]
    case["safeguarding_items"] = [
        dict(
            referred_at="2026-10-15T12:00Z",
            response_due_at="2026-10-17",
            owner=dict(name="SYN-SG-OWNER", role="Safeguarding lead"),
        )
    ]
    return data


class ListClocksOverHttp(MatrixServer):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        path = Path(cls.tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(seed(build())))
        cls.store = Store(str(path))
        app_factory: Any = App
        cls.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(app_factory(cls.store, "zf-test"))
        )
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    def test_list_row_clocks_show_clock_and_named_owner_for_visible_roles(self) -> None:
        case_id = next(iter(self.store.cases))
        checked = 0
        for i, role in enumerate(ROLES):
            session = self.session(f"u{i}@example.test")
            code, body = self.call(session, "/api/cases")
            self.assertEqual(code, 200, role)
            rows = [r for r in json.loads(body)["items"] if r["id"] == case_id]
            if not rows:
                continue
            row = rows[0]
            checked += 1
            work = row.get("work") or {}
            if not projection.can_see_reason({"role": role}):
                self.assertEqual(work.get("safeguarding_clocks", []), [], role)
                continue
            (hazard,) = work["hazard_clocks"]
            self.assertTrue(hazard["owner_named"], role)
            self.assertEqual(hazard["owner"], "SYN-HZ-OWNER", role)
            self.assertIsInstance(hazard["elapsed_hours"], int, role)
            self.assertIn("hours elapsed", hazard["clock_text"], role)
            (safeguarding,) = work["safeguarding_clocks"]
            self.assertTrue(safeguarding["owner_named"], role)
            self.assertEqual(safeguarding["owner"], "SYN-SG-OWNER", role)
            self.assertEqual(safeguarding["response_state"], "Overdue", role)
            self.assertEqual(safeguarding["response_due_at"], "2026-10-17", role)
            code, detail_body = self.call(session, f"/api/cases/{case_id}")
            self.assertEqual(code, 200, role)
            detail_work = json.loads(detail_body)["work"]
            self.assertEqual(detail_work["safeguarding_clocks"][0]["owner"], "SYN-SG-OWNER", role)
            self.assertEqual(detail_work["hazard_clocks"][0]["owner"], "SYN-HZ-OWNER", role)
        self.assertGreaterEqual(checked, 1)


if __name__ == "__main__":
    unittest.main()
