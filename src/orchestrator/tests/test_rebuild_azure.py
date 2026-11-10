"""Disposable-environment tests: a stateful fake az stands in for the cloud; no network."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from collections.abc import Mapping, Sequence
from pathlib import Path

from zava_forward.orchestrator.rebuild import STAGES, RebuildError
from zava_forward.orchestrator.rebuild_azure import (
    AzureBackend,
    AzureConfig,
    ScriptExit,
    assert_no_secret_argv,
    assert_synthetic,
    main,
    run_rebuild,
)

SUB = "22222222-2222-4222-8222-222222222222"
BASE = f"/subscriptions/{SUB}/resourceGroups/ama/providers/"


def rid(kind: str, name: str) -> str:
    namespace, *types = kind.split("/")
    pairs = zip(types, name.split("/"), strict=True)
    return BASE + namespace + "/" + "/".join(p for pair in pairs for p in pair)


class FakeAzure:
    """Records every argv and environment; models the group inventory and budgets."""

    def __init__(self, resources: list[tuple[str, str]] | None = None, lock: bool = False):
        self.resources = [(k, n) for k, n in (resources or [])]
        self.budgets: list[str] = []
        self.lock = lock
        self.calls: list[list[str]] = []
        self.envs: list[Mapping[str, str] | None] = []
        self.deleted: list[str] = []
        self.health = 200
        self.secret_present = True
        self.secret_name = "entra-client-secret"
        self.pool_exists = True
        self.after_staff: str | None = None
        self.cases = "3"
        self.entra_stdout: str | None = None
        self.health_codes: list[int] = []
        self.tags: dict[str, list[str]] = {}
        self.build_fail: str | None = None
        self.skip_push: set[str] = set()

    def _build(self, args: list[str]) -> str:
        repository, _, tag = args[args.index("--image") + 1].partition(":")
        if repository == self.build_fail:
            raise ScriptExit("az acr build failed (1)", 1, "build log")
        if repository not in self.skip_push:
            self.tags.setdefault(repository, []).append(tag)
        return ""

    def health_for(self, url: str) -> int:
        if url.endswith("/healthz"):
            return self.health_codes.pop(0) if self.health_codes else self.health
        if url.endswith("/api/me"):
            return 401
        return 302 if url.endswith("/sign-in") else 200

    def __call__(self, argv: Sequence[str], env: Mapping[str, str] | None = None) -> str:
        args = list(argv)
        self.calls.append(args)
        self.envs.append(env)
        assert_no_secret_argv(args)
        text = " ".join(args)
        if args[0] == "python3":
            return self._python(args, env)
        if "account show" in text:
            return SUB
        if "get-access-token" in text:
            return "fake-token-value"
        if "lock list" in text:
            return json.dumps([{"name": "l"}] if self.lock else [])
        if "resource list" in text and "--query" in args:
            return json.dumps([rid(k, n) for k, n in self.resources])
        if "resource list" in text:
            return json.dumps([{"id": rid(k, n), "type": k} for k, n in self.resources])
        if "Consumption/budgets" in text and "get" in args:
            return json.dumps([{"id": b} for b in self.budgets])
        if "Consumption/budgets" in text and "delete" in args:
            self.deleted.append(args[args.index("--url") + 1])
            self.budgets = [b for b in self.budgets if b not in args[args.index("--url") + 1]]
            return ""
        if "resource delete" in text:
            target = args[args.index("--ids") + 1]
            self.deleted.append(target)
            self.resources = [
                (k, n)
                for k, n in self.resources
                if rid(k, n) != target
                and rid(k, n) != target.replace("privateEndpoints", "networkInterfaces") + "-nic"
            ]
            return ""
        if "private-endpoint show" in text:
            pe = args[args.index("--ids") + 1]
            return json.dumps([pe.replace("privateEndpoints", "networkInterfaces") + "-nic"])
        if "acr agentpool show" in text:
            if not self.pool_exists:
                raise ScriptExit("az acr agentpool failed (3)", 3, "")
            return "{}"
        if "acr build" in text:
            return self._build(args)
        if "resource wait" in text or "revision restart" in text:
            return ""
        if "acr list" in text:
            return json.dumps(["zfreg"])
        if "sql server list" in text:
            return json.dumps(["zfsql"])
        if "keyvault list" in text:
            return json.dumps(["zfvault"])
        if "acr show" in text:
            return "zfreg.azurecr.io"
        if "show-tags" in text:
            repository = args[args.index("--repository") + 1]
            if repository not in self.tags:
                raise ScriptExit("az acr repository failed (3)", 3, "")
            return json.dumps(self.tags[repository])
        if "keyvault secret list" in text:
            return json.dumps([self.secret_name] if self.secret_present else [])
        if "containerapp list" in text and "provisioningState" in text:
            return json.dumps(["Succeeded"])
        if "containerapp list" in text:
            return json.dumps([n for k, n in self.resources if k.endswith("containerApps")])
        if "ingress.fqdn" in text:
            return "app.example.test"
        if "latestRevisionName" in text:
            return "rev1"
        raise AssertionError(f"unexpected az call: {text}")

    def _python(self, args: list[str], env: Mapping[str, str] | None) -> str:
        script = Path(args[1]).name if args[1] != "-c" else "seed"
        if script == "deploy.py":
            if "deployApplications=false" in args:
                self.resources += [
                    ("Microsoft.App/managedEnvironments", "env"),
                    ("Microsoft.Network/virtualNetworks", "vnet"),
                    ("Microsoft.Network/privateEndpoints", "pe"),
                    ("Microsoft.Network/networkInterfaces", "pe-nic"),
                ]
                self.budgets.append(rid("Microsoft.Consumption/budgets", "b"))
            else:
                self.resources.append(("Microsoft.App/containerApps", "api"))
        if script == "initialize-workbench-staff.py" and "--apply" in args:
            self.entra_stdout = self.after_staff or self.entra_stdout
        if script == "setup-entra.py" and self.entra_stdout is not None:
            raise ScriptExit("check failed", 2, self.entra_stdout)
        if script == "seed":
            assert env is not None and env["ZF_STORE"] == "mssql"
            return self.cases
        return ""


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.params = root / "params.bicepparam"
        self.params.write_text("param workload = 'forward'\n")
        self.seed = root / "seed.json"
        self.seed.write_text(json.dumps({"cases": [], "staff": [{"email": "a@example.test"}]}))
        self.roster = root / "roster.json"
        self.roster.write_text(json.dumps([{"code": "S1", "upn": "b@example.test"}]))

    def config(self, **changes: object) -> AzureConfig:
        values: dict[str, object] = dict(
            subscription=SUB,
            registry="zfreg",
            image_tag="t1",
            parameters=self.params,
            seed=self.seed,
            roster=self.roster,
            container_app="api",
            repo_root=Path("/repo"),
            build_pool="pool1",
        )
        values.update(changes)
        return AzureConfig(**values)  # type: ignore[arg-type]

    def argv(self, operation: str, *extra: str) -> list[str]:
        return [
            operation,
            "--subscription", SUB,
            "--registry", "zfreg",
            "--image-tag", "t1",
            "--parameters", str(self.params),
            "--seed", str(self.seed),
            "--roster", str(self.roster),
            "--container-app", "api",
            "--build-pool", "pool1",
            *extra,
        ]  # fmt: skip

    def run_main(self, argv: list[str], fake: FakeAzure) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv, fake, lambda url, mode: fake.health_for(url), lambda s: None)
        return code, out.getvalue(), err.getvalue()


class DryRunTests(Fixture):
    def test_default_is_dry_run_with_no_azure_calls(self) -> None:
        fake = FakeAzure()
        code, out, _ = self.run_main(self.argv("rebuild"), fake)
        self.assertEqual(code, 0)
        self.assertEqual(fake.calls, [])
        report = json.loads(out)
        self.assertIn("dry-run", report["scope"])
        self.assertEqual(report["teardown"]["order"][-1], "microsoft.consumption/budgets")

    def test_dry_run_rejects_non_synthetic_inputs(self) -> None:
        self.roster.write_text(json.dumps([{"upn": "real.person@contoso.com"}]))
        code, _, err = self.run_main(self.argv("rebuild"), FakeAzure())
        self.assertEqual(code, 1)
        self.assertIn("non-synthetic", err)


class GuardTests(Fixture):
    def test_secret_argv_rejected(self) -> None:
        for bad in (
            ["az", "--password", "x"],
            ["az", "--client-secret=abc"],
            ["az", "token=abcdef"],
            ["az", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.abc"],
        ):
            with self.subTest(bad=bad), self.assertRaises(RebuildError):
                assert_no_secret_argv(bad)
        assert_no_secret_argv(["az", "keyvault", "secret", "list", "--query", "[].name"])

    def test_override_secret_rejected(self) -> None:
        with self.assertRaises(RebuildError):
            self.config(overrides=("entraClientSecret=abc",)).validate()

    def test_reserved_and_secure_overrides_rejected(self) -> None:
        for bad in ("deployApplications=true", "apiImage=x.io/y:1", "teamsWebhookUrl=https://h/x"):
            with self.subTest(bad=bad), self.assertRaises(RebuildError):
                self.config(overrides=(bad,)).validate()

    def test_declared_non_secret_overrides_accepted(self) -> None:
        good = (
            "entraClientSecretName=entra-client-secret",
            "enableEntraTokenStore=false",
            "entraTokenStoreReady=false",
        )
        self.config(overrides=good).validate()
        assert_no_secret_argv(list(good))
        self.params.write_text("param entraClientSecretName = 'entra-client-secret'\n")
        fake = FakeAzure()
        AzureBackend(self.config(), fake).verify(STAGES[0])

    def test_synthetic_guard(self) -> None:
        assert_synthetic(self.seed)
        self.seed.write_text(json.dumps({"x": ["someone@contoso.com"]}))
        with self.assertRaises(RebuildError):
            assert_synthetic(self.seed)


class RebuildTests(Fixture):
    def backend(self, fake: FakeAzure) -> AzureBackend:
        return AzureBackend(
            self.config(), fake, lambda url, mode: fake.health_for(url), lambda s: None
        )

    def test_full_sequence_checks_every_stage_and_stops_at_gated(self) -> None:
        fake = FakeAzure()
        evidence = run_rebuild(self.backend(fake), SUB)
        names = [item["stage"] for item in evidence]
        self.assertEqual(names, [s.name for s in STAGES][: len(names)])
        self.assertEqual(names[-1], "workload-sql")
        self.assertEqual(evidence[-1]["evidence"], "operator-gated")
        self.assertTrue(all(e["evidence"] == "azure-verified" for e in evidence[:-1]))

    def test_order_of_deployments_and_no_secret_or_token_on_argv(self) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB)
        deploys = [c for c in fake.calls if c[0] == "python3" and c[1].endswith("deploy.py")]
        self.assertEqual(len(deploys), 2)
        self.assertIn("deployApplications=false", deploys[0])
        self.assertIn("deployApplications=true", deploys[1])
        self.assertIn("apiImage=zfreg.azurecr.io/zava-forward-mvp:t1", deploys[1])
        self.assertTrue(all("fake-token-value" not in " ".join(c) for c in fake.calls))
        seeded = [e for e in fake.envs if e and "ZF_SQL_TOKEN" in e]
        self.assertEqual(len(seeded), 1)

    def test_nonempty_inventory_blocks_from_empty_rebuild(self) -> None:
        fake = FakeAzure([("Microsoft.Network/virtualNetworks", "v")])
        with self.assertRaises(RebuildError):
            run_rebuild(self.backend(fake), SUB)
        self.assertFalse([c for c in fake.calls if c[0] == "python3"])

    def test_missing_vault_secret_stops_before_sql_users(self) -> None:
        fake = FakeAzure()
        fake.secret_present = False
        with self.assertRaises(RebuildError):
            run_rebuild(self.backend(fake), SUB)
        self.assertFalse([c for c in fake.calls if c[1:2] and c[1].endswith("create-sql-users.py")])

    def test_unseeded_store_fails(self) -> None:
        fake = FakeAzure()
        fake.cases = "0"
        with self.assertRaises(RebuildError):
            run_rebuild(self.backend(fake), SUB)

    def test_private_registry_without_pool_stops_before_provisioning(self) -> None:
        fake = FakeAzure()
        backend = AzureBackend(self.config(build_pool=None), fake)
        with self.assertRaises(RebuildError):
            run_rebuild(backend, SUB)
        self.assertFalse([c for c in fake.calls if c[0] == "python3"])

    def test_effective_profile_applies_overrides_last(self) -> None:
        self.params.write_text(
            "param deploymentProfile = 'development'\nparam allowPublicNetworkAccess = true\n"
        )
        self.assertFalse(self.config(overrides=()).registry_is_private())
        override = ("allowPublicNetworkAccess=false",)
        self.assertTrue(self.config(overrides=override).registry_is_private())
        self.params.write_text(
            "param allowPublicNetworkAccess = true\nparam deploymentProfile = 'development'\n"
        )
        self.assertFalse(self.config().registry_is_private())
        self.assertTrue(
            self.config(overrides=("deploymentProfile=production",)).registry_is_private()
        )

    def test_missing_build_pool_stops_with_resume_instruction(self) -> None:
        fake = FakeAzure()
        fake.pool_exists = False
        with self.assertRaisesRegex(RebuildError, "--from-stage images"):
            run_rebuild(self.backend(fake), SUB)
        self.assertFalse([c for c in fake.calls if "build" in c and "acr" in c])

    def test_custom_secret_name_is_the_checked_credential(self) -> None:
        self.params.write_text("param entraClientSecretName = 'custom-secret'\n")
        fake = FakeAzure()
        with self.assertRaisesRegex(RebuildError, "custom-secret"):
            run_rebuild(self.backend(fake), SUB)
        fake = FakeAzure()
        fake.secret_name = "custom-secret"
        run_rebuild(self.backend(fake), SUB)

    def test_pending_roster_grants_are_tolerated_only_before_staff(self) -> None:
        sql = "Remaining: SQL binding and serving-replica restart are not confirmed.\n"
        pending = (
            "Roster: 1 principal(s); 2 missing assignment(s) planned.\n"
            "7/7 Summary: read-only; 2 reconciliation item(s).\n" + sql
        )
        fake = FakeAzure()
        fake.entra_stdout, fake.after_staff = (
            pending,
            "7/7 Summary: read-only; 0 reconciliation item(s).\n" + sql,
        )
        run_rebuild(self.backend(fake), SUB)
        fake = FakeAzure()
        fake.entra_stdout = pending
        with self.assertRaisesRegex(RebuildError, "drift"):
            run_rebuild(self.backend(fake), SUB)
        fake = FakeAzure()
        fake.entra_stdout = (
            "Roster: 1 principal(s); 1 missing assignment(s) planned.\n"
            "7/7 Summary: read-only; 2 reconciliation item(s).\n" + sql
        )
        with self.assertRaisesRegex(RebuildError, "drift"):
            run_rebuild(self.backend(fake), SUB)

    def test_image_build_uses_the_approved_pool(self) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB)
        builds = self.builds(fake)
        self.assertEqual(len(builds), 4)
        for build in builds:
            self.assertEqual(build[build.index("--agent-pool") + 1], "pool1")

    @staticmethod
    def builds(fake: FakeAzure) -> list[list[str]]:
        return [c for c in fake.calls if c[:3] == ["az", "acr", "build"]]

    @staticmethod
    def deploys(fake: FakeAzure) -> list[list[str]]:
        return [c for c in fake.calls if c[0] == "python3" and c[1].endswith("deploy.py")]

    def test_all_four_workloads_build_from_their_source_contexts(self) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB, "images")
        got = [(b[b.index("--image") + 1], b[b.index("-f") + 1], b[-1]) for b in self.builds(fake)]
        self.assertEqual(
            got,
            [
                ("zava-forward-mvp:t1", "src/api/Dockerfile", "/repo/src"),
                ("zava-forward-agents:t1", "src/agents/Dockerfile", "/repo/src"),
                ("zava-forward-orchestrator:t1", "src/orchestrator/Dockerfile", "/repo/src"),
                ("zava-forward-importer:t1", "src/importer/Dockerfile", "/repo/src"),
            ],
        )

    def test_application_deploy_maps_every_tag_and_passes_the_orchestrator_explicitly(
        self,
    ) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB)
        apps = self.deploys(fake)[1]
        reg = "zfreg.azurecr.io"
        for parameter, repository in (
            ("apiImage", "zava-forward-mvp"),
            ("agentImage", "zava-forward-agents"),
            ("importImage", "zava-forward-importer"),
        ):
            self.assertIn(f"{parameter}={reg}/{repository}:t1", apps)
        self.assertEqual(
            apps[apps.index("--orchestrator-image") + 1], f"{reg}/zava-forward-orchestrator:t1"
        )
        text = " ".join(apps)
        self.assertNotIn("orchestratorImage=", text)
        self.assertNotIn("quickstart", text)
        self.assertNotIn(":latest", text)

    def test_build_failure_stops_before_later_builds_and_deployment(self) -> None:
        fake = FakeAzure()
        fake.build_fail = "zava-forward-orchestrator"
        with self.assertRaisesRegex(RebuildError, "orchestrator.*az acr build failed"):
            run_rebuild(self.backend(fake), SUB)
        self.assertEqual(len(self.builds(fake)), 3)
        self.assertEqual(len(self.deploys(fake)), 1)

    def test_unpublished_image_fails_verification_before_deployment(self) -> None:
        fake = FakeAzure()
        fake.skip_push = {"zava-forward-importer"}
        with self.assertRaisesRegex(RebuildError, "importer"):
            run_rebuild(self.backend(fake), SUB)
        self.assertEqual(len(self.deploys(fake)), 1)

    def test_resume_never_treats_the_api_tag_as_four_image_readiness(self) -> None:
        fake = FakeAzure()
        fake.tags = {"zava-forward-mvp": ["t1"]}
        with self.assertRaisesRegex(RebuildError, "agents.*orchestrator.*importer"):
            run_rebuild(self.backend(fake), SUB, "applications")
        self.assertEqual(self.deploys(fake), [])

    def test_resume_deploys_when_all_four_tags_exist(self) -> None:
        fake = FakeAzure()
        fake.tags = {
            r: ["t1"]
            for r in (
                "zava-forward-mvp",
                "zava-forward-agents",
                "zava-forward-orchestrator",
                "zava-forward-importer",
            )
        }
        run_rebuild(self.backend(fake), SUB, "applications")
        (apps,) = self.deploys(fake)
        self.assertIn("--orchestrator-image", apps)
        self.assertIn("agentImage=zfreg.azurecr.io/zava-forward-agents:t1", apps)

    def test_workload_images_cannot_be_overridden(self) -> None:
        for name in ("agentImage", "importImage", "orchestratorImage"):
            with self.subTest(name=name), self.assertRaises(RebuildError):
                self.config(overrides=(f"{name}=x.io/y:1",)).validate()

    def test_dry_run_lists_the_four_images_without_io(self) -> None:
        fake = FakeAzure()
        _, out, _ = self.run_main(self.argv("rebuild"), fake)
        self.assertEqual(fake.calls, [])
        images = json.loads(out)["images"]
        self.assertEqual(
            [(i["project"], i["repository"]) for i in images],
            [
                ("api", "zava-forward-mvp"),
                ("agents", "zava-forward-agents"),
                ("orchestrator", "zava-forward-orchestrator"),
                ("importer", "zava-forward-importer"),
            ],
        )

    def test_staff_only_entra_gap_is_tolerated_and_roster_forwarded(self) -> None:
        fake = FakeAzure()
        fake.entra_stdout = (
            "7/7 Summary: read-only; 0 reconciliation item(s).\n"
            "Remaining: SQL binding and serving-replica restart are not confirmed.\n"
        )
        run_rebuild(self.backend(fake), SUB)
        entra = next(c for c in fake.calls if c[1:2] and c[1].endswith("setup-entra.py"))
        self.assertEqual(entra[entra.index("--roster") + 1], str(self.roster))

    def test_other_entra_drift_fails(self) -> None:
        fake = FakeAzure()
        fake.entra_stdout = "7/7 Summary: read-only; 2 reconciliation item(s).\nRemaining: x\n"
        with self.assertRaises(RebuildError):
            run_rebuild(self.backend(fake), SUB)

    def test_transient_health_is_retried_but_denial_is_strict(self) -> None:
        fake = FakeAzure()
        fake.health_codes = [503, 0, 200]
        evidence = run_rebuild(self.backend(fake), SUB)
        self.assertEqual(evidence[-1]["stage"], "workload-sql")
        self.assertEqual(
            [e["stage"] for e in evidence if e["stage"] == "browser-redirect"],
            ["browser-redirect"],
        )

    def test_root_page_is_not_the_redirect_probe(self) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB)
        self.assertEqual(fake.health_for("https://app.example.test/"), 200)

    def test_unhealthy_application_fails(self) -> None:
        fake = FakeAzure()
        fake.health = 503
        with self.assertRaises(RebuildError):
            run_rebuild(self.backend(fake), SUB)

    def test_resume_rediscovers_and_continues(self) -> None:
        fake = FakeAzure()
        run_rebuild(self.backend(fake), SUB)
        fake.calls.clear()
        evidence = run_rebuild(self.backend(fake), SUB, "health")
        self.assertEqual([e["stage"] for e in evidence][0], "health")
        self.assertTrue(any("acr list" in " ".join(c) for c in fake.calls))

    def test_cli_apply_exit_2_when_operator_gated(self) -> None:
        code, out, _ = self.run_main(self.argv("rebuild", "--apply"), FakeAzure())
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out)["stages"][-1]["stage"], "workload-sql")

    def test_wrong_subscription_stops(self) -> None:
        fake = FakeAzure()
        backend = AzureBackend(self.config(subscription=SUB[:-1] + "3"), fake)
        with self.assertRaises(RebuildError):
            backend.check_account()


class TeardownTests(Fixture):
    def test_dependency_order_budgets_last_and_empty_inventory(self) -> None:
        fake = FakeAzure(
            [
                ("Microsoft.Network/virtualNetworks", "vnet"),
                ("Microsoft.App/managedEnvironments", "env"),
                ("Microsoft.App/containerApps", "api"),
                ("Microsoft.Network/privateEndpoints", "pe"),
            ]
        )
        fake.resources.append(("Microsoft.Network/networkInterfaces", "pe-nic"))
        fake.budgets.append(rid("Microsoft.Consumption/budgets", "b"))
        code, out, _ = self.run_main(self.argv("teardown", "--apply"), fake)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["inventory"], "empty")
        kinds = [d.split("/providers/")[1].split("/")[1] for d in fake.deleted]
        self.assertEqual(
            kinds,
            [
                "containerApps",
                "privateEndpoints",
                "managedEnvironments",
                "virtualNetworks",
                "budgets",
            ],
        )
        self.assertEqual(fake.resources, [])
        self.assertEqual(fake.budgets, [])

    def test_teardown_dry_run_deletes_nothing(self) -> None:
        fake = FakeAzure([("Microsoft.App/containerApps", "api")])
        code, _, _ = self.run_main(self.argv("teardown"), fake)
        self.assertEqual((code, fake.calls, fake.deleted), (0, [], []))

    def test_lock_blocks_all_deletion(self) -> None:
        fake = FakeAzure([("Microsoft.App/containerApps", "api")], lock=True)
        code, _, err = self.run_main(self.argv("teardown", "--apply"), fake)
        self.assertEqual(code, 1)
        self.assertEqual(fake.deleted, [])
        self.assertIn("REBUILD_FAILED", err)

    def test_unknown_resource_type_stops_before_delete(self) -> None:
        fake = FakeAzure([("Microsoft.Unmodeled/things", "x")])
        code, _, _ = self.run_main(self.argv("teardown", "--apply"), fake)
        self.assertEqual((code, fake.deleted), (1, []))

    def test_lingering_resource_after_delete_fails(self) -> None:
        fake = FakeAzure([("Microsoft.App/containerApps", "api")])
        original = fake.__call__

        def sticky(argv: Sequence[str], env: Mapping[str, str] | None = None) -> str:
            if "delete" in argv and "--ids" in argv:
                fake.calls.append(list(argv))
                return ""
            return original(argv, env)

        out = io.StringIO()
        with contextlib.redirect_stderr(out):
            code = main(self.argv("teardown", "--apply"), sticky)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
