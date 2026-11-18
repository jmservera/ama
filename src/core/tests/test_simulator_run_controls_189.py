"""Focused runtime and Bicep contract tests for simulator run controls (issue #189)."""

import asyncio
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import run_plan
from zava_forward.core.synthetic.run_governance import (
    MAX_TIME_LIMIT_MINUTES,
    MAX_TIME_LIMIT_SECONDS,
    BudgetAlertContract,
    RunGovernance,
    SimulatorRunControls,
    governed_text,
    resolve_duration_seconds,
)
from zava_forward.core.synthetic.run_plan import (
    RunController,
    RunPlan,
    record,
    verify_bicep_run_controls,
)
from zava_forward.core.synthetic.sensor_stream import (
    Pacer,
    RunBudget,
    StreamError,
    accountable_text,
)

INFRA = Path(__file__).resolve().parents[3] / "infra"


def default_alert(**overrides: object) -> BudgetAlertContract:
    base = BudgetAlertContract(
        threshold_percent=80.0,
        alert_rule_reference="budget-iot-hub-actual80",
        alert_owner_reference="Platform Cost Owner",
        threshold_type="Actual",
        budget_cap_usd=5.0,
        budget_alert_gbp=Decimal("4.00"),
        budget_cap_gbp=Decimal("5.00"),
    )
    return replace(base, **overrides)  # type: ignore[arg-type]


def default_controls(**overrides: object) -> SimulatorRunControls:
    base = SimulatorRunControls(
        owner="Juan Manuel Servera",
        time_limit_minutes=10.0,
        budget_alert=default_alert(),
    )
    return replace(base, **overrides)  # type: ignore[arg-type]


class OwnerEnforcementTests(unittest.TestCase):
    def test_rejects_anonymous_blank_placeholder_template_and_non_identifier_owners(self) -> None:
        disallowed: tuple[object, ...] = (
            "",
            "   ",
            "\t\n",
            "anonymous",
            "ANON",
            "guest",
            "unowned",
            "unattended",
            "system",
            "auto",
            "automated",
            "bot",
            "TBD",
            "TBC",
            "todo",
            "pending",
            "none",
            "null",
            "nil",
            "N/A",
            "na",
            "unknown",
            "nobody",
            "unassigned",
            "<owner>",
            "---",
            "...",
            "???",
            "Owner\x00Name",
            "Owner\nName",
            "x" * 161,
            None,
            123,
            True,
        )
        for bad in disallowed:
            with self.subTest(bad=bad):
                self.assertFalse(accountable_text(bad))
                self.assertFalse(governed_text(bad))
                with self.assertRaisesRegex(StreamError, "^RUN_OWNER_REQUIRED$"):
                    default_controls(owner=bad).preflight()
                with self.assertRaisesRegex(StreamError, "^RUN_OWNER_COST_ALERT_REQUIRED$"):
                    RunBudget(
                        owner=bad,  # type: ignore[arg-type]
                        cost_reference="estimate:0.33USD",
                        alert_reference="budget-iot-hub-actual80",
                    ).preflight()

    def test_accepts_named_human_and_role_identifiers(self) -> None:
        valid_owners = (
            "Juan Manuel Servera",
            "Housing Retrofit Programme Manager",
            "Platform On-Call (UK South)",
            "alerts-ops@zavanorthhomes.example",
            "o",
        )
        for owner in valid_owners:
            with self.subTest(owner=owner):
                self.assertTrue(accountable_text(owner))
                self.assertTrue(governed_text(owner))
                summary = default_controls(owner=f"  {owner}  ").preflight()
                self.assertEqual(summary["owner"], owner)

    def test_pacer_enforces_budget_preflight_and_bounded_rate_mutation(self) -> None:
        with self.assertRaisesRegex(StreamError, "^RUN_OWNER_COST_ALERT_REQUIRED$"):
            Pacer(RunBudget(owner="anonymous", cost_reference="cost", alert_reference="alert"))
        with self.assertRaisesRegex(StreamError, "^INVALID_RUN_LIMIT$"):
            Pacer(
                RunBudget(
                    owner="Juan",
                    cost_reference="cost",
                    alert_reference="alert",
                    max_seconds=3601,
                )
            )
        pacer = Pacer(RunBudget(owner="Juan", cost_reference="cost", alert_reference="alert"))
        for bad_rate in (0, -1, 100.1, float("nan"), float("inf"), True, False):
            with self.subTest(bad_rate=bad_rate):
                with self.assertRaisesRegex(StreamError, "^INVALID_RUN_LIMIT$"):
                    pacer.set_max_per_second(bad_rate)
                bad_pacer = Pacer(
                    RunBudget(
                        owner="Juan",
                        cost_reference="cost",
                        alert_reference="alert",
                        max_per_second=bad_rate,
                    )
                )
                with self.assertRaisesRegex(StreamError, "^INVALID_RUN_RATE$"):
                    asyncio.run(bad_pacer.admit_send())


class BoundedDurationTests(unittest.TestCase):
    def test_resolves_minutes_seconds_and_agreeing_pair_and_rejects_unbounded_or_mismatched(
        self,
    ) -> None:
        self.assertEqual(resolve_duration_seconds(time_limit_minutes=15), 900.0)
        self.assertEqual(resolve_duration_seconds(max_duration_seconds=240), 240.0)
        self.assertEqual(
            resolve_duration_seconds(max_duration_seconds=600, time_limit_minutes=10),
            600.0,
        )
        self.assertEqual(MAX_TIME_LIMIT_MINUTES, 60.0)
        self.assertEqual(MAX_TIME_LIMIT_SECONDS, 3600.0)
        gov = RunGovernance.from_minutes(
            run_owner="Juan Manuel Servera",
            time_limit_minutes=10,
            budget_alert_gbp="4.00",
            budget_cap_gbp="5.00",
        )
        self.assertEqual(gov.max_duration_seconds, 600.0)
        self.assertEqual(gov.time_limit_minutes, 10.0)

        with self.assertRaisesRegex(StreamError, "^TIME_LIMIT_REQUIRED$"):
            resolve_duration_seconds()
        for bad_minutes in (0, -1, 0.01, 60.01, float("inf"), float("nan"), True, "10"):
            with self.subTest(bad_minutes=bad_minutes):
                with self.assertRaisesRegex(StreamError, "^TIME_LIMIT_REQUIRED$"):
                    resolve_duration_seconds(time_limit_minutes=bad_minutes)  # type: ignore[arg-type]
        for bad_seconds in (0, 0.5, -5, 3600.1, float("inf"), float("nan"), False, "600"):
            with self.subTest(bad_seconds=bad_seconds):
                with self.assertRaisesRegex(StreamError, "^TIME_LIMIT_REQUIRED$"):
                    resolve_duration_seconds(max_duration_seconds=bad_seconds)  # type: ignore[arg-type]
        with self.assertRaisesRegex(StreamError, "^TIME_LIMIT_MISMATCH$"):
            resolve_duration_seconds(max_duration_seconds=600, time_limit_minutes=5)

    def test_cli_supports_time_limit_minutes_and_alert_owner_and_refuses_invalid_inputs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "estimate.json"
            base = [
                "--homes",
                "10",
                "--owner",
                "Juan Manuel Servera",
                "--budget-usd",
                "5",
                "--alert-reference",
                "budget-iot-hub-actual80",
                "--out",
                str(out),
            ]
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                rc = run_plan.main(
                    [*base, "--time-limit-minutes", "10", "--alert-owner", "Platform Cost Owner"]
                )
            self.assertEqual(rc, 0)
            saved = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(saved["plan"]["max_seconds"], 600.0)
            self.assertEqual(saved["plan"]["alert_owner"], "Platform Cost Owner")

            for bad_extra, expected_code in (
                (["--max-seconds", "300", "--time-limit-minutes", "10"], "TIME_LIMIT_MISMATCH"),
                (["--time-limit-minutes", "61"], "TIME_LIMIT_REQUIRED"),
                (["--alert-owner", "anonymous"], "RUN_OWNER_COST_ALERT_REQUIRED"),
            ):
                stderr = io.StringIO()
                with self.subTest(bad_extra=bad_extra), redirect_stderr(stderr):
                    code = run_plan.main([*base, *bad_extra])
                self.assertEqual(code, 2)
                self.assertIn(expected_code, stderr.getvalue())


class LinkedBudgetAlertTests(unittest.TestCase):
    def test_budget_alert_contract_validates_threshold_rule_owner_and_amounts(self) -> None:
        contract = default_alert()
        self.assertEqual(contract.alert_fires_at_usd, 4.0)
        as_dict = contract.as_dict()
        self.assertEqual(as_dict["budget_alert_gbp"], "4.00")
        self.assertEqual(as_dict["budget_cap_gbp"], "5.00")
        self.assertEqual(as_dict["alert_owner_reference"], "Platform Cost Owner")

        for field_name in ("alert_rule_reference", "alert_owner_reference"):
            for bad in ("", "anonymous", "TBD", "<alert>", "---"):
                with self.subTest(field_name=field_name, bad=bad):
                    with self.assertRaisesRegex(StreamError, "^RUN_OWNER_COST_ALERT_REQUIRED$"):
                        default_alert(**{field_name: bad}).validate()
        for bad_threshold in (0, -5, 100.01, float("nan"), float("inf"), True):
            with self.subTest(bad_threshold=bad_threshold):
                with self.assertRaisesRegex(StreamError, "^INVALID_BUDGET$"):
                    default_alert(threshold_percent=bad_threshold).validate()
        with self.assertRaisesRegex(StreamError, "^INVALID_BUDGET$"):
            default_alert(threshold_type="Estimated").validate()
        with self.assertRaisesRegex(StreamError, "^INVALID_BUDGET$"):
            default_alert(budget_cap_usd=0).validate()
        with self.assertRaisesRegex(StreamError, "^INVALID_BUDGET$"):
            default_alert(budget_cap_gbp=None).validate()
        with self.assertRaisesRegex(StreamError, "^BUDGET_ALERT_NOT_BELOW_CAP$"):
            default_alert(budget_alert_gbp="5.00", budget_cap_gbp="5.00").validate()
        with self.assertRaisesRegex(StreamError, "^RUN_OWNER_COST_ALERT_REQUIRED$"):
            default_controls(budget_alert=None).validate()

    def test_from_controls_roundtrip_controller_preflight_status_and_tamper_detection(
        self,
    ) -> None:
        controls = default_controls()
        plan = RunPlan.from_controls(controls, homes=20, max_per_second=10.0)
        self.assertEqual(plan.max_duration_seconds, 600.0)
        self.assertEqual(plan.time_limit_minutes, 10.0)
        self.assertEqual(plan.budget_alert_gbp, "4.00")
        self.assertEqual(plan.budget_cap_gbp, "5.00")
        self.assertEqual(plan.alert_owner, "Platform Cost Owner")

        with tempfile.TemporaryDirectory() as tmp:
            estimate_path = Path(tmp) / "estimate.json"
            record(plan, estimate_path)

            tampered_path = Path(tmp) / "tampered.json"
            tampered = json.loads(estimate_path.read_text(encoding="utf-8"))
            tampered.pop("sha256")
            tampered["plan"]["alert_owner"] = "Different Owner"
            tampered["sha256"] = run_plan._digest(tampered)
            tampered_path.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaisesRegex(StreamError, "^ESTIMATE_MISMATCH$"):
                RunController(plan).start(tampered_path)

            now = [0.0]
            controller = RunController(plan, clock=lambda: now[0])
            preflight = controller.preflight()
            self.assertEqual(preflight["owner"], "Juan Manuel Servera")
            self.assertEqual(preflight["time_limit_minutes"], 10.0)
            self.assertEqual(
                preflight["budget_alert"],
                controls.budget_alert.as_dict(),
            )

            controller.start(estimate_path)
            controller.admit("4.00")
            now[0] = 30.0
            status = controller.status()
            self.assertEqual(status["state"], "running")
            self.assertEqual(status["time_limit_minutes"], 10.0)
            self.assertEqual(status["max_duration_seconds"], 600.0)
            self.assertTrue(status["alert_raised"])
            budget_alert = status["budget_alert"]
            assert isinstance(budget_alert, dict)
            self.assertEqual(budget_alert["alert_owner_reference"], "Platform Cost Owner")
            self.assertEqual(budget_alert["alert_rule_reference"], "budget-iot-hub-actual80")


class BicepRunControlsContractTests(unittest.TestCase):
    def test_live_infra_bicep_matches_actual80_and_forecast100_run_controls(self) -> None:
        actual80 = default_controls()
        verified = verify_bicep_run_controls(INFRA, actual80)
        self.assertTrue(verified.owner_tag_required)
        self.assertEqual(verified.default_owner_tag, "Juan Manuel Servera")
        self.assertTrue(verified.alert_email_param_required)
        self.assertEqual(verified.job_replica_timeout_seconds, 240)
        self.assertLessEqual(verified.job_replica_timeout_seconds, int(MAX_TIME_LIMIT_SECONDS))
        self.assertEqual(verified.job_retry_limit, 0)
        self.assertTrue(verified.job_runs_once)
        self.assertEqual(verified.job_control_file, "/certs/control.json")
        self.assertTrue(verified.hub_budget_resource_scoped)
        self.assertEqual(
            {
                (n.name, n.threshold_percent, n.threshold_type, n.enabled)
                for n in verified.notifications
            },
            {("actual80", 80, "Actual", True), ("forecast100", 100, "Forecasted", True)},
        )

        forecast100 = default_controls(
            budget_alert=default_alert(
                threshold_percent=100.0,
                threshold_type="Forecasted",
                alert_rule_reference="budget-iot-hub-forecast100",
            )
        )
        self.assertEqual(verify_bicep_run_controls(INFRA, forecast100), verified)

    def test_rejects_unaligned_runtime_threshold_without_rounding_drift(self) -> None:
        for threshold_percent, threshold_type in (
            (79.6, "Actual"),
            (80.4, "Actual"),
            (75.0, "Actual"),
            (80.0, "Forecasted"),
            (100.0, "Actual"),
        ):
            bad = default_controls(
                budget_alert=default_alert(
                    threshold_percent=threshold_percent,
                    threshold_type=threshold_type,
                )
            )
            with self.subTest(pct=threshold_percent, kind=threshold_type):
                with self.assertRaisesRegex(StreamError, "^BICEP_CONTRACT_MISMATCH$"):
                    verify_bicep_run_controls(INFRA, bad)

    def test_detects_bicep_drift_across_governance_main_iothub_and_simulator_job(self) -> None:
        mutations: tuple[tuple[str, str, str, str], ...] = (
            ("governance.bicep", "  'owner'\n", "", "missing required owner tag"),
            (
                "main.bicep",
                "param ownerTag string = 'Juan Manuel Servera'",
                "param ownerTag string = 'anonymous'",
                "anonymous default ownerTag",
            ),
            (
                "main.bicep",
                "param alertEmail string",
                "param alertEmail string = ''",
                "optional blank alertEmail",
            ),
            (
                "main.bicep",
                (
                    "  name: 'iothub'\n"
                    "  dependsOn: [guard]\n"
                    "  params: {\n"
                    "    allowPublicNetworkAccess: publicAccess\n"
                    "    name: 'iot-${prefix}-${unique}'\n"
                    "    location: location\n"
                    "    tags: allTags"
                ),
                (
                    "  name: 'iothub'\n"
                    "  dependsOn: [guard]\n"
                    "  params: {\n"
                    "    allowPublicNetworkAccess: publicAccess\n"
                    "    name: 'iot-${prefix}-${unique}'\n"
                    "    location: location\n"
                    "    tags: {}"
                ),
                "iotHub missing allTags owner propagation",
            ),
            (
                "modules/iothub.bicep",
                "      actual80: {\n        enabled: true",
                "      actual80: {\n        enabled: false",
                "disabled actual80 budget alert",
            ),
            (
                "modules/iothub.bicep",
                "name: 'ResourceId'",
                "name: 'ResourceGroupName'",
                "unscoped hub budget",
            ),
            (
                "live-simulator-job.bicep",
                "replicaTimeout: 240",
                "replicaTimeout: 7200",
                "replicaTimeout above 3600s ceiling",
            ),
            (
                "live-simulator-job.bicep",
                "replicaRetryLimit: 0",
                "replicaRetryLimit: 2",
                "nonzero unattended retry limit",
            ),
            (
                "live-simulator-job.bicep",
                "'--once', ",
                "",
                "missing --once bounded execution flag",
            ),
        )
        for rel_path, target, replacement, label in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                copy_dir = Path(tmp) / "infra"
                (copy_dir / "modules").mkdir(parents=True)
                for item in (
                    "governance.bicep",
                    "main.bicep",
                    "modules/iothub.bicep",
                    "live-simulator-job.bicep",
                ):
                    (copy_dir / item).write_text(
                        (INFRA / item).read_text(encoding="utf-8"), encoding="utf-8"
                    )
                mutated_file = copy_dir / rel_path
                original = mutated_file.read_text(encoding="utf-8")
                self.assertIn(target, original)
                mutated_file.write_text(original.replace(target, replacement, 1), encoding="utf-8")
                with self.assertRaisesRegex(StreamError, "^BICEP_CONTRACT_MISMATCH$"):
                    verify_bicep_run_controls(copy_dir, default_controls())

    def test_compiled_bicep_arm_templates_preserve_controls_when_bicep_cli_available(self) -> None:
        bicep_bin = shutil.which("bicep")
        az_bin = shutil.which("az")
        if bicep_bin is not None:
            cmd_prefix = [bicep_bin, "build"]
        elif az_bin is not None:
            cmd_prefix = [az_bin, "bicep", "build", "--file"]
        else:
            self.skipTest("Neither bicep nor az CLI is installed in this environment")

        def compile_arm(source: Path) -> dict[str, Any]:
            proc = subprocess.run(
                [*cmd_prefix, str(source), "--stdout"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if proc.returncode != 0:
                self.fail(f"Bicep compilation failed for {source.name}: {proc.stderr}")
            loaded = json.loads(proc.stdout)
            assert isinstance(loaded, dict)
            return loaded

        hub_arm = compile_arm(INFRA / "modules" / "iothub.bicep")
        job_arm = compile_arm(INFRA / "live-simulator-job.bicep")

        hub_resources = hub_arm.get("resources", {})
        if isinstance(hub_resources, dict):
            budgets = [
                res
                for res in hub_resources.values()
                if isinstance(res, dict) and res.get("type") == "Microsoft.Consumption/budgets"
            ]
        else:
            budgets = [
                res
                for res in hub_resources
                if isinstance(res, dict) and res.get("type") == "Microsoft.Consumption/budgets"
            ]
        self.assertEqual(len(budgets), 1)
        notifications = budgets[0]["properties"]["notifications"]
        self.assertEqual(notifications["actual80"]["threshold"], 80)
        self.assertEqual(notifications["actual80"]["thresholdType"], "Actual")
        self.assertEqual(notifications["forecast100"]["threshold"], 100)
        self.assertEqual(notifications["forecast100"]["thresholdType"], "Forecasted")

        job_resources = job_arm.get("resources", {})
        jobs = (
            list(job_resources.values()) if isinstance(job_resources, dict) else list(job_resources)
        )
        app_jobs = [
            res for res in jobs if isinstance(res, dict) and res.get("type") == "Microsoft.App/jobs"
        ]
        self.assertEqual(len(app_jobs), 1)
        config = app_jobs[0]["properties"]["configuration"]
        self.assertEqual(config["replicaTimeout"], 240)
        self.assertEqual(config["replicaRetryLimit"], 0)
        args = app_jobs[0]["properties"]["template"]["containers"][0]["args"]
        self.assertIn("--once", args)


if __name__ == "__main__":
    unittest.main()
