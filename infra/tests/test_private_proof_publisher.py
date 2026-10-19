"""Compiled security boundary for the explicitly temporary issue360 publisher."""

import json
import shutil
import subprocess
import unittest
from copy import deepcopy
from ipaddress import ip_address, ip_network
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
        inbound = [rule for rule in rules if rule["properties"]["direction"] == "Inbound"]
        self.assertEqual(len(inbound), 1)
        self.assertEqual(inbound[0]["properties"], {
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

    def test_outbound_contract_has_only_private_acr_and_platform_exceptions(self):
        rules = self.resource("Microsoft.Network/networkSecurityGroups")["properties"]["securityRules"]
        expected = [
            ("allow-private-acr-https", 100, "Allow", "Tcp",
             {"destinationAddressPrefixes": ["10.40.4.20/32", "10.40.4.21/32"]},
             {"destinationPortRange": "443"}),
            ("allow-platform-dns-tcp", 110, "Allow", "Tcp",
             {"destinationAddressPrefix": "AzurePlatformDNS"}, {"destinationPortRange": "53"}),
            ("allow-platform-dns-udp", 120, "Allow", "Udp",
             {"destinationAddressPrefix": "AzurePlatformDNS"}, {"destinationPortRange": "53"}),
            ("allow-wireserver-agent", 130, "Allow", "Tcp",
             {"destinationAddressPrefix": "168.63.129.16/32"},
             {"destinationPortRanges": ["80", "32526"]}),
            ("allow-platform-imds-http", 140, "Allow", "Tcp",
             {"destinationAddressPrefix": "AzurePlatformIMDS"}, {"destinationPortRange": "80"}),
            ("deny-other-platform-dns", 150, "Deny", "*",
             {"destinationAddressPrefix": "AzurePlatformDNS"}, {"destinationPortRange": "*"}),
            ("deny-other-platform-imds", 160, "Deny", "*",
             {"destinationAddressPrefix": "AzurePlatformIMDS"}, {"destinationPortRange": "*"}),
            ("deny-all-outbound", 200, "Deny", "*",
             {"destinationAddressPrefix": "*"}, {"destinationPortRange": "*"}),
        ]
        outbound = {rule["name"]: rule["properties"] for rule in rules
                    if rule["properties"]["direction"] == "Outbound"}
        self.assertEqual(len(rules), 9)
        self.assertCountEqual(outbound, [row[0] for row in expected])
        for name, priority, access, protocol, destination, ports in expected:
            with self.subTest(rule=name):
                self.assertEqual(outbound[name], {
                    "priority": priority, "direction": "Outbound", "access": access,
                    "protocol": protocol,
                    "sourceAddressPrefix": "10.40.8.0/28" if access == "Allow" else "*",
                    "sourcePortRange": "*", **destination, **ports,
                })

    def outbound_decision(self, destination, port, protocol="Tcp", source="10.40.8.4"):
        """Bounded first-match model, not an Azure platform/NSG emulator."""
        rules = [rule["properties"] for rule in
                 self.resource("Microsoft.Network/networkSecurityGroups")["properties"]["securityRules"]
                 if rule["properties"]["direction"] == "Outbound"]
        for priority, destination_prefix, access in (
            (65000, "VirtualNetwork", "Allow"), (65001, "Internet", "Allow"),
            (65500, "*", "Deny"),
        ):
            rules.append({
                "priority": priority, "destinationAddressPrefix": destination_prefix,
                "access": access, "protocol": "*", "sourceAddressPrefix": "*",
                "destinationPortRange": "*",
            })

        def matches(prefix, address):
            if prefix == "*":
                return True
            if prefix == "Internet":
                return ip_address(address).is_global
            tags = {"AzurePlatformDNS": "168.63.129.16/32",
                    "AzurePlatformIMDS": "169.254.169.254/32",
                    "VirtualNetwork": "10.40.0.0/16"}
            return ip_address(address) in ip_network(tags.get(prefix, prefix))

        for rule in sorted(rules, key=lambda rule: rule["priority"]):
            destinations = rule.get("destinationAddressPrefixes", [rule.get("destinationAddressPrefix")])
            ports = rule.get("destinationPortRanges", [rule.get("destinationPortRange")])
            if (rule["protocol"] in ("*", protocol)
                    and matches(rule["sourceAddressPrefix"], source)
                    and any(matches(prefix, destination) for prefix in destinations)
                    and any(value in ("*", str(port)) for value in ports)):
                return rule["access"]
        self.fail("Missing terminal outbound policy")

    def test_outbound_first_match_denies_public_packages_and_other_private_services(self):
        allowed = [
            ("10.40.4.20", 443, "Tcp"), ("10.40.4.21", 443, "Tcp"),
            ("168.63.129.16", 53, "Tcp"), ("168.63.129.16", 53, "Udp"),
            ("168.63.129.16", 80, "Tcp"), ("168.63.129.16", 32526, "Tcp"),
            ("169.254.169.254", 80, "Tcp"),
        ]
        denied = [
            ("1.1.1.1", 443, "Tcp"), ("1.1.1.1", 80, "Tcp"),
            ("1.1.1.1", 53, "Udp"), ("1.1.1.1", 22, "Tcp"),
            ("1.1.1.1", 443, "Udp"), ("20.60.1.1", 443, "Tcp"),
            ("10.40.4.25", 1433, "Tcp"), ("10.40.4.22", 443, "Tcp"),
            ("10.40.8.5", 22, "Tcp"), ("10.40.4.20", 80, "Tcp"),
            ("10.40.4.21", 443, "Udp"), ("10.40.4.21", 444, "Tcp"),
            ("168.63.129.16", 443, "Tcp"), ("168.63.129.16", 54, "Udp"),
            ("169.254.169.254", 443, "Tcp"), ("169.254.169.254", 80, "Udp"),
            ("2001:4860:4860::8888", 443, "Tcp"),
        ]
        for expected, cases in (("Allow", allowed), ("Deny", denied)):
            for destination, port, protocol in cases:
                with self.subTest(destination=destination, port=port, protocol=protocol):
                    self.assertEqual(self.outbound_decision(destination, port, protocol), expected)
        self.assertEqual(self.outbound_decision("10.40.4.20", 443, source="10.40.6.4"), "Deny")

    def test_weakened_compiled_outbound_variants_fail(self):
        mutations = [
            ("missing-terminal-deny", "deny-all-outbound", None, None),
            ("terminal-deny-after-defaults", "deny-all-outbound", "priority", 65500),
            ("terminal-allow", "deny-all-outbound", "access", "Allow"),
            ("terminal-tcp-only", "deny-all-outbound", "protocol", "Tcp"),
            ("terminal-internet-only", "deny-all-outbound", "destinationAddressPrefix", "Internet"),
            ("terminal-wrong-source", "deny-all-outbound", "sourceAddressPrefix", "10.40.6.0/23"),
            ("broad-registry-destination", "allow-private-acr-https", "destinationAddressPrefixes", ["0.0.0.0/0"]),
            ("whole-private-subnet", "allow-private-acr-https", "destinationAddressPrefixes", ["10.40.4.0/24"]),
            ("wildcard-registry-port", "allow-private-acr-https", "destinationPortRange", "*"),
            ("wildcard-registry-protocol", "allow-private-acr-https", "protocol", "*"),
            ("arbitrary-dns", "allow-platform-dns-udp", "destinationAddressPrefix", "*"),
            ("arbitrary-agent", "allow-wireserver-agent", "destinationAddressPrefix", "*"),
            ("arbitrary-imds", "allow-platform-imds-http", "destinationAddressPrefix", "*"),
            ("missing-platform-dns-deny", "deny-other-platform-dns", None, None),
            ("missing-platform-imds-deny", "deny-other-platform-imds", None, None),
            ("missing-registry-allow", "allow-private-acr-https", None, None),
            ("remove-all-outbound", None, None, None),
            ("insert-internet-allow", None, None, None),
        ]
        for name, rule_name, key, value in mutations:
            with self.subTest(mutation=name):
                probe = type(self)("test_outbound_contract_has_only_private_acr_and_platform_exceptions")
                probe.template = deepcopy(self.template)
                probe.resources = probe.template["resources"]
                rules = probe.resource("Microsoft.Network/networkSecurityGroups")["properties"]["securityRules"]
                if name == "remove-all-outbound":
                    rules[:] = [rule for rule in rules if rule["properties"]["direction"] != "Outbound"]
                elif name == "insert-internet-allow":
                    rule = deepcopy(next(rule for rule in rules if rule["name"] == "deny-all-outbound"))
                    rule["name"] = "unsafe-internet"
                    rule["properties"].update(priority=190, access="Allow", destinationAddressPrefix="Internet")
                    rules.append(rule)
                else:
                    target = next(rule for rule in rules if rule["name"] == rule_name)
                    if key is None:
                        rules.remove(target)
                    else:
                        target["properties"][key] = value
                with self.assertRaises(AssertionError):
                    probe.test_outbound_contract_has_only_private_acr_and_platform_exceptions()

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
