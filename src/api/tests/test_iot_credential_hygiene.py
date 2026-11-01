"""No device key or connection string in source, logs or telemetry (issue 184, criterion 3).

Local, constructed evidence only: a repository text scan and a fake-SDK publish run that
captures logs, truth records, wire payloads and failure text. It proves nothing about real
credential issue, storage, rotation or Hub-side telemetry.
"""

import asyncio
import json
import logging
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from azure.iot.device import X509
from zava_forward.core.synthetic import sensor_stock
from zava_forward.core.synthetic.sensor_stream import Replay, RunBudget, StreamError, replay

from zava_forward.api.iot_stream import Activation, Binding, HubPublisher

ROOT = Path(__file__).resolve().parents[3]
SCANNED = ("src", "infra", "docs", ".github")
SUFFIXES = {".py", ".md", ".bicep", ".json", ".yaml", ".yml", ".toml", ".txt", ".env"}
SKIPPED_PARTS = {"node_modules", ".git", ".venv", "__pycache__"}
PATTERNS = {
    "shared access key value": re.compile(r"SharedAccessKey\s*=\s*[A-Za-z0-9+/]{20,}={0,2}"),
    "shared access signature": re.compile(r"SharedAccessSignature\s+sr=\S+&sig=\S+"),
    "device connection string": re.compile(
        r"HostName=[^;\s]+\.azure-devices\.net;[^\n]*(?:SharedAccessKey|x509)\s*=", re.I
    ),
    "private key block": re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----"),
}
MARKER = "MARKER-DEVICE-SECRET-7731"
ACTIVE = Activation(
    "iot-fixture.azure-devices.net",
    "eh-iot-fixture.servicebus.windows.net",
    "constructed approval, not live authority",
    routing_ready=True,
)


def is_scanned(path: Path) -> bool:
    name = path.name
    dotenv = name == ".env" or name.startswith(".env.")
    return dotenv or path.suffix in SUFFIXES


def scan_directory(base: Path, skip: Path | None = None) -> list[str]:
    findings: list[str] = []
    for path in base.rglob("*"):
        if (
            not path.is_file()
            or not is_scanned(path)
            or SKIPPED_PARTS & set(path.parts)
            or (skip is not None and path.resolve() == skip)
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(base)}: {name}")
    return findings


class SourceScanTests(unittest.TestCase):
    def test_dotenv_files_are_scanned(self) -> None:
        secret = "HostName=h.azure-devices.net;DeviceId=d;SharedAccessKey=" + "A" * 24 + "=="
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name in (".env", ".env.local", "settings.env"):
                (base / name).write_text(secret, encoding="utf-8")
            (base / "notes.dat").write_text(secret, encoding="utf-8")
            findings = scan_directory(base)
        flagged = {f.split(":")[0] for f in findings}
        self.assertEqual(flagged, {".env", ".env.local", "settings.env"})

    def test_no_device_key_or_connection_string_in_repository_text(self) -> None:
        this = Path(__file__).resolve()
        findings: list[str] = []
        for top in SCANNED:
            base = ROOT / top
            if base.is_dir():
                findings += [f"{top}/{f}" for f in scan_directory(base, this)]
        self.assertEqual(findings, [])

    def test_scanner_detects_each_pattern(self) -> None:
        samples = {
            "shared access key value": "SharedAccessKey=" + "A" * 24 + "==",
            "shared access signature": "SharedAccessSignature sr=h.azure-devices.net&sig=abc",
            "device connection string": "HostName=h.azure-devices.net;DeviceId=d;x509=true",
            "private key block": "-----BEGIN " + "RSA PRIVATE KEY-----",
        }
        for name, sample in samples.items():
            with self.subTest(name=name):
                self.assertRegex(sample, PATTERNS[name])

    def test_publisher_source_has_no_connection_string_client_factory(self) -> None:
        source = (ROOT / "src/api/src/zava_forward/api/iot_stream.py").read_text("utf-8")
        self.assertNotIn("create_from_connection_string", source)
        self.assertNotIn("create_from_sastoken", source)
        self.assertNotRegex(source, r"import logging|logging\.getLogger")
        self.assertNotIn("print(", source)


class RuntimeLeakTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        selected = sensor_stock.select(
            [
                {"synthetic_home_id": h, "is_synthetic": "true", "monitoring_consent": "granted"}
                for h in ("ZF-1", "ZF-2")
            ],
            2,
        )
        self.frames = replay(selected, Replay(fault="burst", end_slot=2))
        bindings = tuple(
            Binding(f.device_id, f.row["sensor_id"], f.row["home_id"]) for f in self.frames
        )
        bindings = tuple({b.device_id: b for b in bindings}.values())
        certs = {b.device_id: X509(MARKER + ".pem", MARKER + ".key", MARKER) for b in bindings}
        self.publisher = HubPublisher(ACTIVE, bindings, certs)
        self.budget = RunBudget(
            "Fixture Owner",
            "USD60 source model",
            "constructed alert",
            max_seconds=2,
            max_per_second=100,
        )
        self.truth: list[dict[str, object]] = []
        self.sent: list[str] = []

    def client(self, failure: Exception | None = None) -> Mock:
        async def capture(message: object) -> None:
            if failure is not None:
                raise failure
            self.sent.append(str(getattr(message, "data", "")))

        return Mock(connect=AsyncMock(), send_message=capture, shutdown=AsyncMock())

    async def run_publisher(self, failure: Exception | None = None) -> str:
        outcome = ""
        with (
            self.assertLogs(level=logging.DEBUG) as logs,
            patch(
                "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
                side_effect=lambda *a, **k: self.client(failure),
            ),
        ):
            logging.getLogger("zava_forward.api").debug("run start")
            try:
                await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
            except StreamError as error:
                if failure is None:
                    raise
                outcome = str(error) + repr(error)
        return "\n".join(logs.output) + outcome

    def assert_clean(self, captured: str) -> None:
        surfaces = [captured, json.dumps(self.truth), "\n".join(self.sent)]
        surfaces += [repr(self.publisher), repr(ACTIVE), repr(self.publisher.bindings)]
        for surface in surfaces:
            self.assertNotIn(MARKER, surface)
            self.assertNotRegex(surface, r"SharedAccess|HostName=|PRIVATE KEY")

    async def test_successful_run_leaks_no_credential_material(self) -> None:
        captured = await self.run_publisher()
        self.assertTrue(self.sent)
        self.assert_clean(captured)

    async def test_failure_text_with_credential_is_replaced_by_stable_code(self) -> None:
        captured = await self.run_publisher(RuntimeError(f"HostName=x;SharedAccessKey={MARKER}"))
        self.assertIn("IOT_PUBLISH_FAILED", captured)
        self.assert_clean(captured)

    async def test_timeout_leaks_nothing(self) -> None:
        async def blocked(*args: object) -> None:
            await asyncio.Event().wait()

        client = self.client()
        client.connect = blocked
        with patch(
            "zava_forward.api.iot_stream.IoTHubDeviceClient.create_from_x509_certificate",
            return_value=client,
        ):
            with self.assertRaises(StreamError) as caught:
                await self.publisher.run(self.frames, self.budget, truth=self.truth.append)
        self.assert_clean(repr(caught.exception))
