"""E2 regressions for issue 1288 (independent findings after E1). Synthetic data, SQLite or a
disposable SQL Server, a real Ai client against a loopback TLS peer and local MOCK providers. No
live model call, no Azure, no private data.

F1 captured readings are never transmitted by a real Ai client (enforced fail-closed boundary);
F2 a durable cursor lets a long adoption history complete within the unchanged per-scan cap;
F3 forecast writes nothing; F4 rotation out of a bounded capture is not deletion."""

import atexit
import importlib
import json
import os
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import release_support
from zava_forward.core import ai_consumption, rai_release
from zava_forward.core import assistants as assistants_module
from zava_forward.core.ai import Ai, may_carry_captured_readings

import test_assistants as ta
import test_quality_sensors_c7 as c7
import test_quality_sensors_e1 as e1

dispatch = importlib.import_module("zava_forward.agents.dispatch")
server = importlib.import_module("zava_forward.api.server")

OPENSSL = shutil.which("openssl")
CERTS: dict[str, str] = {}


def certificate() -> str:
    if "dir" not in CERTS:
        directory = tempfile.mkdtemp(prefix="zf-e2-tls-")
        CERTS["dir"] = directory
        atexit.register(shutil.rmtree, directory, True)
        assert OPENSSL is not None
        subprocess.run(
            [
                OPENSSL,
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-days",
                "1",
                "-keyout",
                f"{directory}/key.pem",
                "-out",
                f"{directory}/cert.pem",
                "-subj",
                "/CN=127.0.0.1",
                "-addext",
                "subjectAltName=IP:127.0.0.1",
            ],
            check=True,
            capture_output=True,
        )
    return CERTS["dir"]


class TlsPeer:
    """A real TLS server on loopback that counts TCP accepts and decrypted request bytes and
    reads the request in small slow reads, so a send to it is genuinely partial."""

    def __init__(self, trickle: bool = True) -> None:
        import socket

        directory = certificate()
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(f"{directory}/cert.pem", f"{directory}/key.pem")
        self.cert = f"{directory}/cert.pem"
        self.accepts, self.bytes, self.trickle = 0, 0, trickle
        self.sock = socket.socket()
        if trickle:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(8)
        self.sock.settimeout(0.2)
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.serve, daemon=True)
        self.thread.start()

    @property
    def endpoint(self) -> str:
        return f"https://127.0.0.1:{self.sock.getsockname()[1]}"

    def serve(self) -> None:
        while not self.stop.is_set():
            try:
                raw, _ = self.sock.accept()
            except (TimeoutError, OSError):
                continue
            self.accepts += 1
            threading.Thread(target=self.handle, args=(raw,), daemon=True).start()

    def handle(self, raw: Any) -> None:
        try:
            conn = self.context.wrap_socket(raw, server_side=True)
            conn.settimeout(5)
            data = b""
            while b"\r\n\r\n" not in data:
                data += conn.recv(512)
            head, _, body = data.partition(b"\r\n\r\n")
            self.bytes += len(body)
            size = int(
                [h for h in head.split(b"\r\n") if h.lower().startswith(b"content-length")][
                    0
                ].split(b":")[1]
            )
            while len(body) < size:
                chunk = conn.recv(256 if self.trickle else 65536)
                body += chunk
                self.bytes += len(chunk)
                if self.trickle:
                    time.sleep(0.002)
            out = b'{"model":"test-model","choices":[{"message":{"content":"{}"}}],"usage":{}}'
            conn.sendall(
                b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: "
                + str(len(out)).encode()
                + b"\r\nConnection: close\r\n\r\n"
                + out
            )
            conn.close()
        except Exception:  # noqa: BLE001 - a refused client simply has no data to read
            pass

    def close(self) -> None:
        self.stop.set()
        self.thread.join(5)
        self.sock.close()


class CountingMeter(c7.Meter):
    def __init__(self, before: Callable[[], object] | None = None) -> None:
        super().__init__(before)
        self.reserved = self.checked = 0

    def reserve(self, *args: object, **kwargs: object) -> str:
        self.reserved += 1
        return super().reserve(*args, **kwargs)

    def dispatch_check(self, rid: str) -> None:
        self.checked += 1
        super().dispatch_check(rid)


@unittest.skipUnless(OPENSSL, "needs the openssl CLI to build a loopback certificate")
class Boundary(e1.GateBase):
    """F1: no real Ai request carries captured readings, however the final check is suspended."""

    def tls_ai(
        self, before: Callable[[], object] | None = None, trickle: bool = True
    ) -> tuple[TlsPeer, Ai]:
        peer = TlsPeer(trickle)
        self.addCleanup(peer.close)
        patcher = patch.dict(os.environ, {"SSL_CERT_FILE": peer.cert})
        patcher.start()
        self.addCleanup(patcher.stop)
        # urllib caches its default opener (and its trust store) across tests
        opener = patch.object(urllib.request, "_opener", None)
        opener.start()
        self.addCleanup(opener.stop)
        ai = Ai()
        ai.endpoint, ai.token, ai.expires = peer.endpoint, "t", time.time() + 3600
        meter = CountingMeter(before)
        self.meter = meter
        ai.consumption = meter
        self.tokens: list[int] = []
        real_token = ai._token

        def counted_token() -> str:
            self.tokens.append(1)
            token: str = real_token()
            return token

        ai._token = counted_token
        self.store.ai = ai
        release_support.install(self.store, cls="actual")
        return peer, ai

    def test_a_non_captured_request_reaches_the_trickling_tls_peer(self) -> None:
        peer, ai = self.tls_ai()
        body = "x" * 20000
        envelope = ai.evidence("system", body)
        self.assertEqual(envelope["outcome"], "returned")
        self.assertGreaterEqual(peer.accepts, 1)
        self.assertGreater(peer.bytes, 20000)
        self.assertEqual((self.meter.reserved, self.meter.checked), (1, 1))
        self.assertEqual(len(self.tokens), 1)

    def test_captured_readings_are_refused_before_any_meter_token_or_socket(self) -> None:
        peer, ai = self.tls_ai()
        with ai_consumption.captured_readings():
            envelope = ai.evidence("system", "x" * 20000)
        self.assertEqual(envelope["outcome"], "suspended-before-dispatch")
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertEqual((self.meter.reserved, self.meter.checked), (0, 0))
        self.assertEqual(self.tokens, [])

    def test_the_assistant_dispatch_holds_captured_readings_with_a_manual_route(self) -> None:
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        peer, ai = self.tls_ai()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        task = self.service.detail(self.pm, tid)
        self.assertNotEqual(task["state"], "ready")
        self.assertIn("cannot be sent to a real AI model", task.get("reason") or "")
        self.assertIn("manual route", task.get("reason") or "")
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertEqual((self.meter.reserved, self.meter.checked), (0, 0))
        self.assertEqual(self.tokens, [])

    def test_no_spoofed_simulation_claim_releases_captured_readings_to_a_real_ai(self) -> None:
        # E3: SYN naming, demo-profile and chat switches, an arbitrary dataset path and
        # free text saying "synthetic" are all inference; none may open the real route.
        spoof = {
            "ZF_CHAT_DEMO_ACTIVATION": "approved-2026-11-03",
            "ZF_DEPLOYMENT_PROFILE": "demo",
            "ZF_DATA": os.path.join(tempfile.gettempdir(), "synthetic-simulation-dataset.json"),
            "ZF_SIMULATION": "1",
        }
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        peer, ai = self.tls_ai()
        with patch.dict(os.environ, spoof):
            self.service.scan()
            (tid,) = self.quality_task()
            self.assertTrue(self.service.execute(tid))
            request = assistants_module.build_request(self.service.detail(self.pm, tid))
        self.assertIn("LIVE-", request[1])
        task = self.service.detail(self.pm, tid)
        self.assertNotEqual(task["state"], "ready")
        self.assertIn("cannot be sent to a real AI model", task.get("reason") or "")
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertEqual((self.meter.reserved, self.meter.checked), (0, 0))
        self.assertEqual(self.tokens, [])

    def withdraw_in_another_process(self) -> float:
        script = (
            "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],timeout=20);"
            "c.execute('UPDATE assistant_dispatch_gate SET expires_at=expires_at-1000');"
            "c.execute(sys.argv[2],(sys.argv[3],));c.commit()"
        )
        sql, sensor = self.withdraw_sql()
        started = time.monotonic()
        subprocess.run(
            [sys.executable, "-c", script, str(self.dbpath), sql, sensor],
            check=True,
            timeout=30,
            capture_output=True,
        )
        return time.monotonic() - started

    def test_a_suspension_at_the_old_final_check_with_another_process_withdrawal_sends_nothing(
        self,
    ) -> None:
        if self.service.mssql:
            self.skipTest("the cross-process SQLite withdrawal is SQLite-only")
        reached: list[float] = []
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        peer, ai = self.tls_ai(before=lambda: reached.append(self.withdraw_in_another_process()))
        self.service.scan()
        (tid,) = self.quality_task()
        self.service.execute(tid)
        self.assertEqual(reached, [])
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertNotEqual(self.service.detail(self.pm, tid)["state"], "ready")
        # No gate row is held, so a later withdrawal by another process is not delayed.
        self.assertLess(self.withdraw_in_another_process(), 10)
        self.assertNotEqual(self.consent_now(), "granted")

    def test_the_agents_worker_never_gives_captured_readings_to_a_real_ai(self) -> None:
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        peer, ai = self.tls_ai()
        self.service.scan()
        (tid,) = self.quality_task()
        with self.service.transaction() as db:
            task = self.service._row(db, tid)
        self.assertTrue(self.service._captured_sensors(task))
        limits = self.service.limits
        worker = dispatch.AgentWorker(dispatch.foundry_provider(ai))
        for _ in range(2):  # a redelivery behaves the same way
            result = worker.handle(dispatch.TaskMessage.from_task(task, limits), limits)
            self.assertIsNotNone(result)
            self.assertNotEqual(result.envelope.get("outcome"), "returned")
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertEqual((self.meter.reserved, self.meter.checked), (0, 0))

    def test_the_api_composition_applies_the_same_policy(self) -> None:
        peer, ai = self.tls_ai()
        app = server.App(self.store)
        self.addCleanup(app.assistants.stop)
        with ai_consumption.captured_readings():
            envelope = app.assistants.provider("system", "user", 50, 5)
        self.assertNotEqual(envelope.get("outcome"), "returned")
        self.assertEqual((peer.accepts, peer.bytes), (0, 0))
        self.assertFalse(may_carry_captured_readings(ai))

        class Silent:
            sends_no_bytes = True

            def evidence(self, *args: object) -> dict[str, Any]:
                return dict(outcome="returned", usage=None, source="unverified", text=None)

        class Undeclared:
            def evidence(self, *args: object) -> dict[str, Any]:
                raise AssertionError("must not be called")

        self.store.ai = Silent()
        self.assertTrue(may_carry_captured_readings(self.store.ai))
        with ai_consumption.captured_readings():
            self.assertEqual(app.assistants.provider("s", "u", 50, 5)["outcome"], "returned")
        self.store.ai = Undeclared()
        with ai_consumption.captured_readings():
            self.assertNotEqual(app.assistants.provider("s", "u", 50, 5).get("outcome"), "returned")

    def test_a_non_transmitting_mock_still_serves_the_demo_path(self) -> None:
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        self.assertEqual(self.service.detail(self.pm, tid)["state"], "ready")
        self.assertEqual(self.provider.calls, 1)


class Cursor(e1.AdoptionHelpers):
    """F2: history beyond the unchanged 100-row per-scan cap progresses by a durable cursor."""

    def history(self, manual: int = 120) -> str:
        first = self.legacy(manual)
        with self.service.transaction() as db:
            raw = db.execute(
                "SELECT body,signature FROM assistant_tasks WHERE id=?", (first,)
            ).fetchone()
            qualifying = json.loads(raw[0])
            body = json.loads(raw[0])
            body["dispatch"] = dict(body.get("dispatch") or {}, trigger="requested")
            db.execute("UPDATE assistant_tasks SET body=? WHERE id=?", (json.dumps(body), first))
            db.execute(
                "INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,"
                "owner,lease_until,attempts,not_before,revision,dispatched)"
                " VALUES ('oldzzz','assessment-preparation','ZF-1',?,?,'ready',1,'',0,1,0,1,1.0)",
                (raw[1], json.dumps(qualifying)),
            )
        return first

    def scan_again(self, service: Any = None) -> dict[str, Any]:
        service = service or self.service
        service.scan_cursor = ""
        report: dict[str, Any] = service.scan()
        return report

    def slot(self) -> Any:
        with self.service.transaction() as db:
            return db.execute(
                "SELECT signature,task_id FROM assistant_schedule"
                " WHERE capability='assessment-preparation'"
                " AND case_id='ZF-1'"
            ).fetchone()

    def test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts(
        self,
    ) -> None:
        self.assertEqual(
            assistants_module.Assistants.ADOPT_ROWS * assistants_module.Assistants.ADOPT_PAGES, 100
        )
        self.history()
        self.complete_documents("1")
        calls = self.provider.calls
        report = self.scan_again()
        self.assertIn("assessment-preparation:ZF-1", report["incomplete_history"])
        self.assertEqual(len(self.assessments()), 1)
        self.assertEqual(self.slot()[0], "incomplete-history")
        restarted = self.other()
        report = self.scan_again(restarted)
        self.assertIn("assessment-preparation:ZF-1", report["incomplete_history"])
        cursor = self.slot()[1]
        self.assertTrue(cursor.startswith("old"), cursor)  # progress, not the same prefix again
        # A retry rewrites `dispatched`; the immutable id walk is not reordered by it.
        self.direct(
            "UPDATE assistant_tasks SET dispatched=?,revision=revision+1 WHERE id='oldzzz'",
            time.time() + 999,
        )
        report = self.scan_again(self.other())
        self.assertNotIn("assessment-preparation:ZF-1", report.get("incomplete_history", []))
        self.assertEqual(len(self.assessments()), 2)
        self.assertEqual(self.provider.calls, calls)

    def test_every_page_reads_strictly_after_the_stored_cursor(self) -> None:
        self.history()
        self.complete_documents("1")
        seen: list[str | None] = []
        real = assistants_module.Assistants._adopt

        def spy(service: Any, db: Any, cap: str, case_id: str, cursor: str | None = None) -> Any:
            seen.append(cursor)
            return real(service, db, cap, case_id, cursor)

        with patch.object(assistants_module.Assistants, "_adopt", spy):
            for _ in range(3):
                self.scan_again()
        starts = [c for c in seen if c is not None]
        self.assertEqual(starts[0], "")
        self.assertGreater(starts[1], starts[0])


class ForecastPurity(e1.AdoptionHelpers):
    """F3: a forecast is read-only for schedule, release, event and in-memory state."""

    TABLES = (
        "assistant_schedule",
        "assistant_tasks",
        "assistant_events",
        "assistant_releases",
        "assistant_allowance",
        "assistant_attempts",
        "assistant_dispatch_gate",
    )

    def dump(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        with self.service.transaction() as db:
            for table in self.TABLES:
                try:
                    out[table] = sorted(map(repr, db.execute(f"SELECT * FROM {table}").fetchall()))
                except Exception:  # noqa: BLE001 - a table absent in this store compares as absent
                    out[table] = None
        out["memory"] = (sorted(self.service.incomplete), self.service.scan_cursor)
        return out

    def assert_pure(self) -> dict[str, Any]:
        before = self.dump()
        result: dict[str, Any] = self.service.forecast(self.pm)
        self.assertEqual(self.dump(), before)
        return result

    def test_a_fresh_store_forecast_changes_nothing_and_a_later_scan_still_adopts(self) -> None:
        self.ready()
        result = self.assert_pure()
        self.assertTrue(result["assistants"])
        self.service.scan()
        self.assertEqual(len(self.quality_task()), 1)

    def test_a_legacy_store_forecast_changes_nothing(self) -> None:
        self.legacy(8)
        self.complete_documents("1")
        self.assert_pure()
        self.scan_legacy()
        self.assertEqual(len(self.assessments()), 2)

    def scan_legacy(self) -> None:
        self.service.scan_cursor = ""
        self.service.scan()

    def test_a_persisted_incomplete_slot_and_the_held_marker_are_not_changed(self) -> None:
        self.legacy(8)
        self.complete_documents("1")
        with patch.object(type(self.service), "ADOPT_PAGES", 1):
            self.scan_legacy()
            self.service.incomplete.add(("assessment-preparation", "ZF-1"))
            self.assert_pure()
            self.assertTrue(self.service.incomplete)
            with self.service.transaction() as db:
                self.assertEqual(
                    db.execute(
                        "SELECT COUNT(*) FROM assistant_schedule"
                        " WHERE signature='incomplete-history'"
                    ).fetchone()[0],
                    1,
                )

    def test_a_material_release_change_is_not_revoked_by_a_forecast(self) -> None:
        self.ready()
        self.service.scan()
        with patch.object(rai_release, "changed_triggers", return_value=["model_version"]):
            before = self.dump()
            self.service.forecast(self.pm)
            self.assertEqual(self.dump(), before)
            with (
                self.service.transaction() as db
            ):  # control: a non-forecast assessment does record it
                self.service.release_reference(db, "quality-evidence")
            self.assertNotEqual(self.dump(), before)


class Rotation(c7.Base):
    """F4: a citation rotated out of the bounded capture is reported as such; rows still exist."""

    def test_rotation_is_not_deletion_and_a_real_delete_is_still_reported_apart(self) -> None:
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        cited = self.service.detail(self.pm, tid)["review_flag"]["readings"]
        for minute in [m for m in range(21) if m != 10]:
            self.add_live(minute)
        flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertEqual(flag["cited_comparison"]["state"], "changed")
        self.assertTrue(flag["cited_comparison"]["missing_ids"])
        self.assertIn("bounded capture", flag["cited_comparison"]["basis"])
        with self.service.transaction() as db:
            stored = [
                db.execute(
                    "SELECT COUNT(*) FROM sensor_reading WHERE sensor_id=? AND reading_id=?",
                    (r["sensor_id"], r["reading_id"]),
                ).fetchone()[0]
                for r in cited
            ]
        self.assertEqual(stored, [1] * len(cited))  # rotated out of the capture, not deleted
        gone = cited[0]
        with self.service.transaction() as db:
            db.execute(
                "DELETE FROM sensor_reading WHERE sensor_id=? AND reading_id=?",
                (gone["sensor_id"], gone["reading_id"]),
            )
            remaining = db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]
        self.assertGreater(remaining, 12)
        self.assertIs(
            self.service.detail(self.pm, tid)["review_flag"]["changed_since_capture"], True
        )


@c7.MSSQL
class MssqlForecastPurity(ta.MssqlFixture, ForecastPurity):
    pass


@c7.MSSQL
class MssqlCursor(ta.MssqlFixture, Cursor):
    pass


@c7.MSSQL
class MssqlBoundary(ta.MssqlFixture, Boundary):
    pass


@c7.MSSQL
class MssqlRotation(ta.MssqlFixture, Rotation):
    pass


if __name__ == "__main__":
    unittest.main()
