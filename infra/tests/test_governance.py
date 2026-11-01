"""Governance as code: policy, Defender, locks, tags and exceptions stay consistent."""
from datetime import date
import json
from pathlib import Path
import re
import unittest

INFRA = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def test_policy_assignments_and_defender_plans_defined(self) -> None:
        text = (INFRA / "governance.bicep").read_text()
        self.assertIn("targetScope = 'subscription'", text)
        self.assertIn("Microsoft.Authorization/policyAssignments", text)
        self.assertIn("Microsoft.Security/pricings", text)
        self.assertIn("param enableDefenderPlans bool = false", text)
        self.assertIn("param enforcementMode string = 'DoNotEnforce'", text)
        for guid in re.findall(r"definitionId: '([^']+)'", text):
            self.assertRegex(guid, r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$")

    def test_defender_decision_record_matches_template(self) -> None:
        record = json.loads((INFRA / "defender-decision.json").read_text())
        text = (INFRA / "governance.bicep").read_text()
        self.assertEqual(record["owner"], "Juan Manuel Servera")
        plans = set(re.findall(r"^\s+'(\w+)'$", text.split("param defenderPlans")[1].split("]")[0], re.M))
        self.assertEqual(set(record["defender"]["plans"]), plans)
        approval = record["defender"]["costApproval"]
        if approval["status"] != "approved":
            self.assertFalse(record["defender"]["enableDefenderPlans"])
            self.assertIsNone(approval["approvedOn"])
        self.assertIn("param enableDefenderPlans bool = false", text)

    def test_required_tags_match_main_template(self) -> None:
        governance = (INFRA / "governance.bicep").read_text()
        main = (INFRA / "main.bicep").read_text()
        block = re.search(r"var allTags = union\(tags, \{(.*?)\}\)", main, re.S)
        assert block is not None
        applied = set(re.findall(r"^\s+(\w+):", block.group(1), re.M))
        required = set(re.findall(r"^\s+'(\w+)'$", governance.split("param requiredTags")[1].split("]")[0], re.M))
        self.assertTrue(required)
        self.assertLessEqual(required, applied)

    def test_pilot_example_enables_locks(self) -> None:
        self.assertIn("param enableLocks = true", (INFRA / "main.pilot.example.bicepparam").read_text())

    def test_pilot_example_is_not_deployable(self) -> None:
        self.assertFalse((INFRA / "main.pilot.bicepparam").exists())
        text = (INFRA / "main.pilot.example.bicepparam").read_text()
        self.assertIn("NON-DEPLOYABLE EXAMPLE", text)
        self.assertIn("example.invalid", text)
        self.assertIn("00000000-0000-0000-0000-000000000000", text)
        self.assertNotIn("environmentName = 'dev'", text)

    def test_environment_parameter_files(self) -> None:
        expected = {"main.bicepparam": "dev", "main.test.bicepparam": "test", "main.pilot.example.bicepparam": "pilot"}
        for name, environment in expected.items():
            text = (INFRA / name).read_text()
            self.assertIn(f"param environmentName = '{environment}'", text, name)
            location = "" if environment == "pilot" else "uksouth"
            self.assertIn(f"param location = '{location}'", text, name)
            self.assertIn("PLACEHOLDER", text, name)
            params = "\n".join(line for line in text.splitlines() if line.startswith("param"))
            self.assertNotRegex(params, r"(?i)password|secret|webhook|sig=", name)
            self.assertIn("param allowPublicNetworkAccess = false", text, name)
            self.assertIn("param regionCheckReference = '' // PLACEHOLDER", text, name)
            self.assertIn("param quotaCheckReference = '' // PLACEHOLDER", text, name)
            profile = "development" if environment == "dev" else "production"
            protection = "false" if environment == "dev" else "true"
            self.assertIn(f"param deploymentProfile = '{profile}'", text, name)
            self.assertIn(f"param keyVaultPurgeProtection = {protection}", text, name)
            self.assertIn(f"param registryQuarantineEnabled = {protection}", text, name)

    def test_pilot_requires_production_profile(self) -> None:
        self.assertIn("pilotRequiresProductionProfile", (INFRA / "main.bicep").read_text())
        self.assertIn("pilotRequiresProductionProfile", (INFRA / "modules/guard.bicep").read_text())

    def test_policy_is_audit_only_and_defender_opt_in_by_default(self) -> None:
        text = (INFRA / "governance.bicep").read_text()
        self.assertIn("param enforcementMode string = 'DoNotEnforce'", text)
        self.assertIn("param enableDefenderPlans bool = false", text)
        readme = (INFRA / "README.md").read_text()
        self.assertIn("DoNotEnforce", readme)
        self.assertIn("until the owner accepts a cost", readme)

    def test_exceptions_have_owner_and_expiry_or_open_item(self) -> None:
        data = json.loads((INFRA / "policy-exceptions.json").read_text())
        self.assertTrue(data["exceptions"])
        for item in data["exceptions"]:
            self.assertTrue(item["owner"])
            expiry = date.fromisoformat(item["expiry"])
            observed = date.fromisoformat(item["firstObserved"])
            self.assertGreater(expiry, observed)
            self.assertLessEqual((expiry - observed).days, 180)


if __name__ == "__main__":
    unittest.main()
