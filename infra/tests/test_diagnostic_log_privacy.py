"""Issue 146 criterion 4: Bicep diagnostic settings keep content-bearing logs out of Log Analytics."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r"resource\s+(\w+)\s+'Microsoft\.Insights/diagnosticSettings@[^']+'\s*=\s*\{(.*?)\n\}",
    re.DOTALL,
)
# Categories that carry device messages, request or response bodies, or query text.
CONTENT_CATEGORIES = {
    "Routes",
    "DeviceTelemetry",
    "D2CTwinOperations",
    "C2DCommands",
    "Connections",
    "AppTraces",
    "AppRequests",
    "AuditEvent",
    "RequestResponse",
    "Trace",
    "SQLInsights",
    "QueryStoreRuntimeStatistics",
    "QueryStoreWaitStatistics",
}
ALLOWED_SINKS = {"workspaceId"}
FORBIDDEN_SINKS = (
    "storageAccountId",
    "eventHubAuthorizationRuleId",
    "marketplacePartnerId",
)


def _settings() -> list[tuple[str, str, str]]:
    found = []
    for path in sorted(INFRA.rglob("*.bicep")):
        text = path.read_text(encoding="utf-8")
        for name, body in BLOCK.findall(text):
            found.append((path.relative_to(INFRA).as_posix(), name, body))
    return found


class DiagnosticSettingsPrivacyTests(unittest.TestCase):
    def test_diagnostic_settings_are_discovered(self) -> None:
        names = {path for path, _, _ in _settings()}
        for module in (
            "modules/iothub.bicep",
            "modules/containerapps.bicep",
            "iot-hub-live.bicep",
        ):
            self.assertIn(module, names)

    def test_every_setting_targets_only_the_log_analytics_workspace(self) -> None:
        for path, name, body in _settings():
            with self.subTest(setting=f"{path}:{name}"):
                self.assertIn("workspaceId:", body)
                for sink in FORBIDDEN_SINKS:
                    self.assertNotIn(sink, body)

    def test_no_enabled_category_carries_message_or_query_content(self) -> None:
        for path, name, body in _settings():
            for category, enabled in re.findall(
                r"category:\s*'(\w+)',\s*enabled:\s*(true|false)", body
            ):
                with self.subTest(setting=f"{path}:{name}", category=category):
                    if category in CONTENT_CATEGORIES:
                        self.assertEqual(enabled, "false")

    def test_iot_hub_diagnostics_keep_device_message_logs_disabled(self) -> None:
        for path, name, body in _settings():
            if not path.endswith(("iothub.bicep", "iot-hub-live.bicep")):
                continue
            with self.subTest(setting=f"{path}:{name}"):
                self.assertIn("{ categoryGroup: 'allLogs', enabled: false }", body)
                self.assertNotIn("categoryGroup: 'allLogs', enabled: true", body)

    def test_storage_and_token_stores_log_audit_group_only(self) -> None:
        for path in ("modules/storage.bicep", "modules/authTokenStore.bicep"):
            text = (INFRA / path).read_text(encoding="utf-8")
            for _, body in BLOCK.findall(text):
                with self.subTest(path=path):
                    self.assertIn("categoryGroup: 'audit'", body)
                    self.assertNotIn("allLogs", body)
                    self.assertNotIn("StorageRead", body)
                    self.assertNotIn("StorageWrite", body)

    def test_sql_server_diagnostics_are_audit_events_only(self) -> None:
        text = (INFRA / "modules" / "sql.bicep").read_text(encoding="utf-8")
        server = next(
            body for name, body in BLOCK.findall(text) if name == "serverDiagnostics"
        )
        self.assertEqual(
            re.findall(r"category:\s*'(\w+)'", server),
            ["SQLSecurityAuditEvents"],
        )

    def test_edge_logs_are_access_and_waf_only(self) -> None:
        text = (INFRA / "modules" / "edge.bicep").read_text(encoding="utf-8")
        body = next(b for n, b in BLOCK.findall(text) if n == "diagnostics")
        self.assertEqual(
            sorted(re.findall(r"category:\s*'(\w+)'", body)),
            ["FrontDoorAccessLog", "FrontDoorWebApplicationFirewallLog"],
        )


if __name__ == "__main__":
    unittest.main()
