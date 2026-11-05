"""Ephemeral authenticated HTTP exercise; no inference or remote data."""

import copy
import csv
import io
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

from dataset import change_metadata
from test_form_staging import batch, schema
from tests.test_mvp import DATA
from zava_forward.core import forms
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class FormApi(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"].append(
            dict(
                code="CON-1",
                name="Synthetic Contractor",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        path = Path(self.tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.app = App(self.store, "synthetic-test-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, actor: str, path: str, body: object = None) -> tuple[int, Any]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-test-password")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_registry_stage_read_and_no_source_or_controlled_writes(self) -> None:
        with urllib.request.urlopen(self.base + "/healthz") as response:
            self.assertEqual(response.status, 200)
        with patch.object(self.store.ai, "_chat", side_effect=AssertionError("No inference")):
            code, registered = self.call("pam", "/api/form-schemas", schema())
            self.assertEqual(code, 201, registered)
            self.assertEqual(registered["approval"], "Unapproved")
            actor = self.store.staff["pam@example.test"]
            doc = self.store.add_document(
                actor,
                "ZF-1",
                "synthetic.txt",
                "EPC",
                b"EPC D\nEPC E",
                metadata=change_metadata(self.store, "ZF-1"),
            )
            before = self.call("pam", "/api/cases/ZF-1")[1]
            code, result = self.call("pam", "/api/cases/ZF-1/form-candidates", batch(doc["id"]))
            self.assertEqual(code, 201, result)
            self.assertEqual(result["candidates"][0]["raw_value"], "D")
            self.assertEqual(result["source"]["id"], doc["id"])
            self.assertEqual(result["processing"]["assertion_status"], "Supplied, unverified")
            rows = self.call("pam", "/api/cases/ZF-1/form-candidates")[1]["batches"]
            self.assertEqual(rows, [result])
            after = self.call("pam", "/api/cases/ZF-1")[1]
            self.assertEqual(before, after)
            self.assertNotIn("form_staging", after)
            self.assertTrue(self.store.verify_audit())

    def test_rescanned_sql_sources_persist_after_repeated_http_reads_and_reopen(self) -> None:
        self.assertEqual(self.call("pam", "/api/form-schemas", schema())[0], 201)
        actor = self.store.staff["pam@example.test"]
        path = "/api/cases/ZF-1/form-candidates"
        for status in ("pending", "missing"):
            with self.subTest(scan=status):
                doc = self.store.add_document(
                    actor,
                    "ZF-1",
                    "synthetic.txt",
                    "EPC",
                    b"EPC D",
                    metadata=change_metadata(self.store, "ZF-1"),
                )
                with self.store.lock:
                    source = next(
                        d for d in self.store._case("ZF-1")["documents"] if d["id"] == doc["id"]
                    )
                    if status == "missing":
                        source.pop("scan")
                    else:
                        source["scan"]["status"] = status
                    self.store.save()
                code, result = self.call("pam", path, batch(doc["id"]))
                self.assertEqual(code, 201, result)
                self.assertEqual(result["candidates"][0]["raw_value"], "D")
                self.assertEqual(result["processing"]["parser_version"], "test-1")
                for _ in range(2):
                    code, rows = self.call("pam", path)
                    self.assertEqual(code, 200, rows)
                    self.assertEqual(
                        next(r for r in rows["batches"] if r["id"] == result["id"]), result
                    )
                    self.assertNotIn("form_staging", self.call("pam", "/api/cases/ZF-1")[1])
                reopened = SqlStore("nonexistent-seed-is-not-read", self.store.db_path)
                self.addCleanup(reopened.db.close)
                rows = forms.list_candidates(reopened, actor, "ZF-1")
                self.assertEqual(next(r for r in rows if r["id"] == result["id"]), result)
                self.assertTrue(reopened.verify_audit())

    def test_auth_source_scope_strict_keys_and_safe_service_errors(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.base + "/api/form-schemas")
        self.assertEqual(caught.exception.code, 401)
        self.assertEqual(self.call("kim", "/api/form-schemas")[0], 403)
        self.assertEqual(self.call("sam", "/api/form-schemas", schema())[0], 403)
        self.assertEqual(
            self.call("pam", "/api/form-schemas", dict(schema(), approved=True))[0], 400
        )
        self.assertEqual(self.call("pam", "/api/form-schemas", schema())[0], 201)
        actor = self.store.staff["pam@example.test"]
        doc = self.store.add_document(
            actor,
            "ZF-1",
            "synthetic.txt",
            "EPC",
            b"EPC D",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        path = "/api/cases/ZF-1/form-candidates"
        self.assertEqual(self.call("sam", path, batch(doc["id"]))[0], 403)
        self.assertEqual(
            self.call("pam", "/api/cases/ZF-2/form-candidates", batch(doc["id"]))[0], 404
        )
        self.assertEqual(self.call("pam", path, dict(batch(doc["id"]), approved=True))[0], 400)
        with patch.object(self.store, "save", side_effect=OSError("private raw must not leak")):
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, result = self.call("pam", path, batch(doc["id"]))
            self.assertEqual(code, 503, result)
            self.assertNotIn("private raw", json.dumps(result))
        self.assertEqual(self.call("pam", path)[1]["batches"], [])

    def working_review(self) -> tuple[Any, Any]:
        self.assertEqual(self.call("pam", "/api/form-schemas", schema())[0], 201)
        actor = self.store.staff["pam@example.test"]
        doc = self.store.add_document(
            actor,
            "ZF-1",
            "synthetic.txt",
            "EPC",
            b"EPC D",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        staged = self.call("pam", "/api/cases/ZF-1/form-candidates", batch(doc["id"]))[1]
        code, draft = self.call(
            "pam",
            "/api/cases/ZF-1/form-review",
            dict(action="open", schema_id="SYN-TECH", schema_version=1),
        )
        self.assertEqual(code, 201, draft)
        request = dict(
            action="review",
            draft_id=draft["draft_id"],
            expected_version=draft["input_version"],
            field_id="epc",
            decision="accept",
            batch_id=staged["id"],
            candidate_id=staged["candidates"][0]["id"],
            value=None,
            reason="SYN field review reason",
        )
        return draft, request

    def test_working_field_review_and_manifest_are_held_and_isolated(self) -> None:
        with urllib.request.urlopen(self.base + "/healthz") as response:
            self.assertEqual(response.status, 200)
        path = "/api/cases/ZF-1/form-review"
        draft, request = self.working_review()
        before = self.call("pam", "/api/cases/ZF-1")[1]
        with patch.object(self.store.ai, "_chat", side_effect=AssertionError("No inference")):
            code, result = self.call("pam", path, request)
            self.assertEqual(code, 201, result)
            self.assertEqual(result["fields"]["epc"]["value"], "D")
            self.assertEqual(result["fields"]["area"], draft["fields"]["area"])
            self.assertFalse(result["reviewed_ready"])
            self.assertEqual(self.call("pam", path, request)[0], 409)
            code, manifest = self.call(
                "pam",
                path,
                dict(
                    action="diagnose",
                    draft_id=result["draft_id"],
                    expected_version=result["input_version"],
                ),
            )
            self.assertEqual(code, 201, manifest)
            self.assertEqual(manifest["template"], schema()["template"])
            self.assertEqual(len(manifest["attachments"]), 1)
            self.assertEqual(manifest["history"][0]["reviewer"], "pam@example.test")
            code, saved = self.call("pam", path)
            self.assertEqual(code, 200, saved)
            self.assertEqual(saved["drafts"][0]["recorded_diagnostics"], [manifest])
            self.assertEqual(len(saved["decision_holds"]), 3)
            self.assertTrue(all(h["approval_evidence"] is None for h in saved["decision_holds"]))
            self.assertEqual(
                saved["drafts"][0]["acceleration"]["signal"], "Pause for human decision"
            )
        self.assertEqual(before, self.call("pam", "/api/cases/ZF-1")[1])
        self.assertNotIn(
            "SYN field review reason", json.dumps(self.call("kim", "/api/cases/ZF-1")[1])
        )

    def test_working_review_denials_quarantine_and_no_approval_actions(self) -> None:
        path = "/api/cases/ZF-1/form-review"
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.base + path)
        self.assertEqual(caught.exception.code, 401)
        draft, request = self.working_review()
        for actor in ("sam", "kim"):
            self.assertEqual(self.call(actor, path)[0], 403)
            self.assertEqual(self.call(actor, path, request)[0], 403)
        self.assertEqual(self.call("pam", path, dict(request, approved=True))[0], 400)
        for action in ("approve", "submit", "reviewed-export", "restart"):
            self.assertEqual(self.call("pam", path, dict(action=action))[0], 400)
        self.assertEqual(self.call("pam", "/api/cases/ZF-2/form-review", request)[0], 404)
        self.assertEqual(self.call("pam", path, request)[0], 201)
        with self.store.lock:
            self.store._case("ZF-1")["documents"][0]["scan"]["status"] = "infected"
            self.store.save()
        code, denied = self.call("pam", path)
        self.assertEqual(code, 200, denied)
        self.assertEqual(
            denied["drafts"],
            [
                dict(
                    draft_id=draft["draft_id"],
                    status="Unavailable",
                    notice=(
                        "Working evidence is unavailable. "
                        "Ask the document owner to recover its source."
                    ),
                )
            ],
        )
        self.assertNotIn("SYN field review reason", json.dumps(denied))
        self.assertNotIn("raw_value", json.dumps(denied))
        self.assertEqual(self.call("pam", path, dict(request, expected_version=2))[0], 403)

    def test_unavailable_draft_does_not_block_readable_sibling(self) -> None:
        path = "/api/cases/ZF-1/form-review"
        draft, request = self.working_review()
        self.assertEqual(self.call("pam", path, request)[0], 201)
        actor = self.store.staff["pam@example.test"]
        doc = self.store.add_document(
            actor,
            "ZF-1",
            "sibling.txt",
            "EPC",
            b"E",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        code, staged = self.call("pam", "/api/cases/ZF-1/form-candidates", batch(doc["id"], "E", 0))
        self.assertEqual(code, 201, staged)
        code, sibling = self.call(
            "pam", path, dict(action="open", schema_id="SYN-TECH", schema_version=1)
        )
        self.assertEqual(code, 201, sibling)
        code, readable = self.call(
            "pam",
            path,
            dict(
                request,
                draft_id=sibling["draft_id"],
                batch_id=staged["id"],
                candidate_id=staged["candidates"][0]["id"],
            ),
        )
        self.assertEqual(code, 201, readable)
        with self.store.lock:
            self.store._case("ZF-1")["documents"][0]["scan"]["status"] = "infected"
            self.store.save()
        code, result = self.call("pam", path)
        self.assertEqual(code, 200, result)
        self.assertEqual(
            result["drafts"],
            [
                dict(
                    draft_id=draft["draft_id"],
                    status="Unavailable",
                    notice=(
                        "Working evidence is unavailable. "
                        "Ask the document owner to recover its source."
                    ),
                ),
                dict(readable, recorded_diagnostics=[], diagnostic_freshness=[]),
            ],
        )

    def test_working_review_storage_failure_reports_error_without_partial_history(self) -> None:
        path = "/api/cases/ZF-1/form-review"
        _, request = self.working_review()
        with patch.object(self.store, "_append_audit", side_effect=OSError("private failure text")):
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, failed = self.call("pam", path, request)
        self.assertEqual(code, 503, failed)
        self.assertNotIn("private failure text", json.dumps(failed))
        code, saved = self.call("pam", path)
        self.assertEqual(code, 200, saved)
        self.assertEqual(saved["drafts"][0]["history"], [])
        self.assertTrue(self.store.verify_audit())

    def raw(self, actor: str, path: str) -> tuple[int, str, dict[str, str]]:
        self.call(actor, "/api/me")
        request = urllib.request.Request(self.base + path, headers={"Cookie": self.cookies[actor]})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read().decode(), dict(response.headers)
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode(), dict(error.headers)

    def two_versions(self) -> None:
        first = schema()
        first["fields"][0]["options"] = ["A", "B", "=SUM(1,2)", 'Zoë, "x"\nline']
        second = dict(schema(), version=2)
        self.assertEqual(self.call("pam", "/api/form-schemas", first)[0], 201)
        self.assertEqual(self.call("pam", "/api/form-schemas", second)[0], 201)

    def test_schema_csv_has_one_row_per_version_matching_json(self) -> None:
        self.two_versions()
        with patch.object(self.store.ai, "_chat", side_effect=AssertionError("No inference")):
            code, text, headers = self.raw("pam", "/api/form-schemas.csv")
        self.assertEqual(code, 200, text)
        self.assertTrue(headers["Content-Type"].startswith("text/csv"))
        self.assertIn('filename="form-schemas.csv"', headers["Content-Disposition"])
        rows = list(csv.reader(io.StringIO(text)))
        self.assertEqual(
            rows[0],
            [
                "definition",
                "digest",
                "approval",
                "approval_evidence",
                "source_policy_status",
                "recorded_by",
                "recorded_at",
            ],
        )
        authoritative = self.call("pam", "/api/form-schemas")[1]["schemas"]
        self.assertEqual(len(rows) - 1, 2)
        for row, source in zip(rows[1:], authoritative, strict=True):
            self.assertEqual(json.loads(row[0]), source["definition"])
            self.assertEqual(row[1], source["digest"])
            self.assertEqual(row[2:4], ["Unapproved", ""])
            self.assertEqual(row[4], "Unapproved")
            self.assertEqual(row[5], "pam@example.test")
            self.assertEqual(row[6], source["recorded_at"])
        self.assertEqual([json.loads(r[0])["version"] for r in rows[1:]], [1, 2])
        options = json.loads(rows[1][0])["fields"][0]["options"]
        self.assertEqual(options[2:], ["=SUM(1,2)", 'Zoë, "x"\nline'])

    def test_schema_csv_formula_text_in_a_metadata_cell_is_neutralised(self) -> None:
        self.two_versions()
        self.store.data["form_schemas"][0]["approval_evidence"] = "=cmd|' /C calc'!A0"
        _, text, _ = self.raw("pam", "/api/form-schemas.csv")
        self.assertIn("'=cmd", text)
        self.assertNotIn(",=cmd", text)

    def test_empty_schema_csv_follows_the_list_convention(self) -> None:
        code, text, _ = self.raw("pam", "/api/form-schemas.csv")
        self.assertEqual((code, text), (200, "\r\n"))

    def test_schema_csv_denies_everyone_without_the_full_rights(self) -> None:
        self.two_versions()
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.base + "/api/form-schemas.csv")
        self.assertEqual(caught.exception.code, 401)
        for actor in ("kim", "sam"):
            code, text, _ = self.raw(actor, "/api/form-schemas.csv")
            self.assertEqual(code, 403, actor)
            self.assertNotIn("SYN-TECH", text)

    def test_schema_csv_follows_revocation_and_reason_view_changes(self) -> None:
        self.two_versions()
        self.assertEqual(self.raw("pam", "/api/form-schemas.csv")[0], 200)
        with patch.dict("os.environ", {"ZF_REASON_ROLES": "Building Safety Liaison"}):
            code, text, _ = self.raw("pam", "/api/form-schemas.csv")
        self.assertEqual(code, 403)
        self.assertNotIn("SYN-TECH", text)
        revoked = dict(self.store.staff["pam@example.test"], role="Programme Support Officer")
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(revoked), "pam@example.test")
        )
        code, text, _ = self.raw("pam", "/api/form-schemas.csv")
        self.assertEqual(code, 403)
        self.assertNotIn("SYN-TECH", text)

    def test_schema_csv_has_no_case_data_and_changes_nothing(self) -> None:
        self.two_versions()
        before = copy.deepcopy(self.store.data["form_schemas"])
        cases = copy.deepcopy(self.store.cases)
        _, text, _ = self.raw("pam", "/api/form-schemas.csv?case=ZF-1&q=x")
        self.assertEqual(text, self.raw("pam", "/api/form-schemas.csv")[1])
        for case in cases.values():
            self.assertNotIn(case["resident"]["name"], text)
            self.assertNotIn(case["id"] + ",", text)
        self.assertEqual(self.store.data["form_schemas"], before)
        self.assertEqual(self.store.cases, cases)
        self.assertTrue(self.store.verify_audit())


if __name__ == "__main__":
    unittest.main()
