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
        self.cases = "3"

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
            self.resources = [(k, n) for k, n in self.resources if rid(k, n) != target]
            return ""
        if "resource wait" in text or "acr build" in text or "revision restart" in text:
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
            return json.dumps(["t1"])
        if "keyvault secret list" in text:
            return json.dumps(["entra-client-secret"] if self.secret_present else [])
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
                ]
                self.budgets.append(rid("Microsoft.Consumption/budgets", "b"))
            else:
                self.resources.append(("Microsoft.App/containerApps", "api"))
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
            *extra,
        ]  # fmt: skip

    def run_main(self, argv: list[str], fake: FakeAzure) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv, fake, lambda url, mode: fake.health_for(url))
        return code, out.getvalue(), err.getvalue()


def _health_for(self: FakeAzure, url: str) -> int:
    if url.endswith("/healthz"):
        return self.health
    return 401 if url.endswith("/api/me") else 302


FakeAzure.health_for = _health_for  # type: ignore[attr-defined]


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

    def test_synthetic_guard(self) -> None:
        assert_synthetic(self.seed)
        self.seed.write_text(json.dumps({"x": ["someone@contoso.com"]}))
        with self.assertRaises(RebuildError):
            assert_synthetic(self.seed)


class RebuildTests(Fixture):
    def backend(self, fake: FakeAzure) -> AzureBackend:
        return AzureBackend(self.config(), fake, lambda url, mode: fake.health_for(url))

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
