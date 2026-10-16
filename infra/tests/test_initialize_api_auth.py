"""Callback initialization never replaces registrations, roles or credentials."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "initialize_api_auth", Path(__file__).resolve().parents[1] / "scripts" / "initialize-api-auth.py",
)
assert SPEC is not None and SPEC.loader is not None
INIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INIT)
TENANT = "11111111-1111-1111-1111-111111111111"
CLIENT = "22222222-2222-2222-2222-222222222222"
OBJECT = "33333333-3333-3333-3333-333333333333"
FQDN = "api.test.uksouth.azurecontainerapps.io"
CALLBACK = f"https://{FQDN}/.auth/login/aad/callback"


class InitializationTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.operator = Path(directory.name) / "operator"
        self.profile = Path(directory.name) / "tenant"
        self.graph_tenant = TENANT
        self.enabled = True
        self.proxy = "Custom"
        self.proxy_host = "X-Forwarded-Host"
        self.proxy_proto = "X-Forwarded-Proto"
        self.fqdn = FQDN
        self.client = CLIENT
        self.application = {
            "id": OBJECT, "appId": CLIENT,
            "web": {"redirectUris": ["https://old.example.test/callback"],
                    "logoutUrl": "https://old.example.test/logout",
                    "implicitGrantSettings": {"enableIdTokenIssuance": True}},
            "appRoles": [{"id": "stable-role", "value": "Existing.Manager"}],
            "passwordCredentials": [{"keyId": "preserved-key"}],
        }
        self.snapshot = copy.deepcopy(self.application)
        self.writes: list[list[str]] = []
        self.calls: list[tuple[list[str], Path]] = []
        self.verify_update = True
        self.read_error = False
        self.write_error = False
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {"AZURE_CONFIG_DIR": str(self.operator)}).start()
        patch.object(INIT, "_json", side_effect=self._read).start()
        patch.object(INIT, "_azure", side_effect=self._write).start()
        patch.object(INIT.time, "sleep").start()

    def _read(self, args: list[str], profile: Path) -> dict[str, object]:
        self.calls.append((args, profile))
        if args[:2] == ["account", "show"]:
            return {"tenantId": TENANT if profile == self.operator else self.graph_tenant}
        if args[:2] == ["containerapp", "show"]:
            self.assertEqual(profile, self.operator)
            return {"fqdn": self.fqdn}
        if args[:3] == ["containerapp", "auth", "show"]:
            self.assertEqual(profile, self.operator)
            return {"enabled": self.enabled, "clientId": self.client, "proxy": self.proxy,
                    "proxyHost": self.proxy_host, "proxyProto": self.proxy_proto}
        self.assertEqual(args[:3], ["ad", "app", "show"])
        self.assertEqual(profile, self.profile)
        self.assertEqual(args[args.index("--id") + 1], CLIENT)
        if self.read_error:
            raise RuntimeError("Insufficient privileges")
        return copy.deepcopy(self.application)

    def _write(self, args: list[str], profile: Path, *, output: str) -> str:
        self.assertEqual(profile, self.profile)
        self.assertEqual(output, "none")
        self.assertEqual(args[:3], ["rest", "--method", "PATCH"])
        self.assertEqual(args[args.index("--url") + 1],
                         f"https://graph.microsoft.com/v1.0/applications/{OBJECT}")
        if self.write_error:
            raise RuntimeError("Graph PATCH denied")
        self.writes.append(args)
        body = json.loads(args[args.index("--body") + 1])
        self.assertTrue(set(body).issubset({"web", "requiredResourceAccess"}))
        if "web" in body:
            self.assertEqual(set(body["web"]), {"redirectUris"})
        if self.verify_update:
            if "web" in body:
                self.application["web"]["redirectUris"] = body["web"]["redirectUris"]
            if "requiredResourceAccess" in body:
                self.application["requiredResourceAccess"] = body["requiredResourceAccess"]
        return ""

    def run_init(self, *, login: bool = False, check: bool = False, account_photo: bool = False) -> dict[str, str]:
        return INIT.initialize("ama", "ca-forward-test-api", tenant_profile=self.profile,
                               login=login, check=check, account_photo=account_photo)

    def test_own_photo_merges_only_user_read_and_preserves_other_permissions(self):
        existing = [{"resourceAppId": "other-api", "resourceAccess": [{"id": "other-grant", "type": "Role"}]},
                    {"resourceAppId": INIT.GRAPH_ID, "resourceAccess": [{"id": "old-scope", "type": "Scope"}]}]
        self.application["requiredResourceAccess"] = copy.deepcopy(existing)
        self.assertEqual(self.run_init(account_photo=True)["status"], "updated")
        actual = self.application["requiredResourceAccess"]
        self.assertEqual(actual[0], existing[0])
        self.assertEqual(actual[1]["resourceAccess"], [*existing[1]["resourceAccess"], {"id": INIT.USER_READ, "type": "Scope"}])
        self.assertEqual(self.run_init(account_photo=True, check=True)["status"], "already-initialized")
        self.assertEqual(len(self.writes), 1)
        self.assertEqual(self.application["appRoles"], self.snapshot["appRoles"])
        self.assertEqual(self.application["passwordCredentials"], self.snapshot["passwordCredentials"])

    def test_own_photo_check_is_read_only_and_invalid_permissions_fail_closed(self):
        self.application["web"]["redirectUris"].append(CALLBACK)
        with self.assertRaisesRegex(RuntimeError, "User.Read is missing"):
            self.run_init(account_photo=True, check=True)
        self.assertFalse(self.writes)
        for bad in ("invalid", [{"resourceAppId": "api"}]):
            self.application["requiredResourceAccess"] = bad
            with self.assertRaises(ValueError):
                self.run_init(account_photo=True)
        self.assertFalse(self.writes)

    def test_initialization_preserves_settings_and_rerun_does_not_write(self) -> None:
        self.assertEqual(self.run_init()["status"], "updated")
        self.assertEqual(self.application["web"]["redirectUris"],
                         ["https://old.example.test/callback", CALLBACK])
        self.assertEqual(self.run_init()["status"], "already-initialized")
        self.assertEqual(len(self.writes), 1)
        for field in ("appRoles", "passwordCredentials", "id", "appId"):
            self.assertEqual(self.application[field], self.snapshot[field])
        self.assertEqual(self.application["web"]["logoutUrl"], self.snapshot["web"]["logoutUrl"])
        self.assertEqual(self.application["web"]["implicitGrantSettings"],
                         self.snapshot["web"]["implicitGrantSettings"])

    def test_check_missing_callback_fails_without_writes(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "Callback is missing"):
            self.run_init(check=True)
        self.assertFalse(self.writes)

    def test_check_existing_callback_is_read_only(self) -> None:
        self.application["web"]["redirectUris"].append(CALLBACK)
        self.assertEqual(self.run_init(check=True)["status"], "already-initialized")
        self.assertFalse(self.writes)

    def test_recreated_environment_adds_its_new_callback_without_dropping_previous(self) -> None:
        self.run_init()
        self.fqdn = "api.recreated.uksouth.azurecontainerapps.io"
        self.run_init()
        self.assertEqual(self.application["web"]["redirectUris"],
                         ["https://old.example.test/callback", CALLBACK,
                          f"https://{self.fqdn}/.auth/login/aad/callback"])

    def test_edge_callback_preserves_origin_callbacks_and_is_idempotent(self) -> None:
        self.run_init()
        result = INIT.initialize("ama", "api", tenant_profile=self.profile,
                                 public_url="https://edge.example.test/")
        self.assertEqual(result["callback"], "https://edge.example.test/.auth/login/aad/callback")
        self.assertIn(CALLBACK, self.application["web"]["redirectUris"])
        self.assertEqual(INIT.initialize("ama", "api", tenant_profile=self.profile,
                                        public_url="https://edge.example.test", check=True)["status"],
                         "already-initialized")
        self.assertEqual(len(self.writes), 2)
        self.assertEqual(self.application["appRoles"], self.snapshot["appRoles"])
        self.assertEqual(self.application["passwordCredentials"], self.snapshot["passwordCredentials"])

    def test_edge_requires_trusted_proxy_and_rejects_unsafe_origins(self) -> None:
        for convention, host, proto in (
            ("NoProxy", self.proxy_host, self.proxy_proto),
            ("Standard", self.proxy_host, self.proxy_proto),
            ("Custom", "Forwarded", self.proxy_proto),
            ("Custom", self.proxy_host, "Forwarded"),
            ("Custom", None, None),
        ):
            self.proxy, self.proxy_host, self.proxy_proto = convention, host, proto
            with self.subTest(convention=convention, host=host, proto=proto), self.assertRaisesRegex(ValueError, "forwardProxy"):
                INIT.initialize("ama", "api", tenant_profile=self.profile,
                                public_url="https://edge.example.test")
        self.proxy, self.proxy_host, self.proxy_proto = "Custom", "X-Forwarded-Host", "X-Forwarded-Proto"
        for url in ("http://edge.example.test", "https://user@edge.example.test",
                    "https://edge.example.test:443", "https://edge.example.test/path",
                    "https://edge.example.test?x=1", "https://edge.example.test#fragment",
                    "https://*.example.test", "https://edge..test", "https://127.0.0.1:8088"):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "Public URL"):
                INIT.initialize("ama", "api", tenant_profile=self.profile, public_url=url)
        self.assertFalse(self.writes)

    def test_tenant_mismatch_fails_before_registration_access(self) -> None:
        self.graph_tenant = "44444444-4444-4444-4444-444444444444"
        with self.assertRaisesRegex(ValueError, "Tenant profile does not match"):
            self.run_init()
        self.assertFalse(self.writes)
        self.assertFalse(any(args[0] == "ad" for args, _ in self.calls))

    def test_different_returned_client_is_rejected(self) -> None:
        self.application["appId"] = "44444444-4444-4444-4444-444444444444"
        with self.assertRaisesRegex(ValueError, "different registration"):
            self.run_init()
        self.assertFalse(self.writes)

    def test_graph_read_denial_is_not_success(self) -> None:
        self.read_error = True
        with self.assertRaisesRegex(RuntimeError, "Insufficient privileges"):
            self.run_init()
        self.assertFalse(self.writes)

    def test_patch_denial_is_not_success(self) -> None:
        self.write_error = True
        with self.assertRaisesRegex(RuntimeError, "PATCH denied"):
            self.run_init()

    def test_unverified_patch_is_not_success(self) -> None:
        self.verify_update = False
        with self.assertRaisesRegex(RuntimeError, "could not be verified"):
            self.run_init()

    def test_disabled_auth_empty_client_and_invalid_host_do_not_write(self) -> None:
        self.enabled = False
        with self.assertRaisesRegex(ValueError, "authentication is disabled"):
            self.run_init()
        self.enabled = True
        self.client = ""
        with self.assertRaisesRegex(ValueError, "invalid clientId"):
            self.run_init()
        self.client = CLIENT
        self.fqdn = "example.test/another-path"
        with self.assertRaisesRegex(ValueError, "invalid ingress FQDN"):
            self.run_init()
        self.assertFalse(self.writes)

    def test_login_uses_isolated_device_code_profile(self) -> None:
        with patch.object(INIT.subprocess, "run") as login:
            self.run_init(login=True)
        self.assertEqual(self.profile.stat().st_mode & 0o077, 0)
        self.assertIn("--use-device-code", login.call_args.args[0])
        self.assertEqual(login.call_args.kwargs["env"]["AZURE_CONFIG_DIR"], str(self.profile))

    def test_login_cannot_overwrite_operator_profile(self) -> None:
        with patch.object(INIT.subprocess, "run") as login:
            with self.assertRaisesRegex(ValueError, "overwrite the deployment"):
                INIT.initialize("ama", "api", tenant_profile=self.operator, login=True)
        login.assert_not_called()

    def test_cli_error_includes_stderr_and_is_not_swallowed(self) -> None:
        with patch.object(INIT.subprocess, "run", return_value=subprocess.CompletedProcess(
            ["az"], 1, "", "permission denied",
        )):
            with self.assertRaisesRegex(RuntimeError, "permission denied"):
                self._azure_function(["ad", "app", "show"], self.profile)

    _azure_function = staticmethod(INIT._azure)


if __name__ == "__main__":
    unittest.main()
