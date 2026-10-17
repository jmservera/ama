"""Ephemeral authenticated HTTP exercise; no inference or remote data."""

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


if __name__ == "__main__":
    unittest.main()
