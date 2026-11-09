"""Receiver startup and retained write under exactly the documented minimum SQL grants (#110).

Runs only against a task-owned SQL Server (`ZF_SENSOR_MSSQL=1`, set by `sensor_sql_check.py`).
Setup and admin provision the schema separately; the receiver principal is a disposable login that
holds only the grants documented in `infra/README.md`, so nothing here is a full-permission write.
"""

import os
import secrets
import tempfile
import unittest
import uuid
from datetime import UTC, datetime

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, SENSOR_STATE_TABLES, store_at
from zava_forward.core.mssqlstore import _Conn, connection_string
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.synthetic.live_readings import Reading

from zava_forward.api import live_receiver as rx
from zava_forward.api.sensor_ingestion import SensorIngestion

GRANTS = (
    "SELECT ON dbo.cases",
    "SELECT ON dbo.sensor_consumer_control",
    "SELECT ON dbo.sensor_consumer_policy",
    "SELECT, INSERT ON dbo.sensor_reading",
    "SELECT, INSERT ON dbo.sensor_delivery",
    "SELECT, INSERT ON dbo.sensor_data_quality_exception",
)
SLOT = datetime(2024, 10, 1, 1, 0, tzinfo=UTC)


@unittest.skipUnless(os.environ.get("ZF_SENSOR_MSSQL") == "1", "needs the task-owned SQL Server")
class ReceiverMinimumGrantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        admin = SensorConsumer(self.store)
        self.assertTrue(admin.mssql)
        with admin._write() as db:
            for table in (*SENSOR_STATE_TABLES, "sensor_register"):
                db.execute(f"IF OBJECT_ID(N'{table}', N'U') IS NOT NULL DROP TABLE {table}")
        admin.configure(POLICY, [CONTROL])
        self.name = "recv_" + uuid.uuid4().hex[:10]
        self.password = "Aa1!" + secrets.token_urlsafe(24)
        self.admin = _Conn(connection_string())
        self.addCleanup(self.admin.close)
        self.admin.execute(f"CREATE LOGIN {self.name} WITH PASSWORD = '{self.password}'")
        self.admin.execute(f"CREATE USER {self.name} FOR LOGIN {self.name}")
        self.addCleanup(self.drop_principal)
        for grant in GRANTS:
            self.admin.execute(f"GRANT {grant} TO {self.name}")
        self.env = {
            k: v for k, v in os.environ.items() if k.startswith("ZF_SQL_") and k != "ZF_SQL_TOKEN"
        } | {"ZF_STORE": "mssql", "ZF_SQL_AUTH": "password"}
        self.env.update(ZF_SQL_USER=self.name, ZF_SQL_PASSWORD=self.password)

    def drop_principal(self) -> None:
        sessions = self.admin.execute(
            "SELECT session_id FROM sys.dm_exec_sessions WHERE login_name = ?", (self.name,)
        ).fetchall()
        for (session,) in sessions:
            self.admin.execute(f"KILL {int(session)}")
        self.admin.execute(f"DROP USER IF EXISTS {self.name}")
        self.admin.execute(f"DROP LOGIN {self.name}")

    def state(self) -> tuple[object, ...]:
        objects = self.admin.execute(
            "SELECT name, type, modify_date FROM sys.objects WHERE is_ms_shipped = 0 ORDER BY name"
        ).fetchall()
        tables = [str(r[0]) for r in objects if str(r[1]).strip() == "U"]
        counts = {
            t: int(self.admin.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]) for t in tables
        }
        return tuple(tuple(r) for r in objects), tuple(sorted(counts.items()))

    def test_startup_and_retained_write_under_documented_grants_only(self) -> None:
        connector = rx.persistence(self.env)
        self.assertEqual(type(connector).__name__, "SensorMssqlConnector")
        ingestion = SensorIngestion(connector)
        self.assertTrue(ingestion.consumer.mssql)
        identity = _Conn(connection_string(self.env))
        try:
            self.assertEqual(identity.execute("SELECT SUSER_NAME()").fetchone()[0], self.name)
            self.assertEqual(
                identity.execute("SELECT IS_SRVROLEMEMBER('sysadmin')").fetchone()[0], 0
            )
            with self.assertRaises(identity.driver.Error):
                identity.execute("CREATE TABLE dbo.receiver_must_not_create (x INT)")
            with self.assertRaises(identity.driver.Error):
                identity.execute("DELETE FROM dbo.cases")
        finally:
            identity.close()
        before = self.state()
        reading = Reading("ZF-1", "SENS-SYN-1", "SYN-SENS-SYN-1", SLOT, 12.34, 66.5, 301.25, 184)
        receipts = ingestion.consume([reading.row()], received_at=RECEIVED)
        self.assertEqual([(r.status, r.reason) for r in receipts], [("accepted", "ACCEPTED")])
        after = self.state()
        self.assertEqual(before[0], after[0])  # no object created or altered
        old, new = dict(before[1]), dict(after[1])  # type: ignore[call-overload]
        changed = {name for name in new if old.get(name) != new[name]}
        self.assertGreater(len(old), 10)  # the whole application schema was compared
        self.assertEqual(changed, {"sensor_reading", "sensor_delivery"}, (old, new))
        row = self.admin.execute(
            "SELECT sensor_id, home_id, source_type, schema_version FROM sensor_reading"
        ).fetchall()
        self.assertEqual(
            [tuple(r) for r in row][0][1:], ("ZF-1", "SYNTHETIC", "live-sim-reading-v1")
        )
        again = ingestion.consume([reading.row()], received_at=RECEIVED)
        self.assertTrue(again[0].replay)

    def test_receiver_refuses_missing_schema_rather_than_creating_it(self) -> None:
        self.admin.execute("DROP TABLE sensor_consumer_policy")
        before = self.state()[0]
        ingestion = SensorIngestion(rx.persistence(self.env))
        reading = Reading("ZF-1", "SENS-SYN-1", "SYN-SENS-SYN-1", SLOT, 12.34, 66.5, 301.25, 184)
        with self.assertRaises(RuntimeError):
            ingestion.consume([reading.row()], received_at=RECEIVED)
        self.assertEqual(self.state()[0], before)
