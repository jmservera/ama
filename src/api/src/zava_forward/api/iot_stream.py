"""Explicit finite Azure IoT runs; no HTTP route or application startup activation."""

import asyncio
import json
import math
import re
import time
from collections.abc import Awaitable, Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient, PartitionContext
from azure.identity.aio import ManagedIdentityCredential
from azure.iot.device import X509, Message
from azure.iot.device.aio import IoTHubDeviceClient
from zava_forward.core.sensor_consumer import ConsumerError, Observation, Receipt, preflight
from zava_forward.core.synthetic.sensor_identity import home_key
from zava_forward.core.synthetic.sensor_stream import Frame, Pacer, RunBudget, StreamError, wire

from .sensor_ingestion import SensorIngestion

DEVICE = b"iothub-connection-device-id"
MODULE = b"iothub-connection-module-id"
AUTH = b"iothub-connection-auth-method"


def _validate_device_activation(hostname: str, approval: str, resource_group: str) -> None:
    if (
        resource_group != "ama"
        or not approval.strip()
        or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}\.azure-devices\.net", hostname)
    ):
        raise StreamError("IOT_ACTIVATION_REQUIRED")


@dataclass(frozen=True)
class DeviceActivation:
    hub_hostname: str
    approval_reference: str
    resource_group: str = "ama"

    def validate(self) -> None:
        _validate_device_activation(self.hub_hostname, self.approval_reference, self.resource_group)


@dataclass(frozen=True)
class Activation:
    hub_hostname: str
    eventhub_namespace: str
    approval_reference: str
    routing_ready: bool = False
    resource_group: str = "ama"
    eventhub_name: str = "sensor-readings"
    consumer_group: str = "api-consumer"
    managed_identity_client_id: str | None = None

    def validate(self) -> None:
        _validate_device_activation(self.hub_hostname, self.approval_reference, self.resource_group)
        if (
            self.routing_ready is not True
            or self.eventhub_namespace
            != "eh-"
            + self.hub_hostname.removesuffix(".azure-devices.net")
            + ".servicebus.windows.net"
            or self.eventhub_name != "sensor-readings"
            or self.consumer_group != "api-consumer"
        ):
            raise StreamError("IOT_ACTIVATION_REQUIRED")


@dataclass(frozen=True)
class Binding:
    device_id: str
    sensor_id: str
    home_id: str

    def validate(self) -> None:
        if (
            not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{0,19}", self.sensor_id)
            or self.device_id != "SYN-" + self.sensor_id
            or not home_key(self.home_id)
        ):
            raise StreamError("INVALID_SYNTHETIC_BINDING")


def _bindings(bindings: tuple[Binding, ...]) -> dict[str, Binding]:
    if not 1 <= len(bindings) <= 100:
        raise StreamError("INVALID_SYNTHETIC_BINDINGS")
    for binding in bindings:
        binding.validate()
    result = {binding.device_id: binding for binding in bindings}
    if len(result) != len(bindings) or len({b.home_id for b in bindings}) != len(bindings):
        raise StreamError("INVALID_SYNTHETIC_BINDINGS")
    return result


def _unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StreamError("IOT_DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _invalid_constant(value: str) -> object:
    raise StreamError("IOT_INVALID_JSON")


def decode(event: EventData, bindings: Mapping[str, Binding]) -> Observation:
    # Custom-endpoint IoT properties are AMQP application properties. Their
    # authority is the dedicated Hub-only sender path, not their Python name.
    props = event.properties or {}
    if any(key in event.system_properties for key in (DEVICE, MODULE, AUTH)):
        raise StreamError("IOT_AMBIGUOUS_ORIGIN")
    if any(key.decode() in props for key in (DEVICE, MODULE, AUTH)):
        raise StreamError("IOT_AMBIGUOUS_ORIGIN")
    if MODULE in props:
        raise StreamError("IOT_MODULE_NOT_ALLOWED")
    device, auth = props.get(DEVICE), props.get(AUTH)
    if not isinstance(device, bytes) or not isinstance(auth, bytes) or len(auth) > 1024:
        raise StreamError("IOT_ORIGIN_REQUIRED")
    try:
        device_id = device.decode("ascii")
        method = json.loads(auth, object_pairs_hook=_unique, parse_constant=_invalid_constant)
    except (UnicodeError, ValueError):
        raise StreamError("IOT_ORIGIN_REQUIRED") from None
    if (
        not isinstance(method, dict)
        or method.get("scope") != "device"
        or method.get("type") != "x509"
    ):
        raise StreamError("IOT_X509_DEVICE_REQUIRED")
    binding = bindings.get(device_id)
    if binding is None:
        raise StreamError("IOT_DEVICE_NOT_ALLOWED")
    body = bytearray()
    raw = event.body
    if not isinstance(raw, Iterable) or isinstance(raw, (str, bytes, dict)):
        raise StreamError("IOT_INVALID_ENVELOPE")
    for chunk in raw:
        if not isinstance(chunk, bytes) or len(body) + len(chunk) > 4096:
            raise StreamError("IOT_INVALID_ENVELOPE")
        body.extend(chunk)
    try:
        row = json.loads(body, object_pairs_hook=_unique, parse_constant=_invalid_constant)
    except (UnicodeError, ValueError, RecursionError):
        raise StreamError("IOT_INVALID_JSON") from None
    result = preflight([row])[0]
    if result.get("sensor_id") != binding.sensor_id or result.get("home_id") != binding.home_id:
        raise StreamError("IOT_DEVICE_BINDING_MISMATCH")
    return result


def _observe[T](task: asyncio.Future[T]) -> None:
    if not task.cancelled():
        task.exception()


async def _bounded[T](
    operation: Awaitable[T],
    deadline: float,
    stopped: Callable[[], bool] | None = None,
) -> T:
    task = asyncio.ensure_future(operation)
    try:
        while True:
            if stopped is not None and stopped():
                raise StreamError("RUN_STOPPED")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise StreamError("IOT_OPERATION_TIMEOUT")
            done, _ = await asyncio.wait([task], timeout=min(remaining, 0.05))
            if done:
                return task.result()
    finally:
        if not task.done():
            task.cancel()
        task.add_done_callback(_observe)


async def _cleanup(operations: list[Awaitable[object]]) -> None:
    tasks = [asyncio.ensure_future(operation) for operation in operations]
    if not tasks:
        return
    try:
        done, pending = await asyncio.wait(tasks, timeout=0.5)
        results = await asyncio.gather(*done, return_exceptions=True)
        if pending or any(isinstance(result, BaseException) for result in results):
            raise StreamError("IOT_CLEANUP_FAILED")
    finally:
        # Do not await SDK cancellation acknowledgement beyond the cleanup allowance.
        for task in tasks:
            if not task.done():
                task.cancel()
            task.add_done_callback(_observe)


class HubReceiver:
    def __init__(
        self,
        ingestion: SensorIngestion,
        activation: Activation,
        bindings: tuple[Binding, ...],
    ) -> None:
        if not isinstance(activation, Activation):
            raise StreamError("IOT_ROUTED_RECEIVER_REQUIRED")
        activation.validate()
        self.bindings = _bindings(bindings)
        self.ingestion = ingestion
        self.activation = activation

    async def run(
        self,
        *,
        max_seconds: float,
        max_events: int,
        stop: asyncio.Event | None = None,
    ) -> tuple[Receipt, ...]:
        if (
            type(max_seconds) not in (int, float)
            or not 1 <= max_seconds <= 3600
            or type(max_events) is not int
            or not 1 <= max_events <= 100000
        ):
            raise StreamError("INVALID_RECEIVE_LIMIT")
        self.activation.validate()
        deadline = time.monotonic() + max_seconds - 0.5
        credential: ManagedIdentityCredential | None = None
        client: EventHubConsumerClient | None = None
        tasks: list[asyncio.Task[None] | asyncio.Task[bool]] = []
        finished = asyncio.Event()
        failure: StreamError | None = None
        receipts: list[Receipt] = []
        locks: dict[str, asyncio.Lock] = {}
        admitted = 0

        async def on_event(context: PartitionContext, event: EventData | None) -> None:
            nonlocal failure, admitted
            async with locks.setdefault(context.partition_id, asyncio.Lock()):
                if finished.is_set() or event is None:
                    return
                if admitted >= max_events:
                    return
                try:
                    if time.monotonic() >= deadline or (stop and stop.is_set()):
                        raise StreamError("RUN_STOPPED")
                    row = decode(event, self.bindings)
                    admitted += 1
                    received = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
                    # A cancelled wait cannot cancel a SQL commit. Keep its
                    # stable identity, observe completion, and never checkpoint it.
                    sql = asyncio.create_task(
                        asyncio.to_thread(
                            self.ingestion.consume,
                            [row],
                            received_at=received,
                        )
                    )
                    sql.add_done_callback(_observe)
                    receipt = (await _bounded(asyncio.shield(sql), deadline))[0]
                    receipts.append(receipt)
                    if finished.is_set() or (stop and stop.is_set()):
                        return
                    if len(receipts) >= max_events:
                        finished.set()
                except (ConsumerError, StreamError) as error:
                    failure = StreamError(str(error))
                    finished.set()
                except Exception:
                    failure = StreamError("IOT_CALLBACK_FAILED")
                    finished.set()

        async def on_error(context: PartitionContext | None, error: Exception) -> None:
            nonlocal failure
            failure = StreamError("IOT_RECEIVE_FAILED")
            finished.set()

        try:
            credential = ManagedIdentityCredential(
                client_id=self.activation.managed_identity_client_id
            )
            client = EventHubConsumerClient(
                fully_qualified_namespace=self.activation.eventhub_namespace,
                consumer_group=self.activation.consumer_group,
                credential=credential,
                eventhub_name=self.activation.eventhub_name,
                logging_enable=False,
                retry_total=0,
                auth_timeout=1,
                prefetch=1,
            )
            receive = asyncio.create_task(
                client.receive(
                    on_event,
                    on_error=on_error,
                    starting_position="-1",
                    starting_position_inclusive=False,
                    max_wait_time=0.1,
                    prefetch=1,
                )
            )
            tasks.append(receive)
            waiting = asyncio.create_task(finished.wait())
            tasks.append(waiting)
            stopping = asyncio.create_task(stop.wait()) if stop is not None else None
            if stopping is not None:
                tasks.append(stopping)
            done, _ = await asyncio.wait(
                tasks,
                timeout=max(0.0, deadline - time.monotonic()),
                return_when=asyncio.FIRST_COMPLETED,
            )
            if failure is not None:
                raise failure
            if stopping in done:
                raise StreamError("RUN_STOPPED")
            if waiting not in done:
                raise StreamError("IOT_RECEIVE_STOPPED" if receive in done else "RUN_DEADLINE")
            return tuple(receipts)
        except (StreamError, asyncio.CancelledError):
            raise
        except Exception:
            raise StreamError("IOT_RECEIVE_FAILED") from None
        finally:
            finished.set()
            for task in tasks:
                task.cancel()
            operations: list[Awaitable[object]] = []
            if tasks:
                operations.append(asyncio.gather(*tasks, return_exceptions=True))
            if client is not None:
                operations.append(client.close())
            if credential is not None:
                operations.append(credential.close())
            await _cleanup(operations)


class HubPublisher:
    def __init__(
        self,
        activation: Activation | DeviceActivation,
        bindings: tuple[Binding, ...],
        certificates: Mapping[str, X509],
    ) -> None:
        activation.validate()
        self.bindings = _bindings(bindings)
        if set(certificates) != set(self.bindings):
            raise StreamError("PER_DEVICE_CERTIFICATES_REQUIRED")
        self.activation = activation
        self._certificates = dict(certificates)

    async def run(
        self,
        frames: tuple[Frame, ...],
        budget: RunBudget,
        *,
        speed: float = 1.0,
        pacer: Pacer | None = None,
        truth: Callable[[dict[str, object]], None],
    ) -> int:
        self.activation.validate()
        frames = tuple(
            Frame(
                frame.device_id,
                frame.slot,
                dict(frame.row),
                frame.truth,
                frame.selected_stock_sha256,
                frame.nominal_at,
            )
            for frame in frames
        )
        budget.validate(frames)
        control = pacer or Pacer(budget, speed=speed)
        now = time.monotonic()
        if (
            type(control.deadline) not in (int, float)
            or not math.isfinite(control.deadline)
            or control.deadline > now + budget.max_seconds
        ):
            raise StreamError("INVALID_RUN_DEADLINE")
        if (
            type(control.max_per_second) not in (int, float)
            or not math.isfinite(control.max_per_second)
            or not 0 < control.max_per_second <= budget.max_per_second
        ):
            raise StreamError("INVALID_RUN_RATE")
        deadline = min(control.deadline, now + budget.max_seconds) - 0.5
        for frame in frames:
            binding = self.bindings.get(frame.device_id)
            if binding is None or (frame.row.get("sensor_id"), frame.row.get("home_id")) != (
                binding.sensor_id,
                binding.home_id,
            ):
                raise StreamError("IOT_DEVICE_BINDING_MISMATCH")
            if frame.row.get("source_type") != "SYNTHETIC":
                raise StreamError("SYNTHETIC_ONLY")
        clients: dict[str, IoTHubDeviceClient] = {}
        sent = 0
        previous: datetime | None = None

        async def send(client: IoTHubDeviceClient, message: Message) -> None:
            await control.admit_send()
            await client.send_message(message)

        try:
            for frame in frames:
                stamp = frame.nominal_at
                interval = max(0.0, (stamp - previous).total_seconds()) if previous else 0.0
                await _bounded(control.wait(0 if frame.truth == "burst" else interval), deadline)
                previous = stamp
                if frame.truth == "disconnect":
                    truth(
                        {
                            "source_type": "SYNTHETIC",
                            "reference": frame.reference,
                            "selected_stock_sha256": frame.selected_stock_sha256,
                            "fault": frame.truth,
                            "status": "injected-stop",
                        }
                    )
                    raise StreamError("INJECTED_DISCONNECT")
                client = clients.get(frame.device_id)
                if client is None:
                    client = IoTHubDeviceClient.create_from_x509_certificate(
                        self._certificates[frame.device_id],
                        self.activation.hub_hostname,
                        frame.device_id,
                        auto_connect=False,
                        connection_retry=False,
                        ensure_desired_properties=False,
                    )
                    clients[frame.device_id] = client
                    await _bounded(client.connect(), deadline, lambda: control.stopped)
                message = Message(wire(frame.row).decode("ascii"))
                message.content_type = "application/json"
                message.content_encoding = "utf-8"
                message.message_id = frame.row["reading_id"]
                truth(
                    {
                        "source_type": "SYNTHETIC",
                        "reference": frame.reference,
                        "selected_stock_sha256": frame.selected_stock_sha256,
                        "slot": frame.slot,
                        "fault": frame.truth,
                        "status": "attempt",
                    }
                )
                await _bounded(send(client, message), deadline, lambda: control.stopped)
                sent += 1
                truth(
                    {
                        "source_type": "SYNTHETIC",
                        "reference": frame.reference,
                        "selected_stock_sha256": frame.selected_stock_sha256,
                        "slot": frame.slot,
                        "fault": frame.truth,
                        "status": "sent",
                    }
                )
            return sent
        except (StreamError, asyncio.CancelledError):
            raise
        except Exception:
            raise StreamError("IOT_PUBLISH_FAILED") from None
        finally:
            await _cleanup([client.shutdown() for client in clients.values()])
