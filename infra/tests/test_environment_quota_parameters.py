"""Deterministic offline verification of environment, region, quota, and recorded checks."""

from __future__ import annotations

import importlib.util
import io
import json
import re
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from copy import deepcopy
from functools import reduce
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest.mock import patch
from uuid import UUID

ROOT = Path(__file__).resolve().parents[2]
INFRA = ROOT / "infra"
ARCH_DOC = ROOT / "docs/architecture/environment-region-quota-strategy.md"
ARCH_INDEX = ROOT / "docs/architecture/README.md"
INFRA_README = INFRA / "README.md"
SYNTHETIC_UUID = str(UUID(int=1))
SECOND_UUID = str(UUID(int=2))


def _load_script(module_name: str, relative_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    assert spec is not None and spec.loader is not None
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


PIPELINE = _load_script("infra_pipeline_137", "infra/scripts/pipeline.py")
DEPLOY = _load_script("infra_deploy_137", "infra/scripts/deploy.py")


def compile_bicep(relative_path: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["az", "bicep", "build", "--file", str(INFRA / relative_path), "--stdout"],
        check=True,
        capture_output=True,
        text=True,
    )
    result: dict[str, Any] = json.loads(completed.stdout)
    return result


def compile_bicepparam(relative_path: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["az", "bicep", "build-params", "--file", str(INFRA / relative_path), "--stdout"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload: dict[str, Any] = json.loads(completed.stdout)
    params_json: dict[str, Any] = json.loads(payload["parametersJson"])
    return {key: entry["value"] for key, entry in params_json["parameters"].items()}


def find_module(template: dict[str, Any], name: str) -> dict[str, Any]:
    resources = template["resources"]
    items = resources.values() if isinstance(resources, dict) else resources
    for item in items:
        if item.get("type") == "Microsoft.Resources/deployments" and item.get("name") == name:
            result: dict[str, Any] = item
            return result
    raise KeyError(f"Deployment module {name!r} not found")


def evaluate_arm(
    expression: Any,
    parameters: dict[str, Any],
    variables: dict[str, Any],
    *,
    rg_name: str = "ama",
    rg_location: str = "uksouth",
) -> Any:
    """Evaluate the deterministic ARM expression subset used in parameter guards."""
    if isinstance(expression, dict):
        return {
            key: evaluate_arm(
                val,
                parameters,
                variables,
                rg_name=rg_name,
                rg_location=rg_location,
            )
            for key, val in expression.items()
        }
    if isinstance(expression, list):
        return [
            evaluate_arm(
                val,
                parameters,
                variables,
                rg_name=rg_name,
                rg_location=rg_location,
            )
            for val in expression
        ]
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
    scope: dict[str, Any] = {
        "if_": lambda cond, left, right: left if cond else right,
        "or_": lambda *args: any(args),
        "and_": lambda *args: all(args),
        "not_": lambda arg: not arg,
        "equals": lambda left, right: left == right,
        "greaterOrEquals": lambda left, right: left >= right,
        "lessOrEquals": lambda left, right: left <= right,
        "greater": lambda left, right: left > right,
        "empty": lambda val: not val,
        "trim": str.strip,
        "toLower": str.lower,
        "length": len,
        "split": lambda val, sep: val.split(sep),
        "take": lambda val, count: val[:count],
        "skip": lambda val, count: val[count:],
        "reduce": lambda items, initial, fn: reduce(fn, items, initial),
        "replace": lambda val, old, new: val.replace(old, new),
        "contains": lambda container, item: item in container,
        "startsWith": lambda val, prefix: val.startswith(prefix),
        "endsWith": lambda val, suffix: val.endswith(suffix),
        "createArray": lambda *items: list(items),
        "createObject": lambda *items: dict(zip(items[::2], items[1::2], strict=True)),
        "union": lambda *objs: {key: val for obj in objs for key, val in obj.items()},
        "concat": lambda *items: reduce(lambda left, right: left + right, items),
        "format": lambda fmt, *args: fmt.format(*args),
        "coalesce": lambda *vals: next(val for val in vals if val is not None),
        "true": lambda: True,
        "false": lambda: False,
        "null": lambda: None,
        "parameters": lambda key: parameters[key],
        "variables": lambda key: evaluate_arm(
            variables[key],
            parameters,
            variables,
            rg_name=rg_name,
            rg_location=rg_location,
        ),
        "resourceGroup": lambda: SimpleNamespace(name=rg_name, location=rg_location),
    }
    return eval(source, {"__builtins__": {}}, scope)


class EnvironmentQuotaParametersTests(unittest.TestCase):
    main: dict[str, Any]
    sql: dict[str, Any]
    guard: dict[str, Any]
    iot_live: dict[str, Any]
    resident_demo: dict[str, Any]
    resident_assistant: dict[str, Any]
    bicepparams: dict[str, dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.main = compile_bicep("main.bicep")
        cls.sql = compile_bicep("modules/sql.bicep")
        cls.guard = compile_bicep("modules/guard.bicep")
        cls.iot_live = compile_bicep("iot-hub-live.bicep")
        cls.resident_demo = compile_bicep("resident-demo.bicep")
        cls.resident_assistant = compile_bicep("resident-assistant.bicep")
        cls.bicepparams = {
            "dev": compile_bicepparam("main.bicepparam"),
            "test": compile_bicepparam("main.test.bicepparam"),
            "pilot": compile_bicepparam("main.pilot.example.bicepparam"),
        }

    def _default_values(self, template: dict[str, Any]) -> dict[str, Any]:
        return {
            key: spec["defaultValue"]
            for key, spec in template["parameters"].items()
            if "defaultValue" in spec
        }

    def _guard_failures(self, template: dict[str, Any], **overrides: Any) -> set[str]:
        values = {
            **self._default_values(template),
            "location": "uksouth",
            "sqlLocation": "offline-sql-region",
            "regionCheckReference": (
                "infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137"
            ),
            "quotaCheckReference": (
                "docs/architecture/environment-region-quota-strategy.md"
                "#recorded-capability-and-quota-check-ledger-r1-through-r17"
            ),
            "entraTokenStoreReady": False,
            **overrides,
        }
        passed = find_module(template, "parameter-guard")["properties"]["parameters"]
        return {
            name
            for name, arg in passed.items()
            if not evaluate_arm(arg, values, template["variables"])["value"]
        }

    def _assert_contract(self, template: dict[str, Any], sql_template: dict[str, Any]) -> None:
        params = template["parameters"]
        self.assertEqual(params["sqlTier"]["allowedValues"], ["serverless", "provisioned"])
        self.assertEqual(params["sqlVCores"]["minValue"], 1)
        self.assertEqual(params["sqlVCores"]["maxValue"], 80)
        self.assertEqual(params["sqlVCores"]["defaultValue"], 2)
        self.assertEqual(params["sqlAutoPauseDelayMinutes"]["minValue"], -1)
        self.assertEqual(params["sqlAutoPauseDelayMinutes"]["defaultValue"], 60)
        self.assertEqual(sql_template["parameters"]["maxVCores"]["minValue"], 1)
        self.assertEqual(sql_template["parameters"]["maxVCores"]["maxValue"], 80)
        self.assertEqual(sql_template["parameters"]["autoPauseDelayMinutes"]["minValue"], -1)
        self.assertEqual(params["monthlyBudget"]["minValue"], 1)
        self.assertEqual(params["monthlyBudget"]["defaultValue"], 300)
        self.assertEqual(params["apiMinReplicas"]["minValue"], 0)
        self.assertEqual(params["apiMinReplicas"]["maxValue"], 4)
        self.assertEqual(params["chatModelSku"]["allowedValues"], ["GlobalStandard", "Standard"])
        self.assertEqual(params["chatModelSku"]["defaultValue"], "GlobalStandard")
        self.assertEqual(params["chatModelCapacity"]["minValue"], 1)
        self.assertEqual(params["chatModelCapacity"]["defaultValue"], 1)
        self.assertEqual(params["iotHubSku"]["allowedValues"], ["B1"])
        self.assertEqual(params["iotHubUnits"]["minValue"], 1)
        self.assertEqual(params["iotHubUnits"]["maxValue"], 1)
        self.assertEqual(params["iotHubRetentionDays"]["minValue"], 1)
        self.assertEqual(params["iotHubRetentionDays"]["maxValue"], 7)
        self.assertEqual(params["iotHubMonthlyCost"]["minValue"], 1)
        self.assertEqual(params["iotHubMonthlyCost"]["maxValue"], 700)
        self.assertEqual(params["modelDeployments"]["minLength"], 1)

        sql_mod = find_module(template, "sql")["properties"]["parameters"]
        self.assertEqual(sql_mod["location"], {"value": "[parameters('sqlLocation')]"})
        self.assertEqual(sql_mod["endpointLocation"], {"value": "[parameters('location')]"})
        self.assertEqual(sql_mod["maxVCores"], {"value": "[parameters('sqlVCores')]"})
        self.assertEqual(sql_mod["sqlTier"], {"value": "[parameters('sqlTier')]"})

        self.assertEqual(self._guard_failures(template), set())
        self.assertIn(
            "regionCheckMustBeRecorded",
            self._guard_failures(template, regionCheckReference="assumed"),
        )
        self.assertIn(
            "quotaCheckMustBeRecorded",
            self._guard_failures(template, quotaCheckReference=SYNTHETIC_UUID),
        )
        self.assertIn(
            "deploymentLocationsMustBeSelected",
            self._guard_failures(template, sqlLocation="placeholder"),
        )
        self.assertIn(
            "primaryLocationMustBeUKSouth",
            self._guard_failures(template, location="ukwest"),
        )

    def test_region_and_standalone_template_boundaries(self) -> None:
        params = self.main["parameters"]
        self.assertEqual(params["location"]["defaultValue"], "[resourceGroup().location]")
        self.assertEqual(params["sqlLocation"]["defaultValue"], "[parameters('location')]")
        self.assertIs(params["zoneRedundant"]["defaultValue"], False)

        for module_name in ("storage", "registry", "sql", "containerapps"):
            forwarded = find_module(self.main, module_name)["properties"]["parameters"]
            self.assertEqual(
                forwarded["zoneRedundant"],
                {"value": "[parameters('zoneRedundant')]"},
                module_name,
            )

        self.assertEqual(self.iot_live["parameters"]["location"]["defaultValue"], "uksouth")
        iot_guard = find_module(self.iot_live, "iot-live-scope-guard")["properties"]["parameters"]
        self.assertIn("iotLocationMustBeUKSouth", iot_guard)
        self.assertEqual(
            self.resident_demo["parameters"]["location"]["defaultValue"],
            "[resourceGroup().location]",
        )
        self.assertEqual(
            self.resident_assistant["parameters"]["location"]["allowedValues"],
            ["swedencentral"],
        )
        self.assertEqual(
            self.resident_assistant["parameters"]["location"]["defaultValue"],
            "swedencentral",
        )

    def test_quota_and_budget_bounds_and_module_forwarding(self) -> None:
        self._assert_contract(self.main, self.sql)
        self.assertEqual(len(self.guard["parameters"]), 33)
        for name, spec in self.guard["parameters"].items():
            self.assertEqual(spec["minLength"], 1, name)
            self.assertIn("Empty means", spec["metadata"]["description"], name)

        foundry_params = find_module(self.main, "foundry")["properties"]["parameters"]
        self.assertIn("modelDeployments", str(foundry_params["deployments"]["value"]))
        iothub_params = find_module(self.main, "iothub")["properties"]["parameters"]
        self.assertEqual(iothub_params["skuName"], {"value": "[parameters('iotHubSku')]"})
        self.assertEqual(iothub_params["unitCount"], {"value": "[parameters('iotHubUnits')]"})
        self.assertEqual(
            iothub_params["retentionDays"],
            {"value": "[parameters('iotHubRetentionDays')]"},
        )
        self.assertEqual(
            iothub_params["monthlyCostEstimate"],
            {"value": "[parameters('iotHubMonthlyCost')]"},
        )
        ca_params = find_module(self.main, "containerapps")["properties"]["parameters"]
        self.assertEqual(
            ca_params["apiMinReplicas"],
            {"value": "[parameters('apiMinReplicas')]"},
        )
        budgets = [
            item
            for item in self.main["resources"]
            if item.get("type") == "Microsoft.Consumption/budgets"
        ]
        self.assertEqual(len(budgets), 1)
        self.assertEqual(budgets[0]["properties"]["amount"], "[parameters('monthlyBudget')]")
        op_mon_params = find_module(self.main, "operational-monitoring")["properties"]["parameters"]
        self.assertEqual(
            op_mon_params["monthlyBudget"],
            {"value": "[parameters('monthlyBudget')]"},
        )

    def test_environment_bicepparam_sets_declare_explicit_quotas_and_fail_closed(self) -> None:
        expected_models = [
            {
                "name": "standard",
                "model": "gpt-4.1-nano",
                "version": "2025-04-14",
                "skuName": "GlobalStandard",
                "capacity": 1,
            }
        ]
        raw_files = {
            "dev": "main.bicepparam",
            "test": "main.test.bicepparam",
            "pilot": "main.pilot.example.bicepparam",
        }
        for env_name, compiled in self.bicepparams.items():
            raw_text = (INFRA / raw_files[env_name]).read_text(encoding="utf-8")
            self.assertEqual(raw_text.count("param apiMinReplicas ="), 1, env_name)
            if env_name in {"dev", "pilot"}:
                self.assertNotIn("chat", raw_text.lower(), env_name)
            if env_name == "pilot":
                self.assertNotIn("AutoPause", raw_text, env_name)
                self.assertEqual(compiled["sqlTier"], "provisioned")
                self.assertEqual(compiled["location"], "")
                self.assertEqual(compiled["sqlLocation"], "")
            else:
                self.assertEqual(compiled["sqlTier"], "serverless")
                self.assertEqual(compiled["sqlAutoPauseDelayMinutes"], 60)
                self.assertEqual(compiled["location"], "uksouth")
                self.assertEqual(compiled["sqlLocation"], "uksouth")

            self.assertEqual(compiled["environmentName"], env_name)
            self.assertEqual(compiled["regionCheckReference"], "")
            self.assertEqual(compiled["quotaCheckReference"], "")
            self.assertEqual(compiled["sqlVCores"], 2)
            self.assertEqual(compiled["apiMinReplicas"], 0)
            self.assertEqual(compiled["monthlyBudget"], 300)
            self.assertEqual(compiled["iotHubSku"], "B1")
            self.assertEqual(compiled["iotHubUnits"], 1)
            self.assertEqual(compiled["iotHubRetentionDays"], 1)
            self.assertEqual(compiled["iotHubMonthlyCost"], 60)
            self.assertEqual(compiled["modelDeployments"], expected_models)

            values = {**self._default_values(self.main), **compiled}
            passed = find_module(self.main, "parameter-guard")["properties"]["parameters"]
            failing = {
                name
                for name, arg in passed.items()
                if not evaluate_arm(arg, values, self.main["variables"])["value"]
            }
            expected_failures = {"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"}
            if env_name == "pilot":
                expected_failures |= {
                    "deploymentLocationsMustBeSelected",
                    "primaryLocationMustBeUKSouth",
                }
            self.assertEqual(failing, expected_failures, env_name)

    def test_bicep_recorded_check_and_location_guards_reject_assumptions_and_uuids(self) -> None:
        rejected_checks = (
            "",
            "   ",
            "PLACEHOLDER",
            "placeholder-2026-11-15",
            "todo",
            "todo_check",
            "TBD: run later",
            "tbd_later",
            "assumed",
            "assumed_uksouth_2026",
            "assumption-only",
            "unverified-check",
            "unverified_quota",
            "pending-review",
            "unknown",
            "none",
            "N/A",
            "na",
            "skip-for-demo",
            "https://quota.example.invalid/ref",
            "00000000-0000-0000-0000-000000000000",
            SYNTHETIC_UUID,
            SYNTHETIC_UUID.upper(),
            f"  {SECOND_UUID}  ",
        )
        for bad in rejected_checks:
            with self.subTest(regionCheckReference=bad):
                self.assertEqual(
                    self._guard_failures(self.main, regionCheckReference=bad),
                    {"regionCheckMustBeRecorded"},
                )
            with self.subTest(quotaCheckReference=bad):
                self.assertEqual(
                    self._guard_failures(self.main, quotaCheckReference=bad),
                    {"quotaCheckMustBeRecorded"},
                )

        accepted_checks = (
            "infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137",
            "docs/reference/research/spending-review-2026-11-01.md#quota-audit",
            "docs/reference/research/spending_review_2026.md#jtbd_notes_2026",
            "docs/reference/research/ux/jtbd-capacity-notes-2026-11-02.md#uksouth",
            "ops-ticket:CHG-2026-1115-uksouth-quota-612cbed78a35a4ab426571aa7d2aeb0ae6d691dd",
        )
        for good in accepted_checks:
            with self.subTest(valid_check=good):
                self.assertEqual(
                    self._guard_failures(
                        self.main,
                        regionCheckReference=good,
                        quotaCheckReference=good,
                    ),
                    set(),
                )

        rejected_sql_locations = (
            "",
            "   ",
            "UKSouth",
            " uksouth",
            "uksouth ",
            "uk",
            "12345",
            "1uksouth",
            "-uksouth",
            "uksouth-",
            "uk--south",
            "uk south",
            "placeholder",
            "assumed",
            "tbd",
            "todo",
            "unknown",
            "pending",
            SYNTHETIC_UUID,
        )
        for bad_loc in rejected_sql_locations:
            with self.subTest(sqlLocation=bad_loc):
                self.assertEqual(
                    self._guard_failures(self.main, sqlLocation=bad_loc),
                    {"deploymentLocationsMustBeSelected"},
                )

        for good_loc in (
            "uksouth",
            "ukwest",
            "northeurope",
            "offline-region",
            "offline-sql-region",
        ):
            with self.subTest(valid_sqlLocation=good_loc):
                self.assertEqual(
                    self._guard_failures(self.main, sqlLocation=good_loc),
                    set(),
                )

        self.assertEqual(
            self._guard_failures(self.main, location=" UKSouth "),
            {"primaryLocationMustBeUKSouth", "deploymentLocationsMustBeSelected"},
        )

    def test_negative_mutations_are_caught_by_contract_assertions(self) -> None:
        for guard_name in (
            "regionCheckMustBeRecorded",
            "quotaCheckMustBeRecorded",
            "deploymentLocationsMustBeSelected",
            "primaryLocationMustBeUKSouth",
        ):
            with self.subTest(guard_bypass=guard_name):
                mutated = deepcopy(self.main)
                find_module(mutated, "parameter-guard")["properties"]["parameters"][guard_name] = {
                    "value": "ok"
                }
                with self.assertRaises(AssertionError):
                    self._assert_contract(mutated, self.sql)

        missing_min = deepcopy(self.main)
        del missing_min["parameters"]["sqlVCores"]["minValue"]
        with self.assertRaises((AssertionError, KeyError)):
            self._assert_contract(missing_min, self.sql)

        missing_autopause_min = deepcopy(self.main)
        del missing_autopause_min["parameters"]["sqlAutoPauseDelayMinutes"]["minValue"]
        with self.assertRaises((AssertionError, KeyError)):
            self._assert_contract(missing_autopause_min, self.sql)

        missing_sql_max = deepcopy(self.sql)
        del missing_sql_max["parameters"]["maxVCores"]["maxValue"]
        with self.assertRaises((AssertionError, KeyError)):
            self._assert_contract(self.main, missing_sql_max)

        wrong_forwarding = deepcopy(self.main)
        find_module(wrong_forwarding, "sql")["properties"]["parameters"]["maxVCores"] = {"value": 2}
        with self.assertRaises(AssertionError):
            self._assert_contract(wrong_forwarding, self.sql)

    def test_pipeline_parameters_enforce_recorded_checks_and_redact_values(self) -> None:
        base_overrides: dict[str, Any] = {
            "entraClientId": SECOND_UUID,
            "entraBearerOnly": False,
            "sqlAdminGroupName": "zava-sql-admins",
            "sqlAdminGroupObjectId": SECOND_UUID,
            "alertEmail": "alerts@zava-housing.example",
            "location": "uksouth",
            "sqlLocation": "ukwest",
            "aiModelLocation": "uksouth",
            "regionCheckReference": (
                "docs/reference/research/spending-review-2026-11-01.md"
                "#612cbed78a35a4ab426571aa7d2aeb0ae6d691dd"
            ),
            "quotaCheckReference": (
                "docs/reference/research/ux/jtbd-capacity-notes-2026-11-02.md#quota-check"
            ),
        }
        cached_build_params = {
            "parametersJson": json.dumps(
                {
                    "parameters": {
                        key: {"value": deepcopy(val)}
                        for key, val in self.bicepparams["test"].items()
                    }
                }
            )
        }
        for valid_region_ref, valid_quota_ref in (
            (
                base_overrides["regionCheckReference"],
                base_overrides["quotaCheckReference"],
            ),
            (
                "infra/README.md#spending_review_2026",
                "docs/reference/research/jtbd_notes_2026",
            ),
        ):
            valid_env = {
                "DEPLOY_PARAMETERS": json.dumps(
                    {
                        **base_overrides,
                        "regionCheckReference": valid_region_ref,
                        "quotaCheckReference": valid_quota_ref,
                    }
                )
            }
            with (
                patch.dict("os.environ", valid_env, clear=False),
                patch.object(PIPELINE, "az", return_value=deepcopy(cached_build_params)),
            ):
                resolved = PIPELINE.parameters(INFRA, "test")["parameters"]
            self.assertEqual(resolved["location"]["value"], "uksouth")
            self.assertEqual(resolved["sqlLocation"]["value"], "ukwest")

        invalid_cases: tuple[tuple[str, str], ...] = (
            ("regionCheckReference", "   "),
            ("regionCheckReference", "assumed-uksouth-2026"),
            ("regionCheckReference", "assumed_uksouth_2026"),
            ("regionCheckReference", "todo_check"),
            ("regionCheckReference", "tbd_later"),
            ("regionCheckReference", "unverified_quota"),
            ("regionCheckReference", "PLACEHOLDER"),
            ("regionCheckReference", SYNTHETIC_UUID),
            ("regionCheckReference", f"sub_{SYNTHETIC_UUID}_uksouth"),
            ("quotaCheckReference", f"checked-on-sub-{SYNTHETIC_UUID}-uksouth"),
            ("quotaCheckReference", f"sub_{SYNTHETIC_UUID}_uksouth"),
            ("quotaCheckReference", "assumed_uksouth_2026"),
            ("quotaCheckReference", "todo_check"),
            ("quotaCheckReference", "tbd_later"),
            ("quotaCheckReference", "unverified_quota"),
            ("quotaCheckReference", "TBD"),
            ("quotaCheckReference", "n/a"),
            ("location", "ukwestleakedregion"),
            ("location", "ukwest-hyphen-region"),
            ("location", "UKSouthInvalidCase"),
            ("sqlLocation", "placeholdersqlsecret"),
            ("sqlLocation", "placeholder"),
            ("sqlLocation", "assumed"),
            ("sqlLocation", "uk-south-hyphen"),
            ("sqlLocation", SYNTHETIC_UUID),
        )
        for field_name, secret_like_bad_value in invalid_cases:
            bad_overrides = {**base_overrides, field_name: secret_like_bad_value}
            bad_env = {"DEPLOY_PARAMETERS": json.dumps(bad_overrides)}
            with (
                self.subTest(field=field_name, value=secret_like_bad_value),
                patch.dict("os.environ", bad_env, clear=False),
                patch.object(PIPELINE, "az", return_value=deepcopy(cached_build_params)),
            ):
                with self.assertRaises(PIPELINE.PipelineError) as ctx:
                    PIPELINE.parameters(INFRA, "test")
                message = str(ctx.exception)
                self.assertNotIn(SYNTHETIC_UUID, message)
                stripped = secret_like_bad_value.strip()
                if len(stripped) >= 8:
                    self.assertNotIn(stripped.lower(), message.lower())

    def test_deploy_cli_rejects_invalid_check_and_region_overrides_before_az(self) -> None:
        base_cli_args = [
            "deploy.py",
            "--resource-group",
            "ama",
            "--parameters",
            str(INFRA / "main.test.bicepparam"),
            "--registry",
            "crforwardtest",
            "--environment",
            "test",
        ]
        bad_arg_cases: tuple[tuple[list[str], tuple[str, ...]], ...] = (
            (
                ["--parameter", "regionCheckReference=assumed_uksouth_2026"],
                ("assumed_uksouth_2026",),
            ),
            (
                ["--parameter", "regionCheckReference=todo_check"],
                ("todo_check",),
            ),
            (
                ["--parameter", "regionCheckReference=tbd_later"],
                ("tbd_later",),
            ),
            (
                ["--parameter", "regionCheckReference=unverified_quota"],
                ("unverified_quota",),
            ),
            (
                ["--parameter", f"regionCheckReference=sub_{SYNTHETIC_UUID}_uksouth"],
                (SYNTHETIC_UUID, f"sub_{SYNTHETIC_UUID}_uksouth"),
            ),
            (
                ["--parameter", f"quotaCheckReference=sub-{SYNTHETIC_UUID}-verified"],
                (SYNTHETIC_UUID,),
            ),
            (
                ["--parameter", f"quotaCheckReference=sub_{SYNTHETIC_UUID}_uksouth"],
                (SYNTHETIC_UUID, f"sub_{SYNTHETIC_UUID}_uksouth"),
            ),
            (
                ["--parameter", "quotaCheckReference=assumed_uksouth_2026"],
                ("assumed_uksouth_2026",),
            ),
            (
                ["--parameter", "quotaCheckReference=todo_check"],
                ("todo_check",),
            ),
            (
                ["--parameter", "quotaCheckReference=tbd_later"],
                ("tbd_later",),
            ),
            (
                ["--parameter", "quotaCheckReference=unverified_quota"],
                ("unverified_quota",),
            ),
            (
                [
                    "--parameter",
                    "regionCheckReference=placeholder_secret_token",
                    "--parameter",
                    "regionCheckReference=infra/README.md#valid-second-value",
                ],
                ("placeholder_secret_token",),
            ),
            (
                ["--parameter", "location=ukwestleakedregion"],
                ("ukwestleakedregion",),
            ),
            (
                ["--parameter", "sqlLocation=placeholdersqlsecret"],
                ("placeholdersqlsecret",),
            ),
            (
                ["--parameter", "sqlLocation=uk-south-hyphen"],
                ("uk-south-hyphen",),
            ),
        )
        for extra_args, forbidden_leaks in bad_arg_cases:
            stderr_buf = io.StringIO()
            with (
                self.subTest(args=extra_args),
                patch.object(sys, "argv", [*base_cli_args, *extra_args]),
                patch.object(DEPLOY, "az_json") as mock_az_json,
                patch.object(DEPLOY.subprocess, "run") as mock_run,
                redirect_stderr(stderr_buf),
            ):
                exit_code = DEPLOY.main()
            self.assertEqual(exit_code, 1)
            mock_az_json.assert_not_called()
            mock_run.assert_not_called()
            stderr_text = stderr_buf.getvalue()
            self.assertNotIn(SYNTHETIC_UUID, stderr_text)
            for leak in forbidden_leaks:
                self.assertNotIn(leak.lower(), stderr_text.lower())

        with self.assertRaises(DEPLOY.DeploymentError):
            DEPLOY.validate_parameter_overrides(["regionCheckReference"])

        DEPLOY.validate_parameter_overrides(
            [
                "location=uksouth",
                "sqlLocation=ukwest",
                "regionCheckReference=infra/README.md#spending_review_2026",
                "quotaCheckReference=docs/reference/research/jtbd_notes_2026",
                (
                    "regionCheckReference=docs/reference/research/spending-2026.md"
                    "#612cbed78a35a4ab426571aa7d2aeb0ae6d691dd"
                ),
            ]
        )

    def test_architecture_doc_and_infra_readme_match_compiled_templates_and_r1_r17(self) -> None:
        self.assertTrue(ARCH_DOC.is_file(), "Missing canonical architecture strategy document")
        arch_text = ARCH_DOC.read_text(encoding="utf-8")
        self.assertTrue(arch_text.startswith("---\ntitle: "))
        arch_body = arch_text.split("---\n", 2)[2]
        self.assertIsNone(re.search(r"^# ", arch_body, re.MULTILINE))
        self.assertNotIn("\u2014", arch_text)
        self.assertIsNone(re.search(r"^\s*[-*]\s+\*\*", arch_body, re.MULTILINE))
        self.assertIsNone(re.search(r"^\s*-\s+", arch_body, re.MULTILINE))
        self.assertNotIn(".copilot-tracking/", arch_text)
        self.assertNotIn("enableDemoChat", arch_text)
        self.assertNotIn(r"\b[0-9a-f]{8}", arch_text)

        for match in re.finditer(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", arch_body):
            rel = match.group(1)
            if rel.startswith("http"):
                continue
            self.assertTrue((ARCH_DOC.parent / rel).resolve().exists(), rel)

        bicep_refs = set(
            re.findall(r"`((?:infra/)?(?:modules/)?[A-Za-z0-9_-]+\.bicep)`", arch_body)
        )
        self.assertGreaterEqual(len(bicep_refs), 7)
        for bicep_ref in sorted(bicep_refs):
            resolved_bicep = (
                ROOT / bicep_ref if bicep_ref.startswith("infra/") else INFRA / bicep_ref
            )
            self.assertTrue(resolved_bicep.is_file(), f"Missing documented Bicep file: {bicep_ref}")

        catalog_section = arch_body.split("## Quota, SKU, and Capacity Parameter Catalog\n", 1)[
            1
        ].split("\n## ", 1)[0]
        catalog_rows = [
            [cell.strip() for cell in line.split("|")[1:-1]]
            for line in catalog_section.splitlines()
            if line.startswith("| `")
        ]
        for param_name in (
            "sqlTier",
            "sqlVCores",
            "sqlAutoPauseDelayMinutes",
            "sqlBackupRetentionDays",
            "apiMinReplicas",
            "chatModelName",
            "chatModelVersion",
            "chatModelSku",
            "chatModelCapacity",
            "iotHubSku",
            "iotHubUnits",
            "iotHubRetentionDays",
            "iotHubMonthlyCost",
            "monthlyBudget",
        ):
            matching_rows = [row for row in catalog_rows if f"`{param_name}`" in row[0]]
            self.assertEqual(len(matching_rows), 1, param_name)
            default_val = self.main["parameters"][param_name]["defaultValue"]
            expected_token = (
                f"`'{default_val}'`" if isinstance(default_val, str) else f"`{default_val}`"
            )
            self.assertIn(expected_token, matching_rows[0][2], param_name)

        arch_index_text = ARCH_INDEX.read_text(encoding="utf-8")
        self.assertIn("./environment-region-quota-strategy.md", arch_index_text)
        added_paragraph = next(
            block
            for block in arch_index_text.split("\n\n")
            if "environment-region-quota-strategy.md" in block
        )
        self.assertNotIn(".copilot-tracking/", added_paragraph)

        for required_token in (
            "GP_S_Gen5",
            "GP_Gen5",
            "modules/operationalMonitoring.bicep",
            "regionCheckMustBeRecorded",
            "quotaCheckMustBeRecorded",
            "deploymentLocationsMustBeSelected",
            "primaryLocationMustBeUKSouth",
            "swedencentral",
            "(?<![a-z0-9])",
            "(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])",
            "612cbed78a35a4ab426571aa7d2aeb0ae6d691dd",
        ):
            self.assertIn(required_token, arch_text)

        infra_readme_text = INFRA_README.read_text(encoding="utf-8")
        env_section = infra_readme_text.split("## Environments\n", 1)[1].split("\n## ", 1)[0]
        self.assertNotIn(".copilot-tracking/", env_section)
        self.assertIn("../docs/architecture/environment-region-quota-strategy.md", env_section)
        self.assertIn("GP_Gen5", env_section)
        self.assertIn("gpt-4.1-nano", env_section)
        self.assertIn(
            "daea1e37adc95f704fba7673883e0b4b6c7b65ab00179b59d8473654ab71f42a", env_section
        )
        for check_num in range(1, 18):
            self.assertRegex(env_section, rf"\|\s*`?R{check_num}`?\s*\|")
            self.assertIn(f"`R{check_num}`", arch_text)


if __name__ == "__main__":
    unittest.main()
