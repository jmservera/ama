"""Finite offline adapter integration, using constructed controls only."""

import unittest

import test_sensor_consumer as coretests
from sensor_consumer_fixture import RECEIVED, observations
from zava_forward.core.sensor_consumer import Observation, Receipt, SensorConsumer

from zava_forward.api.sensor_ingestion import BatchStopped, SensorIngestion


class AdapterExists(unittest.TestCase):
    def test_existing_api_owns_callable(self) -> None:
        from zava_forward.api.sensor_ingestion import SensorIngestion

        self.assertTrue(callable(SensorIngestion))


class ApiSensorTests(coretests.SensorConsumerTests):
    def consume(
        self,
        rows: list[Observation],
        received_at: str = RECEIVED,
        consumer: SensorConsumer | None = None,
    ) -> tuple[Receipt, ...]:
        adapter = SensorIngestion(self.store)
        if consumer is not None:
            adapter.consumer = consumer
        return adapter.consume(rows, received_at=received_at)

    def test_valid_malformed_order_missing_id_and_durable_retry(self) -> None:
        first, second = observations()
        malformed = {k: v for k, v in first.items() if k != "reading_id"}
        result = self.consume([malformed, first, second, malformed])
        self.assertEqual([r.reason for r in result], ["SCHEMA", "ACCEPTED", "ACCEPTED", "SCHEMA"])
        self.assertTrue(result[-1].replay)
        self.assertEqual(self.counts(), (2, 3, 1))

    def test_middle_database_failure_reports_prefix_stops_then_reconciles(self) -> None:
        first, second = observations()
        invalid = {**second, "temperature_unit": "degF"}
        self._trigger("sensor_data_quality_exception")
        with self.assertRaises(BatchStopped) as caught:
            self.consume([first, invalid, second])
        self.assertEqual(len(caught.exception.completed), 1)
        self.assertEqual(caught.exception.code, "SENSOR_SQL_UNAVAILABLE")
        self.assertEqual(self.counts(), (1, 1, 0))
        self._trigger("sensor_data_quality_exception", remove=True)
        result = self.consume([first, invalid, second])
        self.assertTrue(result[0].replay)
        self.assertEqual([r.reason for r in result], ["ACCEPTED", "UNIT", "ACCEPTED"])
        self.assertEqual(self.counts(), (2, 3, 1))

    def test_middle_uncertain_ack_reports_prefix_and_retry(self) -> None:
        class SecondAckLost(SensorConsumer):
            calls = 0

            def acknowledge(self, receipt: Receipt) -> None:
                self.calls += 1
                if self.calls == 2:
                    raise RuntimeError("constructed lost acknowledgement")

        first, second = observations()
        third = {**second, "reading_id": "THIRD", "observed_at": "2024-10-01T02:00:00Z"}
        with self.assertRaises(BatchStopped) as caught:
            self.consume([first, second, third], consumer=SecondAckLost(self.store))
        self.assertEqual(len(caught.exception.completed), 1)
        self.assertEqual(caught.exception.code, "SENSOR_COMMIT_UNCERTAIN")
        self.assertEqual(self.counts(), (2, 2, 0))
        retried = self.consume([first, second, third])
        self.assertEqual([r.replay for r in retried], [True, True, False])
        self.assertEqual(self.counts(), (3, 3, 0))

    def test_full_preflight_before_writes_and_unavailable_not_empty(self) -> None:
        first = observations()[0]
        with self.assertRaisesRegex(RuntimeError, "INVALID_BATCH"):
            SensorIngestion(self.store).consume(
                [first, {"nested": {"not": "observation"}}], received_at=RECEIVED
            )
        self.assertEqual(self.counts(), (0, 0, 0))
        self.store.db.execute("DROP TABLE sensor_delivery")
        with self.assertRaises(BatchStopped) as caught:
            self.consume([first])
        self.assertEqual(caught.exception.code, "SENSOR_SQL_UNAVAILABLE")
        self.assertEqual(caught.exception.completed, ())
        self.assertNotIn(str(first["sensor_id"]), str(caught.exception))

    def test_invalid_receipt_time_no_write(self) -> None:
        for received in ("2024-10-01T02:00:00+01:00", "secret", True):
            with self.assertRaisesRegex(RuntimeError, "INVALID_RECEIPT_TIME"):
                SensorIngestion(self.store).consume(observations(), received_at=received)
        self.assertEqual(self.counts(), (0, 0, 0))
