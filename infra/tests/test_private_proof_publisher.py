"""Compiled security boundary for the explicitly temporary issue360 publisher."""

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PrivatePublisherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bicep = shutil.which("bicep")
        command = [bicep, "build"] if bicep else ["az", "bicep", "build", "--file"]
        result = subprocess.run(
            [*command, str(ROOT / "private-proof-publisher.bicep"), "--stdout"],
            capture_output=True, text=True, check=True,
        )
        cls.template = json.loads(result.stdout)
        cls.resources = cls.template["resources"]

    def resource(self, kind):
        matches = [r for r in self.resources if r["type"] == kind]
        self.assertEqual(len(matches), 1)
        return matches[0]

    def test_exact_new_resource_types_and_no_backing_or_iam_write(self):
        self.assertCountEqual(
            [r["type"] for r in self.resources],
            ["Microsoft.Resources/deployments", "Microsoft.Network/networkSecurityGroups",
             "Microsoft.Network/virtualNetworks/subnets", "Microsoft.Network/publicIPAddresses",
             "Microsoft.Network/networkInterfaces", "Microsoft.Compute/virtualMachines"],
        )
        self.assertEqual(self.template["variables"]["stem"], "issue360-publisher-20261019")

    def test_exact_rg_guard_is_a_dependency(self):
        guard = self.resource("Microsoft.Resources/deployments")
        expression = json.dumps(guard["properties"]["parameters"]["approvedScope"])
        self.assertIn("equals(resourceGroup().name, 'ama')", expression)
        self.assertIn("toLower(resourceGroup().id)", expression)
        self.assertIn("toLower(parameters('expectedResourceGroupId'))", expression)
        for kind in ("Microsoft.Network/networkSecurityGroups",
                     "Microsoft.Network/publicIPAddresses"):
            self.assertTrue(self.resource(kind)["dependsOn"])

    def test_network_is_separate_no_inbound_and_explicit_outbound(self):
        subnet = self.resource("Microsoft.Network/virtualNetworks/subnets")
        self.assertEqual(subnet["properties"]["addressPrefix"], "10.40.8.0/28")
        self.assertFalse(subnet["properties"]["defaultOutboundAccess"])
        rules = self.resource("Microsoft.Network/networkSecurityGroups")["properties"]["securityRules"]
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["properties"], {
            "priority": 100, "direction": "Inbound", "access": "Deny", "protocol": "*",
            "sourceAddressPrefix": "*", "sourcePortRange": "*",
            "destinationAddressPrefix": "*", "destinationPortRange": "*",
        })
        nic = self.resource("Microsoft.Network/networkInterfaces")["properties"]
        self.assertFalse(nic["enableIPForwarding"])
        self.assertEqual(len(nic["ipConfigurations"]), 1)
        self.assertIn("publicIPAddress", nic["ipConfigurations"][0]["properties"])
        self.assertEqual(self.resource("Microsoft.Network/publicIPAddresses")["sku"]["name"], "Standard")

    def test_vm_minimal_pinned_no_password_or_external_identity(self):
        vm = self.resource("Microsoft.Compute/virtualMachines")
        self.assertEqual(vm["identity"], {"type": "SystemAssigned"})
        properties = vm["properties"]
        self.assertEqual(properties["hardwareProfile"]["vmSize"], "Standard_D2as_v5")
        storage = properties["storageProfile"]
        self.assertEqual(storage["imageReference"]["version"], "22.04.202610170")
        self.assertEqual(storage["osDisk"]["managedDisk"]["storageAccountType"], "StandardSSD_LRS")
        self.assertEqual(storage["osDisk"]["diskSizeGB"], 32)
        self.assertEqual(storage["osDisk"]["deleteOption"], "Delete")
        linux = properties["osProfile"]["linuxConfiguration"]
        self.assertTrue(linux["disablePasswordAuthentication"])
        self.assertNotIn("adminPassword", properties["osProfile"])
        self.assertEqual(linux["ssh"]["publicKeys"][0]["keyData"], "[parameters('sshPublicKey')]")
        self.assertFalse(properties["diagnosticsProfile"]["bootDiagnostics"]["enabled"])
        self.assertIn("zava-forward-expires", self.template["variables"]["ownership"])


if __name__ == "__main__":
    unittest.main()
