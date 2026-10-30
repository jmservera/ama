"""Synthetic-only sequencing tests: no cloud, tenant, model or private-data access."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from zava_forward.orchestrator.rebuild import (
    BUDGET,
    LOCAL_SUBSCRIPTION,
    STAGES,
    Inventory,
    LocalBackend,
    RebuildError,
    Resource,
    Stage,
    canonical,
    deletion_order,
    main,
    rebuild,
    teardown,
)

PREFIX = f"/subscriptions/{LOCAL_SUBSCRIPTION}/resourceGroups/ama/providers/"


def resource(kind: str, name: str = "synthetic") -> Resource:
    namespace, *types = kind.split("/")
    rid = (
        PREFIX
        + namespace
        + "/"
        + "/".join(part for pair in zip(types, name.split("/"), strict=True) for part in pair)
    )
    return Resource(rid, kind, False, False)


class MemoryBackend:
    def __init__(self, inventory: Inventory | None = None):
        self.state = inventory if inventory is not None else Inventory()
        self.trace: list[str] = []
        self.deleted: list[Resource] = []
        self.fail = ""
        self.reads = 0
        self.drift: Inventory | None = None

    def inventory(self) -> Inventory:
        self.reads += 1
        if self.reads == 2 and self.drift is not None:
            self.state = self.drift
        return self.state

    def perform(self, stage: Stage) -> None:
        self.trace.append("perform:" + stage.name)
        if self.fail == "perform:" + stage.name:
            raise RebuildError("Synthetic operation failure")

    def verify(self, stage: Stage) -> str:
        self.trace.append("verify:" + stage.name)
        return "" if self.fail == "verify:" + stage.name else "simulated-not-live"

    def delete(self, target: Resource) -> None:
        self.deleted.append(target)
        self.state = Inventory(
            tuple(item for item in self.state.resources if item != target),
            tuple(item for item in self.state.budgets if item != target),
        )


class RebuildTests(unittest.TestCase):
    def test_exact_mandatory_trace(self) -> None:
        expected = (
            "parameters dependencies discover images credential sql-users seed applications "
            "authentication staff health api-denial browser-redirect workload-sql "
            "model-standard model-capable restart"
        ).split()
        self.assertEqual([stage.name for stage in STAGES], expected)
        backend = MemoryBackend()
        evidence = rebuild(backend, LOCAL_SUBSCRIPTION)
        self.assertEqual(
            backend.trace,
            [f"{operation}:{name}" for name in expected for operation in ("perform", "verify")],
        )
        self.assertEqual([row["stage"] for row in evidence], expected)
        self.assertTrue(all(row["evidence"] == "simulated-not-live" for row in evidence))

    def test_every_operation_and_checkpoint_failure_stops_next_step(self) -> None:
        for index, stage in enumerate(STAGES):
            for operation in ("perform", "verify"):
                with self.subTest(stage=stage.name, operation=operation):
                    backend = MemoryBackend()
                    backend.fail = f"{operation}:{stage.name}"
                    with self.assertRaises(RebuildError):
                        rebuild(backend, LOCAL_SUBSCRIPTION)
                    self.assertEqual(backend.trace[-1], backend.fail)
                    self.assertEqual(
                        len(backend.trace), index * 2 + (1 if operation == "perform" else 2)
                    )
                    self.assertEqual(backend.deleted, [])

    def test_nonempty_either_inventory_blocks_bootstrap(self) -> None:
        for inventory in (
            Inventory((resource("Microsoft.App/jobs"),)),
            Inventory(budgets=(resource(BUDGET),)),
        ):
            backend = MemoryBackend(inventory)
            with self.assertRaisesRegex(RebuildError, "requires empty"):
                rebuild(backend, LOCAL_SUBSCRIPTION)
            self.assertEqual(backend.trace, [])

    def test_known_dependency_order_and_budget(self) -> None:
        kinds = (
            "Microsoft.Network/networkSecurityGroups",
            "Microsoft.Network/virtualNetworks",
            "Microsoft.Insights/components",
            "Microsoft.CognitiveServices/accounts",
            "Microsoft.App/managedEnvironments",
            "Microsoft.Insights/privateLinkScopes",
            "Microsoft.Network/privateEndpoints",
            "Microsoft.App/containerApps",
            "Microsoft.App/jobs",
        )
        records = tuple(resource(kind) for kind in kinds)
        project = resource("Microsoft.CognitiveServices/accounts/projects", "synthetic/project")
        scoped = resource("Microsoft.Insights/privateLinkScopes/scopedResources", "synthetic/link")
        inventory = Inventory((*records, project, scoped), (resource(BUDGET),))
        ordered = deletion_order(inventory, LOCAL_SUBSCRIPTION)
        positions = {item.kind: ordered.index(item) for item in ordered}
        for first, last in (
            ("Microsoft.App/containerApps", "Microsoft.App/managedEnvironments"),
            ("Microsoft.App/jobs", "Microsoft.App/managedEnvironments"),
            ("Microsoft.Network/privateEndpoints", "Microsoft.Network/virtualNetworks"),
            (
                "Microsoft.CognitiveServices/accounts/projects",
                "Microsoft.CognitiveServices/accounts",
            ),
            (
                "Microsoft.Insights/privateLinkScopes/scopedResources",
                "Microsoft.Insights/privateLinkScopes",
            ),
            ("Microsoft.Insights/privateLinkScopes", "Microsoft.Insights/components"),
            ("Microsoft.Network/virtualNetworks", "Microsoft.Network/networkSecurityGroups"),
        ):
            self.assertLess(positions[first], positions[last])
        self.assertEqual(ordered[-1].kind, BUDGET)
        backend = MemoryBackend(inventory)
        teardown(backend, LOCAL_SUBSCRIPTION)
        self.assertEqual(backend.deleted, list(ordered))
        self.assertEqual(backend.state, Inventory())

    def test_sql_child_before_parent_and_deterministic_order(self) -> None:
        parent = resource("Microsoft.Sql/servers")
        child = resource("Microsoft.Sql/servers/databases", "synthetic/database")
        one = Inventory((parent, child))
        self.assertEqual(deletion_order(one, LOCAL_SUBSCRIPTION), (child, parent))
        self.assertEqual(
            deletion_order(Inventory((child, parent)), LOCAL_SUBSCRIPTION), (child, parent)
        )

    def test_front_door_profile_before_private_link_environment_and_waf(self) -> None:
        app = resource("Microsoft.App/containerApps")
        job = resource("Microsoft.App/jobs")
        profile = resource("mIcRoSoFt.CdN/PrOfIlEs", "aaa-profile")
        environment = resource("Microsoft.App/managedEnvironments", "zzz-environment")
        waf = resource("Microsoft.Network/FrontDoorWebApplicationFirewallPolicies")
        expected = (app, job, profile, environment, waf)
        records = (environment, waf, job, profile, app)
        for items in (records, tuple(reversed(records))):
            with self.subTest(items=items):
                inventory = Inventory(items)
                self.assertEqual(deletion_order(inventory, LOCAL_SUBSCRIPTION), expected)
                backend = MemoryBackend(inventory)
                teardown(backend, LOCAL_SUBSCRIPTION)
                self.assertEqual(backend.deleted, list(expected))
                self.assertEqual(backend.state, Inventory())

    def test_invalid_scope_type_path_duplicate_and_safety_fail_before_delete(self) -> None:
        good = resource("Microsoft.App/jobs")
        invalid = (
            replace(good, resource_id=good.resource_id.replace("/ama/", "/other/")),
            replace(good, resource_id=good.resource_id.replace(LOCAL_SUBSCRIPTION, "other")),
            replace(good, resource_id=PREFIX.removesuffix("/providers/")),
            replace(good, resource_id=good.resource_id + "/.."),
            replace(good, resource_id=good.resource_id + "?api-version=bad"),
            replace(good, kind="Microsoft.Unknown/resources"),
            replace(good, kind="Microsoft.App/containerApps"),
            replace(good, locked=True),
            replace(good, retained=True),
            replace(good, locked=json.loads("null")),
            replace(good, retained=json.loads("0")),
        )
        for item in invalid:
            with self.subTest(item=item):
                backend = MemoryBackend(Inventory((item,)))
                with self.assertRaises(RebuildError):
                    teardown(backend, LOCAL_SUBSCRIPTION)
                self.assertEqual(backend.deleted, [])
        with self.assertRaises(RebuildError):
            canonical(
                Inventory((good, replace(good, resource_id=good.resource_id.upper()))),
                LOCAL_SUBSCRIPTION,
            )

    def test_budget_collection_cannot_hide_or_misclassify_resources(self) -> None:
        for inventory in (
            Inventory((resource(BUDGET),)),
            Inventory(budgets=(resource("Microsoft.App/jobs"),)),
        ):
            with self.assertRaises(RebuildError):
                canonical(inventory, LOCAL_SUBSCRIPTION)

    def test_invalid_subscription_even_when_empty(self) -> None:
        for subscription in ("", "not-a-uuid", "00000000-0000-0000-0000-000000000000"):
            with self.assertRaises(RebuildError):
                canonical(Inventory(), subscription)

    def test_inventory_drift_same_id_protection_addition_removal_and_budget(self) -> None:
        original = resource("Microsoft.App/jobs")
        inventory = Inventory((original,))
        for drift in (
            Inventory(),
            Inventory((replace(original, locked=True),)),
            Inventory((replace(original, retained=True),)),
            Inventory((replace(original, kind="Microsoft.App/containerApps"),)),
            Inventory((original, resource("Microsoft.App/containerApps"))),
            Inventory((original,), (resource(BUDGET),)),
        ):
            with self.subTest(drift=drift):
                backend = MemoryBackend(inventory)
                backend.drift = drift
                with self.assertRaises(RebuildError):
                    teardown(backend, LOCAL_SUBSCRIPTION)
                self.assertEqual(backend.deleted, [])

    def test_lingering_resource_or_budget_stops_deletion(self) -> None:
        for inventory in (
            Inventory((resource("Microsoft.App/jobs"), resource("Microsoft.App/containerApps"))),
            Inventory(budgets=(resource(BUDGET),)),
        ):
            backend = MemoryBackend(inventory)
            with patch.object(backend, "delete") as delete:
                with self.assertRaisesRegex(RebuildError, "not confirmed"):
                    teardown(backend, LOCAL_SUBSCRIPTION)
                self.assertEqual(delete.call_count, 1)

    def test_inventory_drift_after_first_delete_prevents_next_delete(self) -> None:
        backend = MemoryBackend(
            Inventory(
                (resource("Microsoft.App/jobs"), resource("Microsoft.App/managedEnvironments"))
            )
        )
        original = backend.delete

        def mutate_after_delete(target: Resource) -> None:
            original(target)
            backend.state = replace(backend.state, budgets=(resource(BUDGET),))

        with patch.object(backend, "delete", side_effect=mutate_after_delete) as delete:
            with self.assertRaisesRegex(RebuildError, "inventory changed"):
                teardown(backend, LOCAL_SUBSCRIPTION)
            self.assertEqual(delete.call_count, 1)
            self.assertEqual(len(backend.state.resources), 1)

    def test_final_empty_inventory_is_rechecked(self) -> None:
        backend = MemoryBackend()
        backend.drift = Inventory(budgets=(resource(BUDGET),))
        with self.assertRaisesRegex(RebuildError, "not empty"):
            teardown(backend, LOCAL_SUBSCRIPTION)
        self.assertEqual(backend.deleted, [])

    def test_delete_exception_is_not_hidden_or_rolled_back(self) -> None:
        backend = MemoryBackend(Inventory((resource("Microsoft.App/jobs"),)))
        with patch.object(backend, "delete", side_effect=RebuildError("synthetic denied")):
            with self.assertRaisesRegex(RebuildError, "synthetic denied"):
                teardown(backend, LOCAL_SUBSCRIPTION)
        self.assertEqual(len(backend.state.resources), 1)

    def test_disposable_sqlite_roundtrip_repeated_fresh_and_closed(self) -> None:
        for _ in range(2):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "synthetic.sqlite"
                backend = LocalBackend(path)
                evidence = rebuild(backend, LOCAL_SUBSCRIPTION)
                self.assertEqual(len(evidence), len(STAGES))
                reopened = object.__new__(LocalBackend)
                reopened.path = path
                self.assertEqual(reopened.verify(STAGES[-1]), "local-sql-verified")
                with reopened.connection() as db:
                    self.assertEqual(
                        db.execute("SELECT email FROM staff").fetchall(),
                        [("operator@example.test",)],
                    )
                self.assertEqual(len(teardown(backend, LOCAL_SUBSCRIPTION)), 10)
                self.assertEqual(backend.inventory(), Inventory())
            self.assertFalse(path.exists())

    def test_seed_and_staff_tamper_detected_through_new_connection(self) -> None:
        for table in ("cases", "staff", "audit"):
            with self.subTest(table=table), tempfile.TemporaryDirectory() as directory:
                backend = LocalBackend(Path(directory) / "synthetic.sqlite")
                rebuild(backend, LOCAL_SUBSCRIPTION)
                with backend.connection() as db:
                    db.execute(f"DELETE FROM {table}")
                with self.assertRaises(RebuildError):
                    backend.verify(STAGES[-1])

    def test_inventory_authoring_bound(self) -> None:
        records = tuple(resource("Microsoft.App/jobs", f"synthetic-{i}") for i in range(1001))
        self.assertEqual(len(canonical(Inventory(records[:1000]), LOCAL_SUBSCRIPTION)), 1000)
        with self.assertRaisesRegex(RebuildError, "1000-record"):
            canonical(Inventory(records), LOCAL_SUBSCRIPTION)

    def test_existing_database_is_never_opened_or_reseeded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "existing"
            path.write_bytes(b"SYNTHETIC existing sentinel")
            with self.assertRaises(FileExistsError):
                LocalBackend(path)
            self.assertEqual(path.read_bytes(), b"SYNTHETIC existing sentinel")

    def test_local_backend_rejects_missing_reordered_and_repeated_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            backend = LocalBackend(Path(directory) / "synthetic.sqlite")
            with self.assertRaises(RebuildError):
                backend.perform(STAGES[1])
            with self.assertRaises(RebuildError):
                backend.verify(STAGES[0])
            backend.perform(STAGES[0])
            with self.assertRaises(RebuildError):
                backend.perform(STAGES[0])

    def test_cli_dry_run_no_workspace_or_backend_reads(self) -> None:
        with (
            patch("zava_forward.orchestrator.rebuild.LocalBackend", side_effect=AssertionError),
            patch("tempfile.TemporaryDirectory", side_effect=AssertionError),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(main(["--dry-run"]), 0)
        report = json.loads(output.getvalue())
        self.assertIn("no Azure adapter", report["scope"])
        self.assertEqual(
            [row["name"] for row in report["stages"]], [stage.name for stage in STAGES]
        )
        order = report["teardown"]["order"]
        self.assertLess(
            order.index("microsoft.cdn/profiles"), order.index("microsoft.app/managedenvironments")
        )

    def test_cli_rehearsal_ignores_private_dataset_and_prints_only_synthetic_scope(self) -> None:
        with (
            patch.dict(os.environ, {"ZF_DATA": "/never-read/private.json", "ZF_STORE": "mssql"}),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(main(["--synthetic-local"]), 0)
        report = json.loads(output.getvalue())
        self.assertIn("not Azure/application acceptance", report["scope"])
        self.assertEqual(report["resources_remaining"], 0)
        self.assertEqual(report["budgets_remaining"], 0)
        self.assertNotIn("/never-read", output.getvalue())

    def test_cli_controlled_errors_do_not_disclose_raw_exception(self) -> None:
        for error in (OSError("PRIVATE canary"), RebuildError("PRIVATE canary")):
            with (
                patch("zava_forward.orchestrator.rebuild.LocalBackend", side_effect=error),
                contextlib.redirect_stdout(io.StringIO()) as output,
                contextlib.redirect_stderr(io.StringIO()) as diagnostics,
            ):
                self.assertEqual(main(["--synthetic-local"]), 1)
            self.assertEqual(output.getvalue(), "")
            self.assertIn("REBUILD_FAILED", diagnostics.getvalue())
            self.assertNotIn("PRIVATE", diagnostics.getvalue())

    def test_cli_has_no_cloud_apply_or_data_path_argument(self) -> None:
        for arguments in ([], ["--apply"], ["--synthetic-local", "--data", "private"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
                main(arguments)
            self.assertEqual(result.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
