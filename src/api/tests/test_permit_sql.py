"""Worker-permit lock boundary and stored-attribution contracts on a real disposable SQL Server.

Skipped unless ZF_TEST_MSSQL=1. Admission requires the task-owned loopback container declared by
ZF_SQL_TASK_MANIFEST (see sqlguard). A second connection holds the task row while the actual
`issue_permit` waits on it, so the post-lock database clock, the expiry guards and the stored
attribution root are exercised across a real transaction and lock boundary. Constructed data only;
no provider, model or credential is reachable.
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import threading
import time
import traceback
import unittest
from collections.abc import Callable, Mapping
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest.mock import patch

import sqlguard
from zava_forward.core.ai import Ai
from zava_forward.core.ai_consumption import reference

import test_ai_consumption_api as base
import test_assistants as ta

CLAIMANT = "permit-claimant"
DB_NOW = (
    "SELECT DATEDIFF_BIG(MILLISECOND, CONVERT(datetime2,'1970-01-01'), SYSUTCDATETIME()) / 1000.0"
)
BLOCKED = (
    "SELECT r.session_id, r.blocking_session_id, r.database_id, r.wait_type, r.wait_resource, "
    "r.statement_start_offset, r.statement_end_offset, "
    "SUBSTRING(t.text, r.statement_start_offset / 2 + 1, "
    "((CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(t.text) "
    "ELSE r.statement_end_offset END - r.statement_start_offset) / 2) + 1) "
    "FROM sys.dm_exec_requests AS r CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS t "
    "WHERE r.blocking_session_id = ?"
)
APPLOCK = (
    "SELECT COUNT(*) FROM sys.dm_tran_locks WHERE request_session_id = ? "
    "AND resource_type = 'APPLICATION' AND request_status = 'GRANT'"
)
UPDATE_TEXT = "UPDATE assistant_tasks SET revision=revision+1"
OBSERVE_SECONDS = 10.0
JOIN_SECONDS = 15.0
POLL_SECONDS = 0.1
USAGE = dict(prompt_tokens=100, completion_tokens=20, total_tokens=120)


class InvalidWitness(Exception):
    """A setup, timing, DMV or cleanup witness is wrong: inconclusive, never a source verdict."""


def helpers() -> Any:
    """The existing borrowed helper bodies; never a module-level TestCase, so none is discovered."""
    return base.ConsumptionApi


def db_now(conn: Any) -> float:
    return float(conn.execute(DB_NOW).fetchone()[0])


def scalar(conn: Any, sql: str, *args: Any) -> Any:
    return conn.execute(sql, args).fetchone()[0]


def rollback_quietly(conn: Any, errors: list[str]) -> None:
    try:
        conn.execute("IF @@TRANCOUNT > 0 ROLLBACK TRAN")
    except Exception as error:
        errors.append(f"holder rollback failed: {error!r}")


def close_quietly(conn: Any, label: str, errors: list[str]) -> None:
    try:
        conn.close()
    except Exception as error:
        errors.append(f"{label} close failed: {error!r}")


SCRATCH_SCHEMA = "zf-scratch/1"
GENERAL_PURPOSE = {
    "/", "/tmp", "/var", "/var/tmp", "/dev/shm", "/home", "/root", "/usr", "/opt", "/mnt", "/srv",
}  # fmt: skip


def private_owned(path: Path, kind: str) -> os.stat_result:
    status = os.lstat(path)
    wanted = stat.S_ISDIR if kind == "dir" else stat.S_ISREG
    if not wanted(status.st_mode) or status.st_uid != os.getuid() or status.st_mode & 0o077:
        raise InvalidWitness(f"INVALID-SETUP: {path} is not a private owned {kind}")
    return status


def assert_isolated(environ: Mapping[str, str] | None = None, cwd: Path | None = None) -> None:
    """Every working path must equal the exact scratch identity the launcher wrote beforehand.

    A caller-chosen TMPDIR is never ownership evidence: the private manifest names the exact root
    and each exact path, and every actual value must resolve to it.
    """
    env = os.environ if environ is None else environ
    given = env.get("ZF_SCRATCH_MANIFEST")
    if not given or not Path(given).is_absolute():
        raise InvalidWitness("INVALID-SETUP: ZF_SCRATCH_MANIFEST must be an absolute path")
    private_owned(Path(given), "file")
    manifest = json.loads(Path(given).read_text())
    if manifest.get("schema") != SCRATCH_SCHEMA:
        raise InvalidWitness("INVALID-SETUP: unknown scratch manifest schema")
    root = Path(str(manifest.get("root")))
    if not root.is_absolute() or root.resolve() != root:
        raise InvalidWitness("INVALID-SETUP: the scratch root is not an exact resolved path")
    if str(root) in GENERAL_PURPOSE or len(root.parts) < 4:
        raise InvalidWitness("INVALID-SETUP: the scratch root is a general-purpose directory")
    status = private_owned(root, "dir")
    if manifest.get("root_id") != f"{status.st_dev}:{status.st_ino}":
        raise InvalidWitness("INVALID-SETUP: the scratch root identity does not match")
    actual = {
        "tmp": tempfile.gettempdir(),
        "home": env.get("HOME", ""),
        "data": env.get("ZF_DATA", ""),
        "state": env.get("ZF_STATE", ""),
        "cwd": str(Path.cwd() if cwd is None else cwd),
    }
    for name, value in actual.items():
        expected = Path(str(manifest.get(name)))
        if not value or not expected.is_absolute() or expected.resolve() != expected:
            raise InvalidWitness(f"INVALID-SETUP: the {name} scratch path is not exact")
        if (
            Path(value).resolve() != expected
            or expected == root
            or not expected.is_relative_to(root)
        ):
            raise InvalidWitness(f"INVALID-SETUP: {name} is not the manifest scratch path")
        private_owned(expected, "dir")


@unittest.skipUnless(
    os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)"
)
class MssqlPermitBoundary(unittest.TestCase):
    fixture: Any
    service: Any
    store: Any
    provider: Any
    inner: Any
    pm: dict[str, Any]
    clock: list[tuple[str, float]]

    @classmethod
    def setUpClass(cls) -> None:
        sqlguard.require_task_owned_loopback(os.environ)

    def setUp(self) -> None:
        assert_isolated()
        composite: Any = type("PermitSqlFixture", (ta.MssqlFixture, ta.Base), {})
        self.fixture = composite()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.store = self.fixture.store
        self.provider = self.fixture.provider
        self.pm = self.fixture.pm
        self.inner = Ai()
        self.inner.endpoint = "http://127.0.0.1:1"
        self.inner.model_version = "test-model"
        self.inner.model_version_strong = "test-model"
        self.inner.fast = "test"
        self.inner.strong = "capable"
        self.inner.consumption = self.service.consumption
        if self.inner.is_live("assessment-preparation") or not self.inner.configured:
            raise InvalidWitness("INVALID-SETUP: the Ai fixture is not the loopback one")
        self.clock = []
        original = self.service.now

        def recording(db: Any) -> float:
            value = float(original(db))
            self.clock.append((threading.current_thread().name, value))
            return value

        patched = patch.object(self.service, "now", recording)
        patched.start()
        self.addCleanup(patched.stop)

    def authority(self, *args: Any, **kwargs: Any) -> Any:
        return helpers().authority(self, *args, **kwargs)

    def records(self) -> Any:
        return helpers().records(self)

    def permit_setup(self, authority_seconds: float | None = None) -> Any:
        leased = helpers().permit_setup(self, authority_seconds)
        configured = self.inner.configuration("test", 0, 600)
        stored = [r for r in self.records() if r["kind"] == "authority"]
        if [r["configuration"] for r in stored] != [configured]:
            raise InvalidWitness("INVALID-SETUP: the authority does not bind the fixture Ai")
        return leased

    def permit_request(self, task: dict[str, Any]) -> Any:
        return helpers().permit_request(self, task)

    def reserved(self) -> Any:
        return helpers().reserved(self)

    def kinds(self, tid: str) -> Any:
        return helpers().kinds(self, tid)

    def lease(self, tid: str, seconds: float) -> None:
        helpers().lease(self, tid, seconds)

    def used_calls(self) -> int:
        return int(helpers().used_calls(self))

    def permitted_result(self, task: dict[str, Any], **extra: Any) -> bool:
        return bool(helpers().permitted_result(self, task, **extra))

    def of_kind(self, kind: str) -> list[dict[str, Any]]:
        return [r for r in self.records() if r["kind"] == kind]

    def stored_lease(self, tid: str) -> float:
        with self.service.transaction() as db:
            return float(scalar(db, "SELECT lease_until FROM assistant_tasks WHERE id=?", tid))

    def stored_end(self) -> float:
        (authority,) = self.of_kind("authority")
        return float(authority["end"])

    def settled(self, tid: str) -> dict[str, Any]:
        """Counts a conflicting or repeated result must leave unchanged."""
        with self.service.transaction() as db:
            allowance = db.execute(
                "SELECT id, used_calls, reserved_tokens FROM assistant_allowance ORDER BY id"
            ).fetchall()
            state = self.service._row(db, tid)["state"]
        return dict(
            completed=len(self.of_kind("completed")),
            output=len(self.of_kind("output")),
            allowance=[tuple(row) for row in allowance],
            state=state,
            rejected=self.kinds(tid).count("result-rejected"),
        )

    def claim_behind_lock(
        self,
        task: dict[str, Any],
        request: dict[str, Any],
        lease_seconds: float,
        release_at: Callable[[dict[str, Any]], float],
    ) -> dict[str, Any]:
        """Run the actual issue_permit while a separate connection holds the task row.

        The holder opens a plain transaction (no application lock) so the claimant takes the global
        application lock first and then waits on the row. Every acquisition registers its cleanup
        at once. Unwinding is observer close, holder rollback, holder close, then the join, so the
        holder is always released before the join.
        """
        errors: list[str] = []
        outcome: list[Any] = []
        failure: list[BaseException] = []
        running: threading.Thread | None = None
        primary: BaseException | None = None
        witness: dict[str, Any] = {}

        def finish_worker() -> None:
            if running is None:
                return
            try:
                running.join(JOIN_SECONDS)
            except Exception as error:
                errors.append(f"worker join failed: {error!r}")
            if running.is_alive():
                errors.append("WORKER-STILL-LIVE")

        def claimant() -> None:
            try:
                outcome.append(
                    self.service.issue_permit(task["id"], task["owner"], task["fence"], request)
                )
            except BaseException as error:
                failure.append(error)

        try:
            with ExitStack() as stack:
                stack.callback(finish_worker)
                holder = self.store.assistant_connection()
                stack.callback(close_quietly, holder, "holder", errors)
                stack.callback(rollback_quietly, holder, errors)
                observer = self.store.assistant_connection()
                stack.callback(close_quietly, observer, "observer", errors)

                self.lease(task["id"], lease_seconds)
                witness["lease_until"] = self.stored_lease(task["id"])
                witness["L0"] = witness["lease_until"] - lease_seconds
                holder.execute("BEGIN TRAN")
                held = holder.execute(
                    "UPDATE assistant_tasks SET revision=revision+1 WHERE id=?", (task["id"],)
                )
                if held.rowcount != 1:
                    raise InvalidWitness("INVALID-SETUP: the holder did not lock the task row")
                witness["holder_spid"] = int(scalar(holder, "SELECT @@SPID"))
                witness["database_id"] = int(scalar(holder, "SELECT DB_ID()"))
                if int(scalar(holder, "SELECT @@TRANCOUNT")) != 1:
                    raise InvalidWitness("INVALID-SETUP: the holder is not in one transaction")
                witness["t_lock"] = db_now(holder)

                thread = threading.Thread(target=claimant, name=CLAIMANT, daemon=True)
                thread.start()
                running = thread
                row = self.observe_block(observer, witness)
                witness["blocked"] = dict(
                    session=int(row[0]),
                    blocking=int(row[1]),
                    database=int(row[2]),
                    wait_type=str(row[3]),
                    wait_resource=str(row[4]),
                    statement_start=int(row[5]),
                    statement_end=int(row[6]),
                    statement=str(row[7]).strip()[:120],
                    applock_granted=int(scalar(observer, APPLOCK, int(row[0]))),
                )
                witness["obs"] = db_now(observer)
                self.check_block(witness)

                target = release_at(witness)
                if target <= witness["obs"]:
                    raise InvalidWitness("INVALID-TIMING: release precedes the observation")
                deadline = time.monotonic() + (target - witness["obs"]) + OBSERVE_SECONDS
                while db_now(holder) < target:
                    if time.monotonic() > deadline:
                        raise InvalidWitness("INVALID-TIMING: the release gate was not reached")
                    time.sleep(POLL_SECONDS)
                self.check_holder(holder, witness)
                witness["t_pre"] = db_now(holder)
                holder.execute("IF @@TRANCOUNT > 0 ROLLBACK TRAN")
                witness["t_post"] = db_now(observer)
                if int(scalar(holder, "SELECT @@TRANCOUNT")) != 0:
                    raise InvalidWitness("INVALID-SETUP: the holder did not release the row")
                thread.join(JOIN_SECONDS)
                if thread.is_alive():
                    raise InvalidWitness("WORKER-STILL-LIVE: the claimant did not finish")
        except BaseException as error:
            primary = error
        worker = failure[0] if failure else None
        if worker is not None and worker is not primary:
            if primary is None:
                primary = worker
            else:
                primary.add_note("WORKER-ERROR: " + "".join(traceback.format_exception(worker)))
        if errors:
            text = "CLEANUP-ERRORS: " + "; ".join(errors)
            if primary is None:
                raise InvalidWitness(text)
            primary.add_note(text)
            raise InvalidWitness(text) from primary
        if primary is not None:
            raise primary
        witness["result"] = outcome[0]
        witness["reads"] = [value for name, value in self.clock if name == CLAIMANT]
        return witness

    def observe_block(self, observer: Any, witness: dict[str, Any]) -> Any:
        deadline = time.monotonic() + OBSERVE_SECONDS
        while True:
            rows = observer.execute(BLOCKED, (witness["holder_spid"],)).fetchall()
            if rows:
                if len(rows) != 1:
                    raise InvalidWitness(
                        f"INVALID-WITNESS: {len(rows)} sessions block on the holder"
                    )
                return rows[0]
            if time.monotonic() > deadline:
                raise InvalidWitness("INVALID-WITNESS: no claimant blocked on the holder")
            time.sleep(POLL_SECONDS)

    def check_block(self, witness: dict[str, Any]) -> None:
        blocked = witness["blocked"]
        problems = []
        if blocked["blocking"] != witness["holder_spid"]:
            problems.append("blocker")
        if blocked["database"] != witness["database_id"]:
            problems.append("database")
        if not blocked["wait_type"].startswith("LCK_M_"):
            problems.append("wait type")
        if not blocked["wait_resource"].startswith("KEY:"):
            problems.append("wait resource")
        if UPDATE_TEXT not in blocked["statement"]:
            problems.append("statement")
        if blocked["applock_granted"] < 1:
            problems.append("application lock")
        if problems:
            raise InvalidWitness("INVALID-WITNESS: " + ", ".join(problems))

    def check_holder(self, holder: Any, witness: dict[str, Any]) -> None:
        spid = int(scalar(holder, "SELECT @@SPID"))
        count = int(scalar(holder, "SELECT @@TRANCOUNT"))
        held = int(
            scalar(
                holder,
                "SELECT COUNT(*) FROM sys.dm_tran_session_transactions WHERE session_id = ?",
                spid,
            )
        )
        if spid != witness["holder_spid"] or count != 1 or held < 1:
            raise InvalidWitness("INVALID-SETUP: the holder transaction is not continuous")

    def report(self, label: str, witness: dict[str, Any]) -> None:
        shown = {k: v for k, v in witness.items() if k != "result"}
        print("WITNESS", label, json.dumps(shown, sort_keys=True, default=str), flush=True)

    def test_lock_wait_crossing_the_lease_margin_refuses_without_a_reservation(self) -> None:
        task = self.permit_setup()
        request = self.permit_request(task)
        before = self.used_calls()
        w = self.claim_behind_lock(task, request, 42, lambda s: s["L0"] + 4.5)
        first = w["reads"][0] - w["L0"]
        self.report("E1-MARGIN", dict(w, first_read_offset=first))
        if not (w["t_lock"] <= w["L0"] + 1.5 and w["obs"] <= w["L0"] + 3.0):
            raise InvalidWitness("INVALID-TIMING: coordination headroom exceeded")
        if not (w["L0"] + 4.5 <= w["t_pre"] and w["t_post"] <= w["L0"] + 6.0):
            raise InvalidWitness("INVALID-TIMING: release outside the fixed window")
        self.assertEqual(w["result"], dict(permit=False, reason="lease-expiring"), "E1-MARGIN")
        self.assertGreaterEqual(w["reads"][0], w["t_pre"], "E1-MARGIN")
        self.assertEqual(self.reserved(), [], "E1-MARGIN")
        self.assertNotIn("permitted", self.kinds(task["id"]), "E1-MARGIN")
        self.assertEqual(self.used_calls(), before, "E1-MARGIN")

    def test_lock_wait_crossing_authority_expiry_refuses_and_refunds(self) -> None:
        task = self.permit_setup(authority_seconds=8)
        request = self.permit_request(task)
        end = self.stored_end()
        before = self.used_calls()
        w = self.claim_behind_lock(task, request, 120, lambda s: end - 1.5)
        self.report("E1-AUTHORITY", dict(w, end=end))
        if not (end - 1.5 <= w["t_pre"] and w["t_post"] <= end - 1.0):
            raise InvalidWitness("INVALID-TIMING: release outside the fixed window")
        # The last claimant read bounds the reservation read from above; it is not that read itself.
        if not w["reads"][-1] < end:
            raise InvalidWitness("INVALID-TIMING: the claimant ran past the authority end")
        self.assertEqual(
            w["result"], dict(permit=False, reason="authority-expiring"), "E1-AUTHORITY"
        )
        self.assertEqual(self.reserved(), [], "E1-AUTHORITY")
        self.assertNotIn("permitted", self.kinds(task["id"]), "E1-AUTHORITY")
        self.assertEqual(self.used_calls(), before - 1, "E1-AUTHORITY")
        self.assertEqual(self.kinds(task["id"]).count("permit-denied"), 1, "E1-AUTHORITY")

    def test_valid_window_after_a_real_lock_wait_grants_with_post_lock_time(self) -> None:
        task = self.permit_setup()
        request = self.permit_request(task)
        w = self.claim_behind_lock(task, request, 120, lambda s: s["obs"] + 1.0)
        self.report("E1-ISSUED-AT", w)
        if not w["obs"] + 1.0 <= w["t_pre"]:
            raise InvalidWitness("INVALID-TIMING: release before the planned gate")
        permit = w["result"]
        self.assertTrue(permit["permit"], "E1-ISSUED-AT")
        self.assertGreaterEqual(permit["issued_at"], w["t_pre"], "E1-ISSUED-AT")
        self.assertAlmostEqual(
            permit["lease_remaining"], w["lease_until"] - permit["issued_at"], 6, "E1-ISSUED-AT"
        )
        self.assertGreaterEqual(permit["dispatch_within_ms"], 1, "E1-ISSUED-AT")
        held = self.reserved()
        self.assertEqual([r["id"] for r in held], [permit["meter_id"]], "E1-ISSUED-AT")
        self.assertIn("permitted", self.kinds(task["id"]), "E1-ISSUED-AT")
        with self.service.transaction() as db:
            marker = self.service._markers(db, task["id"]).get("permitted")
            stored = scalar(
                db,
                "SELECT outcome FROM assistant_attempts WHERE id=?",
                f"{task['id']}:{task['fence']}",
            )
        self.assertIsNotNone(marker, "E1-ISSUED-AT")
        self.assertEqual(marker["issued_at"], permit["issued_at"], "E1-ISSUED-AT")
        self.assertEqual(stored, "sending", "E1-ISSUED-AT")
        again = self.service.issue_permit(task["id"], task["owner"], task["fence"], request)
        self.assertEqual(again, dict(permit=False, reason="duplicate-permit"), "E1-ISSUED-AT")
        self.assertEqual(len(self.reserved()), 1, "E1-ISSUED-AT")

    def test_an_unavailable_send_fence_refuses_without_a_reservation_or_a_marker(self) -> None:
        task = self.permit_setup()
        request = self.permit_request(task)
        before = self.used_calls()
        with self.service.transaction() as db:
            db.execute(
                "UPDATE assistant_attempts SET active_until=0 WHERE id=?",
                (f"{task['id']}:{task['fence']}",),
            )
        result = self.service.issue_permit(task["id"], task["owner"], task["fence"], request)
        self.assertEqual(result, dict(permit=False, reason="send-fence-refused"), "E1-FENCE")
        self.assertEqual(self.reserved(), [], "E1-FENCE")
        kinds = self.kinds(task["id"])
        self.assertIn("send-refused", kinds, "E1-FENCE")
        self.assertNotIn("permitted", kinds, "E1-FENCE")
        self.assertEqual(self.used_calls(), before - 1, "E1-FENCE")

    def test_permitted_result_binds_attribution_to_the_stored_reservation_root(self) -> None:
        label = "E2-STORED-ROOT"
        task = self.permit_setup()
        permit = self.service.issue_permit(
            task["id"], task["owner"], task["fence"], self.permit_request(task)
        )
        self.assertTrue(permit["permit"], label)
        self.assertTrue(self.permitted_result(task), label)
        root = self.reserved()[0]["root"]
        outputs = self.of_kind("output")
        self.assertEqual(len(outputs), 1, label)
        self.assertEqual(
            (outputs[0]["root"], outputs[0]["output"], outputs[0]["eligible"]),
            (root, reference(task["id"]), True),
            label,
        )
        stored = self.service.detail(self.pm, task["id"])
        self.assertEqual(stored["state"], "ready", label)
        self.assertEqual(stored["envelope"]["meter_root"], root, label)
        self.assertEqual(stored["envelope"]["meter_id"], permit["meter_id"], label)
        completed = self.of_kind("completed")
        self.assertEqual([r["id"] for r in completed], [permit["meter_id"]], label)
        for key, value in USAGE.items():
            self.assertEqual(completed[0]["tokens"][key], value, label)
        verified = self.fixture.verify(stored)
        self.service.review(
            self.pm, task["id"], "accept", verified["revision"], "Constructed review."
        )
        self.assertEqual(
            [r["output"] for r in self.of_kind("review")], [reference(task["id"])], label
        )
        report = self.service.consumption.report(start=base.START, end=base.END, as_of=base.END)
        self.assertEqual(report["accepted_proposals"], 1, label)
        counts = self.settled(task["id"])
        self.permitted_result(task)
        self.assertEqual(self.settled(task["id"]), counts, label)

    def test_permitted_result_rejects_conflicting_attribution_without_settling(self) -> None:
        task = self.permit_setup()
        permit = self.service.issue_permit(
            task["id"], task["owner"], task["fence"], self.permit_request(task)
        )
        self.assertTrue(permit["permit"], "E2-CONFLICT-SETUP")
        before = self.settled(task["id"])
        self.assertEqual(before["state"], "leased", "E2-CONFLICT-SETUP")
        with self.subTest("E2-CONFLICT-ID"):
            self.assertFalse(self.permitted_result(task, meter_id="a" * 64), "E2-CONFLICT-ID")
            self.assertEqual(
                self.settled(task["id"]),
                dict(before, rejected=before["rejected"] + 1),
                "E2-CONFLICT-ID",
            )
        with self.subTest("E2-CONFLICT-ROOT"):
            self.assertFalse(self.permitted_result(task, meter_root="a" * 64), "E2-CONFLICT-ROOT")
            self.assertEqual(
                self.settled(task["id"]),
                dict(before, rejected=before["rejected"] + 2),
                "E2-CONFLICT-ROOT",
            )
            self.assertTrue(
                self.permitted_result(task, meter_id=permit["meter_id"]), "E2-CONFLICT-ROOT"
            )
            matched = self.settled(task["id"])
            self.assertEqual(matched["completed"], before["completed"] + 1, "E2-CONFLICT-ROOT")
            self.permitted_result(task, meter_id=permit["meter_id"])
            self.assertEqual(self.settled(task["id"]), matched, "E2-CONFLICT-ROOT")

    def test_permitted_failure_without_root_settles_the_meter_and_publishes_no_output(
        self,
    ) -> None:
        label = "E2-FAILURE"
        task = self.permit_setup()
        permit = self.service.issue_permit(
            task["id"], task["owner"], task["fence"], self.permit_request(task)
        )
        self.assertTrue(permit["permit"], label)
        envelope = dict(outcome="provider-unavailable", source="unverified", usage=None)
        self.service.complete_result(
            task["id"], task["owner"], task["fence"], envelope, None, "Provider unavailable."
        )
        completed = self.of_kind("completed")
        self.assertEqual([r["id"] for r in completed], [permit["meter_id"]], label)
        self.assertEqual(completed[0]["outcome"], "provider-unavailable", label)
        self.assertIsNone(completed[0]["tokens"], label)
        self.assertIsNone(completed[0]["charge"], label)
        self.assertIs(completed[0]["held"], True, label)
        self.assertEqual(self.of_kind("output"), [], label)
        self.assertEqual(self.of_kind("review"), [], label)


if __name__ == "__main__":
    unittest.main()
