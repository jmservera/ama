import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from zava_forward.agents import review_effectiveness as re_


class ReviewEffectivenessTests(unittest.TestCase):
    report = re_.run_review_test()

    def test_overall_passes_and_all_checks_hold(self) -> None:
        self.assertTrue(self.report["passed"], self.report["checks"])

    def test_competent_panel_detects_every_defect_class_and_keeps_controls(self) -> None:
        p = self.report["panels"]["competent"]
        self.assertEqual((p["detected"], p["defects"], p["false_rejects"]), (4, 4, 0))
        self.assertEqual(
            {r["defect"] for r in p["rows"] if r["defect"]},
            {"wrong", "stale", "unsupported", "incomplete"},
        )
        self.assertTrue(p["gate_passed"])

    def test_default_acceptance_and_citation_validity_cannot_pass(self) -> None:
        for name in ("default_accept", "automation_bias"):
            p = self.report["panels"][name]
            self.assertFalse(p["gate_passed"], name)
            defects = [r for r in p["rows"] if r["defect"]]
            self.assertTrue(all(r["citation_valid"] for r in defects))
            self.assertTrue(all(not r["gate_satisfied"] for r in defects))

    def test_reviewer_source_and_reason_are_retained(self) -> None:
        for r in self.report["panels"]["competent"]["rows"]:
            self.assertEqual(r["reviewer"], "owner@eval.example")
            self.assertTrue(isinstance(r["source_hashes"], dict) and r["source_hashes"])
            self.assertTrue(r["source_case"])
            if r["defect"]:
                self.assertIn(re_.SOURCE_TAG, r["reason"])

    def test_effort_is_reported_against_workflow_only_on_same_case(self) -> None:
        self.assertGreater(self.report["panels"]["competent"]["effort_units"], 0)
        wf = self.report["workflow_only"]
        self.assertEqual((wf["mode"], wf["seeded_defects"]), ("workflow-only", 0))
        self.assertEqual(wf["reviews"], self.report["panels"]["competent"]["reviews"])
        self.assertIn("not measured reviewer time", self.report["effort_note"])

    def test_edits_keep_supported_claims_and_required_topics(self) -> None:
        rows = {r["proposal"]: r for r in self.report["panels"]["competent"]["rows"]}
        for pid in ("D-WRONG", "D-STALE"):
            self.assertIn("Open safety issues is 1", rows[pid]["replacement"])
            self.assertTrue(rows[pid]["defect_corrected"])

    def test_ineffective_edits_do_not_correct_or_satisfy_gate(self) -> None:
        prop = json.loads(re_.GOLDEN.read_text())["proposals"][2]
        facts = {"Days in stage": "12", "Open safety issues": "1"}
        required = ["Open safety issues"]
        reason = f"mismatch {re_.SOURCE_TAG}Days in stage: 12]"
        labels = ["Days in stage: 12"]
        for text in (
            None,
            "",
            "Days in stage is 3; Open safety issues is 1",
            "Days in stage is 12",
        ):
            rec = dict(
                review_evidence=dict(reviewer="a@b"),
                status="Edited",
                reviewer_action="edit",
                reviewer_reason=reason,
                override_text=text,
            )
            self.assertFalse(re_.replacement_effective(prop, rec, facts, required), text)
            self.assertFalse(re_.gate_satisfied(prop, rec, labels, facts, required)[0], text)
        good = dict(rec, override_text="Days in stage is 12; Open safety issues is 1")
        self.assertTrue(re_.gate_satisfied(prop, good, labels, facts, required)[0])

    def test_prefix_collisions_and_edited_controls_fail(self) -> None:
        props = {p["id"]: p for p in json.loads(re_.GOLDEN.read_text())["proposals"]}
        facts = {"Days in stage": "12", "Open safety issues": "1", "Owner": "Eval Owner"}
        base = dict(review_evidence=dict(reviewer="a@b"), status="Edited", reviewer_action="edit")
        wrong = dict(base, reviewer_reason=f"x {re_.SOURCE_TAG}Days in stage: 12]")
        wrong["override_text"] = "Days in stage is 120; Open safety issues is 10"
        req = ["Open safety issues"]
        self.assertFalse(re_.replacement_effective(props["D-WRONG"], wrong, facts, req))
        self.assertFalse(
            re_.gate_satisfied(props["D-WRONG"], wrong, ["Days in stage: 12"], facts, req)[0]
        )
        ctl = dict(
            base,
            reviewer_reason="",
            override_text="Owner is Eval Previous; Open safety issues is 0",
        )
        self.assertFalse(re_.gate_satisfied(props["C-2"], ctl, [], facts, req)[0])
        ok = dict(ctl, override_text="Owner is Eval Owner; Open safety issues is 1")
        self.assertTrue(re_.gate_satisfied(props["C-2"], ok, [], facts, req)[0])

    def test_non_ai_output_fails_seeded_run(self) -> None:
        import os
        import tempfile
        from unittest import mock

        spec = re_.load_spec()
        with mock.patch.dict(os.environ, {"ZF_AI": "off"}), tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                re_.run_panel("competent", re_.competent, spec, tmp)

    def test_repeated_labels_keep_first_value_and_detail(self) -> None:
        facts = re_._facts(["Extra support: needed", "Extra support: Large print"])
        self.assertEqual(facts["Extra support"], "needed")
        self.assertEqual(facts["Extra support detail"], "Large print")

    def test_unsourced_rejection_of_defect_is_not_credited(self) -> None:
        spec = re_.load_spec()

        def sloppy(prop, facts, rec, required):  # type: ignore[no-untyped-def]
            return (
                ("reject", "Rejected for formatting only", None, 1)
                if prop["defect"]
                else ("accept", "", None, 1)
            )

        with mock.patch.dict(os.environ, {"ZF_AI": "on"}), tempfile.TemporaryDirectory() as tmp:
            r = re_.run_panel("sloppy", sloppy, spec, tmp)
        self.assertEqual(r["detected"], 0)
        self.assertEqual(r["uncorrected_defects"], r["defects"])

    def test_unrelated_resolving_citation_does_not_credit_rejection(self) -> None:
        spec = re_.load_spec()

        def sloppy(prop, facts, rec, required):  # type: ignore[no-untyped-def]
            if prop["defect"]:
                return "reject", "Rejected for formatting only [source: Owner: Eval Owner]", None, 1
            return "accept", "", None, 1

        with mock.patch.dict(os.environ, {"ZF_AI": "on"}), tempfile.TemporaryDirectory() as tmp:
            r = re_.run_panel("sloppy", sloppy, spec, tmp)
        wrong = next(x for x in r["rows"] if x["proposal"] == "D-WRONG")
        self.assertFalse(wrong["defect_corrected"])
        self.assertFalse(wrong["gate_satisfied"])

    def test_aliased_topic_correction_cites_original_label_and_passes_gate(self) -> None:
        labels = ["Extra support: needed", "Extra support: Large print"]
        facts = re_._facts(labels)
        prop = dict(
            defect="wrong",
            claims=[
                dict(
                    topic="Extra support detail",
                    cite="Extra support: Large print",
                    asserted="Braille",
                )
            ],
        )
        found = re_._findings(prop, facts, [])
        self.assertEqual(
            found, [("mismatch", "Extra support detail", "Extra support: Large print")]
        )
        reason = f"mismatch: Extra support detail differs {re_.SOURCE_TAG}{found[0][2]}]"
        rec = dict(
            review_evidence=dict(reviewer="a@b"),
            status="Edited",
            reviewer_action="edit",
            reviewer_reason=reason,
            override_text="Extra support detail is Large print",
        )
        self.assertTrue(re_.gate_satisfied(prop, rec, labels, facts, [])[0])

    def test_gate_refuses_accepted_defect_and_unresolvable_source(self) -> None:
        labels = ["Owner: Eval Owner"]
        defect = dict(defect="wrong")
        base = dict(review_evidence=dict(reviewer="a@b"), status="Edited")
        accepted = dict(base, reviewer_action="accept", reviewer_reason="")
        self.assertFalse(re_.gate_satisfied(defect, accepted, labels)[0])
        no_source = dict(base, reviewer_action="edit", reviewer_reason="looks off")
        self.assertFalse(re_.gate_satisfied(defect, no_source, labels)[0])
        fake = dict(base, reviewer_action="edit", reviewer_reason="x [source: Nope: 1]")
        self.assertFalse(re_.gate_satisfied(defect, fake, labels)[0])
        self.assertFalse(re_.gate_satisfied(defect, dict(status="Not reviewed"), labels)[0])

    def test_claims_match_the_proposal_text_and_report_is_json(self) -> None:
        for prop in json.loads(re_.GOLDEN.read_text())["proposals"]:
            for c in prop["claims"]:
                self.assertIn(c["cite"], prop["output"])
        self.assertEqual(self.report["evidence"]["provider"], "scripted")
        json.dumps(self.report)


class ReviewerAuthorityTests(unittest.TestCase):
    report = re_.run_review_test()

    def test_authority_and_required_evidence_are_defined_and_provisional(self) -> None:
        a = self.report["evidence"]["reviewer_authority"]
        self.assertIn("OQ-017", a["status"])
        self.assertEqual(a["authorised_reviewers"], ["owner@eval.example"])
        self.assertIn("source_hashes", a["required_evidence"])

    def test_competent_answers_from_an_unauthorised_reviewer_do_not_pass(self) -> None:
        u = self.report["unauthorised_reviewer_control"]
        self.assertFalse(u["gate_passed"])
        self.assertTrue(all(not r["gate_satisfied"] for r in u["rows"]))
        self.assertTrue(all("no defined authority" in r["gate_note"] for r in u["rows"]), u["rows"])
        self.assertTrue(self.report["checks"]["unauthorised_reviewer_cannot_pass"])

    def test_gate_requires_source_version_evidence_when_authority_is_defined(self) -> None:
        authority = {
            "task": "summary",
            "authorised_reviewers": ["owner@eval.example"],
            "required_evidence": ["reviewer", "source_hashes"],
        }
        rec = {
            "task": "summary",
            "status": "Reviewed",
            "reviewer_action": "accept",
            "reviewer_reason": "",
            "review_evidence": {"reviewer": "owner@eval.example", "source_hashes": {}},
        }
        ok, why = re_.gate_satisfied({"defect": None}, rec, [], None, None, authority)
        self.assertFalse(ok)
        self.assertIn("source version", why)

    def test_gate_rejects_mismatched_or_missing_task_scope(self) -> None:
        rec = {
            "task": "summary",
            "status": "Reviewed",
            "reviewer_action": "accept",
            "reviewer_reason": "",
            "review_evidence": {"reviewer": "owner@eval.example", "source_hashes": {"a": "1"}},
        }
        base = {"authorised_reviewers": ["owner@eval.example"], "required_evidence": ["reviewer"]}
        scoped = dict(base, task="summary")
        ok, _ = re_.gate_satisfied({"defect": None}, rec, [], None, None, scoped)
        self.assertTrue(ok)
        for authority in (dict(base, task="funding_draft"), dict(base)):
            ok, why = re_.gate_satisfied({"defect": None}, rec, [], None, None, authority)
            self.assertFalse(ok)
            self.assertIn("task", why)

    def test_gate_rejects_unmet_required_source_reason_for_defect(self) -> None:
        rec = {
            "task": "summary",
            "status": "Reviewed",
            "reviewer_action": "reject",
            "reviewer_reason": "looks wrong",
            "review_evidence": {"reviewer": "owner@eval.example", "source_hashes": {"a": "1"}},
        }
        authority = {
            "task": "summary",
            "authorised_reviewers": ["owner@eval.example"],
            "required_evidence": ["source_reason"],
        }
        ok, why = re_.gate_satisfied({"defect": "wrong"}, rec, [], None, None, authority)
        self.assertFalse(ok)
        self.assertIn("source_reason", why)


class HumanSessionTests(unittest.TestCase):
    def _sheet(self, kind: str, seconds: int = 30) -> dict[str, Any]:
        rows = re_.run_review_test()["panels"][kind]["rows"]
        return {
            "version": re_.load_spec()["version"],
            "reviewer_code": "EV-01",
            "workflow_seconds": 60,
            "answers": {
                r["proposal"]: {
                    "action": r["action"],
                    "reason": r["reason"],
                    "replacement": r["replacement"],
                    "seconds": seconds,
                }
                for r in rows
            },
        }

    def test_worksheet_hides_defect_hints_and_is_blank(self) -> None:
        sheet = re_.worksheet()
        self.assertEqual(len(sheet["answers"]), len(re_.load_spec()["proposals"]))
        text = str(sheet)
        self.assertNotIn("defect", text.replace("defects", ""))
        self.assertTrue(all(a["action"] == "" for a in sheet["answers"].values()))

    def test_competent_human_answers_pass_with_measured_time(self) -> None:
        res = re_.score_human_session(self._sheet("competent"))
        self.assertTrue(res["gate_passed"])
        self.assertEqual(res["measured_seconds"], 30 * len(res["panel"]["rows"]))
        self.assertEqual(res["workflow_only_seconds"], 60)
        self.assertEqual(res["panel"]["detected"], res["panel"]["defects"])

    def test_default_acceptance_by_a_person_fails_the_gate(self) -> None:
        res = re_.score_human_session(self._sheet("default_accept", 3))
        self.assertFalse(res["gate_passed"])
        self.assertLess(res["panel"]["detected"], res["panel"]["defects"])

    def test_session_reports_classes_automation_bias_and_effort_comparison(self) -> None:
        good = re_.score_human_session(self._sheet("competent"))
        self.assertEqual(
            {k: v["detected"] == v["seeded"] for k, v in good["by_defect_class"].items()},
            dict(wrong=True, stale=True, unsupported=True, incomplete=True),
        )
        self.assertEqual(good["automation_bias"]["confident_cited_defects_accepted"], [])
        eff = good["effort_comparison"]
        self.assertEqual(eff["difference_seconds"], eff["human_review_seconds"] - 60)
        self.assertEqual(eff["same_scenario_reviews"], len(good["panel"]["rows"]))
        bad = re_.score_human_session(self._sheet("automation_bias", 5))
        self.assertTrue(bad["automation_bias"]["confident_cited_defects_accepted"])
        self.assertFalse(bad["gate_passed"])
        sheet = self._sheet("competent")
        sheet["workflow_seconds"] = None
        self.assertIsNone(re_.score_human_session(sheet)["effort_comparison"]["difference_seconds"])

    def test_malformed_sheets_raise_value_error_not_a_traceback(self) -> None:
        with self.assertRaises(ValueError):
            re_.score_human_session([])  # type: ignore[arg-type]
        sheet = self._sheet("competent")
        sheet["answers"] = []
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)
        sheet = self._sheet("competent")
        sheet["answers"][next(iter(sheet["answers"]))] = "accept"
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)
        sheet = self._sheet("competent")
        sheet["answers"][next(iter(sheet["answers"]))]["seconds"] = float("inf")
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)

    def test_incomplete_or_unmeasured_sheets_are_refused(self) -> None:
        sheet = self._sheet("competent")
        first = next(iter(sheet["answers"]))
        sheet["answers"][first]["seconds"] = None
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)
        sheet = self._sheet("competent")
        sheet["answers"][first]["action"] = ""
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)
        sheet = self._sheet("competent")
        sheet["reviewer_code"] = "nobody"
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)

    def test_stale_or_foreign_sheets_are_refused(self) -> None:
        sheet = self._sheet("competent")
        sheet["version"] = "2000-01-01"
        with self.assertRaisesRegex(ValueError, "fresh worksheet"):
            re_.score_human_session(sheet)
        del sheet["version"]
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)
        sheet = self._sheet("competent")
        sheet["answers"]["not-a-proposal"] = dict(action="accept", seconds=1)
        with self.assertRaisesRegex(ValueError, "outside the scenario"):
            re_.score_human_session(sheet)

    def test_worksheet_round_trips_to_scoring_once_completed(self) -> None:
        sheet = re_.worksheet()
        self.assertEqual(sheet["version"], re_.load_spec()["version"])
        with self.assertRaises(ValueError):
            re_.score_human_session(sheet)

    def test_unmeasured_workflow_time_is_reported_as_such(self) -> None:
        sheet = self._sheet("competent")
        sheet["workflow_seconds"] = None
        res = re_.score_human_session(sheet)
        self.assertIsNone(res["workflow_only_seconds"])
        self.assertIn("not measured", res["evidence"]["workflow_time_note"])

    def test_pooled_sessions_report_each_session_and_total_effort(self) -> None:
        other = self._sheet("competent", 20)
        other["workflow_seconds"] = 40
        pooled = re_.pool_human_sessions([self._sheet("competent"), other])
        self.assertEqual((pooled["session_count"], pooled["distinct_reviewers"]), (2, 1))
        self.assertTrue(pooled["all_sessions_passed"])
        n = len(re_.load_spec()["proposals"])
        eff = pooled["effort_comparison"]
        self.assertEqual(eff["human_review_seconds"], 50 * n)
        self.assertEqual(
            (eff["workflow_only_seconds"], eff["difference_seconds"]), (100, 50 * n - 100)
        )
        self.assertTrue(
            all(c["seeded"] == c["detected"] for c in pooled["by_defect_class"].values())
        )

    def test_pool_does_not_hide_a_failed_session_or_a_repeat_reviewer(self) -> None:
        bad = self._sheet("automation_bias", 5)
        bad["workflow_seconds"] = None
        pooled = re_.pool_human_sessions([self._sheet("competent"), bad])
        self.assertFalse(pooled["all_sessions_passed"])
        self.assertEqual((pooled["sessions_passed"], pooled["distinct_reviewers"]), (1, 1))
        self.assertEqual(pooled["sessions_with_automation_bias_exposure"], 1)
        self.assertIsNone(pooled["effort_comparison"]["difference_seconds"])
        self.assertIn("not conformance", " ".join(pooled["evidence"]["open_items"]))
        with self.assertRaises(ValueError):
            re_.pool_human_sessions([])

    def test_pool_flags_a_duplicate_sheet_and_does_not_double_count_it(self) -> None:
        once = re_.pool_human_sessions([self._sheet("competent")])
        twice = re_.pool_human_sessions([self._sheet("competent"), self._sheet("competent")])
        self.assertEqual(twice["session_count"], 1)
        self.assertEqual(len(twice["duplicate_sheets"]), 1)
        self.assertEqual(twice["duplicate_sheets"][0]["position"], 1)
        self.assertEqual(twice["duplicate_sheets"][0]["duplicate_of"], 0)
        self.assertEqual(twice["effort_comparison"], once["effort_comparison"])
        self.assertEqual(twice["by_defect_class"], once["by_defect_class"])
        self.assertEqual(once["duplicate_sheets"], [])

    def test_pool_fails_a_session_from_a_reviewer_without_defined_authority(self) -> None:
        other = self._sheet("competent")
        other["reviewer_code"] = "EV-02"
        pooled = re_.pool_human_sessions([self._sheet("competent"), other])
        self.assertEqual((pooled["sessions_passed"], pooled["distinct_reviewers"]), (1, 2))
        self.assertFalse(pooled["all_sessions_passed"])

    def test_cli_pools_several_sheets_and_fails_on_a_failed_session(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            paths = []
            for k, kind in enumerate(("competent", "default_accept")):
                path = f"{d}/s{k}.json"
                Path(path).write_text(json.dumps(self._sheet(kind, 9)), encoding="utf-8")
                paths.append(path)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = re_.main(["--score", *paths])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out.getvalue())["session_count"], 2)


if __name__ == "__main__":
    unittest.main()
