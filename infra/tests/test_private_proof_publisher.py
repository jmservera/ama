"""Compiled security boundary for the explicitly temporary issue360 publisher."""

import json
import shutil
import subprocess
import unittest
from copy import deepcopy
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
        self.assertEqual(guard["name"], "[format('{0}-guard', variables('stem'))]")
        properties = guard["properties"]
        self.assertEqual(properties["mode"], "Incremental")
        self.assertEqual(properties["parameters"]["approvedScope"], (
            "[if(and(equals(resourceGroup().name, 'ama'), "
            "equals(toLower(resourceGroup().id), toLower(parameters('expectedResourceGroupId')))), "
            "createObject('value', resourceGroup().id), createObject('value', ''))]"
        ))
        self.assertEqual(properties["template"]["parameters"]["approvedScope"]["type"], "string")
        self.assertEqual(properties["template"]["parameters"]["approvedScope"]["minLength"], 1)
        self.assertEqual(properties["template"]["resources"], [])
        for kind in ("Microsoft.Network/networkSecurityGroups",
                     "Microsoft.Network/publicIPAddresses"):
            self.assertEqual(self.resource(kind)["dependsOn"], [
                "[resourceId('Microsoft.Resources/deployments', format('{0}-guard', variables('stem')))]",
            ])

    def test_network_is_separate_no_inbound_and_explicit_outbound(self):
        subnet = self.resource("Microsoft.Network/virtualNetworks/subnets")
        nsg_id = "[resourceId('Microsoft.Network/networkSecurityGroups', format('{0}-nsg', variables('stem')))]"
        subnet_id = (
            "[resourceId('Microsoft.Network/virtualNetworks/subnets', "
            "'vnet-cutover-test', format('{0}-subnet', variables('stem')))]"
        )
        public_ip_id = "[resourceId('Microsoft.Network/publicIPAddresses', format('{0}-ip', variables('stem')))]"
        self.assertEqual(subnet["name"], (
            "[format('{0}/{1}', 'vnet-cutover-test', format('{0}-subnet', variables('stem')))]"
        ))
        self.assertEqual(
            self.resource("Microsoft.Network/networkSecurityGroups")["name"],
            "[format('{0}-nsg', variables('stem'))]",
        )
        self.assertEqual(subnet["properties"]["networkSecurityGroup"], {"id": nsg_id})
        self.assertEqual(subnet["dependsOn"], [nsg_id])
        self.assertEqual(subnet["properties"]["addressPrefix"], "10.40.8.0/28")
        self.assertFalse(subnet["properties"]["defaultOutboundAccess"])
        rules = self.resource("Microsoft.Network/networkSecurityGroups")["properties"]["securityRules"]
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["properties"], {
            "priority": 100, "direction": "Inbound", "access": "Deny", "protocol": "*",
            "sourceAddressPrefix": "*", "sourcePortRange": "*",
            "destinationAddressPrefix": "*", "destinationPortRange": "*",
        })
        nic_resource = self.resource("Microsoft.Network/networkInterfaces")
        self.assertEqual(nic_resource["name"], "[format('{0}-nic', variables('stem'))]")
        self.assertCountEqual(nic_resource["dependsOn"], [public_ip_id, subnet_id])
        nic = nic_resource["properties"]
        self.assertFalse(nic["enableIPForwarding"])
        self.assertEqual(len(nic["ipConfigurations"]), 1)
        configuration = nic["ipConfigurations"][0]["properties"]
        self.assertEqual(configuration["subnet"], {"id": subnet_id})
        self.assertEqual(configuration["publicIPAddress"], {"id": public_ip_id})
        public_ip = self.resource("Microsoft.Network/publicIPAddresses")
        self.assertEqual(public_ip["name"], "[format('{0}-ip', variables('stem'))]")
        self.assertEqual(public_ip["sku"]["name"], "Standard")
        self.assertEqual(public_ip["properties"]["publicIPAllocationMethod"], "Static")

    def test_vm_minimal_pinned_no_password_or_external_identity(self):
        vm = self.resource("Microsoft.Compute/virtualMachines")
        nic_id = "[resourceId('Microsoft.Network/networkInterfaces', format('{0}-nic', variables('stem')))]"
        self.assertEqual(vm["dependsOn"], [nic_id])
        self.assertEqual(vm["properties"]["networkProfile"]["networkInterfaces"], [
            {"id": nic_id, "properties": {"deleteOption": "Detach"}},
        ])
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

    def test_detached_wrong_target_and_unguarded_compiled_variants_fail(self):
        guard = "Microsoft.Resources/deployments"
        nsg = "Microsoft.Network/networkSecurityGroups"
        subnet = "Microsoft.Network/virtualNetworks/subnets"
        nic = "Microsoft.Network/networkInterfaces"
        vm = "Microsoft.Compute/virtualMachines"
        guard_test = "test_exact_rg_guard_is_a_dependency"
        network_test = "test_network_is_separate_no_inbound_and_explicit_outbound"
        vm_test = "test_vm_minimal_pinned_no_password_or_external_identity"
        expression = self.resource(guard)["properties"]["parameters"]["approvedScope"]
        mutations = [
            ("detached-nsg", network_test, subnet, ("properties", "networkSecurityGroup"), {}),
            ("wrong-nsg", network_test, subnet, ("properties", "networkSecurityGroup", "id"), "[resourceId('Microsoft.Network/networkSecurityGroups', 'other')]"),
            ("wrong-vnet-child", network_test, subnet, ("name",), "[format('{0}/{1}', 'other-vnet', format('{0}-subnet', variables('stem')))]"),
            ("wrong-nic-subnet", network_test, nic, ("properties", "ipConfigurations", 0, "properties", "subnet", "id"), "[resourceId('Microsoft.Network/virtualNetworks/subnets', 'other-vnet', 'other-subnet')]"),
            ("wrong-nic-public-ip", network_test, nic, ("properties", "ipConfigurations", 0, "properties", "publicIPAddress", "id"), "[resourceId('Microsoft.Network/publicIPAddresses', 'other')]"),
            ("wrong-vm-nic", vm_test, vm, ("properties", "networkProfile", "networkInterfaces", 0, "id"), "[resourceId('Microsoft.Network/networkInterfaces', 'other')]"),
            ("unrelated-nsg-dependency", guard_test, nsg, ("dependsOn",), ["[resourceId('Microsoft.Network/publicIPAddresses', 'other')]"]),
            ("unrelated-public-ip-dependency", guard_test, "Microsoft.Network/publicIPAddresses", ("dependsOn",), ["[resourceId('Microsoft.Network/networkSecurityGroups', 'other')]"]),
            ("missing-subnet-dependency", network_test, subnet, ("dependsOn",), []),
            ("missing-nic-dependencies", network_test, nic, ("dependsOn",), []),
            ("missing-vm-dependency", vm_test, vm, ("dependsOn",), []),
            ("accept-refused-scope", guard_test, guard, ("properties", "parameters", "approvedScope"), expression.replace("createObject('value', '')", "createObject('value', resourceGroup().id)")),
            ("wrong-approved-scope", guard_test, guard, ("properties", "parameters", "approvedScope"), expression.replace("createObject('value', resourceGroup().id)", "createObject('value', 'other')")),
            ("empty-scope-allowed", guard_test, guard, ("properties", "template", "parameters", "approvedScope", "minLength"), 0),
            ("missing-name-check", guard_test, guard, ("properties", "parameters", "approvedScope"), expression.replace("equals(resourceGroup().name, 'ama')", "true()")),
            ("missing-id-check", guard_test, guard, ("properties", "parameters", "approvedScope"), expression.replace("equals(toLower(resourceGroup().id), toLower(parameters('expectedResourceGroupId')))", "true()")),
        ]
        for name, test, kind, path, value in mutations:
            with self.subTest(mutation=name):
                probe = type(self)(test)
                probe.template = deepcopy(self.template)
                probe.resources = probe.template["resources"]
                target = probe.resource(kind)
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(AssertionError):
                    getattr(probe, test)()


if __name__ == "__main__":
    unittest.main()
