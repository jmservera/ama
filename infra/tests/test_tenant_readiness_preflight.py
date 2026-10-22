"""Tenant readiness preflight is read-only, sanitized and honest about unavailable capability."""

import ast
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "tenant_readiness_preflight",
    ROOT / "infra" / "scripts" / "tenant-readiness-preflight.py",
)
assert SPEC is not None and SPEC.loader is not None
PRE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRE)

TENANT = "11111111-1111-1111-1111-111111111111"
CLIENT = "22222222-2222-2222-2222-222222222222"
OBJECT = "33333333-3333-3333-3333-333333333333"
UPN = "synthetic.person@example.invalid"
SECRET = "synthetic-secret-sentinel"
FQDN = "api.test.uksouth.azurecontainerapps.io"
EDGE = "edge.example.test"
CALLBACK = f"https://{FQDN}/.auth/login/aad/callback"
EDGE_CALLBACK = f"https://{EDGE}/.auth/login/aad/callback"
CONTRACT = PRE.load_contract(PRE.MANIFEST)
ROLES = CONTRACT["roles"]


def role(value: str, **override: object) -> dict[str, object]:
    return {"value": value, "isEnabled": True, "allowedMemberTypes": ["User"], **override}


class Fake:
    """Canned Azure CLI transport that records every argv it is given."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []
        self.account: object = {"tenantId": TENANT}
        self.fqdn: object = {"fqdn": FQDN}
        self.auth: object = {
            "enabled": True,
            "clientId": CLIENT,
            "issuer": f"https://login.microsoftonline.com/{TENANT}/v2.0",
            "secretSet": True,
            "audiences": [f"api://{CLIENT}", CLIENT],
            "proxy": "Custom",
            "proxyHost": "X-Forwarded-Host",
            "proxyProto": "X-Forwarded-Proto",
        }
        self.probe: object = {"value": [{"appId": OBJECT}]}
        self.registration: object = {
            "appId": CLIENT,
            "signInAudience": "AzureADMyOrg",
            "identifierUris": [f"api://{CLIENT}"],
            "api": {"requestedAccessTokenVersion": 2},
            "web": {"redirectUris": [CALLBACK, EDGE_CALLBACK]},
            "appRoles": [role(v) for v in ROLES],
        }
        self.principal: object = {"value": [{"appRoleAssignmentRequired": True}]}
        self.errors: dict[str, tuple[int, str]] = {}

    def __call__(self, argv: list[str]) -> tuple[int, str, str]:
        self.calls.append(argv)
        if argv[0] == "account":
            key, payload = "account", self.account
        elif argv[:2] == ["containerapp", "show"]:
            key, payload = "fqdn", self.fqdn
        elif argv[:3] == ["containerapp", "auth", "show"]:
            key, payload = "auth", self.auth
        elif "$top=1" in argv[4]:
            key, payload = "probe", self.probe
        elif "/servicePrincipals?" in argv[4]:
            key, payload = "principal", self.principal
        else:
            reg = self.registration
            key, payload = "registration", {"value": [] if reg is None else [reg]}
        if key in self.errors:
            return self.errors[key][0], "", self.errors[key][1]
        return 0, json.dumps(payload), ""


def report(fake: Fake, public_url: str | None = None) -> dict[str, PRE.Finding]:
    findings = PRE.run(PRE.Az(fake), "ama", "api", CONTRACT, public_url)
    return {f.check: f for f in findings}


class GuardTests(unittest.TestCase):
    def test_full_run_emits_only_guarded_read_templates(self) -> None:
        fake = Fake()
        report(fake, f"https://{EDGE}")
        self.assertGreaterEqual(len(fake.calls), 6)
        for argv in fake.calls:
            PRE.guard(argv)
            self.assertNotIn("PATCH", argv)

    def test_rejects_everything_that_is_not_an_exact_read_template(self) -> None:
        graph = PRE.GRAPH
        bad = [
            ["login"],
            ["ad", "app", "credential", "reset", "--id", CLIENT, "--query", "password"],
            ["keyvault", "secret", "show", "--name", "x"],
            ["account", "show"],
            ["account", "show", "--query", "{tenantId:tenantId}", "--debug"],
            ["containerapp", "show", "-g", "ama", "-n", "api"],
            ["containerapp", "show", "-g", "ama", "-n", "api", "--query", "properties"],
            ["containerapp", "secret", "list", "-g", "ama", "-n", "api"],
            ["containerapp", "auth", "show", "-g", "ama", "-n", "api", "--query", "@"],
            ["containerapp", "show", "-g", "a;b", "-n", "api", "--query", PRE.FQDN_QUERY],
            ["rest", "--method", "PATCH", "--url", f"{graph}/applications/{OBJECT}"],
            ["rest", "--method", "POST", "--url", f"{graph}/applications/{OBJECT}/addPassword"],
            ["rest", "--method", "GET", "--url", f"{graph}/applications"],
            ["rest", "--method", "GET", "--url", f"{graph}/users?$top=1&$select=appId"],
            [
                "rest",
                "--method",
                "GET",
                "--url",
                "https://example.test/applications?$top=1&$select=appId",
            ],
            [
                "rest",
                "--method",
                "GET",
                "--url",
                f"{graph}/applications?$filter=appId eq '{CLIENT}'&$select=passwordCredentials",
            ],
            [
                "rest",
                "--method",
                "GET",
                "--url",
                f"{graph}/applications?$filter=appId eq '{CLIENT}'"
                f"&$select={PRE.APP_SELECT}&$expand=owners",
            ],
            [
                "rest",
                "--method",
                "GET",
                "--url",
                f"{graph}/applications?$top=1&$select=appId",
                "--body",
                "{}",
            ],
            [
                "rest",
                "--method",
                "GET",
                "--url",
                f"{graph}/servicePrincipals/{OBJECT}/appRoleAssignedTo",
            ],
        ]
        for argv in bad:
            with self.subTest(argv=argv), self.assertRaises(PRE.ReadOnlyViolation):
                PRE.guard(argv)

    def test_guard_runs_before_transport(self) -> None:
        fake = Fake()
        with self.assertRaises(PRE.ReadOnlyViolation):
            PRE.Az(fake).read(["rest", "--method", "PATCH", "--url", PRE.GRAPH])
        self.assertEqual(fake.calls, [])


class AudienceTests(unittest.TestCase):
    def audience(self, value: object) -> PRE.Finding:
        fake = Fake()
        fake.auth["clientId"] = value  # type: ignore[index]
        return report(fake)["api-audience"]

    def test_uuid_is_ready_and_enables_graph_checks(self) -> None:
        fake = Fake()
        result = report(fake)
        self.assertEqual(result["api-audience"].status, "ready")
        self.assertEqual(result["graph-application"].status, "ready")
        self.assertEqual(PRE.overall(list(result.values())), "ready")

    def test_system_assigned_identity_is_a_blocker_that_skips_graph(self) -> None:
        fake = Fake()
        fake.auth["clientId"] = "systemAssignedIdentity"  # type: ignore[index]
        result = report(fake)
        self.assertEqual(result["api-audience"].status, "mismatch")
        self.assertEqual(result["api-audience"].reason, "system-assigned-identity-literal")
        for check in (
            "graph-application",
            "graph-app-roles",
            "graph-callback",
            "api-audience-allowed",
        ):
            self.assertEqual(
                (result[check].status, result[check].reason), ("unknown", "blocked-by-api-audience")
            )
        self.assertEqual(PRE.overall(list(result.values())), "blocked")
        self.assertFalse(
            any("rest" in c for c in fake.calls if "applications?$filter" in " ".join(c))
        )

    def test_absent_and_malformed_audiences(self) -> None:
        self.assertEqual(self.audience(None).status, "absent")
        self.assertEqual(self.audience("").status, "absent")
        for value in (f"{{{CLIENT}}}", f" {CLIENT}", "SYSTEMASSIGNEDIDENTITY", "not-a-uuid", 7):
            with self.subTest(value=value):
                self.assertEqual(
                    (self.audience(value).status, self.audience(value).reason),
                    ("mismatch", "audience-invalid"),
                )

    def test_uppercase_uuid_is_accepted(self) -> None:
        self.assertEqual(self.audience(CLIENT.upper()).status, "ready")

    def test_allowed_audience_must_contain_client(self) -> None:
        fake = Fake()
        fake.auth["audiences"] = ["api://other"]  # type: ignore[index]
        self.assertEqual(report(fake)["api-audience-allowed"].status, "mismatch")

    def test_credential_setting_is_a_boolean_only(self) -> None:
        fake = Fake()
        fake.auth["secretSet"] = False  # type: ignore[index]
        self.assertEqual(report(fake)["api-credential-setting"].status, "absent")

    def test_issuer_must_be_exact_authority_and_tenant_path(self) -> None:
        bad = [
            f"https://attacker.invalid/login.microsoftonline.com/{TENANT}/v2.0",
            f"http://login.microsoftonline.com/{TENANT}/v2.0",
            f"https://user@login.microsoftonline.com/{TENANT}/v2.0",
            f"https://login.microsoftonline.com:444/{TENANT}/v2.0",
            f"https://login.microsoftonline.com/{TENANT}/v2.0?x=1",
            f"https://login.microsoftonline.com/{TENANT}/v2.0#x",
            f"https://login.microsoftonline.com.attacker.invalid/{TENANT}/v2.0",
            f"https://login.microsoftonline.com/{TENANT}/v2.0/extra",
            f"https://login.microsoftonline.com/x/{TENANT}/v2.0",
        ]
        for issuer in bad:
            with self.subTest(issuer=issuer):
                fake = Fake()
                fake.auth["issuer"] = issuer  # type: ignore[index]
                self.assertNotEqual(report(fake)["api-issuer-tenant"].status, "ready")
        fake = Fake()
        fake.auth["issuer"] = f"https://login.microsoftonline.com/{TENANT}/v2.0/"  # type: ignore[index]
        self.assertEqual(report(fake)["api-issuer-tenant"].status, "ready")

    def test_issuer_tenant_mismatch(self) -> None:
        fake = Fake()
        fake.auth["issuer"] = f"https://login.microsoftonline.com/{OBJECT}/v2.0"  # type: ignore[index]
        self.assertEqual(report(fake)["api-issuer-tenant"].status, "mismatch")


class RoleContractTests(unittest.TestCase):
    def test_contract_matches_runtime_role_maps(self) -> None:
        tree = ast.parse(
            (ROOT / "src/api/src/zava_forward/api/auth.py").read_text(encoding="utf-8")
        )
        runtime: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in {"DEFAULT_ROLE_MAP", "RULE_ROLE_MAP"}
                for t in node.targets
            ):
                runtime |= set(ast.literal_eval(node.value))
        self.assertEqual(set(ROLES), runtime)
        self.assertEqual(len(ROLES), 12)

    def roles(self, roles: list[object]) -> PRE.Finding:
        fake = Fake()
        fake.registration["appRoles"] = roles  # type: ignore[index]
        return report(fake)["graph-app-roles"]

    def test_complete_contract_is_ready(self) -> None:
        self.assertEqual(self.roles([role(v) for v in ROLES]).status, "ready")

    def test_missing_disabled_wrong_type_duplicate_and_extra(self) -> None:
        full = [role(v) for v in ROLES]
        missing = self.roles(full[1:])
        self.assertEqual((missing.status, missing.facts["missing"]), ("mismatch", [ROLES[0]]))
        disabled = self.roles([role(ROLES[0], isEnabled=False), *full[1:]])
        self.assertEqual(disabled.facts["disabled"], [ROLES[0]])
        wrong = self.roles([role(ROLES[0], allowedMemberTypes=["Application"]), *full[1:]])
        self.assertEqual(wrong.facts["wrong_member_type"], [ROLES[0]])
        duplicate = self.roles([*full, role(ROLES[0])])
        self.assertEqual(duplicate.facts["duplicate"], [ROLES[0]])
        extra = self.roles([*full, role("ZavaForward.Invented")])
        self.assertEqual((extra.status, extra.facts["extra"]), ("mismatch", 1))
        unrelated = self.roles([*full, role("Existing.Manager")])
        self.assertEqual(unrelated.status, "ready")

    def test_registration_checks_and_service_principal(self) -> None:
        fake = Fake()
        fake.registration["signInAudience"] = "AzureADMultipleOrgs"  # type: ignore[index]
        fake.registration["identifierUris"] = []  # type: ignore[index]
        fake.registration["api"] = {"requestedAccessTokenVersion": 1}  # type: ignore[index]
        fake.principal = {"value": [{"appRoleAssignmentRequired": False}]}
        result = report(fake)
        for check in (
            "graph-sign-in-audience",
            "graph-identifier-uri",
            "graph-token-version",
            "graph-service-principal",
        ):
            self.assertEqual(result[check].status, "mismatch", check)


class CallbackTests(unittest.TestCase):
    def test_ingress_callback_present_without_proxy_requirement(self) -> None:
        result = report(Fake())
        self.assertEqual(result["graph-callback"].status, "ready")
        self.assertEqual(result["edge-forward-proxy"].status, "not-applicable")

    def test_missing_callback_is_reported_not_added(self) -> None:
        fake = Fake()
        fake.registration["web"] = {"redirectUris": ["https://old.example.test/cb"]}  # type: ignore[index]
        self.assertEqual(report(fake)["graph-callback"].status, "absent")
        self.assertTrue(
            all(c[:3] == ["rest", "--method", "GET"] or c[0] != "rest" for c in fake.calls)
        )

    def test_readable_but_empty_redirects(self) -> None:
        fake = Fake()
        fake.registration["web"] = {}  # type: ignore[index]
        self.assertEqual(report(fake)["graph-callback"].status, "absent")

    def test_edge_callback_requires_custom_forward_proxy(self) -> None:
        result = report(Fake(), f"https://{EDGE}")
        self.assertEqual(result["edge-forward-proxy"].status, "ready")
        self.assertEqual(result["graph-callback"].status, "ready")
        fake = Fake()
        fake.auth["proxy"] = "NoProxy"  # type: ignore[index]
        self.assertEqual(report(fake, f"https://{EDGE}")["edge-forward-proxy"].status, "mismatch")
        fake = Fake()
        fake.registration["web"] = {"redirectUris": [CALLBACK]}  # type: ignore[index]
        self.assertEqual(report(fake, f"https://{EDGE}")["graph-callback"].status, "absent")

    def test_invalid_public_urls_are_rejected(self) -> None:
        for url in (
            "http://edge.example.test",
            f"https://{EDGE}:8443",
            f"https://{EDGE}/path",
            f"https://user@{EDGE}",
            f"https://{EDGE}?x=1",
            "https://nodot",
            "https://-bad.example.test",
        ):
            with self.subTest(url=url):
                self.assertEqual(
                    report(Fake(), url)["callback-target"].reason, "public-url-invalid"
                )


class UnavailableCapabilityTests(unittest.TestCase):
    def test_graph_denied_is_denied_not_absent(self) -> None:
        fake = Fake()
        fake.errors["probe"] = (1, "ERROR: Forbidden Authorization_RequestDenied")
        fake.errors["registration"] = (1, "ERROR: Forbidden Authorization_RequestDenied")
        result = report(fake)
        self.assertEqual(result["graph-read-capability"].status, "denied")
        self.assertEqual(result["graph-application"].status, "denied")
        self.assertEqual(result["graph-app-roles"].reason, "blocked-by-graph-application")
        self.assertEqual(PRE.overall(list(result.values())), "blocked")

    def test_registration_not_found_is_absent(self) -> None:
        fake = Fake()
        fake.registration = None
        self.assertEqual(report(fake)["graph-application"].status, "absent")

    def test_signed_out_missing_cli_timeout_and_malformed(self) -> None:
        fake = Fake()
        fake.errors["account"] = (1, "Please run 'az login' to setup account.")
        self.assertEqual(report(fake)["az-session"].reason, "not-signed-in")
        self.assertEqual(
            PRE.Az(lambda a: (_ for _ in ()).throw(FileNotFoundError()))
            .read(PRE.ACCOUNT_ARGV)
            .reason,
            "azure-cli-unavailable",
        )

        def timeout(argv: list[str]) -> tuple[int, str, str]:
            raise subprocess.TimeoutExpired("az", 1)

        self.assertEqual(PRE.Az(timeout).read(PRE.ACCOUNT_ARGV).reason, "timeout")
        self.assertEqual(
            PRE.Az(lambda a: (0, "not json", "")).read(PRE.ACCOUNT_ARGV).reason,
            "malformed-response",
        )

    def test_app_lookup_denied_degrades_every_dependent_check(self) -> None:
        fake = Fake()
        for key in fake.errors.keys() | {"account", "fqdn", "auth", "probe"}:
            fake.errors[key] = (1, "boom")
        result = report(fake)
        self.assertEqual(PRE.overall(list(result.values())), "blocked")
        self.assertEqual(result["api-audience"].reason, "call-failed")
        self.assertEqual(result["graph-application"].reason, "blocked-by-api-audience")

    def test_ingress_absent(self) -> None:
        fake = Fake()
        fake.fqdn = {"fqdn": None}
        self.assertEqual(report(fake)["api-ingress"].status, "absent")


class SanitizedOutputTests(unittest.TestCase):
    def test_reports_contain_no_identifiers_or_secrets(self) -> None:
        fake = Fake()
        fake.auth["clientSecret"] = SECRET  # type: ignore[index]
        fake.registration["owners"] = [{"userPrincipalName": UPN, "id": OBJECT}]  # type: ignore[index]
        fake.registration["passwordCredentials"] = [{"secretText": SECRET}]  # type: ignore[index]
        fake.errors["principal"] = (1, f"ERROR: {TENANT} {CLIENT} {OBJECT} {UPN} {SECRET}")
        findings = PRE.run(PRE.Az(fake), "ama", "api", CONTRACT, f"https://{EDGE}")
        for as_json in (False, True):
            text = PRE.render(findings, as_json)
            for sentinel in (TENANT, CLIENT, OBJECT, UPN, SECRET, FQDN):
                self.assertNotIn(sentinel.lower(), text.lower())

    def test_facts_reject_free_text(self) -> None:
        with self.assertRaises(ValueError):
            PRE.Finding("x", "ready", "r", {"value": UPN})
        with self.assertRaises(ValueError):
            PRE.Finding("x", "ready", "r", {"roles": [UPN]})


class CliTests(unittest.TestCase):
    def invoke(self, fake: Fake, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = PRE.main(["-g", "ama", "-n", "api", *args], transport=fake)
        return code, output.getvalue()

    def test_exit_codes_and_json(self) -> None:
        code, text = self.invoke(Fake(), "--json")
        payload = json.loads(text)
        self.assertEqual(
            (code, payload["overall"], payload["readOnly"], payload["acceptanceEstablished"]),
            (0, "ready", True, False),
        )
        fake = Fake()
        fake.auth["clientId"] = "systemAssignedIdentity"  # type: ignore[index]
        code, text = self.invoke(fake)
        self.assertEqual(code, 1)
        self.assertIn("Acceptance: not established", text)

    def test_usage_errors_and_help(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            PRE.main(["-g", "bad name", "-n", "api"])
        self.assertEqual(cm.exception.code, 2)
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                PRE.main(
                    ["-g", "ama", "-n", "api", "--manifest", str(Path(directory) / "none.json")]
                )
            self.assertEqual(cm.exception.code, 2)
        help_text = io.StringIO()
        with contextlib.redirect_stdout(help_text), self.assertRaises(SystemExit):
            PRE.main(["--help"])
        self.assertIn("Read-only boundary", help_text.getvalue())


if __name__ == "__main__":
    unittest.main()
