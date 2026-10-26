"""Offline tests for the resident-only demo template and deploy command (fake CLI, no Azure)."""

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INFRA / "scripts"))
import resident_demo_deploy as DEPLOY  # noqa: E402

SUB = "11111111-2222-3333-4444-555555555555"
ROOT = f"/subscriptions/{SUB}/resourceGroups/ama/providers/"
NOW = datetime(2026, 10, 27, 9, 0, tzinfo=UTC)
EXPIRES = "2026-10-31T23:00:00Z"
IMAGE = "crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:" + "a" * 64
SQL = "sql-fake.database.windows.net"
VAULT = ROOT + "Microsoft.KeyVault/vaults/kv-cutovertest-rzsrg/secrets/"
OWNED = [
    ROOT + "Microsoft.ManagedIdentity/userAssignedIdentities/id-resident-demo",
    ROOT + "Microsoft.App/containerApps/ca-resident-demo",
    ROOT + "Microsoft.Resources/deployments/resident-demo-scope",
    VAULT + "resident-demo-password-verifier/providers/Microsoft.Authorization/roleAssignments/a",
    VAULT + "resident-demo-session-key/providers/Microsoft.Authorization/roleAssignments/b",
    ROOT + "Microsoft.ContainerRegistry/registries/crcutovertestrzsrg"
    "/providers/Microsoft.Authorization/roleAssignments/c",
]


def compiled() -> dict:
    result = subprocess.run(
        [
            "az",
            "bicep",
            "build",
            "--file",
            str(INFRA / "resident-demo.bicep"),
            "--stdout",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class TemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = compiled()
        cls.resources = cls.template["resources"]
        cls.app = next(r for r in cls.resources if r["type"] == "Microsoft.App/containerApps")

    def test_only_resident_owned_resource_types(self):
        kinds = sorted(r["type"] for r in self.resources)
        self.assertEqual(
            kinds,
            sorted(
                [
                    "Microsoft.App/containerApps",
                    "Microsoft.Authorization/roleAssignments",
                    "Microsoft.Authorization/roleAssignments",
                    "Microsoft.Authorization/roleAssignments",
                    "Microsoft.ManagedIdentity/userAssignedIdentities",
                    "Microsoft.Resources/deployments",
                ]
            ),
        )

    def test_scale_is_zero_to_one_with_no_jobs_or_schedules(self):
        text = json.dumps(self.template)
        self.assertEqual(
            self.app["properties"]["template"]["scale"],
            {"minReplicas": 0, "maxReplicas": 1},
        )
        for banned in (
            "Microsoft.App/jobs",
            "cronExpression",
            "scheduleTriggerConfig",
            "eventTrigger",
        ):
            self.assertNotIn(banned, text)

    def test_runtime_contract_and_secret_references(self):
        env = {e["name"]: e for e in self.app["properties"]["template"]["containers"][0]["env"]}
        for name in (
            "ZF_DEMO_EXPIRES_AT",
            "ZF_DEMO_ALLOWED_HOSTS",
            "ZF_DEMO_CLIENT_ADDRESS",
            "ZF_DEMO_PASSWORD_VERIFIER",
            "ZF_DEMO_SESSION_KEY",
            "ZF_SQL_AUTH",
            "ZF_SQL_CLIENT_ID",
            "ZF_SQL_SERVER",
            "ZF_SQL_DATABASE",
            "PORT",
        ):
            self.assertIn(name, env)
        self.assertEqual(env["ZF_DEMO_CLIENT_ADDRESS"]["value"], "ingress-rightmost")
        self.assertEqual(env["ZF_SQL_AUTH"]["value"], "msi")
        self.assertEqual(env["PORT"]["value"], "8089")
        self.assertEqual(env["ZF_DEMO_PASSWORD_VERIFIER"]["secretRef"], "demo-password-verifier")
        self.assertEqual(env["ZF_DEMO_SESSION_KEY"]["secretRef"], "demo-session-key")
        # Forbidden prefixes the service refuses at start-up must never be configured.
        for name in env:
            self.assertFalse(name.startswith(("ZF_STORE", "ZF_ENTRA", "ZF_AI", "AI_", "ZF_DATA")))
        for secret in self.app["properties"]["configuration"]["secrets"]:
            self.assertNotIn("value", secret)
            self.assertNotRegex(secret["keyVaultUrl"], r"/secrets/[^/]+/[0-9a-f]{32}")

    def test_roles_are_secret_scoped_and_image_is_digest_guarded(self):
        text = json.dumps(self.template)
        self.assertEqual(text.count("4633458b-17de-408a-b874-0445c86b69e6"), 1)
        assignments = [r for r in self.resources if r["type"].endswith("roleAssignments")]
        scopes = sorted(
            re.findall(
                r"secrets', '([a-z-]+)'|'(resident-demo-[a-z-]+)'",
                json.dumps(assignments),
            )
        )
        self.assertTrue(scopes)
        self.assertIn("@sha256:", text)
        self.assertIn("2026-11-01T00:00:00Z", text)
        self.assertEqual(self.template["parameters"]["externalIngress"]["defaultValue"], True)

    def test_main_stack_defaults_are_untouched(self):
        main = (INFRA / "modules" / "containerapps.bicep").read_text()
        self.assertIn("minReplicas: 2", main)
        self.assertNotIn("resident", (INFRA / "main.bicep").read_text().lower())
        self.assertNotIn("resident", (INFRA / "scripts" / "deploy.py").read_text().lower())


class FakeCli:
    def __init__(self, changes, status="Succeeded", scale=None):
        self.subscription = None
        self.calls: list[list[str]] = []
        self.changes, self.status = changes, status
        self.scale = scale or {"minReplicas": 0, "maxReplicas": 1}

    def call(self, args):
        self.calls.append(args)
        if args[:3] == ["deployment", "group", "what-if"]:
            return {"status": self.status, "changes": self.changes}
        if args[0] == "containerapp":
            return {"properties": {"template": {"scale": self.scale}}}
        return {}


def create(ids):
    return [{"changeType": "Create", "resourceId": i} for i in ids]


class CommandTests(unittest.TestCase):
    def run_cmd(
        self,
        cli,
        *extra,
        apply=False,
        typed=None,
        expires=EXPIRES,
        image=IMAGE,
        tty=True,
    ):
        with tempfile.TemporaryDirectory() as home:
            profile = Path(home) / "p"
            profile.mkdir(mode=0o700)
            argv = [
                "x",
                "--subscription",
                SUB,
                "--expires",
                expires,
                "--image",
                image,
                "--sql-server",
                SQL,
                "--sql-database",
                "db",
                "--tenant-profile",
                str(profile),
                *extra,
            ]
            if apply:
                argv.append("--apply")
            out, err = io.StringIO(), io.StringIO()
            phrase = (
                typed
                if typed is not None
                else DEPLOY.confirmation(SUB, expires, IMAGE, "--no-ingress" not in extra)
            )
            code = DEPLOY.main(
                argv,
                tty,
                out,
                err,
                ask=lambda _: phrase,
                now=lambda: NOW,
                make_cli=lambda _: cli,
            )
        self.output = out.getvalue() + err.getvalue()
        return code

    def test_dry_run_checks_and_never_deploys(self):
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli), 0)
        self.assertEqual([c[:3] for c in cli.calls], [["deployment", "group", "what-if"]])
        self.assertIn("nothing was deployed", self.output)

    def test_apply_needs_exact_phrase_then_deploys_and_reads_scale_back(self):
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, apply=True, typed="yes"), 1)
        self.assertNotIn("create", [c[2] for c in cli.calls if c[0] == "deployment"])
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, apply=True), 0)
        self.assertEqual(
            [c[2] if c[0] == "deployment" else c[0] for c in cli.calls],
            ["what-if", "create", "containerapp"],
        )
        for call in cli.calls:
            self.assertNotIn("main.bicep", " ".join(call))

    def test_scale_readback_failure_is_not_silent(self):
        cli = FakeCli(create(OWNED), scale={"minReplicas": 2, "maxReplicas": 1})
        self.assertEqual(self.run_cmd(cli, apply=True), 1)
        self.assertIn("min 0 / max 1", self.output)

    def test_what_if_outside_resident_resources_is_refused(self):
        outside = [
            ROOT + "Microsoft.App/containerApps/ca-api",
            ROOT + "Microsoft.App/jobs/job-orchestrator",
            ROOT + "Microsoft.Sql/servers/s/databases/d",
            VAULT + "other-secret/providers/Microsoft.Authorization/roleAssignments/x",
            ROOT + "Microsoft.KeyVault/vaults/kv-cutovertest-rzsrg"
            "/providers/Microsoft.Authorization/roleAssignments/x",
        ]
        for extra in outside:
            cli = FakeCli(create([*OWNED, extra]))
            self.assertEqual(self.run_cmd(cli, apply=True), 1, extra)
            self.assertEqual(len(cli.calls), 1)
        deletion = [{"changeType": "Delete", "resourceId": OWNED[1]}]
        self.assertEqual(self.run_cmd(FakeCli(deletion)), 1)
        self.assertEqual(self.run_cmd(FakeCli(create(OWNED), status="Failed")), 1)

    def test_uppercase_subscription_guid_still_matches_owned_resources(self):
        upper = SUB.replace("1", "a").upper()
        owned = [i.replace(SUB, upper) for i in OWNED]
        plan = {"status": "Succeeded", "changes": create(owned)}
        self.assertEqual(DEPLOY.check_changes(plan, upper), 6)
        plan["changes"] = create([*owned, ROOT.replace(SUB, upper) + "Microsoft.App/jobs/x"])
        with self.assertRaises(DEPLOY.DeployError):
            DEPLOY.check_changes(plan, upper)

    def test_compiled_inventory_including_guard_passes_and_unknown_nested_is_refused(
        self,
    ):
        template = compiled()
        names = {
            r["type"]: r["name"] for r in template["resources"] if r["type"].endswith("deployments")
        }
        self.assertEqual(names, {"Microsoft.Resources/deployments": "resident-demo-scope"})
        guard = ROOT + "Microsoft.Resources/deployments/" + names["Microsoft.Resources/deployments"]
        self.assertIn(guard, OWNED)
        self.assertEqual(
            DEPLOY.check_changes({"status": "Succeeded", "changes": create(OWNED)}, SUB),
            6,
        )
        other = ROOT + "Microsoft.Resources/deployments/resident-demo-scope-2"
        for bad in (other, ROOT + "Microsoft.Resources/deployments/main"):
            with self.assertRaises(DEPLOY.DeployError):
                DEPLOY.check_changes({"status": "Succeeded", "changes": create([*OWNED, bad])}, SUB)

    def test_ignored_and_unchanged_resources_do_not_block(self):
        extra = [
            {
                "changeType": "Ignore",
                "resourceId": ROOT + "Microsoft.App/containerApps/ca-api",
            },
            {"changeType": "NoChange", "resourceId": OWNED[0]},
        ]
        self.assertEqual(self.run_cmd(FakeCli(create(OWNED[1:]) + extra)), 0)

    def test_expiry_image_and_terminal_fail_closed(self):
        for expires in (
            "2026-11-01T00:00:01Z",
            "2026-10-27T08:00:00Z",
            "2026-10-31",
            "",
        ):
            cli = FakeCli(create(OWNED))
            self.assertEqual(self.run_cmd(cli, expires=expires), 1, expires)
            self.assertEqual(cli.calls, [])
        for image in (
            "crcutovertestrzsrg.azurecr.io/x:latest",
            "evil.example/x@sha256:" + "a" * 64,
        ):
            cli = FakeCli(create(OWNED))
            self.assertEqual(self.run_cmd(cli, image=image), 1, image)
            self.assertEqual(cli.calls, [])
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, tty=False), 1)
        self.assertEqual(cli.calls, [])

    def test_rollback_flag_turns_ingress_off(self):
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, "--no-ingress", apply=True), 0)
        self.assertIn("externalIngress=false", cli.calls[0])

    def test_rollback_is_permitted_at_and_after_expiry_but_opening_is_not(self):
        for expires in ("2026-10-27T08:00:00Z", "2026-11-01T00:00:00Z"):
            cli = FakeCli(create(OWNED))
            self.assertEqual(
                self.run_cmd(cli, "--no-ingress", apply=True, expires=expires),
                0,
                expires,
            )
            self.assertIn("externalIngress=false", cli.calls[0])
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, apply=True, expires="2026-10-27T08:00:00Z"), 1)
        self.assertEqual(cli.calls, [])
        cli = FakeCli(create(OWNED))
        self.assertEqual(self.run_cmd(cli, "--no-ingress", expires="2026-11-01T00:00:01Z"), 1)
        self.assertEqual(cli.calls, [])


if __name__ == "__main__":
    unittest.main()
