"""Role-assignment matrix, no-shared-key and Entra registration checks (issue 141)."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "mvp"))
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


class RoleMatrixTests(unittest.TestCase):
    def rows(self, resource):
        return [r for r in MATRIX["assignments"] if r["resource"] == resource]

    def test_every_matrix_row_is_in_its_bicep_and_complete(self) -> None:
        for row in MATRIX["assignments"]:
            self.assertTrue(row["reason"] and row["scope"], row)
            self.assertIn(row["roleId"], MATRIX["builtInRoles"])
            self.assertIn(row["roleId"], BICEP[row["bicep"]] + MAIN, row)

    def test_every_bicep_role_is_in_the_matrix_and_none_is_broad(self) -> None:
        all_text = "".join(BICEP.values())
        for guid, name in BROAD.items():
            self.assertNotIn(guid, all_text, name)
        used = {r["roleId"] for r in MATRIX["assignments"]}
        self.assertEqual(used, set(MATRIX["builtInRoles"]))
        for guid in MATRIX["builtInRoles"]:
            self.assertTrue(any(guid in text for text in BICEP.values()), guid)

    def test_module_consumers_match_matrix(self) -> None:
        for module, resource in (("keyvault", "keyvault"), ("registry", "registry"), ("iotHub", "iotHub")):
            expected = {r["identity"] for r in self.rows(resource) if r["identity"] != "token-maintenance"}
            self.assertEqual(module_principals(module), expected, module)
        foundry = {r["identity"] for r in self.rows("foundry")}
        self.assertEqual(module_principals("foundry"), foundry)

    def test_storage_assignments_match_matrix(self) -> None:
        var_ids = dict(re.findall(r"var (\w+) = '(" + GUID.pattern + ")'", MAIN))
        parsed = set()
        for ident, role, scope in re.findall(
                r"principalId: identity\.outputs\.principalIds\.(\w+), roleDefinitionId: (\w+), scope: '(\w+)'", MAIN):
            parsed.add((ident, var_ids[role], scope))
        matrix = {(r["identity"], r["roleId"], "blob" if "blob" in r["scope"] else "queue")
                  for r in self.rows("storage")}
        self.assertEqual(parsed, matrix)

    def test_iot_hub_grants_receiver_only_to_api(self) -> None:
        self.assertEqual([(r["identity"], r["roleId"]) for r in self.rows("iotHub")],
                         [("api", "a638d3c7-ab3a-418d-83e6-5f17a39d4fde")])

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
        from zavaforward_mvp.auth import DEFAULT_ROLE_MAP
        manifest = {f"ZavaForward.{r['key']}": r["label"] for r in ENTRA["appRoles"]}
        self.assertEqual(manifest, DEFAULT_ROLE_MAP)
        script = (ROOT / "scripts" / "create-api-app-registration.sh").read_text(encoding="utf-8")
        pairs = dict(re.findall(r'"(\w+)\|([^"]+)"', script))
        self.assertEqual({f"ZavaForward.{k}": v for k, v in pairs.items()}, DEFAULT_ROLE_MAP)
        self.assertIn(f"name={ENTRA['displayName']}", script)
        self.assertIn("appRoleAssignmentRequired", script)
        self.assertIn(ENTRA["callbackPath"], script)
        self.assertIn("AzureADMyOrg", script)

    def test_owner_and_contractor_decision_explicit(self) -> None:
        self.assertTrue(ENTRA["owner"])
        self.assertIn("Contractor", {r["key"] for r in ENTRA["appRoles"]})
        self.assertIn("open", ENTRA["contractorIdentity"]["status"])
        self.assertTrue(all(s["owner"] for s in ENTRA["manualSteps"]))


if __name__ == "__main__":
    unittest.main()
