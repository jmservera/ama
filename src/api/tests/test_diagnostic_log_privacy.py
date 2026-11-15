"""Issue 146 criterion 4: diagnostic records exclude personal data, readings and chat text."""

import asyncio
import io
import json
import logging
import unittest
from collections.abc import Iterator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from typing import Any
from unittest.mock import patch

from zava_forward.core import diagnostic_logging as dl
from zava_forward.core.synthetic.sensor_stream import StreamError

from zava_forward.api import iot_stream
from zava_forward.api import live_simulator as ls

EMAIL = "resident.canary@example.org"
PROMPT = "my boiler is broken and I live at 12 Canary Road"
REPLY = "Canary reply text for the resident"
READING = "temperature_c=21.7371"
CANARIES = (EMAIL, PROMPT, REPLY, "Canary", "21.7371")


class _Capture(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.lines.append(self.format(record))


@contextmanager
def captured_logs() -> Iterator[list[str]]:
    dl.install_diagnostic_redaction(console=False)
    handler = _Capture()
    logger = logging.getLogger("zava_forward.test_diag_privacy")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        yield handler.lines
    finally:
        logger.removeHandler(handler)
        dl.uninstall_diagnostic_redaction()


class _Event:
    def __init__(self, body: list[bytes], props: dict[Any, Any]) -> None:
        self.body = body
        self.properties = props
        self.system_properties: dict[Any, Any] = {}


class DiagnosticLogPrivacyTests(unittest.TestCase):
    def assertClean(self, text: str) -> None:
        for canary in CANARIES:
            self.assertNotIn(canary, text)

    def test_chat_and_personal_data_in_arguments_extras_and_exceptions_are_dropped(self) -> None:
        log = logging.getLogger("zava_forward.test_diag_privacy")
        with captured_logs() as lines:
            log.error("chat failed for %s: %s", EMAIL, PROMPT, extra={"reply": REPLY})
            log.warning("assistant reply=%s question: %s", REPLY, PROMPT)
            try:
                raise RuntimeError(f"{EMAIL} {PROMPT} {REPLY}")
            except RuntimeError:
                log.exception("assistant unavailable")
        self.assertEqual(len(lines), 3)
        self.assertClean("\n".join(lines))
        self.assertIn("exc=RuntimeError", lines[2])

    def test_iot_rejection_logs_carry_codes_not_payload_readings(self) -> None:
        binding = iot_stream.Binding("SYN-S1", "S1", "HOME-001")
        auth = json.dumps({"scope": "device", "type": "x509"}).encode()
        props = {iot_stream.DEVICE: b"SYN-S1", iot_stream.AUTH: auth}
        log = logging.getLogger("zava_forward.test_diag_privacy")
        with captured_logs() as lines:
            for body in (f'{{"reading": "{READING}"'.encode(), b"x" * 5000):
                event = _Event([body], props)
                try:
                    iot_stream.decode(event, {"SYN-S1": binding})  # type: ignore[arg-type]
                except StreamError as error:
                    log.error("rejected message %s body=%s", error, body.decode())
        self.assertEqual(len(lines), 2)
        self.assertClean("\n".join(lines))
        self.assertNotIn("temperature_c", "\n".join(lines))

    def test_stream_error_codes_are_fixed_tokens(self) -> None:
        binding = iot_stream.Binding("SYN-S1", "S1", "HOME-001")
        auth = json.dumps({"scope": "device", "type": "x509"}).encode()
        event = _Event([READING.encode()], {iot_stream.DEVICE: b"SYN-S1", iot_stream.AUTH: auth})
        with self.assertRaises(StreamError) as raised:
            iot_stream.decode(event, {"SYN-S1": binding})  # type: ignore[arg-type]
        self.assertRegex(str(raised.exception), r"^[A-Z_]+$")

    def test_dry_run_sink_prints_identifiers_and_size_not_readings(self) -> None:
        body = b'{"label": "SYNTHETIC", "temperature_c": 21.7371, "humidity": 55.123}'
        out = io.StringIO()
        with redirect_stdout(out):
            asyncio.run(ls.StdoutSink().send("SYN-S1", "msg-1", body))
        text = out.getvalue()
        self.assertIn("DRY-RUN SYN-S1 msg-1", text)
        self.assertIn(f"bytes={len(body)}", text)
        for leaked in ("temperature_c", "21.7371", "55.123", "humidity"):
            self.assertNotIn(leaked, text)

    def test_simulator_failure_paths_print_fixed_codes_only(self) -> None:
        err = io.StringIO()

        def boom(env: object = None) -> list[str]:
            raise RuntimeError(f"{EMAIL} {READING} {PROMPT}")

        with patch.object(ls, "store_home_ids", boom), redirect_stderr(err):
            code = ls.main(["--once"], env={})
        self.assertEqual(code, 4)
        self.assertIn("SIM_FAILED", err.getvalue())
        self.assertClean(err.getvalue())


if __name__ == "__main__":
    unittest.main()
