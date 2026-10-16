"""Offline safety and exact-outcome contracts for the in-VNet proof runner."""

import importlib.util
import io
import json
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import MagicMock, patch

SPEC = importlib.util.spec_from_file_location(
    "private_cutover_proof", Path(__file__).parents[1] / "scripts/private-cutover-proof.py"
)
proof = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proof)


class PrivateProofTests(unittest.TestCase):
    def test_unknown_database_is_rejected_before_application_queries(self):
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [("cases",)]
        with self.assertRaisesRegex(RuntimeError, "Unrecognized database"):
            proof.preflight(db, {"cases"})
        self.assertEqual(db.execute.call_count, 1)
        self.assertIn("sys.tables", db.execute.call_args.args[0])

    def test_preflight_empty_owned_and_wrong_sentinel(self):
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = []
        self.assertFalse(proof.preflight(db, {"cases"}))
        db.execute.return_value.fetchall.return_value = [("cases",), (proof.SENTINEL,)]
        db.execute.return_value.fetchone.return_value = (proof.PROOF,)
        self.assertTrue(proof.preflight(db, {"cases"}))
        db.execute.return_value.fetchone.return_value = ("different-proof",)
        with self.assertRaises(RuntimeError):
            proof.preflight(db, {"cases"})

    def test_api_assistant_startup_tables_are_known_but_unknown_tables_still_fail(self):
        allowed = proof.allowed_tables()
        self.assertIn("assistant_tasks", allowed)
        self.assertIn("assistant_releases", allowed)
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [
            (table,) for table in allowed | {proof.SENTINEL}
        ]
        db.execute.return_value.fetchone.return_value = (proof.PROOF,)
        self.assertTrue(proof.preflight(db, allowed))
        db.reset_mock()
        db.execute.return_value.fetchall.return_value.append(("unexpected_private_table",))
        with self.assertRaises(RuntimeError):
            proof.preflight(db, allowed)
        self.assertEqual(db.execute.call_count, 1)

    def test_private_dns_rejects_vm_and_public_networks(self):
        for address in ("172.16.0.1", "20.0.0.1", "127.0.0.1"):
            with patch.object(
                proof.socket, "getaddrinfo", return_value=[(0, 0, 0, "", (address, 443))]
            ):
                with self.assertRaises(ValueError):
                    proof.private_dns("example.test")
        with patch.object(
            proof.socket, "getaddrinfo", return_value=[(0, 0, 0, "", ("10.40.4.5", 443))]
        ):
            self.assertEqual(proof.private_dns("example.test"), ["10.40.4.5"])

    def test_grant_sid_idempotence_and_input_rejection(self):
        db = MagicMock()
        client = "00112233-4455-6677-8899-aabbccddeeff"
        db.execute.return_value.fetchone.return_value = ("0x33221100554477668899aabbccddeeff",)
        for _ in range(2):
            proof.grant(db, "id-cutover-test-api", client, ("db_datareader",))
        self.assertIn("IF NOT EXISTS", db.execute.call_args_list[0].args[0])
        self.assertIn(
            "SID=0x33221100554477668899aabbccddeeff", db.execute.call_args_list[0].args[0]
        )
        for name in ("arbitrary", "id-cutover-test-api']; DROP TABLE staff;--"):
            with self.assertRaises(ValueError):
                proof.grant(db, name, client, ())
        db.execute.return_value.fetchone.return_value = ("0x00",)
        with self.assertRaisesRegex(RuntimeError, "SID mismatch"):
            proof.grant(db, "id-cutover-test-api", client, ())

    def test_fixture_is_nonempty_unbound_and_survives_seedless_reopen(self):
        from zava_forward.core.sqlstore import SqlStore

        fixture = proof.fixture()
        self.assertEqual(fixture["staff"], [])
        self.assertEqual(len(fixture["cases"]), 1)
        with tempfile.TemporaryDirectory() as directory:
            seed, db = Path(directory) / "seed.json", str(Path(directory) / "state.sqlite")
            seed.write_text(json.dumps(fixture))
            first = SqlStore(str(seed), db)
            first.db.close()
            seed.unlink()
            reopened = SqlStore(str(seed), db)
            try:
                self.assertEqual(reopened.cases[proof.CASE_ID]["reason"], proof.PROOF)
                self.assertFalse(reopened.staff)
            finally:
                reopened.db.close()

    def test_owned_partial_initialization_retains_a_seed_for_safe_retry(self):
        from zava_forward.core import mssqlstore

        def store(seed, **kwargs):
            self.assertTrue(Path(seed).exists())
            result = MagicMock()
            result.cases = {proof.CASE_ID: {"reason": proof.PROOF}}
            result.staff = {}
            return result

        with (
            patch.dict(
                "os.environ",
                {
                    "ZF_SQL_SERVER": "sql.example.test",
                    "ZF_SQL_DATABASE": "proof",
                    "ZF_SQL_CLIENT_ID": "explicit-identity",
                    "PROOF_API_CLIENT_ID": "00112233-4455-6677-8899-aabbccddeeff",
                    "PROOF_IMPORT_CLIENT_ID": "00112233-4455-6677-8899-aabbccddeeff",
                },
            ),
            patch.object(proof, "private_dns"),
            patch.object(proof, "preflight", return_value=True),
            patch.object(proof, "grant"),
            patch.object(proof, "emit"),
            patch.object(mssqlstore, "_Conn"),
            patch.object(mssqlstore, "MssqlStore", side_effect=store),
        ):
            proof.sql_probe(True)

    def test_smoke_requires_exact_codes_and_checks_forged_headers(self):
        with (
            patch.object(proof, "private_dns", return_value=["10.40.0.1"]),
            patch.object(proof, "http_status", side_effect=[200, 401, 401, 401]) as status,
            patch.object(proof, "emit"),
        ):
            proof.smoke("https://test.internal.example.azurecontainerapps.io")
            self.assertIn("X-MS-CLIENT-PRINCIPAL", status.call_args.args[1])
        with (
            patch.object(proof, "private_dns"),
            patch.object(proof, "http_status", return_value=302),
            patch.object(proof, "emit"),
        ):
            with self.assertRaises(RuntimeError):
                proof.smoke("https://test.internal.example.azurecontainerapps.io")

    def test_smoke_rejects_arbitrary_origins_before_request(self):
        for url in (
            "http://test.azurecontainerapps.io",
            "https://example.com",
            "https://test.azurecontainerapps.io/api",
            "https://user@test.azurecontainerapps.io",
        ):
            with self.subTest(url=url), patch.object(proof, "http_status") as status:
                with self.assertRaises(ValueError):
                    proof.smoke(url)
                status.assert_not_called()

    def test_error_output_does_not_include_raw_exception(self):
        with (
            patch.object(sys, "argv", ["proof", "verify"]),
            patch.object(proof, "sql_probe", side_effect=RuntimeError("secret-token")),
            patch.object(proof, "emit") as emit,
        ):
            self.assertEqual(proof.main(), 1)
            self.assertNotIn("secret-token", str(emit.call_args))

    def test_help_retains_successful_exit_without_failed_probe_record(self):
        output = io.StringIO()
        with (
            patch.object(sys, "argv", ["proof", "--help"]),
            redirect_stdout(output),
            self.assertRaises(SystemExit) as stopped,
        ):
            proof.main()
        self.assertEqual(stopped.exception.code, 0)
        self.assertIn("--direct-ingress", output.getvalue())
        self.assertNotIn('"status": "Failed"', output.getvalue())


class DirectProofTests(unittest.TestCase):
    BASE = "https://fictional.public.azurecontainerapps.io"
    SECRET = "fictional-private-session-do-not-log"

    def setUp(self):
        self.responses = {
            "/healthz": (200, ""),
            "/": (200, ""),
            "/welcome.html": (200, ""),
            "/app": (302, "https://login.microsoftonline.com/fictional/oauth2/authorize?secret=query"),
        }
        self.browser_api = 401
        self.wrong_role = 403
        self.session_status = 200
        self.requests: list[tuple[str, dict[str, str]]] = []
        self.output = io.StringIO()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.requests.append((self.path, dict(self.headers)))
                if self.path == "/api/me":
                    if self.headers.get("Cookie") or self.headers.get("Authorization") == (
                            "Bearer " + owner.SECRET):
                        code, location = owner.session_status, ""
                    else:
                        browser = "Mozilla" in self.headers.get("User-Agent", "")
                        code = owner.browser_api if browser else 401
                        location = "https://hostile.invalid/?credential=never-follow"
                elif self.path == "/api/stats":
                    code, location = owner.wrong_role, ""
                else:
                    code, location = owner.responses.get(self.path, (404, ""))
                self.send_response(code)
                if location:
                    self.send_header("Location", location)
                self.end_headers()

            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server_thread.join)
        self.addCleanup(server.shutdown)
        self.real_result = proof.http_result
        self.local = f"http://127.0.0.1:{server.server_port}"

    def result(self, url, headers=None):
        self.assertTrue(url.startswith(self.BASE + "/"), "Unvalidated redirect was requested")
        return self.real_result(self.local + url[len(self.BASE):], headers)

    def run_probe(self, **kwargs):
        with (
            redirect_stdout(self.output),
            patch.object(proof, "http_result", side_effect=self.result),
            patch.object(proof, "private_dns",
                         side_effect=AssertionError("Private DNS in direct mode")),
        ):
            proof.smoke(self.BASE, direct_ingress=True, **kwargs)

    def records(self):
        return [json.loads(line) for line in self.output.getvalue().splitlines()]

    def test_direct_strict_statuses_and_not_run_is_not_authorization_pass(self):
        self.run_probe()
        records = {row["check"]: row for row in self.records()}
        for name in ("health", "root", "welcome"):
            self.assertEqual(records[name]["http_status"], 200)
        for name in ("anonymous_api_denial", "browser_json_api_denial",
                     "malformed_bearer_denial", "forged_principal_denial"):
            self.assertEqual(records[name]["http_status"], 401)
        self.assertEqual(records["wrong_role_denial"]["status"], "Not run")
        self.assertEqual(records["browser_sign_in"]["status"], "Passed")
        self.assertNotIn("secret=query", self.output.getvalue())
        self.assertEqual(len(self.requests), 8)
        native = [headers for path, headers in self.requests if path == "/api/me"
                  and headers.get("User-Agent") == "ZavaForwardDirectProbe/1.0"]
        self.assertEqual(len(native), 1)
        self.assertEqual(native[0]["Accept"], "application/json")

    def test_browser_api302_health_redirect_and_inexact_statuses_fail(self):
        for path, code in (("/healthz", 302), ("/", 204), ("/welcome.html", 404)):
            with self.subTest(path=path):
                original = self.responses[path]
                self.responses[path] = (code, "https://hostile.invalid")
                with self.assertRaises(RuntimeError):
                    self.run_probe()
                self.responses[path] = original
        self.browser_api = 302
        with self.assertRaises(RuntimeError):
            self.run_probe()
        self.assertTrue(any(row["check"] == "browser_json_api_denial"
                            and row["status"] == "Failed" for row in self.records()))
        self.assertFalse(any("hostile" in path for path, _ in self.requests))

    def test_redirects_never_automatically_follow_and_hostile_hosts_fail(self):
        for location in (
            "https://login.microsoftonline.com.hostile.invalid/authorize",
            "https://login.microsoftonline.com@hostile.invalid/authorize",
            "https://hostile.invalid",
            "//hostile.invalid/.auth/login",
            "http://login.microsoftonline.com/authorize",
            "https://login.microsoftonline.com:444/authorize",
            "https://login.microsoftonline.com/authorize#fragment",
            "https://[malformed",
            "/app",
            "",
        ):
            with self.subTest(location=location):
                self.responses["/app"] = (302, location)
                self.requests.clear()
                with self.assertRaises(RuntimeError):
                    self.run_probe(auth_hops=2)
                self.assertEqual(len(self.requests), 8)
        self.responses["/app"] = (301, "https://login.microsoftonline.com/authorize")
        with self.assertRaises(RuntimeError):
            self.run_probe()

    def test_same_origin_auth_hops_are_opt_in_individually_checked_and_bounded(self):
        self.responses["/app"] = (302, "/.auth/login/aad?credential=not-logged")
        self.responses["/.auth/login/aad?credential=not-logged"] = (
            302, "https://login.microsoftonline.com/fictional/authorize?client_id=not-logged")
        with self.assertRaises(RuntimeError):
            self.run_probe()
        self.requests.clear()
        self.run_probe(auth_hops=1)
        self.assertEqual(len(self.requests), 9)
        self.assertEqual(self.records()[-1]["same_origin_hops"], 1)
        self.assertNotIn("not-logged", self.output.getvalue())
        self.responses["/.auth/login/aad?credential=not-logged"] = (302, "https://hostile.invalid")
        with self.assertRaises(RuntimeError):
            self.run_probe(auth_hops=5)
        self.responses["/.auth/login/aad?credential=not-logged"] = (
            302, "/.auth/login/aad?credential=not-logged")
        self.requests.clear()
        with self.assertRaises(RuntimeError):
            self.run_probe(auth_hops=2)
        self.assertEqual(len(self.requests), 10)

    def test_wrong_role_private_cookie_and_token_exact403_no_leakage(self):
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / "session.json"
            with patch.object(proof, "REPO", Path(directory) / "fictional-repository"):
                for key in ("cookie", "token"):
                    private.write_text(json.dumps({key: self.SECRET}))
                    private.chmod(0o600)
                    self.run_probe(wrong_role_session=private)
                    row = [r for r in self.records() if r["check"] == "wrong_role_denial"][-1]
                    self.assertEqual(row["status"], "Passed")
                    self.assertEqual(row["http_status"], 403)
                    self.assertTrue(any(path == "/api/stats" for path, _ in self.requests))
                for code in (200, 302, 401):
                    self.wrong_role = code
                    with self.assertRaises(RuntimeError):
                        self.run_probe(wrong_role_session=private)
                self.assertNotIn(self.SECRET, self.output.getvalue())
                self.assertNotIn(str(private), self.output.getvalue())

    def test_wrong_role_probe_requires_authenticated_session_before_role_request(self):
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / "session.json"
            private.write_text(json.dumps({"cookie": self.SECRET}))
            private.chmod(0o600)
            self.session_status = 401
            with patch.object(proof, "REPO", Path(directory) / "fictional-repository"):
                with self.assertRaisesRegex(RuntimeError, "authenticated Contractor"):
                    self.run_probe(wrong_role_session=private)
            self.assertFalse(any(path == "/api/stats" for path, _ in self.requests))
            self.assertNotIn(self.SECRET, self.output.getvalue())

    def test_real_trusted_provider_router_allows_me_and_denies_contractor_stats(self):
        import base64

        from zava_forward.api.auth import TrustedProxyProvider
        from zava_forward.api.server import App, make_handler
        from zava_forward.core.store import Store

        with tempfile.TemporaryDirectory() as directory:
            seed = Path(directory) / "seed.json"
            fixture = proof.fixture()
            fixture["staff"] = [{
                "code": "CON-FIXTURE", "name": "Synthetic Contractor",
                "email": "contractor@example.test", "role": "Contractor",
                "contractor": "Fictional Ltd", "oid": "synthetic-contractor",
            }]
            seed.write_text(json.dumps(fixture))
            store = Store(str(seed))
            provider = TrustedProxyProvider(
                store, {"ZF_ENTRA_TENANT_ID": "synthetic-tenant", "ZF_TRUSTED_PROXY": "1"})
            server = ThreadingHTTPServer(
                ("127.0.0.1", 0), make_handler(App(store, provider=provider)))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            principal = base64.b64encode(json.dumps({
                "auth_typ": "aad",
                "claims": [
                    {"typ": "roles", "val": "ZavaForward.Contractor"},
                    {"typ": "tid", "val": "synthetic-tenant"},
                    {"typ": "oid", "val": "synthetic-contractor"},
                ],
            }).encode()).decode()
            headers = {"X-MS-CLIENT-PRINCIPAL": principal}
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                self.assertEqual(self.real_result(base + "/api/me", headers)[0], 200)
                self.assertEqual(self.real_result(base + "/api/stats", headers)[0], 403)
                self.assertEqual(self.real_result(base + "/api/me")[0], 401)
                private = Path(directory) / "session.json"
                private.write_text(json.dumps({"cookie": self.SECRET}))
                private.chmod(0o600)
                fake_result = self.result

                def transport(url, request_headers=None):
                    if request_headers and request_headers.get("Cookie") == self.SECRET:
                        return self.real_result(base + url[len(self.BASE):], headers)
                    return fake_result(url, request_headers)

                with (
                    patch.object(proof, "REPO", Path(directory) / "fictional-repository"),
                    patch.object(self, "result", side_effect=transport),
                ):
                    self.run_probe(wrong_role_session=private)
                self.assertNotIn(self.SECRET, self.output.getvalue())
                self.assertNotIn("synthetic-contractor", self.output.getvalue())
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_private_session_permissions_schema_symlink_repo_and_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            private = root / "session.json"
            private.write_text(json.dumps({"cookie": self.SECRET}))
            private.chmod(0o600)
            with patch.object(proof, "REPO", root):
                with self.assertRaises(ValueError):
                    proof.session_headers(private)
            with patch.object(proof, "REPO", root / "fictional-repository"):
                private.chmod(0o644)
                with self.assertRaises(ValueError):
                    proof.session_headers(private)
                private.chmod(0o600)
                link = root / "link.json"
                link.symlink_to(private)
                with self.assertRaises(ValueError):
                    proof.session_headers(link)
                for data in ({"cookie": "bad\r\nheader"}, {"cookie": "", "token": self.SECRET},
                             {"token": ""}, ["token"], {"token": 123}):
                    private.write_text(json.dumps(data))
                    with self.assertRaises(ValueError):
                        proof.session_headers(private)

    def test_bad_options_and_session_read_errors_never_log_private_input(self):
        for arguments in (
            ["smoke", "--base-url", self.BASE, "--direct-ingress",
             "--wrong-role-session", "/nonexistent/" + self.SECRET],
            ["smoke", "--base-url", self.BASE, "--auth-hops", "1"],
            ["smoke", "--base-url", self.BASE, "--direct-ingress", "--auth-hops", "6"],
            ["verify", "--direct-ingress"],
            ["smoke", "--auth-hops", self.SECRET],
        ):
            with (
                patch.object(sys, "argv", ["proof", *arguments]),
                redirect_stdout(self.output),
            ):
                self.assertEqual(proof.main(), 1)
        self.assertNotIn(self.SECRET, self.output.getvalue())
        self.assertEqual(self.requests, [])


if __name__ == "__main__":
    unittest.main()
