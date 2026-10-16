"""Offline, stateful az contract tests for the one-command Entra setup."""
import base64
import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

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
ENV_ID = (f"/subscriptions/{SUB}/resourceGroups/ama/providers"
          "/Microsoft.App/managedEnvironments/direct-demo")
ENV_URL = SETUP.ARM + ENV_ID + f"?api-version={SETUP.API_VERSION}"


class FakeAzure:
    def __init__(self):
        self.app: dict[str, Any] = {
            "etag": '"fictional-version"',
            "name": "ca-cutover-test-api", "id": APP_ID,
            "tags": {"zava-forward-role": "api"},
            "identity": {"type": "UserAssigned", "userAssignedIdentities": {"managed-identity": {}}},
            "properties": {
                "provisioningState": "Succeeded",
                "configuration": {"ingress": {"fqdn": FQDN}, "secrets": [{"name": "preserved"}]},
                "template": {"containers": [{"name": "api", "env": [{"name": "ZF_AUTH", "value": "trusted-proxy"}]}]},
            },
        }
        self.auth: dict[str, Any] = {
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
        self.reg: Any = None
        self.sp: Any = None
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
        self.environment: dict[str, Any] = {
            "properties": {"vnetConfiguration": {"internal": False}}}
        self.tag_writes = []
        self.sql_calls = []
        self.sql_code = 0
        self.sql_failure = None
        self.candidates = [{"code": "fictional-coordinator", "role": "Coordinator", "bound": False}]
        self.users = []
        self.purposes = {}
        self.candidate_code = 0
        self.revisions = []
        self.deployments = []
        self.vaults = [{"name": "fictional-vault"}]
        self.identities = []

    def run(self, command, *, env=None, capture_output, text, timeout, check):
        self.calls.append((command, env))
        if command[0] != "az":
            self.sql_calls.append(command)
            if "--list-candidates" in command:
                return subprocess.CompletedProcess(
                    command, self.candidate_code, json.dumps(self.candidates), "")
            summary = self.sql_failure or {
                "staff_changes": 0, "owner_labels": 0, "restart_required": "--restart" not in command,
            }
            return subprocess.CompletedProcess(command, self.sql_code, json.dumps(summary), "")
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
            stderr = getattr(self, "fail_stderr", None) or f"Forbidden {TENANT} {SECRET}"
            return subprocess.CompletedProcess(command, 1, "", stderr)
        if args[0] == "rest":
            method = args[args.index("--method") + 1]
            url = args[args.index("--url") + 1]
            if body is not None and set(body) == {"tags"}:
                self.tag_writes.append(body)
            elif method != "GET" and "/listSecrets?" not in url:
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
        elif args[:3] == ["containerapp", "revision", "list"]:
            value = self.revisions
        elif args[:3] == ["deployment", "group", "list"]:
            value = self.deployments
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
            value = self.vaults
        elif args[:2] == ["identity", "list"]:
            value = self.identities
        elif args[:3] == ["keyvault", "secret", "list"]:
            assert args[args.index("--vault-name") + 1] == "fictional-vault"
            assert args[args.index("--maxresults") + 1] == "1"
            value = []
        elif args[:3] == ["keyvault", "secret", "set"]:
            assert Path(args[args.index("--file") + 1]).read_text() == SECRET
            value = {"id": "https://fictional-vault.vault.azure.net/secrets/entra-generated/version"}
        elif args[0] == "version" or args[:2] == ["extension", "show"]:
            value = {}
        else:
            raise AssertionError(f"Unexpected fake az operation: {args[:3]}")
        return subprocess.CompletedProcess(command, 0, json.dumps(copy.deepcopy(value)), "")

    def rest(self, method, url, body):
        if url == ENV_URL:
            return self.environment
        if url == AUTH_URL:
            if method == "PUT":
                self.auth = copy.deepcopy(body["properties"])
            return {"properties": self.auth}
        if url == ARM_APP:
            if method == "PATCH":
                if "tags" in body:
                    self.app["tags"] = copy.deepcopy(body["tags"])
                properties = body.get("properties", {})
                if "configuration" in properties:
                    assert body["properties"]["configuration"]["ingress"]["fqdn"] == FQDN
                    self.app["properties"]["configuration"]["secrets"] = body["properties"]["configuration"]["secrets"]
                if "template" in properties:
                    self.app["properties"]["template"] = body["properties"]["template"]
            return self.app
        if "/listSecrets?" in url:
            return {"value": [
                {"name": "preserved", "value": "preserved-private-value"}
                if s["name"] == "preserved" else copy.deepcopy(s)
                for s in self.app["properties"]["configuration"]["secrets"]]}
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
        if route == "users":
            return {"value": self.users}
        if route.startswith("users/") and route.endswith("/mailboxSettings/userPurpose"):
            return {"value": self.purposes.get(route.split("/")[1], "user")}
        if route.startswith("users/") and route != f"users/{USER}/memberOf/microsoft.graph.group":
            user_id = route.split("/")[1]
            if "/memberOf/" in route:
                return {"value": []}
            return next(u for u in self.users if u["id"] == user_id)
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
        patch.object(SETUP, "REPO", self.home / "repository").start()
        patch.object(SETUP.subprocess, "run", side_effect=self.fake.run).start()
        patch.object(SETUP.shutil, "which", return_value="/fake/az").start()
        patch.object(SETUP.time, "sleep").start()
        patch.dict(os.environ, {"AZURE_CONFIG_DIR": str(self.home / "operator")}).start()

    def write_roster(self, value):
        self.roster.write_text(json.dumps(value))
        self.roster.chmod(0o600)

    def invoke(self, *args):
        with redirect_stdout(self.output), redirect_stderr(self.output):
            code = SETUP.main(["--yes", *args])
        for sensitive in (TENANT, SUB, CLIENT, OBJECT, SP, USER, GROUP, SECRET, "preserved-private-value"):
            self.assertNotIn(sensitive, self.output.getvalue())
        return code

    def bootstrap(self):
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 0, self.output.getvalue())

    def direct(self, *, tagged=True):
        if tagged:
            self.fake.app["tags"]["zava-forward-ingress"] = "direct"
        self.fake.app["properties"]["managedEnvironmentId"] = ENV_ID
        self.fake.app["properties"]["configuration"]["ingress"]["external"] = True

    def assert_no_edge_calls(self):
        for command, _env in self.fake.calls:
            self.assertNotIn("afd", command)
            self.assertNotIn("cdn", command)

    def test_direct_flag_and_tag_need_no_frontdoor_permissions_or_extension(self):
        for tagged in (True, False):
            with self.subTest(tagged=tagged):
                self.fake = FakeAzure()
                SETUP.subprocess.run.side_effect = self.fake.run
                self.direct(tagged=tagged)
                self.fake.fail = lambda a: a[0] == "afd" or "cdn" in a
                flags = [] if tagged else ["--direct-ingress"]
                self.assertEqual(self.invoke(*flags, "--create-secret", "--secret-store", "app"),
                                 0, self.output.getvalue())
                self.assertEqual(self.fake.auth["httpSettings"]["forwardProxy"],
                                 {"convention": "NoProxy"})
                callbacks = self.fake.reg["web"]["redirectUris"]
                self.assertEqual(callbacks, [f"https://{FQDN}/.auth/login/aad/callback"])
                self.assertTrue(self.fake.sp["appRoleAssignmentRequired"])
                self.assertEqual(len(self.fake.assignments), 1)
                env = self.fake.app["properties"]["template"]["containers"][0]["env"]
                self.assertIn({"name": "ZF_ENV", "value": "production"}, env)
                self.assertIn({"name": "ZF_TRUSTED_PROXY", "value": "1"}, env)
                writes = len(self.fake.writes)
                self.assertEqual(self.invoke(*flags), 0, self.output.getvalue())
                self.assertEqual(self.invoke(*flags, "--check"), 0, self.output.getvalue())
                self.assertEqual(len(self.fake.writes), writes)
                self.assert_no_edge_calls()

    def test_direct_prefers_unique_tagged_api_and_rejects_ambiguity(self):
        self.direct()
        legacy = copy.deepcopy(self.fake.app)
        legacy["name"] = "ca-old-api"
        legacy["tags"].pop("zava-forward-ingress")
        self.fake.apps = [legacy, self.fake.app]
        self.assertEqual(self.invoke("--dry-run"), 2, self.output.getvalue())
        self.assert_no_edge_calls()
        duplicate = copy.deepcopy(self.fake.app)
        duplicate["name"] = "ca-second-demo-api"
        self.fake.apps.append(duplicate)
        self.assertEqual(self.invoke("--dry-run"), 1)
        self.assertIn("--container-app", self.output.getvalue())
        self.assertFalse(self.fake.writes)
        self.assertEqual(self.invoke("--container-app", self.fake.app["name"], "--dry-run"), 2)
        self.assert_no_edge_calls()

    def test_direct_guards_environment_origin_and_conflicting_edge(self):
        self.direct()
        self.fake.environment["properties"]["vnetConfiguration"]["internal"] = True
        self.assertEqual(self.invoke(), 1)
        self.fake.environment["properties"]["vnetConfiguration"]["internal"] = False
        self.fake.app["properties"]["configuration"]["ingress"]["external"] = False
        self.assertEqual(self.invoke(), 1)
        self.fake.app["properties"]["configuration"]["ingress"]["external"] = True
        self.assertEqual(self.invoke("--public-url", f"https://{EDGE}"), 1)
        self.assertEqual(self.invoke("--edge-profile", "afd-cutover-test"), 1)
        self.fake.app["properties"]["managedEnvironmentId"] = "/untrusted/environment"
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.writes)
        self.assert_no_edge_calls()

    def test_direct_replaces_stale_proxy_but_retains_registered_callbacks(self):
        self.bootstrap()
        callbacks = self.fake.reg["web"]["redirectUris"][:]
        for convention in ("Standard", "Custom"):
            with self.subTest(convention=convention):
                self.direct()
                self.fake.auth["httpSettings"]["forwardProxy"] = {
                    "convention": convention, "customHostHeaderName": "untrusted-host",
                    "customProtoHeaderName": "untrusted-protocol",
                }
                self.fake.calls.clear()
                self.assertEqual(self.invoke(), 0, self.output.getvalue())
                self.assertEqual(self.fake.auth["httpSettings"]["forwardProxy"],
                                 {"convention": "NoProxy"})
                self.assertEqual(self.fake.reg["web"]["redirectUris"], callbacks)
                self.assert_no_edge_calls()

    def test_direct_return401_automatically_enables_browser_unless_explicit_bearer(self):
        self.direct()
        self.fake.auth["globalValidation"]["unauthenticatedClientAction"] = "Return401"
        self.assertEqual(self.invoke("--bearer-only"), 2)
        self.assertEqual(
            self.fake.auth["globalValidation"]["unauthenticatedClientAction"], "Return401")
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertEqual(
            self.invoke("--enable-browser", "--create-secret", "--secret-store", "app"), 0)
        self.assertEqual(
            self.fake.auth["globalValidation"]["unauthenticatedClientAction"],
            "RedirectToLoginPage")
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(self.invoke("--enable-browser", "--bearer-only"), 1)
        self.assert_no_edge_calls()

    def test_missing_extensions_diagnose_only_required_isolated_install(self):
        self.direct()
        self.fake.fail = lambda a: a[:2] == ["extension", "show"] and "containerapp" in a
        self.assertEqual(self.invoke(), 1)
        self.assertIn("--name containerapp --upgrade", self.output.getvalue())
        self.assertIn("AZURE_EXTENSION_DIR=", self.output.getvalue())
        self.assertIn(str(self.profile / "cliextensions"), self.output.getvalue())
        self.assert_no_edge_calls()
        self.fake.fail = lambda a: a[:2] == ["extension", "show"] and "cdn" in a
        self.assertEqual(self.invoke("--dry-run"), 2)
        self.fake.app["tags"].pop("zava-forward-ingress")
        self.assertEqual(self.invoke("--dry-run"), 1)
        self.assertIn("--name cdn --upgrade", self.output.getvalue())
        self.assertFalse(self.fake.writes)

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

    def test_no_arguments_creates_missing_credential_without_uuid_traceback(self):
        self.assertEqual(self.invoke(), 0)
        self.assertTrue(self.fake.reg["passwordCredentials"])
        self.assertNotIn("hexadecimal", self.output.getvalue())
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], CLIENT)

    def test_managed_identity_sentinel_finds_existing_registration_and_rewires_uuid(self):
        self.bootstrap()
        self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"] = "systemAssignedIdentity"
        before = copy.deepcopy(self.fake.reg)
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(self.fake.reg, before)
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], CLIENT)
        creates = [w for w in self.fake.writes if w[:2] == ("POST", SETUP.GRAPH + "applications")]
        self.assertEqual(len(creates), 1)

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
        self.assertEqual(self.invoke("--dry-run"), 1)
        self.assertIn("Automatic demo roster refused", self.output.getvalue())

    def test_missing_roster_refuses_unknown_profile_without_creating_a_template(self):
        self.roster.unlink()
        self.roster = self.home / "new-private-roster" / "roster.json"
        SETUP.ROSTER = self.roster
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.roster.exists())
        self.assertFalse(self.roster.parent.exists())
        self.assertIn("Automatic demo roster refused", self.output.getvalue())
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)

    def test_invalid_directory_mode_and_duplicate_codes_precede_cloud_access(self):
        self.roster.parent.chmod(0o755)
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.calls)
        self.roster.parent.chmod(0o700)
        self.write_roster([{"code": "same", "userId": USER, "role": "Coordinator"},
                           {"code": "same", "userId": GROUP, "role": "SupportOfficer"}])
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.calls)

    def demo_roster(self):
        self.roster.unlink(missing_ok=True)
        self.fake.app["tags"].update({
            SETUP.PROFILE_TAG: "development", "environment": "test"})
        self.fake.candidates = [
            {"code": "PM-02", "role": "Retrofit Programme Manager", "bound": False},
            {"code": "CT-01", "role": "Contractor",
             "contractor": "Fixture Supplier", "bound": False},
            {"code": "RC-01", "role": "Coordinator", "bound": False},
            {"code": "PM-01", "role": "ProgrammeManager", "bound": False},
        ]
        self.fake.users = [self.demo_person("administrator", upn="ADMIN@example.invalid")]
        self.fake.users += [self.demo_person(f"person-{n}") for n in range(6)]

    @staticmethod
    def demo_person(key, *, upn=None, **changes):
        return {"id": uid(key), "displayName": f"Fictional Person {key}",
                "userPrincipalName": upn or f"{key}@example.invalid",
                "accountEnabled": True, "userType": "Member", **changes}

    def assert_no_generation_writes(self):
        self.assertFalse(self.roster.exists())
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)

    def test_demo_generation_seed_permissions_scope_and_no_personal_output(self):
        self.demo_roster()
        self.assertEqual(self.invoke("--seed", "178"), 0, self.output.getvalue())
        data = json.loads(self.roster.read_text())
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["seed"], 178)
        rows = data["staff"]
        self.assertEqual([r["code"] for r in rows], ["CT-01", "PM-01", "PM-02", "RC-01"])
        assigned_admin = next(r for r in rows if r["code"] == "PM-01")["userId"]
        self.assertEqual(assigned_admin, uid("administrator"))
        self.assertEqual(rows[0]["contractor"], "Fixture Supplier")
        self.assertEqual(len({r["userId"] for r in rows}), len(rows))
        self.assertEqual(self.roster.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.roster.parent.stat().st_mode & 0o777, 0o700)
        output = self.output.getvalue()
        for user in self.fake.users:
            for field in ("id", "displayName", "userPrincipalName"):
                self.assertNotIn(user[field], output)
        self.assertNotIn("Fixture Supplier", output)
        self.assertIn("ProgrammeManager: 2", output)
        self.assertIn("not evidence of professional competence", output)
        self.assertIn("replica restart: verified", output)

    def test_seed_reproducible_with_unsorted_graph_and_sql_and_rerun_never_reshuffles(self):
        self.demo_roster()
        self.assertEqual(self.invoke("--seed", "41"), 0, self.output.getvalue())
        original = self.roster.read_bytes()
        self.fake.users.reverse()
        self.fake.candidates.reverse()
        self.roster.unlink()
        self.assertEqual(self.invoke("--seed", "41"), 0, self.output.getvalue())
        self.assertEqual(self.roster.read_bytes(), original)
        self.fake.candidates = []
        self.assertEqual(self.invoke("--seed", "999"), 0, self.output.getvalue())
        self.assertEqual(self.roster.read_bytes(), original)
        self.assertIn("Reusing persisted roster", self.output.getvalue())

    def test_seed_changes_assignment_only_before_persistence(self):
        self.demo_roster()
        self.assertEqual(self.invoke("--seed", "1", "--dry-run"), 2)
        graph = SETUP.Azure(self.profile)
        candidates = SETUP.candidate_staff(
            graph, SETUP.parser().parse_args(["--roster", str(self.roster)]), self.fake.app)
        args = SETUP.parser().parse_args(["--yes", "--seed", "1", "--roster", str(self.roster)])
        with redirect_stdout(self.output):
            SETUP.generate_roster(graph, args, candidates, readonly=False, expected=None)
        first = json.loads(self.roster.read_text())["staff"]
        self.roster.unlink()
        args.seed = 2
        with redirect_stdout(self.output):
            SETUP.generate_roster(graph, args, candidates, readonly=False, expected=None)
        second = json.loads(self.roster.read_text())["staff"]
        self.assertNotEqual(first, second)

    def test_exact_template_is_replaced_but_partial_placeholders_are_rejected(self):
        self.demo_roster()
        self.write_roster(SETUP.TEMPLATE)
        self.assertEqual(self.invoke("--seed", "1"), 0, self.output.getvalue())
        self.assertIsInstance(json.loads(self.roster.read_text()), dict)
        self.fake.calls.clear()
        self.write_roster([{**SETUP.TEMPLATE[0], "code": "PM-01"}])
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.calls)

    def test_admin_none_many_and_explicit_resolution_are_private(self):
        for count in (0, 2):
            with self.subTest(count=count):
                self.demo_roster()
                self.fake.assignments.clear()
                self.fake.users = [u for u in self.fake.users
                                   if not u["userPrincipalName"].lower().startswith("admin@")]
                self.fake.users += [self.demo_person(f"admin-{n}", upn=f"admin@domain-{n}.invalid")
                                    for n in range(count)]
                self.fake.writes.clear()
                self.fake.tag_writes.clear()
                self.assertEqual(self.invoke(), 1)
                self.assertIn(f"Found {count} eligible", self.output.getvalue())
                self.assert_no_generation_writes()
                self.assertEqual(self.invoke("--admin-upn", "person-1@example.invalid"), 0,
                                 self.output.getvalue())
                rows = json.loads(self.roster.read_text())["staff"]
                assigned_admin = next(r for r in rows if r["code"] == "PM-01")["userId"]
                self.assertEqual(assigned_admin, uid("person-1"))
                self.assertNotIn("person-1@example.invalid", self.output.getvalue())

    def test_admin_ambiguity_asks_exactly_one_plain_question_then_stops_on_bad_input(self):
        self.demo_roster()
        self.fake.users = self.fake.users[1:]
        with patch.object(SETUP.sys.stdin, "isatty", return_value=True), \
                patch("builtins.input", return_value="unknown@example.invalid") as ask, \
                redirect_stdout(self.output), redirect_stderr(self.output):
            self.assertEqual(SETUP.main([]), 1)
        ask.assert_called_once_with("Which tenant administrator UPN should this demo use? ")
        self.assertNotIn("unknown@example.invalid", self.output.getvalue())
        self.assert_no_generation_writes()

    def test_explicit_admin_must_be_eligible_and_manager_code_must_exist(self):
        for changes in ({"accountEnabled": False}, {"userType": "Guest"},
                        {"displayName": "Shared Mailbox"}, {"id": "not-a-guid"}):
            self.demo_roster()
            self.fake.users[0].update(changes)
            self.assertEqual(self.invoke("--admin-upn", "admin@example.invalid"), 1)
            self.assert_no_generation_writes()
        self.demo_roster()
        self.fake.candidates = [
            r for r in self.fake.candidates if not r["code"].startswith("PM-")]
        self.assertEqual(self.invoke(), 1)
        self.assertIn("no ProgrammeManager position", self.output.getvalue())
        self.assert_no_generation_writes()

    def test_eligibility_guests_disabled_resources_shared_and_unknown_purpose(self):
        self.demo_roster()
        self.fake.users += [
            self.demo_person("guest", userType="Guest"),
            self.demo_person("disabled", accountEnabled=False),
            self.demo_person("boardroom", displayName="Meeting Room"),
            self.demo_person("desk", upn="desk.office@example.invalid"),
            self.demo_person("workspace", displayName="Main Workspace"),
            self.demo_person("shared", displayName="Shared Mailbox"),
            self.demo_person("service", displayName="Service Account"),
            self.demo_person("ordinary-looking"),
            self.demo_person("unknown-purpose"),
            self.demo_person(
                "principal-object", **{"@odata.type": "#microsoft.graph.servicePrincipal"}),
        ]
        self.fake.purposes[uid("ordinary-looking")] = "shared"
        self.fake.purposes[uid("unknown-purpose")] = "unknownFutureValue"
        graph = SETUP.Azure(self.profile)
        people = SETUP.eligible_people(graph)
        self.assertEqual(len(people), 7)
        self.assertNotIn(uid("ordinary-looking"), [p["oid"] for p in people])
        self.fake.fail = lambda args: any("/mailboxSettings/" in str(a) for a in args)
        self.assertEqual(self.invoke(), 1)
        self.assertIn("MailboxSettings.Read", self.output.getvalue())
        self.assert_no_generation_writes()

    def test_user_without_mailbox_is_skipped_not_fatal(self):
        self.demo_roster()
        self.fake.users.append(self.demo_person("ordinary-looking"))
        unlicensed = uid("ordinary-looking")
        self.fake.fail = lambda args: unlicensed in " ".join(str(a) for a in args) and any(
            "/mailboxSettings/" in str(a) for a in args
        )
        self.fake.fail_stderr = "MailboxNotEnabledForRESTAPI status code: 404"
        graph = SETUP.Azure(self.profile)
        people = SETUP.eligible_people(graph)
        self.assertNotIn(unlicensed, [p["oid"] for p in people])
        self.assertEqual(len(people), 7)

    def test_persisted_people_revalidate_mailbox_type_without_reshuffling(self):
        self.demo_roster()
        self.assertEqual(self.invoke("--seed", "7"), 0, self.output.getvalue())
        original = self.roster.read_bytes()
        self.fake.purposes[uid("administrator")] = "shared"
        self.fake.writes.clear()
        self.fake.tag_writes.clear()
        self.fake.sql_calls.clear()
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(self.roster.read_bytes(), original)
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)
        self.assertFalse(self.fake.sql_calls)

    def test_shortage_counts_only_eligible_non_admin_members_and_stops(self):
        self.demo_roster()
        self.fake.users = self.fake.users[:3]
        self.fake.users += [self.demo_person("disabled", accountEnabled=False),
                            self.demo_person("guest", userType="Guest")]
        self.assertEqual(self.invoke(), 1)
        self.assertIn("Need 3 distinct non-admin users; 2 eligible. Missing exactly 1",
                      self.output.getvalue())
        self.assert_no_generation_writes()
        self.fake.users.append(self.demo_person("enough"))
        self.assertEqual(self.invoke(), 0, self.output.getvalue())

    def test_profile_unknown_production_conflicting_and_unrelated_deployment_refused(self):
        for profile in ("production", None, "unknown"):
            self.demo_roster()
            self.fake.app["tags"].pop(SETUP.PROFILE_TAG)
            if profile:
                self.fake.app["tags"][SETUP.PROFILE_TAG] = profile
            self.fake.deployments = [{"properties": {
                "provisioningState": "Succeeded",
                "outputResources": [{"id": "/unrelated"}],
                "parameters": {"deploymentProfile": {"value": "development"}}}}]
            self.assertEqual(self.invoke(), 1)
            self.assert_no_generation_writes()
            self.assertFalse(self.fake.sql_calls)
        for params in ({}, {"deploymentProfile": {"value": "production"}}):
            self.demo_roster()
            self.fake.deployments = [{"properties": {"provisioningState": "Succeeded",
                                      "outputResources": [{"id": APP_ID}], "parameters": params}}]
            self.assertEqual(self.invoke(), 1)
            self.assert_no_generation_writes()
            self.assertFalse(self.fake.sql_calls)

    def test_deployments_with_null_properties_are_ignored(self):
        self.demo_roster()
        self.fake.deployments = [
            {"properties": None},
            {"properties": {"provisioningState": "Succeeded", "outputResources": None,
                            "parameters": None}},
            {"properties": {"provisioningState": "Failed", "outputResources": [{"id": APP_ID}],
                            "parameters": {"tags": None, "deploymentProfile": {"value": "development"},
                                           "environmentName": {"value": "test"}}}},
        ]
        self.fake.deployments[2]["properties"]["provisioningState"] = "Succeeded"
        self.assertEqual(self.invoke(), 0, self.output.getvalue())

    def test_bound_deployment_can_prove_profile_but_production_environment_overrides(self):
        self.demo_roster()
        self.fake.app["tags"].pop(SETUP.PROFILE_TAG)
        self.fake.deployments = [{"properties": {
            "provisioningState": "Succeeded", "outputResources": [{"id": APP_ID}],
            "parameters": {"deploymentProfile": {"value": "development"},
                           "environmentName": {"value": "test"}}}}]
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.demo_roster()
        self.direct()
        self.fake.environment["tags"] = {SETUP.PROFILE_TAG: "production"}
        self.fake.writes.clear()
        self.fake.tag_writes.clear()
        self.assertEqual(self.invoke(), 1)
        self.assert_no_generation_writes()

    def test_nested_module_profile_tags_are_bound_to_actual_output_resources(self):
        self.demo_roster()
        self.fake.app["tags"].pop(SETUP.PROFILE_TAG)
        self.fake.deployments = [{"properties": {
            "provisioningState": "Succeeded", "outputResources": [{"id": APP_ID}],
            "parameters": {"tags": {"value": {SETUP.PROFILE_TAG: "development",
                                             "environment": "test"}}}}}]
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.demo_roster()
        parameters = self.fake.deployments[0]["properties"]["parameters"]
        parameters["deploymentProfile"] = {"value": "production"}
        self.fake.writes.clear()
        self.fake.tag_writes.clear()
        self.assertEqual(self.invoke(), 1)
        self.assert_no_generation_writes()

    def test_persisted_generated_roster_cannot_run_in_production_either(self):
        self.demo_roster()
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        original = self.roster.read_bytes()
        self.fake.app["tags"][SETUP.PROFILE_TAG] = "production"
        self.fake.writes.clear()
        self.fake.tag_writes.clear()
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(self.roster.read_bytes(), original)
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)

    def test_bound_sql_candidate_wrong_role_duplicate_and_missing_supplier_stop_early(self):
        for changes in ({"bound": True}, {"role": "Unknown"}, {"bound": None},
                        {"code": "PM-01"}, {"contractor": ""}):
            self.demo_roster()
            self.fake.candidates[1].update(changes)
            self.assertEqual(self.invoke(), 1)
            self.assert_no_generation_writes()

    def test_readonly_generation_preview_writes_nothing_and_never_applies_sql(self):
        for mode in ("--check", "--dry-run"):
            self.demo_roster()
            self.roster = self.home / "missing-parent" / "roster.json"
            SETUP.ROSTER = self.roster
            self.assertEqual(self.invoke(mode, "--seed", "5"), 2, self.output.getvalue())
            self.assertFalse(self.roster.parent.exists())
            self.assert_no_generation_writes()
            self.assertTrue(all("--list-candidates" in cmd for cmd in self.fake.sql_calls))

    def test_generation_confirmation_decline_and_accept_once_before_sql_confirmation(self):
        self.demo_roster()
        with patch.object(SETUP.sys.stdin, "isatty", return_value=True), \
                patch("builtins.input", return_value="n") as ask, \
                redirect_stdout(self.output), redirect_stderr(self.output):
            self.assertEqual(SETUP.main([]), 1)
        ask.assert_called_once_with("Write this private demo roster? [y/N] ")
        self.assert_no_generation_writes()
        with patch.object(SETUP.sys.stdin, "isatty", return_value=True), \
                patch("builtins.input", side_effect=["y", "y"]) as ask, \
                redirect_stdout(self.output), redirect_stderr(self.output):
            self.assertEqual(SETUP.main([]), 0, self.output.getvalue())
        self.assertEqual([c.args[0] for c in ask.call_args_list], [
            "Write this private demo roster? [y/N] ",
            "Apply these SQL bindings and restart the API replicas? [y/N] "])
        output = self.output.getvalue()
        self.assertLess(output.index("Private roster saved"), output.index("4/7 Reconciling"))
        final_sql = output.rindex("SQL plan:")
        self.assertGreater(final_sql, output.index("5/7 Checking"))
        self.assertGreater(output.rindex("replica restart: verified"), final_sql)
        self.assertEqual(sum("--apply" in cmd for cmd in self.fake.sql_calls), 1)

    def test_missing_sql_candidates_prints_single_exact_safe_handoff_never_admin_upn(self):
        self.demo_roster()
        self.fake.candidate_code = 1
        self.assertEqual(self.invoke("--admin-upn", "private-admin@example.invalid",
                                     "--seed", "11", "--dry-run"), 1)
        output = self.output.getvalue()
        self.assertEqual(output.count("python3 infra/scripts/setup-entra.py "), 1)
        self.assertIn("--seed 11", output)
        self.assertIn("--dry-run", output)
        self.assertNotIn("private-admin@example.invalid", output)
        self.assertNotIn("--admin-upn", output)
        self.assert_no_generation_writes()

    def test_missing_roster_honours_remote_lock_before_candidate_sql_or_writes(self):
        self.demo_roster()
        self.fake.app["tags"][SETUP.LOCK_TAG] = "another-session"
        self.assertEqual(self.invoke(), 1)
        self.assert_no_generation_writes()
        self.assertFalse(self.fake.sql_calls)

    def test_roster_symlinks_and_changed_input_never_overwrite_private_work(self):
        self.demo_roster()
        target = self.home / "private-target.json"
        target.write_text("private-work")
        self.roster.symlink_to(target)
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(target.read_text(), "private-work")
        self.assertFalse(self.fake.calls)
        self.roster.unlink()
        self.write_roster(SETUP.TEMPLATE)
        before = self.roster.read_bytes()
        args = SETUP.parser().parse_args(["--roster", str(self.roster), "--yes"])
        graph = SETUP.Azure(self.profile)
        candidates = SETUP.candidate_staff(graph, args, self.fake.app)
        self.roster.write_text("private-work")
        with redirect_stdout(self.output), self.assertRaises(SETUP.SetupError):
            SETUP.generate_roster(graph, args, candidates, readonly=False, expected=before)
        self.assertEqual(self.roster.read_text(), "private-work")
        self.assertFalse(self.fake.writes)

    def test_generated_envelope_and_invalid_seed_are_validated_before_cloud_access(self):
        for envelope in ({"version": 2, "seed": 1, "staff": []},
                         {"version": 1, "seed": -1, "staff": []},
                         {"version": 1, "seed": True, "staff": []},
                         {"version": True, "seed": 1, "staff": []},
                         {"version": 1, "seed": 1, "staff": None}):
            self.write_roster(envelope)
            self.assertEqual(self.invoke(), 1)
            self.assertFalse(self.fake.calls)
        self.assertEqual(self.invoke("--seed", "-3"), 1)
        self.assertFalse(self.fake.calls)

    def test_direct_demo_falls_back_automatically_without_vault_flags(self):
        self.direct()
        self.fake.fail = lambda a: a[:3] == ["keyvault", "secret", "list"]
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.assertIn("using the Container App secret store", self.output.getvalue())
        self.assertEqual(self.fake.app["tags"][SETUP.STORE_TAG], "app")
        self.assertIn("value", self.fake.app["properties"]["configuration"]["secrets"][-1])
        self.assert_no_edge_calls()
        self.assertFalse(any("network-rule" in command for command, _ in self.fake.calls))
        count = len(self.fake.reg["passwordCredentials"])
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(len(self.fake.reg["passwordCredentials"]), count)

    def test_direct_fallback_also_handles_vault_write_permission_failure(self):
        self.direct()
        self.fake.fail = lambda a: a[:3] == ["keyvault", "secret", "set"]
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.assertEqual(self.fake.app["tags"][SETUP.STORE_TAG], "app")
        self.assertIn("write unavailable", self.output.getvalue())

    def test_vault_reference_precedence_and_attached_identity_selection(self):
        other = "/fictional/other-identity"
        self.fake.app["identity"]["userAssignedIdentities"][other] = {}
        self.fake.app["properties"]["configuration"]["secrets"].append({
            "name": "other", "keyVaultUrl": "https://fictional-vault.vault.azure.net/secrets/other",
            "identity": "managed-identity"})
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.assertEqual(self.fake.app["properties"]["configuration"]["secrets"][-1]["identity"],
                         "managed-identity")

    def test_vault_discovery_uses_deployment_tags_and_then_outputs(self):
        for use_outputs in (False, True):
            self.fake = FakeAzure()
            SETUP.subprocess.run.side_effect = self.fake.run
            self.fake.vaults.append({"name": "unrelated-vault", "tags": {"environment": "other"}})
            if use_outputs:
                self.fake.deployments = [{"properties": {
                    "outputs": {"keyVaultName": {"value": "fictional-vault"}}}}]
            else:
                self.fake.app["tags"]["environment"] = "test"
                self.fake.app["tags"]["workload"] = "api"
                self.fake.vaults[0]["tags"] = {"environment": "test",
                                              "workload": "zava-forward-demonstrator"}
            self.assertEqual(self.invoke(), 0, self.output.getvalue())
            self.assertEqual(self.fake.app["tags"][SETUP.STORE_TAG], "keyvault")

    def test_ambiguous_or_missing_vault_never_mints_a_credential_or_asks_for_required_flags(self):
        for vaults in ([], [{"name": "first"}, {"name": "second"}]):
            self.fake.vaults = vaults
            self.assertEqual(self.invoke(), 1)
            self.assertFalse(self.fake.reg["passwordCredentials"])
            self.assertIn("Candidates:", self.output.getvalue())

    def test_expired_credential_rotates_without_removing_in_use_old_credential(self):
        self.bootstrap()
        old = self.fake.reg["passwordCredentials"][0]
        old["endDateTime"] = "2000-01-01T00:00:00Z"
        self.assertEqual(self.invoke(), 0, self.output.getvalue())
        self.assertEqual(len(self.fake.reg["passwordCredentials"]), 2)
        self.assertNotEqual(self.fake.reg["passwordCredentials"][-1]["displayName"], old["displayName"])
        self.assertEqual(len(self.fake.app["properties"]["configuration"]["secrets"]), 3)

    def test_advisory_lock_deployment_and_revision_updates_refuse_before_auth_writes(self):
        for state in ("lock", "deployment", "revision"):
            with self.subTest(state=state):
                self.fake.app["tags"].pop(SETUP.LOCK_TAG, None)
                self.fake.revisions, self.fake.deployments = [], []
                self.fake.sql_calls.clear()
                if state == "lock":
                    self.fake.app["tags"][SETUP.LOCK_TAG] = "another-session"
                elif state == "deployment":
                    self.fake.deployments = [{"properties": {"provisioningState": "Running"}}]
                else:
                    self.fake.revisions = [{"properties": {"provisioningState": "Provisioning"}}]
                self.assertEqual(self.invoke(), 1)
                self.assertFalse(self.fake.writes)
                self.assertFalse(self.fake.sql_calls)
                self.assertEqual(self.invoke("--check"), 2)
                self.assertIn("Coordination: blocked", self.output.getvalue())
                self.assertFalse(self.fake.tag_writes)

    def test_sql_check_confirmation_apply_restart_and_post_entra_verification_order(self):
        self.assertEqual(self.invoke(), 0)
        calls = [c for c, _ in self.fake.calls]
        sql = [i for i, c in enumerate(calls) if c[0] != "az"]
        self.assertEqual(len(sql), 2)
        self.assertIn("--check", calls[sql[0]])
        self.assertIn("--apply", calls[sql[1]])
        self.assertIn("--restart", calls[sql[1]])
        verifications = [i for i, c in enumerate(calls) if "/appRoleAssignedTo" in " ".join(c)
                         and "--body" not in c]
        self.assertLess(verifications[-1], sql[0])
        self.assertNotIn(SETUP.LOCK_TAG, self.fake.app["tags"])
        self.fake.sql_calls.clear()
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(len(self.fake.sql_calls), 1)
        self.assertIn("--check", self.fake.sql_calls[0])
        self.assertEqual(self.invoke("--check"), 0)

    def test_sql_unreachable_returns_exact_private_host_command_and_incomplete_summary(self):
        self.fake.sql_code = 1
        self.assertEqual(self.invoke(), 2)
        self.assertIn("authorized host with private SQL connectivity", self.output.getvalue())
        self.assertIn("--apply --restart", self.output.getvalue())
        self.assertIn("SQL binding/restart: NOT confirmed", self.output.getvalue())
        self.assertIn("SQL public access must stay Disabled", self.output.getvalue())
        self.assertEqual(len(self.fake.sql_calls), 1)

    def test_sql_validation_failure_is_not_misreported_as_network_or_applied(self):
        self.fake.sql_code = 1
        self.fake.sql_failure = {"error": "validation"}
        self.assertEqual(self.invoke(), 2)
        self.assertIn("SQL preflight rejected the private roster", self.output.getvalue())
        self.assertNotIn("authorized host with private SQL connectivity", self.output.getvalue())
        self.assertTrue(all("--apply" not in c for c in self.fake.sql_calls))

    def test_sql_confirmation_decline_and_readonly_never_apply_or_restart(self):
        args = SETUP.parser().parse_args(["--roster", str(self.roster)])
        args.tenant_profile = self.profile
        with redirect_stdout(self.output), patch.object(SETUP.sys.stdin, "isatty", return_value=True), \
                patch("builtins.input", return_value="n") as question:
            self.assertFalse(SETUP.sql_staff_step(args, self.fake.app, readonly=False))
            question.assert_called_once()
        self.assertTrue(all("--apply" not in c for c in self.fake.sql_calls))
        self.fake.sql_calls.clear()
        self.assertEqual(self.invoke("--check"), 2)
        self.assertTrue(all("--apply" not in c and "--restart" not in c for c in self.fake.sql_calls))

    def test_staff_candidate_listing_needs_no_roster_and_prints_only_codes_roles(self):
        self.roster.unlink()
        self.assertEqual(self.invoke("--list-staff"), 0)
        self.assertIn("fictional-coordinator / Coordinator", self.output.getvalue())
        self.assertFalse(self.roster.exists())
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)

    def test_upn_lookup_saves_mapping_privately_with_read_permission_only(self):
        self.fake.permissions = {"User.Read.All"}
        self.roster.unlink()
        original = self.fake.rest

        def person(method, url, body):
            if "/users/person%40example.invalid?" in url:
                return {"id": USER, "accountEnabled": True, "userType": "Member"}
            return original(method, url, body)

        with patch.object(self.fake, "rest", side_effect=person):
            self.assertEqual(self.invoke("--lookup-upn", "person@example.invalid",
                                         "--staff-code", "fictional-coordinator",
                                         "--staff-role", "Retrofit Coordinator"), 0)
        files = list(self.roster.parent.glob("person-*.json"))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(files[0].read_text())[0]["userId"], USER)
        self.assertFalse(self.roster.exists())
        self.assertFalse(self.fake.writes)
        self.assertFalse(self.fake.tag_writes)

    def test_lost_lock_ownership_stops_and_does_not_remove_another_sessions_tag(self):
        original = self.fake.rest

        def takeover(method, url, body):
            response = original(method, url, body)
            if method == "PATCH" and body.get("tags", {}).get(SETUP.LOCK_TAG):
                self.fake.app["tags"][SETUP.LOCK_TAG] = "other-session"
            return response

        with patch.object(self.fake, "rest", side_effect=takeover):
            self.assertEqual(self.invoke(), 1)
        self.assertEqual(self.fake.app["tags"][SETUP.LOCK_TAG], "other-session")
        self.assertFalse(self.fake.writes)
        headers = [c for c, _ in self.fake.calls if "--headers" in c]
        self.assertTrue(headers)

    def test_interactive_resource_ambiguity_asks_once_without_printing_ids(self):
        rows = [{"name": "first"}, {"name": "second"}]
        with redirect_stdout(self.output), patch.object(SETUP.sys.stdin, "isatty", return_value=True), \
                patch("builtins.input", return_value="second") as question:
            selected = SETUP.choose(rows, None, "Key Vault", ".*", "--vault", interactive=True)
        self.assertEqual(selected["name"], "second")
        question.assert_called_once()

    def test_group_assignment_and_planned_user_group_conflict(self):
        self.write_roster([{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"}])
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.writes)
        self.fake.memberships = [GROUP]
        self.write_roster([{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"},
                           {"code": "fictional-officer", "userId": USER, "role": "SupportOfficer"}])
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 1)
        self.assertIn("individual userId", self.output.getvalue())
        self.assertEqual(len(self.fake.writes), count)

    def test_fresh_planned_user_group_conflict_precedes_all_directory_writes(self):
        self.fake.memberships = [GROUP]
        roster = [{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"},
                  {"code": "fictional-officer", "userId": USER, "role": "SupportOfficer"}]
        for rows in (roster, list(reversed(roster))):
            for mode in ((), ("--check",), ("--dry-run",)):
                with self.subTest(reversed=rows != roster, mode=mode):
                    self.write_roster(rows)
                    self.assertEqual(self.invoke(*mode), 1)
                    self.assertIn("individual userId", self.output.getvalue())
                    self.assertFalse(self.fake.writes)
                    self.assertIsNone(self.fake.reg)
                    self.assertIsNone(self.fake.sp)

    def test_matching_group_roles_resolve_but_sql_roster_requires_individuals(self):
        self.fake.memberships = [GROUP]
        self.write_roster([{"code": "fictional-team", "groupId": GROUP, "role": "Coordinator"},
                           {"code": "fictional-officer", "userId": USER, "role": "Coordinator"}])
        rows = SETUP.read_roster(self.roster, {"Coordinator"})
        graph = SETUP.Azure(self.profile)
        self.assertEqual(len(SETUP.resolve_roster(graph, rows)), 2)
        self.assertEqual(self.invoke("--check"), 1)
        self.assertEqual(self.invoke(), 1)
        self.assertFalse(self.fake.writes)

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

    def test_secret_failure_never_activates_and_rerun_recovers_with_distinct_pair(self):
        self.fake.fail = lambda a: (a[0] == "rest" and a[a.index("--method") + 1] == "PATCH"
                                   and a[a.index("--url") + 1] == ARM_APP
                                   and "configuration" in json.loads(Path(a[a.index("--body") + 1][1:]).read_text()).get("properties", {}))
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"], "systemAssignedIdentity")
        self.fake.fail = None
        count = len(self.fake.reg["passwordCredentials"])
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 0)
        self.assertEqual(len(self.fake.reg["passwordCredentials"]), count + 1)
        credentials = self.fake.reg["passwordCredentials"]
        self.assertNotEqual(credentials[-1]["displayName"], credentials[-2]["displayName"])
        self.assertFalse(list(self.profile.iterdir()))

    def test_keyvault_credential_storage_no_secret_argv_and_identity_validation(self):
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 0, self.output.getvalue())
        secret = self.fake.app["properties"]["configuration"]["secrets"][-1]
        self.assertIn("keyVaultUrl", secret)
        self.assertNotIn("value", secret)
        count = len(self.fake.writes)
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(len(self.fake.writes), count)

    def test_unreachable_vault_preflight_prevents_one_time_credential(self):
        self.fake.fail = lambda a: a[:3] in (["keyvault", "secret", "list"],
                                            ["keyvault", "secret", "set"])
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 1)
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertFalse(any("/addPassword" in url for _, url, _ in self.fake.writes))
        self.assertIn("Private Key Vault preflight failed", self.output.getvalue())
        self.assertEqual(self.fake.auth["identityProviders"]["azureActiveDirectory"]["registration"]["clientId"],
                         "systemAssignedIdentity")
        self.assertFalse(list(self.profile.iterdir()))
        self.fake.fail = None
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 0)

    def test_vault_metadata_probe_precedes_password_and_is_not_repeated_on_rerun(self):
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 0)
        commands = [command for command, _ in self.fake.calls]
        probe = next(i for i, c in enumerate(commands) if c[1:4] == ["keyvault", "secret", "list"])
        password = next(i for i, c in enumerate(commands) if any("/addPassword" in arg for arg in c))
        self.assertLess(probe, password)
        self.fake.calls.clear()
        self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 0)
        self.assertFalse(any(c[1:4] == ["keyvault", "secret", "list"] for c, _ in self.fake.calls))

    def test_vault_endpoint_timeout_creates_no_credential_and_readonly_only_probes_metadata(self):
        original = self.fake.run
        def timeout(command, **kwargs):
            if command[1:4] == ["keyvault", "secret", "list"]:
                raise subprocess.TimeoutExpired("az", 120)
            return original(command, **kwargs)
        with patch.object(SETUP.subprocess, "run", side_effect=timeout):
            self.assertEqual(self.invoke("--create-secret", "--vault-identity", "managed-identity"), 1)
        self.assertFalse(self.fake.reg["passwordCredentials"])
        self.assertFalse(any("/addPassword" in url for _, url, _ in self.fake.writes))
        self.fake.calls.clear()
        count = len(self.fake.writes)
        for mode in ("--check", "--dry-run"):
            self.assertEqual(self.invoke(mode, "--create-secret",
                                         "--vault-identity", "managed-identity"), 2)
        self.assertEqual(len(self.fake.writes), count)
        self.assertTrue(any(c[1:4] == ["keyvault", "secret", "list"] for c, _ in self.fake.calls))

    def test_attached_vault_identity_is_discovered_without_flags(self):
        self.assertEqual(self.invoke(), 0)
        self.assertTrue(self.fake.reg["passwordCredentials"])
        self.assertEqual(self.fake.app["properties"]["configuration"]["secrets"][-1]["identity"],
                         "managed-identity")

    def test_unverified_runtime_rollout_is_not_success(self):
        self.fake.app["properties"]["provisioningState"] = "Failed"
        self.assertEqual(self.invoke("--create-secret", "--secret-store", "app"), 1)
        self.assertIn("provisioning/revision update", self.output.getvalue())
        self.assertFalse(list(self.profile.iterdir()))

    def test_converged_runtime_requires_successful_provisioning_in_every_mode(self):
        self.bootstrap()
        count = len(self.fake.writes)
        for state in ("Failed", "Updating", "InProgress", "Canceled", None):
            for mode in ((), ("--check",), ("--dry-run",)):
                with self.subTest(state=state, mode=mode):
                    self.fake.app["properties"]["provisioningState"] = state
                    self.assertEqual(self.invoke(*mode), 2 if mode else 1)
                    self.assertIn("provisioning/revision update", self.output.getvalue())
                    self.assertEqual(len(self.fake.writes), count)
        self.fake.app["properties"]["provisioningState"] = "Succeeded"
        self.assertEqual(self.invoke("--check"), 0)
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(len(self.fake.writes), count)

    def test_pending_edge_custom_forward_headers_and_public_url_fit(self):
        proxy = {"convention": "Custom", "customHostHeaderName": "X-Forwarded-Host",
                 "customProtoHeaderName": "X-Forwarded-Proto"}
        self.fake.auth["httpSettings"]["forwardProxy"] = copy.deepcopy(proxy)
        self.assertEqual(self.invoke("--public-url", f"https://{EDGE}",
                                     "--create-secret", "--secret-store", "app"), 0)
        self.assertEqual(self.fake.auth["httpSettings"]["forwardProxy"], proxy)
        self.assertIn(f"https://{EDGE}/.auth/login/aad/callback", self.fake.reg["web"]["redirectUris"])
        count = len(self.fake.writes)
        self.assertEqual(self.invoke("--public-url", f"https://{EDGE}", "--check"), 0)
        self.assertEqual(self.invoke("--public-url", f"https://{EDGE}"), 0)
        self.assertEqual(len(self.fake.writes), count)

    def test_legacy_cli_delegates_public_url_without_reimplementing_setup(self):
        path = Path(__file__).resolve().parents[1] / "scripts" / "initialize-api-auth.py"
        spec = importlib.util.spec_from_file_location("legacy_api_auth", path)
        assert spec and spec.loader
        legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy)
        args = [str(path), "--public-url", f"https://{EDGE}", "--check"]
        main = unittest.mock.Mock(return_value=2)
        with (patch("sys.argv", args),
              patch("runpy.run_path", return_value={"main": main}) as run):
            self.assertEqual(legacy.main(), 2)
            self.assertEqual(SETUP.sys.argv, args)
        run.assert_called_once_with(str(path.with_name("setup-entra.py")))
        main.assert_called_once_with()

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

    def test_missing_afd_command_reports_isolated_cdn_install_without_mutations(self):
        original = self.fake.run

        def missing_afd(command, **kwargs):
            if command[1] == "afd":
                return subprocess.CompletedProcess(
                    command, 2, "",
                    f"ERROR: 'afd' is misspelled or not recognized by the system.\n{TENANT} {SECRET}")
            return original(command, **kwargs)

        with patch.object(SETUP.subprocess, "run", side_effect=missing_afd):
            self.assertEqual(self.invoke(), 1)
        self.assertIn("az extension add --name cdn --upgrade", self.output.getvalue())
        self.assertIn("AZURE_EXTENSION_DIR=$HOME/.azure/zava-entra-init/cliextensions",
                      self.output.getvalue())
        self.assertFalse(self.fake.writes)

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
                  self.assertRaisesRegex(SETUP.SetupError, "could not run or timed out|network")):
                cli.call(["version"])
        with (patch.object(SETUP.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, SECRET, "")),
              self.assertRaisesRegex(SETUP.SetupError, "invalid JSON")):
            cli.call(["version"])

    def test_device_login_only_prints_device_prompt_and_uses_isolated_profile(self):
        process = unittest.mock.Mock()
        process.wait.return_value = 0

        def start_login(args, **kwargs):
            suppressed = ("--only-show-errors" in args
                          or kwargs["env"]["AZURE_CORE_ONLY_SHOW_ERRORS"] != "false")
            prompt = "" if suppressed else (
                "To sign in, use a web browser to open https://microsoft.com/devicelogin "
                "and enter the code ABCD12345 to authenticate.\n")
            process.stdout = io.StringIO(f"{prompt}{TENANT} {SECRET}\n")
            return process

        with (patch.dict(os.environ, AZURE_CORE_ONLY_SHOW_ERRORS="true"),
              patch.object(SETUP.subprocess, "Popen", side_effect=start_login) as popen,
              redirect_stdout(self.output)):
            SETUP.device_login(SETUP.Azure(self.profile), TENANT)
        self.assertIn("ABCD12345", self.output.getvalue())
        self.assertNotIn(TENANT, self.output.getvalue())
        self.assertNotIn(SECRET, self.output.getvalue())
        self.assertEqual(popen.call_args.kwargs["env"]["AZURE_CONFIG_DIR"], str(self.profile))
        self.assertIn("--use-device-code", popen.call_args.args[0])
        self.assertEqual(SETUP.Azure(self.profile).environment()["AZURE_CORE_ONLY_SHOW_ERRORS"], "true")

    def test_bicep_discovery_tags_exist(self):
        infra = Path(__file__).resolve().parents[1]
        self.assertIn("'zava-forward-role': 'api'", (infra / "modules/containerapps.bicep").read_text())
        self.assertEqual((infra / "modules/edge.bicep").read_text().count("'zava-forward-role': 'api-edge'"), 2)


if __name__ == "__main__":
    unittest.main()
