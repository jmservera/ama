"""Governance as code: policy, Defender, locks, tags and exceptions stay consistent."""
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

    def test_required_tags_match_main_template(self) -> None:
        governance = (INFRA / "governance.bicep").read_text()
        main = (INFRA / "main.bicep").read_text()
        block = re.search(r"var allTags = union\(tags, \{(.*?)\}\)", main, re.S)
        assert block is not None
        applied = set(re.findall(r"^\s+(\w+):", block.group(1), re.M))
        required = set(re.findall(r"^\s+'(\w+)'$", governance.split("param requiredTags")[1].split("]")[0], re.M))
        self.assertTrue(required)
        self.assertLessEqual(required, applied)

    def test_pilot_parameters_enable_locks(self) -> None:
        self.assertIn("param enableLocks = true", (INFRA / "main.pilot.bicepparam").read_text())

    def test_exceptions_have_owner_and_expiry_or_open_item(self) -> None:
        data = json.loads((INFRA / "policy-exceptions.json").read_text())
        self.assertTrue(data["exceptions"])
        for item in data["exceptions"]:
            self.assertTrue(item["owner"])
            self.assertTrue(item["expiry"] or "open owner decision" in item["expiryStatus"])


if __name__ == "__main__":
    unittest.main()
