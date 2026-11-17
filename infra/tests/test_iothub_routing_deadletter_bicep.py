"""IoT Hub routing, consumer group and fallback quarantine contract (issue 145)."""

import shutil
import unittest

from test_bicep_policy import compile_bicep

HUB = "Microsoft.Devices/IotHubs"
HUB_GROUP = "Microsoft.Devices/IotHubs/eventHubEndpoints/ConsumerGroups"
TELEMETRY_GROUP = "Microsoft.EventHub/namespaces/eventhubs/consumergroups"


@unittest.skipUnless(shutil.which("az"), "Azure CLI with Bicep is needed to compile the templates")
class IotHubRoutingDeadLetterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = compile_bicep("modules/iothub.bicep")
        resources = cls.template["resources"]
        cls.hub = next(r for r in resources if r["type"] == HUB)
        cls.routing = cls.hub["properties"]["routing"]

    def of_type(self, kind: str) -> list[dict]:
        return [r for r in self.template["resources"] if r["type"] == kind]

    def test_dedicated_consumer_group_avoids_default_and_builtin_endpoint(self) -> None:
        groups = self.of_type(TELEMETRY_GROUP)
        self.assertEqual(len(groups), 1)
        name = self.template["variables"]["consumerGroupName"]
        self.assertEqual(name, "api-consumer")
        self.assertNotEqual(name.lower(), "$default")
        self.assertIn("consumerGroupName", groups[0]["name"])
        self.assertEqual(
            self.template["outputs"]["consumerGroup"]["value"], "[variables('consumerGroupName')]"
        )
        self.assertEqual(self.of_type(HUB_GROUP), [])

    def test_fallback_route_is_explicitly_disabled_so_no_builtin_retention(self) -> None:
        fallback = self.routing["fallbackRoute"]
        self.assertFalse(fallback["isEnabled"])
        self.assertEqual(fallback["source"], "DeviceMessages")
        self.assertEqual(fallback["endpointNames"], ["events"])
        self.assertEqual(
            self.hub["properties"]["eventHubEndpoints"]["events"]["retentionTimeInDays"],
            "[parameters('retentionDays')]",
        )

    def test_explicit_route_is_gated_and_identity_based(self) -> None:
        routes = self.routing["routes"]
        self.assertIn("routingReady", routes)
        self.assertIn("all-device-messages", routes)
        self.assertIn("DeviceMessages", routes)
        endpoints = self.routing["endpoints"]["eventHubs"]
        self.assertIn("identityBased", endpoints)
        self.assertNotIn("connectionString", endpoints)
        self.assertNotIn("connectionString", str(self.routing))

    def test_shared_key_over_privilege_is_disabled_where_identity_applies(self) -> None:
        props = self.hub["properties"]
        self.assertTrue(props["disableLocalAuth"])
        self.assertTrue(props["disableModuleSAS"])
        self.assertEqual(self.hub["identity"]["type"], "SystemAssigned")
        for namespace in self.of_type("Microsoft.EventHub/namespaces"):
            self.assertTrue(namespace["properties"]["disableLocalAuth"])


if __name__ == "__main__":
    unittest.main()
