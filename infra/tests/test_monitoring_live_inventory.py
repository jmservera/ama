"""Issue #146 criterion 1: live alert inventory classifier never overstates coverage."""

from __future__ import annotations

import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "monitoring_live_inventory", REPO_ROOT / "infra/scripts/monitoring_live_inventory.py"
)
assert _SPEC is not None and _SPEC.loader is not None
inventory = importlib.util.module_from_spec(_SPEC)
sys.modules["monitoring_live_inventory"] = inventory
_SPEC.loader.exec_module(inventory)

# Names and enabled flags as observed with the Azure CLI on 2026-11-23 (resource group ama).
LIVE_METRIC = {
    "alert-cutover-test-api-5xx": True,
    "alert-job-cutover-test-demo-orch-failed": False,
    "alert-job-cutover-test-demo-load-failed": False,
    "alert-cutover-test-iot-routing-dropped": False,
    "alert-cutover-test-iot-ingress-throttle": False,
}
LIVE_QUERY = {
    "alert-cutover-test-demo-ledger-digest-mismatch": True,
    "alert-cutover-test-ledger-verify-missing": True,
    "alert-cutover-test-agent-tasks-poison": False,
    "alert-cutover-test-ai-limits": False,
}


def _rules(flags: dict[str, bool]) -> list[dict[str, object]]:
    return [{"name": n, "enabled": e} for n, e in flags.items()]


class MonitoringLiveInventoryTests(unittest.TestCase):
    def test_live_demo_shape_is_partial_and_disabled_is_not_enabled(self) -> None:
        report = inventory.classify(_rules(LIVE_METRIC) + _rules(LIVE_QUERY))
        status = {k: v["status"] for k, v in report["classes"].items()}
        self.assertEqual(
            status,
            {
                "job_failure": "disabled",
                "poison_queue": "disabled",
                "ledger_digest": "enabled",
                "iot_ingestion": "disabled",
            },
        )
        self.assertEqual(report["coverage"], "partial")
        self.assertFalse(report["all_classes_enabled"])
        self.assertFalse(report["firing_observed"])

    def test_missing_class_and_empty_inventory(self) -> None:
        report = inventory.classify(_rules({"alert-x-api-5xx": True}))
        self.assertEqual(report["coverage"], "none")
        self.assertTrue(all(c["status"] == "missing" for c in report["classes"].values()))

    def test_all_enabled_still_never_claims_firing(self) -> None:
        names = [
            "alert-job-a-failed",
            "alert-p-agent-tasks-poison",
            "alert-p-ledger-digest-mismatch",
            "alert-p-iot-routing-dropped",
        ]
        report = inventory.classify(_rules({n: True for n in names}))
        self.assertTrue(report["all_classes_enabled"])
        self.assertFalse(report["firing_observed"])

    def test_non_boolean_enabled_is_not_enabled(self) -> None:
        report = inventory.classify([{"name": "alert-job-a-failed", "enabled": "true"}])
        self.assertEqual(report["classes"]["job_failure"]["status"], "disabled")

    def test_output_carries_only_name_and_enabled(self) -> None:
        rule = {"name": "alert-job-a-failed", "enabled": True, "id": "/subscriptions/secret"}
        report = inventory.classify([rule])
        self.assertNotIn("subscriptions", json.dumps(report))

    def test_patterns_match_names_the_bicep_declares(self) -> None:
        module = (REPO_ROOT / "infra/modules/operationalMonitoring.bicep").read_text("utf-8")
        main = (REPO_ROOT / "infra/main.bicep").read_text("utf-8")
        self.assertIn("name: 'alert-${jobName}-failed'", module)
        self.assertIn("name: 'alert-${prefix}-agent-tasks-poison'", module)
        for suffix in re.findall(r"suffix: '(iot-[a-z-]+)'", module):
            self.assertRegex(f"alert-p-{suffix}", inventory.CLASSES["iot_ingestion"])
        for suffix in ("ledger-digest-mismatch", "ledger-verify-missing"):
            self.assertIn(f"name: 'alert-${{applicationPrefix}}-{suffix}'", main)
            self.assertRegex(f"alert-p-{suffix}", inventory.CLASSES["ledger_digest"])
        self.assertRegex("alert-job-x-orch-failed", inventory.CLASSES["job_failure"])
        self.assertRegex("alert-p-agent-tasks-poison", inventory.CLASSES["poison_queue"])

    def test_enabled_rule_for_one_job_does_not_cover_a_job_without_a_rule(self) -> None:
        rules = _rules({"alert-job-a-failed": True, "alert-job-b-failed": False})
        report = inventory.classify(rules, ["job-a", "job-b", "job-live-receiver"])
        job = report["classes"]["job_failure"]
        self.assertEqual(job["status"], "partial")
        self.assertEqual(job["uncovered_jobs"], ["job-b", "job-live-receiver"])
        self.assertFalse(report["all_classes_enabled"])
        covered = inventory.classify(rules[:1], ["job-a"])["classes"]["job_failure"]
        self.assertEqual(covered["status"], "enabled")
        self.assertEqual(covered["uncovered_jobs"], [])
        self.assertNotIn("uncovered_jobs", inventory.classify(rules)["classes"]["job_failure"])

    def test_cli_reports_and_rejects_bad_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            metric = Path(tmp, "m.json")
            query = Path(tmp, "q.json")
            metric.write_text(json.dumps(_rules(LIVE_METRIC)), encoding="utf-8")
            query.write_text(json.dumps(_rules(LIVE_QUERY)), encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                code = inventory.main(
                    ["--metric-alerts", str(metric), "--scheduled-queries", str(query)]
                )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue())["coverage"], "partial")
            jobs = Path(tmp, "j.json")
            jobs.write_text(json.dumps([{"name": "job-x", "id": "/subscriptions/s"}]), "utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                inventory.main(
                    [
                        "--metric-alerts",
                        str(metric),
                        "--scheduled-queries",
                        str(query),
                        "--jobs",
                        str(jobs),
                    ]
                )
            self.assertEqual(
                json.loads(out.getvalue())["classes"]["job_failure"]["uncovered_jobs"], ["job-x"]
            )
            self.assertNotIn("subscriptions", out.getvalue())
            query.write_text('{"not": "a list"}', encoding="utf-8")
            err = io.StringIO()
            with redirect_stderr(err):
                code = inventory.main(
                    ["--metric-alerts", str(metric), "--scheduled-queries", str(query)]
                )
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
