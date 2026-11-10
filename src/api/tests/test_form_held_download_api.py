"""Served Held draft download of the existing core export; synthetic, default OFF."""

import hashlib
import json
import os
import unittest
import urllib.error
import urllib.request
from typing import Any
from unittest.mock import patch

from tests import test_form_staging_api as staging
from zava_forward.core import form_export

from zava_forward.api import server

ON = {"ZF_FORM_HELD_DOWNLOAD": "synthetic-demo-only", "ZF_DEPLOYMENT_PROFILE": "demo"}
FILENAME = "held-form-draft-export.json"


class HeldDownload(unittest.TestCase):
    setUp = staging.FormApi.setUp
    shutdown = staging.FormApi.shutdown
    call = staging.FormApi.call
    working_review = staging.FormApi.working_review

    def prepare(self) -> tuple[Any, str]:
        draft, request = self.working_review()
        self.assertEqual(self.call("pam", "/api/cases/ZF-1/form-review", request)[0], 201)
        return draft, f"/api/cases/ZF-1/form-review/{draft['draft_id']}/held-export"

    def fetch(self, actor: str, path: str, method: str = "GET") -> tuple[int, Any, bytes]:
        self.call(actor, "/api/me")
        request = urllib.request.Request(
            self.base + path,
            headers={"Cookie": self.cookies[actor]},
            method=method,
            data=b"{}" if method == "POST" else None,
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.headers, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.headers, error.read()

    def state(self) -> str:
        with self.store.lock:
            return json.dumps(
                [self.store.data, self.store.cases.get("ZF-1"), self.store.audit_log_length()]
                if hasattr(self.store, "audit_log_length")
                else [self.store.data, self.store.cases.get("ZF-1")],
                sort_keys=True,
                default=str,
            )

    def test_default_off_and_each_guard_condition_alone_serve_nothing(self) -> None:
        _, path = self.prepare()
        variants = [
            {},
            {"ZF_FORM_HELD_DOWNLOAD": "synthetic-demo-only"},
            {"ZF_DEPLOYMENT_PROFILE": "demo"},
            {**ON, "ZF_FORM_HELD_DOWNLOAD": "yes"},
            {**ON, "ZF_DEPLOYMENT_PROFILE": "production"},
        ]
        for env in variants:
            with self.subTest(env=env), patch.dict(os.environ, env, clear=False):
                for key in ON:
                    if key not in env:
                        os.environ.pop(key, None)
                code, headers, body = self.fetch("pam", path)
                self.assertEqual(code, 404, body)
                self.assertNotIn("attachment", headers.get("Content-Disposition", ""))
                self.assertNotIn(b"content_sha256", body)
                view = self.call("pam", "/api/cases/ZF-1/form-review")[1]
                self.assertNotIn("held_download_enabled", view)
        self.assertFalse(server.held_download_enabled("trusted-proxy", ON))
        self.assertTrue(server.held_download_enabled("password", ON))

    def test_served_body_equals_core_export_with_safe_headers(self) -> None:
        draft, path = self.prepare()
        with (
            patch.dict(os.environ, ON),
            patch.object(self.store.ai, "_chat", side_effect=AssertionError("No inference")),
        ):
            before = self.state()
            code, headers, body = self.fetch("pam", path)
            again = self.fetch("pam", path)
            self.assertEqual(self.state(), before)
            view = self.call("pam", "/api/cases/ZF-1/form-review")[1]
        self.assertEqual(code, 200, body)
        direct = form_export.draft_export(
            self.store, self.store.staff["pam@example.test"], "ZF-1", draft["draft_id"]
        )
        served = json.loads(body)
        self.assertEqual(served, direct)
        self.assertEqual(served["content_sha256"], direct["content_sha256"])
        self.assertEqual(again[2], body)
        self.assertEqual(
            (served["status"], served["reviewed"], served["submission"], served["eligibility"]),
            ("Held", False, "Not submitted", "Not assessed"),
        )
        self.assertEqual(served["history"][0]["reviewer"], "pam@example.test")
        self.assertEqual(headers["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(headers["Content-Disposition"], f'attachment; filename="{FILENAME}"')
        self.assertEqual(headers["Cache-Control"], "private, no-store")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(int(headers["Content-Length"]), len(body))
        self.assertNotIn(draft["draft_id"], headers["Content-Disposition"])
        self.assertTrue(view["held_download_enabled"])
        self.assertTrue(self.store.verify_audit())

    def test_unauthorised_revoked_and_unknown_requests_get_no_artifact(self) -> None:
        draft, path = self.prepare()
        did = draft["draft_id"]
        with patch.dict(os.environ, ON):
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(self.base + path)
            self.assertEqual(caught.exception.code, 401)
            for actor in ("sam", "kim"):
                code, headers, body = self.fetch(actor, path)
                self.assertEqual(code, 403, actor)
                self.assertNotIn("attachment", headers.get("Content-Disposition", ""))
                self.assertNotIn(b"history", body)
            for bad in (
                f"/api/cases/ZF-2/form-review/{did}/held-export",
                "/api/cases/NOPE/form-review/" + did + "/held-export",
                "/api/cases/ZF-1/form-review/NOPE/held-export",
                "/api/cases/ZF-1/form-review/%2e%2e/held-export",
            ):
                code, headers, body = self.fetch("pam", bad)
                self.assertIn(code, (400, 403, 404), bad)
                self.assertNotIn("attachment", headers.get("Content-Disposition", ""), bad)
                self.assertNotIn(b"content_sha256", body, bad)
            for odd in (
                path + "/extra",
                path.replace("held-export", "held-exports"),
                path.replace("held-export", "")[:-1],
            ):
                code, headers, body = self.fetch("pam", odd)
                self.assertNotEqual(code, 200, odd)
                self.assertNotIn("attachment", headers.get("Content-Disposition", ""), odd)
            for method in ("POST",):
                code, headers, body = self.fetch("pam", path, method)
                self.assertNotEqual(code, 200)
                self.assertNotIn("attachment", headers.get("Content-Disposition", ""))
            before = self.state()
            self.assertEqual(self.fetch("pam", path)[0], 200)
            staff = self.store.staff["pam@example.test"]
            original = staff["role"]
            staff["role"] = "Contractor"
            try:
                code, headers, body = self.fetch("pam", path)
                self.assertIn(code, (401, 403))
                self.assertNotIn(b"content_sha256", body)
            finally:
                staff["role"] = original
            self.assertEqual(self.state(), before)

    def test_unavailable_working_evidence_is_a_non_success_without_attachment(self) -> None:
        draft, path = self.prepare()
        with patch.dict(os.environ, ON):
            with self.store.lock:
                self.store._case("ZF-1")["documents"][0]["scan"]["status"] = "infected"
                self.store.save()
            code, headers, body = self.fetch("pam", path)
            view = self.call("pam", "/api/cases/ZF-1/form-review")[1]
        self.assertEqual(code, 409, body)
        self.assertNotIn("Content-Disposition", headers)
        self.assertNotIn(b"content_sha256", body)
        self.assertIn("unavailable", json.loads(body)["error"].lower())
        self.assertEqual(view["drafts"][0]["status"], "Unavailable")

    def test_each_request_rechecks_current_state_not_the_screen_version(self) -> None:
        draft, request = self.working_review()
        path = f"/api/cases/ZF-1/form-review/{draft['draft_id']}/held-export"
        with patch.dict(os.environ, ON):
            self.assertEqual(self.call("pam", "/api/cases/ZF-1/form-review", request)[0], 201)
            shown = self.call("pam", "/api/cases/ZF-1/form-review")[1]["drafts"][0]["input_version"]
            second = dict(action="diagnose", draft_id=draft["draft_id"], expected_version=shown)
            self.assertEqual(self.call("pam", "/api/cases/ZF-1/form-review", second)[0], 201)
            code, _, body = self.fetch("pam", path)
        served = json.loads(body)
        self.assertEqual(code, 200)
        self.assertGreater(served["input_version"], shown)
        expected = hashlib.sha256(
            json.dumps(
                {k: served[k] for k in form_export.BODY_KEYS}, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        self.assertEqual(served["content_sha256"], expected)


if __name__ == "__main__":
    unittest.main()
