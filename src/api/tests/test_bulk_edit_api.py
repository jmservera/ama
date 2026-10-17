"""Actual authenticated bulk routes on ephemeral synthetic SQLite, without model calls."""

import base64
import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.auth import PasswordProvider, TrustedProxyProvider
from zava_forward.api.server import App, make_handler

PREVIEW = "/api/bulk-edits/preview"
APPLY = "/api/bulk-edits/apply"
TENANT = "11111111-2222-3333-4444-555555555555"
OID = "aaaaaaaa-0000-0000-0000-000000000001"


class BulkEditApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        data = copy.deepcopy(DATA)
        data["staff"][0]["oid"] = OID
        data["staff"].append(
            dict(
                code="CON-1",
                name="Synthetic Builder",
                email="builder@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        self.path.write_text(json.dumps(data))
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app = App(
            self.store,
            provider=PasswordProvider(self.store, "synthetic-password"),
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies: dict[str, str] = {}
        self.request: dict[str, Any] = dict(
            case_ids=["ZF-1", "ZF-2"],
            changes={"case_reason": "Review the synthetic reference"},
            source="SYN-REGISTER",
            source_version="v1",
            reason="Synthetic field correction",
        )

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(
        self,
        path: str,
        body: object = None,
        actor: str = "sam",
        headers: dict[str, str] | None = None,
    ) -> tuple[int, Any]:
        if headers is None:
            if actor not in self.cookies:
                request = urllib.request.Request(
                    self.base + "/api/login",
                    json.dumps(
                        dict(email=f"{actor}@example.test", password="synthetic-password")
                    ).encode(),
                )
                with urllib.request.urlopen(request) as response:
                    self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
            headers = {"Cookie": self.cookies[actor]}
        request = urllib.request.Request(
            self.base + path,
            None if body is None else json.dumps(body).encode(),
            headers=headers,
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_responsive_app_exact_preview_apply_history_and_replay(self) -> None:
        with urllib.request.urlopen(self.base + "/healthz") as health:
            self.assertEqual(health.status, 200)
        before = copy.deepcopy(self.store.cases)
        code, preview = self.call(PREVIEW, self.request)
        self.assertEqual(code, 200)
        self.assertEqual(self.store.cases, before)
        self.assertEqual([r["outcome"] for r in preview["records"]], ["would_apply", "would_apply"])
        self.assertEqual(
            preview["records"][0]["changes"]["case_reason"],
            {"old": before["ZF-1"]["reason"], "new": self.request["changes"]["case_reason"]},
        )
        body = {"preview_id": preview["preview_id"]}
        self.assertEqual(self.call(APPLY, body, actor="pam")[0], 403)
        code, result = self.call(APPLY, body)
        self.assertEqual(code, 200)
        self.assertEqual([r["outcome"] for r in result["records"]], ["applied", "applied"])
        code, detail = self.call("/api/cases/ZF-1")
        self.assertEqual(code, 200)
        self.assertEqual(detail["edit_history"][0]["source_version"], "v1")
        self.assertEqual(self.call(APPLY, body)[0], 409)
        self.assertTrue(self.store.verify_audit())

    def test_mixed_targets_noops_and_blocked_apply_have_ordered_outcomes(self) -> None:
        body = dict(self.request, case_ids=["ZF-1", "ZF-5", "MISSING"])
        code, preview = self.call(PREVIEW, body)
        self.assertEqual(code, 200)
        self.assertEqual([r["case_id"] for r in preview["records"]], body["case_ids"])
        self.assertEqual(
            [r["outcome"] for r in preview["records"]],
            ["batch_blocked", "blocked", "blocked"],
        )
        self.assertEqual(preview["records"][1]["changes"], {})
        self.assertEqual(self.call(APPLY, {"preview_id": preview["preview_id"]})[0], 409)
        body = dict(self.request, changes={"case_reason": self.store.cases["ZF-1"]["reason"]})
        code, preview = self.call(PREVIEW, body)
        self.assertEqual(code, 200)
        self.assertEqual([r["outcome"] for r in preview["records"]], ["no_change"] * 2)
        self.assertEqual(self.call(APPLY, {"preview_id": preview["preview_id"]})[0], 200)
        self.assertNotIn("edit_history", self.store.cases["ZF-1"])

    def test_forbidden_malformed_unauthorized_and_stale_inputs(self) -> None:
        before = copy.deepcopy(self.store.cases)
        self.assertEqual(self.call(PREVIEW, self.request, headers={})[0], 401)
        self.assertEqual(self.call(PREVIEW, self.request, actor="builder")[0], 403)
        self.assertEqual(self.call(PREVIEW, dict(self.request, actor="pam"))[0], 400)
        for field in (
            "technical",
            "consent",
            "safety",
            "procurement",
            "budget",
            "invoices",
            "payments",
            "claims",
            "quality",
            "defects",
            "complaints",
            "contractor_instructions",
        ):
            self.assertEqual(
                self.call(PREVIEW, dict(self.request, changes={field: "Approved"}))[0], 400
            )
        self.assertEqual(self.store.cases, before)
        code, preview = self.call(PREVIEW, self.request)
        self.assertEqual(code, 200)
        with self.store.lock:
            self.store._case("ZF-1")["reason"] = "Changed after inspection"
            self.store.save()
        self.assertEqual(self.call(APPLY, {"preview_id": preview["preview_id"]})[0], 409)
        self.assertNotIn("edit_history", self.store.cases["ZF-2"])
        self.assertTrue(
            any(e["action"] == "bulk_edit_rejected" for e in self.store.audit_entries())
        )

    def test_password_cached_identity_cannot_survive_sql_revocation(self) -> None:
        code, preview = self.call(PREVIEW, self.request)
        self.assertEqual(code, 200)
        self.store.db.execute("DELETE FROM staff WHERE email=?", ("sam@example.test",))
        self.assertEqual(self.call(PREVIEW, self.request)[0], 403)
        self.assertEqual(self.call(APPLY, {"preview_id": preview["preview_id"]})[0], 403)
        self.assertNotIn("edit_history", self.store.cases["ZF-1"])

    def test_malformed_object_is_audited_and_storage_failure_is_explicit(self) -> None:
        self.assertEqual(self.call(PREVIEW, [self.request])[0], 400)
        entries = list(self.store.audit_entries())
        self.assertEqual(entries[-1]["action"], "bulk_edit_rejected")
        self.assertIn("Malformed", entries[-1]["detail"])
        code, preview = self.call(PREVIEW, self.request)
        self.assertEqual(code, 200)
        before = copy.deepcopy(self.store.cases)
        with (
            patch.object(self.store, "_proc_write", side_effect=RuntimeError("Synthetic outage")),
            self.assertLogs("zava_forward.api.server", level="ERROR"),
        ):
            code, result = self.call(APPLY, {"preview_id": preview["preview_id"]})
        self.assertEqual(code, 503)
        self.assertIn("unknown", result["error"])
        self.assertEqual(self.store.cases, before)
        self.assertNotIn("edit_history", self.store.cases["ZF-1"])

    def test_trusted_proxy_csrf_oid_rebinding_and_claim_role_are_enforced(self) -> None:
        self.app.provider = TrustedProxyProvider(
            self.store, dict(ZF_TRUSTED_PROXY="1", ZF_ENTRA_TENANT_ID=TENANT)
        )
        principal: dict[str, Any] = dict(
            auth_typ="aad",
            claims=[
                dict(typ="roles", val="ZavaForward.LiaisonOfficer"),
                dict(typ="oid", val=OID),
                dict(typ="tid", val=TENANT),
            ],
        )
        headers = {
            "X-MS-CLIENT-PRINCIPAL": base64.b64encode(json.dumps(principal).encode()).decode()
        }
        self.assertEqual(self.call(PREVIEW, self.request, headers=headers)[0], 403)
        headers["X-ZF-CSRF"] = "1"
        code, preview = self.call(PREVIEW, self.request, headers=headers)
        self.assertEqual(code, 200)
        rebound = dict(self.store.staff["sam@example.test"], oid="different-synthetic-oid")
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(rebound), "sam@example.test")
        )
        self.assertEqual(self.call(PREVIEW, self.request, headers=headers)[0], 403)
        self.assertEqual(
            self.call(APPLY, {"preview_id": preview["preview_id"]}, headers=headers)[0], 403
        )
        principal["claims"][0]["val"] = "ZavaForward.ProgrammeManager"
        headers["X-MS-CLIENT-PRINCIPAL"] = base64.b64encode(json.dumps(principal).encode()).decode()
        self.assertEqual(self.call(PREVIEW, self.request, headers=headers)[0], 403)
