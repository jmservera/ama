"""Compiled IoT transport contracts and mutation guards (issue 140)."""

import json
import os
import shutil
import subprocess
import unittest
from copy import deepcopy
from types import SimpleNamespace

from test_bicep_policy import (
    INFRA,
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
SERVICE_BUS_ENDPOINTS = (
    "https://eh-fixture.servicebus.windows.net/",
    "https://eh-fixture.servicebus.windows.net:443/",
    "https://eh-fixture.servicebus.windows.net",
    "https://eh-fixture.servicebus.windows.net:443",
)


@unittest.skipUnless(
    shutil.which("az") or os.environ.get("REQUIRE_AZ_BICEP") == "1",
    "Azure CLI with Bicep is needed to compile the templates",
)
class IotHubModuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = compile_bicep("modules/iothub.bicep")
        cls.main = compile_bicep("main.bicep")
        cls.live = compile_bicep("iot-hub-live.bicep")

    def test_live_parameters_compile_and_match_the_approved_contract(self) -> None:
        result = subprocess.run(
            [
                "az",
                "bicep",
                "build-params",
                "--file",
                str(INFRA / "iot-hub-live.bicepparam"),
                "--stdout",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        compiled = json.loads(result.stdout)
        self.assertEqual(json.loads(compiled["templateJson"]), self.live)
        self.assertEqual(
            json.loads(compiled["parametersJson"])["parameters"],
            {
                "name": {"value": "iot-cutover-test-rzsrg"},
                "location": {"value": "uksouth"},
                "skuName": {"value": "B1"},
                "unitCount": {"value": 1},
            },
        )

    def test_live_profile_cannot_deploy_paid_adapter_endpoints_or_roles(self) -> None:
        self.assertEqual(
            sorted(item["type"] for item in resources(self.live)),
            sorted(
                [
                    f"{HUB}/eventHubEndpoints/ConsumerGroups",
                    "Microsoft.Insights/diagnosticSettings",
                ]
            ),
        )
        self.assertEqual(
            self.live["parameters"]["name"]["allowedValues"], ["iot-cutover-test-rzsrg"]
        )
        self.assertEqual(self.live["parameters"]["skuName"]["allowedValues"], ["B1"])
        self.assertEqual(self.live["parameters"]["unitCount"]["minValue"], 1)
        self.assertEqual(self.live["parameters"]["unitCount"]["maxValue"], 1)
        self.assertEqual(set(self.live["outputs"]), {"id", "hostname", "consumerGroup"})
        self.assertEqual(unguarded_resources(self.live, "iot-live-scope-guard"), set())

    def assert_live_sku_guards(self, template) -> None:
        self.assertFalse(any(item["type"] == HUB for item in resources(template)))
        guard = module(template, "iot-live-scope-guard")
        for key in ("existingHubSkuMustMatch", "existingHubUnitsMustMatch"):
            self.assertEqual(guard["properties"]["template"]["parameters"][key]["minLength"], 1)
            self.assertIn("reference(", guard["properties"]["parameters"][key]["value"])
        for sku, units in (("B1", 1), ("B1", 2), ("S1", 1)):

            def reference(identifier, *args, sku=sku, units=units):
                self.assertEqual(identifier, "/fixture/Microsoft.Devices/IotHubs/fixture")
                return SimpleNamespace(sku=SimpleNamespace(name=sku, capacity=units))

            context = {
                "reference": reference,
                "string": str,
            }
            for key, accepted in (
                ("existingHubSkuMustMatch", sku == "B1"),
                ("existingHubUnitsMustMatch", units == 1),
            ):
                value = evaluate(
                    guard["properties"]["parameters"][key],
                    self.values(template),
                    template.get("variables", {}),
                    context,
                )["value"]
                self.assertEqual(bool(value), accepted, (sku, units, key))
        self.assert_live_consumer_group(template)

    def test_live_profile_never_puts_existing_hub_and_guards_actual_sku(self) -> None:
        self.assert_live_sku_guards(self.live)

    def assert_live_consumer_group(self, template) -> None:
        group = resource(template, f"{HUB}/eventHubEndpoints/ConsumerGroups")
        self.assertEqual(
            evaluate(group["name"], self.values(template), template.get("variables", {})),
            "fixture/events/api-consumer",
        )

    def test_mutations_reject_live_consumer_group_wrong_hub_or_group(self) -> None:
        for name in (
            "[format('{0}/events/api-consumer', 'wrong-hub')]",
            "[format('{0}/events/wrong-group', parameters('name'))]",
        ):
            with self.subTest(name=name):
                mutated = deepcopy(self.live)
                resource(mutated, f"{HUB}/eventHubEndpoints/ConsumerGroups")["name"] = name
                with self.assertRaises(AssertionError):
                    self.assert_live_consumer_group(mutated)

    def assert_live_diagnostics(self, template) -> None:
        diagnostics = [
            item
            for item in resources(template)
            if item["type"] == "Microsoft.Insights/diagnosticSettings"
        ]
        self.assertEqual(len(diagnostics), 1)
        setting = diagnostics[0]
        self.assertEqual(setting["name"], "to-log-analytics")
        self.assertEqual(
            setting["scope"], "[resourceId('Microsoft.Devices/IotHubs', parameters('name'))]"
        )
        self.assertEqual(
            setting["properties"],
            {
                "workspaceId": (
                    "[resourceId('Microsoft.OperationalInsights/workspaces', 'log-cutover-test')]"
                ),
                "logAnalyticsDestinationType": "AzureDiagnostics",
                "logs": [{"categoryGroup": "allLogs", "enabled": False}],
                "metrics": [{"category": "AllMetrics", "enabled": True}],
            },
        )

    def test_live_profile_diagnostics_target_existing_hub_and_workspace(self) -> None:
        self.assert_live_diagnostics(self.live)

    def test_mutations_reject_live_diagnostics_wrong_name_hub_or_workspace(self) -> None:
        for change in ("name", "scope", "workspace"):
            with self.subTest(change=change):
                mutated = deepcopy(self.live)
                setting = resource(mutated, "Microsoft.Insights/diagnosticSettings")
                if change == "name":
                    setting["name"] = "wrong-setting"
                elif change == "scope":
                    setting["scope"] = "[resourceId('Microsoft.Devices/IotHubs', 'wrong-hub')]"
                else:
                    setting["properties"]["workspaceId"] = (
                        "[resourceId('Microsoft.OperationalInsights/workspaces', 'wrong-log')]"
                    )
                with self.assertRaises(AssertionError):
                    self.assert_live_diagnostics(mutated)

    def assert_live_scope_guards(self, template) -> None:
        guard = module(template, "iot-live-scope-guard")
        for group, requested, actual in (
            ("ama", "uksouth", "uksouth"),
            ("other", "uksouth", "uksouth"),
            ("ama", "westus", "westus"),
            ("ama", "uksouth", "westus"),
            ("ama", "westus", "uksouth"),
        ):

            def reference(identifier, *args, actual=actual):
                self.assertEqual(identifier, "/fixture/Microsoft.Devices/IotHubs/fixture")
                return SimpleNamespace(location=actual)

            context = {
                "resourceGroup": lambda group=group: SimpleNamespace(name=group),
                "reference": reference,
            }
            for check, accepted in (
                ("resourceGroupMustBeAma", group == "ama"),
                ("iotLocationMustBeUKSouth", requested == "uksouth" and actual == requested),
            ):
                self.assertIn(check, guard["properties"]["parameters"])
                self.assertIn(check, guard["properties"]["template"]["parameters"])
                spec = guard["properties"]["template"]["parameters"][check]
                self.assertEqual(spec.get("minLength"), 1)
                value = evaluate(
                    guard["properties"]["parameters"][check],
                    self.values(template, location=requested),
                    template.get("variables", {}),
                    context,
                )["value"]
                self.assertEqual(value, "ok" if accepted else "", (group, requested, actual, check))
        self.assertEqual(unguarded_resources(template, "iot-live-scope-guard"), set())

    def test_live_profile_scope_checks_requested_and_actual_location(self) -> None:
        self.assert_live_scope_guards(self.live)

    def test_mutations_reject_live_guards_referencing_another_hub(self) -> None:
        for key, assert_guards in (
            ("existingHubSkuMustMatch", self.assert_live_sku_guards),
            ("existingHubUnitsMustMatch", self.assert_live_sku_guards),
            ("iotLocationMustBeUKSouth", self.assert_live_scope_guards),
        ):
            with self.subTest(key=key):
                mutated = deepcopy(self.live)
                params = module(mutated, "iot-live-scope-guard")["properties"]["parameters"]
                parameter = params[key]
                before = parameter["value"] if isinstance(parameter, dict) else parameter
                after = before.replace(
                    "resourceId('Microsoft.Devices/IotHubs', parameters('name'))",
                    "resourceId('Microsoft.Devices/IotHubs', 'wrong-hub')",
                )
                self.assertNotEqual(after, before)
                params[key] = {"value": after} if isinstance(parameter, dict) else after
                with self.assertRaises(AssertionError) as failure:
                    assert_guards(mutated)
                self.assertIn(
                    "/fixture/Microsoft.Devices/IotHubs/wrong-hub", str(failure.exception)
                )
                self.assertIn("/fixture/Microsoft.Devices/IotHubs/fixture", str(failure.exception))

    def test_mutations_reject_live_scope_guard_bypass(self) -> None:
        for check in ("resourceGroupMustBeAma", "iotLocationMustBeUKSouth"):
            for change in ("bypass", "input-removed", "constraint", "constraint-removed"):
                with self.subTest(check=check, change=change):
                    mutated = deepcopy(self.live)
                    guard = module(mutated, "iot-live-scope-guard")
                    if change == "bypass":
                        guard["properties"]["parameters"][check] = {"value": "ok"}
                    elif change == "input-removed":
                        del guard["properties"]["parameters"][check]
                    else:
                        spec = guard["properties"]["template"]["parameters"][check]
                        if change == "constraint":
                            spec["minLength"] = 0
                        else:
                            del spec["minLength"]
                    with self.assertRaises(AssertionError):
                        self.assert_live_scope_guards(mutated)
        actual_location = (
            "equals(reference(resourceId('Microsoft.Devices/IotHubs', parameters('name')), "
            "'2023-06-30', 'full').location, parameters('location'))"
        )
        for original, replacement in (
            ("equals(parameters('location'), 'uksouth')", "true()"),
            (actual_location, "true()"),
            ("and(", "or("),
        ):
            with self.subTest(clause=original):
                mutated = deepcopy(self.live)
                params = module(mutated, "iot-live-scope-guard")["properties"]["parameters"]
                before = params["iotLocationMustBeUKSouth"]
                params["iotLocationMustBeUKSouth"] = before.replace(original, replacement)
                self.assertNotEqual(params["iotLocationMustBeUKSouth"], before)
                with self.assertRaises(AssertionError):
                    self.assert_live_scope_guards(mutated)
        for kind in (
            f"{HUB}/eventHubEndpoints/ConsumerGroups",
            "Microsoft.Insights/diagnosticSettings",
        ):
            with self.subTest(dependency=kind):
                mutated = deepcopy(self.live)
                resource(mutated, kind)["dependsOn"] = []
                with self.assertRaises(AssertionError):
                    self.assert_live_scope_guards(mutated)

    def values(self, template=None, **overrides):
        source = self.template if template is None else template
        defaults = {
            key: spec["defaultValue"]
            for key, spec in source["parameters"].items()
            if "defaultValue" in spec
        }
        return {**defaults, "name": "fixture", "location": "uksouth", **overrides}

    def assert_routing(self, template, service_bus_endpoint=SERVICE_BUS_ENDPOINTS[0]) -> None:
        hub = resource(template, HUB)
        self.assertEqual(hub["identity"], {"type": "SystemAssigned"})
        self.assertFalse(template["parameters"]["routingReady"]["defaultValue"])
        self.assertFalse(
            any(
                "Microsoft.Authorization/roleAssignments" in dep for dep in hub.get("dependsOn", [])
            )
        )
        context = {
            "reference": lambda *args: SimpleNamespace(serviceBusEndpoint=service_bus_endpoint),
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
        for endpoint in SERVICE_BUS_ENDPOINTS:
            with self.subTest(endpoint=endpoint):
                self.assert_routing(self.template, endpoint)

    def assert_consumer_outputs(self, template, main) -> None:
        for endpoint in SERVICE_BUS_ENDPOINTS:
            for ready in (False, True):
                context = {
                    "reference": lambda *args, endpoint=endpoint: SimpleNamespace(
                        serviceBusEndpoint=endpoint
                    )
                }
                expected = {
                    "eventHubNamespaceFqdn": "eh-fixture.servicebus.windows.net",
                    "eventHubCompatibleName": "sensor-readings",
                    "consumerGroup": "api-consumer",
                    "routingEnabled": ready,
                }
                actual = {
                    name: evaluate(
                        template["outputs"][name]["value"],
                        self.values(template, routingReady=ready),
                        template["variables"],
                        context,
                    )
                    for name in expected
                }
                self.assertEqual(actual, expected, (endpoint, ready))

                def reference(identifier, api_version, actual=actual):
                    self.assertEqual(identifier, "/fixture/Microsoft.Resources/deployments/iothub")
                    return SimpleNamespace(
                        outputs=SimpleNamespace(
                            **{name: SimpleNamespace(value=value) for name, value in actual.items()}
                        )
                    )

                for forwarded, original in (
                    ("iotHubEventHubNamespaceFqdn", "eventHubNamespaceFqdn"),
                    ("iotHubEventHubName", "eventHubCompatibleName"),
                    ("iotHubConsumerGroup", "consumerGroup"),
                    ("iotHubRoutingEnabled", "routingEnabled"),
                ):
                    self.assertEqual(
                        evaluate(
                            main["outputs"][forwarded]["value"],
                            self.values(main),
                            main["variables"],
                            {"reference": reference},
                        ),
                        expected[original],
                        (endpoint, ready, forwarded),
                    )

    def test_namespace_and_forwarded_outputs_are_evaluated_without_scheme_or_port(self) -> None:
        self.assert_consumer_outputs(self.template, self.main)

    def test_mutations_reject_management_ports_and_wrong_forwarded_outputs(self) -> None:
        for change in ("hostname", "routing-port", "forwarding"):
            with self.subTest(change=change):
                template, main = deepcopy(self.template), deepcopy(self.main)
                if change == "routing-port":
                    routing = resource(template, HUB)["properties"]["routing"]
                    original = routing["endpoints"]["eventHubs"]
                    routing["endpoints"]["eventHubs"] = original.replace(
                        "'sb://{0}/'", "'sb://{0}:443/'"
                    )
                    self.assertNotEqual(routing["endpoints"]["eventHubs"], original)
                    with self.assertRaises(AssertionError):
                        self.assert_routing(template, SERVICE_BUS_ENDPOINTS[1])
                else:
                    if change == "hostname":
                        template["outputs"]["eventHubNamespaceFqdn"]["value"] = (
                            "[replace(replace(reference(resourceId("
                            "'Microsoft.EventHub/namespaces', "
                            "'eh-fixture'), '2024-01-01').serviceBusEndpoint, "
                            "'https://', ''), '/', '')]"
                        )
                    else:
                        main["outputs"]["iotHubEventHubNamespaceFqdn"]["value"] = main["outputs"][
                            "iotHubEventHubNamespaceFqdn"
                        ]["value"].replace(
                            ".outputs.eventHubNamespaceFqdn", ".outputs.eventHubCompatibleName"
                        )
                    with self.assertRaises(AssertionError):
                        self.assert_consumer_outputs(template, main)

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
