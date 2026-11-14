"""Container Apps demo wiring contract: identity, environment, secrets, AI and telemetry (Refs #146, #165).

Reads the Bicep sources as text, so it needs no Azure access and no change to the templates.
It is a source contract, not evidence of a deployed revision or of live identity grants.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INFRA = ROOT / "infra"
APPS = (INFRA / "modules" / "containerapps.bicep").read_text()
MAIN = (INFRA / "main.bicep").read_text()
IOT_JOBS = ("live-receiver-job.bicep", "live-simulator-job.bicep")

RESOURCE = re.compile(
    r"^resource (\w+) 'Microsoft\.App/(?:containerApps|jobs)@[\w-]+' = ", re.MULTILINE
)
ENV_ENTRY = re.compile(r"\{ name: '(\w+)', (value|secretRef): ([^}]+?) \}")
SECRET_NAME = re.compile(
    r"(secret|password|passwd|pwd|key|token|sas|connectionstring)", re.IGNORECASE
)
ALLOWED_PLAIN_NAMES = frozenset(
    {
        "APPLICATIONINSIGHTS_CONNECTION_STRING",
        "KEY_VAULT_URI",
        "ZF_SIM_KEY_FILE",
        "AUTH_TOKEN_STORE_ROTATION",
        "TOKEN_STORAGE_ACCOUNT",
    }
)
WORKLOAD_IDENTITY = {
    "api": "identityIds.api",
    "agents": "identityIds.agents",
    "orchestrator": "identityIds.orchestrator",
    "ledgerVerify": "identityIds.api",
    "rankingPublish": "identityIds.api",
    "importJob": "identityIds.import",
}
WORKLOAD_CLIENT_ID = {
    "api": "identityClientIds.api",
    "agents": "identityClientIds.agents",
    "orchestrator": "identityClientIds.orchestrator",
    "ledgerVerify": "identityClientIds.api",
    "rankingPublish": "identityClientIds.api",
    "importJob": "identityClientIds.import",
}


def blocks(text: str) -> dict[str, str]:
    """Every container resource body keyed by symbol name."""
    matches = list(RESOURCE.finditer(text))
    found: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        found[match.group(1)] = text[match.start() : end]
    return found


def env_entries(body: str) -> list[tuple[str, str, str]]:
    return [
        (m.group(1), m.group(2), m.group(3).strip()) for m in ENV_ENTRY.finditer(body)
    ]


class ContainerAppIdentityWiring(unittest.TestCase):
    def setUp(self) -> None:
        self.blocks = blocks(APPS)

    def test_every_workload_is_known(self) -> None:
        extras = set(self.blocks) - set(WORKLOAD_IDENTITY) - {"tokenRenewal"}
        self.assertEqual(set(), extras, "new workload needs identity wiring assertions")

    def test_workloads_use_user_assigned_identity_only(self) -> None:
        for name, body in self.blocks.items():
            with self.subTest(workload=name):
                self.assertIn("type: 'UserAssigned'", body)
                self.assertNotIn("SystemAssigned", body)

    def test_identity_registry_and_client_id_match(self) -> None:
        for name, identity in WORKLOAD_IDENTITY.items():
            body = self.blocks[name]
            with self.subTest(workload=name):
                self.assertIn(
                    f"userAssignedIdentities: {{ '${{{identity}}}': {{}} }}", body
                )
                self.assertIn(
                    f"registries: [{{ server: registryServer, identity: {identity} }}]",
                    body,
                )
                self.assertIn(
                    f"{{ name: 'AZURE_CLIENT_ID', value: {WORKLOAD_CLIENT_ID[name]} }}",
                    body,
                )

    def test_token_renewal_uses_dedicated_identity(self) -> None:
        body = self.blocks["tokenRenewal"]
        self.assertIn("'${tokenMaintenanceIdentityId}': {}", body)
        self.assertIn("identity: tokenMaintenanceIdentityId", body)
        self.assertIn(
            "{ name: 'AZURE_CLIENT_ID', value: tokenMaintenanceClientId }", body
        )

    def test_main_passes_identity_outputs(self) -> None:
        self.assertIn("identityIds: identity.outputs.ids", MAIN)
        self.assertIn("identityClientIds: identity.outputs.clientIds", MAIN)
        identity = (INFRA / "modules" / "identity.bicep").read_text()
        for key in ("api", "agents", "orchestrator", "import"):
            self.assertRegex(identity, rf"output ids object = \{{[^}}]*\b{key}: ")
            self.assertRegex(identity, rf"output clientIds object = \{{[^}}]*\b{key}: ")


class ContainerAppSecretHygiene(unittest.TestCase):
    def setUp(self) -> None:
        self.blocks = blocks(APPS)

    def test_no_plaintext_secret_values_in_environment(self) -> None:
        for name, body in self.blocks.items():
            for env_name, kind, expr in env_entries(body):
                if kind != "value" or not SECRET_NAME.search(env_name):
                    continue
                with self.subTest(workload=name, env=env_name):
                    self.assertIn(env_name, ALLOWED_PLAIN_NAMES)
                    self.assertNotRegex(
                        expr, r"^'[^']*'$|listKeys|listSecrets|\.value$"
                    )

    def test_secret_environment_uses_secret_reference(self) -> None:
        for name, body in self.blocks.items():
            for env_name, kind, expr in env_entries(body):
                if kind == "secretRef":
                    with self.subTest(workload=name, env=env_name):
                        self.assertEqual("AUTH_TOKEN_STORE_ROTATION", env_name)
                        self.assertEqual("'entra-token-store-sas'", expr)

    def test_container_secrets_come_from_key_vault_with_identity(self) -> None:
        start = APPS.index("secrets: concat(")
        section = APPS[start : APPS.index("\n    }\n    template", start)]
        entries = re.findall(r"\{ name: .*? \}$", section, re.MULTILINE)
        self.assertEqual(2, len(entries))
        for entry in entries:
            with self.subTest(entry=entry):
                self.assertIn("keyVaultUrl: '${keyVaultUri}/secrets/", entry)
                self.assertIn("identity: identityIds.api", entry)
                self.assertNotIn("value:", entry)

    def test_no_literal_credentials_in_bicep(self) -> None:
        for name in ("main.bicep", "modules/containerapps.bicep", *IOT_JOBS):
            text = (INFRA / name).read_text()
            with self.subTest(file=name):
                self.assertNotRegex(
                    text, r"(?i)(AccountKey|SharedAccessKey|Password|pwd)="
                )
                self.assertNotRegex(text, r"(?i)\bsig=[A-Za-z0-9%]{8,}")
                self.assertNotIn("listKeys(", text)
                self.assertNotIn("listKeys\n", text)

    def test_sql_and_blob_use_managed_identity(self) -> None:
        api = self.blocks["api"]
        self.assertIn("{ name: 'ZF_SQL_AUTH', value: 'msi' }", api)
        self.assertIn("{ name: 'ZF_SQL_CLIENT_ID', value: identityClientIds.api }", api)
        self.assertIn(
            "{ name: 'ZF_BLOB_CLIENT_ID', value: identityClientIds.api }", api
        )


class DemoAiAndTelemetryWiring(unittest.TestCase):
    def setUp(self) -> None:
        self.blocks = blocks(APPS)

    def test_ai_is_default_off_and_gated(self) -> None:
        self.assertIn("param enableApiAi bool = false", APPS)
        self.assertIn("param enableApiAi bool = false", MAIN)
        self.assertIn("enableApiAi: enableApiAi", MAIN)
        self.assertRegex(
            APPS,
            r"enableApiAi \? \[\s*\{ name: 'AI_ENDPOINT', value: openAiEndpoint \}",
        )
        for name, body in self.blocks.items():
            if name != "api":
                self.assertNotIn("AI_ENDPOINT", body, name)

    def test_ai_uses_endpoint_and_deployment_names_only(self) -> None:
        start = APPS.index("enableApiAi ? [")
        section = APPS[start : APPS.index("] : [], authEnabled", start)]
        names = {n for n, _, _ in env_entries(section)}
        self.assertEqual(
            {
                "AI_ENDPOINT",
                "AI_DEPLOYMENT",
                "AI_DEPLOYMENT_STRONG",
                "AI_MODEL_VERSION",
                "AI_MODEL_VERSION_STRONG",
            },
            names,
        )
        self.assertNotRegex(section, r"(?i)api[-_]?key|secretRef")

    def test_chat_demo_activation_requires_direct_ingress_and_exact_approval(
        self,
    ) -> None:
        self.assertIn(
            "var chatDemoActive = demoDirectIngress && chatDemoActivation == 'approved-2026-11-03'",
            APPS,
        )
        self.assertRegex(
            APPS,
            r"!chatDemoActive \? \[\] : \[\s*\{ name: 'ZF_CHAT_DEMO_ACTIVATION', value: chatDemoActivation \}\s*"
            r"\{ name: 'ZF_DEPLOYMENT_PROFILE', value: 'demo' \}",
        )
        self.assertIn("param chatDemoActivation string = ''", APPS)
        self.assertIn("param chatDemoActivation string = ''", MAIN)
        self.assertIn("chatDemoActivation: chatDemoActivation", MAIN)
        self.assertEqual(1, len(re.findall(r"name: 'ZF_DEPLOYMENT_PROFILE'", APPS)))

    def test_chat_governance_refs_require_all_inputs(self) -> None:
        for param in (
            "chatDpiaRef",
            "chatLawfulBasisRef",
            "chatNoticeRef",
            "chatRetentionRef",
        ):
            self.assertIn(f"!empty(trim({param}))", APPS)
            self.assertIn(f"{param}: {param}", MAIN)
        self.assertIn("chatRetentionDays > 0", APPS)
        self.assertIn("!chatEnabled ? [] : [", APPS)

    def test_telemetry_is_wired_through_every_workload(self) -> None:
        self.assertIn(
            "{ name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsightsConnectionString }",
            APPS,
        )
        self.assertIn("{ name: 'OTEL_SERVICE_NAMESPACE', value: 'zava-forward' }", APPS)
        self.assertIn(
            "appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString",
            MAIN,
        )
        for name, body in self.blocks.items():
            if name == "tokenRenewal":
                continue
            with self.subTest(workload=name):
                self.assertIn("env: concat(commonEnv, [", body)

    def test_demo_profile_is_not_hardcoded_in_shared_environment(self) -> None:
        common = APPS[APPS.index("var commonEnv") : APPS.index("resource api ")]
        self.assertNotIn("ZF_DEPLOYMENT_PROFILE", common)
        self.assertNotIn("ZF_CHAT_DEMO_ACTIVATION", common)


class OrchestratorAndIotWiring(unittest.TestCase):
    def setUp(self) -> None:
        self.blocks = blocks(APPS)

    def test_orchestrator_and_agents_call_api_with_entra_audience(self) -> None:
        for name in ("agents", "orchestrator"):
            body = self.blocks[name]
            with self.subTest(workload=name):
                self.assertIn(
                    "API_BASE_URL', value: 'https://${api!.properties.configuration.ingress.fqdn}'",
                    body,
                )
                self.assertIn(
                    "{ name: 'API_AUDIENCE', value: 'api://${entraClientId}' }", body
                )
                self.assertIn("{ name: 'QUEUE_ENDPOINT', value: queueEndpoint }", body)

    def test_queue_scale_rules_authenticate_with_workload_identity(self) -> None:
        self.assertIn("identity: identityIds.agents", self.blocks["agents"])
        self.assertIn("identity: identityIds.import", self.blocks["importJob"])

    def test_live_iot_jobs_use_existing_identity_and_no_secrets(self) -> None:
        for name in IOT_JOBS:
            text = (INFRA / name).read_text()
            with self.subTest(file=name):
                self.assertIn(
                    "Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing",
                    text,
                )
                self.assertIn("userAssignedIdentities: { '${identity.id}': {} }", text)
                self.assertIn(
                    "registries: [{ server: registryServer, identity: identity.id }]",
                    text,
                )
                self.assertIn("{ name: 'ZF_SQL_AUTH', value: 'msi' }", text)
                self.assertIn(
                    "{ name: 'ZF_SQL_CLIENT_ID', value: identity.properties.clientId }",
                    text,
                )
                self.assertNotIn("secretRef", text)
                self.assertNotIn("secrets:", text)
                for env_name, kind, _ in env_entries(text):
                    self.assertEqual("value", kind)
                    self.assertFalse(
                        SECRET_NAME.search(env_name) and env_name != "ZF_SIM_KEY_FILE",
                        env_name,
                    )


if __name__ == "__main__":
    unittest.main()
