"""Loopback checks for the versioned home case API and its separated screen."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from building_fixture import fixture, open_store

from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"


class HomeCaseApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        data = fixture()
        data["schemes"] = [{"id": "SCH-1", "name": "Fictional scheme", "source": "SYN-SCHEME"}]
        data["staff"].append(
            {
                "code": "CON-1",
                "email": "provider@example.test",
                "name": "Synthetic Provider",
                "role": "Contractor",
                "contractor": "Test Ltd",
            }
        )
        self.store = open_store(self.tmp.name, True, data)
        app_type: Any = App
        self.app = app_type(self.store, "synthetic-only")
        handler: Any = make_handler
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
    ) -> tuple[int, Any, Any]:
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Cookie": cookie, "X-ZF-CSRF": "1"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read()), response.headers
        except HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}"), {}

    def login(self, email: str) -> str:
        code, _, headers = self.call(
            "/api/login", body={"email": email, "password": "synthetic-only"}
        )
        self.assertEqual(code, 200)
        return str(headers["Set-Cookie"]).split(";")[0]

    def test_view_separates_home_and_building_and_denies_unauthorised(self) -> None:
        self.assertEqual(self.call("/api/cases/ZF-2/home-case")[0], 401)
        pam = self.login("pam@example.test")
        code, view, _ = self.call("/api/cases/ZF-2/home-case", pam)
        self.assertEqual(code, 200)
        self.assertEqual(view["version"], 0)
        self.assertEqual(view["links"]["building_id"], "SYN-B1")
        self.assertNotIn("homes", view["building"])
        self.assertIn("does not transfer", view["notice"])
        self.assertEqual(view["home"]["decision"]["status"], "Accepted")
        self.assertEqual(self.call("/api/cases/NOPE/home-case", pam)[0], 404)
        self.assertEqual(self.call("/api/cases/ZF-2/extra/home-case", pam)[0], 404)
        provider = self.login("provider@example.test")
        self.assertEqual(self.call("/api/cases/ZF-2/home-case", provider)[0], 403)
        self.assertEqual(
            self.call("/api/cases/ZF-2/home-case-version", provider, {"expected_version": 0})[0],
            403,
        )

    def test_version_recorded_through_http_and_retained(self) -> None:
        pam = self.login("pam@example.test")
        meta = {
            "expected_version": 0,
            "source": "SYN-CASE-REVIEW",
            "source_version": "1",
            "reason": "Check links before ordering",
            "scheme_id": "SCH-1",
        }
        code, view, _ = self.call("/api/cases/ZF-2/home-case-version", pam, meta)
        self.assertEqual(code, 200)
        self.assertEqual(view["version"], 1)
        self.assertEqual(view["links"]["scheme_id"], "SCH-1")
        self.assertEqual(self.call("/api/cases/ZF-2/home-case-version", pam, meta)[0], 409)
        self.assertEqual(
            self.call("/api/cases/ZF-2/home-case-version", pam, {"reason": "x"})[0], 400
        )
        other = self.call("/api/cases/ZF-3/home-case", pam)[1]
        self.assertEqual(other["version"], 0)
        self.assertEqual(other["links"]["scheme_id"], None)
        _, again, _ = self.call("/api/cases/ZF-2/home-case", pam)
        self.assertEqual([v["version"] for v in again["versions"]], [1])

    def test_screen_is_wired_with_manual_path(self) -> None:
        script = (WEB / "app.js").read_text()
        self.assertIn("#/case-home/", script)
        self.assertIn("/home-case`", script)
        self.assertIn("This home only", script)
        self.assertIn("Shared at building level", script)
        self.assertIn("Use the case and building screens instead", script)
        self.assertIn("This home's share of shared cost", script)
        self.assertNotIn("JSON.stringify(x)", script)
