"""Policy-as-code checks on the compiled Bicep: README security claims and parameter guards."""

import json
import os
import re
import shutil
import subprocess
import unittest
from copy import deepcopy
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, ClassVar

INFRA = Path(__file__).resolve().parents[1]
CONFIG = json.loads((INFRA / "bicepconfig.json").read_text(encoding="utf-8"))
PUBLIC = "[if(parameters('allowPublicNetworkAccess'), 'Enabled', 'Disabled')]"
PUBLIC_PROPERTIES = (
    "publicNetworkAccess",
    "publicNetworkAccessForIngestion",
    "publicNetworkAccessForQuery",
)
FORBIDDEN_KEY_FUNCTIONS = (
    "listKeys",
    "listAccountSas",
    "listCredentials",
    "listSecrets",
    "administratorLoginPassword",
)
SERVICES = {
    "storage": (
        "Microsoft.Storage/storageAccounts",
        {"blob": ["zoneIds.blob"], "queue": ["zoneIds.queue"]},
    ),
    "auth-token-store": ("Microsoft.Storage/storageAccounts", {"blob": ["blobZoneId"]}),
    "sql": ("Microsoft.Sql/servers", {"sqlServer": ["zoneId"]}),
    "keyvault": ("Microsoft.KeyVault/vaults", {"vault": ["zoneId"]}),
    "registry": ("Microsoft.ContainerRegistry/registries", {"registry": ["zoneId"]}),
    "foundry": (
        "Microsoft.CognitiveServices/accounts",
        {"account": ["zoneIds.cognitive", "zoneIds.openai", "zoneIds.aiServices"]},
    ),
    "iothub": (
        "Microsoft.Devices/IotHubs",
        {"iotHub": ["zoneIds.iotHub", "zoneIds.iotHubEndpoint"]},
    ),
    "monitoring": (
        "microsoft.insights/privateLinkScopes",
        {
            "azuremonitor": [
                "zoneIds.monitor",
                "zoneIds.oms",
                "zoneIds.ods",
                "zoneIds.agentsvc",
                "zoneIds.blob",
            ]
        },
    ),
}
NETWORK_RESOURCES: dict[str, dict[str, tuple[str, ...]]] = {
    **{
        name: {kind: ("publicNetworkAccess",)}
        for name, (kind, _) in SERVICES.items()
        if name not in ("monitoring", "sql")
    },
    "monitoring": {
        "Microsoft.OperationalInsights/workspaces": PUBLIC_PROPERTIES[1:],
        "Microsoft.Insights/components": PUBLIC_PROPERTIES[1:],
    },
    "containerapps": {"Microsoft.App/managedEnvironments": ("publicNetworkAccess",)},
}


def module(template: dict, name: str) -> dict:
    return next(r for r in template["resources"] if r["name"] == name)


def module_template(template: dict, name: str) -> dict:
    return module(template, name)["properties"]["template"]


def resource(template: dict, kind: str) -> dict:
    return next(r for r in resources(template) if r["type"] == kind)


def compile_bicep(name: str) -> dict:
    result = subprocess.run(
        ["az", "bicep", "build", "--file", str(INFRA / name), "--stdout"],
        capture_output=True,
        text=True,
        check=False,
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
    if not (
        isinstance(expression, str) and expression.startswith("[") and expression.endswith("]")
    ):
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
        "createObject": lambda *a: dict(zip(a[::2], a[1::2], strict=True)),
        "union": lambda *objects: {key: value for obj in objects for key, value in obj.items()},
        "true": lambda: True,
        "null": lambda: None,
        "format": lambda pattern, *args: pattern.format(*args),
    }
    return eval(source, {"__builtins__": {}}, scope)  # noqa: S307 - compiled repository template only


@unittest.skipUnless(
    shutil.which("az") or os.environ.get("REQUIRE_AZ_BICEP") == "1",
    "Azure CLI with Bicep is needed to compile the templates",
)
class BicepPolicyTests(unittest.TestCase):
    main: ClassVar[dict[str, Any]]
    guard: ClassVar[dict[str, Any]]
    defaults: ClassVar[dict[str, Any]]
    guard_module: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.main = compile_bicep("main.bicep")
        cls.guard = compile_bicep("modules/guard.bicep")
        cls.defaults = {
            k: v.get("defaultValue")
            for k, v in cls.main["parameters"].items()
            if "defaultValue" in v
        }
        cls.guard_module = next(r for r in cls.main["resources"] if r["name"] == "parameter-guard")

    def test_missing_az_is_a_failure_when_required(self) -> None:
        if os.environ.get("REQUIRE_AZ_BICEP") == "1":
            self.assertIsNotNone(shutil.which("az"), "az is required (REQUIRE_AZ_BICEP=1)")

    def test_every_deployed_resource_waits_for_the_guard(self) -> None:
        guard_id = "[resourceId('Microsoft.Resources/deployments', 'parameter-guard')]"
        items = self.main["resources"]
        items = list(items.values()) if isinstance(items, dict) else items
        depends = {r["name"]: set(r.get("dependsOn", [])) for r in items}

        def waits(name: str, seen: frozenset = frozenset()) -> bool:
            if guard_id in depends[name]:
                return True
            by_id = {
                f"[resourceId('{r['type']}', '{r['name']}')]": r["name"]
                for r in items
                if "/" not in r["name"] and r["type"] == "Microsoft.Resources/deployments"
            }
            return any(
                d in by_id and by_id[d] not in seen and waits(by_id[d], seen | {name})
                for d in depends[name]
            )

        for item in items:
            if item["name"] == "parameter-guard":
                continue
            self.assertTrue(
                waits(item["name"]), f"{item['name']} can deploy before the parameter guard"
            )
        self.assertEqual(depends["parameter-guard"], set())

    def test_lint_rules_are_errors(self) -> None:
        self.assertIs(CONFIG["analyzers"]["core"]["enabled"], True)
        levels = {rule["level"] for rule in CONFIG["analyzers"]["core"]["rules"].values()}
        self.assertEqual(levels, {"error"})
        for required in (
            "no-unused-params",
            "secure-secrets-in-params",
            "outputs-should-not-contain-secrets",
        ):
            self.assertIn(required, CONFIG["analyzers"]["core"]["rules"])

    def test_configured_lint_error_fails_build_and_lint(self) -> None:
        with TemporaryDirectory(prefix="ama-bicep-policy-") as directory:
            path = Path(directory)
            (path / "bicepconfig.json").write_text(json.dumps(CONFIG), encoding="utf-8")
            source = path / "unused.bicep"
            source.write_text("param unused string = 'mutation'\n", encoding="utf-8")
            for action in ("build", "lint"):
                with self.subTest(action=action):
                    result = subprocess.run(
                        ["az", "bicep", action, "--file", str(source)],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("Error no-unused-params", result.stderr)

    def test_governance_uses_tenant_scoped_builtin_policy_ids(self) -> None:
        template = compile_bicep("governance.bicep")
        assignments = [
            r
            for r in resources(template)
            if r["type"] == "Microsoft.Authorization/policyAssignments"
        ]
        self.assertEqual(len(assignments), 2)
        for assignment in assignments:
            self.assertTrue(
                assignment["properties"]["policyDefinitionId"].startswith(
                    "[tenantResourceId('Microsoft.Authorization/policyDefinitions', "
                ),
                assignment["name"],
            )

    def test_src_workload_images_and_job_commands(self) -> None:
        template = compile_bicep("modules/containerapps.bicep")
        containers = {
            container["name"]: container
            for resource in resources(template)
            for container in resource.get("properties", {})
            .get("template", {})
            .get("containers", [])
        }
        self.assertEqual(containers["api"]["image"], "[parameters('apiImage')]")
        for name, module, args in (
            ("auth-renewal", "token_store", []),
            ("ledger-verify", "digest_blob", ["--publish"]),
        ):
            self.assertEqual(containers[name]["image"], "[parameters('orchestratorImage')]")
            self.assertEqual(
                containers[name]["command"],
                ["python", "-m", f"zava_forward.orchestrator.{module}", *args],
            )

    def test_production_is_the_default_profile(self) -> None:
        self.assertEqual(self.defaults["deploymentProfile"], "production")
        self.assertIs(self.defaults["allowPublicNetworkAccess"], False)
        self.assertIs(self.defaults["keyVaultPurgeProtection"], True)
        self.assertIs(self.defaults["registryQuarantineEnabled"], True)
        self.assertIn(
            "param deploymentProfile = 'production'",
            (INFRA / "main.pilot.example.bicepparam").read_text(encoding="utf-8"),
        )

    def test_committed_environment_parameters_compile_and_match_the_contract(self) -> None:
        files = {
            "dev": "main.bicepparam",
            "test": "main.test.bicepparam",
            "pilot": "main.pilot.example.bicepparam",
        }
        guards = module(self.main, "parameter-guard")["properties"]["parameters"]
        for environment, filename in files.items():
            with self.subTest(environment=environment):
                result = subprocess.run(
                    ["az", "bicep", "build-params", "--file", str(INFRA / filename), "--stdout"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                compiled = json.loads(json.loads(result.stdout)["parametersJson"])["parameters"]
                values = {**self.defaults, **{k: v["value"] for k, v in compiled.items()}}
                self.assertEqual(values["environmentName"], environment)
                self.assertEqual(values["workload"], "forward")
                self.assertEqual(
                    values["deploymentProfile"],
                    "development" if environment == "dev" else "production",
                )
                self.assertIs(values["allowPublicNetworkAccess"], False)
                self.assertIs(values["keyVaultPurgeProtection"], environment != "dev")
                self.assertIs(values["registryQuarantineEnabled"], environment != "dev")
                self.assertIs(values["enableLocks"], environment == "pilot")
                self.assertIs(values["zoneRedundant"], False)
                self.assertEqual(values["regionCheckReference"], "")
                self.assertEqual(values["quotaCheckReference"], "")
                self.assertTrue(values["alertEmail"].endswith("@example.invalid"))
                self.assertEqual(
                    values["sqlAdminGroupObjectId"], "00000000-0000-0000-0000-000000000000"
                )
                self.assertEqual(values["entraClientId"], "")
                failures = {
                    name
                    for name, arg in guards.items()
                    if not evaluate(arg, values, self.main["variables"])["value"]
                }
                expected = {"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"}
                if environment == "pilot":
                    self.assertEqual(values["location"], "")
                    self.assertEqual(values["sqlLocation"], "")
                    expected.add("deploymentLocationsMustBeSelected")
                else:
                    self.assertEqual(values["location"], "uksouth")
                    self.assertEqual(values["sqlLocation"], "uksouth")
                self.assertEqual(failures, expected)
                source = (INFRA / filename).read_text(encoding="utf-8")
                for line in source.splitlines():
                    if "example.invalid" in line or "00000000-" in line or "= ''" in line:
                        self.assertIn("PLACEHOLDER", line)

    def test_naming_and_tags_are_forwarded_without_changing_existing_names(self) -> None:
        variables = self.main["variables"]
        self.assertEqual(
            variables["prefix"],
            "[format('{0}-{1}', parameters('workload'), parameters('environmentName'))]",
        )
        self.assertEqual(variables["compact"], "[replace(variables('prefix'), '-', '')]")
        self.assertEqual(
            variables["unique"],
            "[take(uniqueString(resourceGroup().id, parameters('location'), 'v2'), 5)]",
        )
        tags = variables["allTags"]
        for key in ("workload", "environment", "dataClassification", "purpose", "owner"):
            self.assertIn(f"'{key}'", tags)
        self.assertIn("union(parameters('tags'),", tags)
        self.assertIn("parameters('ownerTag')", tags)
        self.assertIn("parameters('environmentName')", tags)
        self.assertEqual(
            evaluate(
                tags,
                {
                    **self.defaults,
                    "environmentName": "test",
                    "ownerTag": "synthetic-resource-contact",
                    "tags": {"environment": "wrong", "owner": "wrong", "extra": "retained"},
                },
                variables,
            ),
            {
                "workload": "zava-forward-demonstrator",
                "environment": "test",
                "dataClassification": "constructed-non-identifying",
                "purpose": "non-production-demonstrator",
                "owner": "synthetic-resource-contact",
                "extra": "retained",
            },
        )
        for item in self.main["resources"]:
            params = item.get("properties", {}).get("parameters", {})
            if item["name"] == "parameter-guard":
                continue
            if item["type"] == "Microsoft.Resources/deployments":
                self.assertEqual(params["tags"]["value"], "[variables('allTags')]", item["name"])
            elif "tags" in item:
                self.assertEqual(item["tags"], "[variables('allTags')]", item["name"])
        for name, expression in {
            "keyvault": "[format('kv-{0}-{1}', variables('compact'), variables('unique'))]",
            "storage": "[format('st{0}{1}', variables('compact'), variables('unique'))]",
            "registry": "[format('cr{0}{1}', variables('compact'), variables('unique'))]",
            "sql": "[format('sql-{0}-{1}', variables('prefix'), variables('unique'))]",
        }.items():
            self.assertEqual(
                module(self.main, name)["properties"]["parameters"]["name"]["value"], expression
            )

    def assert_orchestrator_image_contract(self, template: dict) -> None:
        self.assertEqual(template["parameters"]["orchestratorImage"]["defaultValue"], "")
        expression = module(template, "containerapps")["properties"]["parameters"][
            "orchestratorImage"
        ]
        for value in (None, "", "registry/image:release", "registry/image@sha256:abc123"):
            parameters = {
                "orchestratorImage": (
                    template["parameters"]["orchestratorImage"]["defaultValue"]
                    if value is None
                    else value
                )
            }
            self.assertEqual(
                evaluate(expression, parameters, template.get("variables", {})),
                {"value": value or "mcr.microsoft.com/k8se/quickstart:latest"},
            )

    def test_orchestrator_image_empty_means_placeholder_explicit_image_is_preserved(self) -> None:
        self.assert_orchestrator_image_contract(self.main)
        template = module_template(self.main, "containerapps")
        for name in ("orchestrator", "auth-renewal", "ledger-verify"):
            container = next(
                c
                for r in template["resources"]
                for c in r.get("properties", {}).get("template", {}).get("containers", [])
                if c["name"] == name
            )
            self.assertEqual(container["image"], "[parameters('orchestratorImage')]")

    def test_orchestrator_image_contract_rejects_default_and_forwarding_mutations(self) -> None:
        for mutation in ("old-default", "empty-forwarding", "always-placeholder"):
            with self.subTest(mutation=mutation):
                template = deepcopy(self.main)
                if mutation == "old-default":
                    template["parameters"]["orchestratorImage"]["defaultValue"] = (
                        "mcr.microsoft.com/k8se/quickstart:latest"
                    )
                else:
                    module(template, "containerapps")["properties"]["parameters"][
                        "orchestratorImage"
                    ] = (
                        "[createObject('value', parameters('orchestratorImage'))]"
                        if mutation == "empty-forwarding"
                        else "[createObject('value', 'mcr.microsoft.com/k8se/quickstart:latest')]"
                    )
                with self.assertRaises(AssertionError):
                    self.assert_orchestrator_image_contract(template)

    def test_every_public_access_setting_follows_the_single_switch(self) -> None:
        self.assert_network_controls(self.main)

    def assert_network_controls(self, template: dict) -> None:
        for name, kinds in NETWORK_RESOURCES.items():
            nested = module_template(template, name)
            passed = module(template, name)["properties"]["parameters"]
            self.assertEqual(
                passed.get("allowPublicNetworkAccess"),
                {"value": "[variables('publicAccess')]"},
                name,
            )
            for kind, properties in kinds.items():
                matches = [r for r in resources(nested) if r["type"] == kind]
                self.assertEqual(len(matches), 1, f"{name}: missing/duplicate {kind}")
                for prop in properties:
                    self.assertEqual(matches[0]["properties"].get(prop), PUBLIC, f"{name}.{prop}")
        environment = resource(
            module_template(template, "containerapps"), "Microsoft.App/managedEnvironments"
        )
        self.assertEqual(
            environment["properties"]["vnetConfiguration"].get("internal"),
            "[not(parameters('allowPublicNetworkAccess'))]",
        )
        sql = module_template(template, "sql")
        self.assertNotIn("allowPublicNetworkAccess", sql["parameters"])
        self.assertNotIn(
            "allowPublicNetworkAccess", module(template, "sql")["properties"]["parameters"]
        )
        self.assertEqual(
            resource(sql, "Microsoft.Sql/servers")["properties"].get("publicNetworkAccess"),
            "Disabled",
        )
        self.assertFalse(
            any(r["type"] == "Microsoft.Sql/servers/firewallRules" for r in resources(sql))
        )

    def test_every_module_gets_the_computed_public_access(self) -> None:
        for module in self.main["resources"]:
            params = module.get("properties", {}).get("parameters", {})
            if "allowPublicNetworkAccess" in params:
                self.assertEqual(
                    params["allowPublicNetworkAccess"]["value"],
                    "[variables('publicAccess')]",
                    module["name"],
                )

    def test_production_profile_has_no_public_access(self) -> None:
        production = {**self.defaults, "deploymentProfile": "production"}
        self.assertFalse(
            evaluate(self.main["variables"]["publicAccess"], production, self.main["variables"])
        )
        self.assertTrue(
            evaluate(self.main["variables"]["purgeProtection"], production, self.main["variables"])
        )
        development = {
            **production,
            "deploymentProfile": "development",
            "allowPublicNetworkAccess": True,
        }
        self.assertTrue(
            evaluate(self.main["variables"]["publicAccess"], development, self.main["variables"])
        )

    def test_development_can_explicitly_keep_every_endpoint_private(self) -> None:
        parameters = {
            **self.defaults,
            "deploymentProfile": "development",
            "allowPublicNetworkAccess": False,
        }
        self.assertFalse(
            evaluate(self.main["variables"]["publicAccess"], parameters, self.main["variables"])
        )

    def test_ledger_alerts_use_azure_monitor_resource_specific_console_schema(self) -> None:
        alerts = [
            item
            for item in self.main["resources"]
            if item["type"] == "Microsoft.Insights/scheduledQueryRules"
            and "ledger-" in item["name"]
        ]
        self.assertEqual(len(alerts), 2)
        for alert in alerts:
            query = alert["properties"]["criteria"]["allOf"][0]["query"]
            self.assertIn("ContainerAppConsoleLogs | where JobName", query)
            self.assertIn(" and Log has ", query)
            self.assertNotIn("_CL", query)
            self.assertNotIn("Log_s", query)

    def test_environment_only_does_not_start_workloads(self) -> None:
        apps = module(self.main, "containerapps")
        self.assertEqual(
            apps["condition"],
            "[or(parameters('deployApplications'), parameters('deployEnvironmentOnly'))]",
        )
        self.assertEqual(
            apps["properties"]["parameters"]["deployWorkloads"]["value"],
            "[parameters('deployApplications')]",
        )
        template = module_template(self.main, "containerapps")
        for item in template["resources"]:
            if item["type"] in ("Microsoft.App/containerApps", "Microsoft.App/jobs"):
                self.assertIn("parameters('deployWorkloads')", item["condition"])

    def test_bearer_only_keeps_validation_and_omits_browser_secret(self) -> None:
        template = module_template(self.main, "containerapps")
        auth = resource(template, "Microsoft.App/containerApps/authConfigs")
        properties = auth["properties"]
        self.assertEqual(
            properties["globalValidation"]["unauthenticatedClientAction"],
            "[if(parameters('entraBearerOnly'), 'Return401', 'RedirectToLoginPage')]",
        )
        aad = properties["identityProviders"]["azureActiveDirectory"]
        self.assertIn("tenant().tenantId", aad["registration"]["openIdIssuer"])
        self.assertEqual(
            aad["registration"]["clientSecretSettingName"],
            "[if(parameters('entraBearerOnly'), null(), 'entra-client-secret')]",
        )
        self.assertIn("parameters('entraClientId')", aad["validation"]["allowedAudiences"])
        api = resource(template, "Microsoft.App/containerApps")
        self.assertIn(
            "not(parameters('entraBearerOnly'))", api["properties"]["configuration"]["secrets"]
        )
        guard = module(self.main, "parameter-guard")["properties"]["parameters"]
        expression = guard["bearerOnlyRequiresAudience"]
        for overrides, expected in (
            ({"entraBearerOnly": True}, ""),
            ({"entraBearerOnly": True, "entraClientId": "audience"}, "ok"),
            (
                {
                    "entraBearerOnly": True,
                    "entraClientId": "audience",
                    "enableEntraTokenStore": True,
                },
                "",
            ),
            ({"entraBearerOnly": False}, "ok"),
        ):
            self.assertEqual(
                evaluate(expression, {**self.defaults, **overrides}, self.main["variables"])[
                    "value"
                ],
                expected,
            )

    def test_no_keys_or_sql_logins(self) -> None:
        self.assert_key_controls(self.main)

    def assert_key_controls(self, template: dict) -> None:
        text = json.dumps(template).lower()
        for function in FORBIDDEN_KEY_FUNCTIONS:
            self.assertNotIn(function.lower(), text)
        by_type: dict[str, list[dict]] = {}
        for resource in resources(template):
            by_type.setdefault(resource["type"], []).append(resource.get("properties", {}))
        for props in by_type["Microsoft.Storage/storageAccounts"]:
            self.assertIs(props.get("allowSharedKeyAccess"), False)
            self.assertIs(props.get("allowBlobPublicAccess"), False)
        for props in by_type["Microsoft.ContainerRegistry/registries"]:
            self.assertIs(props.get("adminUserEnabled"), False)
        for props in by_type["Microsoft.CognitiveServices/accounts"]:
            self.assertIs(props.get("disableLocalAuth"), True)
        for props in by_type["Microsoft.Insights/components"]:
            self.assertIs(props.get("DisableLocalAuth"), True)
        for props in by_type["Microsoft.Devices/IotHubs"]:
            self.assertIs(props.get("disableLocalAuth"), True)
            self.assertIs(props.get("disableModuleSAS"), True)
        for props in by_type["Microsoft.OperationalInsights/workspaces"]:
            self.assertIs(props.get("features", {}).get("disableLocalAuth"), True)

    def test_sql_is_entra_only(self) -> None:
        self.assert_sql_controls(self.main)

    def assert_sql_controls(self, template: dict) -> None:
        servers = [
            r["properties"] for r in resources(template) if r["type"] == "Microsoft.Sql/servers"
        ]
        self.assertTrue(servers)
        for props in servers:
            self.assertIs(props.get("administrators", {}).get("azureADOnlyAuthentication"), True)
            self.assertNotIn("administratorLogin", props)
            self.assertNotIn("administratorLoginPassword", props)

    def test_key_vault_purge_protection_follows_profile(self) -> None:
        self.assert_purge_controls(self.main)

    def assert_purge_controls(self, template: dict) -> None:
        vaults = [
            r["properties"] for r in resources(template) if r["type"] == "Microsoft.KeyVault/vaults"
        ]
        self.assertTrue(vaults)
        for props in vaults:
            self.assertEqual(
                props.get("enablePurgeProtection"),
                "[if(parameters('purgeProtection'), true(), null())]",
            )
            self.assertIs(props.get("enableRbacAuthorization"), True)
            self.assertIs(props.get("enableSoftDelete"), True)
            self.assertEqual(
                props.get("softDeleteRetentionInDays"), "[if(parameters('purgeProtection'), 90, 7)]"
            )
        keyvault = module(template, "keyvault")
        self.assertEqual(
            keyvault["properties"]["parameters"].get("purgeProtection"),
            {"value": "[variables('purgeProtection')]"},
        )

    def test_audit_containers_have_immutability_policies(self) -> None:
        self.assert_retention_controls(self.main)

    def assert_retention_controls(self, template: dict) -> None:
        storage = module_template(template, "storage")
        policies = [r for r in resources(storage) if r["type"].endswith("/immutabilityPolicies")]
        self.assertEqual(len(policies), 2)
        names = {}
        for policy in policies:
            self.assertNotIn("condition", policy)
            name = evaluate(policy["name"], {"name": "fixture"}, storage["variables"])
            names[name] = policy
        for container, param, append in (
            ("audit-archive", "auditImmutabilityDays", True),
            ("ledger-digests", "ledgerDigestImmutabilityDays", False),
        ):
            name = f"fixture/default/{container}/default"
            self.assertIn(name, names, f"missing policy on {container}")
            props = names[name]["properties"]
            self.assertEqual(
                props.get("immutabilityPeriodSinceCreationInDays"), f"[parameters('{param}')]"
            )
            self.assertIs(props.get("allowProtectedAppendWrites"), append)
            spec = storage["parameters"][param]
            self.assertGreaterEqual(spec.get("minValue", 0), 1, param)
            self.assertGreaterEqual(spec["defaultValue"], spec["minValue"], param)

    def test_each_data_service_has_a_private_endpoint(self) -> None:
        self.assert_endpoint_controls(self.main)

    def assert_endpoint_controls(self, template: dict) -> None:
        for name, (kind, groups) in SERVICES.items():
            nested = module_template(template, name)
            target = resource(nested, kind)
            endpoints = [
                r
                for r in nested["resources"]
                if r["type"] == "Microsoft.Resources/deployments"
                and "groupId" in r["properties"].get("parameters", {})
            ]
            self.assertEqual(len(endpoints), len(groups), name)
            self.assertEqual(
                {r["properties"]["parameters"]["groupId"]["value"] for r in endpoints},
                set(groups),
                name,
            )
            self.assertEqual(
                module(template, name)["properties"]["parameters"].get("peSubnetId"),
                {
                    "value": "[reference(resourceId('Microsoft.Resources/deployments', "
                    "'network'), '2025-04-01').outputs.peSubnetId.value]"
                },
                name,
            )
            for endpoint in endpoints:
                self.assertNotIn("condition", endpoint, name)
                params = endpoint["properties"]["parameters"]
                group = params["groupId"]["value"]
                self.assertEqual(
                    params.get("targetResourceId"),
                    {"value": f"[resourceId('{kind}', {target['name'][1:-1]})]"},
                    name,
                )
                self.assertEqual(
                    params.get("subnetId"), {"value": "[parameters('peSubnetId')]"}, name
                )
                expected_zones = []
                for zone in groups[group]:
                    param, _, field = zone.partition(".")
                    expected_zones.append(f"[parameters('{param}'){'.' + field if field else ''}]")
                self.assertEqual(params.get("dnsZoneIds"), {"value": expected_zones}, name)
                pe_template = endpoint["properties"]["template"]
                pes = [
                    r
                    for r in resources(pe_template)
                    if r["type"] == "Microsoft.Network/privateEndpoints"
                ]
                self.assertEqual(len(pes), 1, name)
                self.assertNotIn("condition", pes[0], name)
                self.assertEqual(
                    pes[0]["properties"].get("subnet"), {"id": "[parameters('subnetId')]"}, name
                )
                connections = pes[0]["properties"].get("privateLinkServiceConnections", [])
                self.assertEqual(len(connections), 1, name)
                self.assertEqual(
                    connections[0]["properties"],
                    {
                        "privateLinkServiceId": "[parameters('targetResourceId')]",
                        "groupIds": ["[parameters('groupId')]"],
                    },
                    name,
                )
                dns = [
                    r
                    for r in resources(pe_template)
                    if r["type"] == "Microsoft.Network/privateEndpoints/privateDnsZoneGroups"
                ]
                self.assertEqual(len(dns), 1, name)
                self.assertNotIn("condition", dns[0], name)
                self.assertEqual(
                    evaluate(dns[0]["name"], {"name": "fixture"}, {}),
                    evaluate(pes[0]["name"], {"name": "fixture"}, {}) + "/default",
                    name,
                )
                self.assertEqual(
                    dns[0]["properties"].get("copy"),
                    [
                        {
                            "name": "privateDnsZoneConfigs",
                            "count": "[length(parameters('dnsZoneIds'))]",
                            "input": {
                                "name": "[format('zone{0}', copyIndex('privateDnsZoneConfigs'))]",
                                "properties": {
                                    "privateDnsZoneId": "[parameters('dnsZoneIds')"
                                    "[copyIndex('privateDnsZoneConfigs')]]"
                                },
                            },
                        }
                    ],
                    name,
                )

    def test_unsupported_parameter_combinations_are_rejected_with_a_named_check(self) -> None:
        self.assert_parameter_controls(self.main)

    def assert_parameter_controls(self, template: dict) -> None:
        guard_parameters = self.guard["parameters"]
        defaults = {
            k: v["defaultValue"] for k, v in template["parameters"].items() if "defaultValue" in v
        }
        for name, spec in guard_parameters.items():
            self.assertEqual(spec["minLength"], 1, name)
            self.assertIn("Empty means", spec["metadata"]["description"], name)
        passed = module(template, "parameter-guard")["properties"]["parameters"]
        self.assertEqual(set(passed), set(guard_parameters))

        def failures(**overrides) -> set[str]:
            values = {
                **defaults,
                "location": "offline-region",
                "sqlLocation": "offline-sql-region",
                "regionCheckReference": "synthetic-region-check",
                "quotaCheckReference": "synthetic-quota-check",
                "entraTokenStoreReady": False,
                **overrides,
            }
            return {
                name
                for name, arg in passed.items()
                if not evaluate(arg, values, template["variables"])["value"]
            }

        self.assertEqual(failures(), set())
        self.assertEqual(failures(regionCheckReference=""), {"regionCheckMustBeRecorded"})
        self.assertEqual(failures(quotaCheckReference=""), {"quotaCheckMustBeRecorded"})
        self.assertEqual(
            failures(regionCheckReference="", quotaCheckReference=""),
            {"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"},
        )
        for name in ("location", "sqlLocation"):
            self.assertEqual(failures(**{name: ""}), {"deploymentLocationsMustBeSelected"})
        self.assertEqual(
            failures(registryQuarantineEnabled=False),
            {"productionProfileRequiresRegistryQuarantine"},
        )
        self.assertEqual(
            failures(deploymentProfile="development", registryQuarantineEnabled=False), set()
        )
        self.assertEqual(
            module(template, "registry")["properties"]["parameters"]["quarantine"],
            {"value": "[parameters('registryQuarantineEnabled')]"},
        )
        self.assertEqual(
            failures(deploymentProfile="development", allowPublicNetworkAccess=True), set()
        )
        self.assertEqual(
            failures(allowPublicNetworkAccess=True), {"productionProfileForbidsPublicNetworkAccess"}
        )
        self.assertEqual(
            failures(keyVaultPurgeProtection=False),
            {"productionProfileRequiresKeyVaultPurgeProtection"},
        )
        self.assertEqual(
            failures(deploymentProfile="development", keyVaultPurgeProtection=False), set()
        )
        self.assertEqual(
            failures(evidenceStore="sharepoint", sharePointSiteId=""),
            {"sharePointEvidenceStoreRequiresSiteId"},
        )
        self.assertEqual(failures(evidenceStore="sharepoint", sharePointSiteId="site"), set())
        self.assertEqual(
            failures(entraTokenStoreReady=True, enableEntraTokenStore=False),
            {"tokenStoreReadyRequiresTokenStore"},
        )
        self.assertEqual(
            failures(entraRoleMap={"a": "b"}, entraClientId=""),
            {"entraRoleMapRequiresEntraClientId"},
        )
        self.assertEqual(failures(entraRoleMap={"a": "b"}, entraClientId="id"), set())
        for profile, public, purge, quarantine in product(
            ("production", "development"), (False, True), (False, True), (False, True)
        ):
            expected = set()
            if profile == "production":
                if public:
                    expected.add("productionProfileForbidsPublicNetworkAccess")
                if not purge:
                    expected.add("productionProfileRequiresKeyVaultPurgeProtection")
                if not quarantine:
                    expected.add("productionProfileRequiresRegistryQuarantine")
            overrides = {
                "deploymentProfile": profile,
                "allowPublicNetworkAccess": public,
                "keyVaultPurgeProtection": purge,
                "registryQuarantineEnabled": quarantine,
            }
            self.assertEqual(failures(**overrides), expected, str(overrides))
            if not expected:
                self.assertEqual(
                    evaluate(
                        template["variables"]["publicAccess"],
                        {**defaults, **overrides},
                        template["variables"],
                    ),
                    profile == "development" and public,
                    str(overrides),
                )
                self.assertEqual(
                    evaluate(
                        template["variables"]["purgeProtection"],
                        {**defaults, **overrides},
                        template["variables"],
                    ),
                    profile == "production" or purge,
                    str(overrides),
                )
            edge_expected = expected | (
                {"publicEdgeRequiresProductionProfile"}
                if profile != "production" or public
                else set()
            )
            self.assertEqual(failures(**overrides, enablePublicEdge=True), edge_expected)
            pilot_expected = expected | (
                {"pilotRequiresProductionProfile"} if profile != "production" or public else set()
            )
            self.assertEqual(failures(**overrides, environmentName="pilot"), pilot_expected)
        self.assertEqual(
            failures(enablePublicEdge=True, deployApplications=False),
            {"publicEdgeRequiresApplications"},
        )

    def assert_mutation_rejected(self, assertion, mutated: dict) -> None:
        with self.assertRaises(AssertionError):
            assertion(mutated)

    def test_mutations_reject_missing_or_public_network_controls(self) -> None:
        for name, kinds in NETWORK_RESOURCES.items():
            for kind, properties in kinds.items():
                for prop, remove in product(properties, (False, True)):
                    with self.subTest(module=name, property=prop, remove=remove):
                        mutated = deepcopy(self.main)
                        props = resource(module_template(mutated, name), kind)["properties"]
                        if remove:
                            del props[prop]
                        else:
                            props[prop] = "Enabled"
                        self.assert_mutation_rejected(self.assert_network_controls, mutated)
            with self.subTest(module=name, forwarding="removed"):
                mutated = deepcopy(self.main)
                del module(mutated, name)["properties"]["parameters"]["allowPublicNetworkAccess"]
                self.assert_mutation_rejected(self.assert_network_controls, mutated)
        mutated = deepcopy(self.main)
        resource(module_template(mutated, "containerapps"), "Microsoft.App/managedEnvironments")[
            "properties"
        ]["vnetConfiguration"]["internal"] = False
        self.assert_mutation_rejected(self.assert_network_controls, mutated)
        for change in ("public", "missing", "firewall", "switch"):
            with self.subTest(sql=change):
                mutated = deepcopy(self.main)
                sql = module_template(mutated, "sql")
                props = resource(sql, "Microsoft.Sql/servers")["properties"]
                if change == "public":
                    props["publicNetworkAccess"] = "Enabled"
                elif change == "missing":
                    del props["publicNetworkAccess"]
                elif change == "switch":
                    sql["parameters"]["allowPublicNetworkAccess"] = {"type": "bool"}
                else:
                    sql["resources"].append(
                        {
                            "type": "Microsoft.Sql/servers/firewallRules",
                            "name": "mutated-firewall",
                        }
                    )
                self.assert_mutation_rejected(self.assert_network_controls, mutated)

    def test_mutations_reject_key_auth_and_key_functions(self) -> None:
        controls = [
            ("storage", "Microsoft.Storage/storageAccounts", "allowSharedKeyAccess", True),
            ("auth-token-store", "Microsoft.Storage/storageAccounts", "allowSharedKeyAccess", True),
            ("registry", "Microsoft.ContainerRegistry/registries", "adminUserEnabled", True),
            ("foundry", "Microsoft.CognitiveServices/accounts", "disableLocalAuth", False),
            ("monitoring", "Microsoft.Insights/components", "DisableLocalAuth", False),
            ("iothub", "Microsoft.Devices/IotHubs", "disableLocalAuth", False),
            ("iothub", "Microsoft.Devices/IotHubs", "disableModuleSAS", False),
        ]
        for name, kind, prop, value in controls:
            for remove in (False, True):
                with self.subTest(module=name, property=prop, remove=remove):
                    mutated = deepcopy(self.main)
                    props = resource(module_template(mutated, name), kind)["properties"]
                    if remove:
                        del props[prop]
                    else:
                        props[prop] = value
                    self.assert_mutation_rejected(self.assert_key_controls, mutated)
        mutated = deepcopy(self.main)
        resource(
            module_template(mutated, "monitoring"), "Microsoft.OperationalInsights/workspaces"
        )["properties"]["features"]["disableLocalAuth"] = False
        self.assert_mutation_rejected(self.assert_key_controls, mutated)
        for function in FORBIDDEN_KEY_FUNCTIONS:
            with self.subTest(function=function):
                mutated = deepcopy(self.main)
                mutated.setdefault("outputs", {})["credential"] = {
                    "type": "string",
                    "value": f"[{function}('fixture', '2024-01-01')]",
                }
                self.assert_mutation_rejected(self.assert_key_controls, mutated)

    def test_mutations_reject_sql_and_purge_control_removal(self) -> None:
        for remove in (False, True):
            with self.subTest(control="entra-only", remove=remove):
                mutated = deepcopy(self.main)
                admin = resource(module_template(mutated, "sql"), "Microsoft.Sql/servers")[
                    "properties"
                ]["administrators"]
                if remove:
                    del admin["azureADOnlyAuthentication"]
                else:
                    admin["azureADOnlyAuthentication"] = False
                self.assert_mutation_rejected(self.assert_sql_controls, mutated)
            with self.subTest(control="purge", remove=remove):
                mutated = deepcopy(self.main)
                props = resource(module_template(mutated, "keyvault"), "Microsoft.KeyVault/vaults")[
                    "properties"
                ]
                if remove:
                    del props["enablePurgeProtection"]
                else:
                    props["enablePurgeProtection"] = False
                self.assert_mutation_rejected(self.assert_purge_controls, mutated)
        mutated = deepcopy(self.main)
        module(mutated, "keyvault")["properties"]["parameters"]["purgeProtection"]["value"] = False
        self.assert_mutation_rejected(self.assert_purge_controls, mutated)

    def test_mutations_reject_missing_wrong_or_zero_retention(self) -> None:
        kind = "Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies"
        for index in (0, 1):
            for change in ("remove", "target", "zero", "disabled"):
                with self.subTest(policy=index, change=change):
                    mutated = deepcopy(self.main)
                    storage = module_template(mutated, "storage")
                    policies = [r for r in resources(storage) if r["type"] == kind]
                    policy = policies[index]
                    if change == "remove":
                        storage["resources"].remove(policy)
                    elif change == "target":
                        policy["name"] = (
                            "[format('{0}/default/evidence/default', parameters('name'))]"
                        )
                    elif change == "disabled":
                        policy["condition"] = False
                    else:
                        policy["properties"]["immutabilityPeriodSinceCreationInDays"] = 0
                    self.assert_mutation_rejected(self.assert_retention_controls, mutated)
        for param in ("auditImmutabilityDays", "ledgerDigestImmutabilityDays"):
            mutated = deepcopy(self.main)
            del module_template(mutated, "storage")["parameters"][param]["minValue"]
            self.assert_mutation_rejected(self.assert_retention_controls, mutated)

    def test_mutations_reject_missing_or_disconnected_private_endpoints(self) -> None:
        for name in SERVICES:
            for change in ("remove", "target", "subnet", "zones", "resource", "connection", "dns"):
                with self.subTest(module=name, change=change):
                    mutated = deepcopy(self.main)
                    nested = module_template(mutated, name)
                    endpoint = next(
                        r
                        for r in nested["resources"]
                        if "groupId" in r.get("properties", {}).get("parameters", {})
                    )
                    params = endpoint["properties"]["parameters"]
                    pe_template = endpoint["properties"]["template"]
                    if change == "remove":
                        nested["resources"].remove(endpoint)
                    elif change in ("target", "subnet", "zones"):
                        key = {
                            "target": "targetResourceId",
                            "subnet": "subnetId",
                            "zones": "dnsZoneIds",
                        }[change]
                        params[key]["value"] = [] if change == "zones" else "wrong-resource"
                    elif change == "resource":
                        pe_template["resources"].remove(
                            resource(pe_template, "Microsoft.Network/privateEndpoints")
                        )
                    elif change == "connection":
                        resource(pe_template, "Microsoft.Network/privateEndpoints")["properties"][
                            "privateLinkServiceConnections"
                        ] = []
                    else:
                        pe_template["resources"].remove(
                            resource(
                                pe_template,
                                "Microsoft.Network/privateEndpoints/privateDnsZoneGroups",
                            )
                        )
                    self.assert_mutation_rejected(self.assert_endpoint_controls, mutated)

    def test_mutations_reject_production_guard_bypass(self) -> None:
        for name in (
            "productionProfileForbidsPublicNetworkAccess",
            "productionProfileRequiresKeyVaultPurgeProtection",
            "productionProfileRequiresRegistryQuarantine",
            "regionCheckMustBeRecorded",
            "quotaCheckMustBeRecorded",
            "deploymentLocationsMustBeSelected",
        ):
            with self.subTest(guard=name):
                mutated = deepcopy(self.main)
                module(mutated, "parameter-guard")["properties"]["parameters"][name] = {
                    "value": "ok"
                }
                self.assert_mutation_rejected(self.assert_parameter_controls, mutated)
        mutated = deepcopy(self.main)
        module(mutated, "registry")["properties"]["parameters"]["quarantine"]["value"] = False
        self.assert_mutation_rejected(self.assert_parameter_controls, mutated)
        for variable, value in (("publicAccess", True), ("purgeProtection", False)):
            with self.subTest(variable=variable):
                mutated = deepcopy(self.main)
                mutated["variables"][variable] = value
                self.assert_mutation_rejected(self.assert_parameter_controls, mutated)


if __name__ == "__main__":
    unittest.main()
