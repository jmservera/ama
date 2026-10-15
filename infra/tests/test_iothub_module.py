"""Static guards on the IoT Hub Bicep module (issue 140)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = (ROOT / "modules" / "iothub.bicep").read_text(encoding="utf-8")
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")


class IotHubModuleTests(unittest.TestCase):
    def test_no_shared_keys_and_private_by_default(self) -> None:
        self.assertIn("disableLocalAuth: true", MODULE)
        self.assertIn("allowPublicNetworkAccess ? 'Enabled' : 'Disabled'", MODULE)
        self.assertNotIn("listKeys", MODULE)
        self.assertNotIn("ConnectionString", MODULE)

    def test_least_privilege_receiver_role_only(self) -> None:
        self.assertIn("a638d3c7-ab3a-418d-83e6-5f17a39d4fde", MODULE)
        self.assertNotIn("IoT Hub Data Contributor", MODULE)

    def test_diagnostics_exclude_device_telemetry(self) -> None:
        self.assertNotIn("category: 'DeviceTelemetry'", MODULE)
        self.assertIn("'to-log-analytics'", MODULE)

    def test_wired_in_main_with_region_neutral_defaults(self) -> None:
        self.assertIn("modules/iothub.bicep", MAIN)
        self.assertIn("param iotHubSku string = 'B1'", MAIN)
        self.assertIn("name: 'ResourceId'", MODULE)


if __name__ == "__main__":
    unittest.main()
