"""Diagnostic logs exclude personal data, raw readings and chat content (issue 146)."""

import io
import logging
import unittest
from pathlib import Path

from zava_forward.core import diagnostic_logging as dl

SRC = Path(__file__).resolve().parents[2]
ENTRYPOINTS = (
    "api/src/zava_forward/api/server.py",
    "api/src/zava_forward/api/live_simulator.py",
    "api/src/zava_forward/api/live_receiver.py",
    "api/src/zava_forward/api/resident_demo/__main__.py",
    "agents/src/zava_forward/agents/worker.py",
    "importer/src/zava_forward/importer/__main__.py",
)
CANARIES = (
    "resident@example.org",
    "CHAT-CANARY-my boiler is leaking at number 4",
    "READING-CANARY-21.5C",
    "192.168.4.20",
    "eyJhbGciOiJIUzI1.payload.sig",
)


class RedactionTests(unittest.TestCase):
    def setUp(self) -> None:
        dl.install_diagnostic_redaction(console=False)
        self.addCleanup(dl.uninstall_diagnostic_redaction)
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.logger = logging.getLogger("zava_forward.test.diagnostic")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.addCleanup(self.logger.removeHandler, self.handler)

    def output(self) -> str:
        return self.stream.getvalue()

    def test_free_text_args_extras_and_exceptions_are_dropped(self) -> None:
        try:
            raise RuntimeError(CANARIES[1])
        except RuntimeError:
            self.logger.exception(
                "failed for %s with %s",
                CANARIES[0],
                {"chat": CANARIES[1]},
                extra={"reading": CANARIES[2], "ip": CANARIES[3]},
                stack_info=True,
            )
        self.logger.warning("sent %s", CANARIES[1])
        self.logger.error("body=%s ip %s token %s", CANARIES[2], CANARIES[3], CANARIES[4])
        self.logger.error(f"unformatted {CANARIES[0]} {CANARIES[3]} {CANARIES[4]}")
        out = self.output()
        for canary in CANARIES:
            self.assertNotIn(canary, out)
        self.assertNotIn("Traceback", out)
        self.assertIn("exc=RuntimeError", out)
        self.assertIn("body=<redacted>", out)

    def test_extra_fields_never_reach_the_record(self) -> None:
        records: list[logging.LogRecord] = []

        class Capture(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                records.append(record)

        self.logger.addHandler(Capture())
        self.logger.info("ok", extra={"chat": CANARIES[1]})
        self.assertFalse(hasattr(records[0], "chat"))

    def test_hidden_temp_file_name_survives_for_cleanup(self) -> None:
        self.logger.warning("temporary file %s was not removed", ".ranking-ab12.tmp")
        self.assertIn(".ranking-ab12.tmp", self.output())

    def test_safe_operational_fields_survive(self) -> None:
        self.logger.warning(
            "http-error %s %s status=%s exc=%s at=%s",
            "GET",
            "/api/me?token=tok-SECRET",
            500,
            "RuntimeError",
            "server.py:1390",
        )
        line = self.output()
        self.assertIn("http-error GET /api/me status=500 exc=RuntimeError at=server.py:1390", line)
        self.assertNotIn("tok-SECRET", line)

    def test_install_is_idempotent_and_failure_withholds(self) -> None:
        dl.install_diagnostic_redaction(console=False)
        dl.install_diagnostic_redaction(console=False)

        class Hostile(dict):  # type: ignore[type-arg]
            def items(self):  # type: ignore[no-untyped-def]
                raise RuntimeError("boom")

        self.logger.warning("%(a)s", Hostile(a=CANARIES[1]))
        self.assertIn(dl.WITHHELD, self.output())
        self.assertNotIn(CANARIES[1], self.output())

    def test_uninstall_restores_original(self) -> None:
        dl.uninstall_diagnostic_redaction()
        self.logger.warning("raw %s", CANARIES[0])
        self.assertIn(CANARIES[0], self.output())

    def test_console_install_adds_handler_and_meter_level(self) -> None:
        root = logging.getLogger()
        saved, level = root.handlers[:], root.level
        root.handlers = []

        def restore() -> None:
            root.handlers = saved
            root.setLevel(level)

        self.addCleanup(restore)
        dl.install_diagnostic_redaction()
        self.assertTrue(root.handlers)
        self.assertEqual(logging.getLogger(dl.METER_LOGGER).level, logging.INFO)


class EntrypointTests(unittest.TestCase):
    def test_every_service_entrypoint_installs_redaction(self) -> None:
        for path in ENTRYPOINTS:
            with self.subTest(path=path):
                text = (SRC / path).read_text(encoding="utf-8")
                self.assertIn("install_diagnostic_redaction()", text)


if __name__ == "__main__":
    unittest.main()
