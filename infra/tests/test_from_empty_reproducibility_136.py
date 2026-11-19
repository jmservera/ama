"""Unit and fail-closed mutation tests for Issue #136 from-empty deployment reproducibility."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
INFRA_DIR = ROOT / "infra"


def _load_script_module(
    module_name: str, script_path: Path, *, register_sys_modules: bool = True
) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    if register_sys_modules:
        sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if register_sys_modules:
            sys.modules.pop(module_name, None)
    return module


REPRO_MOD = _load_script_module(
    "_test_reproducibility_check_136",
    INFRA_DIR / "scripts" / "reproducibility_check.py",
)
INVENTORY_MOD = _load_script_module(
    "_test_bicep_inventory_136",
    INFRA_DIR / "scripts" / "bicep_inventory.py",
)


def _create_fixture_repo(base_dir: Path) -> Path:
    """Build a fast isolated fixture workspace with writable copies of mutable infra files."""
    repo = base_dir / "repo"
    (repo / "infra" / "parameters").mkdir(parents=True, exist_ok=True)
    (repo / "infra" / "scripts").mkdir(parents=True, exist_ok=True)
    (repo / "infra" / "sql").mkdir(parents=True, exist_ok=True)
    (repo / "infra" / "entra").mkdir(parents=True, exist_ok=True)

    # Symlink read-only directories and copy mutable files edited by mutation tests.
    os.symlink(INFRA_DIR / "modules", repo / "infra" / "modules")

    for rel_file in (
        "infra/README.md",
        "infra/main.bicep",
        "infra/governance.bicep",
        "infra/staff-initializer-rbac.bicep",
        "infra/main.bicepparam",
        "infra/main.test.bicepparam",
        "infra/main.pilot.example.bicepparam",
        "infra/parameters/dev.bicepparam",
        "infra/parameters/prod.bicepparam",
        "infra/defender-decision.json",
        "infra/secret-inventory.json",
        "infra/entra/app-registration.json",
        "infra/sql/resident-showcase.sql",
        "infra/sql/resident-assistant.sql",
        "infra/scripts/pipeline.py",
        "infra/scripts/reproducibility_check.py",
        "infra/scripts/tenant-readiness-preflight.py",
        "infra/scripts/deploy.py",
        "infra/scripts/setup-entra.py",
        "infra/scripts/credential_arm.py",
        "infra/scripts/create-sql-users.py",
        "infra/scripts/create-sql-users.sql",
        "infra/scripts/resident_sensor_seed.py",
        "infra/scripts/initialize-workbench-staff.py",
        "infra/scripts/private-cutover-proof.py",
    ):
        shutil.copy2(ROOT / rel_file, repo / rel_file)

    for project in ("api", "agents", "orchestrator", "importer"):
        proj_dir = repo / "src" / project
        proj_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "src" / project / "Dockerfile", proj_dir / "Dockerfile")

    orch_pkg = repo / "src" / "orchestrator" / "src" / "zava_forward" / "orchestrator"
    orch_pkg.mkdir(parents=True, exist_ok=True)
    for orch_file in ("rebuild.py", "rebuild_azure.py"):
        shutil.copy2(
            ROOT / "src" / "orchestrator" / "src" / "zava_forward" / "orchestrator" / orch_file,
            orch_pkg / orch_file,
        )
    return repo


class FromEmptyReproducibility136Tests(unittest.TestCase):
    """Proves Issue #136 from-empty deployment reproducibility criteria (a), (b), and (c)."""

    def test_live_repository_passes_via_pipeline_and_reproducibility_check(self) -> None:
        # Load pipeline.py without registering in sys.modules (matches test_pipeline.py pattern).
        unregistered_pipeline = _load_script_module(
            "_unregistered_pipeline_136",
            INFRA_DIR / "scripts" / "pipeline.py",
            register_sys_modules=False,
        )
        from_pipeline = unregistered_pipeline.verify_from_empty_deployment_reproducibility(ROOT)
        from_repro = REPRO_MOD.verify_from_empty_deployment_reproducibility(ROOT)
        self.assertTrue(from_pipeline.ok, msg=from_pipeline.errors)
        self.assertTrue(from_repro.ok, msg=from_repro.errors)
        self.assertEqual(from_pipeline.to_dict(), from_repro.to_dict())

        inventory_report = INVENTORY_MOD.verify_all(ROOT)
        self.assertTrue(inventory_report.ok, msg=inventory_report.errors)

    def test_criterion_a_canonical_steps_registered_and_documented_without_manual_gaps(
        self,
    ) -> None:
        expected_steps = ("preflight", "what-if", "deploy", "sql-init", "seed", "smoke")
        report = REPRO_MOD.verify_step_registration_and_docs(ROOT)
        self.assertTrue(report.ok, msg=report.errors)
        self.assertEqual(report.registered_steps, expected_steps)
        self.assertEqual(report.documented_steps, expected_steps)
        self.assertEqual(report.undocumented_manual_steps, ())
        self.assertEqual(len(report.covered_rebuild_stages), 17)
        self.assertEqual(len(set(report.covered_rebuild_stages)), 17)

    def test_criterion_a_fails_closed_when_step_unregistered_in_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            pipeline_path = repo / "infra" / "scripts" / "pipeline.py"
            text = pipeline_path.read_text(encoding="utf-8")
            mutated = text.replace('    "seed",\n', "", 1)
            self.assertNotEqual(text, mutated)
            pipeline_path.write_text(mutated, encoding="utf-8")

            report = REPRO_MOD.verify_step_registration_and_docs(repo)
            self.assertFalse(report.ok)
            self.assertTrue(
                any("FROM_EMPTY_STEP_ORDER" in err for err in report.errors),
                msg=report.errors,
            )

    def test_criterion_a_fails_closed_on_undocumented_manual_steps_in_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            readme_path = repo / "infra" / "README.md"
            original = readme_path.read_text(encoding="utf-8")

            # Case 1: Automated step acquires an ad-hoc manual prerequisite.
            manual_sql = original.replace(
                "| `sql-init` | `FROM_EMPTY_STEPS[3]` (`check_sql`) | `sql-users` | "
                "`infra/scripts/create-sql-users.py`, `infra/scripts/create-sql-users.sql`, "
                "`infra/sql/resident-showcase.sql`, `infra/sql/resident-assistant.sql`, "
                "`infra/staff-initializer-rbac.bicep` | none (automated from repository files) |",
                "| `sql-init` | `FROM_EMPTY_STEPS[3]` (`check_sql`) | `sql-users` | "
                "`infra/scripts/create-sql-users.py`, `infra/scripts/create-sql-users.sql`, "
                "`infra/sql/resident-showcase.sql`, `infra/sql/resident-assistant.sql`, "
                "`infra/staff-initializer-rbac.bicep` | Open portal query editor by hand |",
            )
            self.assertNotEqual(original, manual_sql)
            readme_path.write_text(manual_sql, encoding="utf-8")
            report_sql = REPRO_MOD.verify_step_registration_and_docs(repo)
            self.assertFalse(report_sql.ok)
            self.assertIn("sql-init", report_sql.undocumented_manual_steps)

            # Case 2: Preflight prerequisite drops its named owner.
            unowned_preflight = original.replace(
                "Juan Manuel Servera (@jmservera)", "platform team"
            )
            readme_path.write_text(unowned_preflight, encoding="utf-8")
            report_owner = REPRO_MOD.verify_step_registration_and_docs(repo)
            self.assertFalse(report_owner.ok)
            self.assertIn("preflight", report_owner.undocumented_manual_steps)

            # Case 3: Section prose introduces a manual portal workaround.
            prose_leak = original.replace(
                "zero unrecorded operator steps:",
                "zero unrecorded operator steps unless you run manually in portal:",
            )
            readme_path.write_text(prose_leak, encoding="utf-8")
            report_prose = REPRO_MOD.verify_step_registration_and_docs(repo)
            self.assertFalse(report_prose.ok)
            self.assertIn("section-prose", report_prose.undocumented_manual_steps)

    def test_criterion_a_fails_closed_on_missing_artifact_or_stage_partition_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            (repo / "infra" / "scripts" / "resident_sensor_seed.py").unlink()
            missing_report = REPRO_MOD.verify_step_registration_and_docs(repo)
            self.assertFalse(missing_report.ok)
            self.assertTrue(
                any("resident_sensor_seed.py" in err for err in missing_report.errors),
                msg=missing_report.errors,
            )

    def test_criterion_b_bicepparam_compiles_via_az_bicep_and_matches_offline_parser(
        self,
    ) -> None:
        az_bin = shutil.which("az")
        if az_bin is None:
            self.skipTest("az CLI is not installed in this test environment")

        for rel_param in ("infra/parameters/dev.bicepparam", "infra/parameters/prod.bicepparam"):
            param_path = ROOT / rel_param
            offline = REPRO_MOD.parse_bicepparam_file(param_path, ROOT)
            self.assertEqual(offline.errors, ())
            self.assertEqual(offline.using_target, "infra/main.bicep")

            completed = subprocess.run(
                [az_bin, "bicep", "build-params", "--file", str(param_path), "--stdout"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            compiled_outer = json.loads(completed.stdout)
            compiled_inner = json.loads(compiled_outer["parametersJson"])["parameters"]
            compiled_values = {key: spec["value"] for key, spec in compiled_inner.items()}
            self.assertEqual(offline.parameters, compiled_values)

    def test_criterion_b_defaultless_parameter_satisfied_by_bicepparam_or_pipeline_injection(
        self,
    ) -> None:
        live_cov = REPRO_MOD.verify_bicep_parameter_coverage(ROOT)
        self.assertTrue(live_cov.ok, msg=live_cov.errors)
        self.assertEqual(
            live_cov.defaultless_parameters,
            ("alertEmail", "sqlAdminGroupName", "sqlAdminGroupObjectId"),
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            main_bicep = repo / "infra" / "main.bicep"
            dev_param = repo / "infra" / "parameters" / "dev.bicepparam"
            prod_param = repo / "infra" / "parameters" / "prod.bicepparam"
            pipeline_py = repo / "infra" / "scripts" / "pipeline.py"

            base_bicep = main_bicep.read_text(encoding="utf-8")
            main_bicep.write_text(
                base_bicep + "\nparam syntheticAuditEndpoint string\n",
                encoding="utf-8",
            )

            # 1. Missing from both .bicepparam files and pipeline.py -> fails closed.
            uncovered = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertFalse(uncovered.ok)
            self.assertEqual(uncovered.coverage_sources["syntheticAuditEndpoint"], "uncovered")

            # 2. Supplied in dev.bicepparam only (missing from prod.bicepparam) -> still fails.
            base_dev = dev_param.read_text(encoding="utf-8")
            dev_param.write_text(
                base_dev + "param syntheticAuditEndpoint = 'https://audit-dev.internal'\n",
                encoding="utf-8",
            )
            half_covered = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertFalse(half_covered.ok)
            self.assertEqual(half_covered.coverage_sources["syntheticAuditEndpoint"], "uncovered")

            # 3. Supplied in both dev.bicepparam and prod.bicepparam -> passes via bicepparam.
            base_prod = prod_param.read_text(encoding="utf-8")
            prod_param.write_text(
                base_prod + "param syntheticAuditEndpoint = 'https://audit-prod.internal'\n",
                encoding="utf-8",
            )
            via_bicepparam = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertTrue(via_bicepparam.ok, msg=via_bicepparam.errors)
            self.assertEqual(
                via_bicepparam.coverage_sources["syntheticAuditEndpoint"], "bicepparam"
            )

            # 4. Omitted from .bicepparam files, explicitly injected by pipeline.py -> passes.
            dev_param.write_text(base_dev, encoding="utf-8")
            prod_param.write_text(base_prod, encoding="utf-8")
            base_pipeline = pipeline_py.read_text(encoding="utf-8")
            injected_pipeline = base_pipeline.replace(
                '    "entraBearerOnly",\n}',
                '    "entraBearerOnly",\n    "syntheticAuditEndpoint",\n}',
                1,
            )
            self.assertNotEqual(base_pipeline, injected_pipeline)
            pipeline_py.write_text(injected_pipeline, encoding="utf-8")
            via_pipeline = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertTrue(via_pipeline.ok, msg=via_pipeline.errors)
            self.assertEqual(via_pipeline.coverage_sources["syntheticAuditEndpoint"], "pipeline")

    def test_criterion_b_fails_closed_on_ast_drift_unknown_param_or_secret_literal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            dev_param = repo / "infra" / "parameters" / "dev.bicepparam"
            pipeline_py = repo / "infra" / "scripts" / "pipeline.py"

            base_dev = dev_param.read_text(encoding="utf-8")
            # Construct synthetic secret pattern dynamically so source scanners stay clean.
            dynamic_secret = "SharedAccess" + "Key=" + ("A" * 24) + "=="
            dev_param.write_text(
                base_dev + f"param undeclaredParam = '{dynamic_secret}'\n",
                encoding="utf-8",
            )
            bad_param_cov = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertFalse(bad_param_cov.ok)
            self.assertTrue(
                any("undeclaredParam" in err for err in bad_param_cov.errors),
                msg=bad_param_cov.errors,
            )
            self.assertTrue(
                any("secret-like literal" in err for err in bad_param_cov.errors),
                msg=bad_param_cov.errors,
            )

            dev_param.write_text(base_dev, encoding="utf-8")
            drifted_pipeline = pipeline_py.read_text(encoding="utf-8").replace(
                "INJECTED_PARAMETERS = frozenset(",
                'INJECTED_PARAMETERS = frozenset({"alertEmail"}) or frozenset(',
                1,
            )
            pipeline_py.write_text(drifted_pipeline, encoding="utf-8")
            drift_cov = REPRO_MOD.verify_bicep_parameter_coverage(repo)
            self.assertFalse(drift_cov.ok)
            self.assertTrue(
                any("INJECTED_PARAMETERS" in err for err in drift_cov.errors),
                msg=drift_cov.errors,
            )

    def test_criterion_c_offline_dry_run_is_deterministic_and_isolates_ambient_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            summary_sentinel = Path(tmp) / "step-summary.md"
            summary_sentinel.write_text("KEEP_UNCHANGED\n", encoding="utf-8")

            with patch.dict(os.environ, {}, clear=True):
                dev_clean = REPRO_MOD.execute_from_empty_dry_run(ROOT, environment="dev")
                prod_clean = REPRO_MOD.execute_from_empty_dry_run(ROOT, environment="prod")

            noisy_env = {
                "DEPLOY_PARAMETERS": '{"corrupted": true}',
                "GITHUB_STEP_SUMMARY": str(summary_sentinel),
                "RELEASE_SHA": "f" * 40,
            }
            with patch.dict(os.environ, noisy_env, clear=True):
                dev_noisy = REPRO_MOD.execute_from_empty_dry_run(ROOT, environment="dev")
                prod_noisy = REPRO_MOD.execute_from_empty_dry_run(ROOT, environment="prod")

            self.assertTrue(dev_clean.ok, msg=dev_clean.errors)
            self.assertTrue(prod_clean.ok, msg=prod_clean.errors)
            self.assertEqual(
                tuple(step.step_id for step in dev_clean.steps),
                ("preflight", "what-if", "deploy", "sql-init", "seed", "smoke"),
            )
            self.assertEqual(dev_clean, dev_noisy)
            self.assertEqual(prod_clean, prod_noisy)
            self.assertNotEqual(dev_clean.sequence_digest, prod_clean.sequence_digest)
            self.assertNotEqual(dev_clean.parameter_sha256, prod_clean.parameter_sha256)
            self.assertEqual(summary_sentinel.read_text(encoding="utf-8"), "KEEP_UNCHANGED\n")

    def test_criterion_c_dry_run_tracks_bicepparam_edits_and_fails_closed_on_corrupt_files(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_fixture_repo(Path(tmp))
            baseline = REPRO_MOD.execute_from_empty_dry_run(repo, environment="dev")
            self.assertTrue(baseline.ok, msg=baseline.errors)

            # Changing monthlyBudget in parameters/dev.bicepparam alters parameter_sha256 & digest.
            dev_param = repo / "infra" / "parameters" / "dev.bicepparam"
            dev_param.write_text(
                dev_param.read_text(encoding="utf-8").replace(
                    "param monthlyBudget = 300", "param monthlyBudget = 450"
                ),
                encoding="utf-8",
            )
            updated = REPRO_MOD.execute_from_empty_dry_run(repo, environment="dev")
            self.assertTrue(updated.ok, msg=updated.errors)
            self.assertNotEqual(baseline.parameter_sha256, updated.parameter_sha256)
            self.assertNotEqual(baseline.sequence_digest, updated.sequence_digest)

            # Corrupting create-sql-users.sql causes Step 4 (sql-init) to fail closed.
            sql_script = repo / "infra" / "scripts" / "create-sql-users.sql"
            sql_script.write_text("SELECT 1;\n", encoding="utf-8")
            broken = REPRO_MOD.execute_from_empty_dry_run(repo, environment="dev")
            self.assertFalse(broken.ok)
            statuses = {step.step_id: step.status for step in broken.steps}
            self.assertEqual(statuses["sql-init"], "failed")
            self.assertTrue(any("sql-init failed" in err for err in broken.errors))

    def test_cli_check_and_dry_run_json_modes_exit_zero(self) -> None:
        check_buf = io.StringIO()
        with contextlib.redirect_stdout(check_buf):
            rc_check = REPRO_MOD.main(["--check", "--json"])
        self.assertEqual(rc_check, 0)
        check_payload = json.loads(check_buf.getvalue())
        self.assertTrue(check_payload["ok"])

        dry_buf = io.StringIO()
        with contextlib.redirect_stdout(dry_buf):
            rc_dry = REPRO_MOD.main(["--dry-run", "--environment", "prod", "--json"])
        self.assertEqual(rc_dry, 0)
        dry_payload = json.loads(dry_buf.getvalue())
        self.assertTrue(dry_payload["ok"])
        self.assertEqual(len(dry_payload["steps"]), 6)


if __name__ == "__main__":
    unittest.main()
