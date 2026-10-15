"""Policy-as-code checks on the compiled Bicep: README security claims and parameter guards."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

INFRA = Path(__file__).resolve().parents[1]
CONFIG = json.loads((INFRA / "bicepconfig.json").read_text(encoding="utf-8"))
PUBLIC = "[if(parameters('allowPublicNetworkAccess'), 'Enabled', 'Disabled')]"
PUBLIC_PROPERTIES = ("publicNetworkAccess", "publicNetworkAccessForIngestion", "publicNetworkAccessForQuery")
FORBIDDEN_KEY_FUNCTIONS = ("listKeys", "listAccountSas", "listCredentials", "listSecrets", "administratorLoginPassword")


def compile_bicep(name: str) -> dict:
    result = subprocess.run(
        ["az", "bicep", "build", "--file", str(INFRA / name), "--stdout"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def resources(template: dict):
    """Yield every resource, descending into nested module templates."""
    items = template["resources"]
    for item in items.values() if isinstance(items, dict) else items:
        properties = item.get("properties", {})
        if item["type"] == "Microsoft.Resources/deployments" and "template" in properties:
            yield from resources(properties["template"])
        else:
            yield item


def evaluate(expression, parameters: dict, variables: dict):
    """Evaluate the small ARM expression subset used by the guard conditions."""
    if not (isinstance(expression, str) and expression.startswith("[") and expression.endswith("]")):
        return expression
    source = re.sub(r"\b(if|or|and|not)\(", r"\1_(", expression[1:-1])
    scope = {
        "if_": lambda c, a, b: a if c else b,
        "or_": lambda *a: any(a),
        "and_": lambda *a: all(a),
        "not_": lambda a: not a,
        "equals": lambda a, b: a == b,
        "empty": lambda a: not a,
        "parameters": lambda n: parameters[n],
        "variables": lambda n: evaluate(variables[n], parameters, variables),
        "createObject": lambda *a: dict(zip(a[::2], a[1::2])),
        "true": lambda: True,
        "null": lambda: None,
    }
    return eval(source, {"__builtins__": {}}, scope)  # noqa: S307 - compiled repository template only


@unittest.skipUnless(shutil.which("az"), "Azure CLI with Bicep is needed to compile the templates")
class BicepPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.main = compile_bicep("main.bicep")
        cls.guard = compile_bicep("modules/guard.bicep")
        cls.defaults = {k: v.get("defaultValue") for k, v in cls.main["parameters"].items() if "defaultValue" in v}
        cls.guard_module = next(r for r in cls.main["resources"] if r["name"] == "parameter-guard")

    def test_lint_rules_are_errors(self) -> None:
        levels = {rule["level"] for rule in CONFIG["analyzers"]["core"]["rules"].values()}
        self.assertEqual(levels, {"error"})
        for required in ("no-unused-params", "secure-secrets-in-params", "outputs-should-not-contain-secrets"):
            self.assertIn(required, CONFIG["analyzers"]["core"]["rules"])

    def test_production_is_the_default_profile(self) -> None:
        self.assertEqual(self.defaults["deploymentProfile"], "production")
        self.assertIs(self.defaults["allowPublicNetworkAccess"], False)
        self.assertIs(self.defaults["keyVaultPurgeProtection"], True)
        parameter_file = (INFRA / "main.bicepparam").read_text(encoding="utf-8")
        self.assertIn("param deploymentProfile = 'production'", parameter_file)

    def test_every_public_access_setting_follows_the_single_switch(self) -> None:
        seen = 0
        for resource in resources(self.main):
            for name in PUBLIC_PROPERTIES:
                if name in resource.get("properties", {}):
                    seen += 1
                    self.assertEqual(resource["properties"][name], PUBLIC, f"{resource['type']}.{name}")
        self.assertGreaterEqual(seen, 8)

    def test_every_module_gets_the_computed_public_access(self) -> None:
        for module in self.main["resources"]:
            params = module.get("properties", {}).get("parameters", {})
            if "allowPublicNetworkAccess" in params:
                self.assertEqual(params["allowPublicNetworkAccess"]["value"], "[variables('publicAccess')]", module["name"])

    def test_production_profile_has_no_public_access(self) -> None:
        production = {**self.defaults, "deploymentProfile": "production"}
        self.assertFalse(evaluate(self.main["variables"]["publicAccess"], production, self.main["variables"]))
        self.assertTrue(evaluate(self.main["variables"]["purgeProtection"], production, self.main["variables"]))
        development = {**production, "deploymentProfile": "development"}
        self.assertTrue(evaluate(self.main["variables"]["publicAccess"], development, self.main["variables"]))

    def test_no_keys_or_sql_logins(self) -> None:
        text = json.dumps(self.main)
        for function in FORBIDDEN_KEY_FUNCTIONS:
            self.assertNotIn(function, text)
        by_type: dict[str, list[dict]] = {}
        for resource in resources(self.main):
            by_type.setdefault(resource["type"], []).append(resource.get("properties", {}))
        for props in by_type["Microsoft.Storage/storageAccounts"]:
            self.assertIs(props["allowSharedKeyAccess"], False)
            self.assertIs(props["allowBlobPublicAccess"], False)
        for props in by_type["Microsoft.ContainerRegistry/registries"]:
            self.assertIs(props["adminUserEnabled"], False)
        for props in by_type["Microsoft.CognitiveServices/accounts"]:
            self.assertIs(props["disableLocalAuth"], True)
        for props in by_type["Microsoft.Insights/components"]:
            self.assertIs(props["DisableLocalAuth"], True)

    def test_sql_is_entra_only(self) -> None:
        servers = [r["properties"] for r in resources(self.main) if r["type"] == "Microsoft.Sql/servers"]
        self.assertTrue(servers)
        for props in servers:
            self.assertIs(props["administrators"]["azureADOnlyAuthentication"], True)
            self.assertNotIn("administratorLogin", props)
            self.assertNotIn("administratorLoginPassword", props)

    def test_key_vault_purge_protection_follows_profile(self) -> None:
        vaults = [r["properties"] for r in resources(self.main) if r["type"] == "Microsoft.KeyVault/vaults"]
        self.assertTrue(vaults)
        for props in vaults:
            self.assertEqual(props["enablePurgeProtection"], "[if(parameters('purgeProtection'), true(), null())]")
            self.assertIs(props["enableRbacAuthorization"], True)
        keyvault = next(m for m in self.main["resources"] if m["name"] == "keyvault")
        self.assertEqual(keyvault["properties"]["parameters"]["purgeProtection"]["value"], "[variables('purgeProtection')]")

    def test_audit_containers_have_immutability_policies(self) -> None:
        policies = [r for r in resources(self.main) if r["type"].endswith("/immutabilityPolicies")]
        self.assertGreaterEqual(len(policies), 2)
        for policy in policies:
            self.assertIn("immutabilityPeriodSinceCreationInDays", policy["properties"])

    def test_each_data_service_has_a_private_endpoint(self) -> None:
        groups = set()

        def collect(template: dict) -> None:
            items = template["resources"]
            for item in items.values() if isinstance(items, dict) else items:
                properties = item.get("properties", {})
                if item["type"] != "Microsoft.Resources/deployments":
                    continue
                if "groupId" in properties.get("parameters", {}):
                    groups.add(properties["parameters"]["groupId"]["value"])
                if "template" in properties:
                    collect(properties["template"])

        collect(self.main)
        self.assertTrue({"sqlServer", "blob", "queue", "vault", "registry", "account", "azuremonitor"} <= groups, groups)

    def test_unsupported_parameter_combinations_are_rejected_with_a_named_check(self) -> None:
        guard_parameters = self.guard["parameters"]
        for name, spec in guard_parameters.items():
            self.assertEqual(spec["minLength"], 1, name)
            self.assertIn("Empty means", spec["metadata"]["description"], name)
        passed = self.guard_module["properties"]["parameters"]
        self.assertEqual(set(passed), set(guard_parameters))

        def failures(**overrides) -> set[str]:
            values = {**self.defaults, "entraTokenStoreReady": False, **overrides}
            return {
                name for name, arg in passed.items()
                if not evaluate(arg, values, self.main["variables"])["value"]
            }

        self.assertEqual(failures(), set())
        self.assertEqual(failures(deploymentProfile="development", allowPublicNetworkAccess=True), set())
        self.assertEqual(failures(allowPublicNetworkAccess=True), {"productionProfileForbidsPublicNetworkAccess"})
        self.assertEqual(failures(keyVaultPurgeProtection=False), {"productionProfileRequiresKeyVaultPurgeProtection"})
        self.assertEqual(failures(deploymentProfile="development", keyVaultPurgeProtection=False), set())
        self.assertEqual(failures(evidenceStore="sharepoint", sharePointSiteId=""), {"sharePointEvidenceStoreRequiresSiteId"})
        self.assertEqual(failures(evidenceStore="sharepoint", sharePointSiteId="site"), set())
        self.assertEqual(failures(entraTokenStoreReady=True, enableEntraTokenStore=False), {"tokenStoreReadyRequiresTokenStore"})
        self.assertEqual(failures(entraRoleMap={"a": "b"}, entraClientId=""), {"entraRoleMapRequiresEntraClientId"})
        self.assertEqual(failures(entraRoleMap={"a": "b"}, entraClientId="id"), set())


if __name__ == "__main__":
    unittest.main()
