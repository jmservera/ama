"""Keep current measurement explanations and literal prompt examples source-bound."""

import hashlib
import json
import unittest
from pathlib import Path

ANC = Path(__file__).resolve().parent
PACKAGE = ANC.parent
PROMPTS = {
    "consolidation-active-e71037d9.prompt.txt": (
        "1ee3da712fcb787a7843d1270aabf61b55abb7c8b7df2534d4adc078b0241494",
        "fe00defa94b65eeb319e24256e425942247e0a14",
    ),
    "review-only-active-e71037d9.prompt.txt": (
        "06a8dfcaee30ab52c243c771844619cf08f23854ef866f1bfde5277362391725",
        "706d15d3c7e1615d58c0902a050b0e80d163e929",
    ),
}


class MeasurementProvenanceTests(unittest.TestCase):
    def test_active_prompt_bytes_match_the_inspected_source(self):
        for name, (sha256, blob) in PROMPTS.items():
            with self.subTest(prompt=name):
                data = (ANC / name).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), sha256)
                self.assertEqual(
                    hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
                    blob,
                )

    def test_literal_bindings_preserve_historical_and_active_prompts(self):
        bindings = json.loads((ANC / "supplement-integration.json").read_text())
        self.assertEqual(
            bindings["literal_inputs"]["anc/consolidation-frozen-v4.prompt.txt"],
            "75f646edbe04e1e3403b092b13edd6b66615a3362e67ad49744d229cdcb94f29",
        )
        for name, (sha256, _) in PROMPTS.items():
            self.assertEqual(bindings["literal_inputs"][f"anc/{name}"], sha256)
        for name, sha256 in bindings["runtime_flow_revision"]["source_sha256"].items():
            with self.subTest(source=name):
                self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(), sha256)

    def test_measurement_slice_and_prompt_examples_are_active(self):
        supplement = (ANC / "supplement-section.tex").read_text()
        slice_text = (ANC / "measurement-provenance.tex").read_text()
        self.assertIn(r"\input{anc/measurement-provenance.tex}", supplement)
        for name in PROMPTS:
            self.assertIn(f"{{anc/{name}}}", slice_text)
        self.assertIn("not a new judge prompt", slice_text)
        self.assertIn("not parse either note into a numerical quality", slice_text)

    def test_current_measurements_are_not_described_as_ai_judge_scores(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        self.assertIn("does not call a separate LLM-as-judge", protocol)
        self.assertIn(r"\label{tab:measurementprovenance}", protocol)
        self.assertIn("not instrumented", protocol)
        self.assertIn("comprehension is not measured", protocol)

    def test_current_ruff_limit_is_explicit_not_claimed_remedied(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        self.assertIn(r"but does not include", protocol)
        self.assertIn(r"\texttt{--ignore-noqa}", protocol)
        self.assertIn("exports no separate suppression", protocol)
        self.assertIn("changes no running instrumentation", protocol)

    def test_active_fields_and_units_remain_named(self):
        text = (ANC / "measurement-provenance.tex").read_text()
        for field in (
            r"hidden\_passed", r"hidden\_total", r"mean\_ccn", r"max\_ccn",
            r"share\_ccn\_over\_10", r"dup\_pct", r"lint\_per\_kloc",
            r"nloc\_src", r"md\_words", r"test\_counts", "totalNanoAiu",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)
        self.assertIn("not interchangeable instruments", text)
        self.assertIn("not a remeasurement", text)

    def test_judging_is_a_prospective_supplement_not_a_treatment_change(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn(r"\label{sec:postrunjudging}", protocol)
        self.assertIn(r"\ref{app:postrunjudging}", protocol)
        self.assertIn("original coverage, retained-contract-loss", protocol)
        self.assertIn("supplementary exploratory evidence", protocol)
        self.assertIn("not a replacement for", text)
        self.assertIn("b7973e200a6edbb1d19355badae3b7e03a066b09", text)
        self.assertIn("6cc0c236e4ca093198d38909dceb80f850196faa", text)
        self.assertIn(r"\resultsfalse", (PACKAGE / "main.tex").read_text())

    def test_judging_preserves_witnessed_risk_sets_and_undefined_density(self):
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn(r"\label{eq:workflowloss}", text)
        self.assertIn("An empty risk set", text)
        self.assertIn("density undefined", text)
        self.assertIn("incomplete histories with no observed pass", text)
        self.assertIn("F10 first becomes eligible", text)
        self.assertIn("cannot alone rank treatment efficacy", text)
        self.assertIn("nine scenarios", text)
        self.assertIn("eleven after CR1", text)
        self.assertIn("passing $P_{10}$", text)

    def test_judging_ratings_are_separate_ordinal_dimensions(self):
        text = (ANC / "measurement-provenance.tex").read_text()

        for dimension in (
            "Functional completeness", "workflow coherence",
            "error recovery", "API", "usability",
        ):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, text)
        self.assertIn("Unsupported dimensions are null, not zero", text)
        self.assertIn("no composite software-quality score", text)
        self.assertIn("not established inter-rater", text)
        self.assertIn("blinded human-reviewed calibration sample", text)
        self.assertIn("earlier passing witness", text)
        self.assertIn("Historical and final observations reuse", text)
        self.assertIn("separately versioned instrument", text)

    def test_judging_aggregation_retains_full_frame_and_nested_units(self):
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn("all scheduled judge/repeat ratings", text)
        self.assertIn("both compared", text)
        self.assertIn("every allocated development model", text)
        self.assertIn("complete survivors", text)
        self.assertIn("equally weight within-model differences", text)
        self.assertIn("nested within", text)
        self.assertIn("bootstrap intervals, hypothesis tests or formal verdicts", text)

    def test_judging_costs_and_authorisations_remain_separate(self):
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn(r"$2NJR$", text)
        self.assertIn("Preparation spends no AI credits", text)
        self.assertIn("separate explicit operator authorisation", text)
        self.assertIn("unknown-charge reservations", text)
        self.assertIn("hard provider spending cap", text)
        self.assertIn("raw packets and mappings", text)

    def test_judging_delivery_binding_preserves_the_historical_measurement_record(self):
        bindings = json.loads((ANC / "supplement-integration.json").read_text())
        current = bindings["runtime_flow_revision"]
        historical = bindings["measurement_provenance_revision"]

        self.assertEqual(
            hashlib.sha256((PACKAGE / "main.pdf").read_bytes()).hexdigest(),
            current["delivery_sha256"],
        )
        self.assertEqual(current["delivery_pages"], 49)
        self.assertEqual(current["supplement_start_page"], 39)
        self.assertEqual(bindings["blind_judging_revision"]["delivery_pages"], 47)
        self.assertEqual(historical["delivery_pages"], 45)
        self.assertEqual(
            historical["delivery_sha256"],
            "58287cefefb4d0b10b6db6bac086a23c329597fe356211a88cda3ac144fea52f",
        )

    def test_runtime_flow_separates_development_commands_from_tool_free_judging(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()

        self.assertIn(r"\label{sec:runtimeboundaries}", protocol)
        self.assertIn(r"{fig-runtime-boundaries.png}", protocol)
        self.assertIn(r"\texttt{isolated\_exec}", protocol)
        self.assertIn("fresh isolated container", protocol)
        self.assertIn("Validated filesystem/Git state is replayed", protocol)
        self.assertIn("processes and memory do not persist", protocol)
        self.assertIn("no command tools or candidate-repository access", protocol)
        self.assertIn("outside the replay container", protocol)
        self.assertIn("isolation or collection failure", protocol)
        self.assertIn("successfully collected candidate failure", protocol)
        self.assertIn("re-adds four for its protected supervisor", protocol)
        self.assertIn("not capability-free", protocol)


if __name__ == "__main__":
    unittest.main()
