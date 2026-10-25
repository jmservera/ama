"""HTTP authorization and isolation for the synthetic resident preview (real local server)."""

import http.client
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import resident_preview as rp
from zava_forward.core.synthetic.resident_preview_fixture import build

from zava_forward.api.resident_preview import __main__ as entry
from zava_forward.api.resident_preview.app import ResidentPreview, serve

CANARY = "SYN-CANARY"
UNAVAILABLE = (
    "/resident/messages",
    "/resident/uploads",
    "/resident/downloads",
    "/resident/appointments/respond",
    "/resident/consent",
    "/resident/ai",
)
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


class Live:
    def __init__(self, store: Any, fixture: Path, subject: str) -> None:
        self.app = ResidentPreview(store, fixture, subject, "127.0.0.1", 0)
        self.server = serve(self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.app.port

    def call(
        self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def json(self, path: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any]]:
        status, _, body = self.call("GET", path, headers)
        return status, json.loads(body)

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)


class ResidentHttp(unittest.TestCase):
    tmp: tempfile.TemporaryDirectory[str]
    root: Path
    grants: Path
    store: Any
    work: Any
    servers: dict[str, Live]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory(prefix="ama444-http-")
        cls.root = Path(cls.tmp.name) / "fixture"
        build(cls.root)
        cls.grants = cls.root / "grants.json"
        cls.store, cls.work = rp.open_store(cls.root / "dataset.json")
        cls.servers = {}

    @classmethod
    def tearDownClass(cls) -> None:
        for live in cls.servers.values():
            live.stop()
        cls.work.cleanup()
        cls.tmp.cleanup()

    def live(self, subject: str) -> Live:
        if subject not in self.servers:
            self.servers[subject] = Live(self.store, self.grants, subject)
        return self.servers[subject]

    def test_health_pages_and_security_headers(self) -> None:
        live = self.live("SYN-RES-A")
        status, body = live.json("/healthz")
        self.assertEqual((status, body["status"], body["synthetic"]), (200, "ok", True))
        for path in ("/", "/index.html", "/resident.css", "/resident.js"):
            status, headers, content = live.call("GET", path)
            self.assertEqual(status, 200, path)
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
            self.assertNotIn(CANARY.encode(), content)
        page = live.call("GET", "/")[2].decode()
        self.assertIn("Synthetic preview - not a live resident service", page)
        self.assertNotIn("<script>", page.replace('<script src="/resident.js"></script>', ""))

    def test_server_owned_identity_each_process_shows_only_its_own_case(self) -> None:
        a = self.live("SYN-RES-A").json("/resident/view")[1]
        b = self.live("SYN-RES-B").json("/resident/view")[1]
        self.assertEqual(a["home"]["address"], "1 Synthetic Row")
        self.assertEqual(b["home"]["address"], "2 Synthetic Row")
        self.assertEqual(len(a["appointments"]["confirmed"]["items"]), 1)
        self.assertEqual(len(b["appointments"]["confirmed"]["items"]), 0)
        for view in (a, b):
            self.assertNotIn(CANARY, json.dumps(view))

    def test_claimed_identity_is_ignored_everywhere(self) -> None:
        live = self.live("SYN-RES-A")
        expected = live.json("/resident/view")[1]
        claims = {
            "X-Subject": "SYN-RES-B",
            "X-Forwarded-User": "SYN-RES-B",
            "Authorization": "Bearer SYN-RES-B",
            "Cookie": "subject=SYN-RES-B; case=SYN-C2",
            "X-Case-Id": "SYN-C2",
        }
        for path in (
            "/resident/view?subject=SYN-RES-B&case=SYN-C2&case_id=SYN-C2",
            "/resident/view?as=SYN-REP-B",
            "/resident/view#SYN-C2",
        ):
            status, body = live.json(path, claims)
            self.assertEqual(status, 200, path)
            self.assertEqual(body, expected, path)
        self.assertEqual(live.json("/resident/SYN-C2/view", claims)[0], 404)

    def test_host_header_must_be_loopback_with_the_bound_port(self) -> None:
        live = self.live("SYN-RES-A")
        for host in ("evil.example", f"localhost:{live.port + 1}", "127.0.0.1", ""):
            status, _, _ = live.call("GET", "/resident/view", {"Host": host})
            self.assertEqual(status, 403, host)
        status, _, _ = live.call("GET", "/resident/view", {"Host": f"localhost:{live.port}"})
        self.assertEqual(status, 200)

    def test_staff_routes_do_not_exist(self) -> None:
        live = self.live("SYN-RES-A")
        for path in (
            "/api/cases/SYN-C1/resident",
            "/api/cases/SYN-C1",
            "/api/cases",
            "/api/me",
            "/api/chat",
            "/staff",
            "/resident/cases/SYN-C1",
            "/index.html/../server.py",
        ):
            for method in METHODS:
                status, _, body = live.call(method, path)
                self.assertIn(status, (404, 405), (method, path))
                self.assertNotIn(CANARY.encode(), body)

    def test_unavailable_features_are_server_denied_for_every_method(self) -> None:
        live = self.live("SYN-RES-A")
        for path in UNAVAILABLE:
            for method in (*METHODS, "OPTIONS"):
                status, _, body = live.call(method, path, body=b"x" if method != "GET" else None)
                self.assertEqual(status, 403, (method, path))
                self.assertIn(b"not available", body)

    def test_writes_are_refused_and_store_unchanged(self) -> None:
        live = self.live("SYN-RES-A")
        before = json.dumps(self.store.data, sort_keys=True)
        for path in ("/", "/healthz", "/resident/view", "/resident/about"):
            for method in ("POST", "PUT", "PATCH", "DELETE"):
                status, _, _ = live.call(method, path, body=b'{"status":"Accepted"}')
                self.assertEqual(status, 405, (method, path))
        self.assertEqual(before, json.dumps(self.store.data, sort_keys=True))
        self.assertFalse(
            Path(self.store.live_path).exists() and Path(self.store.audit_path).exists()
        )

    def test_denied_subjects_get_403_and_no_data(self) -> None:
        for subject, code in (
            ("SYN-RES-EXPIRED", "expired"),
            ("SYN-RES-REVOKED", "revoked"),
            ("SYN-RES-AMBIG", "ambiguous"),
            ("SYN-RES-NOGRANT", "no_grant"),
        ):
            live = self.live(subject)
            status, body = live.json("/resident/view")
            self.assertEqual(status, 403, code)
            self.assertEqual(body["error"], "You cannot see this page.")
            self.assertNotIn("home", body)
            self.assertNotIn(code, json.dumps(body))
            self.assertEqual(live.json("/healthz")[0], 200)

    def test_revocation_and_expiry_take_effect_on_the_next_request(self) -> None:
        live = self.live("SYN-RES-A")
        original = self.grants.read_text()
        try:
            self.assertEqual(live.json("/resident/view")[0], 200)
            data = json.loads(original)
            data["grants"][0]["revoked"] = True
            self.grants.write_text(json.dumps(data))
            self.assertEqual(live.json("/resident/view")[0], 403)
            data["grants"][0]["revoked"] = False
            data["grants"][0]["valid_to"] = "2026-06-01T00:00:00+00:00"
            self.grants.write_text(json.dumps(data))
            self.assertEqual(live.json("/resident/view")[0], 403)
            self.grants.write_text("{not json")
            self.assertEqual(live.json("/resident/view")[0], 403)
        finally:
            self.grants.write_text(original)
        self.assertEqual(live.json("/resident/view")[0], 200)

    def test_representative_and_wrong_authority(self) -> None:
        status, view = self.live("SYN-REP-B").json("/resident/view")
        self.assertEqual((status, view["viewer"]["kind"]), (200, "representative"))
        self.assertIn("appointments", view)
        status, view = self.live("SYN-REP-WRONG").json("/resident/view")
        self.assertEqual(status, 200)
        self.assertNotIn("appointments", view)

    def test_about_lists_limitations_without_data(self) -> None:
        status, body = self.live("SYN-RES-A").json("/resident/about")
        self.assertEqual(status, 200)
        self.assertTrue(any("Loopback only" in x for x in body["limitations"]))
        self.assertNotIn(CANARY, json.dumps(body))

    def test_every_response_body_is_canary_free(self) -> None:
        for subject in ("SYN-RES-A", "SYN-RES-B", "SYN-REP-B", "SYN-REP-WRONG"):
            live = self.live(subject)
            for path in ("/", "/resident.js", "/resident.css", "/resident/view", "/resident/about"):
                self.assertNotIn(CANARY.encode(), live.call("GET", path)[2], (subject, path))

    def test_resident_module_does_not_load_the_staff_server(self) -> None:
        code = (
            "import sys; import zava_forward.api.resident_preview.app as a; "
            "staff = ('zava_forward.api.server', 'zava_forward.api.auth'); "
            "print(any(m.startswith(staff) for m in sys.modules))"
        )
        out = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, check=True
        )
        self.assertEqual(out.stdout.strip(), "False")


class CommandLine(unittest.TestCase):
    def test_refuses_unsafe_configuration(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ama444-cli-") as tmp:
            root = Path(tmp) / "fixture"
            build(root)
            base = ["--data-dir", str(root), "--subject", "SYN-RES-A"]
            saved = dict(os.environ)
            try:
                for key in [
                    k for k in os.environ if k.upper().startswith(rp.FORBIDDEN_ENV_PREFIXES)
                ]:
                    del os.environ[key]
                self.assertEqual(entry.main([*base, "--host", "0.0.0.0"]), 2)
                self.assertEqual(entry.main([*base, "--host", "::"]), 2)
                self.assertEqual(entry.main(["--data-dir", str(root), "--subject", "SYN-NOPE"]), 2)
                self.assertEqual(entry.main([*base, "--data-dir", str(Path(tmp) / "missing")]), 2)
                os.environ["ZF_DATA"] = "/tmp/anything"
                self.assertEqual(entry.main(base), 2)
                self.assertEqual(entry.main(["--build-fixture", str(Path(tmp) / "again")]), 2)
            finally:
                os.environ.clear()
                os.environ.update(saved)


if __name__ == "__main__":
    unittest.main()
