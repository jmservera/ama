"""Local report/CSV contract on tiny fictional JSON, SQLite and opt-in MSSQL."""

import copy
import csv
import io
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import uuid
from datetime import UTC, datetime
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA, change_metadata
from test_progress_reports import AS_OF, disposition, events
from zava_forward.core import progress
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler


class ProgressApi(unittest.TestCase):
    backend = "sqlite"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["cases"][0].update({k: v for k, v in events().items() if k != "id"})
        data["cases"][0].update(closed=False, stage="Contacting resident")
        data["staff"].append(
            dict(
                code="CON-102",
                name="Fictional Provider",
                email="con@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
        )
        self.sam, self.pam = data["staff"][:2]
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(data))
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

            if os.environ.get("ZF_SQL_SERVER") not in ("127.0.0.1", "localhost"):
                raise RuntimeError("Issue 102 MSSQL tests require an explicit loopback server.")
            environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
            environment.start()
            self.addCleanup(environment.stop)
            admin = _Conn(connection_string())
            database = "zf_progress102_" + uuid.uuid4().hex
            admin.execute(f"CREATE DATABASE [{database}]")
            admin.close()
            os.environ["ZF_SQL_DATABASE"] = database
            self.store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        elif self.backend == "sqlite":
            self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        else:
            self.store = Store(str(self.path))
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        self.app = App(self.store, "fictional-local-only-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def get(self, actor: str, path: str) -> tuple[int, bytes]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="fictional-local-only-password")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(self.base + path, headers={"Cookie": self.cookies[actor]})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()

    def query(self, suffix: str = "") -> str:
        return f"?report=progress&as_of={AS_OF}{suffix}"

    def test_json_csv_complete_semantic_equality_and_no_mutation(self) -> None:
        before = copy.deepcopy(self.store.cases)
        audit = list(self.store.audit_entries())
        query = self.query("&view=all&ready=2&capacity=2&weeks=4&area=Test")
        code, body = self.get("pam", "/api/stats" + query)
        self.assertEqual(code, 200, body)
        report = json.loads(body)
        code, body = self.get("pam", "/api/cases.csv" + query)
        self.assertEqual(code, 200, body)
        decoded = {
            row["section"]: json.loads(row["value"])
            for row in csv.DictReader(io.StringIO(body.decode()))
        }
        self.assertEqual(decoded, report)
        self.assertEqual(self.get("pam", "/api/cases.csv" + query)[1], body)
        self.assertEqual(report["cohort"]["case_ids"], [f"ZF-{n}" for n in range(1, 6)])
        self.assertEqual(report["denominators"]["selected_cases"], 5)
        self.assertEqual(report["forecast"]["label"], "Forecast")
        self.assertEqual(report["as_of"], "2026-10-10T12:00:00+00:00")
        self.assertNotIn(b"PRIVATE", body)
        self.assertNotIn(b"Pat Test", body)
        self.assertNotIn(b"01000", body)
        self.assertEqual(self.store.cases, before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertTrue(self.store.verify_audit())

    def test_role_filters_empty_denominators_and_direct_default_deny(self) -> None:
        code, raw = self.get("sam", "/api/stats" + self.query())
        self.assertEqual(code, 200, raw)
        report = json.loads(raw)
        self.assertEqual(report["cohort"]["case_ids"], ["ZF-1", "ZF-2", "ZF-3", "ZF-4"])
        for path in ("/api/stats", "/api/cases.csv"):
            self.assertEqual(self.get("con", path + self.query())[0], 403)
            self.assertEqual(self.get("sam", path + self.query("&view=closed"))[0], 403)
        for user in ({"role": "Contractor"}, {"role": "Unknown"}, {}):
            with self.assertRaises(PermissionError):
                self.store.progress_report(user, as_of=AS_OF)
        code, raw = self.get("sam", "/api/stats" + self.query("&area=NotHere"))
        self.assertEqual(code, 200, raw)
        empty = json.loads(raw)
        self.assertEqual(empty["cohort"]["baseline_cases"], 4)
        self.assertEqual(empty["cohort"]["excluded_by_filters"], 4)
        self.assertEqual(empty["denominators"]["selected_cases"], 0)
        self.assertEqual(empty["status"], "No cohort evidence")
        self.assertEqual(empty["exceptions"][0]["code"], "empty_authorized_cohort")

    def test_invalid_inputs_do_not_expand_scope_or_default_to_success(self) -> None:
        for suffix in (
            "",
            "&view=unexpected",
            "&ready=-1",
            "&ready=100",
            "&capacity=2",
            "&ready=true",
            "&weeks=0&ready=1",
            "&start=2026-10-11T12:00Z",
            "&q=PRIVATE",
            "&area=Test&area=Other",
        ):
            query = "?report=progress" if suffix == "" else self.query(suffix)
            for path in ("/api/stats", "/api/cases.csv"):
                code, raw = self.get("pam", path + query)
                self.assertEqual(code, 400, raw)
                self.assertIn("error", json.loads(raw))
        with self.assertRaises(ValueError):
            self.store.progress_report(self.sam, as_of=AS_OF, filters={"secret": "x"})

    def test_legacy_stats_and_case_csv_unchanged(self) -> None:
        code, raw = self.get("pam", "/api/stats")
        self.assertEqual(code, 200, raw)
        self.assertIn("kpis", json.loads(raw))
        self.assertNotIn("forecast", json.loads(raw))
        code, raw = self.get("pam", "/api/cases.csv?view=all")
        self.assertEqual(code, 200, raw)
        self.assertNotEqual(raw.decode().splitlines()[0], "section,value")

    def test_blank_report_fields_and_duplicates_are_refused_not_dropped(self) -> None:
        for query in (
            "?report=&as_of=2026-10-10T12:00Z",
            self.query("&ready="),
            self.query("&ready=1&capacity="),
            self.query("&start="),
            self.query("&view="),
            self.query("&stage="),
            self.query("&unknown="),
            self.query("&ready=1&ready="),
            self.query("&report="),
        ):
            for path in ("/api/stats", "/api/cases.csv"):
                with self.subTest(query=query, path=path):
                    code, raw = self.get("pam", path + query)
                    self.assertEqual(code, 400, raw)
                    self.assertIn("error", json.loads(raw))

    def test_unrepresentable_utc_boundaries_are_explicit_400(self) -> None:
        for as_of in ("0001-01-01T00:00:00%2B01:00", "9999-12-31T23:59:59-01:00"):
            for path in ("/api/stats", "/api/cases.csv"):
                code, raw = self.get("pam", path + "?report=progress&as_of=" + as_of)
                self.assertEqual(code, 400, raw)
                self.assertIn("error", json.loads(raw))

    def test_unavailable_audit_is_explicit_and_never_a_trusted_clock(self) -> None:
        for failure in (ValueError("Fictional malformed ledger"), OSError("Fictional outage")):
            with (
                patch.object(self.store, "verify_ledger", side_effect=failure),
                self.assertLogs("zava_forward.core.store", level="ERROR"),
            ):
                report = self.store.progress_report(self.pam, as_of=AS_OF, view="all")
            self.assertEqual(report["audit_integrity"], "Unknown")
            self.assertEqual(report["status"], "Untrusted evidence")
            self.assertIn("audit_integrity_unknown", [e["code"] for e in report["exceptions"]])
            self.assertTrue(
                all(
                    interval["elapsed_seconds"] is None
                    for item in report["histories"]
                    for interval in item["stage_intervals"] + item["handoff_waits"]
                )
            )

    def reopen(self) -> Any:
        if self.backend == "sqlite":
            other = SqlStore("unused-seed", self.store.db_path)
        elif self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore

            other = MssqlStore("unused-seed", state_dir=self.tmp.name)
        else:
            return Store(str(self.path))
        self.addCleanup(other.db.close)
        return other

    def test_reopen_external_writer_refresh_and_ledger_invariance(self) -> None:
        with self.store.lock:
            self.store.audit(
                "fictional", "issue102_fixture_observed", "ZF-1", "No history inferred"
            )
            self.store.save()
        before = list(self.store.audit_entries())
        other = self.reopen()
        initial = other.progress_report(self.pam, as_of=AS_OF, view="all")
        self.assertEqual(list(other.audit_entries()), before)
        with other.lock:
            other._case("ZF-1")["returns"].append(
                disposition(3, "2026-10-04T12:00:00Z", "Contacting resident", "Home identified")
            )
            other.save()
        # Only the fixture writer appends events; the report remains read-only.
        actual = self.store if self.backend != "json" else self.reopen()
        refreshed = actual.progress_report(self.pam, as_of=AS_OF, view="all")
        self.assertEqual(initial["histories"][0]["stage_intervals"][0]["elapsed_seconds"], 172800)
        self.assertIsNone(initial["histories"][0]["stage_intervals"][1]["elapsed_seconds"])
        self.assertEqual(refreshed["histories"][0]["stage_intervals"][1]["elapsed_seconds"], 86400)
        self.assertEqual(list(actual.audit_entries()), before)
        self.assertTrue(actual.verify_audit())
        self.assertEqual(
            progress.export_csv(refreshed),
            progress.export_csv(actual.progress_report(self.pam, as_of=AS_OF, view="all")),
        )

    def test_committed_handoff_failure_returns_existing_explicit_outcome_contract(self) -> None:
        if self.backend == "json":
            self.skipTest("JSON does not have a SQL COMMIT acknowledgement boundary.")
        self.get("sam", "/api/stats")
        save = self.store.save

        def committed_without_ack() -> None:
            save()
            raise OSError("Synthetic lost post-COMMIT acknowledgement")

        request = urllib.request.Request(
            self.base + "/api/cases/ZF-2/offer-handoff",
            json.dumps(dict(change_metadata(self.store, "ZF-2"), to=self.pam["email"])).encode(),
            headers={"Cookie": self.cookies["sam"]},
        )
        with patch.object(self.store, "save", side_effect=committed_without_ack):
            with self.assertLogs("zava_forward.core.change_provenance", level="ERROR"):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code, 503)
        body = json.loads(caught.exception.read())
        self.assertEqual(body["outcome"], "committed")
        self.assertIn("Reload", body["error"])
        reopened = self.reopen()
        self.assertEqual(len(reopened.cases["ZF-2"]["handoff_history"]), 1)
        self.assertEqual(sum(e["action"] == "handoff_offered" for e in reopened.audit_entries()), 1)
        self.assertFalse(
            any(e["action"] == "handoff_offered_rejected" for e in reopened.audit_entries())
        )

    def test_actual_legacy_mixed_precision_writer_reopen_as_of_and_export(self) -> None:
        offer = datetime(2026, 10, 1, 12, 0, 45, 123456, tzinfo=UTC)
        accepted = datetime(2026, 10, 1, 12, 1, 15, 123456, tzinfo=UTC)
        with (
            patch("zava_forward.core.change_provenance.datetime", wraps=datetime) as clock,
            patch("zava_forward.core.workflows._now", return_value="2026-10-01T12:00+00:00"),
        ):
            clock.now.side_effect = [offer, accepted]
            self.store.offer_handoff(
                self.sam, "ZF-2", self.pam["email"], metadata=change_metadata(self.store, "ZF-2")
            )
            self.store.receive_handoff(self.pam, "ZF-2")
            self.store.accept_handoff(
                self.pam, "ZF-2", metadata=change_metadata(self.store, "ZF-2")
            )
        reopened = self.reopen()
        before = copy.deepcopy(reopened.cases["ZF-2"]["handoff_history"])
        audit = list(reopened.audit_entries())
        result = reopened.progress_report(self.pam, as_of=AS_OF, view="all")
        item = next(h for h in result["histories"] if h["case_id"] == "ZF-2")
        self.assertEqual([e["version"] for e in item["events"]], [1, 2, 3])
        self.assertNotIn("contradictory_event_order", [e["code"] for e in item["exceptions"]])
        self.assertNotIn("contradictory_handoff_chain", [e["code"] for e in item["exceptions"]])
        self.assertIn("unknown_handoff_duration", [e["code"] for e in item["exceptions"]])
        self.assertEqual(item["handoff_waits"][0]["outcome"], "Accepted")
        self.assertIsNone(item["handoff_waits"][0]["elapsed_seconds"])
        for boundary in ("2026-10-01T12:00:46Z", AS_OF):
            query = "?report=progress&view=all&as_of=" + boundary
            status, raw = self.get("pam", "/api/stats" + query)
            self.assertEqual(status, 200, raw)
            status, exported = self.get("pam", "/api/cases.csv" + query)
            self.assertEqual(status, 200, exported)
            decoded = {
                row["section"]: json.loads(row["value"])
                for row in csv.DictReader(io.StringIO(exported.decode()))
            }
            self.assertEqual(decoded, json.loads(raw))
            item = next(h for h in decoded["histories"] if h["case_id"] == "ZF-2")
            if boundary != AS_OF:
                self.assertEqual([e["state"] for e in item["events"]], ["Offered"])
                self.assertIn("unknown_event_as_of", [e["code"] for e in item["exceptions"]])
            self.assertIsNone(item["handoff_waits"][0]["elapsed_seconds"])
        self.assertEqual(reopened.cases["ZF-2"]["handoff_history"], before)
        self.assertEqual(list(reopened.audit_entries()), audit)
        self.assertTrue(reopened.verify_audit())

    def test_prospective_handoff_writers_retain_microseconds(self) -> None:
        for outcome in ("decline", "withdraw", "accept"):
            with self.subTest(outcome=outcome):
                self.store.offer_handoff(
                    self.sam,
                    "ZF-2",
                    self.pam["email"],
                    metadata=change_metadata(self.store, "ZF-2"),
                )
                self.store.receive_handoff(self.pam, "ZF-2")
                self.store.escalate_handoff(self.sam, "ZF-2", self.pam["email"], "Fictional chase")
                if outcome == "accept":
                    self.store.accept_handoff(
                        self.pam, "ZF-2", metadata=change_metadata(self.store, "ZF-2")
                    )
                    self.store.complete_handoff(self.pam, "ZF-2", "Fictional complete")
                elif outcome == "decline":
                    self.store.decline_handoff(self.pam, "ZF-2", "Fictional decline")
                else:
                    self.store.withdraw_handoff(self.sam, "ZF-2")
                rows = self.reopen().cases["ZF-2"]["handoff_history"]
                for row in rows:
                    self.assertRegex(row["at"], r"T\d{2}:\d{2}:\d{2}(?:\.\d{6})?\+00:00$")
                    if row["state"] not in {"Offered", "Accepted"}:
                        self.assertRegex(row["at"], r"\.\d{6}\+00:00$")
                as_of = datetime.now(UTC).isoformat()
                report = self.store.progress_report(self.pam, as_of=as_of, view="all")
                item = next(h for h in report["histories"] if h["case_id"] == "ZF-2")
                self.assertFalse(
                    any(e["code"].startswith("contradictory_") for e in item["exceptions"])
                )
                self.assertTrue(
                    all(w["elapsed_seconds"] is not None for w in item["handoff_waits"])
                )
                if outcome == "accept":
                    self.sam, self.pam = self.pam, self.sam


class JsonProgressApi(ProgressApi):
    backend = "json"


@unittest.skipUnless(os.environ.get("ZF_PROGRESS_MSSQL") == "1", "opt-in loopback SQL Server")
class MssqlProgressApi(ProgressApi):
    backend = "mssql"
