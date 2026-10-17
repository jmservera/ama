import csv
import hashlib
import io
import json
import logging
import os
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import dataset
from zava_forward.core import ai_tasks, insights
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import sensor_backfill as sb
from zava_forward.core.synthetic import sensor_stock as ss

DEVICE = "DEVICE-PRIVATE-SENTINEL-112"
RAW = "RAW-READING-PRIVATE-SENTINEL-112"
PACKET = dict(device_id=DEVICE, readings=[dict(value=RAW)])


class SensorPrivacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def store(self) -> Any:
        seed = self.root / "seed.json"
        seed.write_text(json.dumps(dataset.DATA))
        store = SqlStore(str(seed), str(self.root / "test.db"))
        self.addCleanup(store.db.close)
        return store

    def snapshot(self) -> Path:
        out = self.root / "snapshot"
        sb.write(out, homes=1, days=1, cadence=360)
        return out

    def assert_clean(self, value: object) -> None:
        text = json.dumps(value, default=str)
        self.assertNotIn(DEVICE, text)
        self.assertNotIn(RAW, text)

    def refuse(self, out: Path, **kwargs: Any) -> None:
        connection, schema = Mock(), Mock()
        connection.execute.return_value.rowcount = 1
        with self.assertRaises(ValueError) as error:
            sb.load_into(connection, out, create_schema=schema, **kwargs)
        schema.assert_not_called()
        connection.execute.assert_not_called()
        self.assert_clean(str(error.exception))

    def test_chat_actual_request_excludes_nested_home_diagnostics(self) -> None:
        store = self.store()
        user = store.staff["sam@example.test"]
        with store.lock:
            c = store._case("ZF-1")
            c["home"]["diagnostics"] = {"nested": PACKET}
            c["monitoring"] = PACKET
            store.save()
        captured: list[str] = []

        def model(system: str, prompt: str) -> str:
            captured.extend([system, prompt])
            return json.dumps(dict(answer="See the stage.", citations=["ZF-1/stage"]))

        thread = store.chat_create_thread(user, case_id="ZF-1")
        panel = ChatPanel(
            ChatIsolation(
                store,
                env={
                    "CHAT_DPIA_REF": "SYNTHETIC-CHAT-TEST",
                    "CHAT_LAWFUL_BASIS_REF": "SYNTHETIC-CHAT-TEST",
                    "CHAT_NOTICE_REF": "SYNTHETIC-CHAT-TEST",
                },
            ),
            model,
        )
        panel.ask(user, thread["id"], "What stage is this case?")
        self.assertTrue(captured)
        self.assert_clean(captured)
        self.assertIn("Contacting resident", captured[-1])
        self.assertEqual(store.detail("ZF-1", user)["home"]["diagnostics"]["nested"], PACKET)

    def test_legacy_assembled_requests_ignore_unselected_sensor_payloads(self) -> None:
        store = self.store()
        c = store.cases["ZF-1"]
        c["home"]["diagnostics"] = PACKET
        c["monitoring"] = PACKET
        user = store.staff["sam@example.test"]
        store.ai.endpoint = "https://offline.invalid"
        store.ai.gate = store.ai.release = None
        with patch.object(store.ai, "_chat", return_value="No cited proposal.") as model:
            store.ai_run(user, "ZF-1", "summary")
            self.assertTrue(model.called)
            self.assert_clean(model.call_args.args)

    def test_malformed_selected_fields_refuse_before_ai_call(self) -> None:
        store = self.store()
        user = store.staff["sam@example.test"]
        with patch.object(store.ai, "_chat") as model:
            store.cases["ZF-1"]["home"]["address"] = PACKET
            with self.assertRaises(ValueError) as error:
                store.ai_run(user, "ZF-1", "summary")
            model.assert_not_called()
            self.assert_clean(str(error.exception))

    def test_actual_legacy_transport_body_is_closed(self) -> None:
        store = self.store()
        store.cases["ZF-1"]["home"]["opaque"] = {"deep": [PACKET]}
        store.cases["ZF-1"]["sensor_analysis"] = PACKET
        store.ai.endpoint = "https://offline.invalid"
        store.ai.gate = store.ai.release = None
        body = json.dumps({"choices": [{"message": {"content": "Not a cited proposal."}}]}).encode()
        with (
            patch.object(store.ai, "_token", return_value="offline-test"),
            patch("urllib.request.urlopen", return_value=io.BytesIO(body)) as transport,
        ):
            store.ai_run(store.staff["sam@example.test"], "ZF-1", "summary")
        request = transport.call_args.args[0]
        assembled = json.loads(request.data)
        self.assert_clean(assembled)
        self.assertEqual([m["role"] for m in assembled["messages"]], ["system", "user"])
        self.assertIn("Contacting resident", assembled["messages"][1]["content"])

    def test_raw_status_inputs_refuse_before_chat_and_briefing_dispatch(self) -> None:
        store = self.store()
        user = store.staff["sam@example.test"]
        store.ai.endpoint = "https://offline.invalid"
        store.ai.gate = store.ai.release = None
        for cid, field in (("ZF-1", "reason"), ("ZF-4", "owner")):
            with self.subTest(field=field):
                with store.lock:
                    c = store._case(cid)
                    source = c if field == "reason" else c["hazards"][0]
                    original = source[field]
                    source[field] = PACKET
                    store.save()
                thread = store.chat_create_thread(user, case_id=cid)
                model = Mock()
                panel = ChatPanel(
                    ChatIsolation(
                        store,
                        env={
                            "CHAT_DPIA_REF": "SYNTHETIC-CHAT-TEST",
                            "CHAT_LAWFUL_BASIS_REF": "SYNTHETIC-CHAT-TEST",
                            "CHAT_NOTICE_REF": "SYNTHETIC-CHAT-TEST",
                        },
                    ),
                    model,
                )
                with self.subTest(route="chat"):
                    with self.assertRaises(ValueError) as error:
                        panel.ask(user, thread["id"], "What stage is this case?")
                    model.assert_not_called()
                    self.assert_clean(str(error.exception))
                with (
                    self.subTest(route="briefing"),
                    patch.object(store.ai, "_chat", return_value="Synthetic proposal") as provider,
                ):
                    with self.assertRaises(ValueError) as error:
                        store.briefing(user)
                    provider.assert_not_called()
                    self.assert_clean(str(error.exception))
                with store.lock:
                    c = store._case(cid)
                    source = c if field == "reason" else c["hazards"][0]
                    self.assertEqual(source[field], PACKET)
                    source[field] = original
                    store.save()

    def test_document_metadata_refuses_before_transport_and_audit(self) -> None:
        store = self.store()
        user = store.staff["sam@example.test"]
        doc = dict(
            id="SYN-112-DOC",
            name=PACKET,
            mime="text/plain",
            kind="Other",
            at="2026-01-01",
            by="Synthetic",
            generated=False,
        )
        with store.lock:
            store._case("ZF-1")["documents"].append(doc)
            store.save()
        store.ai.endpoint = "https://offline.invalid"
        store.ai.gate = store.ai.release = None
        with (
            patch.object(store.ai, "_chat", return_value="Synthetic reply") as provider,
            patch("urllib.request.urlopen") as transport,
            patch.object(store, "audit") as audit,
            patch.object(store, "ensure_scanned"),
            patch.object(store, "require_clean"),
            patch.object(store.docstore, "get", return_value=b"SYNTHETIC DOCUMENT"),
        ):
            calls = (
                lambda: ai_tasks.run_document(store, user, "ZF-1", doc, b"SYNTHETIC DOCUMENT"),
                lambda: store.ai.look_at(doc["name"], b"SYNTHETIC DOCUMENT", doc["mime"]),
                lambda: store.read_document(user, "ZF-1", doc["id"]),
            )
            for index, call in enumerate(calls):
                with self.subTest(route=index):
                    provider.reset_mock()
                    transport.reset_mock()
                    audit.reset_mock()
                    with self.assertRaises(ValueError) as error:
                        call()
                    self.assert_clean(str(error.exception))
                    provider.assert_not_called()
                    transport.assert_not_called()
                    audit.assert_not_called()

    def test_chat_malformed_selected_scalar_refuses(self) -> None:
        store = self.store()
        store.cases["ZF-1"]["home"]["epc"] = PACKET
        with self.assertRaises(ValueError) as error:
            ChatIsolation(store).case_context(store.staff["sam@example.test"], "ZF-1")
        self.assert_clean(str(error.exception))

    def test_map_points_and_forced_clusters_and_logs(self) -> None:
        store = self.store()
        for c in store.cases.values():
            c["home"]["diagnostics"] = PACKET
            c["monitoring"] = PACKET
        captured: list[logging.LogRecord] = []

        class Capture(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                captured.append(record)

        handler = Capture()
        logger = logging.getLogger()
        logger.addHandler(handler)
        self.addCleanup(logger.removeHandler, handler)
        self.assert_clean(store.map_points({}))
        self.assert_clean(store.map_view({}))
        clusters = insights.map_view(store.cases.values(), {}, cap=1)
        self.assertEqual(clusters["mode"], "clusters")
        self.assertEqual(sum(c["count"] for c in clusters["items"]), 5)
        self.assert_clean(clusters)
        self.assert_clean([r.getMessage() for r in captured])

    def test_map_malformed_display_fields_refuse_without_value_echo(self) -> None:
        store = self.store()
        store.cases["ZF-1"]["home"]["address"] = PACKET
        for call in (store.map_points, store.map_view):
            with self.subTest(call=call.__name__):
                with self.assertRaises(ValueError) as error:
                    call({})
                self.assert_clean(str(error.exception))

    def test_missing_real_unknown_malformed_manifest_refuses_before_sql(self) -> None:
        out = self.snapshot()
        manifest = out / "manifest.json"
        original = json.loads(manifest.read_text())
        for classification in ("REAL", "UNKNOWN", None, {"hidden": PACKET}):
            manifest.write_text(json.dumps({**original, "source_type": classification}))
            self.refuse(out)
        manifest.unlink()
        self.refuse(out)

    def test_tampered_and_rehashed_raw_or_register_refuses(self) -> None:
        out = self.snapshot()
        path = out / "readings-0000.csv"
        content = path.read_text()
        rows = list(csv.DictReader(content.splitlines()))
        rows[0]["temperature_c"] = "21.123456"
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=sb.READING_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        self.refuse(out)
        manifest = out / "manifest.json"
        meta = json.loads(manifest.read_text())
        meta["file_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(meta))
        self.refuse(out)
        path.write_text(content)
        register = out / "sensors.csv"
        register.write_text(register.read_text().replace("SENS-SYN-", DEVICE))
        self.refuse(out)

    def test_wrong_revision_or_bad_parameters_refuse_before_generation(self) -> None:
        out = self.snapshot()
        manifest = out / "manifest.json"
        original = json.loads(manifest.read_text())
        for key, value in (
            ("generator_revision", "unverified"),
            ("seed", True),
            ("days", 1000000),
            ("cadence_minutes", 0),
            ("homes_covered", "1"),
        ):
            with self.subTest(key=key):
                manifest.write_text(json.dumps({**original, key: value}))
                with patch.object(sb, "write") as render:
                    self.refuse(out)
                    render.assert_not_called()

    def test_valid_synthetic_receipt_is_counts_only_and_idempotent(self) -> None:
        out = self.snapshot()
        with patch.object(sb, "write") as render:
            self.refuse(out, max_rows=3)
            render.assert_not_called()
        with sqlite3.connect(":memory:") as conn:
            first = sb.load_into(conn, out, max_rows=4)
            second = sb.load_into(conn, out)
        self.assertEqual(first, dict(inserted=4, rejected={}))
        self.assertEqual(second, dict(inserted=0, rejected={}))
        self.assert_clean(first)

    def test_post_verification_source_race_never_changes_inserted_values(self) -> None:
        out = self.snapshot()
        conn = Mock()
        conn.execute.return_value.rowcount = 1

        def schema(connection: object) -> None:
            for name in ("sensors.csv", "readings-0000.csv"):
                (out / name).write_text(f"sensor_id,reading_id\n{DEVICE},{RAW}\n")

        sb.load_into(conn, out, create_schema=schema)
        self.assertTrue(conn.execute.called)
        self.assert_clean(conn.execute.call_args_list)

    def test_stock_requires_explicit_matching_selection(self) -> None:
        selection = ss.select(
            [dict(synthetic_home_id="SYN-112", is_synthetic="true", monitoring_consent="granted")],
            1,
        )
        out = self.root / "stock"
        sb.write(out, stock=selection, days=1, cadence=360)
        self.refuse(out)
        other = ss.select(
            [dict(synthetic_home_id="OTHER", is_synthetic="true", monitoring_consent="granted")],
            1,
        )
        self.refuse(out, stock=other)
        with sqlite3.connect(":memory:") as conn:
            self.assertEqual(sb.load_into(conn, out, stock=selection)["inserted"], 4)

    @unittest.skipUnless(os.environ.get("ZF_SENSOR112_MSSQL") == "1", "opt-in own local SQL")
    def test_actual_owned_mssql_admission_and_idempotency(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        server = os.environ.get("ZF_SQL_SERVER", "")
        self.assertIn(server, ("127.0.0.1", "localhost"))
        database = "zf_sensor112_" + uuid.uuid4().hex
        with patch.dict(os.environ, ZF_SQL_DATABASE="master"):
            admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{database}]")

        def cleanup() -> None:
            admin.execute(f"ALTER DATABASE [{database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
            admin.execute(f"DROP DATABASE [{database}]")

        self.addCleanup(cleanup)
        with patch.dict(os.environ, ZF_SQL_DATABASE=database):
            conn = _Conn(connection_string())
        self.addCleanup(conn.close)

        class LoaderConnection:
            def execute(self, sql: str, params: object = ()) -> Any:
                return conn.execute(sql, params)

            def commit(self) -> None:
                pass  # _Conn opens its actual driver connection with autocommit=True.

        loader = LoaderConnection()
        out = self.snapshot()
        meta = json.loads((out / "manifest.json").read_text())
        (out / "manifest.json").write_text(json.dumps({**meta, "source_type": "REAL"}))
        schema = Mock()
        with self.assertRaises(ValueError):
            sb.load_into(loader, out, create_schema=schema)
        schema.assert_not_called()
        self.assertEqual(
            conn.execute(
                "SELECT COUNT(*) FROM sys.tables "
                "WHERE name IN ('sensor_reading', 'sensor_register')"
            ).fetchone()[0],
            0,
        )
        (out / "manifest.json").write_text(json.dumps(meta))

        def sql_schema(connection: Any) -> None:
            for statement in sb.SQL_DDL.split(";"):
                if statement.strip():
                    connection.execute(statement)

        self.assertEqual(sb.load_into(loader, out, create_schema=sql_schema)["inserted"], 4)
        self.assertEqual(sb.load_into(loader, out, create_schema=None)["inserted"], 0)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0], 4)
