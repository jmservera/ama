"""Static guards on private-endpoint coverage and the public edge (issue 143)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
EDGE = (MODULES / "edge.bicep").read_text(encoding="utf-8")
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")
GUARD = (MODULES / "guard.bicep").read_text(encoding="utf-8")

# Services with a publicNetworkAccess switch and the group IDs of their private endpoints.
COVERAGE = {
    "sql.bicep": ["sqlServer"],
    "storage.bicep": ["blob", "queue"],
    "keyvault.bicep": ["vault"],
    "registry.bicep": ["registry"],
    "foundry.bicep": ["account"],
    "iothub.bicep": ["iotHub"],
    "monitoring.bicep": ["azuremonitor"],
    "authTokenStore.bicep": ["blob"],
}


class PrivateEndpointCoverageTests(unittest.TestCase):
    def test_every_public_switch_module_has_private_endpoint(self) -> None:
        for name, groups in COVERAGE.items():
            text = (MODULES / name).read_text(encoding="utf-8")
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
        self.assertIn("internal: !allowPublicNetworkAccess", text)


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


if __name__ == "__main__":
    unittest.main()
