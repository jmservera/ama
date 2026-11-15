"""Deterministic contract tests for Key Vault and managed-identity secret governance."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
KEYVAULT = (INFRA / "modules" / "keyvault.bicep").read_text(encoding="utf-8")
KV_ROLE_SECRETS_USER = "4633458b-17de-408a-b874-0445c86b69e6"
KV_PRIVILEGED_ROLES = {
    "00482a5a-887f-4fb3-b363-3b7fe8e74483": "Key Vault Administrator",
    "a4417e6f-fecd-4de8-b567-7b0420556985": "Key Vault Certificates Officer",
    "b86a8fe4-44ce-4948-aee5-eccb2c155cd7": "Key Vault Secrets Officer",
}


def bicep_files() -> list[Path]:
    return sorted(INFRA.rglob("*.bicep"))


class VaultHardeningTests(unittest.TestCase):
    def test_rbac_soft_delete_and_purge_protection(self) -> None:
        self.assertIn("enableRbacAuthorization: true", KEYVAULT)
        self.assertIn("enableSoftDelete: true", KEYVAULT)
        self.assertIn("enablePurgeProtection: purgeProtection ? true : null", KEYVAULT)
        self.assertIn("softDeleteRetentionInDays: purgeProtection ? 90 : 7", KEYVAULT)
        self.assertIn("param purgeProtection bool = true", KEYVAULT)
        self.assertNotIn("enableRbacAuthorization: false", KEYVAULT)
        self.assertNotIn("accessPolicies", KEYVAULT)

    def test_network_default_is_private(self) -> None:
        self.assertIn("param allowPublicNetworkAccess bool = false", KEYVAULT)
        self.assertIn("defaultAction: allowPublicNetworkAccess ? 'Allow' : 'Deny'", KEYVAULT)

    def test_main_does_not_disable_purge_protection_by_default(self) -> None:
        main = (INFRA / "main.bicep").read_text(encoding="utf-8")
        block = main[main.index("module keyvault 'modules/keyvault.bicep'") :]
        block = block[: block.index("\n}\n")]
        self.assertNotRegex(block, r"purgeProtection:\s*false")


class RotationMetadataTests(unittest.TestCase):
    def test_rotation_parameter_is_bounded_and_recorded(self) -> None:
        self.assertRegex(
            KEYVAULT,
            r"@minValue\(1\)\s*@maxValue\(365\)\s*param secretRotationDays int = 90",
        )
        self.assertIn("'secret-rotation-days': string(secretRotationDays)", KEYVAULT)

    def test_expiry_alert_and_audit_diagnostics(self) -> None:
        self.assertIn("categoryGroup: 'allLogs', enabled: true", KEYVAULT)
        self.assertIn("SecretNearExpiryEventGridNotification", KEYVAULT)
        self.assertIn("SecretExpiredEventGridNotification", KEYVAULT)
        self.assertIn("scopes: [workspaceId]", KEYVAULT)
        self.assertIn("actions: { actionGroups: [actionGroupId] }", KEYVAULT)


class ManagedIdentityRbacTests(unittest.TestCase):
    def test_vault_assignments_are_read_only_service_principals(self) -> None:
        self.assertIn(KV_ROLE_SECRETS_USER, KEYVAULT)
        self.assertIn("principalType: 'ServicePrincipal'", KEYVAULT)
        for role in KV_PRIVILEGED_ROLES:
            self.assertNotIn(role, KEYVAULT)

    def test_privileged_vault_roles_are_limited_to_one_secret_scope(self) -> None:
        officer = "b86a8fe4-44ce-4948-aee5-eccb2c155cd7"
        for path in bicep_files():
            text = path.read_text(encoding="utf-8")
            for role, label in KV_PRIVILEGED_ROLES.items():
                if role == officer and path.name == "authTokenStore.bicep":
                    self.assertRegex(
                        text,
                        r"scope: secret\s+name: guid\(secret\.id[^\n]*\n[^}]*" + officer,
                    )
                    continue
                self.assertNotIn(role, text, f"{path.name} grants {label}")


class PlaintextSecretOutputTests(unittest.TestCase):
    def test_no_bicep_output_exposes_secret_material(self) -> None:
        pattern = re.compile(r"^\s*output\s+(\w+)\s+(\w+)\s*=\s*(.*)$", re.MULTILINE)
        banned_name = re.compile(r"secret|password|sas|key(?!VaultName|VaultUri)|token", re.I)
        banned_value = re.compile(
            r"list(Keys|Secrets|Credentials|AccountSas|ServiceSas)\(|\.value\b", re.I
        )
        for path in bicep_files():
            text = path.read_text(encoding="utf-8")
            for name, _kind, value in pattern.findall(text):
                self.assertIsNone(banned_name.search(name), f"{path.name} output {name}")
                self.assertIsNone(banned_value.search(value), f"{path.name} output {name}")

    def test_secure_outputs_are_not_declared(self) -> None:
        for path in bicep_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"@secure\(\)\s*output", path.name)


if __name__ == "__main__":
    unittest.main()
