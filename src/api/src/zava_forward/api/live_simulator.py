"""Live synthetic readings for every home into Azure IoT Hub (issue 184, stage 2).

`python -m zava_forward.api.live_simulator` sends one reading per home per 5-minute UTC slot built
by `zava_forward.core.synthetic.live_readings`. The default sink is stdout (dry run). The IoT Hub
sink needs an owner approval reference, the hub host name and a per-device X.509 certificate and
key pair mounted from a secret store; nothing is read from or written to source control, and no
key or connection string is ever logged. The simulator never connects to, discovers or represents
installed real devices, uses no AI and has no resident-facing action.
"""

import argparse
import asyncio
import logging
import math
import os
import random
import re
import sys
import time
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from zava_forward.core.diagnostic_logging import install_diagnostic_redaction
from zava_forward.core.synthetic import live_readings as lr
from zava_forward.core.synthetic.run_plan import (
    B1_DAILY_MESSAGES,
    B1_MONTHLY_USD,
    RESERVED_HEADROOM,
)
from zava_forward.core.synthetic.sensor_identity import demo_homes
from zava_forward.core.synthetic.sensor_stream import StreamError

from . import live_control

if TYPE_CHECKING:
    from .iot_stream import DeviceActivation

LOG = logging.getLogger("zava_forward.live_simulator")
DAILY_MESSAGE_BUDGET = B1_DAILY_MESSAGES - RESERVED_HEADROOM
DEVICE_FILE = re.compile(r"SYN-[A-Z0-9][A-Z0-9_-]{0,19}\Z")
Sleep = Callable[[float], Awaitable[None]]
FENCED = "RUN_CONTROL_FENCED"


class SinkError(RuntimeError):
    """Fixed-code sink failure; the text never carries SDK or credential detail."""

    def __init__(self, code: str, retryable: bool = True) -> None:
        super().__init__(code)
        self.code = code
        self.retryable = retryable


class Sink(Protocol):
    async def send(self, device_id: str, message_id: str, body: bytes) -> None: ...

    async def close(self) -> None: ...


class MemorySink:
    """In-memory fake for tests; `failures` maps a device to a number of transient failures."""

    def __init__(self, failures: Mapping[str, int] | None = None) -> None:
        self.messages: list[tuple[str, str, bytes]] = []
        self.attempts = 0
        self.closed = False
        self._failures = dict(failures or {})

    async def send(self, device_id: str, message_id: str, body: bytes) -> None:
        self.attempts += 1
        if self._failures.get(device_id, 0) > 0:
            self._failures[device_id] -= 1
            raise SinkError("FAKE_TRANSIENT")
        self.messages.append((device_id, message_id, body))

    async def close(self) -> None:
        self.closed = True


class StdoutSink:
    """Dry run: prints identifiers and size only (never the readings) and sends nothing."""

    async def send(self, device_id: str, message_id: str, body: bytes) -> None:
        label = "SYNTHETIC" if b"SYNTHETIC" in body else "UNLABELLED"
        print(f"DRY-RUN {device_id} {message_id} {label} bytes={len(body)}", flush=True)

    async def close(self) -> None:
        return None


class IotHubSink:
    """Per-home simulated device over X.509; at most `max_open` connections are kept open."""

    def __init__(
        self,
        activation: "DeviceActivation",
        cert_dir: Path,
        max_open: int = 100,
        client_factory: Callable[[str, str, Path, Path], Any] | None = None,
    ) -> None:
        activation.validate()
        if not 1 <= max_open <= 1000:
            raise StreamError("INVALID_RUN_LIMIT")
        self._activation = activation
        self._cert_dir = cert_dir
        self._max_open = max_open
        self._factory = client_factory or _sdk_client
        self._clients: dict[str, Any] = {}

    async def send(self, device_id: str, message_id: str, body: bytes) -> None:
        if not DEVICE_FILE.fullmatch(device_id):
            raise SinkError("INVALID_DEVICE_ID", retryable=False)
        cert, key = self._cert_dir / f"{device_id}.pem", self._cert_dir / f"{device_id}.key"
        if not (cert.is_file() and key.is_file()):
            raise SinkError("DEVICE_CREDENTIAL_MISSING", retryable=False)
        client = self._clients.get(device_id)
        try:
            if client is None:
                while len(self._clients) >= self._max_open:
                    oldest = next(iter(self._clients))
                    await _quiet_shutdown(self._clients.pop(oldest))
                client = self._factory(self._activation.hub_hostname, device_id, cert, key)
                self._clients[device_id] = client
                await client.connect()
            await client.send_message(_message(message_id, body))
        except Exception:
            self._clients.pop(device_id, None)
            if client is not None:
                await _quiet_shutdown(client)
            raise SinkError("IOT_SEND_FAILED") from None

    async def close(self) -> None:
        clients, self._clients = list(self._clients.values()), {}
        for client in clients:
            await _quiet_shutdown(client)


def _sdk_client(hostname: str, device_id: str, cert: Path, key: Path) -> Any:
    from azure.iot.device import X509
    from azure.iot.device.aio import IoTHubDeviceClient

    return IoTHubDeviceClient.create_from_x509_certificate(
        X509(str(cert), str(key)),  # type: ignore[no-untyped-call]
        hostname,
        device_id,
        auto_connect=False,
        connection_retry=False,
        ensure_desired_properties=False,
    )


def _message(message_id: str, body: bytes) -> Any:
    from azure.iot.device import Message

    message = Message(body.decode("ascii"))  # type: ignore[no-untyped-call]
    message.content_type = "application/json"
    message.content_encoding = "utf-8"
    message.message_id = message_id
    return message


async def _quiet_shutdown(client: Any) -> None:
    try:
        await client.shutdown()
    except Exception:
        LOG.warning("device client shutdown failed")


@dataclass(frozen=True)
class Limits:
    max_per_second: float = 10.0
    batch_size: int = 50
    attempts: int = 4
    backoff_base_seconds: float = 1.0
    backoff_cap_seconds: float = 30.0

    def validate(self) -> None:
        numbers = (self.max_per_second, self.backoff_base_seconds, self.backoff_cap_seconds)
        if any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in numbers):
            raise StreamError("INVALID_RUN_LIMIT")
        if (
            not 0 < self.max_per_second <= 100
            or type(self.batch_size) is not int
            or not 1 <= self.batch_size <= 500
            or type(self.attempts) is not int
            or not 1 <= self.attempts <= 10
        ):
            raise StreamError("INVALID_RUN_LIMIT")


def check_capacity(
    homes: int, limits: Limits, cadence_seconds: int = lr.SLOT_SECONDS
) -> dict[str, float | int]:
    """Refuse a fleet that would exceed the B1 daily message budget or overrun its own slot."""
    limits.validate()
    lr.require_cadence(cadence_seconds)
    if type(homes) is not int or homes < 1:
        raise StreamError("NO_HOMES")
    per_day = homes * (86400 // cadence_seconds)
    if per_day > DAILY_MESSAGE_BUDGET:
        raise StreamError("B1_QUOTA_HEADROOM")
    if homes / limits.max_per_second > cadence_seconds * 0.8:
        raise StreamError("RATE_TOO_LOW_FOR_HOMES")
    return {
        "homes": homes,
        "messages_per_day": per_day,
        "daily_budget": DAILY_MESSAGE_BUDGET,
        "quota_fraction": round(per_day / B1_DAILY_MESSAGES, 4),
        "seconds_per_slot": round(homes / limits.max_per_second, 1),
        "hub_usd_per_month": B1_MONTHLY_USD,
    }


@dataclass
class Summary:
    slot: datetime
    homes: int
    sent: int = 0
    failed: int = 0
    retries: int = 0
    codes: dict[str, int] = field(default_factory=dict)


class Pacer:
    """Spaces sends at least 1/max_per_second apart across all concurrent tasks."""

    def __init__(
        self,
        rate: float,
        sleep: Sleep = asyncio.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._gap = 1.0 / rate
        self._sleep = sleep
        self._clock = clock
        self._next = 0.0
        self._lock = asyncio.Lock()

    async def admit(self) -> None:
        async with self._lock:
            now = self._clock()
            wait = self._next - now
            self._next = max(now, self._next) + self._gap
            if wait > 0:
                await self._sleep(wait)


def attempt_permitted(
    control_path: Path,
    home: str,
    moment: datetime,
    demo: Sequence[str] | None = None,
    refusals: list[str] | None = None,
) -> bool:
    """Fresh control read: sending, unexpired and the home still in the cohort; else False.

    With `demo`, the control cohort must still be exactly that set; a differing cohort is also
    appended to `refusals` as DEMO_COHORT_MISMATCH so the caller can tell it from a stop.
    """
    try:
        control = live_control.load(control_path)
        if demo is not None and set(control.homes) != set(demo):
            if refusals is not None:
                refusals.append("DEMO_COHORT_MISMATCH")
            return False
        return live_control.decide(control, moment) == live_control.SEND and home in control.homes
    except StreamError:
        return False


def _permitted(attempt_gate: Callable[[str], bool], home: str) -> bool:
    try:
        return attempt_gate(home)
    except Exception:  # noqa: BLE001 - any gate failure is a refusal
        return False


async def send_slot(
    homes: Sequence[str],
    slot: datetime,
    generator: lr.Generator,
    sink: Sink,
    limits: Limits,
    *,
    sleep: Sleep = asyncio.sleep,
    clock: Callable[[], float] = time.monotonic,
    rng: random.Random | None = None,
    attempt_gate: Callable[[str], bool] | None = None,
) -> Summary:
    """Send one reading per home for the slot in batches, throttled, with exponential backoff.

    `attempt_gate(home)` is asked after pacing and right before every send attempt, retries
    included. A False or an error stops that home with `RUN_CONTROL_FENCED`; a send already handed
    to the sink is not recalled.
    """
    check_capacity(len(homes), limits, generator.cadence_seconds)
    if len(set(homes)) != len(homes):
        raise lr.LiveReadingError("DEVICE_ID_COLLISION")
    jitter = rng or random.Random(generator.seed)
    pacer = Pacer(limits.max_per_second, sleep, clock)
    summary = Summary(lr.slot_floor(slot, generator.cadence_seconds), len(homes))

    async def one(home: str) -> None:
        try:
            reading = generator.reading(home, slot)
            lr.validate_row(reading.row())
        except lr.LiveReadingError as error:
            summary.codes[str(error)] = summary.codes.get(str(error), 0) + 1
            summary.failed += 1
            return
        for attempt in range(limits.attempts):
            await pacer.admit()
            if attempt_gate is not None and not _permitted(attempt_gate, home):
                summary.codes[FENCED] = summary.codes.get(FENCED, 0) + 1
                summary.failed += 1
                return
            try:
                await sink.send(reading.device_id, reading.reading_id, reading.body())
            except SinkError as error:
                summary.codes[error.code] = summary.codes.get(error.code, 0) + 1
                if not error.retryable or attempt == limits.attempts - 1:
                    summary.failed += 1
                    return
                summary.retries += 1
                delay = min(limits.backoff_cap_seconds, limits.backoff_base_seconds * 2**attempt)
                await sleep(delay * (0.5 + jitter.random() / 2))
            else:
                summary.sent += 1
                return

    for start in range(0, len(homes), limits.batch_size):
        await asyncio.gather(*(one(h) for h in homes[start : start + limits.batch_size]))
    return summary


class HomeListError(Exception):
    """Fixed-text failure reading the home list; the cause and connection details are never kept."""


HOME_IDS_SQL = "SELECT id FROM cases WHERE closed = 0 ORDER BY id"


def mssql_home_ids(env: Mapping[str, str], connect: Callable[[], Any] | None = None) -> list[str]:
    """Read open case ids with one parameter-free SELECT; no DDL, seeding, migration or write."""
    conn = None
    try:
        if connect is None:
            from zava_forward.core.mssqlstore import _Conn, connection_string

            conn_str, token = connection_string(env), env.get("ZF_SQL_TOKEN")

            def connect() -> Any:
                return _Conn(conn_str, token)

        conn = connect()
        return [str(row[0]) for row in conn.execute(HOME_IDS_SQL).fetchall()]
    except (Exception, SystemExit):  # noqa: BLE001 - no driver text or traceback gets out
        raise HomeListError("HOME_LIST_UNAVAILABLE") from None
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass


def store_home_ids(env: Mapping[str, str] | None = None) -> list[str]:
    """Open home (case) ids. mssql uses a read-only SELECT of ids; json and sqlite are local/dev."""
    env = os.environ if env is None else env
    if (env.get("ZF_STORE") or "json").lower() == "mssql":
        return mssql_home_ids(env)
    from zava_forward.core.factory import open_store

    try:
        store = open_store(env)
    except (Exception, SystemExit):  # noqa: BLE001
        raise HomeListError("HOME_LIST_UNAVAILABLE") from None
    if hasattr(store, "query_case_ids"):
        ids: list[str] = []
        after: str | None = None
        while page := store.query_case_ids(after=after, limit=500):
            ids.extend(page)
            after = page[-1]
        return ids
    return sorted(cid for cid, case in store.cases.items() if not case.get("closed"))


def _demo_cohort(homes: Sequence[str], demo: Sequence[str], exact: bool = False) -> list[str]:
    """Exactly the configured five homes, or a refusal; never a subset or another home.

    `exact` also refuses extra homes (the control cohort must be the demo set itself).
    """
    present = set(homes)
    if not set(demo) <= present or (exact and present != set(demo)):
        raise StreamError("DEMO_COHORT_MISMATCH")
    return list(demo)


def cohort_homes(control: live_control.Control, existing: Sequence[str]) -> list[str]:
    """The control cohort present in the store, in control order; never the whole fleet."""
    present = set(existing)
    cohort = [home for home in control.homes if home in present]
    if not cohort:
        raise StreamError("COHORT_NOT_IN_STORE")
    return cohort


async def run(
    list_homes: Callable[[], Sequence[str]],
    generator: lr.Generator,
    sink: Sink,
    limits: Limits,
    *,
    once: bool = False,
    max_slots: int | None = None,
    refresh_slots: int = 12,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
    sleep: Sleep = asyncio.sleep,
    clock: Callable[[], float] = time.monotonic,
    report: Callable[[Summary], None] | None = None,
    gate: Callable[[datetime], bool] | None = None,
    attempt_gate: Callable[[str], bool] | None = None,
    fence_error: Callable[[], str | None] | None = None,
) -> list[Summary]:
    """Send the current slot, then (unless `once`) one per cadence; missed slots are skipped.

    `gate` is asked before every slot and a False ends the run, so a stop or an expiry is final.
    `attempt_gate` is also asked before every send attempt; a slot it fenced ends the run, and
    `fence_error` then names a DEMO_COHORT_MISMATCH refusal to raise instead of ending cleanly.
    """
    summaries: list[Summary] = []
    homes: Sequence[str] = []
    try:
        while True:
            slot = lr.slot_floor(now(), generator.cadence_seconds)
            if gate is not None and not gate(now()):
                LOG.warning("run control: stopped or expired; nothing sent")
                return summaries
            try:
                if not homes or len(summaries) % refresh_slots == 0:
                    homes = list_homes() or homes
            except StreamError as error:
                if str(error) == "DEMO_COHORT_MISMATCH":
                    raise
                LOG.error("run control refused the current cohort; nothing sent")
                return summaries
            except Exception:
                LOG.error("home enumeration failed; reusing the previous list")
            if homes:
                summary = await send_slot(
                    homes,
                    slot,
                    generator,
                    sink,
                    limits,
                    sleep=sleep,
                    clock=clock,
                    attempt_gate=attempt_gate,
                )
                summaries.append(summary)
                if report:
                    report(summary)
                if FENCED in summary.codes:
                    if fence_error is not None and fence_error() == "DEMO_COHORT_MISMATCH":
                        raise StreamError("DEMO_COHORT_MISMATCH")
                    LOG.warning("run control: stopped or expired during the slot")
                    return summaries
            else:
                LOG.error("no homes available for slot %s", slot.isoformat())
            if once or (max_slots is not None and len(summaries) >= max_slots):
                return summaries
            await sleep(
                max(0.0, (lr.next_slot(slot, generator.cadence_seconds) - now()).total_seconds())
            )
    finally:
        await sink.close()


def _report(summary: Summary) -> None:
    LOG.info(
        "slot=%s homes=%d sent=%d failed=%d retries=%d codes=%s",
        summary.slot.strftime("%Y-%m-%dT%H:%MZ"),
        summary.homes,
        summary.sent,
        summary.failed,
        summary.retries,
        dict(sorted(summary.codes.items())),
    )


def _sink(args: argparse.Namespace, env: Mapping[str, str]) -> Sink:
    if args.sink == "stdout":
        return StdoutSink()
    try:
        from .iot_stream import DeviceActivation
    except ModuleNotFoundError:
        raise StreamError("IOT_SDK_MISSING") from None
    activation = DeviceActivation(
        env.get("ZF_SIM_HUB_HOSTNAME", ""),
        env.get("ZF_SIM_APPROVAL", ""),
        env.get("ZF_SIM_RESOURCE_GROUP", "ama"),
    )
    cert_dir = env.get("ZF_SIM_CERT_DIR", "")
    if not cert_dir:
        raise StreamError("IOT_ACTIVATION_REQUIRED")
    return IotHubSink(activation, Path(cert_dir))


def main(argv: Sequence[str], env: Mapping[str, str] | None = None) -> int:
    env = os.environ if env is None else env
    parser = argparse.ArgumentParser(prog="zava_forward.api.live_simulator")
    parser.add_argument("--sink", choices=("stdout", "iothub"), default="stdout")
    parser.add_argument("--once", action="store_true", help="send the current slot and exit")
    try:
        default_seed = int(env.get("ZF_SIM_SEED", "184"))
    except ValueError:
        print("Cannot run: SIM_CONFIG_INVALID", file=sys.stderr)
        return 2
    try:
        default_cadence = int(env.get("ZF_SIM_CADENCE_MINUTES", "5"))
    except ValueError:
        default_cadence = 0
    parser.add_argument("--seed", type=int, default=default_seed)
    parser.add_argument("--max-homes", type=int, default=0, help="0 means every home (stdout only)")
    parser.add_argument("--control-file", default=env.get("ZF_SIM_CONTROL_FILE", ""))
    parser.add_argument("--cadence-minutes", type=int, choices=(1, 5), default=default_cadence)
    parser.add_argument("--max-per-second", type=float, default=Limits.max_per_second)
    parser.add_argument("--batch-size", type=int, default=Limits.batch_size)
    args = parser.parse_args(list(argv))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    install_diagnostic_redaction()
    limits = Limits(max_per_second=args.max_per_second, batch_size=args.batch_size)
    try:
        sink = _sink(args, env)
        if args.cadence_minutes not in (1, 5):
            raise StreamError("SIM_CONFIG_INVALID")
        generator = lr.Generator(args.seed, cadence_seconds=args.cadence_minutes * 60)
        try:
            demo = demo_homes(env.get("ZF_ASSIST_QUALITY_DEMO_HOMES"))
        except ValueError:
            raise StreamError("DEMO_HOMES_INVALID") from None
        if demo is not None and args.max_homes > 0:
            raise StreamError("SIM_CONFIG_INVALID")

        control_path = Path(args.control_file) if args.control_file else None
        if args.sink == "iothub" and control_path is None:
            raise StreamError("CONTROL_REQUIRED")

        cached: list[str] = []

        def homes() -> list[str]:
            if control_path is None:
                ids = store_home_ids(env)
                if demo is not None:
                    return _demo_cohort(ids, demo)
                return ids[: args.max_homes] if args.max_homes > 0 else ids
            control = live_control.load(control_path)
            if demo is not None:
                # The control itself must be exactly the five, before any store intersection.
                _demo_cohort(control.homes, demo, exact=True)
            try:
                result = cohort_homes(control, store_home_ids(env))
            except HomeListError:
                # Transient store failure: reuse only cached homes the current control authorizes.
                result = [h for h in cached if h in control.homes]
                if not result:
                    raise
            if demo is not None:
                result = _demo_cohort(result, demo)
            cached[:] = result
            return result

        def gate(moment: datetime) -> bool:
            if control_path is None:
                return True
            try:
                return (
                    live_control.decide(live_control.load(control_path), moment)
                    == live_control.SEND
                )
            except StreamError:
                return False

        refusals: list[str] = []

        def permit(home: str) -> bool:
            return attempt_permitted(
                Path(args.control_file), home, datetime.now(UTC), demo, refusals
            )

        if not gate(datetime.now(UTC)):
            LOG.warning("run control: stopped or expired; nothing sent")
            return 0
        first = homes()
        LOG.info("capacity %s", check_capacity(len(first), limits, generator.cadence_seconds))
        asyncio.run(
            run(
                lambda: homes(),
                generator,
                sink,
                limits,
                once=args.once,
                report=_report,
                gate=gate,
                attempt_gate=permit if control_path is not None else None,
                fence_error=lambda: refusals[0] if refusals else None,
                refresh_slots=1,
            )
        )
    except HomeListError as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 3
    except (StreamError, lr.LiveReadingError, SystemExit) as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001 - fixed code only, never a traceback or connection detail
        print("Cannot run: SIM_FAILED", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
