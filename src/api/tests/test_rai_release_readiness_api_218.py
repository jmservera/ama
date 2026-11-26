"""Focused HTTP API tests for Epic #218 RAI release gating, readiness, and traceability."""

from __future__ import annotations

import copy
import importlib
import json
import os
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import dataset as _dataset
import release_support as _release_support
from zava_forward.core import assistants as _assistants
from zava_forward.core import projection, rai_control_plane
from zava_forward.core.sqlstore import SqlStore as _SqlStore

from zava_forward.api.server import App as _App
from zava_forward.api.server import make_handler as _make_handler

dataset_mod: Any = _dataset
assistants_mod: Any = _assistants
SqlStore: Any = _SqlStore
release_support: Any = _release_support
App: Any = _App
make_handler: Any = _make_handler

# GET /api/ai/report alone takes about 2.5 s unloaded, so a flat 10 s read budget fails under load.
REQUEST_TIMEOUT_S = 120


class RaiReleaseReadinessApi218Tests(unittest.TestCase):
    """Verify Epic #218 HTTP surfaces for OQ-017 rejection and separated RAI readiness."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        data = copy.deepcopy(dataset_mod.DATA)
        data["staff"] = [
            {
                "code": f"ROLE-{idx}",
                "name": f"Staff Member {idx}",
                "email": f"staff{idx}@zavanorth.example",
                "role": role,
            }
            for idx, role in enumerate(projection.STAFF_ROLES)
        ]
        seed_path = Path(self._tmp.name) / "synthetic-218.json"
        seed_path.write_text(json.dumps(data), encoding="utf-8")

        self.pm_email = str(
            next(s["email"] for s in data["staff"] if s["role"] == "Retrofit Programme Manager")
        )
        self.officer_email = str(
            next(s["email"] for s in data["staff"] if s["role"] == "Resident Liaison Officer")
        )
        self._env = patch.dict(
            os.environ,
            {"ZF_ASSIST_RELEASE_APPROVERS": self.pm_email},
            clear=False,
        )
        self._env.start()
        self.addCleanup(self._env.stop)

        self.store = SqlStore(str(seed_path), str(seed_path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.password = "SYN-rai-218"
        self.app = App(self.store, self.password)
        self.addCleanup(self.app.assistants.stop)
        release_support.install(self.store, self.store.ai, cls="constructed-fixture")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()
        self.addCleanup(self._shutdown_server)
        self._cookies: dict[str, str] = {}
        self.pm_headers: dict[str, str] = {"X-User": self.pm_email}
        self.officer_headers: dict[str, str] = {"X-User": self.officer_email}

    def _shutdown_server(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self._thread.join(timeout=5)

    def _raw_request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, Any], None]:
        email = (headers or {}).get("X-User")
        req_headers: dict[str, str] = {"Content-Type": "application/json"}
        if email:
            if email not in self._cookies:
                login_req = Request(
                    self.base + "/api/login",
                    data=json.dumps({"email": email, "password": self.password}).encode("utf-8"),
                    headers=req_headers,
                    method="POST",
                )
                with urlopen(login_req, timeout=REQUEST_TIMEOUT_S) as resp:
                    self._cookies[email] = resp.headers["Set-Cookie"].split(";")[0]
            req_headers["Cookie"] = self._cookies[email]
        payload_bytes = json.dumps(body).encode("utf-8") if body is not None else None
        req = Request(
            self.base + path,
            data=payload_bytes,
            headers=req_headers,
            method=method,
        )
        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
                return resp.status, json.loads(resp.read()), None
        except HTTPError as error:
            return error.code, json.loads(error.read()), None

    def test_request_budget_is_the_read_timeout_against_a_slow_server(self) -> None:
        delay_s = 0.8

        class Slow(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 http.server API
                time.sleep(delay_s)
                body = b'{"slow": true}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass  # the client timed out on purpose; keep the traceback out of the gate log

            def log_message(self, *_args: Any) -> None:
                return

        slow = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
        thread = threading.Thread(target=slow.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(slow.server_close)
        self.addCleanup(slow.shutdown)
        self.base = f"http://127.0.0.1:{slow.server_port}"

        self.assertGreater(REQUEST_TIMEOUT_S, delay_s)
        status, payload, _ = self._raw_request("GET", "/slow")
        self.assertEqual((status, payload), (200, {"slow": True}))
        with patch(f"{__name__}.REQUEST_TIMEOUT_S", delay_s / 4), self.assertRaises(TimeoutError):
            self._raw_request("GET", "/slow")

    def test_live_release_post_without_named_approval_is_rejected_with_oq017_and_audited(
        self,
    ) -> None:
        binding = assistants_mod.runtime_binding("funding-evidence", self.store.ai)
        missing_approver = release_support.fixture(
            "funding-evidence",
            binding,
            cls="actual",
            expires="2099-01-01T00:00:00Z",
        )
        missing_approver.pop("approved_by", None)

        status, body, _ = self._raw_request(
            "POST",
            "/api/assistants/releases",
            body=missing_approver,
            headers=self.pm_headers,
        )
        self.assertEqual(status, 403, body)
        self.assertIn("OQ-017", body["error"])

        placeholder_id = release_support.fixture(
            "funding-evidence",
            binding,
            cls="actual",
            expires="2099-01-01T00:00:00Z",
            named_approval_id="example-approval-id",
        )
        status2, body2, _ = self._raw_request(
            "POST",
            "/api/assistants/releases",
            body=placeholder_id,
            headers=self.pm_headers,
        )
        self.assertEqual(status2, 403, body2)
        self.assertIn("OQ-017", body2["error"])

        live_flag_without_approval = release_support.fixture(
            "funding-evidence",
            binding,
            cls="constructed-fixture",
            expires="2099-01-01T00:00:00Z",
            live=True,
        )
        status3, body3, _ = self._raw_request(
            "POST",
            "/api/assistants/releases",
            body=live_flag_without_approval,
            headers=self.pm_headers,
        )
        self.assertEqual(status3, 403, body3)
        self.assertIn("OQ-017", body3["error"])

        rejected_audits = [
            entry
            for entry in self.store.audit_entries()
            if entry["action"] == rai_control_plane.AUDIT_ACTION_REJECTED
        ]
        self.assertEqual(len(rejected_audits), 3)
        self.assertIs(self.store.verify_audit(), True)

        valid_actual = release_support.fixture(
            "funding-evidence",
            dict(binding, endpoint="https://zava-live-openai.invalid"),
            cls="actual",
            expires="2099-01-01T00:00:00Z",
        )
        ok_status, ok_body, _ = self._raw_request(
            "POST",
            "/api/assistants/releases",
            body=valid_actual,
            headers=self.pm_headers,
        )
        self.assertEqual(ok_status, 201, ok_body)
        self.assertEqual(ok_body["status"], "active")

    def test_readiness_endpoints_expose_separated_rai_exercise_acceptance_and_real_ai_gate(
        self,
    ) -> None:
        status_a, assistants_body, _ = self._raw_request(
            "GET",
            "/api/assistants",
            headers=self.pm_headers,
        )
        self.assertEqual(status_a, 200, assistants_body)
        self.assertEqual(assistants_body["rai_exercise_acceptance"]["status"], "passed")
        self.assertEqual(assistants_body["real_ai_delivery_gate"]["status"], "blocked")
        self.assertNotEqual(
            assistants_body["rai_exercise_acceptance"]["section"],
            assistants_body["real_ai_delivery_gate"]["section"],
        )

        status_g, gov_body, _ = self._raw_request(
            "GET",
            "/api/governance",
            headers=self.pm_headers,
        )
        self.assertEqual(status_g, 200, gov_body)
        self.assertEqual(gov_body["rai_exercise_acceptance"]["status"], "passed")
        self.assertEqual(gov_body["real_ai_delivery_gate"]["status"], "blocked")

        gov_fixtures: Any = importlib.import_module("test_governance")
        query = urlencode({"assessment": json.dumps(gov_fixtures.ASSESSMENT)})
        status_ga, gov_assessed_body, _ = self._raw_request(
            "GET",
            f"/api/governance?{query}",
            headers=self.pm_headers,
        )
        self.assertEqual(status_ga, 200, gov_assessed_body)
        self.assertEqual(gov_assessed_body["rai_exercise_acceptance"]["status"], "passed")
        self.assertEqual(gov_assessed_body["real_ai_delivery_gate"]["status"], "blocked")

        status_r, report_body, _ = self._raw_request(
            "GET",
            "/api/ai/report",
            headers=self.pm_headers,
        )
        self.assertEqual(status_r, 200, report_body)
        self.assertEqual(
            set(report_body),
            {"evaluation", "chat_evaluation", "live", "registry", "consumption"},
        )
        self.assertEqual(
            report_body["live"]["rai_exercise_acceptance"]["status"],
            "passed",
        )
        self.assertEqual(
            report_body["live"]["real_ai_delivery_gate"]["status"],
            "blocked",
        )

        denied_gov, _, _ = self._raw_request(
            "GET",
            "/api/governance",
            headers=self.officer_headers,
        )
        self.assertEqual(denied_gov, 403)
        denied_rep, _, _ = self._raw_request(
            "GET",
            "/api/ai/report",
            headers=self.officer_headers,
        )
        self.assertEqual(denied_rep, 403)

    def test_traceability_targets_import_and_resolve_across_core_and_api_suites(self) -> None:
        for row in rai_control_plane.requirement_traceability():
            for target in row["acceptance_checks"]:
                file_part, _, symbol_part = str(target).partition("::")
                mod_name = Path(file_part).stem
                cls_name, _, method_name = symbol_part.partition(".")
                with self.subTest(requirement_id=row["id"], target=target):
                    mod = importlib.import_module(mod_name)
                    cls_obj = getattr(mod, cls_name, None)
                    self.assertIsNotNone(
                        cls_obj,
                        f"Missing {cls_name} in {mod_name}",
                    )
                    method_obj = getattr(cls_obj, method_name, None)
                    self.assertTrue(
                        callable(method_obj),
                        f"Missing callable {cls_name}.{method_name}",
                    )
        self.assertIs(rai_control_plane.verify_traceability_targets()["all_resolved"], True)

    def test_ai_report_rejects_drifted_or_legacy_unapproved_sql_release_rows_read_only(
        self,
    ) -> None:
        from zava_forward.core import assistant_release as _rel

        rel: Any = _rel
        self.store.ai.endpoint = "https://zava-live-openai.invalid"
        release_support.install(
            self.store,
            self.store.ai,
            model="gpt-4o-2024-11-20",
            cls="actual",
        )
        ok_status, ok_report, _ = self._raw_request(
            "GET",
            "/api/ai/report",
            headers=self.pm_headers,
        )
        self.assertEqual(ok_status, 200, ok_report)
        self.assertIs(
            ok_report["live"]["real_ai_delivery_gate"]["checks"][
                "oq017_named_live_releases_recorded"
            ]["passed"],
            True,
        )

        cap = "funding-evidence"
        binding = assistants_mod.runtime_binding(cap, self.store.ai)
        drifted = release_support.fixture(
            cap,
            dict(binding, prompt_version="stale-prompt-v0"),
            model="gpt-4o-2024-11-20",
            cls="actual",
        )
        with self.app.assistants.transaction() as db:
            db.execute(
                "UPDATE assistant_releases SET body=? WHERE id=?",
                (rel.canonical(drifted), f"fx-{cap}"),
            )

        drift_status, drift_report, _ = self._raw_request(
            "GET",
            "/api/ai/report",
            headers=self.pm_headers,
        )
        self.assertEqual(drift_status, 200, drift_report)
        self.assertEqual(
            drift_report["live"]["rai_exercise_acceptance"]["status"],
            "passed",
        )
        self.assertIs(
            drift_report["live"]["real_ai_delivery_gate"]["checks"][
                "oq017_named_live_releases_recorded"
            ]["passed"],
            False,
        )
        self.assertIn(
            cap,
            drift_report["live"]["real_ai_delivery_gate"]["checks"][
                "oq017_named_live_releases_recorded"
            ]["unapproved_live_tasks"],
        )
        with self.app.assistants.transaction() as db:
            stored_status = db.execute(
                "SELECT status FROM assistant_releases WHERE id=?",
                (f"fx-{cap}",),
            ).fetchone()[0]
        self.assertEqual(stored_status, "active")


if __name__ == "__main__":
    unittest.main()
