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
        for name, sha256 in bindings["measurement_provenance_revision"]["source_sha256"].items():
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


if __name__ == "__main__":
    unittest.main()
