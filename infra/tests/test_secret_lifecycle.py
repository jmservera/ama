"""Secret inventory, expiry/rotation checks, access review and Bicep wiring."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("secret_lifecycle", ROOT / "scripts" / "secret_lifecycle.py")
LIFE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIFE)
NOW = LIFE.parse_time("2026-10-15T00:00:00Z")
INVENTORY = json.loads((ROOT / "secret-inventory.json").read_text(encoding="utf-8"))


class InventoryTests(unittest.TestCase):
    def test_inventory_complete_and_covers_container_apps_secrets(self) -> None:
        self.assertEqual(LIFE.validate_inventory(INVENTORY), [])
        names = {entry["name"] for entry in INVENTORY["secrets"]}
        apps = (ROOT / "modules" / "containerapps.bicep").read_text(encoding="utf-8")
        for name in names:
            self.assertIn(f"/secrets/{name}'", apps)

    def test_missing_owner_is_reported(self) -> None:
        bad = {"secrets": [{"name": "x", "rotationIntervalDays": 1, "expiryAlertDays": 1}]}
        self.assertEqual(LIFE.validate_inventory(bad), ["x: missing owner"])


class CheckTests(unittest.TestCase):
    def secret(self, name, expires, updated="2026-10-01T00:00:00Z"):
        return {"name": name, "attributes": {"enabled": True, "expires": expires, "updated": updated}}

    def kinds(self, listed):
        return {(n, k) for n, k, _ in LIFE.check_secrets(INVENTORY, listed, NOW)}

    def test_healthy_secrets_have_no_findings(self) -> None:
        listed = [self.secret("entra-client-secret", "2027-04-01T00:00:00Z"),
                  self.secret("entra-token-store-sas", "2026-10-30T00:00:00Z", "2026-10-14T12:00:00Z")]
        self.assertEqual(self.kinds(listed), set())

    def test_expiring_expired_overdue_and_missing(self) -> None:
        listed = [self.secret("entra-client-secret", "2026-10-30T00:00:00Z", "2026-01-01T00:00:00Z")]
        kinds = self.kinds(listed)
        self.assertIn(("entra-client-secret", "expiring"), kinds)
        self.assertIn(("entra-client-secret", "rotation-overdue"), kinds)
        self.assertIn(("entra-token-store-sas", "missing"), kinds)
        expired = self.kinds([self.secret("entra-client-secret", "2026-10-01T00:00:00Z")])
        self.assertIn(("entra-client-secret", "expired"), expired)

    def test_no_expiry_is_a_finding(self) -> None:
        self.assertIn(("entra-client-secret", "no-expiry"), self.kinds([self.secret("entra-client-secret", None)]))


class ReviewAndRotationTests(unittest.TestCase):
    def test_review_record_is_pending_and_dated(self) -> None:
        record = LIFE.access_review(INVENTORY, [
            {"principalId": "p1", "principalType": "ServicePrincipal", "roleDefinitionName": "Key Vault Secrets User", "scope": "/v"},
            {"principalId": "p2", "principalType": "User", "roleDefinitionName": "Contributor", "scope": "/v"},
        ], "Reviewer", NOW)
        self.assertEqual(record["nextReviewDue"], "2027-01-13")
        self.assertEqual([r["decision"] for r in record["assignments"]], ["pending", "pending"])
        self.assertTrue(record["assignments"][1]["access"].startswith("unclassified"))

    def test_rotation_deletes_old_credential_only_after_verification(self) -> None:
        plan = LIFE.rotation_plan("kv", "app")
        text = "\n".join(plan)
        self.assertIn("--append", plan[0])
        self.assertLess(text.index("confirm /app"), text.index("credential delete"))


class BicepWiringTests(unittest.TestCase):
    def test_diagnostics_and_alerts(self) -> None:
        kv = (ROOT / "modules" / "keyvault.bicep").read_text(encoding="utf-8")
        self.assertIn("categoryGroup: 'allLogs'", kv)
        self.assertIn("workspaceId: workspaceId", kv)
        self.assertIn("SecretNearExpiryEventGridNotification", kv)
        self.assertIn("SecretExpiredEventGridNotification", kv)
        main = (ROOT / "main.bicep").read_text(encoding="utf-8")
        self.assertIn("actionGroupId: monitoring.outputs.actionGroupId", main)


if __name__ == "__main__":
    unittest.main()
