"""Offline, stateful az contract tests for the one-command Entra setup."""
import base64
import copy
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "setup_entra", Path(__file__).resolve().parents[1] / "scripts" / "setup-entra.py")
assert SPEC and SPEC.loader
SETUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SETUP)


def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"fictional-{name}.invalid"))


TENANT, SUB, CLIENT, OBJECT, SP, USER, GROUP = map(uid, ("tenant", "subscription", "client", "app", "sp", "user", "group"))
SECRET = "FICTIONAL-SECRET-DO-NOT-LOG"
APP_ID = f"/subscriptions/{SUB}/resourceGroups/ama/providers/Microsoft.App/containerApps/ca-cutover-test-api"
FQDN = "api.internal.example.invalid"
EDGE = "edge.azurefd.net"
ARM_APP = SETUP.ARM + APP_ID + f"?api-version={SETUP.API_VERSION}"
AUTH_URL = SETUP.ARM + APP_ID + f"/authConfigs/current?api-version={SETUP.API_VERSION}"


class FakeAzure:
    def __init__(self):
        self.app = {
            "name": "ca-cutover-test-api", "id": APP_ID,
            "tags": {"zava-forward-role": "api"},
            "identity": {"type": "UserAssigned", "userAssignedIdentities": {"managed-identity": {}}},
            "properties": {
                "provisioningState": "Succeeded",
                "configuration": {"ingress": {"fqdn": FQDN}, "secrets": [{"name": "preserved"}]},
                "template": {"containers": [{"name": "api", "env": [{"name": "ZF_AUTH", "value": "trusted-proxy"}]}]},
            },
        }
        self.auth = {
            "platform": {"enabled": True},
            "httpSettings": {"forwardProxy": {"convention": "Standard"}},
            "globalValidation": {"unauthenticatedClientAction": "RedirectToLoginPage",
                                 "redirectToProvider": "azureactivedirectory",
                                 "excludedPaths": ["/", "/healthz", "/sign-in"]},
            "login": {"tokenStore": {"enabled": True}},
            "identityProviders": {"azureActiveDirectory": {
                "enabled": True, "registration": {"clientId": "systemAssignedIdentity"},
                "login": {"loginParameters": ["prompt=select_account"]},
            }},
        }
        self.apps = [self.app]
        self.reg = None
        self.sp = None
        self.assignments = []
        self.permissions = {"Application.ReadWrite.All", "AppRoleAssignment.ReadWrite.All",
                            "User.Read.All", "GroupMember.Read.All"}
        self.writes = []
        self.calls = []
        self.fail = None
        self.tenant = TENANT
        self.profiles = [{"name": "afd-cutover-test", "tags": {"zava-forward-role": "api-edge"}}]
        self.origins = [{"hostName": FQDN, "enabledState": "Enabled"}]
        self.routes = [{"enabledState": "Enabled", "originGroup": {"id": "/originGroups/api"},
                        "patternsToMatch": ["/*"], "supportedProtocols": ["Https"],
                        "linkToDefaultDomain": "Enabled", "customDomains": []}]
        self.domains = []
        self.memberships = []
        self.consent = []

    def run(self, command, *, env, capture_output, text, timeout, check):
        self.calls.append((command, env))
        assert command[0] == "az"
        assert env["AZURE_LOGGING_ENABLE_LOG_FILE"] == "false"
        assert capture_output and text and timeout
        args = command[1:-3]
        body = None
        if "--body" in args:
            filename = Path(args[args.index("--body") + 1][1:])
            assert filename.stat().st_mode & 0o077 == 0
            body = json.loads(filename.read_text())
            assert SECRET not in " ".join(command)
        if self.fail and self.fail(args):
            return subprocess.CompletedProcess(command, 1, "", f"Forbidden {TENANT} {SECRET}")
        if args[0] == "rest":
            method = args[args.index("--method") + 1]
            url = args[args.index("--url") + 1]
            if method != "GET" and "/listSecrets?" not in url:
                self.writes.append((method, url, body))
            value = self.rest(method, url, body)
        elif args[:2] == ["account", "show"]:
            value = {"tenantId": self.tenant, "id": SUB, "user": {"type": "user"}}
        elif args[:2] == ["account", "get-access-token"]:
            payload = base64.urlsafe_b64encode(json.dumps({"scp": " ".join(self.permissions), "tid": self.tenant}).encode()).decode()
            value = {"accessToken": "header." + payload + ".signature"}
        elif args[:2] == ["containerapp", "list"]:
            value = self.apps
        elif args[:2] == ["containerapp", "show"]:
            value = self.app
        elif args[:3] == ["afd", "profile", "list"]:
            value = self.profiles
        elif args[:3] == ["afd", "origin-group", "list"]:
            value = [{"name": "api", "id": "/originGroups/api"}]
        elif args[:3] == ["afd", "origin", "list"]:
            value = self.origins
        elif args[:3] == ["afd", "endpoint", "list"]:
            value = [{"name": "ep-cutover-test", "hostName": EDGE, "enabledState": "Enabled"}]
        elif args[:3] == ["afd", "custom-domain", "list"]:
            value = self.domains
        elif args[:3] == ["afd", "route", "list"]:
            value = self.routes
        elif args[:2] == ["keyvault", "list"]:
            value = [{"name": "fictional-vault"}]
        elif args[:3] == ["keyvault", "secret", "set"]:
            assert Path(args[args.index("--file") + 1]).read_text() == SECRET
            value = {"id": "https://fictional-vault.vault.azure.net/secrets/entra-generated/version"}
        elif args[0] == "version" or args[:2] == ["extension", "show"]:
            value = {}
        else:
            raise AssertionError(f"Unexpected fake az operation: {args[:3]}")
        return subprocess.CompletedProcess(command, 0, json.dumps(copy.deepcopy(value)), "")

    def rest(self, method, url, body):
        if url == AUTH_URL:
            if method == "PUT":
                self.auth = copy.deepcopy(body["properties"])
            return {"properties": self.auth}
        if url == ARM_APP:
            if method == "PATCH":
                if "configuration" in body["properties"]:
                    assert body["properties"]["configuration"]["ingress"]["fqdn"] == FQDN
                    self.app["properties"]["configuration"]["secrets"] = body["properties"]["configuration"]["secrets"]
                if "template" in body["properties"]:
                    self.app["properties"]["template"] = body["properties"]["template"]
            return self.app
        if "/listSecrets?" in url:
            return {"value": [{"name": "preserved", "value": "preserved-private-value"}]}
        path = url.removeprefix(SETUP.GRAPH)
        route = path.split("?")[0]
        if route == "applications":
            if method == "POST":
                self.reg = {"id": OBJECT, "appId": CLIENT, "web": {}, "appRoles": [], "api": {},
                            "passwordCredentials": [], "identifierUris": [], **body}
                return self.reg
            return {"value": [self.reg] if self.reg else []}
        if route in (f"applications/{OBJECT}", f"applications(appId='{CLIENT}')"):
            if self.reg is None:
                raise SETUP.AzureError("not-found")
            if method == "PATCH":
                self.reg.update(copy.deepcopy(body))
                if self.sp:
                    self.sp["appRoles"] = copy.deepcopy(self.reg["appRoles"])
            return self.reg
        if route == f"applications/{OBJECT}/addPassword":
            credential = {**body["passwordCredential"], "keyId": uid("credential")}
            self.reg["passwordCredentials"].append(credential)
            return {**credential, "secretText": SECRET}
        if route == "servicePrincipals":
            if method == "GET" and SETUP.GRAPH_APP in url:
                return {"value": [{"id": uid("graph-sp"), "appId": SETUP.GRAPH_APP}]}
            if method == "POST":
                self.sp = {"id": SP, "appId": CLIENT, "appRoleAssignmentRequired": False,
                           "appRoles": copy.deepcopy(self.reg["appRoles"])}
                return self.sp
            return {"value": [self.sp] if self.sp else []}
        if route == f"servicePrincipals/{SP}":
            if method == "PATCH":
                self.sp.update(body)
            return self.sp
        if route == f"servicePrincipals/{SP}/appRoleAssignedTo":
            if method == "POST":
                self.assignments.append(copy.deepcopy(body))
                return body
            return {"value": self.assignments}
        if route == f"users/{USER}":
            assert "$select=id,accountEnabled,userType" in url
            return {"id": USER, "accountEnabled": True, "userType": "Member"}
        if route == f"groups/{GROUP}":
            assert "$select=id,securityEnabled" in url
            return {"id": GROUP, "securityEnabled": True}
        if route == f"users/{USER}/memberOf/microsoft.graph.group":
            return {"value": [{"id": group} for group in self.memberships]}
        if route == "oauth2PermissionGrants":
            return {"value": self.consent}
        raise AssertionError(f"Unexpected fake API route: {route}")


class SetupTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        self.profile = self.home / "profile"
        self.profile.mkdir(mode=0o700)
        self.roster = self.home / "roster.json"
        self.home.chmod(0o700)
        self.write_roster([{"code": "fictional-coordinator", "userId": USER, "role": "Coordinator"}])
        self.fake = FakeAzure()
        self.output = io.StringIO()
        self.addCleanup(patch.stopall)
        patch.object(SETUP, "PROFILE", self.profile).start()
        patch.object(SETUP, "ROSTER", self.roster).start()
        patch.object(SETUP.subprocess, "run", side_effect=self.fake.run).start()
        patch.object(SETUP.shutil, "which", return_value="/fake/az").start()
        patch.object(SETUP.time, "sleep").start()
        patch.dict(os.environ, {"AZURE_CONFIG_DIR": str(self.home / "operator")}).start()

    def write_roster(self, value):
        self.roster.write_text(json.dumps(value))
        self.roster.chmod(0o600)

    def invoke(self, *args):
        with redirect_stdout(self.output), redirect_stderr(self.output):
            code = SETUP.main(list(args))
        for sensitive in (TENANT, SUB, CLIENT, OBJECT, SP, USER, GROUP, SECRET, "preserved-private-value"):
            self.assertNotIn(sensitive, self.output.getvalue())
        return code

    def bootstrap(self):
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 0, self.output.getvalue())

    def test_tag_discovery_managed_identity_creation_and_idempotent_rerun(self):
        self.fake.app["name"] = "api-not-a-pattern"
        self.fake.app["id"] = APP_ID.rsplit("/", 1)[0] + "/api-not-a-pattern"
        # Keep ARM fixtures stable in other tests; exercise tag precedence separately here.
        selected = SETUP.choose([self.fake.app, {"name": "ca-other-api", "tags": {}}],
                                None, "api", r"ca-.+-api", "--container-app")
        self.assertIs(selected, self.fake.app)
        self.fake = FakeAzure()
        SETUP.subprocess.run.side_effect = self.fake.run
        original = copy.deepcopy(self.fake.auth)
        self.bootstrap()
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], CLIENT)
        self.assertEqual(self.fake.auth["login"], original["login"])
        self.assertEqual(self.fake.auth["globalValidation"], original["globalValidation"])
        self.assertIn({"name": "ZF_TRUSTED_PROXY", "value": "1"},
                      self.fake.app["properties"]["template"]["containers"][0]["env"])
        self.assertTrue(self.fake.sp["appRoleAssignmentRequired"])
        self.assertEqual(len(self.fake.reg["appRoles"]), 8)
        callbacks = self.fake.reg["web"]["redirectUris"]
        self.assertIn(f"https://{FQDN}/.auth/login/aad/callback", callbacks)
        self.assertIn(f"https://{EDGE}/.auth/login/aad/callback", callbacks)
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.assertEqual(len(self.fake.writes), count)
        self.assertFalse(list(self.profile.iterdir()))

    def test_no_arguments_reports_missing_credential_not_uuid_traceback(self):
        self.assertEqual(self.invoke(), 2)
        self.assertIn("Browser credential missing", self.output.getvalue())
        self.assertNotIn("hexadecimal", self.output.getvalue())
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], "systemAssignedIdentity")

    def test_disabled_null_auth_is_created_with_probe_exemptions(self):
        self.fake.auth = {"platform": None, "identityProviders": None, "globalValidation": None, "httpSettings": None}
        self.bootstrap()
        self.assertTrue(self.fake.auth["platform"]["enabled"])
        self.assertIn("/healthz", self.fake.auth["globalValidation"]["excludedPaths"])
        self.assertEqual(self.fake.auth["globalValidation"]["unauthenticatedClientAction"], "RedirectToLoginPage")
        self.assertEqual(self.fake.auth["httpSettings"]["forwardProxy"]["convention"], "Standard")

    def test_unresolved_configured_uuid_does_not_create_replacement(self):
        self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"] = CLIENT
        self.assertEqual(self.invoke(), 1)
        self.assertIn("review it before selecting another", self.output.getvalue())
        self.assertFalse(self.fake.writes)

    def test_ambiguous_tag_candidates_fail_before_directory_writes(self):
        second = copy.deepcopy(self.fake.app)
        second["name"] = "ca-other-api"
        self.fake.apps.append(second)
        self.assertEqual(self.invoke(), 1)
        self.assertIn("ca-other-api", self.output.getvalue())
        self.assertFalse(self.fake.writes)
        self.assertEqual(self.invoke("-n", "ca-cutover-test-api", "--dry-run"), 2)

    def test_fallback_and_wrong_name_candidate_list(self):
        self.fake.app["tags"] = {}
        self.assertEqual(self.invoke("--dry-run"), 2)
        self.assertEqual(self.invoke("-n", "ca-forward-test-api"), 1)
        self.assertIn("ca-cutover-test-api", self.output.getvalue())

    def test_dry_run_and_check_are_read_only_and_detect_missing_state(self):
        before = list(self.profile.iterdir())
        self.assertEqual(self.invoke("--dry-run", "--create-secret", "--secret-store", "app"), 2)
        self.assertEqual(self.invoke("--check"), 2)
        self.assertFalse(self.fake.writes)
        self.assertEqual(before, list(self.profile.iterdir()))
        self.assertEqual(self.invoke("--check", "--login"), 1)
        self.assertFalse(self.fake.writes)

    def test_check_initialized_and_old_callbacks_roles_credentials_are_preserved(self):
        self.bootstrap()
        self.fake.reg["web"]["redirectUris"].append("https://old.example.invalid/callback")
        self.fake.reg["appRoles"].append({"id": uid("other-role"), "value": "Unrelated.Role",
                                         "isEnabled": True, "allowedMemberTypes": ["User"]})
        snapshot = copy.deepcopy(self.fake.reg)
        writes = len(self.fake.writes)
        self.assertEqual(self.invoke("--check"), 0)
        self.assertEqual(self.fake.reg, snapshot)
        self.assertEqual(len(self.fake.writes), writes)

    def test_missing_tools_python_and_extension_have_install_instructions(self):
        with patch.object(SETUP.shutil, "which", return_value=None):
            self.assertEqual(self.invoke(), 1)
        self.assertIn("python3 -m pip install azure-cli", self.output.getvalue())
        self.fake.fail = lambda a: a[:2] == ["extension", "show"]
        self.assertEqual(self.invoke(), 1)
        self.assertIn("az extension add", self.output.getvalue())
        with patch.object(SETUP.sys, "version_info", (3, 9)):
            self.assertEqual(self.invoke(), 1)
        self.assertIn("Python 3.10+", self.output.getvalue())
        self.assertFalse(self.fake.writes)

    def test_permission_denial_is_explicit_redacted_not_absence(self):
        self.fake.fail = lambda a: a[0] == "rest" and "applications?" in a[a.index("--url") + 1]
        self.assertEqual(self.invoke(), 1)
        self.assertIn("Option A", self.output.getvalue())
        self.assertFalse(self.fake.writes)
        self.assertIsNone(self.fake.reg)

    def test_assignment_permission_preflight_before_mutations(self):
        self.fake.permissions.remove("AppRoleAssignment.ReadWrite.All")
        self.assertEqual(self.invoke(), 1)
        self.assertIn("assignment permission is missing", self.output.getvalue())
        self.assertFalse(self.fake.writes)

    def test_roster_validation_and_legacy_role_gap(self):
        for value in (
                [], {}, [{"code": "legacy", "userId": USER}],
                [{"code": "bad", "userId": "not-an-identifier", "role": "Coordinator"}],
                [{"code": "bad", "userId": USER, "groupId": GROUP, "role": "Coordinator"}],
                [{"code": "a", "userId": USER, "role": "Coordinator"},
                 {"code": "b", "userId": USER, "role": "Coordinator"}],
                [{"code": "a", "userId": USER, "role": "Administrator"}]):
            self.write_roster(value)
            self.assertEqual(self.invoke(), 1)
            self.assertFalse(self.fake.writes)
        self.roster.chmod(0o644)
        self.assertEqual(self.invoke(), 1)

    def test_missing_roster_reports_incomplete(self):
        self.roster.unlink()
        self.assertEqual(self.invoke("--dry-run"), 2)
        self.assertIn("Private roster missing", self.output.getvalue())

    def test_group_assignment_and_planned_user_group_conflict(self):
        self.write_roster([{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"}])
        self.bootstrap()
        self.assertEqual(self.fake.assignments[0]["principalId"], GROUP)
        self.fake.assignments = []
        self.fake.memberships = [GROUP]
        self.write_roster([{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"},
                           {"code": "fictional-officer", "userId": USER, "role": "SupportOfficer"}])
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 1)
        self.assertIn("Planned group and user assignments conflict", self.output.getvalue())
        self.assertEqual(len(self.fake.writes), count)

    def test_existing_group_role_conflict_fails_without_new_assignments(self):
        self.bootstrap()
        self.fake.assignments = [{"principalId": GROUP, "resourceId": SP,
                                  "appRoleId": str(uuid.uuid5(SETUP.ROLE_NAMESPACE, "SupportOfficer"))}]
        self.fake.memberships = [GROUP]
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(len(self.fake.writes), count)

    def test_disabled_user_and_nonsecurity_group_rejected(self):
        self.bootstrap()
        self.fake.assignments = []
        original = self.fake.rest
        def directory(method, url, body):
            if url.startswith(SETUP.GRAPH + f"users/{USER}?"):
                return {"id": USER, "accountEnabled": False, "userType": "Member"}
            return original(method, url, body)
        with patch.object(self.fake, "rest", side_effect=directory):
            self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.assignments)
        self.write_roster([{"code": "team", "groupId": GROUP, "role": "Coordinator"}])
        def group_directory(method, url, body):
            if url.startswith(SETUP.GRAPH + f"groups/{GROUP}?"):
                return {"id": GROUP, "securityEnabled": False}
            return original(method, url, body)
        with patch.object(self.fake, "rest", side_effect=group_directory):
            self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.assignments)

    def test_edge_origin_association_domains_and_explicit_override(self):
        self.fake.origins = [{"hostName": "unrelated.example.invalid"}]
        self.assertEqual(self.invoke("--dry-run"), 2)
        self.assertIn("1 API/edge", self.output.getvalue())
        self.assertEqual(self.invoke("--dry-run", "--edge-profile", "afd-cutover-test"), 1)
        self.fake.origins = [{"hostName": FQDN}]
        self.fake.routes[0]["customDomains"] = [{"id": "/domains/workbench"}]
        self.fake.domains = [{"id": "/domains/workbench", "hostName": "workbench.example.invalid",
                              "domainValidationState": "Approved", "deploymentStatus": "Succeeded"}]
        self.assertEqual(self.invoke("--dry-run", "--public-url", "https://workbench.example.invalid"), 2)
        self.fake.domains[0]["domainValidationState"] = "Pending"
        self.assertEqual(self.invoke("--dry-run", "--public-url", "https://workbench.example.invalid"), 1)
        self.assertFalse(self.fake.writes)

    def test_pending_custom_domain_remains_in_final_summary(self):
        self.fake.routes[0]["customDomains"] = [{"id": "/domains/workbench"}]
        self.fake.domains = [{"id": "/domains/workbench", "hostName": "workbench.example.invalid",
                              "domainValidationState": "Pending", "deploymentStatus": "InProgress"}]
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 2)
        self.assertIn("Remaining: Linked custom domain", self.output.getvalue())

    def test_edge_ambiguity_and_mixed_origins_rejected(self):
        self.fake.profiles[0]["tags"] = {}
        self.fake.profiles.append({"name": "afd-another"})
        self.assertEqual(self.invoke("--dry-run"), 1)
        self.assertIn("Cannot select one api-edge", self.output.getvalue())
        self.assertEqual(self.invoke("--dry-run", "--edge-profile", "afd-cutover-test"), 2)
        self.fake.origins.append({"hostName": "other.example.invalid"})
        self.assertEqual(self.invoke("--dry-run"), 1)
        self.assertFalse(self.fake.writes)

    def test_tagged_edge_preferred_over_legacy_linked_edge(self):
        self.fake.profiles.append({"name": "afd-another"})
        self.assertEqual(self.invoke("--dry-run"), 2)
        self.assertFalse(self.fake.writes)

    def test_secret_failure_never_activates_and_rerun_requires_orphan_recovery(self):
        self.fake.fail = lambda a: a[0] == "rest" and a[a.index("--method") + 1] == "PATCH" and a[a.index("--url") + 1] == ARM_APP
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], "systemAssignedIdentity")
        self.fake.fail = None
        count = len(self.fake.reg["passwordCredentials"])
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertIn("handoff is incomplete", self.output.getvalue())
        self.assertEqual(len(self.fake.reg["passwordCredentials"]), count)
        self.assertFalse(list(self.profile.iterdir()))

    def test_keyvault_credential_storage_no_secret_argv_and_identity_validation(self):
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 0, self.output.getvalue())
        secret = self.fake.app["properties"]["configuration"]["secrets"][-1]
        self.assertIn("keyVaultUrl", secret)
        self.assertNotIn("value", secret)
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(len(self.fake.writes), count)

    def test_missing_vault_identity_fails_before_password_creation(self):
        self.assertEqual(self.invoke("--create-secret"), 1)
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertIn("--vault-identity", self.output.getvalue())

    def test_unverified_runtime_rollout_is_not_success(self):
        self.fake.app["properties"]["provisioningState"] = "Failed"
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertIn("runtime authentication settings are not verified", self.output.getvalue())
        self.assertFalse(list(self.profile.iterdir()))

    def test_unknown_creation_outcome_is_discovered_on_rerun_without_duplicate(self):
        original = self.fake.rest
        def lost_response(method, url, body):
            result = original(method, url, body)
            if method == "POST" and url == SETUP.GRAPH + "applications":
                raise SETUP.AzureError("transient")
            return result
        with patch.object(self.fake, "rest", side_effect=lost_response):
            self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertIsNotNone(self.fake.reg)
        self.bootstrap()
        creates = [w for w in self.fake.writes if w[:2] == ("POST", SETUP.GRAPH + "applications")]
        self.assertEqual(len(creates), 1)

    def test_explicit_bearer_mode_removes_reference_without_deleting_secret(self):
        self.bootstrap()
        before = copy.deepcopy(self.fake.app["properties"]["configuration"]["secrets"])
        self.assertEqual(self.invoke("--bearer-only"), 2)
        self.assertEqual(self.fake.auth["globalValidation"]["unauthenticatedClientAction"], "Return401")
        self.assertNotIn("clientSecretSettingName",
                         self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"])
        self.assertEqual(self.fake.app["properties"]["configuration"]["secrets"], before)
        self.assertEqual(self.invoke("--bearer-only", "--create-secret"), 1)

    def test_bearer_mode_preserved_without_implicit_browser_activation(self):
        self.fake.auth["globalValidation"]["unauthenticatedClientAction"] = "Return401"
        self.assertEqual(self.invoke(), 2)
        self.assertEqual(self.fake.auth["globalValidation"]["unauthenticatedClientAction"], "Return401")
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], CLIENT)
        self.assertIn("browser sign-in still needs", self.output.getvalue())

    def test_account_photo_consent_read_only_and_polling(self):
        self.bootstrap()
        self.assertEqual(self.invoke("--account-photo", "--check"), 2)
        self.assertIn("Grant admin consent", self.output.getvalue())
        self.fake.consent = [{"scope": "User.Read", "consentType": "AllPrincipals", "resourceId": uid("graph-sp")}]
        self.assertEqual(self.invoke("--account-photo"), 0)
        self.assertIn({"id": SETUP.USER_READ, "type": "Scope"},
                      self.fake.reg["requiredResourceAccess"][0]["resourceAccess"])

    def test_human_consent_polls_matching_graph_grant_and_timeout_is_blocked(self):
        self.bootstrap()
        original = self.fake.rest
        calls = []
        def eventual_consent(method, url, body):
            if url.startswith(SETUP.GRAPH + "oauth2PermissionGrants?"):
                calls.append(url)
                if len(calls) >= 3:
                    return {"value": [{"scope": "User.Read", "consentType": "AllPrincipals",
                                        "resourceId": uid("graph-sp")}]}
                return {"value": []}
            return original(method, url, body)
        with patch.object(self.fake, "rest", side_effect=eventual_consent):
            self.assertEqual(self.invoke("--account-photo", "--wait-seconds", "4"), 0)
        self.assertEqual(len(calls), 3)
        self.assertEqual(self.invoke("--account-photo", "--wait-seconds", "2"), 1)
        self.assertIn("Admin consent is still pending", self.output.getvalue())
        self.assertFalse(any(w[0] != "GET" and "oauth2PermissionGrants" in w[1] for w in self.fake.writes))

    def test_service_principal_without_directory_authority_gets_options(self):
        self.fake.permissions -= SETUP.APPLICATION_WRITE
        original = self.fake.run
        def service_account(command, **kwargs):
            response = original(command, **kwargs)
            if command[1:3] == ["account", "show"]:
                data = json.loads(response.stdout)
                data["user"] = {"type": "servicePrincipal"}
                response.stdout = json.dumps(data)
            return response
        with patch.object(SETUP.subprocess, "run", side_effect=service_account):
            self.assertEqual(self.invoke(), 1)
        self.assertIn("service principal without directory", self.output.getvalue())
        self.assertIn("Option A", self.output.getvalue())
        self.assertIn("Option B", self.output.getvalue())
        self.assertFalse(self.fake.writes)

    def test_invalid_origin_scope_profile_and_duplicate_lock(self):
        for value in ("http://example.invalid", "https://user@example.invalid", "https://example.invalid/path"):
            self.assertEqual(self.invoke("--public-url", value, "--dry-run"), 1)
        self.assertEqual(self.invoke("-g", "other"), 1)
        self.assertEqual(self.invoke("--tenant-profile", str(self.home / "operator")), 1)
        (self.profile / "setup-entra.lock").touch()
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.writes)
        self.assertTrue((self.profile / "setup-entra.lock").exists())

    def test_argument_errors_do_not_echo_identifiers_or_secrets(self):
        self.assertEqual(self.invoke("--not-an-option", TENANT), 1)
        self.assertEqual(self.invoke("--secret-store", SECRET), 1)
        self.assertFalse(self.fake.writes)

    def test_readonly_does_not_create_missing_profile_or_login(self):
        self.profile.rmdir()
        with patch.object(SETUP, "device_login") as login:
            self.assertEqual(self.invoke("--check"), 1)
            login.assert_not_called()
        self.assertFalse(self.profile.exists())

    def test_cross_tenant_login_fails_before_mutation(self):
        original = self.fake.run
        def different_tenant(command, **kwargs):
            response = original(command, **kwargs)
            if command[1:3] == ["account", "show"] and kwargs["env"]["AZURE_CONFIG_DIR"] == str(self.profile):
                response.stdout = json.dumps({"tenantId": uid("other-tenant"), "id": SUB})
            return response
        with patch.object(SETUP.subprocess, "run", side_effect=different_tenant):
            self.assertEqual(self.invoke(), 1)
        self.assertIn("different tenant", self.output.getvalue())
        self.assertFalse(self.fake.writes)

    def test_missing_graph_login_starts_isolated_device_flow(self):
        original = self.fake.run
        missing = [True]
        def no_session(command, **kwargs):
            if (missing[0] and command[1:3] == ["account", "show"]
                    and kwargs["env"]["AZURE_CONFIG_DIR"] == str(self.profile)):
                return subprocess.CompletedProcess(command, 1, "", "Please run az login")
            return original(command, **kwargs)
        def login(cli, tenant):
            self.assertEqual(cli.profile, self.profile)
            self.assertEqual(tenant, TENANT)
            missing[0] = False
        with (patch.object(SETUP.subprocess, "run", side_effect=no_session),
              patch.object(SETUP, "device_login", side_effect=login) as device):
            self.bootstrap()
        device.assert_called_once()
        self.assertEqual(self.profile.stat().st_mode & 0o077, 0)

    def test_fixed_host_pagination_and_partial_failure(self):
        cli = SETUP.Azure(self.profile)
        for link in ("https://evil.invalid/v1.0/users", SETUP.GRAPH + "users"):
            with (patch.object(cli, "rest", return_value={"value": [], "@odata.nextLink": link}),
                  self.assertRaises(SETUP.SetupError)):
                cli.pages("users")

    def test_transient_reads_retry_not_posts_and_cli_failures_are_sanitized(self):
        cli = SETUP.Azure(self.profile, body_directory=self.profile)
        with patch.object(cli, "call", side_effect=[SETUP.AzureError("transient"), {"value": []}]) as call:
            self.assertEqual(cli.pages("users"), [])
            self.assertEqual(call.call_count, 2)
        with patch.object(cli, "call", side_effect=SETUP.AzureError("transient")) as call:
            with self.assertRaises(SETUP.AzureError):
                cli.rest(SETUP.GRAPH + "applications", method="POST", body={})
            self.assertEqual(call.call_count, 1)
        for result in (OSError("sensitive"), subprocess.TimeoutExpired("sensitive", 1)):
            with (patch.object(SETUP.subprocess, "run", side_effect=result),
                  self.assertRaisesRegex(SETUP.SetupError, "could not run or timed out")):
                cli.call(["version"])
        with (patch.object(SETUP.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, SECRET, "")),
              self.assertRaisesRegex(SETUP.SetupError, "invalid JSON")):
            cli.call(["version"])

    def test_device_login_only_prints_device_prompt_and_uses_isolated_profile(self):
        process = unittest.mock.Mock()
        process.stdout = io.StringIO(
            f"To sign in, use a web browser to open https://microsoft.com/devicelogin and enter the code ABCD12345 to authenticate.\n{TENANT} {SECRET}\n")
        process.wait.return_value = 0
        with (patch.object(SETUP.subprocess, "Popen", return_value=process) as popen,
              redirect_stdout(self.output)):
            SETUP.device_login(SETUP.Azure(self.profile), TENANT)
        self.assertIn("ABCD12345", self.output.getvalue())
        self.assertNotIn(TENANT, self.output.getvalue())
        self.assertNotIn(SECRET, self.output.getvalue())
        self.assertEqual(popen.call_args.kwargs["env"]["AZURE_CONFIG_DIR"], str(self.profile))
        self.assertIn("--use-device-code", popen.call_args.args[0])

    def test_bicep_discovery_tags_exist(self):
        infra = Path(__file__).resolve().parents[1]
        self.assertIn("'zava-forward-role': 'api'", (infra / "modules/containerapps.bicep").read_text())
        self.assertEqual((infra / "modules/edge.bicep").read_text().count("'zava-forward-role': 'api-edge'"), 2)


if __name__ == "__main__":
    unittest.main()
