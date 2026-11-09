"""Actual SQL Server run of the retained sensor analysis tests (Refs #111)."""

import os
import tempfile
import unittest

import test_sensor_analysis_store as base
from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.core import sensor_analysis_store as store
from zava_forward.core.sensor_consumer import SensorConsumer, preflight

SENSOR_TABLES = (
    "sensor_data_quality_exception",
    "sensor_delivery",
    "sensor_consumer_control",
    "sensor_consumer_policy",
    "sensor_reading",
    "sensor_register",
)


@unittest.skipUnless(os.environ.get("ZF_SENSOR_MSSQL") == "1", "requires ZF_SENSOR_MSSQL=1")
class MssqlRetainedAnalysisTests(base.RetainedAnalysisTests):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.assertTrue(self.consumer.mssql, "actual MSSQL backend required")
        with self.consumer._write() as db:
            for table in SENSOR_TABLES:
                db.execute(f"IF OBJECT_ID(N'{table}', N'U') IS NOT NULL DROP TABLE {table}")
            db.execute("DELETE FROM cases WHERE id='ZF-2'")
        # configure recreates any table a test deliberately drops, restoring the shared database.
        self.addCleanup(lambda: self.consumer.configure(POLICY, [CONTROL]))
        self.consumer.configure(POLICY, [CONTROL])
        for row in preflight(observations()):
            self.assertEqual(self.consumer.process(row, RECEIVED).status, "accepted")

    def test_reopened_store_reproduces_signal_without_writes(self) -> None:
        first = store.analyse_retained(self.consumer, base.HOME, base.WINDOW, base.AS_OF)
        self.assertGreater(first.valid, 0)
        before = self.snapshot()
        reopened = store_at(self.tmp.name)
        self.addCleanup(reopened.db.close)
        again = store.analyse_retained(SensorConsumer(reopened), base.HOME, base.WINDOW, base.AS_OF)
        self.assertEqual(again, first)
        self.assertEqual(again.priority_effect, "NONE")
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
