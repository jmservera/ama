"""Role-assignment matrix, no-shared-key and Entra registration checks (issue 141)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "role-assignments.json").read_text(encoding="utf-8"))
ENTRA = json.loads((ROOT / "entra" / "app-registration.json").read_text(encoding="utf-8"))
MAIN = (ROOT / "main.bicep").read_text(encoding="utf-8")
BICEP = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ROOT.rglob("*.bicep")}
GUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
BROAD = {"8e3af657-a8ff-443c-a75c-2fe8c4bcb635": "Owner", "b24988ac-6180-42a0-ab88-20f7382dd24c": "Contributor",
         "18d7d88d-d35e-4fb5-a5c3-7773c20a72d9": "User Access Administrator",
         "acdd72a7-3385-48ef-bd42-f606fba81ae7": "Reader"}


def module_principals(name: str) -> set[str]:
    block = re.search(rf"^module {name} '.*?^}}", MAIN, re.S | re.M).group(0)
    return set(re.findall(r"principalIds\.(\w+)", block))


SCOPE_NAMES = {
    ("modules/keyvault.bicep", "vault"): "Key Vault",
    ("modules/registry.bicep", "registry"): "Container registry",
    ("modules/foundry.bicep", "account"): "Foundry account",
    ("modules/iothub.bicep", "telemetry"): "IoT telemetry Event Hub",
    ("modules/iothub.bicep", "telemetryNamespace"): "IoT telemetry namespace",
    ("modules/authTokenStore.bicep", "account"): "Token store account",
    ("modules/authTokenStore.bicep", "tokens"): "auth-tokens container",
    ("modules/authTokenStore.bicep", "secret"): "Secret entra-token-store-sas only",
    ("modules/authTokenStore.bicep", "registry"): "Container registry",
}
STORAGE_SCOPES = {"blob": "Storage account, blob service", "queue": "Storage account, queue service"}
MODULE_FILES = {"modules/keyvault.bicep": "keyvault", "modules/registry.bicep": "registry",
                "modules/foundry.bicep": "foundry", "modules/iothub.bicep": "iotHub"}
STANDALONE = {
    "resident-assistant.bicep": ("resident-demo", {
        "account": "Resident assistant OpenAI account",
    }),
    "resident-demo.bicep": ("resident-demo", {
        "verifier": "Secret resident-demo-password-verifier only",
        "sessionKey": "Secret resident-demo-session-key only",
        "registry": "Container registry",
    }),
}
ROLE_RESOURCE = re.compile(
    r"^resource \w+ 'Microsoft\.Authorization/roleAssignments@[^']+' = .*?^\}", re.S | re.M)


def parse_bicep_assignments() -> list[tuple[str, str, str]]:
    """Return (identity, roleId, scope) for every role assignment resource in the Bicep."""
    found = []
    for path, text in BICEP.items():
        if path == "main.bicep" or path in {r["bicep"] for r in MATRIX.get("customRoles", [])}:
            continue
        variables = dict(re.findall(r"^(?:var|param) (\w+)(?: string)? = '(" + GUID.pattern + ")'", text, re.M))
        variables.update(re.findall(
            r"^var (\w+) = subscriptionResourceId\('Microsoft\.Authorization/roleDefinitions', '(" + GUID.pattern + r")'\)",
            text, re.M))
        for block in ROLE_RESOURCE.findall(text):
            if path == "modules/storage.bicep":
                continue
            scope = re.search(r"scope: (\w+)", block).group(1)
            principal = re.search(r"principalId: ([\w.]+)", block).group(1)
            if path in STANDALONE:
                identity, scope_names = STANDALONE[path]
                role_ref = re.search(r"roleDefinitionId: (\w+)", block)
                inline = re.search(r"roleDefinitions', '(" + GUID.pattern + r")'\)", block)
                role = inline.group(1) if inline else variables[role_ref.group(1)]
                found.append((identity, role, scope_names[scope]))
                continue
            role = re.search(r"roleDefinitions', ('?[\w-]+'?)\)", block).group(1)
            role = role.strip("'") if role.startswith("'") else variables[role]
            if principal == "maintenance.properties.principalId":
                identities = {"token-maintenance"}
            elif path == "modules/iothub.bicep" and principal == "hub.identity.principalId":
                identities = {"iot-hub"}
            else:
                identities = module_principals(MODULE_FILES[path])
            for identity in identities:
                found.append((identity, role, SCOPE_NAMES[(path, scope)]))
    var_ids = dict(re.findall(r"var (\w+) = '(" + GUID.pattern + ")'", MAIN))
    for ident, role, scope in re.findall(
            r"principalId: identity\.outputs\.principalIds\.(\w+), roleDefinitionId: (\w+), scope: '(\w+)'", MAIN):
        found.append((ident, var_ids[role], STORAGE_SCOPES[scope]))
    return found


class RoleMatrixTests(unittest.TestCase):
    def rows(self, resource):
        return [r for r in MATRIX["assignments"] if r["resource"] == resource]

    def test_matrix_rows_are_complete(self) -> None:
        for row in MATRIX["assignments"]:
            self.assertTrue(row["reason"] and row["scope"], row)
            self.assertIn(row["roleId"], MATRIX["builtInRoles"])

    def test_bicep_assignments_equal_matrix_tuples(self) -> None:
        parsed = parse_bicep_assignments()
        self.assertEqual(len(parsed), len(set(parsed)), "duplicate Bicep assignment")
        matrix = [(r["identity"], r["roleId"], r["scope"]) for r in MATRIX["assignments"]]
        self.assertEqual(len(matrix), len(set(matrix)), "duplicate matrix row")
        self.assertEqual(set(parsed), set(matrix))
        self.assertGreaterEqual(len(parsed), 19)

    def test_every_bicep_role_is_in_the_matrix_and_none_is_broad(self) -> None:
        all_text = "".join(BICEP.values())
        for guid, name in BROAD.items():
            self.assertNotIn(guid, all_text, name)
        used = {r["roleId"] for r in MATRIX["assignments"]}
        self.assertEqual(used, set(MATRIX["builtInRoles"]))

    def test_staff_initializer_custom_role_matches_matrix_and_api_only_assignment(self) -> None:
        self.assertEqual(len(MATRIX["customRoles"]), 2)
        role = MATRIX["customRoles"][0]
        text = BICEP[role["bicep"]]
        actions = re.search(r"actions: \[(.*?)\]", text, re.S).group(1)
        self.assertEqual(re.findall(r"'([^']+)'", actions), role["actions"])
        self.assertTrue(all("*" not in action for action in role["actions"]))
        assignment, relay_assignment = ROLE_RESOURCE.findall(text)
        self.assertIn("scope: api", assignment)
        self.assertIn("roleDefinitionId: restartRole.id", assignment)
        self.assertIn("principalId: initializer.properties.principalId", assignment)
        self.assertIn("notActions: []", text)
        self.assertIn("dataActions: []", text)
        self.assertIn("notDataActions: []", text)
        blob = MATRIX["customRoles"][1]
        blob_block = re.search(r"resource resultRole .*?^}", text, re.S | re.M).group(0)
        data = re.search(r"dataActions: \[(.*?)\]", blob_block, re.S).group(1)
        self.assertEqual(re.findall(r"'([^']+)'", data), blob["dataActions"])
        self.assertEqual(blob["actions"], [])
        self.assertIn("actions: []", blob_block)
        self.assertFalse(any("delete" in a or "read" in a for a in blob["dataActions"]))
        self.assertIn("scope: resultContainer", relay_assignment)
        self.assertIn("roleDefinitionId: resultRole.id", relay_assignment)
        self.assertIn("param includeResultBlob bool = false", text)
        self.assertIn("= if (includeResultBlob) {", blob_block)
        self.assertIn("= if (includeResultBlob) {", relay_assignment)
        self.assertNotIn("Microsoft.Resources/tags", text)

    def test_iot_hub_grants_receiver_only_to_api(self) -> None:
        self.assertEqual(
            [(r["identity"], r["roleId"], r["scope"]) for r in self.rows("iotHub")],
            [
                ("api", "a638d3c7-ab3a-418d-83e6-5f17a39d4fde", "IoT telemetry Event Hub"),
                ("iot-hub", "2b629674-e913-4c01-ae53-ef4638d8f975", "IoT telemetry namespace"),
            ],
        )

    def test_identities_match_bicep_and_sql_grants(self) -> None:
        workloads = re.search(r"var workloads = \[(.*?)\]", BICEP["modules/identity.bicep"]).group(1)
        names = set(re.findall(r"'(\w+)'", workloads))
        self.assertEqual({g["identity"] for g in MATRIX["sqlGrants"]}, names)
        sql = (ROOT / "scripts" / "create-sql-users.py").read_text(encoding="utf-8")
        for grant in MATRIX["sqlGrants"]:
            for role in grant["roles"]:
                self.assertIn(role, sql)
        self.assertEqual([g["identity"] for g in MATRIX["sqlGrants"] if not g["roles"]], ["agents", "orchestrator"])


class NoSharedCredentialTests(unittest.TestCase):
    def test_no_shared_keys_sql_logins_or_connection_strings(self) -> None:
        allowed_conn = {"modules/monitoring.bicep": "appInsightsConnectionString"}
        for path, text in BICEP.items():
            self.assertNotIn("listKeys", text, path)
            self.assertNotIn("listAccountSas", text, path)
            self.assertNotIn("administratorLoginPassword", text, path)
            self.assertNotRegex(text, r"allowSharedKeyAccess:\s*true", path)
            self.assertNotRegex(text, r"disableLocalAuth:\s*false", path)
            if "onnectionString" in text.replace("APPLICATIONINSIGHTS_CONNECTION_STRING", "").replace(
                    "appInsightsConnectionString", "").replace("properties.ConnectionString", ""):
                self.fail(f"connection string in {path}")
        self.assertIn("azureADOnlyAuthentication: true", BICEP["modules/sql.bicep"])
        self.assertNotIn("administratorLogin:", BICEP["modules/sql.bicep"])

    def test_every_data_plane_resource_disables_key_auth(self) -> None:
        self.assertIn("allowSharedKeyAccess: false", BICEP["modules/storage.bicep"])
        self.assertIn("allowSharedKeyAccess: false", BICEP["modules/authTokenStore.bicep"])
        for mod in ("foundry", "iothub", "monitoring"):
            self.assertIn("disableLocalAuth: true", BICEP[f"modules/{mod}.bicep"])

    def test_scripts_use_no_sql_password(self) -> None:
        for path in (ROOT / "scripts").glob("create-sql-users.*"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)password\s*=|User ID=|CREATE LOGIN")


class EntraRegistrationTests(unittest.TestCase):
    def test_manifest_matches_script_and_mvp_role_map(self) -> None:
        from zava_forward.api.auth import DEFAULT_ROLE_MAP, RULE_ROLE_MAP
        manifest = {f"ZavaForward.{r['key']}": r["label"] for r in ENTRA["appRoles"]}
        self.assertEqual(manifest, DEFAULT_ROLE_MAP)
        capabilities = {f"ZavaForward.{r['key']}": r["capability"] for r in ENTRA["capabilityRoles"]}
        self.assertEqual(capabilities, RULE_ROLE_MAP | {"ZavaForward.ApplicationAdmin": "application_admin"})
        self.assertTrue(set(manifest).isdisjoint(capabilities))
        script = (ROOT / "scripts" / "create-api-app-registration.sh").read_text(encoding="utf-8")
        pairs = dict(re.findall(r'"(\w+)\|([^"]+)"', script))
        labels = {f"ZavaForward.{r['key']}": r["label"] for r in ENTRA["capabilityRoles"]}
        self.assertEqual({f"ZavaForward.{k}": v for k, v in pairs.items()}, DEFAULT_ROLE_MAP | labels)
        self.assertIn(f"name={ENTRA['displayName']}", script)
        self.assertIn("appRoleAssignmentRequired", script)
        self.assertIn(ENTRA["callbackPath"], script)
        self.assertIn("AzureADMyOrg", script)

    def test_owner_and_contractor_decision_explicit(self) -> None:
        self.assertTrue(ENTRA["owner"])
        self.assertIn("Contractor", {r["key"] for r in ENTRA["appRoles"]})
        self.assertIn("open", ENTRA["contractorIdentity"]["status"])
        self.assertTrue(all(s["owner"] for s in ENTRA["manualSteps"]))

    def test_contractor_guest_design_is_enforced_by_code(self) -> None:
        design = ENTRA["contractorIdentity"]
        self.assertEqual(design["guestAssignableRoles"], ["Contractor"])
        self.assertTrue(ENTRA["appRoleAssignmentRequired"])
        self.assertNotIn("Contractor", {r["key"] for r in ENTRA["capabilityRoles"]})
        self.assertTrue(design["decisionOwner"])
        for name in design["memberOnlyInitializers"]:
            text = (ROOT / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn('"Member"', text, name)


if __name__ == "__main__":
    unittest.main()
