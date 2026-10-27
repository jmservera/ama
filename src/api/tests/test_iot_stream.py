"""Local SDK representation and actual constructed SQLite integration, never Azure."""

import asyncio
import json
import tempfile
import threading
import time
import unittest
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock, patch

from azure.eventhub import EventData
from azure.eventhub.aio import PartitionContext
from azure.iot.device import X509
from sensor_consumer_fixture import CONTROL, POLICY, observations, store_at
from zava_forward.core.sensor_consumer import ConsumerError, Receipt, SensorConsumer
from zava_forward.core.synthetic import sensor_stock
from zava_forward.core.synthetic.sensor_stream import (
    Pacer,
    Replay,
    RunBudget,
    StreamError,
    replay,
    wire,
)

from zava_forward.api.iot_stream import (
    AUTH,
    DEVICE,
    Activation,
    Binding,
    HubPublisher,
    HubReceiver,
    decode,
)
from zava_forward.api.sensor_ingestion import SensorIngestion

ACTIVE = Activation(
    "iot-fixture.azure-devices.net",
    "eh-iot-fixture.servicebus.windows.net",
    "constructed approval, not live authority",
    routing_ready=True,
)
BINDING = Binding("SYN-SENS-SYN-1", "SENS-SYN-1", "ZF-1")


def event(row: Mapping[str, object], device: str = BINDING.device_id) -> EventData:
    result = EventData(json.dumps(dict(row)).encode())
    result.properties = {
        DEVICE: device.encode(),
        AUTH: b'{"scope":"device","type":"x509"}',
    }
    return result


class FixtureClock(datetime):
    @classmethod
    def now(cls, tz: object = None) -> "FixtureClock":
        return cls(2024, 10, 1, 2, tzinfo=UTC)


class ReceiverTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.consumer.configure(POLICY, [CONTROL])
        self.receiver = HubReceiver(SensorIngestion(self.store), ACTIVE, (BINDING,))
        self.credentials = Mock(close=AsyncMock())
        self.client = Mock(close=AsyncMock())
        self.contexts: dict[str, Mock] = {}
        self.events: list[tuple[str, EventData]] = []
        self.checkpoints: list[str] = []
        self.checkpoint_failure = False

    def count(self, table: str) -> int:
        return int(self.store.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

    async def test_partial_setup_failure_sanitizes_and_cleans_owned_resources(self) -> None:
        for phase in ("credential", "client", "receive"):
            for close_fails in (False, True):
                with self.subTest(phase=phase, close_fails=close_fails):
                    credential = Mock(close=AsyncMock())
                    client = Mock(close=AsyncMock())
                    if close_fails:
                        credential.close.side_effect = RuntimeError("constructed private detail")
                    client.receive = Mock(side_effect=RuntimeError("constructed private detail"))
                    code = (
                        "IOT_CLEANUP_FAILED"
                        if close_fails and phase != "credential"
                        else "IOT_RECEIVE_FAILED"
                    )
                    with (
                        patch(
                            "zava_forward.api.iot_stream.ManagedIdentityCredential",
                            side_effect=(
                                RuntimeError("constructed private detail")
                                if phase == "credential"
                                else None
                            ),
                            return_value=credential,
                        ),
                        patch(
                            "zava_forward.api.iot_stream.EventHubConsumerClient",
                            side_effect=(
                                RuntimeError("constructed private detail")
                                if phase == "client"
                                else None
                            ),
                            return_value=client,
                        ) as factory,
                    ):
                        with self.assertRaisesRegex(StreamError, f"^{code}$"):
                            await self.receiver.run(max_seconds=2, max_events=1)
                    if phase == "credential":
                        factory.assert_not_called()
                        credential.close.assert_not_called()
                    else:
                        credential.close.assert_awaited_once()
                    if phase == "receive":
                        client.close.assert_awaited_once()
                    else:
                        client.close.assert_not_called()
                    self.assertEqual(self.count("sensor_delivery"), 0)

    async def test_cancelled_setup_cleans_credential_and_preserves_cancellation(self) -> None:
        with (
            patch(
                "zava_forward.api.iot_stream.ManagedIdentityCredential",
                return_value=self.credentials,
            ),
            patch(
                "zava_forward.api.iot_stream.EventHubConsumerClient",
                side_effect=asyncio.CancelledError,
            ),
        ):
            with self.assertRaises(asyncio.CancelledError):
                await self.receiver.run(max_seconds=2, max_events=1)
        self.credentials.close.assert_awaited_once()
        self.client.close.assert_not_called()

    async def receive(
        self,
        on_event: Callable[[PartitionContext, EventData | None], Awaitable[None]],
        **kwargs: object,
    ) -> None:
        self.assertEqual(kwargs["starting_position"], "-1")
        for partition, item in self.events:
            context = self.contexts.get(partition)
            if context is None:
                context = Mock(spec=PartitionContext, partition_id=partition)

                async def checkpoint(e: EventData, p: str = partition) -> None:
                    self.assertGreater(self.count("sensor_delivery"), 0)
                    if self.checkpoint_failure:
                        raise RuntimeError("constructed SECRET must not escape")
                    self.checkpoints.append(p)

                context.update_checkpoint = AsyncMock(side_effect=checkpoint)
                self.contexts[partition] = context
            # The SDK may continue invoking callbacks after catching failures.
            await on_event(context, item)
        await asyncio.Event().wait()

    async def run_receiver(
        self, count: int, stop: asyncio.Event | None = None
    ) -> tuple[Receipt, ...]:
        self.client.receive = self.receive
        with (
            patch(
                "zava_forward.api.iot_stream.ManagedIdentityCredential",
                return_value=self.credentials,
            ) as credential,
            patch(
                "zava_forward.api.iot_stream.EventHubConsumerClient", return_value=self.client
            ) as factory,
            patch("zava_forward.api.iot_stream.datetime", FixtureClock),
        ):
            try:
                return await self.receiver.run(max_seconds=2, max_events=count, stop=stop)
            finally:
                credential.assert_called_once_with(client_id=None)
                self.assertEqual(factory.call_args.kwargs["retry_total"], 0)
                self.assertIs(factory.call_args.kwargs["logging_enable"], False)
                self.assertEqual(factory.call_args.kwargs["eventhub_name"], "sensor-readings")
                self.client.close.assert_awaited_once()
                self.credentials.close.assert_awaited_once()

    async def test_two_partitions_and_new_receiver_replay_without_checkpoint_store(self) -> None:
        first, second = observations()
        bad = {**second, "temperature_unit": "degF"}
        self.events = [("0", event(first)), ("1", event(bad))]
        receipts = await self.run_receiver(2)
        self.assertEqual(len(receipts), 2)
        self.assertEqual(self.count("sensor_reading"), 1)
        self.assertEqual(self.count("sensor_data_quality_exception"), 1)
        self.assertEqual(self.checkpoints, [])
        self.receiver = HubReceiver(SensorIngestion(self.store), ACTIVE, (BINDING,))
        self.client = Mock(close=AsyncMock())
        self.credentials = Mock(close=AsyncMock())
        await self.run_receiver(2)
        self.assertEqual(self.count("sensor_reading"), 1)
        self.assertEqual(self.count("sensor_data_quality_exception"), 1)

    async def test_sql_failure_stops_admission_without_checkpoint_then_recovers(self) -> None:
        first, second = observations()
        self.events = [("0", event(first)), ("0", event(second))]
        with patch.object(
            self.receiver.ingestion, "consume", side_effect=ConsumerError("SENSOR_SQL_UNAVAILABLE")
        ):
            with self.assertRaisesRegex(StreamError, "^SENSOR_SQL_UNAVAILABLE$"):
                await self.run_receiver(2)
        self.assertEqual(self.checkpoints, [])
        self.assertEqual(self.count("sensor_reading"), 0)
        self.client = Mock(close=AsyncMock())
        self.credentials = Mock(close=AsyncMock())
        await self.run_receiver(2)
        self.assertEqual(self.count("sensor_reading"), 2)

    async def test_uncertain_sql_commit_restart_reconciles(self) -> None:
        first, second = observations()
        self.events = [("0", event(first)), ("0", event(second))]
        consume = self.receiver.ingestion.consume

        def lost_ack(*args: object, **kwargs: object) -> tuple[Receipt, ...]:
            consume([first], received_at="2024-10-01T02:00:00Z")
            raise ConsumerError("SENSOR_COMMIT_UNCERTAIN")

        with patch.object(self.receiver.ingestion, "consume", side_effect=lost_ack):
            with self.assertRaisesRegex(StreamError, "^SENSOR_COMMIT_UNCERTAIN$"):
                await self.run_receiver(2)
        self.assertEqual(self.count("sensor_reading"), 1)
        self.assertEqual(self.checkpoints, [])
        self.client = Mock(close=AsyncMock())
        self.credentials = Mock(close=AsyncMock())
        await self.run_receiver(2)
        self.assertEqual(self.count("sensor_reading"), 2)

    async def test_identity_refusal_no_write_and_no_later_checkpoint(self) -> None:
        first, second = observations()
        self.events = [
            ("0", event({**first, "sensor_id": "UNMAPPED-SENS-SYN-1"})),
            ("1", event(second)),
        ]
        with self.assertRaisesRegex(StreamError, "IOT_DEVICE_BINDING_MISMATCH"):
            await self.run_receiver(2)
        self.assertEqual(self.count("sensor_delivery"), 0)
        self.assertEqual(self.checkpoints, [])

    async def test_trusted_unmapped_binding_produces_owned_dq(self) -> None:
        row = {**observations()[0], "sensor_id": "UNMAPPED-SENS-SYN-1"}
        binding = Binding("SYN-UNMAPPED-SENS-SYN-1", "UNMAPPED-SENS-SYN-1", "ZF-1")
        self.receiver = HubReceiver(SensorIngestion(self.store), ACTIVE, (binding,))
        self.events = [("0", event(row, binding.device_id))]
        await self.run_receiver(1)
        self.assertEqual(self.count("sensor_reading"), 0)
        self.assertEqual(self.count("sensor_data_quality_exception"), 1)
        reason = self.store.db.execute(
            "SELECT reason FROM sensor_data_quality_exception"
        ).fetchone()
        self.assertEqual(reason[0], "UNMAPPED")

    async def test_fault_inputs_keep_owned_dq_and_property_state(self) -> None:
        before = tuple(self.store.db.execute("SELECT id, body FROM cases ORDER BY id").fetchall())
        for fault, expected in (
            ("wrong_unit", "UNIT"),
            ("clock_skewed", "MAPPING_INTERVAL"),
            ("uncalibrated", "CALIBRATION"),
        ):
            self.events = [("0", event(observations(fault)[0]))]
            self.client = Mock(close=AsyncMock())
            self.credentials = Mock(close=AsyncMock())
            receipts = await self.run_receiver(1)
            self.assertEqual(receipts[0].reason, expected)
        self.assertEqual(self.count("sensor_data_quality_exception"), 3)
        self.assertEqual(
            tuple(self.store.db.execute("SELECT id, body FROM cases ORDER BY id").fetchall()),
            before,
        )

    async def test_idle_deadline_and_external_stop_cleanup(self) -> None:
        for stopped in (False, True):
            self.client = Mock(close=AsyncMock())
            self.credentials = Mock(close=AsyncMock())
            stop = asyncio.Event()
            if stopped:
                stop.set()
            with self.assertRaisesRegex(StreamError, "RUN_STOPPED|RUN_DEADLINE"):
                await self.run_receiver(1, stop)

    async def test_cancel_during_sql_does_not_checkpoint_or_claim_rollback(self) -> None:
        started, release = threading.Event(), threading.Event()
        consume = self.receiver.ingestion.consume

        def delayed(*args: object, **kwargs: object) -> object:
            started.set()
            release.wait(2)
            return consume([observations()[0]], received_at="2024-10-01T02:00:00Z")

        self.events = [("0", event(observations()[0]))]
        with patch.object(self.receiver.ingestion, "consume", side_effect=delayed):
            task = asyncio.create_task(self.run_receiver(1))
            await asyncio.to_thread(started.wait, 1)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
            self.assertEqual(self.checkpoints, [])
            release.set()
            for _ in range(100):
                if self.count("sensor_reading"):
                    break
                await asyncio.sleep(0.01)
            self.assertEqual(self.count("sensor_reading"), 1)

    async def test_backfill_and_stream_same_home_exact_numeric_seam_and_retry(self) -> None:
        selected = sensor_stock.select(
            [
                {
                    "synthetic_home_id": "ZF-1",
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                    "building_form_osm": "terrace",
                }
            ],
            1,
        )
        frames = replay(selected, Replay(days=1, cadence_minutes=60, end_slot=2))
        sensor = frames[0].row["sensor_id"]
        binding = Binding(frames[0].device_id, sensor, "ZF-1")
        self.consumer.configure(POLICY, [replace(CONTROL, sensor_id=sensor)])
        self.receiver = HubReceiver(SensorIngestion(self.store), ACTIVE, (binding,))
        # Backfill enters through the unchanged canonical SQL admission boundary.
        self.receiver.ingestion.consume([frames[0].row], received_at="2024-10-01T02:00:00Z")
        self.events = [("0", event(frame.row, binding.device_id)) for frame in frames]
        await self.run_receiver(2)
        stored = self.store.db.execute(
            "SELECT home_id, observed_at, temperature_c, humidity_pct FROM sensor_reading "
            "ORDER BY observed_at"
        ).fetchall()
        self.assertEqual(len(stored), 2)
        for actual, expected in zip(stored, frames, strict=True):
            self.assertEqual(actual[0:2], ("ZF-1", expected.row["observed_at"]))
            self.assertEqual(float(actual[2]), float(expected.row["temperature_c"]))
            self.assertEqual(float(actual[3]), float(expected.row["humidity_pct"]))


class MetadataTests(unittest.TestCase):
    def test_actual_eventdata_properties_and_refusals(self) -> None:
        row = observations()[0]
        valid = event(row)
        self.assertEqual(decode(valid, {BINDING.device_id: BINDING}), row)
        mutations: tuple[dict[str | bytes, object], ...] = (
            {},
            {DEVICE: BINDING.device_id},
            {DEVICE: b"OTHER", AUTH: b"{}"},
            {DEVICE: BINDING.device_id.encode(), AUTH: b'{"scope":"device","type":"sas"}'},
            {DEVICE: BINDING.device_id.encode(), AUTH: b"{}", DEVICE.decode(): b"SPOOF"},
        )
        for mutation in mutations:
            invalid = event(row)
            invalid.properties = mutation
            with self.subTest(mutation=mutation), self.assertRaises(StreamError):
                decode(invalid, {BINDING.device_id: BINDING})
        duplicate = event(row)
        annotations = duplicate.raw_amqp_message.annotations
        assert annotations is not None
        annotations[DEVICE] = b"SPOOF"
        with self.assertRaisesRegex(StreamError, "IOT_AMBIGUOUS_ORIGIN"):
            decode(duplicate, {BINDING.device_id: BINDING})
        for body in (b'{"sensor_id":"A","sensor_id":"B"}', b"x" * 4097, b"\xff"):
            invalid = EventData(body)
            invalid.properties = valid.properties
            with self.assertRaises(StreamError):
                decode(invalid, {BINDING.device_id: BINDING})

    def test_activation_and_binding_are_fail_closed(self) -> None:
        for config in (
            replace(ACTIVE, routing_ready=False),
            replace(ACTIVE, resource_group="other"),
            replace(ACTIVE, approval_reference=""),
            replace(ACTIVE, consumer_group="$Default"),
            replace(ACTIVE, eventhub_namespace="other.servicebus.windows.net"),
        ):
            with self.assertRaisesRegex(StreamError, "IOT_ACTIVATION_REQUIRED"):
                config.validate()
        with self.assertRaisesRegex(StreamError, "INVALID_SYNTHETIC_BINDING"):
            Binding("installed-real-device", "SENS-SYN-1", "ZF-1").validate()


class PublisherTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        selected = sensor_stock.select(
            [
                {
                    "synthetic_home_id": "ZF-1",
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                }
            ],
            1,
        )
        self.frames = replay(selected, Replay(fault="burst", end_slot=2))
        binding = Binding(self.frames[0].device_id, self.frames[0].row["sensor_id"], "ZF-1")
        # Only inert paths are constructed; no certificate file is opened.
        self.publisher = HubPublisher(
            ACTIVE, (binding,), {binding.device_id: X509("not-read.pem", "not-read-key.pem")}
        )
        self.budget = RunBudget(
            "Fixture Owner",
            "USD60 source model",
            "constructed alert",
            max_seconds=2,
            max_per_second=100,
        )
        self.client = Mock(connect=AsyncMock(), send_message=AsyncMock(), shutdown=AsyncMock())
        self.truth: list[dict[str, object]] = []

    async def test_actual_send_rate_after_connect_and_preparation_across_devices(self) -> None:
        selected = sensor_stock.select(
            [
                {
                    "synthetic_home_id": home,
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                }
                for home in ("ZF-1", "ZF-2")
            ],
            2,
        )
        for delay in ("connect", "truth"):
            for homes in (1, 2):
                with self.subTest(delay=delay, homes=homes):
                    frames = replay(
                        sensor_stock.select(selected.rows, homes),
                        Replay(fault="burst", end_slot=2),
                    )
                    bindings = tuple(
                        Binding(frame.device_id, frame.row["sensor_id"], frame.row["home_id"])
                        for frame in frames[:homes]
                    )
                    publisher = HubPublisher(
                        ACTIVE,
                        bindings,
                        {b.device_id: X509("not-read.pem", "not-read-key.pem") for b in bindings},
                    )
                    sent: list[float] = []

                    async def connect(delay: str = delay) -> None:
                        if delay == "connect":
                            await asyncio.sleep(0.08)

                    async def send(message: object, sent: list[float] = sent) -> None:
                        sent.append(time.monotonic())

                    def truth(
                        row: dict[str, object], delay: str = delay, sent: list[float] = sent
                    ) -> None:
                        if delay == "truth" and not sent:
                            time.sleep(0.08)

                    clients = [
                        Mock(
                            connect=AsyncMock(side_effect=connect),
                            send_message=AsyncMock(side_effect=send),
                            shutdown=AsyncMock(),
                        )
                        for _ in bindings
                    ]
                    budget = replace(self.budget, max_seconds=4, max_per_second=20)
                    with patch(
                        "zava_forward.api.iot_stream.IoTHubDeviceClient."
                        "create_from_x509_certificate",
                        side_effect=clients,
                    ):
                        self.assertEqual(
                            await publisher.run(frames, budget, truth=truth), len(frames)
                        )
                    self.assertEqual(len(sent), len(frames))
                    for first, second in zip(sent, sent[1:], strict=False):
                        self.assertGreaterEqual(second - first, 1 / budget.max_per_second)
                    for client in clients:
                        client.shutdown.assert_awaited_once()

    async def test_post_preparation_controls_prevent_actual_send(self) -> None:
        for state in ("stop", "pause-stop", "deadline", "cancel"):
            with self.subTest(state=state):
                control = Pacer(self.budget)
                prepared = asyncio.Event()
                self.client = Mock(
                    connect=AsyncMock(), send_message=AsyncMock(), shutdown=AsyncMock()
                )

                def truth(
                    row: dict[str, object],
                    state: str = state,
                    control: Pacer = control,
                    prepared: asyncio.Event = prepared,
                ) -> None:
                    if row["status"] == "attempt":
                        prepared.set()
                        if state == "stop":
                            control.stopped = True
                        elif state == "deadline":
                            control.deadline = time.monotonic()
                        else:
                            control.paused = True

                with patch(
                    "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
                    return_value=self.client,
                ):
                    task = asyncio.create_task(
                        self.publisher.run(self.frames, self.budget, pacer=control, truth=truth)
                    )
                    await prepared.wait()
                    if state == "cancel":
                        await asyncio.sleep(0)
                        task.cancel()
                        with self.assertRaises(asyncio.CancelledError):
                            await task
                    else:
                        if state == "pause-stop":
                            await asyncio.sleep(0.02)
                            self.client.send_message.assert_not_called()
                            control.stopped = True
                        with self.assertRaisesRegex(StreamError, "RUN_STOPPED|RUN_DEADLINE"):
                            await task
                self.client.send_message.assert_not_called()
                self.client.shutdown.assert_awaited_once()

    async def test_per_device_x509_message_schema_truth_and_cleanup(self) -> None:
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
            return_value=self.client,
        ) as factory:
            count = await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
        self.assertEqual(count, 2)
        self.assertEqual(factory.call_args.kwargs["auto_connect"], False)
        self.assertEqual(factory.call_args.kwargs["connection_retry"], False)
        self.client.shutdown.assert_awaited_once()
        for call, frame in zip(self.client.send_message.call_args_list, self.frames, strict=True):
            message = call.args[0]
            self.assertEqual(message.data, wire(frame.row).decode("ascii"))
            self.assertEqual(message.content_type, "application/json")
            self.assertEqual(message.content_encoding, "utf-8")
        self.assertEqual([row["status"] for row in self.truth], ["attempt", "sent"] * 2)
        self.assertTrue(all("home_id" not in row for row in self.truth))
        self.assertEqual(
            {row["selected_stock_sha256"] for row in self.truth},
            {frame.selected_stock_sha256 for frame in self.frames},
        )

    async def test_connect_send_timeout_stop_failure_and_cancellation(self) -> None:
        async def blocked(*args: object) -> None:
            await asyncio.Event().wait()

        for phase in ("connect", "send_message"):
            self.client = Mock(connect=AsyncMock(), send_message=AsyncMock(), shutdown=AsyncMock())
            getattr(self.client, phase).side_effect = blocked
            with patch(
                "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
                return_value=self.client,
            ):
                with self.assertRaisesRegex(StreamError, "IOT_OPERATION_TIMEOUT"):
                    await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
                self.client.shutdown.assert_awaited_once()
        self.client = Mock(connect=AsyncMock(), send_message=AsyncMock(), shutdown=AsyncMock())
        self.client.send_message.side_effect = RuntimeError("SECRET not logged")
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
            return_value=self.client,
        ):
            with self.assertRaisesRegex(StreamError, "^IOT_PUBLISH_FAILED$"):
                await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
        control = Pacer(self.budget)
        control.stopped = True
        with self.assertRaisesRegex(StreamError, "RUN_STOPPED"):
            await self.publisher.run(
                self.frames, self.budget, pacer=control, truth=self.truth.append
            )

    async def test_unmapped_claim_refused_before_any_client(self) -> None:
        bad = replace(self.frames[0], row={**self.frames[0].row, "sensor_id": "UNMAPPED"})
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate"
        ) as factory:
            with self.assertRaisesRegex(StreamError, "IOT_DEVICE_BINDING_MISMATCH"):
                await self.publisher.run((bad,), self.budget, truth=self.truth.append)
            factory.assert_not_called()

    async def test_distinct_homes_use_distinct_device_clients(self) -> None:
        selected = sensor_stock.select(
            [
                {
                    "synthetic_home_id": home,
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                }
                for home in ("ZF-1", "ZF-2")
            ],
            2,
        )
        frames = replay(selected, Replay(fault="burst", end_slot=1))
        bindings = tuple(
            Binding(frame.device_id, frame.row["sensor_id"], frame.row["home_id"])
            for frame in frames
        )
        publisher = HubPublisher(
            ACTIVE,
            bindings,
            {b.device_id: X509("not-read.pem", "not-read-key.pem") for b in bindings},
        )
        clients = [
            Mock(connect=AsyncMock(), send_message=AsyncMock(), shutdown=AsyncMock())
            for _ in bindings
        ]
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
            side_effect=clients,
        ) as factory:
            await publisher.run(frames, self.budget, truth=self.truth.append)
        self.assertEqual(
            {call.args[2] for call in factory.call_args_list},
            {binding.device_id for binding in bindings},
        )
        for client in clients:
            client.send_message.assert_awaited_once()
            client.shutdown.assert_awaited_once()

    async def test_external_stop_and_cancel_blocked_send_clean_up(self) -> None:
        entered = asyncio.Event()

        async def blocked(message: object) -> None:
            entered.set()
            await asyncio.Event().wait()

        for cancel in (False, True):
            entered.clear()
            self.client = Mock(
                connect=AsyncMock(),
                send_message=AsyncMock(side_effect=blocked),
                shutdown=AsyncMock(),
            )
            control = Pacer(self.budget)
            with patch(
                "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
                return_value=self.client,
            ):
                task = asyncio.create_task(
                    self.publisher.run(
                        self.frames, self.budget, pacer=control, truth=self.truth.append
                    )
                )
                await entered.wait()
                if cancel:
                    task.cancel()
                    with self.assertRaises(asyncio.CancelledError):
                        await task
                else:
                    control.stopped = True
                    with self.assertRaisesRegex(StreamError, "RUN_STOPPED"):
                        await task
                self.client.shutdown.assert_awaited_once()
                self.assertEqual(self.client.send_message.await_count, 1)

    async def test_cleanup_failure_is_explicit_and_bounded(self) -> None:
        async def blocked() -> None:
            await asyncio.Event().wait()

        self.client.shutdown.side_effect = blocked
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
            return_value=self.client,
        ):
            with self.assertRaisesRegex(StreamError, "^IOT_CLEANUP_FAILED$"):
                await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
