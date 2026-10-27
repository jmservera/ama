"""Compiled IoT transport contracts and mutation guards (issue 140)."""

import os
import shutil
import unittest
from copy import deepcopy
from types import SimpleNamespace

from test_bicep_policy import (
    compile_bicep,
    evaluate,
    module,
    resource,
    resources,
    unguarded_resources,
)

HUB = "Microsoft.Devices/IotHubs"
NAMESPACE = "Microsoft.EventHub/namespaces"
EVENT_HUB = f"{NAMESPACE}/eventhubs"
RECEIVER = "a638d3c7-ab3a-418d-83e6-5f17a39d4fde"
SENDER = "2b629674-e913-4c01-ae53-ef4638d8f975"


@unittest.skipUnless(
    shutil.which("az") or os.environ.get("REQUIRE_AZ_BICEP") == "1",
    "Azure CLI with Bicep is needed to compile the templates",
)
class IotHubModuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = compile_bicep("modules/iothub.bicep")
        cls.main = compile_bicep("main.bicep")

    def values(self, template=None, **overrides):
        source = self.template if template is None else template
        defaults = {
            key: spec["defaultValue"]
            for key, spec in source["parameters"].items()
            if "defaultValue" in spec
        }
        return {**defaults, "name": "fixture", "location": "uksouth", **overrides}

    def assert_routing(self, template) -> None:
        hub = resource(template, HUB)
        self.assertEqual(hub["identity"], {"type": "SystemAssigned"})
        self.assertFalse(template["parameters"]["routingReady"]["defaultValue"])
        self.assertFalse(
            any(
                "Microsoft.Authorization/roleAssignments" in dep for dep in hub.get("dependsOn", [])
            )
        )
        context = {
            "reference": lambda *args: SimpleNamespace(
                serviceBusEndpoint="https://eh-fixture.servicebus.windows.net/"
            ),
            "subscription": lambda: SimpleNamespace(subscriptionId="synthetic-subscription"),
        }
        for ready in (False, True):
            routing = evaluate(
                hub["properties"]["routing"],
                self.values(template, routingReady=ready),
                template["variables"],
                context,
            )
            self.assertFalse(routing["fallbackRoute"]["isEnabled"])
            endpoints = routing["endpoints"]["eventHubs"]
            routes = routing["routes"]
            self.assertEqual(len(endpoints), int(ready))
            self.assertEqual(len(routes), int(ready))
            if ready:
                self.assertEqual(
                    endpoints[0],
                    {
                        "name": "api-telemetry",
                        "authenticationType": "identityBased",
                        "endpointUri": "sb://eh-fixture.servicebus.windows.net/",
                        "entityPath": "sensor-readings",
                        "resourceGroup": "ama",
                        "subscriptionId": "synthetic-subscription",
                        "identity": {},
                    },
                )
                self.assertEqual(
                    routes[0],
                    {
                        "name": "all-device-messages",
                        "source": "DeviceMessages",
                        "condition": "true",
                        "endpointNames": ["api-telemetry"],
                        "isEnabled": True,
                    },
                )
        roles = [
            item
            for item in resources(template)
            if item["type"] == "Microsoft.Authorization/roleAssignments"
        ]
        self.assertEqual(len(roles), 2)
        self.assertTrue(all("condition" not in item for item in roles))

    def test_bootstrap_and_activation_have_distinct_endpoint_registration(self) -> None:
        self.assert_routing(self.template)

    def test_mutations_reject_bootstrap_registration_fallback_and_wrong_auth(self) -> None:
        for change in ("bootstrap-endpoint", "fallback", "route-disabled", "auth", "sender-cycle"):
            with self.subTest(change=change):
                mutated = deepcopy(self.template)
                routing = resource(mutated, HUB)["properties"]["routing"]
                if change == "bootstrap-endpoint":
                    routing["endpoints"]["eventHubs"] = routing["endpoints"]["eventHubs"].replace(
                        "parameters('routingReady')", "true()"
                    )
                elif change == "fallback":
                    routing["fallbackRoute"]["isEnabled"] = True
                elif change == "route-disabled":
                    routing["routes"] = []
                elif change == "sender-cycle":
                    resource(mutated, HUB)["dependsOn"].append(
                        "[resourceId('Microsoft.Authorization/roleAssignments', 'sender')]"
                    )
                else:
                    routing["endpoints"]["eventHubs"] = routing["endpoints"]["eventHubs"].replace(
                        "identityBased", "keyBased"
                    )
                with self.assertRaises(AssertionError):
                    self.assert_routing(mutated)

    def assert_identity(self, template) -> None:
        receiver, sender = [
            item
            for item in template["resources"]
            if item["type"] == "Microsoft.Authorization/roleAssignments"
        ]
        self.assertEqual(
            receiver["scope"],
            "[resourceId('Microsoft.EventHub/namespaces/eventhubs', "
            "format('eh-{0}', parameters('name')), variables('telemetryName'))]",
        )
        self.assertEqual(
            receiver["properties"]["principalId"], "[parameters('consumerPrincipalId')]"
        )
        self.assertIn("eventHubsDataReceiver", receiver["properties"]["roleDefinitionId"])
        self.assertEqual(template["variables"]["eventHubsDataReceiver"], RECEIVER)
        self.assertEqual(
            sender["scope"],
            "[resourceId('Microsoft.EventHub/namespaces', format('eh-{0}', parameters('name')))]",
        )
        self.assertEqual(template["variables"]["eventHubsDataSender"], SENDER)
        self.assertIn("eventHubsDataSender", sender["properties"]["roleDefinitionId"])
        self.assertIn(".identity.principalId", sender["properties"]["principalId"])
        self.assertIn("Microsoft.Devices/IotHubs", sender["properties"]["principalId"])
        self.assertTrue(
            all(
                item["properties"]["principalType"] == "ServicePrincipal"
                for item in (receiver, sender)
            )
        )
        self.assertTrue(any("Microsoft.Devices/IotHubs" in dep for dep in sender["dependsOn"]))
        for kind in (HUB, NAMESPACE):
            self.assertTrue(resource(template, kind)["properties"]["disableLocalAuth"])
        self.assertFalse(resource(template, HUB)["properties"]["disableDeviceSAS"])
        self.assertTrue(resource(template, HUB)["properties"]["disableModuleSAS"])
        self.assertFalse(
            any(
                item["type"] == f"{HUB}/eventHubEndpoints/ConsumerGroups"
                for item in resources(template)
            )
        )

    def test_service_identity_and_device_credentials_are_distinct(self) -> None:
        self.assert_identity(self.template)

    def test_mutations_reject_wrong_receiver_scope_principal_and_auth(self) -> None:
        for change in ("scope", "principal", "role", "shared-auth"):
            with self.subTest(change=change):
                mutated = deepcopy(self.template)
                receiver = next(
                    item
                    for item in mutated["resources"]
                    if item["type"] == "Microsoft.Authorization/roleAssignments"
                )
                if change == "scope":
                    receiver["scope"] = (
                        "[format('Microsoft.Devices/IotHubs/{0}', parameters('name'))]"
                    )
                elif change == "principal":
                    receiver["properties"]["principalId"] = "wrong-principal"
                elif change == "role":
                    mutated["variables"]["eventHubsDataReceiver"] = SENDER
                else:
                    resource(mutated, NAMESPACE)["properties"]["disableLocalAuth"] = False
                with self.assertRaises(AssertionError):
                    self.assert_identity(mutated)

    def assert_private_network(self, template) -> None:
        namespace = resource(template, NAMESPACE)
        self.assertEqual(namespace["properties"]["publicNetworkAccess"], "Disabled")
        self.assertEqual(namespace["properties"]["minimumTlsVersion"], "1.2")
        rules = resource(template, f"{NAMESPACE}/networkRuleSets")["properties"]
        self.assertEqual(
            rules,
            {
                "publicNetworkAccess": "Disabled",
                "defaultAction": "Deny",
                "trustedServiceAccessEnabled": True,
                "ipRules": [],
                "virtualNetworkRules": [],
            },
        )
        hub_props = resource(template, HUB)["properties"]
        self.assertEqual(hub_props["minTlsVersion"], "1.2")
        for public in (False, True):
            self.assertEqual(
                evaluate(
                    hub_props["publicNetworkAccess"], {"allowPublicNetworkAccess": public}, {}
                ),
                "Enabled" if public else "Disabled",
            )
        endpoints = [
            item
            for item in template["resources"]
            if "groupId" in item.get("properties", {}).get("parameters", {})
        ]
        self.assertEqual(len(endpoints), 2)
        for endpoint in endpoints:
            self.assertNotIn("condition", endpoint)
            params = endpoint["properties"]["parameters"]
            self.assertEqual(params["subnetId"]["value"], "[parameters('peSubnetId')]")
            group = params["groupId"]["value"]
            zones = ["[parameters('zoneIds').iotHubEndpoint]"]
            if group == "iotHub":
                zones.insert(0, "[parameters('zoneIds').iotHub]")
                self.assertIn("Microsoft.Devices/IotHubs", params["targetResourceId"]["value"])
            else:
                self.assertEqual(group, "namespace")
                self.assertIn("Microsoft.EventHub/namespaces", params["targetResourceId"]["value"])
            self.assertEqual(params["dnsZoneIds"]["value"], zones)

    def test_private_endpoints_and_trusted_egress_exception(self) -> None:
        self.assert_private_network(self.template)

    def test_mutations_reject_public_namespace_and_missing_endpoint_dns(self) -> None:
        for change in ("public", "allow", "no-trust", "endpoint", "dns"):
            with self.subTest(change=change):
                mutated = deepcopy(self.template)
                rules = resource(mutated, f"{NAMESPACE}/networkRuleSets")["properties"]
                if change == "public":
                    resource(mutated, NAMESPACE)["properties"]["publicNetworkAccess"] = "Enabled"
                elif change == "allow":
                    rules["defaultAction"] = "Allow"
                elif change == "no-trust":
                    rules["trustedServiceAccessEnabled"] = False
                else:
                    endpoint = next(
                        item
                        for item in mutated["resources"]
                        if item.get("properties", {})
                        .get("parameters", {})
                        .get("groupId", {})
                        .get("value")
                        == "namespace"
                    )
                    if change == "endpoint":
                        mutated["resources"].remove(endpoint)
                    else:
                        endpoint["properties"]["parameters"]["dnsZoneIds"]["value"] = []
                with self.assertRaises(AssertionError):
                    self.assert_private_network(mutated)

    def assert_diagnostics(self, template) -> None:
        diagnostics = [
            item
            for item in resources(template)
            if item["type"] == "Microsoft.Insights/diagnosticSettings"
        ]
        self.assertEqual(len(diagnostics), 2)
        for item in diagnostics:
            self.assertEqual(item["name"], "to-log-analytics")
            self.assertEqual(
                item["properties"],
                {
                    "workspaceId": "[parameters('workspaceId')]",
                    "logs": [{"categoryGroup": "allLogs", "enabled": False}],
                    "metrics": [{"category": "AllMetrics", "enabled": True}],
                },
            )
        self.assertTrue(any("Microsoft.Devices/IotHubs" in item["scope"] for item in diagnostics))
        self.assertTrue(
            any("Microsoft.EventHub/namespaces" in item["scope"] for item in diagnostics)
        )

    def test_diagnostics_export_metrics_and_explicitly_disable_resource_logs(self) -> None:
        self.assert_diagnostics(self.template)

    def test_mutations_reject_device_bearing_logs_or_wrong_workspace(self) -> None:
        for change in ("enabled-logs", "connections", "workspace"):
            with self.subTest(change=change):
                mutated = deepcopy(self.template)
                props = resource(mutated, "Microsoft.Insights/diagnosticSettings")["properties"]
                if change == "enabled-logs":
                    props["logs"][0]["enabled"] = True
                elif change == "connections":
                    props["logs"].append({"category": "Connections", "enabled": True})
                else:
                    props["workspaceId"] = "wrong-workspace"
                with self.assertRaises(AssertionError):
                    self.assert_diagnostics(mutated)

    def test_sizing_retention_consumer_group_and_cost_are_bounded(self) -> None:
        for template, sku, units, cost in (
            (self.template, "skuName", "unitCount", "monthlyCostEstimate"),
            (self.main, "iotHubSku", "iotHubUnits", "iotHubMonthlyCost"),
        ):
            params = template["parameters"]
            self.assertEqual(params[sku]["allowedValues"], ["B1"])
            self.assertEqual(params[sku]["defaultValue"], "B1")
            self.assertEqual(params[units]["minValue"], 1)
            self.assertEqual(params[units]["maxValue"], 1)
            self.assertEqual(params[cost]["defaultValue"], 60)
            self.assertEqual(params[cost]["minValue"], 1)
            self.assertEqual(params[cost]["maxValue"], 700)
        params = self.template["parameters"]
        self.assertEqual(params["retentionDays"]["defaultValue"], 1)
        self.assertEqual(params["retentionDays"]["minValue"], 1)
        self.assertEqual(params["retentionDays"]["maxValue"], 7)
        self.assertEqual(params["partitionCount"]["defaultValue"], 2)
        self.assertEqual(params["partitionCount"]["minValue"], 2)
        self.assertEqual(params["partitionCount"]["maxValue"], 32)
        namespace = resource(self.template, NAMESPACE)
        self.assertEqual(namespace["sku"], {"name": "Standard", "tier": "Standard", "capacity": 1})
        self.assertFalse(namespace["properties"]["isAutoInflateEnabled"])
        self.assertEqual(namespace["properties"]["maximumThroughputUnits"], 1)
        hub = resource(self.template, HUB)
        self.assertEqual(
            hub["sku"], {"name": "[parameters('skuName')]", "capacity": "[parameters('unitCount')]"}
        )
        telemetry = resource(self.template, EVENT_HUB)
        for days in (1, 7):
            self.assertEqual(
                evaluate(
                    telemetry["properties"]["retentionDescription"],
                    {"retentionDays": days},
                    {},
                ),
                {"cleanupPolicy": "Delete", "retentionTimeInHours": days * 24},
            )
        self.assertEqual(
            hub["properties"]["eventHubEndpoints"]["events"]["retentionTimeInDays"],
            "[parameters('retentionDays')]",
        )
        group = resource(self.template, f"{EVENT_HUB}/consumergroups")
        self.assertEqual(
            evaluate(group["name"], self.values(), self.template["variables"]),
            "eh-fixture/sensor-readings/api-consumer",
        )
        budget = resource(self.template, "Microsoft.Consumption/budgets")["properties"]
        self.assertEqual(budget["amount"], "[parameters('monthlyCostEstimate')]")
        self.assertEqual(budget["timeGrain"], "Monthly")
        filters = budget["filter"]["dimensions"]
        self.assertEqual(filters["name"], "ResourceId")
        self.assertEqual(filters["operator"], "In")
        self.assertEqual(len(filters["values"]), 4)
        self.assertEqual(len(set(filters["values"])), 4)
        for kind in (HUB, NAMESPACE, "Microsoft.Network/privateEndpoints"):
            self.assertTrue(any(kind in value for value in filters["values"]))
        self.assertEqual(set(budget["notifications"]), {"actual80", "forecast100"})
        for name, threshold, kind in (
            ("actual80", 80, "Actual"),
            ("forecast100", 100, "Forecasted"),
        ):
            notice = budget["notifications"][name]
            self.assertTrue(notice["enabled"])
            self.assertEqual(notice["threshold"], threshold)
            self.assertEqual(notice["thresholdType"], kind)
            self.assertEqual(notice["contactEmails"], ["[parameters('alertEmail')]"])

    def assert_scope_guards(self, main, standalone) -> None:
        for template, guard_name, region_name in (
            (main, "parameter-guard", "primaryLocationMustBeUKSouth"),
            (standalone, "iot-scope-guard", "iotLocationMustBeUKSouth"),
        ):
            guard = module(template, guard_name)
            for group, region in (
                ("ama", "uksouth"),
                ("other", "uksouth"),
                ("ama", "westus"),
                ("other", "westus"),
            ):
                context = {
                    "resourceGroup": lambda group=group, region=region: SimpleNamespace(
                        name=group, location=region
                    )
                }
                for check, accepted in (
                    ("resourceGroupMustBeAma", group == "ama"),
                    (region_name, region == "uksouth"),
                ):
                    self.assertIn(check, guard["properties"]["template"]["parameters"])
                    self.assertIn(check, guard["properties"]["parameters"])
                    spec = guard["properties"]["template"]["parameters"][check]
                    self.assertEqual(spec["minLength"], 1)
                    value = evaluate(
                        guard["properties"]["parameters"][check],
                        {"location": region},
                        template.get("variables", {}),
                        context,
                    )["value"]
                    self.assertEqual(bool(value), accepted, (guard_name, check, group, region))
            self.assertEqual(unguarded_resources(template, guard_name), set())

    def test_main_and_standalone_scope_checks_precede_every_resource(self) -> None:
        self.assert_scope_guards(self.main, self.template)

    def test_mutations_reject_scope_guard_bypass(self) -> None:
        for target in ("main", "standalone"):
            for change in (
                "group",
                "region",
                "dependency",
                "group-removed",
                "region-removed",
                "constraint",
            ):
                with self.subTest(target=target, change=change):
                    main, standalone = deepcopy(self.main), deepcopy(self.template)
                    template = main if target == "main" else standalone
                    name = "parameter-guard" if target == "main" else "iot-scope-guard"
                    guard = module(template, name)
                    if change == "dependency":
                        item = (
                            module(main, "identity")
                            if target == "main"
                            else resource(standalone, NAMESPACE)
                        )
                        item["dependsOn"] = []
                    else:
                        check = (
                            "resourceGroupMustBeAma"
                            if change.startswith("group")
                            else (
                                "primaryLocationMustBeUKSouth"
                                if target == "main"
                                else "iotLocationMustBeUKSouth"
                            )
                        )
                        if change.endswith("-removed"):
                            del guard["properties"]["parameters"][check]
                        elif change == "constraint":
                            guard["properties"]["template"]["parameters"][check]["minLength"] = 0
                        else:
                            guard["properties"]["parameters"][check] = {"value": "ok"}
                    with self.assertRaises(AssertionError):
                        self.assert_scope_guards(main, standalone)

    def test_main_wires_only_api_identity_and_nonsecret_consumer_outputs(self) -> None:
        params = module(self.main, "iothub")["properties"]["parameters"]
        self.assertEqual(
            params["consumerPrincipalId"]["value"],
            "[reference(resourceId('Microsoft.Resources/deployments', 'identity'), "
            "'2025-04-01').outputs.principalIds.value.api]",
        )
        self.assertEqual(params["routingReady"], {"value": "[parameters('iotHubRoutingReady')]"})
        self.assertFalse(self.main["parameters"]["iotHubRoutingReady"]["defaultValue"])
        self.assertEqual(
            params["allowPublicNetworkAccess"], {"value": "[variables('publicAccess')]"}
        )
        for output in (
            "iotHubEventHubNamespaceFqdn",
            "iotHubEventHubName",
            "iotHubConsumerGroup",
            "iotHubRoutingEnabled",
        ):
            self.assertIn(output, self.main["outputs"])


if __name__ == "__main__":
    unittest.main()
