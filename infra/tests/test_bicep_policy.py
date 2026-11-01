"""Policy-as-code checks on the compiled Bicep: README security claims and parameter guards."""

import json
import os
import re
import shutil
import subprocess
import unittest
from copy import deepcopy
from functools import reduce
from ipaddress import IPv4Network
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
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
        {
            "iotHub": ["zoneIds.iotHub", "zoneIds.iotHubEndpoint"],
            "namespace": ["zoneIds.iotHubEndpoint"],
        },
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


def evaluate(expression, parameters: dict, variables: dict, context: dict | None = None):
    """Evaluate the small ARM expression subset used by the guard conditions."""
    if isinstance(expression, dict):
        return {
            key: evaluate(value, parameters, variables, context)
            for key, value in expression.items()
        }
    if isinstance(expression, list):
        return [evaluate(value, parameters, variables, context) for value in expression]
    if not (
        isinstance(expression, str) and expression.startswith("[") and expression.endswith("]")
    ):
        return expression
    source = re.sub(r"\b(if|or|and|not)\(", r"\1_(", expression[1:-1])
    source = source.replace(
        "lambda('remaining', 'digit', replace(lambdaVariables('remaining'), "
        "lambdaVariables('digit'), ''))",
        "(lambda remaining, digit: remaining.replace(digit, ''))",
    )
    scope = {
        "if_": lambda c, a, b: a if c else b,
        "or_": lambda *a: any(a),
        "and_": lambda *a: all(a),
        "not_": lambda a: not a,
        "equals": lambda a, b: a == b,
        "greaterOrEquals": lambda a, b: a >= b,
        "lessOrEquals": lambda a, b: a <= b,
        "empty": lambda a: not a,
        "coalesce": lambda *values: next(value for value in values if value is not None),
        "length": len,
        "split": lambda value, delimiter: value.split(delimiter),
        "toLower": str.lower,
        "take": lambda value, count: value[:count],
        "skip": lambda value, count: value[count:],
        "reduce": lambda values, initial, function: reduce(function, values, initial),
        "parameters": lambda n: parameters[n],
        "variables": lambda n: evaluate(variables[n], parameters, variables, context),
        "resourceGroup": lambda: SimpleNamespace(name="ama", location="uksouth"),
        "createObject": lambda *a: dict(zip(a[::2], a[1::2], strict=True)),
        "union": lambda *objects: {key: value for obj in objects for key, value in obj.items()},
        "true": lambda: True,
        "null": lambda: None,
        "format": lambda pattern, *args: pattern.format(*args),
        "replace": lambda value, old, new: value.replace(old, new),
        "createArray": lambda *values: list(values),
        "concat": lambda *values: reduce(lambda left, right: left + right, values),
        "mul": lambda left, right: left * right,
        "resourceId": lambda kind, *names: "/fixture/" + kind + "/" + "/".join(names),
    }
    scope.update(context or {})
    return eval(source, {"__builtins__": {}}, scope)  # noqa: S307 - compiled repository template only


def unguarded_resources(template: dict, guard_name: str) -> set[str]:
    """Resolve compiled dependency IDs, including child-resource name segments."""
    values = {
        key: spec["defaultValue"]
        for key, spec in template["parameters"].items()
        if "defaultValue" in spec
    } | {"name": "fixture", "location": "uksouth", "consumerPrincipalId": "synthetic-api"}
    variables = template.get("variables", {})
    context = {"guid": lambda *parts: "|".join(parts)}
    by_id = {
        f"/fixture/{item['type']}/{evaluate(item['name'], values, variables, context)}": item
        for item in template["resources"]
    }
    guard_id = f"/fixture/Microsoft.Resources/deployments/{guard_name}"

    def waits(identifier: str, seen: frozenset) -> bool:
        if identifier == guard_id:
            return True
        if identifier in seen or identifier not in by_id:
            return False
        return any(
            waits(evaluate(dep, values, variables, context), seen | {identifier})
            for dep in by_id[identifier].get("dependsOn", [])
        )

    return {
        item["name"]
        for identifier, item in by_id.items()
        if identifier != guard_id and not waits(identifier, frozenset())
    }


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

    def assert_staff_initializer_relay_selection(self, template: dict) -> None:
        self.assertEqual(template["parameters"]["includeResultBlob"]["defaultValue"], False)
        items = list(resources(template))
        self.assertEqual(len(items), 4)
        self.assertEqual(
            {item["type"] for item in items},
            {"Microsoft.Authorization/roleDefinitions", "Microsoft.Authorization/roleAssignments"},
        )
        matrix = json.loads((INFRA / "role-assignments.json").read_text())["customRoles"]
        for role in matrix:
            definition = next(
                item
                for item in items
                if item["type"] == "Microsoft.Authorization/roleDefinitions"
                and role["name"] in item["name"]
            )
            assignment = next(
                item
                for item in items
                if item["type"] == "Microsoft.Authorization/roleAssignments"
                and role["name"] in item["properties"]["roleDefinitionId"]
            )
            self.assertEqual(
                definition["properties"]["permissions"],
                [
                    {
                        "actions": role["actions"],
                        "notActions": [],
                        "dataActions": role.get("dataActions", []),
                        "notDataActions": [],
                    }
                ],
            )
            self.assertEqual(definition["properties"]["assignableScopes"], ["[resourceGroup().id]"])
            self.assertEqual(
                assignment["properties"]["principalId"],
                "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', "
                "parameters('initializerIdentityName')), '2023-01-31').principalId]",
            )
            self.assertEqual(assignment["properties"]["principalType"], "ServicePrincipal")
            if role["name"] == "staff-initializer-result-blob-write":
                self.assertEqual(definition.get("condition"), "[parameters('includeResultBlob')]")
                self.assertEqual(assignment.get("condition"), "[parameters('includeResultBlob')]")
                self.assertIn("staff-results", json.dumps(assignment["scope"]))
            else:
                self.assertNotIn("condition", definition)
                self.assertNotIn("condition", assignment)
                self.assertEqual(
                    assignment["scope"],
                    "[resourceId('Microsoft.App/containerApps', parameters('apiName'))]",
                )
        for enabled, count in ((True, 4), (False, 2)):
            active = [
                item
                for item in items
                if evaluate(item.get("condition", True), {"includeResultBlob": enabled}, {})
            ]
            self.assertEqual(len(active), count)
            if not enabled:
                self.assertTrue(
                    all("staff-initializer-api-restart" in item["name"] for item in active)
                )

    def test_staff_initializer_compiled_relay_selection(self) -> None:
        self.assert_staff_initializer_relay_selection(compile_bicep("staff-initializer-rbac.bicep"))

    def test_staff_initializer_relay_condition_mutations_are_rejected(self) -> None:
        template = compile_bicep("staff-initializer-rbac.bicep")
        for index, item in enumerate(template["resources"]):
            if "condition" not in item:
                continue
            with self.subTest(resource=item["type"]):
                mutated = deepcopy(template)
                del mutated["resources"][index]["condition"]
                self.assert_mutation_rejected(
                    self.assert_staff_initializer_relay_selection, mutated
                )
        mutated = deepcopy(template)
        mutated["parameters"]["includeResultBlob"]["defaultValue"] = True
        self.assert_mutation_rejected(self.assert_staff_initializer_relay_selection, mutated)

    def test_every_deployed_resource_waits_for_the_guard(self) -> None:
        self.assertEqual(unguarded_resources(self.main, "parameter-guard"), set())
        self.assertEqual(module(self.main, "parameter-guard").get("dependsOn", []), [])

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
        for name, parameter in (
            ("api", "apiImage"),
            ("agents", "agentImage"),
            ("orchestrator", "orchestratorImage"),
            ("import", "importImage"),
            ("auth-renewal", "orchestratorImage"),
            ("ledger-verify", "orchestratorImage"),
        ):
            with self.subTest(container=name):
                self.assertEqual(containers[name]["image"], f"[parameters('{parameter}')]")
        self.assertEqual(len(containers), 6)
        for name, module, args in (
            ("auth-renewal", "token_store", []),
            ("ledger-verify", "digest_blob", ["--publish"]),
        ):
            self.assertEqual(containers[name]["image"], "[parameters('orchestratorImage')]")
            self.assertEqual(
                containers[name]["command"],
                [
                    "python",
                    "-m",
                    f"zava_forward.orchestrator.{module}",
                    *args,
                ],
            )

    def test_api_minimum_replicas_parameter_contract(self) -> None:
        apps = module_template(self.main, "containerapps")
        standalone = compile_bicep("modules/containerapps.bicep")
        for name, template in (("main", self.main), ("nested", apps), ("module", standalone)):
            with self.subTest(template=name):
                parameter = template["parameters"]["apiMinReplicas"]
                self.assertEqual(parameter["type"], "int")
                self.assertEqual(parameter["defaultValue"], 0)
                self.assertEqual(parameter["minValue"], 0)
                self.assertEqual(parameter["maxValue"], 4)
                self.assertIn("cost-safe demos", parameter["metadata"]["description"])
                self.assertIn("set 2 explicitly", parameter["metadata"]["description"])
        forwarded = module(self.main, "containerapps")["properties"]["parameters"]["apiMinReplicas"]
        self.assertEqual(forwarded["value"], "[parameters('apiMinReplicas')]")
        for template in (apps, standalone):
            api = next(
                r
                for r in resources(template)
                if r["type"] == "Microsoft.App/containerApps"
                and r["properties"]["template"]["containers"][0]["name"] == "api"
            )
            scale = api["properties"]["template"]["scale"]
            for minimum in (self.defaults["apiMinReplicas"], 1, 2, 4):
                with self.subTest(minimum=minimum, template=template is standalone):
                    passed = evaluate(forwarded["value"], {"apiMinReplicas": minimum}, {})
                    self.assertEqual(
                        evaluate(scale["minReplicas"], {"apiMinReplicas": passed}, {}),
                        minimum,
                    )

    def test_employee_model_defaults_and_scalar_overrides(self) -> None:
        default = evaluate(
            self.main["parameters"]["modelDeployments"]["defaultValue"], self.defaults, {}
        )
        self.assertEqual(
            default,
            [
                {
                    "name": "standard",
                    "model": "gpt-4.1-nano",
                    "version": "2025-04-14",
                    "skuName": "GlobalStandard",
                    "capacity": 1,
                }
            ],
        )
        overrides = {
            "chatModelName": "gpt-4.1-mini",
            "chatModelVersion": "2025-04-14",
            "chatModelSku": "Standard",
            "chatModelCapacity": 2,
        }
        selected = evaluate(
            self.main["parameters"]["modelDeployments"]["defaultValue"],
            self.defaults | overrides,
            {},
        )
        self.assertEqual(
            selected,
            [
                {
                    "name": "standard",
                    "model": "gpt-4.1-mini",
                    "version": "2025-04-14",
                    "skuName": "Standard",
                    "capacity": 2,
                }
            ],
        )
        self.assert_employee_ai_binding(self.main, default)
        self.assert_employee_ai_binding(self.main, selected)

    def test_employee_model_parameter_constraints(self) -> None:
        self.assertEqual(self.main["parameters"]["chatModelCapacity"]["minValue"], 1)
        self.assertEqual(
            self.main["parameters"]["chatModelSku"]["allowedValues"],
            ["GlobalStandard", "Standard"],
        )
        self.assertEqual(self.main["parameters"]["modelDeployments"]["minLength"], 1)
        foundry = module_template(self.main, "foundry")
        self.assertEqual(foundry["parameters"]["deployments"]["minLength"], 1)
        self.assertIs(self.main["parameters"]["enableApiAi"]["defaultValue"], False)
        self.assertIs(
            module_template(self.main, "containerapps")["parameters"]["enableApiAi"][
                "defaultValue"
            ],
            False,
        )

    def assert_employee_ai_binding(self, template: dict, deployments: list[dict]) -> None:
        foundry = module_template(template, "foundry")
        forwarded = module(template, "foundry")["properties"]["parameters"]["deployments"]
        self.assertEqual(
            evaluate(forwarded["value"], {"modelDeployments": deployments}, {}), deployments
        )
        model = resource(foundry, "Microsoft.CognitiveServices/accounts/deployments")
        parameters = {
            "name": "synthetic-account",
            "deployments": [SimpleNamespace(**row) for row in deployments],
        }
        self.assertEqual(evaluate(model["copy"]["count"], parameters, {}), len(deployments))
        context: dict[str, Any]
        for index, row in enumerate(deployments):
            context = {"copyIndex": lambda index=index: index}
            self.assertEqual(
                evaluate(model["name"], parameters, {}, context),
                f"synthetic-account/{row['name']}",
            )
            self.assertEqual(
                evaluate(model["sku"], parameters, {}, context),
                {"name": row["skuName"], "capacity": row["capacity"]},
            )
            self.assertEqual(
                evaluate(model["properties"], parameters, {}, context),
                {
                    "model": {
                        "format": "OpenAI",
                        "name": row["model"],
                        "version": row["version"],
                    },
                    "versionUpgradeOption": "NoAutoUpgrade",
                    "raiPolicyName": "Microsoft.DefaultV2",
                },
            )
        endpoint = "https://synthetic-account.openai.azure.com/"
        account = SimpleNamespace(
            endpoint="https://synthetic-account.cognitiveservices.azure.com/",
            endpoints={"OpenAI Language Model Instance API": endpoint},
        )
        context = {
            "greater": lambda left, right: left > right,
            "reference": lambda identifier, version: account,
        }
        output_values = {
            key: evaluate(foundry["outputs"][key]["value"], parameters, {}, context)
            for key in ("openAiEndpoint", "modelDeploymentNames", "modelVersions")
        }
        outputs = SimpleNamespace(
            **{
                key: SimpleNamespace(
                    value=SimpleNamespace(**value) if isinstance(value, dict) else value
                )
                for key, value in output_values.items()
            }
        )
        context["reference"] = lambda identifier, version: SimpleNamespace(outputs=outputs)
        app_parameters = module(template, "containerapps")["properties"]["parameters"]
        bindings = {
            key: evaluate(app_parameters[key]["value"], {}, {}, context) for key in output_values
        }
        apps = module_template(template, "containerapps")
        api = resource(apps, "Microsoft.App/containerApps")
        env = api["properties"]["template"]["containers"][0]["env"]
        values = {
            name: spec.get("defaultValue", "") for name, spec in apps["parameters"].items()
        } | bindings
        values["identityClientIds"] = SimpleNamespace(api="synthetic-api-client")
        context = {
            "tenant": lambda: SimpleNamespace(tenantId="synthetic-tenant"),
            "environment": lambda: SimpleNamespace(
                suffixes=SimpleNamespace(storage="core.windows.net")
            ),
            "string": json.dumps,
        }
        first, capable = deployments[0], deployments[1] if len(deployments) > 1 else deployments[0]
        expected = {
            "AI_ENDPOINT": endpoint,
            "AI_DEPLOYMENT": first["name"],
            "AI_DEPLOYMENT_STRONG": capable["name"],
            "AI_MODEL_VERSION": f"{first['model']}-{first['version']}",
            "AI_MODEL_VERSION_STRONG": f"{capable['model']}-{capable['version']}",
        }
        for enabled in (False, True):
            actual = {
                row["name"]: row["value"]
                for row in evaluate(
                    env, values | {"enableApiAi": enabled}, apps["variables"], context
                )
            }
            self.assertEqual(
                {key: value for key, value in actual.items() if key.startswith("AI_")},
                expected if enabled else {},
            )
            self.assertEqual(actual["AZURE_CLIENT_ID"], "synthetic-api-client")

    def test_employee_single_and_two_model_override_bindings(self) -> None:
        rows = [
            {
                "name": "custom-small",
                "model": "gpt-4o-mini",
                "version": "2024-07-18",
                "skuName": "GlobalStandard",
                "capacity": 1,
            },
            {
                "name": "custom-strong",
                "model": "gpt-4.1",
                "version": "2025-04-14",
                "skuName": "Standard",
                "capacity": 3,
            },
        ]
        for deployments in (rows[:1], rows):
            self.assert_employee_ai_binding(self.main, deployments)

    def test_employee_binding_and_opt_in_mutations_are_rejected(self) -> None:
        deployments = evaluate(
            self.main["parameters"]["modelDeployments"]["defaultValue"], self.defaults, {}
        )
        for target in ("capable", "opt-in"):
            mutated = deepcopy(self.main)
            if target == "capable":
                module_template(mutated, "foundry")["outputs"]["modelDeploymentNames"]["value"][
                    "capable"
                ] = "nonexistent-capable"
            else:
                api = resource(
                    module_template(mutated, "containerapps"), "Microsoft.App/containerApps"
                )
                container = api["properties"]["template"]["containers"][0]
                container["env"] = container["env"].replace(
                    "if(parameters('enableApiAi'),", "if(true(),"
                )
            with self.subTest(mutation=target), self.assertRaises(AssertionError):
                self.assert_employee_ai_binding(mutated, deployments)

    def test_parameter_examples_keep_api_scaled_to_zero(self) -> None:
        for name in (
            "main.bicepparam",
            "main.test.bicepparam",
            "main.pilot.example.bicepparam",
        ):
            with self.subTest(parameters=name):
                result = subprocess.run(
                    ["az", "bicep", "build-params", "--file", str(INFRA / name), "--stdout"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                compiled = json.loads(json.loads(result.stdout)["parametersJson"])
                self.assertEqual(compiled["parameters"]["apiMinReplicas"]["value"], 0)

    def test_chat_privacy_env_wiring_is_conditional_and_api_only(self) -> None:
        apps = module_template(self.main, "containerapps")
        for template in (apps, self.main):
            for name in ("chatDpiaRef", "chatLawfulBasisRef", "chatNoticeRef", "chatRetentionRef"):
                self.assertEqual(template["parameters"][name]["defaultValue"], "")
            self.assertEqual(template["parameters"]["chatRetentionDays"]["defaultValue"], 0)
        containers = {
            r["properties"]["template"]["containers"][0]["name"]: r
            for r in resources(apps)
            if r["type"] == "Microsoft.App/containerApps"
        }
        api_env = json.dumps(containers["api"]["properties"]["template"]["containers"][0]["env"])
        self.assertIn("if(not(variables('chatEnabled')), createArray(), createArray(", api_env)
        for name in (
            "CHAT_DPIA_REF",
            "CHAT_LAWFUL_BASIS_REF",
            "CHAT_NOTICE_REF",
            "CHAT_RETENTION_REF",
            "CHAT_RETENTION_DAYS",
        ):
            self.assertEqual(api_env.count(f"createObject('name', '{name}'"), 1)
        self.assertNotIn("CHAT_", json.dumps(containers["agents"]["properties"]["template"]))
        self.assertEqual(
            containers["api"]["properties"]["template"]["scale"]["minReplicas"],
            "[parameters('apiMinReplicas')]",
        )

    def test_test_parameters_record_demo_chat_privacy_refs(self) -> None:
        result = subprocess.run(
            [
                "az",
                "bicep",
                "build-params",
                "--file",
                str(INFRA / "main.test.bicepparam"),
                "--stdout",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        compiled = json.loads(json.loads(result.stdout)["parametersJson"])
        chat = {k: v["value"] for k, v in compiled["parameters"].items() if k.startswith("chat")}
        self.assertEqual(chat["chatRetentionDays"], 30)
        record = INFRA.parent / "docs/reference/research/chat-demo-storage-approval-2026-11-01.md"
        text = record.read_text()
        for key, heading in (
            ("chatLawfulBasisRef", "Lawful basis"),
            ("chatNoticeRef", "Notice"),
            ("chatRetentionRef", "Retention"),
        ):
            path, _, anchor = chat[key].partition("#")
            self.assertEqual(path, "docs/reference/research/" + record.name)
            self.assertEqual(anchor, heading.lower().replace(" ", "-"))
            self.assertIn(f"\n## {heading}\n", text)
        self.assertTrue((INFRA.parent / chat["chatDpiaRef"]).is_file())
        self.assertEqual(compiled["parameters"]["apiMinReplicas"]["value"], 0)
        for name in ("main.bicepparam", "main.pilot.example.bicepparam"):
            self.assertNotIn("chat", (INFRA / name).read_text().lower())

    def test_api_replicas_probes_and_private_edge_contract(self) -> None:
        apps = module_template(self.main, "containerapps")
        api = next(r for r in resources(apps) if r["type"] == "Microsoft.App/containerApps")
        template = api["properties"]["template"]
        self.assertEqual(template["scale"]["minReplicas"], "[parameters('apiMinReplicas')]")
        self.assertEqual(template["scale"]["maxReplicas"], 4)
        self.assertEqual(
            template["scale"]["rules"],
            [{"name": "http", "http": {"metadata": {"concurrentRequests": "50"}}}],
        )
        agents = next(
            r
            for r in resources(apps)
            if r["type"] == "Microsoft.App/containerApps"
            and r["properties"]["template"]["containers"][0]["name"] == "agents"
        )
        self.assertEqual(agents["properties"]["template"]["scale"]["minReplicas"], 0)
        self.assertEqual(agents["properties"]["template"]["scale"]["maxReplicas"], 5)
        self.assertEqual(
            template["containers"][0]["probes"],
            [
                {
                    "type": "Startup",
                    "httpGet": {"path": "/healthz", "port": 8088},
                    "periodSeconds": 5,
                    "failureThreshold": 24,
                },
                {"type": "Liveness", "httpGet": {"path": "/healthz", "port": 8088}},
                {"type": "Readiness", "httpGet": {"path": "/healthz", "port": 8088}},
            ],
        )
        self.assert_hosting_limits_and_rollout(apps)
        self.assertFalse(self.defaults["enablePublicEdge"])
        edge = module(self.main, "edge")
        self.assertEqual(edge["condition"], "[parameters('enablePublicEdge')]")
        compiled = edge["properties"]["template"]
        profile = resource(compiled, "Microsoft.Cdn/profiles")
        waf = resource(compiled, "Microsoft.Network/FrontDoorWebApplicationFirewallPolicies")
        self.assertEqual(profile["sku"]["name"], "Premium_AzureFrontDoor")
        self.assertEqual(waf["sku"]["name"], "Premium_AzureFrontDoor")
        self.assertEqual(waf["properties"]["policySettings"]["enabledState"], "Enabled")
        self.assertEqual(compiled["parameters"]["wafMode"]["defaultValue"], "Prevention")
        origin = resource(compiled, "Microsoft.Cdn/profiles/originGroups/origins")
        self.assertEqual(
            origin["properties"]["sharedPrivateLinkResource"]["groupId"], "managedEnvironments"
        )
        self.assertEqual(
            origin["properties"]["sharedPrivateLinkResource"]["privateLink"],
            {"id": "[parameters('environmentId')]"},
        )
        policy = resource(compiled, "Microsoft.Cdn/profiles/securityPolicies")
        self.assertEqual(
            policy["properties"]["parameters"]["wafPolicy"]["id"],
            "[resourceId('Microsoft.Network/FrontDoorWebApplicationFirewallPolicies', "
            "variables('wafName'))]",
        )
        route = resource(compiled, "Microsoft.Cdn/profiles/afdEndpoints/routes")
        self.assertEqual(route["properties"]["supportedProtocols"], ["Https"])
        self.assertEqual(route["properties"]["forwardingProtocol"], "HttpsOnly")

    def assert_hosting_limits_and_rollout(self, apps: dict) -> None:
        """Resource limits, single active revision and queue scale rules for every app."""
        by_name = {
            r["properties"]["template"]["containers"][0]["name"]: r["properties"]
            for r in resources(apps)
            if r["type"] == "Microsoft.App/containerApps"
        }
        for name, cpu, memory in (("api", "0.5", "1Gi"), ("agents", "0.5", "1Gi")):
            with self.subTest(app=name):
                limits = by_name[name]["template"]["containers"][0]["resources"]
                self.assertEqual(limits, {"cpu": f"[json('{cpu}')]", "memory": memory})
                # Single mode: rollback is a reviewed revert and release, not a traffic split.
                self.assertEqual(by_name[name]["configuration"]["activeRevisionsMode"], "Single")
        rule = by_name["agents"]["template"]["scale"]["rules"][0]
        self.assertEqual(rule["name"], "agent-task-queue")
        self.assertEqual(rule["custom"]["type"], "azure-queue")
        self.assertEqual(rule["custom"]["metadata"]["queueName"], "agent-tasks")
        self.assertEqual(rule["custom"]["metadata"]["queueLength"], "5")
        jobs = {
            r["properties"]["template"]["containers"][0]["name"]: r["properties"]["configuration"]
            for r in resources(apps)
            if r["type"] == "Microsoft.App/jobs"
        }
        self.assertEqual(jobs["import"]["eventTriggerConfig"]["scale"]["maxExecutions"], 2)
        self.assertEqual(jobs["import"]["eventTriggerConfig"]["scale"]["minExecutions"], 0)
        for name in ("orchestrator", "ledger-verify", "auth-renewal"):
            with self.subTest(job=name):
                self.assertEqual(jobs[name]["scheduleTriggerConfig"]["parallelism"], 1)
                self.assertGreater(jobs[name]["replicaTimeout"], 0)

    def test_defender_opt_in_does_not_downgrade_existing_subscription_plans(self) -> None:
        governance = compile_bicep("governance.bicep")
        self.assertFalse(governance["parameters"]["enableDefenderPlans"]["defaultValue"])
        pricing = resource(governance, "Microsoft.Security/pricings")
        self.assertEqual(pricing["condition"], "[parameters('enableDefenderPlans')]")
        self.assertEqual(pricing["properties"]["pricingTier"], "Standard")
        self.assertEqual(
            governance["parameters"]["defenderPlans"]["defaultValue"],
            ["StorageAccounts", "SqlServers", "KeyVaults", "Containers"],
        )
        self.assertEqual(
            governance["parameters"]["enforcementMode"]["defaultValue"], "DoNotEnforce"
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
                    expected.add("primaryLocationMustBeUKSouth")
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
                    "tags": {
                        "environment": "wrong",
                        "owner": "wrong",
                        "extra": "retained",
                        "zava-forward-deployment-profile": "development",
                    },
                },
                variables,
            ),
            {
                "workload": "zava-forward-demonstrator",
                "environment": "test",
                "zava-forward-deployment-profile": "production",
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
                    expected = (
                        "[if(variables('externalEnvironment'), 'Enabled', 'Disabled')]"
                        if name == "containerapps"
                        else PUBLIC
                    )
                    self.assertEqual(matches[0]["properties"].get(prop), expected, f"{name}.{prop}")
        environment = resource(
            module_template(template, "containerapps"), "Microsoft.App/managedEnvironments"
        )
        self.assertEqual(
            environment["properties"]["vnetConfiguration"].get("internal"),
            "[not(variables('externalEnvironment'))]",
        )
        self.assertEqual(
            module_template(template, "containerapps")["variables"]["externalEnvironment"],
            "[or(parameters('demoDirectIngress'), parameters('allowPublicNetworkAccess'))]",
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

    def assert_demo_guard_controls(self, template: dict) -> None:
        passed = module(template, "parameter-guard")["properties"]["parameters"]
        defaults = {
            name: spec["defaultValue"]
            for name, spec in template["parameters"].items()
            if "defaultValue" in spec
        }
        for demo, profile, edge, public, apps, env_only, audience, bearer in product(
            (False, True),
            ("development", "production"),
            (False, True),
            (False, True),
            (False, True),
            (False, True),
            ("", "synthetic-audience"),
            (False, True),
        ):
            values = {
                **defaults,
                "demoDirectIngress": demo,
                "deploymentProfile": profile,
                "enablePublicEdge": edge,
                "allowPublicNetworkAccess": public,
                "deployApplications": apps,
                "deployEnvironmentOnly": env_only,
                "entraClientId": audience,
                "entraBearerOnly": bearer,
                "regionCheckReference": "synthetic-region-check",
                "quotaCheckReference": "synthetic-quota-check",
                "location": "uksouth",
                "sqlLocation": "offline-region",
            }
            expected = set()
            if demo:
                if profile != "development":
                    expected.add("demoRequiresDevelopmentProfile")
                if edge:
                    expected.add("demoForbidsPublicEdge")
                if public:
                    expected.add("demoRequiresPrivateBackingServices")
                if apps and (not audience or bearer):
                    expected.add("demoRequiresBrowserAuthentication")
            if profile == "production" and public:
                expected.add("productionProfileForbidsPublicNetworkAccess")
            if edge and (profile != "production" or public):
                expected.add("publicEdgeRequiresProductionProfile")
            if edge and not apps:
                expected.add("publicEdgeRequiresApplications")
            if bearer and not audience:
                expected.add("bearerOnlyRequiresAudience")
            actual = {
                name
                for name, expression in passed.items()
                if not evaluate(expression, values, template["variables"])["value"]
            }
            self.assertEqual(actual, expected, str(values))
        for name in (
            "demoRequiresDevelopmentProfile",
            "demoForbidsPublicEdge",
            "demoRequiresPrivateBackingServices",
            "demoRequiresBrowserAuthentication",
        ):
            self.assertEqual(self.guard["parameters"][name]["minLength"], 1)

    def test_demo_guard_matrix_including_environment_only_staging(self) -> None:
        self.assertIs(self.defaults["demoDirectIngress"], False)
        self.assertIs(self.defaults["deployBackgroundWorkloads"], True)
        self.assert_demo_guard_controls(self.main)

    def test_demo_guard_bypass_mutations_are_rejected(self) -> None:
        for name in (
            "demoRequiresDevelopmentProfile",
            "demoForbidsPublicEdge",
            "demoRequiresPrivateBackingServices",
            "demoRequiresBrowserAuthentication",
        ):
            with self.subTest(guard=name):
                mutated = deepcopy(self.main)
                module(mutated, "parameter-guard")["properties"]["parameters"][name] = {
                    "value": "ok"
                }
                self.assert_mutation_rejected(self.assert_demo_guard_controls, mutated)

    def test_demo_mode_is_external_with_no_internal_dns_and_direct_auth(self) -> None:
        apps = module(self.main, "containerapps")
        passed = apps["properties"]["parameters"]
        template = apps["properties"]["template"]
        environment = resource(template, "Microsoft.App/managedEnvironments")
        dns = next(
            r for r in template["resources"] if r["type"] == "Microsoft.Resources/deployments"
        )
        api = resource(template, "Microsoft.App/containerApps")
        auth = resource(template, "Microsoft.App/containerApps/authConfigs")
        for demo, public, edge in product((False, True), repeat=3):
            values = {
                **self.defaults,
                "demoDirectIngress": demo,
                "allowPublicNetworkAccess": public,
                "deploymentProfile": "development" if public or demo else "production",
                "enablePublicEdge": edge,
                "entraClientId": "synthetic-audience",
            }
            nested = {
                **values,
                **{
                    name: evaluate(passed[name], values, self.main["variables"])["value"]
                    for name in (
                        "demoDirectIngress",
                        "allowPublicNetworkAccess",
                        "behindPublicEdge",
                    )
                },
            }
            variables = template["variables"]
            self.assertEqual(
                evaluate(environment["properties"]["publicNetworkAccess"], nested, variables),
                "Enabled" if demo or public else "Disabled",
            )
            self.assertEqual(
                evaluate(
                    environment["properties"]["vnetConfiguration"]["internal"], nested, variables
                ),
                not (demo or public),
            )
            self.assertEqual(evaluate(dns["condition"], nested, variables), not (demo or public))
            forwarding = evaluate(
                auth["properties"]["httpSettings"]["forwardProxy"], nested, variables
            )
            self.assertEqual(forwarding["convention"], "Custom" if edge else "NoProxy")
            if demo and not edge:
                self.assertFalse(nested["behindPublicEdge"])
                self.assertEqual(
                    evaluate(
                        auth["properties"]["globalValidation"]["unauthenticatedClientAction"],
                        nested,
                        variables,
                    ),
                    "RedirectToLoginPage",
                )
                tags = evaluate(api["tags"], nested, variables)
                self.assertEqual(tags["zava-forward-ingress"], "direct")
                self.assertEqual(tags["zava-forward-role"], "api")
            elif not demo:
                self.assertNotIn("zava-forward-ingress", evaluate(api["tags"], nested, variables))
        self.assertEqual(
            api["properties"]["managedEnvironmentId"],
            "[resourceId('Microsoft.App/managedEnvironments', "
            "format('cae-{0}', parameters('prefix')))]",
        )
        self.assertIs(api["properties"]["configuration"]["ingress"]["external"], True)
        self.assertIs(api["properties"]["configuration"]["ingress"]["allowInsecure"], False)
        self.assertEqual(
            auth["properties"]["identityProviders"]["azureActiveDirectory"]["validation"][
                "allowedAudiences"
            ],
            "[if(parameters('entraBearerOnly'), createArray(parameters('entraClientId'), "
            "format('api://{0}', parameters('entraClientId'))), "
            "createArray(format('api://{0}', parameters('entraClientId'))))]",
        )

    def test_demo_preserves_private_backing_services_names_and_identity_inputs(self) -> None:
        demo = {
            **self.defaults,
            "demoDirectIngress": True,
            "deploymentProfile": "development",
            "entraClientId": "synthetic-audience",
        }
        self.assertFalse(
            evaluate(self.main["variables"]["publicAccess"], demo, self.main["variables"])
        )
        for name, kinds in NETWORK_RESOURCES.items():
            if name == "containerapps":
                continue
            passed = module(self.main, name)["properties"]["parameters"]
            nested = module_template(self.main, name)
            public = evaluate(passed["allowPublicNetworkAccess"], demo, self.main["variables"])[
                "value"
            ]
            self.assertIs(public, False, name)
            for kind, properties in kinds.items():
                item = resource(nested, kind)
                for prop in properties:
                    self.assertEqual(
                        evaluate(
                            item["properties"][prop], {"allowPublicNetworkAccess": public}, {}
                        ),
                        "Disabled",
                        f"{name}.{prop}",
                    )
        self.assertEqual(
            resource(module_template(self.main, "sql"), "Microsoft.Sql/servers")["properties"][
                "publicNetworkAccess"
            ],
            "Disabled",
        )
        for item in self.main["resources"]:
            if item["type"] != "Microsoft.Resources/deployments" or item["name"] == "containerapps":
                continue
            passed = item["properties"]["parameters"]
            for key in ("name", "prefix"):
                if key not in passed:
                    continue
                # Stable fixture avoids evaluating Azure's resourceGroup()/uniqueString().
                variables = {**self.main["variables"], "unique": "fixed"}
                self.assertEqual(
                    evaluate(passed[key], demo, variables),
                    evaluate(passed[key], {**demo, "demoDirectIngress": False}, variables),
                    f"{item['name']}.{key}",
                )
        passed = module(self.main, "containerapps")["properties"]["parameters"]
        for name in ("identityIds", "identityClientIds"):
            output = "ids" if name == "identityIds" else "clientIds"
            self.assertEqual(
                passed[name]["value"],
                f"[reference(resourceId('Microsoft.Resources/deployments', 'identity'), "
                f"'2025-04-01').outputs.{output}.value]",
            )
        self.assert_endpoint_controls(self.main)
        self.assert_key_controls(self.main)

    def test_demo_names_are_workload_only_and_reuse_existing_uamis(self) -> None:
        apps = module_template(self.main, "containerapps")
        naming = module(self.main, "containerapps")["properties"]["parameters"]["prefix"]
        items = [
            r
            for r in apps["resources"]
            if r["type"]
            in (
                "Microsoft.App/managedEnvironments",
                "Microsoft.App/containerApps",
                "Microsoft.App/jobs",
            )
        ]
        original = {
            "cae-forward-dev",
            "ca-forward-dev-api",
            "ca-forward-dev-agents",
            "job-forward-dev-auth-renewal",
            "job-forward-dev-orchestrator",
            "job-forward-dev-ledger-verify",
            "job-forward-dev-import",
        }
        expected = {
            "cae-forward-dev-demo",
            "ca-forward-dev-demo-api",
            "ca-forward-dev-demo-agents",
            "job-forward-dev-demo-auth",
            "job-forward-dev-demo-orch",
            "job-forward-dev-demo-audit",
            "job-forward-dev-demo-load",
        }
        for demo in (False, True):
            values = {**self.defaults, "demoDirectIngress": demo}
            prefix = evaluate(naming, values, self.main["variables"])["value"]
            nested = {
                "prefix": prefix,
                "demoDirectIngress": demo,
                "identityIds": SimpleNamespace(
                    api="existing-api",
                    agents="existing-agents",
                    orchestrator="existing-orchestrator",
                    import_="existing-import",
                ),
                "tokenMaintenanceIdentityId": "existing-token-maintenance",
            }
            actual = {evaluate(item["name"], nested, {}) for item in items}
            self.assertEqual(actual, expected if demo else original)
            for item in items:
                if "identity" not in item:
                    continue
                identity = item["identity"]
                self.assertEqual(identity["type"], "UserAssigned")
                keys = [
                    evaluate(key.replace(".import", ".import_"), nested, {})
                    for key in identity["userAssignedIdentities"]
                ]
                role = item["properties"]["template"]["containers"][0]["name"]
                expected_role = {"auth-renewal": "token-maintenance", "ledger-verify": "api"}.get(
                    role, role
                )
                self.assertEqual(keys, ["existing-" + expected_role])

    def test_demo_names_fit_platform_bounds_and_ledger_alerts_match(self) -> None:
        apps = module_template(self.main, "containerapps")
        naming = module(self.main, "containerapps")["properties"]["parameters"]["prefix"]
        jobs = [item for item in apps["resources"] if item["type"] == "Microsoft.App/jobs"]
        for workload, environment in product(
            ("abc", "forward", "cutover", "abcdefghij"), ("dev", "test", "pilot")
        ):
            with self.subTest(workload=workload, environment=environment):
                values = {
                    **self.defaults,
                    "workload": workload,
                    "environmentName": environment,
                    "demoDirectIngress": True,
                }
                prefix = evaluate(naming, values, self.main["variables"])["value"]
                nested = {"prefix": prefix, "demoDirectIngress": True}
                names = [evaluate(job["name"], nested, {}) for job in jobs]
                self.assertEqual(len(set(names)), 4)
                for name in names:
                    self.assertLess(len(name), 32, name)
                    self.assertRegex(name, r"^[a-z][a-z0-9-]*[a-z0-9]$")
                    self.assertIn("-demo-", name)
                ledger_name = evaluate(
                    self.main["variables"]["ledgerJobName"], values, self.main["variables"]
                )
                self.assertIn(ledger_name, names)
                for item in self.main["resources"]:
                    if item["type"] == "Microsoft.Insights/scheduledQueryRules" and (
                        "ledger-" in item["name"]
                    ):
                        query = item["properties"]["criteria"]["allOf"][0]["query"]
                        self.assertIn(
                            f'JobName startswith "{ledger_name}"',
                            evaluate(query, values, self.main["variables"]),
                        )

    def test_demo_subnet_and_https_nsg_are_conditional_and_non_overlapping(self) -> None:
        template = module_template(self.main, "network")
        passed = module(self.main, "network")["properties"]["parameters"]
        self.assertEqual(
            passed["demoDirectIngress"], {"value": "[parameters('demoDirectIngress')]"}
        )
        defaults = {
            name: spec["defaultValue"]
            for name, spec in template["parameters"].items()
            if "defaultValue" in spec
        }
        defaults["prefix"] = "forward-dev"
        vnet = resource(template, "Microsoft.Network/virtualNetworks")
        demo_nsg = next(r for r in template["resources"] if "-aca-demo" in r["name"])
        before = evaluate(
            vnet["properties"]["subnets"], {**defaults, "demoDirectIngress": False}, {}
        )
        after = evaluate(vnet["properties"]["subnets"], {**defaults, "demoDirectIngress": True}, {})
        self.assertEqual([subnet["name"] for subnet in before], ["snet-aca", "snet-pe"])
        self.assertEqual(after[:2], before)
        self.assertEqual(
            [subnet["name"] for subnet in after], ["snet-aca", "snet-pe", "snet-aca-demo"]
        )
        demo_subnet = after[2]["properties"]
        self.assertEqual(demo_subnet["addressPrefix"], "10.40.6.0/23")
        for old in before:
            self.assertFalse(
                IPv4Network(demo_subnet["addressPrefix"]).overlaps(
                    IPv4Network(old["properties"]["addressPrefix"])
                )
            )
        self.assertTrue(
            IPv4Network(demo_subnet["addressPrefix"]).subnet_of(
                IPv4Network(defaults["vnetAddressPrefix"])
            )
        )
        self.assertEqual(
            demo_subnet["delegations"][0]["properties"]["serviceName"], "Microsoft.App/environments"
        )
        self.assertTrue(
            demo_subnet["networkSecurityGroup"]["id"].endswith("/nsg-forward-dev-aca-demo")
        )
        rules = demo_nsg["properties"]["securityRules"]
        self.assertEqual(
            [rule["properties"]["sourceAddressPrefix"] for rule in rules],
            ["Internet", "VirtualNetwork"],
        )
        internet = [
            rule["properties"]
            for rule in rules
            if rule["properties"]["sourceAddressPrefix"] == "Internet"
        ]
        self.assertEqual(len(internet), 1)
        self.assertEqual(
            {
                key: internet[0][key]
                for key in ("direction", "access", "protocol", "destinationPortRange")
            },
            {
                "direction": "Inbound",
                "access": "Allow",
                "protocol": "Tcp",
                "destinationPortRange": "443",
            },
        )
        for demo in (False, True):
            values = {**defaults, "demoDirectIngress": demo}
            self.assertEqual(evaluate(demo_nsg["condition"], values, {}), demo)
            output = evaluate(template["outputs"]["demoAcaSubnetId"]["value"], values, {})
            self.assertEqual(output.endswith("/vnet-forward-dev/snet-aca-demo"), demo)
        old_nsg = next(
            r
            for r in template["resources"]
            if r["name"] == "[format('nsg-{0}-aca', parameters('prefix'))]"
        )
        self.assertNotIn("condition", old_nsg)
        self.assertEqual(
            [
                r["properties"]["sourceAddressPrefix"]
                for r in old_nsg["properties"]["securityRules"]
            ],
            ["AzureFrontDoor.Backend", "VirtualNetwork"],
        )
        subnet_input = module(self.main, "containerapps")["properties"]["parameters"][
            "infrastructureSubnetId"
        ]
        if isinstance(subnet_input, dict):
            subnet_input = "[createObject('value', " + subnet_input["value"][1:-1] + ")]"
        for demo in (False, True):
            expression = subnet_input
            for output in ("acaSubnetId", "demoAcaSubnetId"):
                expression = expression.replace(
                    "reference(resourceId('Microsoft.Resources/deployments', 'network'), "
                    f"'2025-04-01').outputs.{output}.value",
                    f"parameters('{output}')",
                )
            self.assertEqual(
                evaluate(
                    expression,
                    {
                        "demoDirectIngress": demo,
                        "acaSubnetId": "old-subnet",
                        "demoAcaSubnetId": "demo-subnet",
                    },
                    {},
                )["value"],
                "demo-subnet" if demo else "old-subnet",
            )

    def assert_background_staging_controls(self, main: dict) -> None:
        module_resource = module(main, "containerapps")
        passed = module_resource["properties"]["parameters"]
        template = module_resource["properties"]["template"]
        self.assertEqual(
            passed["deployBackgroundWorkloads"],
            {"value": "[parameters('deployBackgroundWorkloads')]"},
        )
        self.assertIs(template["parameters"]["deployBackgroundWorkloads"]["defaultValue"], True)
        consumers = [
            item
            for item in template["resources"]
            if item["type"] in ("Microsoft.App/containerApps", "Microsoft.App/jobs")
        ]
        self.assertEqual(len(consumers), 6)
        for demo, apps, env_only, background, maintenance in product((False, True), repeat=5):
            values = {
                **self.defaults,
                "demoDirectIngress": demo,
                "deployApplications": apps,
                "deployEnvironmentOnly": env_only,
                "deployBackgroundWorkloads": background,
            }
            nested = {
                "deployWorkloads": evaluate(passed["deployWorkloads"], values, main["variables"])[
                    "value"
                ],
                "deployBackgroundWorkloads": evaluate(
                    passed["deployBackgroundWorkloads"], values, main["variables"]
                )["value"],
                "tokenMaintenanceIdentityId": "existing-token-maintenance" if maintenance else "",
                "prefix": "fixture",
                "demoDirectIngress": demo,
            }
            self.assertEqual(
                evaluate(module_resource["condition"], values, main["variables"]), apps or env_only
            )
            for item in consumers:
                name = evaluate(item["name"], nested, {})
                expected = apps and (name.endswith("-api") or background)
                if item["properties"]["template"]["containers"][0]["name"] == "auth-renewal":
                    expected = expected and maintenance
                self.assertEqual(
                    evaluate(item["condition"], nested, template["variables"]), expected, name
                )
            job = evaluate(template["outputs"]["ledgerVerifyJobName"]["value"], nested, {})
            expected_job = "job-fixture-audit" if demo else "job-fixture-ledger-verify"
            self.assertEqual(job, expected_job if apps and background else "")
            for alert in main["resources"]:
                if (
                    alert["type"] == "Microsoft.Insights/scheduledQueryRules"
                    and "ledger-" in alert["name"]
                ):
                    self.assertEqual(
                        evaluate(alert["condition"], values, main["variables"]), apps and background
                    )

    def test_api_only_staging_omits_all_background_consumers(self) -> None:
        self.assert_background_staging_controls(self.main)

    def test_staging_rejects_background_condition_bypass_mutations(self) -> None:
        template = module_template(self.main, "containerapps")
        for item in template["resources"]:
            if (
                item["type"] not in ("Microsoft.App/jobs", "Microsoft.App/containerApps")
                or "-api" in item["name"]
            ):
                continue
            with self.subTest(resource=item["name"]):
                mutated = deepcopy(self.main)
                target = next(
                    r
                    for r in module_template(mutated, "containerapps")["resources"]
                    if r["name"] == item["name"]
                )
                target["condition"] = "[parameters('deployWorkloads')]"
                self.assert_mutation_rejected(self.assert_background_staging_controls, mutated)

    def test_bearer_only_keeps_validation_and_omits_browser_secret(self) -> None:
        template = module_template(self.main, "containerapps")
        self.assertEqual(
            template["parameters"]["entraClientSecretName"]["defaultValue"], "entra-client-secret"
        )
        apps = module(self.main, "containerapps")["properties"]["parameters"]
        self.assertEqual(
            apps["entraClientSecretName"]["value"], "[parameters('entraClientSecretName')]"
        )
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
            "[if(parameters('entraBearerOnly'), null(), parameters('entraClientSecretName'))]",
        )
        self.assertIn("parameters('entraClientId')", aad["validation"]["allowedAudiences"])
        api = resource(template, "Microsoft.App/containerApps")
        self.assertIn(
            "not(parameters('entraBearerOnly'))", api["properties"]["configuration"]["secrets"]
        )
        self.assertIn(
            "parameters('entraClientSecretName')", api["properties"]["configuration"]["secrets"]
        )

    def test_existing_stack_edge_is_additive_and_single_origin(self) -> None:
        template = compile_bicep("public-edge-existing.bicep")
        self.assertEqual(
            {item["name"] for item in template["resources"]},
            {"edge-existing-guard", "edge-existing-auth", "public-edge-existing"},
        )
        guards = module(template, "edge-existing-guard")["properties"]
        private_guard = json.dumps(guards["parameters"]["privateEnvironment"])
        auth_guard = json.dumps(guards["parameters"]["authenticatedOrigin"])
        self.assertIn("'Disabled'", private_guard)
        self.assertIn(".internal", private_guard)
        self.assertIn("managedEnvironmentId", auth_guard)
        self.assertIn("platform.enabled", auth_guard)
        self.assertFalse(template["parameters"]["entraBearerOnly"]["defaultValue"])
        auth_template = module_template(template, "edge-existing-auth")
        browser_auth = resource(auth_template, "Microsoft.App/containerApps/authConfigs")
        self.assertIn("RedirectToLoginPage", browser_auth["properties"])
        for setting in ("'Custom'", "'X-Forwarded-Host'", "'X-Forwarded-Proto'"):
            self.assertIn(setting, browser_auth["properties"])
        self.assertNotIn("'Standard'", browser_auth["properties"])
        edge = module_template(template, "public-edge-existing")
        origins = [
            r for r in resources(edge) if r["type"] == "Microsoft.Cdn/profiles/originGroups/origins"
        ]
        self.assertEqual(len(origins), 1)
        origin = origins[0]["properties"]
        self.assertEqual(origin["hostName"], origin["originHostHeader"])
        self.assertTrue(origin["enforceCertificateNameCheck"])
        self.assertEqual(origin["sharedPrivateLinkResource"]["groupId"], "managedEnvironments")
        route = resource(edge, "Microsoft.Cdn/profiles/afdEndpoints/routes")["properties"]
        self.assertEqual(route["patternsToMatch"], ["/*"])
        self.assertEqual(route["supportedProtocols"], ["Https"])
        self.assertNotIn("cacheConfiguration", route)
        self.assertNotIn("ruleSets", route)
        probe = resource(edge, "Microsoft.Cdn/profiles/originGroups")["properties"][
            "healthProbeSettings"
        ]
        self.assertEqual((probe["probePath"], probe["probeRequestType"]), ("/healthz", "GET"))
        waf = resource(edge, "Microsoft.Network/FrontDoorWebApplicationFirewallPolicies")
        self.assertEqual(waf["properties"]["policySettings"]["mode"], "[parameters('wafMode')]")
        self.assertEqual(
            module(template, "public-edge-existing")["properties"]["parameters"]["wafMode"][
                "value"
            ],
            "Prevention",
        )

    def test_edge_auth_trusts_only_front_door_overwritten_headers(self) -> None:
        template = module_template(self.main, "containerapps")
        auth = resource(template, "Microsoft.App/containerApps/authConfigs")
        expression = auth["properties"]["httpSettings"]["forwardProxy"]
        for behind_edge, expected in (
            (False, {"convention": "NoProxy"}),
            (
                True,
                {
                    "convention": "Custom",
                    "customHostHeaderName": "X-Forwarded-Host",
                    "customProtoHeaderName": "X-Forwarded-Proto",
                },
            ),
        ):
            self.assertEqual(evaluate(expression, {"behindPublicEdge": behind_edge}, {}), expected)

    def assert_existing_edge_client_guard(self, template: dict) -> None:
        guard = module(template, "edge-existing-guard")
        definition = module_template(template, "edge-existing-guard")["parameters"][
            "registeredClient"
        ]
        self.assertEqual(definition["minLength"], 1)
        self.assertIn("python3 infra/scripts/setup-entra.py", definition["metadata"]["description"])
        self.assertIn("edge-existing-guard", module(template, "edge-existing-auth")["dependsOn"][0])
        self.assertIn(
            "edge-existing-auth", module(template, "public-edge-existing")["dependsOn"][0]
        )
        expression = guard["properties"]["parameters"]["registeredClient"]
        client_read = (
            "coalesce(tryGet(reference(resourceId('Microsoft.App/containerApps/authConfigs', "
            "parameters('apiName'), 'current'), '2025-07-01')"
            ".identityProviders.azureActiveDirectory.registration, 'clientId'), '')"
        )
        self.assertIn(client_read, expression)
        expression = expression.replace(client_read, "coalesce(parameters('clientId'), '')")
        valid = "01234567-89ab-cdef-0123-456789abcdef"
        cases: tuple[tuple[str | None, bool], ...] = (
            (None, False),
            ("", False),
            ("systemAssignedIdentity", False),
            ("not-an-application", False),
            (valid, True),
            (valid.upper(), True),
            (valid.replace("-", ""), False),
            ("{" + valid + "}", False),
            (" " + valid[1:], False),
            (valid[:-1] + "g", False),
            (valid[:-1] + "-", False),
            (valid.replace("-", "_"), False),
            (valid[:7] + "-" + valid[8:9] + valid[10:], False),
            (valid + "0", False),
            (valid[:-1], False),
        )
        cases += tuple(
            (valid[:index] + valid[index + 1] + "-" + valid[index + 2 :], False)
            for index in (8, 13, 18, 23)
        )
        for client_id, accepted in cases:
            value = evaluate(expression, {"clientId": client_id}, {})["value"]
            self.assertEqual(len(value) >= definition["minLength"], accepted, repr(client_id))

    def test_existing_edge_requires_uuid_before_auth_or_edge_write(self) -> None:
        self.assert_existing_edge_client_guard(compile_bicep("public-edge-existing.bicep"))

    def test_existing_edge_client_guard_mutations_are_rejected(self) -> None:
        template = compile_bicep("public-edge-existing.bicep")
        for mutation in ("nonempty-only", "always-ok", "constraint-removed", "auth-unordered"):
            with self.subTest(mutation=mutation):
                mutated = deepcopy(template)
                guard = module(mutated, "edge-existing-guard")
                if mutation == "nonempty-only":
                    expression = guard["properties"]["parameters"]["registeredClient"]
                    client = re.search(r"coalesce\(tryGet\(.*?'clientId'\), ''\)", expression)
                    self.assertIsNotNone(client)
                    assert client is not None
                    guard["properties"]["parameters"]["registeredClient"] = (
                        f"[if(not(empty({client.group()})), "
                        "createObject('value', 'ok'), createObject('value', ''))]"
                    )
                elif mutation == "always-ok":
                    guard["properties"]["parameters"]["registeredClient"] = {"value": "ok"}
                elif mutation == "constraint-removed":
                    guard["properties"]["template"]["parameters"]["registeredClient"][
                        "minLength"
                    ] = 0
                else:
                    module(mutated, "edge-existing-auth")["dependsOn"] = ["unrelated"]
                self.assert_mutation_rejected(self.assert_existing_edge_client_guard, mutated)

    def test_bearer_only_guard_requires_identified_audience(self) -> None:
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
                target_kind = (
                    "Microsoft.EventHub/namespaces"
                    if name == "iothub" and group == "namespace"
                    else kind
                )
                target = resource(nested, target_kind)
                self.assertEqual(
                    params.get("targetResourceId"),
                    {"value": f"[resourceId('{target_kind}', {target['name'][1:-1]})]"},
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
                "location": "uksouth",
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
        self.assertEqual(defaults["entraCredentialStore"], "keyvault")
        self.assertEqual(
            failures(
                entraCredentialStore="app",
                demoDirectIngress=True,
                deploymentProfile="development",
                entraClientId="synthetic-client",
            ),
            {"appCredentialBlocksApplicationDeployment"},
        )
        self.assertEqual(
            failures(
                entraCredentialStore="app",
                demoDirectIngress=True,
                deploymentProfile="development",
                entraClientId="synthetic-client",
                deployApplications=False,
            ),
            set(),
        )
        self.assertEqual(failures(regionCheckReference=""), {"regionCheckMustBeRecorded"})
        self.assertEqual(failures(quotaCheckReference=""), {"quotaCheckMustBeRecorded"})
        self.assertEqual(
            failures(regionCheckReference="", quotaCheckReference=""),
            {"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"},
        )
        for name in ("location", "sqlLocation"):
            expected = {"deploymentLocationsMustBeSelected"}
            if name == "location":
                expected.add("primaryLocationMustBeUKSouth")
            self.assertEqual(failures(**{name: ""}), expected)
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
            for environment, locks in product(("dev", "test", "pilot"), (False, True)):
                environment_expected = expected
                if environment == "pilot":
                    environment_expected = pilot_expected | (
                        set() if locks else {"pilotRequiresLocks"}
                    )
                self.assertEqual(
                    failures(**overrides, environmentName=environment, enableLocks=locks),
                    environment_expected,
                    str({**overrides, "environmentName": environment, "enableLocks": locks}),
                )
        self.assertEqual(
            failures(enablePublicEdge=True, deployApplications=False),
            {"publicEdgeRequiresApplications"},
        )
        guard = "serverlessAutoPauseDelayMustBeSupported"
        for tier, delay in product(("serverless", "provisioned"), (-1, 0, 14, 15, 10080, 10081)):
            valid = tier == "provisioned" or delay in (-1, 15, 10080)
            self.assertEqual(
                failures(sqlTier=tier, sqlAutoPauseDelayMinutes=delay),
                set() if valid else {guard},
                f"{tier} {delay}",
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
            "pilotRequiresLocks",
            "serverlessAutoPauseDelayMustBeSupported",
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
