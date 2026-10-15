"""Real loopback HTTP checks using wholly fictional building/home fixtures."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from building_fixture import fixture, hold, open_store

from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"


class BuildingHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        data = fixture()
        data["staff"].extend(
            [
                {
                    "code": "CON-1",
                    "email": "provider@example.test",
                    "name": "Synthetic Provider",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
                {
                    "code": "UNKNOWN",
                    "email": "unknown@example.test",
                    "name": "Synthetic Unknown",
                    "role": "Mystery",
                },
            ]
        )
        self.store = open_store(self.tmp.name, True, data)
        app_type: Any = App
        handler: Any = make_handler
        self.app = app_type(self.store, "synthetic-only")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler(self.app))
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.store.db.close()
        self.tmp.cleanup()

    def call(
        self, path: str, cookie: str = "", body: dict[str, Any] | None = None
    ) -> tuple[int, bytes, str]:
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={
                "Content-Type": "application/json",
                "Cookie": cookie,
                "X-ZF-CSRF": "1",
            },
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, response.read(), response.headers.get("Set-Cookie", "")
        except HTTPError as exc:
            return exc.code, exc.read(), ""

    def login(self, email: str) -> str:
        code, _, cookie = self.call(
            "/api/login", body={"email": email, "password": "synthetic-only"}
        )
        self.assertEqual(code, 200)
        return cookie.split(";")[0]

    def test_local_app_and_bidirectional_navigation(self) -> None:
        self.assertEqual(self.call("/healthz")[0], 200)
        self.assertEqual(self.call("/app")[0], 200)
        self.assertEqual(self.call("/app.js")[0], 200)
        cookie = self.login("pam@example.test")
        code, raw, _ = self.call("/api/buildings/SYN-B1", cookie)
        self.assertEqual(code, 200)
        building = json.loads(raw)
        self.assertEqual(building["costs"][0]["amount_gbp"], "12000.00")
        self.assertEqual({h["id"] for h in building["homes"]}, {"ZF-2", "ZF-3"})
        for home in building["homes"]:
            code, raw, _ = self.call(f"/api/cases/{home['id']}", cookie)
            self.assertEqual(code, 200)
            self.assertEqual(json.loads(raw)["building_id"], building["id"])
            self.assertIn("cost_allocation", json.loads(raw))
        source = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("#/building/${encodeURIComponent(c.building_id)}", source)
        self.assertIn("#/case/${encodeURIComponent(c.id)}", source)
        self.assertIn("Shared systems", source)
        self.assertIn("Shared building costs", source)
        self.assertTrue(callable(self.app.assistants.invoke))

    def test_api_role_projection_has_no_sibling_evidence_or_unauthorized_amounts(self) -> None:
        for email, status in (
            ("sam@example.test", 200),
            ("pam@example.test", 200),
            ("provider@example.test", 403),
            ("unknown@example.test", 403),
        ):
            with self.subTest(email=email):
                cookie = self.login(email)
                code, raw, _ = self.call("/api/buildings/SYN-B1", cookie)
                self.assertEqual(code, status)
                self.assertNotIn(b"SIBLING-EVIDENCE", raw)
                self.assertNotIn(b"SYN-QA-SIBLING", raw)
                self.assertNotIn(b"6000.00", raw)
                if email != "pam@example.test":
                    self.assertNotIn(b"12000.00", raw)
                    _, home, _ = self.call("/api/cases/ZF-2", cookie)
                    self.assertNotIn(b"cost_allocation", home)
                    self.assertNotIn(b"6000.00", home)
        self.assertEqual(self.call("/api/buildings/SYN-B1")[0], 401)
        cookie = self.login("pam@example.test")
        self.assertEqual(self.call("/api/buildings/missing", cookie)[0], 404)
        self.assertEqual(self.call("/api/buildings/SYN-B1/extra", cookie)[0], 404)

    def test_shared_hold_blocks_advance_and_retains_ai_and_safety_intake(self) -> None:
        self.store.data["buildings"][0]["holds"].append(hold())
        self.store.save()
        cookie = self.login("pam@example.test")
        code, raw, _ = self.call("/api/cases/ZF-2/advance", cookie, {})
        self.assertEqual(code, 409)
        self.assertIn(b"Building SYN-B1", raw)
        self.assertEqual(self.store.cases["ZF-2"]["stage"], "Final checks before ordering")
        self.assertEqual(self.call("/api/cases/ZF-3/advance", cookie, {})[0], 200)
        code, raw, _ = self.call("/api/assistants", cookie)
        self.assertEqual(code, 200)
        self.assertIn(b"proposal", raw.lower())
        self.assertEqual(
            self.call("/api/cases/ZF-2/call", cookie, {"outcome": "Safety referral"})[0], 200
        )
