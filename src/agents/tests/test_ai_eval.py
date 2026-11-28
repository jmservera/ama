import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from zava_forward.agents import ai_eval
from zava_forward.core import ai_registry
from zava_forward.core.store import Store


class AiEvalTests(unittest.TestCase):
    def scenario(self, index):
        return copy.deepcopy(json.loads(ai_eval.GOLDEN.read_text())["scenarios"][index])

    def evaluate(self, sc):
        with tempfile.TemporaryDirectory() as tmp:
            failures, measures = ai_eval.run_scenario(sc, tmp)
        return failures, measures, ai_eval.summarise([dict(name=sc["name"], measures=measures)])

    def test_missing_golden_file_names_the_configuration_variable(self):
        with tempfile.TemporaryDirectory() as tmp:
            absent = Path(tmp) / "absent.json"
            with self.assertRaises(ai_eval.GoldenFileError) as ctx:
                ai_eval.run_eval(golden=absent)
        self.assertIn("ZF_AI_GOLDEN", str(ctx.exception))
        self.assertIn(str(absent), str(ctx.exception))
        self.assertIsInstance(ctx.exception, FileNotFoundError)

    def test_golden_run_and_scenario_denominators_reconcile(self):
        report = ai_eval.run_eval()
        summary = report["summary"]
        priority = [r["measures"] for r in report["results"] if r["measures"]]
        rows = [run for m in priority for run in m["run_results"]]
        self.assertTrue(report["passed"], report["results"])
        self.assertEqual(summary["recommendation_runs"], len(rows))
        self.assertEqual(summary["recommendation_runs"], sum(m["runs"] for m in priority))
        self.assertEqual(summary["recommendation_runs"], 14)
        self.assertEqual(summary["ai_runs"], sum(r["source"] == "ai" for r in rows))
        self.assertEqual(summary["template_runs"], sum(r["source"] == "template" for r in rows))
        self.assertEqual((summary["ai_runs"], summary["template_runs"]), (8, 6))
        self.assertEqual(summary["priority_scenarios"], len(priority))
        self.assertEqual((summary["priority_scenarios"], report["scenarios"]), (10, 11))
        self.assertEqual((summary["ai_scenarios"], summary["template_scenarios"]), (4, 6))
        self.assertEqual(summary["latency_ms"]["runs"], len(rows))
        self.assertEqual(sum(summary["reviewer"]["counts"].values()), len(priority))

    def test_five_output_scenario_retains_each_returned_identity_and_latency(self):
        sc = self.scenario(-2)
        real, returned = Store.ai_priority, []

        def identified(store, user, n=5, mode=None):
            rec = real(store, user, n, mode)
            if mode != "workflow":
                i = len(returned) + 1
                rec.update(
                    model=f"returned-model-{i}",
                    prompt_version=f"returned-prompt-{i}",
                    latency_ms=i * 11.5,
                )
                returned.append(copy.deepcopy(rec))
            return rec

        with mock.patch.object(Store, "ai_priority", identified):
            failures, measures, summary = self.evaluate(sc)
        self.assertEqual(failures, [])
        rows = measures["run_results"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(len({r["recommendation_id"] for r in rows}), 5)
        for i, (row, rec) in enumerate(zip(rows, returned), 1):
            self.assertEqual(row["run"], i)
            self.assertEqual(row["recommendation_id"], rec["id"])
            for key in ("source", "model", "prompt_version"):
                self.assertEqual(row[key], rec[key])
            self.assertEqual(row["model_latency_ms"], rec["latency_ms"])
            self.assertEqual(row["latency_ms"], measures["latency_ms"][i - 1])
        self.assertEqual(measures["model_latency_ms"], [r["model_latency_ms"] for r in rows])
        self.assertEqual(summary["models"], sorted(r["model"] for r in returned))
        self.assertEqual(summary["prompt_versions"], sorted(r["prompt_version"] for r in returned))
        self.assertEqual((summary["recommendation_runs"], summary["ai_runs"]), (5, 5))
        self.assertEqual(summary["priority_scenarios"], 1)
        self.assertEqual(summary["reviewer"]["counts"], dict(accept=0, edit=1, reject=0))
        self.assertEqual(measures["review"]["reviewer"], ai_eval.OWNER["email"])
        self.assertEqual(measures["review"]["recommendation_id"], returned[-1]["id"])
        self.assertEqual(measures["review"]["reason"], sc["answer"]["reason"])

    def test_mixed_ai_and_fallback_runs_are_counted_in_both_orders(self):
        real = Store.ai_priority
        for ai_first in (True, False):
            with self.subTest(ai_first=ai_first):
                sc = self.scenario(1)
                valid = sc.pop("model_output")
                sc["model_outputs"] = (
                    [valid, "invalid JSON"] if ai_first else ["invalid JSON", valid]
                )
                sc["expect"] = {}
                returned = []

                def identified(store, user, n=5, mode=None):
                    rec = real(store, user, n, mode)
                    if mode != "workflow":
                        rec["model"] = "actual-returned-label" if rec["source"] == "ai" else None
                        rec["prompt_version"] = f"returned-prompt-{len(returned) + 1}"
                        returned.append(copy.deepcopy(rec))
                    return rec

                with mock.patch.object(Store, "ai_priority", identified):
                    failures, measures, summary = self.evaluate(sc)
                self.assertEqual(failures, [])
                rows = measures["run_results"]
                self.assertEqual([r["source"] for r in rows], [r["source"] for r in returned])
                self.assertEqual([r["model"] for r in rows], [r["model"] for r in returned])
                self.assertEqual(
                    (summary["recommendation_runs"], summary["ai_runs"], summary["template_runs"]),
                    (2, 1, 1),
                )
                self.assertEqual(
                    (
                        summary["priority_scenarios"],
                        summary["ai_scenarios"],
                        summary["template_scenarios"],
                    ),
                    (1, 1, 1),
                )
                self.assertEqual(summary["models"], ["actual-returned-label"])
                self.assertEqual(
                    summary["prompt_versions"], ["returned-prompt-1", "returned-prompt-2"]
                )
                self.assertEqual(measures["source"], returned[-1]["source"])
                self.assertEqual(summary["added_value"]["scenarios"], 0 if ai_first else 1)
                self.assertEqual(sum(summary["reviewer"]["counts"].values()), 1)
                self.assertEqual(measures["review"]["recommendation_id"], returned[-1]["id"])

    def test_template_only_repetitions_keep_unknown_model_and_single_review(self):
        sc = self.scenario(0)
        sc["runs"] = 3
        failures, measures, summary = self.evaluate(sc)
        self.assertEqual(failures, [])
        self.assertEqual([r["source"] for r in measures["run_results"]], ["template"] * 3)
        self.assertEqual([r["model"] for r in measures["run_results"]], [None] * 3)
        self.assertEqual(
            (summary["recommendation_runs"], summary["ai_runs"], summary["template_runs"]),
            (3, 0, 3),
        )
        self.assertEqual(
            (summary["priority_scenarios"], summary["ai_scenarios"], summary["template_scenarios"]),
            (1, 0, 1),
        )
        self.assertEqual(summary["models"], [])
        self.assertEqual(summary["latency_ms"]["runs"], 3)
        self.assertEqual(sum(summary["reviewer"]["counts"].values()), 1)

    def test_repetition_preserves_final_only_quality_scope(self):
        sc = self.scenario(-2)
        failures, measures, summary = self.evaluate(sc)
        single = copy.deepcopy(sc)
        single["model_outputs"] = [sc["model_outputs"][-1]]
        single_failures, last, last_summary = self.evaluate(single)
        self.assertEqual((failures, single_failures), ([], []))
        for key in ("overlap", "spearman", "recall"):
            self.assertEqual(measures[key], last[key])
        for key in ("mean_overlap", "mean_spearman", "added_value"):
            self.assertEqual(summary[key], last_summary[key])
        self.assertIn("final recommendation", summary["quality_scope"])
        self.assertEqual(summary["critical_misses"], 0)
        self.assertEqual(summary["citation_validity"], 1.0)

    def test_early_critical_miss_still_fails_after_valid_repetition(self):
        sc = self.scenario(1)
        valid = sc.pop("model_output")
        sc["model_outputs"] = [
            json.dumps([dict(case_id="G-1", reason="Short wait", cites=["Days in stage: 5"])]),
            valid,
        ]
        sc["expect"] = {}
        with mock.patch.object(ai_eval.ai_tasks, "critical_misses", return_value=[]):
            failures, measures, summary = self.evaluate(sc)
        self.assertTrue(any("critical miss" in f for f in failures))
        self.assertEqual(summary["critical_misses"], 1)
        self.assertEqual((measures["runs"], summary["ai_runs"]), (2, 2))
        self.assertEqual(measures["source"], "ai")

    def test_early_bad_citation_still_fails_after_valid_repetition(self):
        sc = self.scenario(1)
        valid = sc.pop("model_output")
        sc["model_outputs"] = [
            json.dumps(
                [dict(case_id="G-3", reason="Unsupported stage", cites=["Stage: Survey booked"])]
            ),
            valid,
        ]
        sc["expect"] = {}
        with mock.patch.object(ai_eval.ai_tasks, "resolve", return_value=True):
            failures, measures, summary = self.evaluate(sc)
        self.assertTrue(any("citation does not exist" in f for f in failures))
        self.assertLess(summary["citation_validity"], 1.0)
        self.assertEqual((measures["runs"], summary["ai_runs"]), (2, 2))

    def test_golden_scenarios_pass(self):
        rep = ai_eval.run_eval()
        self.assertGreaterEqual(rep["scenarios"], 5)
        self.assertTrue(rep["passed"], rep["results"])

    def test_harness_catches_an_ai_that_changes_ranking_or_cases(self):
        real = Store.ai_priority

        def bad(self, user, n=5):
            rec = real(self, user, n)
            top = self.cases[rec["items"][0]["case_id"]]
            top["days_in_stage"] = 1000
            self.version += 1
            return rec

        with mock.patch.object(Store, "ai_priority", bad):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        text = " ".join(f for r in rep["results"] for f in r["failures"])
        self.assertIn("ranking changed", text)
        self.assertIn("case data changed", text)

    def test_harness_catches_an_ai_that_acts_without_approval(self):
        real = Store.ai_priority

        def auto(self, user, n=5):
            rec = real(self, user, n)
            self.resolve_priority(user, rec["id"], "accept")
            return rec

        with mock.patch.object(Store, "ai_priority", auto):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertIn("Proposed", " ".join(f for r in rep["results"] for f in r["failures"]))

    def test_harness_catches_a_model_answer_that_is_not_checked(self):
        with mock.patch(
            "zava_forward.core.ai.Ai.run",
            lambda self, task, s, u, t, strong=False, check=None: dict(
                text='[{"case_id": "G-999", "reason": "x"}]',
                source="ai",
                model="m",
                validated=True,
                task=task,
            ),
        ):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])

    def test_evidence_gate_refuses_benefit_and_records_open_items(self):
        rep = ai_eval.run_eval()
        ev = rep["evidence"]
        self.assertEqual(len(ev["golden_sha256"]), 64)
        self.assertTrue(ev["benefit_claim"].startswith("not permitted"))
        self.assertTrue(ev["actual_model_evaluation"].startswith("not evaluated"))
        self.assertTrue(ev["calibration"].startswith("not applicable"))
        self.assertTrue(any("quota" in o for o in ev["open_items"]))
        self.assertTrue(
            rep["prompt_version"] and "latency_ms" in rep["summary"] and rep["summary"]["reviewer"]
        )

    def test_region_confirmation_never_infers_quota_headroom(self):
        dep = dict(
            name="d",
            model="gpt-4.1-nano",
            version="2025-04-14",
            sku="Standard",
            capacity=10,
            rate_limits=dict(requests_per_minute=10, tokens_per_minute=10000),
            state="Succeeded",
        )
        record = dict(
            region="uksouth",
            account="a",
            retrieved_on="2026-11-19",
            source="az",
            deployments=[dep],
            quota_headroom=dict(status="unavailable"),
        )
        self.assertEqual(ai_eval.region_confirmation(None)["status"], "none")
        part = ai_eval.region_confirmation(record)
        self.assertEqual((part["status"], part["missing"]), ("partial", ["quota headroom"]))
        record["quota_headroom"] = dict(status="confirmed")
        self.assertEqual(ai_eval.region_confirmation(record)["status"], "confirmed")
        record["deployments"] = [dict(dep, version=None, state="Creating")]
        bad = ai_eval.region_confirmation(record)
        self.assertEqual(bad["status"], "incomplete")
        self.assertIn("version", bad["missing"][0])

    def test_serving_region_record_matches_infra_model_pins(self):
        import re

        root = Path(__file__).resolve().parents[3]
        record = json.loads((root / "src/agents/evals/serving_region_record.json").read_text())
        recorded = {(d["model"], d["version"]) for d in record["deployments"]}

        def pin(path, name_param, version_param):
            text = (root / path).read_text()
            return tuple(
                re.search(rf"param {p} string = '([^']+)'", text).group(1)
                for p in (name_param, version_param)
            )

        for pair in (
            pin("infra/main.bicep", "chatModelName", "chatModelVersion"),
            pin("infra/resident-assistant.bicep", "modelName", "modelVersion"),
        ):
            self.assertIn(pair, recorded)

    def test_resident_deployment_names_match_serving_record(self):
        import re

        root = Path(__file__).resolve().parents[3]
        record = json.loads((root / "src/agents/evals/serving_region_record.json").read_text())
        names = {d["name"] for d in record["deployments"]}
        code = (root / "src/api/src/zava_forward/api/resident_demo/aoai.py").read_text()
        bicep = (root / "infra/resident-assistant.bicep").read_text()
        in_code = re.search(r'^DEPLOYMENT = "([^"]+)"', code, re.M).group(1)
        in_bicep = re.search(
            r"resource model '[^']+' = if \(active\) \{\s+parent: account\s+name: '([^']+)'", bicep
        ).group(1)
        self.assertEqual(in_code, in_bicep)
        self.assertIn(in_code, names)

    def test_run_eval_loads_the_record_named_by_the_environment(self):
        record_path = Path(__file__).resolve().parents[1] / "evals" / "serving_region_record.json"
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("[1]")
            cases = {record_path: "confirmed", bad: "none", Path(tmp) / "absent.json": "none"}
            for path, status in cases.items():
                with mock.patch.dict("os.environ", {ai_eval.SERVING_REGION_ENV: str(path)}):
                    self.assertEqual(
                        ai_eval.run_eval()["evidence"]["serving_region"]["status"], status
                    )
        with mock.patch.dict("os.environ", {}, clear=False) as env:
            env.pop(ai_eval.SERVING_REGION_ENV, None)
            self.assertEqual(ai_eval.run_eval()["evidence"]["serving_region"]["status"], "none")

    def test_recorded_rate_limits_follow_capacity(self):
        record = json.loads(
            (
                Path(__file__).resolve().parents[3] / "src/agents/evals/serving_region_record.json"
            ).read_text()
        )
        for d in record["deployments"]:
            self.assertEqual(d["rate_limits"]["requests_per_minute"], d["capacity"], d["name"])
            self.assertEqual(d["rate_limits"]["tokens_per_minute"], d["capacity"] * 1000, d["name"])

    def test_quota_rows_agree_with_their_deployment_sku_and_model(self):
        record = json.loads(
            (
                Path(__file__).resolve().parents[3] / "src/agents/evals/serving_region_record.json"
            ).read_text()
        )
        deployments = {d["name"]: d for d in record["deployments"]}
        for row in record["quota_headroom"]["rows"]:
            dep = deployments[row["deployment"]]
            expected = f"OpenAI.{dep['sku']}.{dep['model'].replace('gpt-', 'gpt')}"
            self.assertEqual(row["name"], expected, row["deployment"])

    def test_gate_keeps_region_open_item_until_headroom_is_confirmed(self):
        record = json.loads(
            (
                Path(__file__).resolve().parents[3] / "src/agents/evals/serving_region_record.json"
            ).read_text()
        )
        ev = ai_eval.run_eval(serving_region=record)["evidence"]
        self.assertEqual(ev["serving_region"]["status"], "confirmed")
        self.assertFalse(any("names, versions and quotas" in o for o in ev["open_items"]))
        names = {r["deployment"] for r in record["quota_headroom"]["rows"]}
        self.assertEqual(names, {d["name"] for d in record["deployments"]})
        capacity = {d["name"]: d["capacity"] for d in record["deployments"]}
        for row in record["quota_headroom"]["rows"]:
            self.assertEqual(row["current"], capacity[row["deployment"]], row["name"])
            self.assertLess(row["current"], row["limit"], row["name"])
        record["quota_headroom"] = dict(status="unavailable")
        ev = ai_eval.run_eval(serving_region=record)["evidence"]
        self.assertEqual(ev["serving_region"]["status"], "partial")
        self.assertIn("missing: quota headroom", ev["open_items"][0])
        self.assertEqual(ai_eval.run_eval()["evidence"]["serving_region"]["status"], "none")

    def test_report_carries_per_cohort_record_that_stays_blocked_and_synthetic(self):
        co = ai_eval.run_eval()["cohorts"]
        self.assertEqual((co["status"], co["activation_allowed"]), ("blocked", False))
        self.assertEqual(co["owner_approval_status"], "unapproved")
        self.assertFalse(co["lawful_analysis_fields_approved"])
        self.assertFalse(co["live_activation_allowed"])
        self.assertTrue(co["synthetic"] and not co["fairness_evidence"])
        self.assertTrue(co["synthetic_not_fairness_evidence"])
        self.assertIn("OQ-018", co["non_fairness_provenance_notice"])
        self.assertIn("unapproved_thresholds", co["blockers"])
        self.assertEqual(
            set(co["dimensions"]),
            {"sensor_completeness", "support_need", "source_completeness", "appointment_history"},
        )
        for labels in co["dimensions"].values():
            self.assertEqual(sum(row["n"] for row in labels.values()), co["total_cases"])
        self.assertTrue(co["ai_task_cohorts"].startswith("not evaluated"))
        exp = ai_eval.cohort_evaluation_export()
        self.assertEqual(exp["owner_approval_status"], "unapproved")
        self.assertFalse(exp["lawful_analysis_fields_approved"])
        self.assertFalse(exp["live_activation_allowed"])
        self.assertTrue(exp["synthetic_not_fairness_evidence"])
        self.assertIn("OQ-018", exp["non_fairness_provenance_notice"])
        self.assertEqual(exp["ranking"]["record_hash"], co["record_hash"])
        self.assertEqual(exp["ai_priority"]["task_id"], "ai-priority-recommendation")
        self.assertEqual(exp["ai_priority"]["owner_approval_status"], "unapproved")
        self.assertFalse(exp["ai_priority"]["lawful_analysis_fields_approved"])
        self.assertTrue(exp["ai_priority"]["synthetic_not_fairness_evidence"])

    def test_a_critical_miss_fails_the_run(self):
        real = ai_eval.summarise

        def missed(results):
            s = real(results)
            s["critical_misses"] = 1
            return s

        with mock.patch.object(ai_eval, "summarise", missed):
            self.assertFalse(ai_eval.run_eval()["passed"])


RETAINED = {"briefing", "message", "summary", "priority", "funding_draft", "read_document"}


def _failures(rep, word):
    return [f for r in rep["results"] for f in r["failures"] if word in f]


class TaskCoverageTests(unittest.TestCase):
    def test_coverage_is_registry_derived_and_states_what_is_not_evaluated(self):
        rep = ai_eval.run_eval()
        cov = rep["evidence"]["task_coverage"]
        self.assertTrue(rep["passed"], rep["results"])
        self.assertEqual(set(cov["tasks"]), set(ai_registry.tasks()))
        for task_id, row in cov["tasks"].items():
            want = ai_eval.EXERCISED if task_id in RETAINED else ai_eval.NOT_EVALUATED
            self.assertEqual(row["status"], want, task_id)
        for assistant in (
            "stock-prioritisation",
            "assessment-preparation",
            "funding-evidence",
            "works-resident-coordination",
            "quality-evidence",
        ):
            self.assertEqual(cov["tasks"][assistant]["status"], ai_eval.NOT_EVALUATED)
        self.assertEqual(cov["namespace_errors"], [])
        self.assertIn("not held-out semantic accuracy", cov["note"])

    def test_a_template_fallback_is_not_coverage(self):
        def template(self, name, data, mime, off=False):
            return dict(
                text="The file is stored.",
                source="template",
                model=None,
                validated=True,
                task="read_document",
            )

        with mock.patch("zava_forward.core.ai.Ai.look_at", template):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertEqual(
            rep["evidence"]["task_coverage"]["tasks"]["read_document"]["status"],
            ai_eval.FALLBACK_ONLY,
        )

    def test_a_late_quarantined_result_is_not_coverage(self):
        real = Store.continuity_publish
        with mock.patch.object(
            Store,
            "continuity_publish",
            lambda self, task, epoch, source, publish: (
                publish(True)
                if task == "funding_draft"
                else real(self, task, epoch, source, publish)
            ),
        ):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertEqual(
            rep["evidence"]["task_coverage"]["tasks"]["funding_draft"]["status"],
            ai_eval.FALLBACK_ONLY,
        )

    def test_a_retained_task_that_is_never_exercised_fails_the_run(self):
        with mock.patch.object(ai_eval, "run_document_checks", lambda workdir, observed=None: []):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertEqual(
            rep["evidence"]["task_coverage"]["tasks"]["read_document"]["status"],
            ai_eval.NOT_EVALUATED,
        )
        self.assertIn("read_document", " ".join(rep["evidence"]["task_coverage"]["failures"]))

    def test_assistant_or_prefixed_names_seen_by_the_spy_are_namespace_errors(self):
        seen = [
            dict(kind="dispatch", task=name, via="run", source="ai", model_called=True)
            for name in ("stock-prioritisation", "legacy:funding_draft")
        ]
        cov = ai_eval.task_coverage(seen)
        self.assertEqual(
            sorted(cov["namespace_errors"]), ["legacy:funding_draft", "stock-prioritisation"]
        )
        self.assertEqual(cov["tasks"]["stock-prioritisation"]["status"], ai_eval.NOT_EVALUATED)
        self.assertEqual(cov["tasks"]["funding_draft"]["status"], ai_eval.NOT_EVALUATED)

    def test_funding_draft_and_document_checks_discriminate(self):
        with mock.patch.object(ai_eval.ai_tasks, "workflow_only", lambda mode: False):
            rep = ai_eval.run_eval()
        self.assertTrue(_failures(rep, "funding draft"))
        self.assertTrue(_failures(rep, "document"))
        with mock.patch.object(ai_eval.ai_tasks, "resolve", lambda label, sources: True):
            rep = ai_eval.run_eval()
        self.assertTrue(_failures(rep, "funding draft"))
        with mock.patch.object(ai_eval.ai_tasks, "resolve", lambda label, sources: False):
            rep = ai_eval.run_eval()
        self.assertTrue(_failures(rep, "document"))


AUDIT = (
    Path(__file__).resolve().parents[3]
    / "docs/reference/research/evaluation/issue-108-closure-audit.md"
)


class ClosureAuditDocTests(unittest.TestCase):
    def test_audit_names_every_task_the_harness_does_not_evaluate(self):
        text = AUDIT.read_text()
        cov = ai_eval.run_eval()["evidence"]["task_coverage"]["tasks"]
        missing = [
            t for t, row in cov.items() if row["status"] == ai_eval.NOT_EVALUATED and t not in text
        ]
        self.assertEqual(missing, [])
        for phrase in ("eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4", "not on main", "Refs #108"):
            self.assertIn(phrase, text)
