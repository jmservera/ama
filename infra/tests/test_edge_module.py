"""Static guards on private-endpoint coverage and the public edge (issue 143)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
EDGE = (MODULES / "edge.bicep").read_text(encoding="utf-8")
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")
GUARD = (MODULES / "guard.bicep").read_text(encoding="utf-8")

# Data services and the group IDs of their private endpoints.
COVERAGE = {
    "sql.bicep": ["sqlServer"],
    "storage.bicep": ["blob", "queue"],
    "keyvault.bicep": ["vault"],
    "registry.bicep": ["registry"],
    "foundry.bicep": ["account"],
    "iothub.bicep": ["iotHub", "namespace"],
    "monitoring.bicep": ["azuremonitor"],
    "authTokenStore.bicep": ["blob"],
}


# Private DNS zone names (prefix match against network.bicep dnsZones) each endpoint group must use.
EXPECTED_ZONES = {
    "sql.bicep": {"sqlServer": ["privatelink${environment().suffixes.sqlServerHostname}"]},
    "storage.bicep": {"blob": ["privatelink.blob."], "queue": ["privatelink.queue."]},
    "keyvault.bicep": {"vault": ["privatelink.vaultcore.azure.net"]},
    "registry.bicep": {"registry": ["privatelink${environment().suffixes.acrLoginServer}"]},
    "foundry.bicep": {"account": ["privatelink.cognitiveservices.azure.com", "privatelink.openai.azure.com", "privatelink.services.ai.azure.com"]},
    "iothub.bicep": {
        "iotHub": ["privatelink.azure-devices.net", "privatelink.servicebus.windows.net"],
        "namespace": ["privatelink.servicebus.windows.net"],
    },
    "monitoring.bicep": {"azuremonitor": ["privatelink.monitor.azure.com", "privatelink.oms.opinsights.azure.com", "privatelink.ods.opinsights.azure.com", "privatelink.agentsvc.azure-automation.net", "privatelink.blob."]},
    "authTokenStore.bicep": {"blob": ["privatelink.blob."]},
}


def _zone_key_names() -> dict:
    """Map each zoneIds output key to its zone name by position in network.bicep."""
    network = (MODULES / "network.bicep").read_text(encoding="utf-8")
    zones = re.findall(r"^  '(.+)'$", re.search(r"var dnsZones = \[(.*?)\n\]", network, re.S).group(1), re.M)
    keys = re.findall(r"^  (\w+): zones\[(\d+)\]\.id$", network, re.M)
    return {k: zones[int(i)] for k, i in keys}


def _main_zone_params(module_file: str) -> dict:
    """Map single-zone parameter names passed to a module in main.bicep to the zoneIds key."""
    block = re.search(rf"module \w+ 'modules/{re.escape(module_file)}' = [^\n]*?\{{\n(.*?)\n\}}", MAIN, re.S)
    return dict(re.findall(r"(\w+): network\.outputs\.zoneIds\.(\w+)", block.group(1))) if block else {}


def _endpoint_calls(text: str, module_file: str) -> dict:
    """Return {groupId: [zone names]} for every privateEndpoint.bicep call in a module."""
    zone_names = _zone_key_names()
    passed = _main_zone_params(module_file)
    calls = {}
    for body in re.findall(r"module \w+ 'privateEndpoint\.bicep' = .*?\{(.*?)\n\}", text, re.S):
        group = re.search(r"groupId: '(\w+)'", body).group(1)
        ids = re.search(r"dnsZoneIds: \[(.*?)\]", body).group(1)
        names = []
        for ref in [r.strip() for r in ids.split(",")]:
            key = ref.split(".")[-1] if ref.startswith("zoneIds.") else passed[ref]
            names.append(zone_names[key])
        calls[group] = names
    return calls


class PrivateEndpointCoverageTests(unittest.TestCase):
    def test_endpoint_dns_zones_resolve_to_network_zone_list(self) -> None:
        for name, groups in EXPECTED_ZONES.items():
            text = (MODULES / name).read_text(encoding="utf-8")
            calls = _endpoint_calls(text, name)
            self.assertEqual(set(calls), set(groups), name)
            for group, expected in groups.items():
                self.assertEqual(len(calls[group]), len(expected), f"{name} {group}")
                for actual, prefix in zip(calls[group], expected):
                    self.assertTrue(actual.startswith(prefix), f"{name} {group}: {actual} != {prefix}")

    def test_every_public_switch_module_has_private_endpoint(self) -> None:
        for name, groups in COVERAGE.items():
            text = (MODULES / name).read_text(encoding="utf-8")
            if name == "sql.bicep":
                self.assertIn("publicNetworkAccess: 'Disabled'", text, name)
                self.assertNotIn("param allowPublicNetworkAccess", text, name)
                self.assertNotIn("Microsoft.Sql/servers/firewallRules", text, name)
            else:
                self.assertIn("allowPublicNetworkAccess ? 'Enabled' : 'Disabled'", text, name)
            self.assertIn("privateEndpoint.bicep", text, name)
            for group in groups:
                self.assertIn(f"groupId: '{group}'", text, name)

    def test_no_unchecked_public_switch_module(self) -> None:
        for path in MODULES.glob("*.bicep"):
            if "publicNetworkAccess" in path.read_text(encoding="utf-8"):
                self.assertTrue(path.name in COVERAGE or path.name == "containerapps.bicep", path.name)

    def test_container_environment_internal_in_production(self) -> None:
        text = (MODULES / "containerapps.bicep").read_text(encoding="utf-8")
        self.assertIn("internal: !externalEnvironment", text)
        self.assertIn("var externalEnvironment = demoDirectIngress || allowPublicNetworkAccess", text)


class PublicEdgeTests(unittest.TestCase):
    def test_front_door_premium_waf_and_private_link_origin(self) -> None:
        self.assertIn("Premium_AzureFrontDoor", EDGE)
        self.assertIn("Microsoft_DefaultRuleSet", EDGE)
        self.assertIn("groupId: 'managedEnvironments'", EDGE)
        self.assertIn("securityPolicies", EDGE)
        self.assertIn("ManagedCertificate", EDGE)

    def test_edge_off_by_default_and_production_only(self) -> None:
        self.assertIn("param enablePublicEdge bool = false", MAIN)
        self.assertIn("!enablePublicEdge || (!isDev && !allowPublicNetworkAccess)", MAIN)
        self.assertIn("publicEdgeRequiresProductionProfile", GUARD)

    def test_entra_callback_follows_edge_host(self) -> None:
        self.assertIn("/.auth/login/aad/callback", EDGE)
        self.assertIn("output entraRedirectUri", MAIN)
        self.assertIn("behindPublicEdge: enablePublicEdge", MAIN)

    def test_entra_callback_path_and_host_are_single_sourced(self) -> None:
        manifest = json.loads((ROOT / "entra" / "app-registration.json").read_text(encoding="utf-8"))
        match = re.search(r"output entraRedirectUri string = 'https://\$\{([^}]+)\}(/[^']+)'", EDGE)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.group(2), manifest["callbackPath"])
        self.assertEqual(match.group(1), "hasDomain ? customDomain : endpoint.properties.hostName")
        self.assertIn("output entraRedirectUri string = enablePublicEdge ? edge!.outputs.entraRedirectUri : ''", MAIN)
        self.assertIn("customDomain: edgeCustomDomain", MAIN)

    def test_health_and_all_path_route_do_not_cache_sessions(self) -> None:
        self.assertIn("probePath: '/healthz'", EDGE)
        self.assertIn("probeRequestType: 'GET'", EDGE)
        self.assertIn("patternsToMatch: ['/*']", EDGE)
        self.assertNotIn("cacheConfiguration:", EDGE)
        self.assertIn("originHostHeader: originHostName", EDGE)
        self.assertIn("enforceCertificateNameCheck: true", EDGE)


if __name__ == "__main__":
    unittest.main()
