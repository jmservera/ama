"""Served Held draft download of the existing core export; synthetic, default OFF."""

import copy
import hashlib
import json
import os
import unittest
import urllib.error
import urllib.request
from typing import Any
from unittest.mock import patch

from dataset import change_metadata
from zava_forward.core import form_export

import test_form_staging_api as staging

ON = {"ZF_FORM_HELD_DOWNLOAD": "synthetic-demo-only", "ZF_DEPLOYMENT_PROFILE": "demo"}
FILENAME = "held-form-draft-export.json"


class HeldDownload(staging.FormApiFixture):
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

    def test_trusted_proxy_provider_never_serves_even_with_both_switches(self) -> None:
        _, path = self.prepare()
        with patch.dict(os.environ, ON), patch.object(self.app.provider, "name", "trusted-proxy"):
            code, headers, body = self.fetch("pam", path)
            self.assertEqual(code, 404, body)
            self.assertNotIn("attachment", headers.get("Content-Disposition", ""))
            self.assertNotIn(b"content_sha256", body)
            view = self.call("pam", "/api/cases/ZF-1/form-review")[1]
            self.assertNotIn("held_download_enabled", view)
        with patch.dict(os.environ, ON):
            self.assertEqual(self.fetch("pam", path)[0], 200)

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

    def saved(self) -> tuple[str, dict[str, Any]]:
        draft, path = self.prepare()
        with patch.dict(os.environ, ON):
            code, _, body = self.fetch("pam", path)
        self.assertEqual(code, 200, body)
        return path + "/freshness", json.loads(body)

    def check(self, actor: str, path: str, body: object) -> tuple[int, Any, bytes]:
        self.call(actor, "/api/me")
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode(),
            headers={"Cookie": self.cookies[actor], "X-ZF-CSRF": "1"},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.headers, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.headers, error.read()

    def test_default_off_and_trusted_proxy_serve_nothing(self) -> None:
        path, saved = self.saved()
        for env in (
            {},
            {"ZF_FORM_HELD_DOWNLOAD": "synthetic-demo-only"},
            {"ZF_DEPLOYMENT_PROFILE": "demo"},
        ):
            with self.subTest(env=env), patch.dict(os.environ, env):
                for key in ON:
                    if key not in env:
                        os.environ.pop(key, None)
                code, _, body = self.check("pam", path, saved)
                self.assertEqual(code, 404, body)
                self.assertNotIn(b"stale_fields", body)
        with patch.dict(os.environ, ON), patch.object(self.app.provider, "name", "trusted-proxy"):
            self.assertEqual(self.check("pam", path, saved)[0], 404)

    def test_fresh_copy_is_current_and_the_check_writes_nothing(self) -> None:
        path, saved = self.saved()
        with patch.dict(os.environ, ON):
            before = self.state()
            code, headers, body = self.check("pam", path, saved)
            self.assertEqual(self.state(), before)
        result = json.loads(body)
        self.assertEqual(code, 200, body)
        self.assertEqual(
            (result["status"], result["stale_fields"], result["reviewed"]), ("Current", [], False)
        )
        self.assertEqual(headers["Cache-Control"], "private, no-store")
        self.assertEqual(
            result,
            form_export.export_freshness(
                self.store, self.store.staff["pam@example.test"], "ZF-1", saved
            ),
        )

    def test_changed_source_stales_dependents_and_unrelated_change_stays_current(self) -> None:
        path, saved = self.saved()
        actor = self.store.staff["pam@example.test"]
        other = self.store.add_document(
            actor,
            "ZF-1",
            "unrelated.txt",
            "EPC",
            b"EPC E",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        bound = {row["source_id"] for row in saved["fields"] if row["source_id"]}
        self.assertTrue(bound)
        self.assertNotIn(other["id"], bound)

        def bump(ids: set[str]) -> None:
            with self.store.lock:
                for document in self.store._case("ZF-1")["documents"]:
                    if document["id"] in ids:
                        document["version"] += 1
                self.store.save()

        with patch.dict(os.environ, ON):
            bump({other["id"]})
            self.assertEqual(json.loads(self.check("pam", path, saved)[2])["status"], "Current")
            bump(bound)
            code, _, body = self.check("pam", path, saved)
        result = json.loads(body)
        self.assertEqual(code, 200, body)
        self.assertEqual(result["status"], "Stale")
        direct = form_export.export_freshness(
            self.store, self.store.staff["pam@example.test"], "ZF-1", saved
        )
        self.assertEqual(result, direct)
        self.assertIn("epc", result["stale_fields"])
        self.assertEqual(
            sorted(result["stale_fields"] + result["unaffected_fields"]),
            sorted(row["field_id"] for row in saved["fields"]),
        )
        self.assertFalse(result["reviewed"])
        for row in saved["fields"]:
            if isinstance(row["value"], str) and row["value"]:
                self.assertNotIn(row["value"].encode(), body)

    def test_edited_or_legacy_copy_is_invalid_and_never_repaired(self) -> None:
        path, saved = self.saved()
        edited = copy.deepcopy(saved)
        edited["fields"][0]["value"] = "tampered"
        legacy = {key: value for key, value in saved.items() if key != "history"}
        with patch.dict(os.environ, ON):
            for name, copy_ in (("edited", edited), ("legacy", legacy)):
                with self.subTest(copy=name):
                    code, _, body = self.check("pam", path, copy_)
                    result = json.loads(body)
                    self.assertEqual(code, 200, body)
                    self.assertEqual((result["status"], result["stale_fields"]), ("Invalid", []))
                    self.assertIn("Create a new held export", result["action"])

    def test_wrong_draft_non_object_and_unauthorised_requests_are_refused(self) -> None:
        path, saved = self.saved()
        other = dict(saved, draft_id="OTHER")
        with patch.dict(os.environ, ON):
            for bad in (other, [saved], "x", None):
                with self.subTest(body=type(bad).__name__):
                    code, _, body = self.check("pam", path, bad)
                    self.assertEqual(code, 400, body)
                    self.assertNotIn(b"stale_fields", body)
            for actor in ("sam", "kim"):
                code, _, body = self.check(actor, path, saved)
                self.assertEqual(code, 403, actor)
                self.assertNotIn(b"stale_fields", body)
            missing = path.replace("ZF-1", "NOPE")
            code, _, body = self.check("pam", missing, saved)
            self.assertEqual((code, json.loads(body)["status"]), (200, "Unavailable"))
            self.assertNotEqual(self.fetch("pam", path)[0], 200)

    def forge(self, saved: dict[str, Any], **changes: Any) -> dict[str, Any]:
        forged = {**copy.deepcopy(saved), **changes}
        forged["content_sha256"] = form_export._digest(
            {k: forged[k] for k in form_export.BODY_KEYS}
        )
        return forged

    def test_forged_self_consistent_copy_is_controlled_and_digest_is_not_provenance(self) -> None:
        path, saved = self.saved()
        mixed = copy.deepcopy(saved["fields"])
        mixed[0]["field_id"] = 5
        extra = saved["fields"] + [dict(saved["fields"][0], field_id="fabricated")]
        with patch.dict(os.environ, ON):
            before = self.state()
            code, headers, body = self.check("pam", path, self.forge(saved, fields=mixed))
            self.assertEqual(code, 200, body)
            self.assertEqual(json.loads(body)["status"], "Invalid")
            self.assertEqual(headers["Cache-Control"], "private, no-store")
            code, _, body = self.check("pam", path, self.forge(saved, fields=extra))
            result = json.loads(body)
            self.assertEqual(code, 200, body)
            self.assertFalse(result["reviewed"])
            # The digest detects accidental edits only, so a recomputed one is compared as supplied.
            self.assertEqual(result["status"], "Current")
            self.assertEqual(self.state(), before)

    def test_binding_to_the_path_case_and_draft_discloses_and_writes_nothing(self) -> None:
        path, saved = self.saved()
        missing = self.forge(saved, draft_id="NOPE")
        with patch.dict(os.environ, ON):
            before = self.state()
            cases = (
                (path.replace("ZF-1", "ZF-2"), saved),
                (path.replace(saved["draft_id"], "NOPE"), missing),
            )
            for target, copy_ in cases:
                with self.subTest(path=target):
                    code, _, body = self.check("pam", target, copy_)
                    result = json.loads(body)
                    self.assertEqual((code, result["status"]), (200, "Unavailable"), body)
                    self.assertEqual((result["stale_fields"], result["reviewed"]), ([], False))
                    self.assertNotIn("unaffected_fields", result)
            self.assertEqual(
                self.check("pam", path.replace(saved["draft_id"], "NOPE"), saved)[0], 400
            )
            self.assertEqual(self.state(), before)

    def test_anonymous_revoked_empty_and_error_responses_are_not_served_or_cached(self) -> None:
        path, saved = self.saved()
        with patch.dict(os.environ, ON):
            anonymous = urllib.request.Request(self.base + path, json.dumps(saved).encode())
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(anonymous)
            self.assertEqual(caught.exception.code, 401)
            self.assertNotIn(b"stale_fields", caught.exception.read())
            code, headers, body = self.check("pam", path, {})
            self.assertEqual(code, 400, body)
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertEqual(self.check("pam", path, saved)[0], 200)
            staff = self.store.staff["pam@example.test"]
            original = staff["role"]
            staff["role"] = "Contractor"
            try:
                code, _, body = self.check("pam", path, saved)
                self.assertIn(code, (401, 403))
                self.assertNotIn(b"stale_fields", body)
            finally:
                staff["role"] = original


if __name__ == "__main__":
    unittest.main()
