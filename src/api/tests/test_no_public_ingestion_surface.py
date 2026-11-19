"""AC-066 'no public unauthenticated ingestion endpoint' (#110): HTTP modules stay consumer-free."""

import ast
import re
import unittest
from pathlib import Path

API_DIR = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api"
HTTP_MODULES = (
    "server.py",
    "workbench.py",
    "nomination_routes.py",
    "resident_demo/app.py",
    "resident_preview/app.py",
)
CONSUMER_MODULES = (
    "zava_forward.api.iot_stream",
    "zava_forward.api.sensor_ingestion",
    "zava_forward.api.live_receiver",
    "zava_forward.core.sensor_consumer",
)
CONSUMER_ROOTS = ("azure.eventhub", "azure.iot")
INGEST_PATH = re.compile(r"^/[\w./-]*(ingest|telemetry|readings|iothub|eventhub)", re.IGNORECASE)


def imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def violations(source: str) -> list[str]:
    tree = ast.parse(source)
    found = [
        name
        for name in sorted(imported_names(tree))
        if name in CONSUMER_MODULES or name.startswith(CONSUMER_ROOTS)
    ]
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if INGEST_PATH.match(node.value):
                found.append(node.value)
    return found


class NoPublicIngestionSurface(unittest.TestCase):
    def test_http_modules_exist_and_are_clean(self) -> None:
        for name in HTTP_MODULES:
            path = API_DIR / name
            self.assertTrue(path.is_file(), name)
            self.assertEqual(violations(path.read_text(encoding="utf-8")), [], name)

    def test_guard_detects_consumer_import_and_ingestion_path(self) -> None:
        self.assertEqual(
            violations("from zava_forward.api.sensor_ingestion import SensorIngestion"),
            ["zava_forward.api.sensor_ingestion"],
        )
        self.assertEqual(violations("import azure.eventhub.aio"), ["azure.eventhub.aio"])
        self.assertEqual(violations("ROUTE = '/api/sensors/readings'"), ["/api/sensors/readings"])
        self.assertEqual(violations("from zava_forward.core import sensor_scenarios"), [])


if __name__ == "__main__":
    unittest.main()
