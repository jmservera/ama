import json
import unittest

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

        spec = json.loads(re_.GOLDEN.read_text())
        with mock.patch.dict(os.environ, {"ZF_AI": "off"}), tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                re_.run_panel("competent", re_.competent, spec, tmp)

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


if __name__ == "__main__":
    unittest.main()
