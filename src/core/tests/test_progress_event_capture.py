"""Prospective actual-domain capture, never reconstructed historical fixtures."""

import copy
import csv
import io
import json
import os
import tempfile
import unittest
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Self
from unittest.mock import patch

from dataset import DATA, RESIDENT_BINDINGS, change_metadata, supplied_contract_fixture
from zava_forward.core import progress
from zava_forward.core.quality import checklist_for
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

Record = dict[str, Any]
BASE = datetime(2026, 10, 17, 10, tzinfo=UTC)
QI = dict(
    code="QI-102", name="Synthetic Inspector", email="qi102@example.test", role="Quality Inspector"
)


@contextmanager
def clock(seconds: int) -> Any:
    class Clock(datetime):
        @classmethod
        def now(cls, tz: Any = None) -> Self:
            return cls.fromtimestamp((BASE + timedelta(seconds=seconds)).timestamp(), tz)

    with (
        patch("zava_forward.core.change_provenance.datetime", Clock),
        patch("zava_forward.core.workflows.datetime", Clock),
    ):
        yield


class JsonCapture(unittest.TestCase):
    backend = "json"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(DATA)
        data["staff"].append(QI)
        data["cases"][1].update(stage="Completed", closed=True)
        self.sam, self.pam = data["staff"][:2]
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(data))
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import _Conn, connection_string

            if os.environ.get("ZF_SQL_SERVER") not in ("127.0.0.1", "localhost"):
                raise RuntimeError("Task-owned loopback MSSQL required.")
            env = patch.dict(os.environ, ZF_SQL_DATABASE="master")
            env.start()
            self.addCleanup(env.stop)
            admin = _Conn(connection_string())
            self.database = "zf_capture102_" + uuid.uuid4().hex
            admin.execute(f"CREATE DATABASE [{self.database}]")
            admin.close()
            os.environ["ZF_SQL_DATABASE"] = self.database
        self.store = self.open_store()

    def open_store(self) -> Any:
        store: Any
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore

            store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        elif self.backend == "sqlite":
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        else:
            return Store(str(self.path))
        self.addCleanup(store.db.close)
        return store

    def report(self, seconds: int = 600, start: int | None = None) -> Record:
        result: Record = self.store.progress_report(
            self.pam,
            as_of=(BASE + timedelta(seconds=seconds)).isoformat(),
            start=(BASE + timedelta(seconds=start)).isoformat() if start is not None else None,
            view="all",
        )
        return result

    def history(self, cid: str = "ZF-3", seconds: int = 600) -> Record:
        return next(h for h in self.report(seconds)["histories"] if h["case_id"] == cid)

    def prepare_advance(self) -> None:
        pid = self.store.create_package(
            self.pam,
            "SYN package",
            "2026-01-01",
            "2099-12-31",
            "Loft",
            "SYN-CALL-OFF",
            "SYN-1",
        )
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 3, 1, "SYN commitment", details)
        wid = self.store.issue_work_order(
            self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS
        )
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")

    def offer(self) -> None:
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.pam["email"],
            metadata=change_metadata(self.store, "ZF-1"),
        )

    def submit(self) -> int:
        return int(
            self.store.submit_quality(
                self.sam,
                "ZF-3",
                "Loft insulation",
                "SYN separate installer",
                "Installer",
                {key: "SYN observed photo" for key in checklist_for("Loft insulation")["items"]},
                context_revision=1,
            )
        )

    def quality_pair(self) -> None:
        with clock(0):
            self.submit()
        with clock(60):
            self.store.accept_quality(QI, "ZF-3", 0, "SYN independent inspection")
        with clock(180):
            self.store.hand_over_quality(self.sam, "ZF-3", 0, "SYN guide and guarantees", True)

    def success_count(self, action: str) -> int:
        return sum(e["action"] == action for e in self.store.audit_entries())

    def test_actual_forward_return_pause_and_reopen(self) -> None:
        self.prepare_advance()
        with clock(0):
            self.store.advance(self.pam, "ZF-3")
        with clock(60):
            self.store.return_case(
                self.pam,
                "ZF-3",
                "Resident paused works",
                "SYN requested pause",
                change_metadata(self.store, "ZF-3") | {"next_action": "SYN contact"},
            )
        with clock(180):
            self.store.return_case(
                self.pam,
                "ZF-3",
                "Contacting resident",
                "SYN contact restart",
                change_metadata(self.store, "ZF-3") | {"next_action": "SYN call"},
            )
        with clock(240):
            self.store.reopen_case(
                self.pam,
                "ZF-2",
                "SYN aftercare report",
                change_metadata(self.store, "ZF-2") | {"next_action": "SYN investigate"},
            )
        rows = self.open_store().detail("ZF-3")["returns"]
        self.assertEqual([r["event_type"] for r in rows], ["advance", "return", "return"])
        self.assertEqual([r["version"] for r in rows], [1, 2, 3])
        self.assertTrue(rows[0]["work_order_versions"])
        self.assertTrue(all(r["actor"]["email"] == self.pam["email"] for r in rows))
        self.assertTrue(all("." in r["at"] and r["at"].endswith("+00:00") for r in rows))
        h = self.history()
        self.assertEqual([e["kind"] for e in h["events"]], ["advance", "return", "return"])
        self.assertEqual([i["elapsed_seconds"] for i in h["stage_intervals"]], [60, 120, None])
        self.assertEqual(h["stage_intervals"][1]["classification"], "Paused stage")
        self.assertEqual(self.history("ZF-2")["events"][0]["kind"], "reopen")
        self.assertIsNone(self.history("ZF-2")["stage_intervals"][0]["elapsed_seconds"])
        clipped = next(h for h in self.report(start=90)["histories"] if h["case_id"] == "ZF-3")
        self.assertEqual(clipped["stage_intervals"][0]["elapsed_seconds"], 90)
        self.assertTrue(self.store.verify_audit())

    def test_actual_handoff_offered_received_accepted_ownership_and_exact_wait(self) -> None:
        with clock(0):
            self.offer()
        with clock(60):
            self.store.receive_handoff(self.pam, "ZF-1")
        self.assertEqual(self.store.detail("ZF-1")["owner_code"], self.sam["code"])
        with clock(180):
            self.store.accept_handoff(
                self.pam, "ZF-1", metadata=change_metadata(self.store, "ZF-1")
            )
        self.assertEqual(self.open_store().detail("ZF-1")["owner_code"], self.pam["code"])
        rows = self.store.detail("ZF-1")["handoff_history"]
        self.assertEqual(
            [r["event_type"] for r in rows],
            ["handoff_offered", "handoff_received", "handoff_accepted"],
        )
        self.assertEqual([r["version"] for r in rows], [1, 2, 3])
        self.assertTrue(
            all(r["source_version"] and r["actor"] and r["receiving_owner"] for r in rows)
        )
        h = self.history("ZF-1")
        self.assertEqual(h["handoff_waits"][0]["elapsed_seconds"], 180)
        self.assertEqual(self.history("ZF-1", 90)["handoff_waits"][0]["outcome"], "Pending")
        self.assertEqual(self.history("ZF-1", 90)["handoff_waits"][0]["elapsed_seconds"], 90)
        before = self.success_count("handoff_accepted")
        with self.assertRaises(ValueError):
            self.store.accept_handoff(
                self.pam, "ZF-1", metadata=change_metadata(self.store, "ZF-1")
            )
        self.assertEqual(self.success_count("handoff_accepted"), before)
        self.assertEqual(len(self.store.detail("ZF-1")["handoff_history"]), 3)

    def test_later_contradictory_handoff_invalidates_wait_only_when_observed(self) -> None:
        self.test_actual_handoff_offered_received_accepted_ownership_and_exact_wait()
        case = copy.deepcopy(self.store.cases["ZF-1"])
        row = copy.deepcopy(case["handoff_history"][1])
        row.update(version=4, at=(BASE + timedelta(seconds=240)).isoformat())
        case["handoff_history"].append(row)
        before = copy.deepcopy(case)
        early = progress.history(case, BASE + timedelta(seconds=200), None)
        self.assertEqual(early["handoff_waits"][0]["elapsed_seconds"], 180)
        self.assertNotIn("contradictory_handoff_chain", [e["code"] for e in early["exceptions"]])
        late = progress.history(case, BASE + timedelta(seconds=300), None)
        self.assertIn("contradictory_handoff_chain", [e["code"] for e in late["exceptions"]])
        self.assertIsNone(late["handoff_waits"][0]["elapsed_seconds"])
        self.assertEqual(late["handoff_waits"][0]["status"], "Unknown")
        self.assertEqual([e["version"] for e in late["events"]], [1, 2, 3, 4])
        self.assertEqual(case, before)
        for trust in (True, False, None):
            report = progress.report(
                [case],
                as_of=(BASE + timedelta(seconds=300)).isoformat(),
                start=None,
                cohort={},
                scenario=None,
                audit_intact=trust,
            )
            self.assertIsNone(report["histories"][0]["handoff_waits"][0]["elapsed_seconds"])
            decoded = {
                r["section"]: json.loads(r["value"])
                for r in csv.DictReader(io.StringIO(progress.export_csv(report)))
            }
            self.assertEqual(decoded, report)

    def test_quality_actual_pair_replacement_asof_and_no_cross_version_pairing(self) -> None:
        self.quality_pair()
        earlier = self.history(seconds=200)
        pair = earlier["accepted_handovers"][0]
        self.assertEqual(pair["elapsed_seconds"], 120)
        self.assertEqual(pair["evidence_version"], 1)
        self.assertEqual(pair["source"], "quality/0/history/1")
        with clock(300):
            self.submit()
        self.assertEqual(self.history(seconds=200), earlier)
        self.assertEqual(
            self.history()["accepted_handovers"][0]["superseded_at"],
            (BASE + timedelta(seconds=300)).isoformat(),
        )
        with clock(360):
            self.store.accept_quality(QI, "ZF-3", 1, "SYN separate inspection v2")
        self.assertEqual(len(self.history()["accepted_handovers"]), 1)
        with clock(480):
            self.store.hand_over_quality(self.sam, "ZF-3", 1, "SYN new guide", True)
        pairs = self.history()["accepted_handovers"]
        self.assertEqual([p["evidence_version"] for p in pairs], [1, 2])
        self.assertEqual([p["elapsed_seconds"] for p in pairs], [120, 120])
        self.assertIsNone(self.report()["denominators"]["accepted_handover_actuals"])
        report = self.report()
        decoded = {
            r["section"]: json.loads(r["value"])
            for r in csv.DictReader(io.StringIO(progress.export_csv(report)))
        }
        self.assertEqual(decoded, report)
        for private in (self.sam["email"], self.sam["name"], QI["email"], "SYN guide"):
            self.assertNotIn(private, json.dumps(report))

    def test_quality_audit_trust_gate_covers_csv_and_actual_measurement(self) -> None:
        self.quality_pair()
        self.assertEqual(self.history()["accepted_handovers"][0]["elapsed_seconds"], 120)
        for trust in (False, None):
            report = progress.report(
                [self.store.cases["ZF-3"]],
                as_of=(BASE + timedelta(seconds=600)).isoformat(),
                start=None,
                cohort={},
                scenario=None,
                audit_intact=trust,
            )
            self.assertIsNone(report["histories"][0]["accepted_handovers"][0]["elapsed_seconds"])
            self.assertEqual(report["histories"][0]["accepted_handovers"][0]["status"], "Untrusted")
            decoded = {
                r["section"]: json.loads(r["value"])
                for r in csv.DictReader(io.StringIO(progress.export_csv(report)))
            }
            self.assertEqual(decoded, report)

    def test_missing_and_contradictory_quality_events_are_unknown(self) -> None:
        self.quality_pair()
        case = copy.deepcopy(self.store.cases["ZF-3"])
        for key, value in (
            ("version", 99),
            ("at", "bad"),
            ("evidence_version", 2),
            ("event_type", "quality_other"),
            ("from_state", "Returned"),
            ("receiving_owner", None),
            ("actor", None),
            ("event_type", []),
            ("event_type", {}),
            ("source_version", "not the evidence version"),
            ("checklist_version", "not the checklist"),
            ("receiving_owner", {"unknown": "unknown"}),
        ):
            bad = copy.deepcopy(case)
            bad["quality"][0]["history"][1][key] = value
            h = progress.history(bad, BASE + timedelta(seconds=600), None)
            self.assertTrue(h["exceptions"])
            self.assertTrue(all(p["elapsed_seconds"] is None for p in h["accepted_handovers"]))
        legacy = copy.deepcopy(case)
        for row in legacy["quality"][0]["history"]:
            for key in ("actor", "event_type", "version", "evidence_version"):
                row.pop(key)
        self.assertTrue(
            all(
                p["elapsed_seconds"] is None
                for p in progress.history(legacy, BASE + timedelta(seconds=600), None)[
                    "accepted_handovers"
                ]
            )
        )

    def test_unauthorized_or_missing_prerequisites_never_capture(self) -> None:
        before, audit = copy.deepcopy(self.store.cases), list(self.store.audit_entries())
        for user in (
            dict(self.pam, email="unregistered@example.test"),
            dict(self.sam, role="Quality Inspector"),
        ):
            with self.assertRaises(PermissionError):
                self.store.advance(user, "ZF-3")
            with self.assertRaises(PermissionError):
                self.store.reopen_case(user, "ZF-2", "SYN request", {})
        with self.assertRaises(ValueError):
            self.store.advance(self.pam, "ZF-3")
        self.assertEqual(self.store.cases, before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(self.history()["stage_intervals"], [])

    def test_failed_save_has_no_event_or_success_audit_and_clean_retry_once(self) -> None:
        with clock(0):
            self.offer()
        before, audit = self.store.detail("ZF-1"), list(self.store.audit_entries())
        with patch.object(self.store, "save", side_effect=OSError("SYN write failed")):
            with self.assertRaisesRegex(OSError, "write failed"):
                self.store.receive_handoff(self.pam, "ZF-1")
        self.assertEqual(self.open_store().detail("ZF-1"), before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        with clock(60):
            self.store.receive_handoff(self.pam, "ZF-1")
        self.assertEqual(self.success_count("handoff_received"), 1)
        self.assertEqual(len(self.open_store().detail("ZF-1")["handoff_history"]), 2)

    def test_all_handoff_terminal_states_capture_registered_versions(self) -> None:
        with clock(0):
            self.offer()
        with clock(60):
            self.store.escalate_handoff(self.sam, "ZF-1", self.pam["email"], "SYN chase")
        with clock(120):
            self.store.decline_handoff(self.pam, "ZF-1", "SYN unavailable")
        with clock(180):
            self.offer()
        with clock(240):
            self.store.withdraw_handoff(self.sam, "ZF-1")
        with clock(300):
            self.offer()
        with clock(360):
            self.store.accept_handoff(
                self.pam, "ZF-1", metadata=change_metadata(self.store, "ZF-1")
            )
        with clock(420):
            self.store.complete_handoff(self.pam, "ZF-1", "SYN action complete")
        h = self.history("ZF-1")
        self.assertEqual([w["elapsed_seconds"] for w in h["handoff_waits"]], [120, 60, 60])
        self.assertEqual([e["version"] for e in h["events"]], list(range(1, 9)))

    def test_actual_stage_write_and_audit_failures_rollback_then_retry_once(self) -> None:
        self.prepare_advance()
        for operation in ("advance", "return", "reopen"):
            with self.subTest(operation=operation):
                self.check_stage_failure(operation)

    def check_stage_failure(self, operation: str) -> None:
        store = self.store
        cid = "ZF-2" if operation == "reopen" else "ZF-3"
        action = {"advance": "advance", "return": "return_case", "reopen": "reopen_case"}[operation]

        def write() -> None:
            if operation == "advance":
                store.advance(self.pam, cid)
            elif operation == "return":
                store.return_case(
                    self.pam,
                    cid,
                    "Resident paused works",
                    "SYN pause",
                    change_metadata(store, cid) | {"next_action": "SYN call"},
                )
            else:
                store.reopen_case(
                    self.pam,
                    cid,
                    "SYN aftercare",
                    change_metadata(store, cid) | {"next_action": "SYN investigate"},
                )

        before, audit = store.detail(cid), list(store.audit_entries())
        for failure in ("save", "audit"):
            target = (
                "save"
                if failure == "save"
                else ("_append_audit" if hasattr(store, "db") else "audit")
            )
            original = getattr(store, target)

            def fail(*args: Any, original: Any = original, failure: str = failure) -> None:
                if failure == "audit":
                    original(*args)
                raise OSError("SYN stage write failure")

            with clock(0), patch.object(store, target, side_effect=fail):
                with self.assertRaisesRegex(OSError, "stage write failure"):
                    write()
            self.assertEqual(self.open_store().detail(cid), before)
            self.assertEqual(list(store.audit_entries()), audit)
        with clock(60):
            write()
        self.assertEqual(self.success_count(action), 1)
        self.assertEqual(
            len(self.open_store().detail(cid)["returns"]), len(before.get("returns", [])) + 1
        )
        self.assertTrue(store.verify_audit())

    def test_actual_quality_remediation_and_independent_handover_versions(self) -> None:
        with clock(0):
            self.submit()
        with clock(30):
            self.store.return_quality(QI, "ZF-3", 0, "SYN gap", "SYN defect", "SYN team")
        with clock(60):
            self.store.record_fix(self.sam, "ZF-3", 0, "SYN fitter", "SYN photo version2")
        with self.assertRaises(PermissionError):
            self.store.reinspect_quality(self.sam, "ZF-3", 0, "pass")
        with clock(120):
            self.store.reinspect_quality(QI, "ZF-3", 0, "pass", "SYN independent")
        with clock(180):
            self.store.hand_over_quality(self.sam, "ZF-3", 0, "SYN guide", True)
        h = self.history()
        self.assertEqual(
            [e["kind"] for e in h["events"]],
            [
                "quality_submitted",
                "quality_returned",
                "quality_fixed",
                "quality_accepted",
                "quality_handover",
            ],
        )
        self.assertEqual(h["accepted_handovers"][0]["elapsed_seconds"], 60)

    def test_legacy_stage_minute_precision_remains_unknown_in_append_order(self) -> None:
        self.prepare_advance()
        with clock(45):
            self.store.advance(self.pam, "ZF-3")
        with clock(50):
            self.store.return_case(
                self.pam,
                "ZF-3",
                "Resident paused works",
                "SYN pause",
                change_metadata(self.store, "ZF-3") | {"next_action": "SYN call"},
            )
        with clock(75):
            self.store.return_case(
                self.pam,
                "ZF-3",
                "Contacting resident",
                "SYN contact",
                change_metadata(self.store, "ZF-3") | {"next_action": "SYN call"},
            )
        case = copy.deepcopy(self.store.cases["ZF-3"])
        case["returns"][1]["at"] = "2026-10-17T10:00+00:00"
        before = copy.deepcopy(case)
        result = progress.history(case, BASE + timedelta(seconds=600), None)
        self.assertEqual([e["version"] for e in result["events"]], [1, 2, 3])
        self.assertTrue(all(i["elapsed_seconds"] is None for i in result["stage_intervals"]))
        self.assertNotIn("contradictory_event_order", [e["code"] for e in result["exceptions"]])
        self.assertIn("unknown_event_precision", [e["code"] for e in result["exceptions"]])
        bounded = progress.history(case, BASE + timedelta(seconds=55), None)
        self.assertIn("unknown_event_as_of", [e["code"] for e in bounded["exceptions"]])
        self.assertEqual(case, before)
        kind: Any
        for kind in ([], {}, 42):
            malformed = copy.deepcopy(case)
            malformed["returns"][0]["event_type"] = kind
            result = progress.history(malformed, BASE + timedelta(seconds=600), None)
            self.assertIn("unmappable_stage_event", [e["code"] for e in result["exceptions"]])
            self.assertTrue(all(i["elapsed_seconds"] is None for i in result["stage_intervals"]))


class SqliteCapture(JsonCapture):
    backend = "sqlite"

    def test_sql_rollback_and_failed_recovery_preserve_original_prefix_and_retry(self) -> None:
        with clock(0):
            self.offer()
        for metadata_path in (False, True):
            for failure in ("save", "audit"):
                with self.subTest(metadata=metadata_path, failure=failure):
                    action = "handoff_accepted" if metadata_path else "handoff_received"
                    before = self.store.detail("ZF-1")
                    prior = self.success_count("SYN_prior")
                    original = OSError("SYN original failure")
                    target = "save" if failure == "save" else "_append_audit"
                    store = self.store
                    db = store.db

                    class RecoveryFault:
                        armed = False

                        def __init__(self, connection: Any) -> None:
                            self.db = connection

                        def execute(self, sql: str, args: Any = ()) -> Any:
                            if self.armed and sql.startswith(("SELECT rowversion", "SELECT value")):
                                raise OSError("SYN recovery read failed")
                            return self.db.execute(sql, args)

                        def __getattr__(self, name: str) -> Any:
                            return getattr(self.db, name)

                    fault = RecoveryFault(db)

                    def fail(*args: Any, fault: Any = fault, original: OSError = original) -> None:
                        fault.armed = True
                        raise original

                    with store.lock:
                        store.audit(self.sam["email"], "SYN_prior", "ZF-1", "SYN preserved")
                        with (
                            patch.object(store, "db", fault),
                            patch.object(store, target, side_effect=fail),
                            self.assertLogs("zava_forward.core.change_provenance", level="ERROR"),
                        ):
                            with self.assertRaises(OSError) as caught:
                                if metadata_path:
                                    store.accept_handoff(
                                        self.pam, "ZF-1", metadata=change_metadata(store, "ZF-1")
                                    )
                                else:
                                    store.receive_handoff(self.pam, "ZF-1")
                            self.assertIs(caught.exception, original)
                            self.assertTrue(original.__notes__)
                            self.assertFalse(store.local.touched)
                            self.assertEqual([e[1] for e in store.local.pending], ["SYN_prior"])
                    self.assertEqual(self.success_count("SYN_prior"), prior + 1)
                    self.assertEqual(self.open_store().detail("ZF-1"), before)
                    self.assertEqual(self.success_count(action), 0)
        with clock(60):
            self.store.receive_handoff(self.pam, "ZF-1")
        with clock(180):
            self.store.accept_handoff(
                self.pam, "ZF-1", metadata=change_metadata(self.store, "ZF-1")
            )
        self.assertEqual(self.success_count("handoff_received"), 1)
        self.assertEqual(self.success_count("handoff_accepted"), 1)
        self.assertEqual(len(self.open_store().detail("ZF-1")["handoff_history"]), 3)
        self.assertTrue(self.store.verify_audit())

    def test_sql_postcommit_sync_failure_is_committed_once_second_connection_and_retry(
        self,
    ) -> None:
        self.prepare_advance()
        for operation in (
            "advance",
            "return",
            "resume",
            "reopen",
            "offer",
            "receive",
            "accept",
            "submit",
            "quality",
            "quality_handover",
        ):
            with self.subTest(operation=operation):
                other = self.open_store()
                store, save, sync = self.store, self.store.save, self.store._sync
                action = {
                    "advance": "advance",
                    "return": "return_case",
                    "resume": "return_case",
                    "reopen": "reopen_case",
                    "offer": "handoff_offered",
                    "receive": "handoff_received",
                    "accept": "handoff_accepted",
                    "submit": "quality_submitted",
                    "quality": "quality_accepted",
                    "quality_handover": "quality_handover",
                }[operation]
                prior_audits = self.success_count(action)
                committed = {"saved": False}
                cid = (
                    "ZF-2"
                    if operation == "reopen"
                    else (
                        "ZF-3"
                        if operation
                        in ("advance", "return", "resume", "submit", "quality", "quality_handover")
                        else "ZF-1"
                    )
                )
                stream = (
                    "returns"
                    if operation in ("advance", "return", "resume", "reopen")
                    else (
                        "quality"
                        if operation in ("submit", "quality", "quality_handover")
                        else "handoff_history"
                    )
                )

                def history_rows(target: Any, cid: str = cid, stream: str = stream) -> list[Record]:
                    detail = target.detail(cid)
                    if stream == "quality":
                        return detail["quality"][0]["history"] if detail.get("quality") else []
                    return list(detail.get(stream, []))

                prior_rows = copy.deepcopy(history_rows(store))
                kind = (
                    "return"
                    if operation in ("return", "resume")
                    else ("reopen" if operation == "reopen" else action)
                )

                def write(operation: str = operation, store: Any = store) -> None:
                    if operation == "advance":
                        store.advance(self.pam, "ZF-3")
                    elif operation == "return":
                        store.return_case(
                            self.pam,
                            "ZF-3",
                            "Resident paused works",
                            "SYN pause",
                            change_metadata(store, "ZF-3") | {"next_action": "SYN call"},
                        )
                    elif operation == "resume":
                        store.return_case(
                            self.pam,
                            "ZF-3",
                            "Contacting resident",
                            "SYN resumed contact",
                            change_metadata(store, "ZF-3") | {"next_action": "SYN call"},
                        )
                    elif operation == "reopen":
                        store.reopen_case(
                            self.pam,
                            "ZF-2",
                            "SYN aftercare",
                            change_metadata(store, "ZF-2") | {"next_action": "SYN inspect"},
                        )
                    elif operation == "offer":
                        self.offer()
                    elif operation == "receive":
                        store.receive_handoff(self.pam, "ZF-1")
                    elif operation == "accept":
                        store.accept_handoff(
                            self.pam, "ZF-1", metadata=change_metadata(store, "ZF-1")
                        )
                    elif operation == "submit":
                        self.submit()
                    elif operation == "quality":
                        store.accept_quality(QI, "ZF-3", 0, "SYN independent")
                    else:
                        store.hand_over_quality(self.sam, "ZF-3", 0, "SYN guide", True)

                def concurrent_save(
                    other: Any = other,
                    operation: str = operation,
                    save: Any = save,
                    committed: dict[str, bool] = committed,
                ) -> None:
                    with other.lock:
                        other._case("ZF-5")["reason"] = "SYN second writer " + operation
                        other.save()
                    committed["saved"] = True
                    save()

                def failed_sync(
                    committed: dict[str, bool] = committed,
                    sync: Any = sync,
                ) -> None:
                    if committed["saved"]:
                        raise OSError("SYN post-COMMIT sync failed")
                    sync()

                logger = (
                    "zava_forward.core.quality"
                    if operation in ("submit", "quality", "quality_handover")
                    else "zava_forward.core.change_provenance"
                )
                with (
                    clock(60),
                    patch.object(store, "save", side_effect=concurrent_save),
                    patch.object(store, "_sync", side_effect=failed_sync),
                    self.assertLogs(logger, level="ERROR"),
                ):
                    with self.assertRaisesRegex(RuntimeError, "committed"):
                        write()
                self.assertEqual(self.success_count(action), prior_audits + 1)
                self.assertFalse(store.local.pending)
                self.assertFalse(store.local.touched)
                restarted = self.open_store()
                self.assertTrue(restarted.verify_audit())
                self.assertEqual(
                    sum(e["action"] == action for e in restarted.audit_entries()),
                    prior_audits + 1,
                )
                rows = history_rows(store)
                self.assertEqual(len(rows), len(prior_rows) + 1)
                self.assertEqual(rows[:-1], prior_rows)
                self.assertEqual(rows[-1]["version"], len(prior_rows) + 1)
                self.assertEqual(rows[-1]["event_type"], kind)
                self.assertEqual(history_rows(other), rows)
                self.assertEqual(history_rows(restarted), rows)
                self.assertFalse(
                    any(e["action"] == action + "_rejected" for e in restarted.audit_entries())
                )
                with self.assertRaises(ValueError):
                    write()
                self.assertEqual(self.success_count(action), prior_audits + 1)
                self.assertEqual(history_rows(store), rows)
                self.assertEqual(history_rows(other), rows)
                self.assertEqual(history_rows(self.open_store()), rows)


@unittest.skipUnless(os.environ.get("ZF_CAPTURE_MSSQL") == "1", "Opt-in task-owned MSSQL")
class MssqlCapture(SqliteCapture):
    backend = "mssql"
