"""Compiled deployment policy, with no Azure writes."""

import json
import subprocess
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]


class ResidentAssistantTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run = subprocess.run(
            [
                "az",
                "bicep",
                "build",
                "--file",
                str(INFRA / "resident-assistant.bicep"),
                "--stdout",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        cls.template = json.loads(run.stdout)
        cls.resources = cls.template["resources"]

    def test_default_off_and_ama_only_for_every_deployable_resource(self):
        self.assertFalse(self.template["parameters"]["enabled"]["defaultValue"])
        self.assertIn("ama", self.template["variables"]["active"])
        self.assertEqual(len(self.resources), 3)
        for resource in self.resources:
            self.assertEqual(resource["condition"], "[variables('active')]")

    def test_only_account_deployment_and_one_scoped_inference_role(self):
        kinds = {r["type"] for r in self.resources}
        self.assertEqual(
            kinds,
            {
                "Microsoft.CognitiveServices/accounts",
                "Microsoft.CognitiveServices/accounts/deployments",
                "Microsoft.Authorization/roleAssignments",
            },
        )
        role = next(r for r in self.resources if r["type"].endswith("roleAssignments"))
        self.assertIn("Microsoft.CognitiveServices/accounts", role["scope"])
        self.assertIn(
            "5e0bd9bd-7b93-4f28-af87-19fc36ad61bd",
            role["properties"]["roleDefinitionId"],
        )
        self.assertIn("residentIdentityName", role["properties"]["principalId"])

    def test_pinned_small_regional_model_and_no_keys_or_dynamic_quota(self):
        account = self.resources[0]
        self.assertTrue(account["properties"]["disableLocalAuth"])
        self.assertFalse(account["properties"]["dynamicThrottlingEnabled"])
        model = next(r for r in self.resources if r["type"].endswith("/deployments"))
        self.assertEqual(model["sku"]["name"], "Standard")
        self.assertEqual(model["properties"]["versionUpgradeOption"], "NoAutoUpgrade")
        self.assertEqual(self.template["parameters"]["capacity"]["allowedValues"], [1])
        self.assertEqual(
            self.template["parameters"]["modelName"]["allowedValues"], ["gpt-4.1-mini"]
        )
        self.assertEqual(
            self.template["parameters"]["modelVersion"]["allowedValues"], ["2025-04-14"]
        )
        self.assertNotIn("listKeys", json.dumps(self.template))
