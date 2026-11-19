"""Tests for issue #136 architecture-to-Bicep inventory, module matrix, and rebuild sequence."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, ClassVar

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "bicep_inventory", REPO_ROOT / "infra/scripts/bicep_inventory.py"
)
assert _SPEC is not None and _SPEC.loader is not None
bicep_inventory = importlib.util.module_from_spec(_SPEC)
sys.modules["bicep_inventory"] = bicep_inventory
_SPEC.loader.exec_module(bicep_inventory)


class BicepArchitectureInventory136Tests(unittest.TestCase):
    """Prove the three engineering acceptance criteria of Epic #136."""

    readme_text: ClassVar[str]
    bicep_tree: ClassVar[Any]
    arch_rows: ClassVar[tuple[dict[str, str], ...]]
    mod_rows: ClassVar[tuple[dict[str, str], ...]]
    seq_rows: ClassVar[tuple[dict[str, str], ...]]
    rebuild_stages: ClassVar[tuple[str, ...]]
    pipeline_ops: ClassVar[tuple[str, ...]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.readme_text = (REPO_ROOT / "infra/README.md").read_text(encoding="utf-8")
        cls.bicep_tree = bicep_inventory.scan_bicep_tree(REPO_ROOT)
        cls.arch_rows, arch_errs = bicep_inventory.parse_markdown_section_table(
            cls.readme_text, bicep_inventory.ARCH_HEADING, bicep_inventory.ARCH_COLUMNS
        )
        cls.mod_rows, mod_errs = bicep_inventory.parse_markdown_section_table(
            cls.readme_text, bicep_inventory.MODULE_HEADING, bicep_inventory.MODULE_COLUMNS
        )
        cls.seq_rows, seq_errs = bicep_inventory.parse_markdown_section_table(
            cls.readme_text, bicep_inventory.SEQUENCE_HEADING, bicep_inventory.SEQUENCE_COLUMNS
        )
        cls.rebuild_stages, stage_errs = bicep_inventory.load_rebuild_stages(REPO_ROOT)
        cls.pipeline_ops, pipe_errs = bicep_inventory.load_pipeline_operations(REPO_ROOT)
        if arch_errs or mod_errs or seq_errs or stage_errs or pipe_errs:
            raise AssertionError(
                f"Setup parse errors: {arch_errs + mod_errs + seq_errs + stage_errs + pipe_errs}"
            )

    def test_live_repository_passes_inventory_and_cli_check(self) -> None:
        report = bicep_inventory.verify_all(REPO_ROOT)
        self.assertTrue(report.ok, msg=f"Unexpected inventory errors: {report.errors}")
        self.assertEqual(report.errors, ())
        self.assertEqual(
            report.architecture_rows, len(bicep_inventory.REQUIRED_ARCHITECTURE_COMPONENTS)
        )
        self.assertEqual(report.module_rows, 20)
        self.assertEqual(report.sequence_steps, 12)
        self.assertEqual(len(report.rebuild_stages), 17)

        check_stdout = io.StringIO()
        with redirect_stdout(check_stdout):
            rc_check = bicep_inventory.main(["--check", "--repo-root", str(REPO_ROOT)])
        self.assertEqual(rc_check, 0)
        self.assertIn("20 Bicep modules", check_stdout.getvalue())

        json_stdout = io.StringIO()
        with redirect_stdout(json_stdout):
            rc_json = bicep_inventory.main(["--json", "--repo-root", str(REPO_ROOT)])
        self.assertEqual(rc_json, 0)
        payload = json.loads(json_stdout.getvalue())
        self.assertIs(payload["ok"], True)
        self.assertEqual(payload["errors"], [])
        self.assertEqual(payload["module_rows"], 20)

    def test_every_adr_proposed_resource_mapped_to_bicep_or_owned_manual(self) -> None:
        errors = bicep_inventory.verify_architecture_inventory(
            REPO_ROOT, self.bicep_tree, self.arch_rows
        )
        self.assertEqual(errors, [])

        dispositions = {
            row["Component ID"].strip("`"): row["Disposition"].strip("`") for row in self.arch_rows
        }
        self.assertEqual(dispositions["ledger-digest-verification"], "bicep")
        self.assertEqual(dispositions["entra-app-registration-and-roles"], "manual")
        self.assertEqual(dispositions["custom-domain-dns-records"], "manual")
        self.assertEqual(dispositions["contractor-entra-b2b-policy"], "manual")
        self.assertEqual(dispositions["deferred-egress-and-phase2-services"], "deferred")

        for row in self.arch_rows:
            disp = row["Disposition"].strip("`")
            if disp in {"manual", "deferred"}:
                self.assertIn("@jmservera", row["Named owner"])

    def test_bicep_comment_stripping_and_case_normalization(self) -> None:
        sample = (
            "// resource ignored 'Microsoft.Fake/singleLine@2024-01-01' = {}\n"
            "/* resource ignoredBlock 'Microsoft.Fake/block@2024-01-01' = {}\n"
            "   module fakeMod 'modules/fake.bicep' = {} */\n"
            "param label string = 'keep // inside string and ''escaped'' quote'\n"
            "resource scope 'microsoft.insights/privateLinkScopes@2021-07-01-preview' = {}\n"
            "resource existingVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {}\n"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            bicep_file = root / "infra" / "sample.bicep"
            bicep_file.parent.mkdir(parents=True)
            bicep_file.write_text(sample, encoding="utf-8")
            summary = bicep_inventory.parse_bicep_file(bicep_file, root)

        self.assertEqual(
            summary.provisioned_types, frozenset({"microsoft.insights/privatelinkscopes"})
        )
        self.assertEqual(summary.existing_types, frozenset({"microsoft.keyvault/vaults"}))
        self.assertEqual(summary.module_targets, ())
        self.assertIn(
            "microsoft.insights/privatelinkscopes",
            self.bicep_tree.files["infra/modules/monitoring.bicep"].provisioned_types,
        )

    def test_architecture_inventory_fails_closed_on_missing_row_owner_or_fake_arm_type(
        self,
    ) -> None:
        reduced = [
            dict(row)
            for row in self.arch_rows
            if row["Component ID"].strip("`") != "custom-domain-dns-records"
        ]
        missing_errs = bicep_inventory.verify_architecture_inventory(
            REPO_ROOT, self.bicep_tree, reduced
        )
        self.assertTrue(any("custom-domain-dns-records" in err for err in missing_errs))

        ownerless = [dict(row) for row in self.arch_rows]
        for row in ownerless:
            if row["Component ID"].strip("`") == "entra-app-registration-and-roles":
                row["Named owner"] = "TBD"
        owner_errs = bicep_inventory.verify_architecture_inventory(
            REPO_ROOT, self.bicep_tree, ownerless
        )
        self.assertTrue(any("entra-app-registration-and-roles" in err for err in owner_errs))

        fake_arm = [dict(row) for row in self.arch_rows]
        for row in fake_arm:
            if row["Component ID"].strip("`") == "key-vault-resource":
                row["ARM resource types or external plane"] = "`Microsoft.Fake/nonExistentVaults`"
        arm_errs = bicep_inventory.verify_architecture_inventory(
            REPO_ROOT, self.bicep_tree, fake_arm
        )
        self.assertTrue(any("microsoft.fake/nonexistentvaults" in err for err in arm_errs))

        missing_path = [dict(row) for row in self.arch_rows]
        for row in missing_path:
            if row["Component ID"].strip("`") == "container-registry":
                row["Bicep template or artifact"] = "`infra/modules/does-not-exist.bicep`"
        path_errs = bicep_inventory.verify_architecture_inventory(
            REPO_ROOT, self.bicep_tree, missing_path
        )
        self.assertTrue(any("infra/modules/does-not-exist.bicep" in err for err in path_errs))

    def test_module_delivery_matrix_matches_all_disk_modules_callers_and_types(self) -> None:
        errors = bicep_inventory.verify_module_delivery_matrix(
            REPO_ROOT, self.bicep_tree, self.mod_rows
        )
        self.assertEqual(errors, [])

        disk_modules = sorted(
            p.relative_to(REPO_ROOT).as_posix()
            for p in (REPO_ROOT / "infra/modules").glob("*.bicep")
        )
        table_modules = sorted(row["Module path"].strip("`") for row in self.mod_rows)
        self.assertEqual(table_modules, disk_modules)
        self.assertTrue(self.bicep_tree.placeholder_workers)

        by_mod = {row["Module path"].strip("`"): row for row in self.mod_rows}
        self.assertEqual(
            by_mod["infra/modules/containerapps.bicep"]["Delivery status"].strip("`"),
            "delivered-placeholder-workers",
        )
        for guard_mod in (
            "infra/modules/guard.bicep",
            "infra/modules/edge-existing-guard.bicep",
            "infra/modules/iothub-scope-guard.bicep",
            "infra/modules/staff-initializer-guard.bicep",
        ):
            self.assertEqual(by_mod[guard_mod]["Delivery status"].strip("`"), "delivered-guard")

    def test_module_delivery_matrix_fails_closed_on_drift_or_premature_worker_status(self) -> None:
        dropped = [
            dict(row)
            for row in self.mod_rows
            if row["Module path"].strip("`") != "infra/modules/sql.bicep"
        ]
        drop_errs = bicep_inventory.verify_module_delivery_matrix(
            REPO_ROOT, self.bicep_tree, dropped
        )
        self.assertTrue(any("infra/modules/sql.bicep" in err for err in drop_errs))

        phantom = [
            *[dict(row) for row in self.mod_rows],
            {
                "Module path": "`infra/modules/phantom.bicep`",
                "Wired in entrypoint(s)": "`infra/main.bicep`",
                "Provisioned ARM resource types": "`none (compile-time guard)`",
                "Delivery status": "`delivered-guard`",
                "Notes and remaining gates": "Phantom test module",
            },
        ]
        phantom_errs = bicep_inventory.verify_module_delivery_matrix(
            REPO_ROOT, self.bicep_tree, phantom
        )
        self.assertTrue(any("infra/modules/phantom.bicep" in err for err in phantom_errs))

        premature = [dict(row) for row in self.mod_rows]
        for row in premature:
            if row["Module path"].strip("`") == "infra/modules/containerapps.bicep":
                row["Delivery status"] = "`delivered`"
        premature_errs = bicep_inventory.verify_module_delivery_matrix(
            REPO_ROOT, self.bicep_tree, premature
        )
        self.assertTrue(any("delivered-placeholder-workers" in err for err in premature_errs))

        caller_drift = [dict(row) for row in self.mod_rows]
        for row in caller_drift:
            if row["Module path"].strip("`") == "infra/modules/envDns.bicep":
                row["Wired in entrypoint(s)"] = "`infra/main.bicep`"
        caller_errs = bicep_inventory.verify_module_delivery_matrix(
            REPO_ROOT, self.bicep_tree, caller_drift
        )
        self.assertTrue(any("caller mismatch" in err for err in caller_errs))

    def test_from_empty_sequence_maps_every_step_and_rebuild_stage_to_repo_artifacts(self) -> None:
        errors = bicep_inventory.verify_from_empty_sequence(
            REPO_ROOT, self.seq_rows, self.rebuild_stages, self.pipeline_ops
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            self.pipeline_ops,
            (
                "plan",
                "deploy",
                "publish",
                "changed-images",
                "verify-environment",
                "verify-federation",
            ),
        )
        self.assertEqual(self.rebuild_stages[0], "parameters")
        self.assertEqual(self.rebuild_stages[-1], "restart")

    def test_from_empty_sequence_fails_closed_on_missing_script_undocumented_step_or_stage_drift(
        self,
    ) -> None:
        bad_script = [dict(row) for row in self.seq_rows]
        bad_script[2]["Repository template or script"] = "`infra/scripts/missing-step.py`"
        script_errs = bicep_inventory.verify_from_empty_sequence(
            REPO_ROOT, bad_script, self.rebuild_stages, self.pipeline_ops
        )
        self.assertTrue(any("infra/scripts/missing-step.py" in err for err in script_errs))

        undocumented = [dict(row) for row in self.seq_rows]
        undocumented[4]["Verification check"] = "undocumented"
        undoc_errs = bicep_inventory.verify_from_empty_sequence(
            REPO_ROOT, undocumented, self.rebuild_stages, self.pipeline_ops
        )
        self.assertTrue(any("undocumented 'Verification check'" in err for err in undoc_errs))

        stage_gap = [dict(row) for row in self.seq_rows if row["Step"] != "8"]
        gap_errs = bicep_inventory.verify_from_empty_sequence(
            REPO_ROOT, stage_gap, self.rebuild_stages, self.pipeline_ops
        )
        self.assertTrue(any("step numbering error" in err for err in gap_errs))
        self.assertTrue(any("rebuild stage coverage/order" in err for err in gap_errs))

        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_root = Path(tmp_dir)
            (bad_root / "infra").mkdir()
            (bad_root / "infra/README.md").write_text("# Broken README\n", encoding="utf-8")
            err_buf = io.StringIO()
            with redirect_stderr(err_buf):
                rc = bicep_inventory.main(["--check", "--repo-root", str(bad_root)])
        self.assertEqual(rc, 1)
        self.assertIn("ERROR:", err_buf.getvalue())


if __name__ == "__main__":
    unittest.main()
