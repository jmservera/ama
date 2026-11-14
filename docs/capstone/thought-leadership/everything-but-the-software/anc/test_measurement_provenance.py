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
        for name, sha256 in bindings["finalization_revision"]["source_sha256"].items():
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

    def test_given_completed_judging_when_described_then_original_endpoints_remain_distinct(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn(r"\label{sec:postrunjudging}", protocol)
        self.assertIn(r"\ref{app:postrunjudging}", protocol)
        self.assertIn("original coverage, retained-contract-loss", protocol)
        self.assertIn("supplementary exploratory evidence", protocol)
        self.assertIn("not a replacement for", text)
        self.assertIn("b7973e200a6edbb1d19355badae3b7e03a066b09", text)
        self.assertIn("6cc0c236e4ca093198d38909dceb80f850196faa", text)
        self.assertIn(r"\resultstrue", (PACKAGE / "main.tex").read_text())
        methods = protocol.split(r"\label{sec:postrunjudging}", 1)[1].split(
            r"\subsection{Replication and uncertainty}", 1
        )[0]
        self.assertIn("designed and run after", methods)
        self.assertNotIn("will receive", methods)
        self.assertNotIn("will replay", methods)

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
        current = bindings["finalization_revision"]
        runtime_flow = bindings["runtime_flow_revision"]
        historical = bindings["measurement_provenance_revision"]

        self.assertEqual(
            hashlib.sha256((PACKAGE / "main.pdf").read_bytes()).hexdigest(),
            current["delivery_sha256"],
        )
        self.assertEqual(current["delivery_pages"], 64)
        self.assertEqual(current["supplement_start_page"], 45)
        self.assertEqual(bindings["attested_report_revision"]["delivery_pages"], 64)
        self.assertEqual(bindings["attested_report_revision"]["supplement_start_page"], 45)
        self.assertEqual(bindings["readability_revision"]["delivery_pages"], 60)
        self.assertEqual(bindings["readability_revision"]["supplement_start_page"], 44)
        self.assertEqual(bindings["study_results_revision"]["delivery_pages"], 56)
        self.assertEqual(bindings["study_results_revision"]["supplement_start_page"], 46)
        self.assertEqual(runtime_flow["delivery_pages"], 49)
        self.assertEqual(runtime_flow["supplement_start_page"], 39)
        self.assertEqual(bindings["blind_judging_revision"]["delivery_pages"], 47)
        self.assertEqual(historical["delivery_pages"], 45)
        self.assertEqual(
            historical["delivery_sha256"],
            "58287cefefb4d0b10b6db6bac086a23c329597fe356211a88cda3ac144fea52f",
        )

    def test_study_results_tables_and_mandatory_guardrails_are_present(self):
        from check_paper import expand_inputs

        manuscript = (PACKAGE / "main.tex").read_text()
        source = expand_inputs(manuscript)
        supplement = (ANC / "measurement-provenance.tex").read_text()

        for label in (
            r"\label{sec:resultsledger}",
            r"\label{sec:resultscorrectness}",
            r"\label{sec:resultsstructural}",
            r"\label{sec:resultsjudging}",
            r"\label{tab:resultsbenchmark}",
            r"\label{tab:resultsadaptation}",
            r"\label{tab:resultsstructural}",
            r"\label{tab:resultscosts}",
            r"\label{tab:resultsjudgecontrasts}",
            r"\label{tab:resultsjudgemeans}",
            r"\label{tab:resultsjudgemeanscr1}",
            r"\label{tab:resultscalibration}",
            r"\label{tab:executionepochs}",
        ):
            with self.subTest(label=label):
                self.assertIn(label, source)

        for marker in (
            "primary_estimates_available=false",
            "intervention-coverage/v1",
            "pilot-estimation-gemini-4-argon-E-15",
            "pilot-estimation-gpt-6.1-sol-C-20",
            "62,052.61",
            "18,900.0",
            "783.16",
            "418.64",
            "human-calibration-guidance/v3",
            "review_status=in_progress",
            "42,594",
            "5,357",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)

        for commit in (
            "7943e40347862e76e3bc04490040ad5904487c86",
            "a9d76bb6dbb118c43315fb2a13b7bcdb732d946d",
            "3e44ae10547b6376864089e605e946f74a378d56",
        ):
            with self.subTest(commit=commit):
                self.assertIn(commit, manuscript)

        self.assertIn("fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f256f2de1", supplement)
        self.assertIn("c10e6d6f62785a5028406a9963acdd499f6bd6b6", supplement)

    def test_given_readable_results_when_checked_then_tables_preserve_allocations_and_outcomes(self):
        from test_protocol_planning import table_rows

        protocol = (ANC / "experiment-protocol.tex").read_text()
        tables = {
            label: {
                (row[0].removeprefix(r"\midrule").strip(), row[1]): row[2:]
                for row in table_rows(protocol, label)
            }
            for label in (
                "tab:resultsbenchmark", "tab:resultsadaptation",
                "tab:resultsstructural", "tab:resultscosts",
            )
        }
        expected_cells = {
            (model, arm)
            for model in ("Sonnet 5.5", "Gemini 4 Argon", "GPT 6.1 Sol")
            for arm in "ABCDE"
        }

        for label, rows in tables.items():
            with self.subTest(table=label):
                self.assertEqual(set(rows), expected_cells)
        coverage = tables["tab:resultsbenchmark"]
        adaptation = tables["tab:resultsadaptation"]
        self.assertEqual(sum(int(row[0].split("/")[0]) for row in coverage.values()), 313)
        self.assertEqual(coverage[("Gemini 4 Argon", "E")][0], "20/21")
        self.assertEqual(coverage[("GPT 6.1 Sol", "C")][0], "20/21")
        self.assertEqual(
            [coverage[("GPT 6.1 Sol", arm)][2] for arm in "ABDE"],
            ["5", "12", "6", "12"],
        )
        for identity, row in adaptation.items():
            with self.subTest(cell=identity):
                self.assertEqual(sum(int(value) for value in row[:3]), 21)
        self.assertEqual(adaptation[("Gemini 4 Argon", "B")][0], "8")
        self.assertEqual(adaptation[("Gemini 4 Argon", "C")][0], "16")
        results = protocol.split(r"\ifresults", 1)[1].split(r"\else", 1)[0]
        self.assertNotIn(r"\scriptsize", results)

    def test_given_structural_summary_when_read_then_target_shortfalls_are_explicit(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())

        self.assertIn("not uniformly achieved", protocol)
        self.assertIn("2.26 lint warnings", protocol)
        self.assertIn("did not satisfy every B target", protocol)
        self.assertIn("50\\% more time and twice the credit allowance", manuscript)
        self.assertNotIn("baseline code already satisfied", manuscript)
        self.assertNotIn("enforced its structural stopping targets", protocol)

    def test_given_report_refresh_when_read_then_attestation_and_gates_remain_distinct(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())

        self.assertIn("all 313 completed trajectories", protocol)
        self.assertIn("operator account of intervention", protocol)
        self.assertIn("primary_estimates_available=false", protocol)
        self.assertIn("five-arm frame is incomplete", protocol)
        self.assertIn("63 versus 63", protocol)
        self.assertIn("post-collection exploratory", protocol)
        self.assertNotIn("attestation remains absent", protocol)
        self.assertNotIn("missing intervention attestation", manuscript)
        self.assertIn("not an independent verification", supplement)
        self.assertIn("not mean paired statistical resampling", supplement)
        self.assertIn("not multiplicity-adjusted", supplement)

    def test_given_report_refresh_when_coverage_compared_then_intervals_and_bounds_stay_separate(self):
        from test_protocol_planning import table_rows

        supplement = (ANC / "measurement-provenance.tex").read_text()
        pooled = {
            row[0]: row[1:] for row in table_rows(supplement, "tab:resultsh1contrasts")
        }
        model_rows = table_rows(supplement, "tab:resultsh1modelintervals")
        cr_rows = table_rows(supplement, "tab:resultscrintervals")

        self.assertEqual(pooled, {
            "B -- D": ["63/63", "+1.1874", "[+0.1000, +2.2247]", "[+1.1874, +1.1874]"],
            "B -- A": ["63/63", "+1.4123", "[+0.3250, +2.4497]", "[+1.4123, +1.4123]"],
            "B -- C": ["63/62", "---", "---", "[+0.6624, +2.2497]"],
            "E -- B": ["62/63", "---", "---", "[-1.5498, +0.0375]"],
        })
        self.assertEqual(len(model_rows), 12)
        self.assertEqual(sum(row[2] == "---" and row[3] == "---" for row in model_rows), 2)
        self.assertEqual(len(cr_rows), 7)
        self.assertFalse(any(row[0].startswith("GPT") for row in cr_rows))
        for row in cr_rows:
            with self.subTest(model=row[0], contrast=row[1]):
                lower, upper = [float(value) for value in row[-1].strip("[]").split(",")]
                self.assertLessEqual(lower, 0)
                self.assertGreaterEqual(upper, 0)
        self.assertIn("not simultaneous coverage over all comparisons", supplement)

    def test_given_report_refresh_when_judging_summarised_then_abstentions_remain_visible(self):
        from test_protocol_planning import table_rows

        supplement = (ANC / "measurement-provenance.tex").read_text()
        observed = table_rows(supplement, "tab:judgeobservedcontrasts")
        partial_counts = {
            "tab:judgepartialp10": ["0/0", "2/5", "9/13", "0/0", "0/0", "2/2", "11/9", "0/0"],
            "tab:judgepartialcr1": ["0/0", "2/1", "8/13", "0/0", "0/0", "1/2", "9/8", "0/0"],
        }

        self.assertEqual(len(observed), 8)
        self.assertEqual([row[-1] for row in observed], ["2/8", "9/16", "2/4", "9/17", "2/1", "8/16", "2/0", "8/18"])
        for label, expected in partial_counts.items():
            with self.subTest(table=label):
                self.assertEqual([row[-1] for row in table_rows(supplement, label)], expected)
        normalised = " ".join(supplement.split())
        self.assertIn("not the complete-scenario estimand", normalised)
        self.assertIn("not the unrated dimensions within observed trajectories", normalised)
        self.assertIn("not substituted for the full-allocation bounds", normalised)

    def test_given_finalization_when_approval_recorded_then_cela_clearance_is_not_invented(self):
        manuscript = (PACKAGE / "main.tex").read_text()
        approval_note = next(
            line for line in manuscript.splitlines()
            if line.startswith("% TODO(author)") and "CELA" in line
        )

        self.assertIn("owner-reported manager approval", approval_note)
        self.assertIn("27 October 2026 CELA submission", approval_note)
        self.assertIn("confirm that the applicable clearance process covers the final draft", approval_note)
        self.assertIn("not a separately inspected final-version clearance", approval_note)
        self.assertNotIn("CELA approved", approval_note)

    def test_given_finalization_when_metadata_recovered_then_history_is_not_rerun(self):
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())

        self.assertIn("all 5,357 attempts", supplement)
        self.assertIn(".study/pilot-estimation/state.json", supplement)
        self.assertIn("no separate finish or boot/launch IDs", supplement)
        self.assertIn("human-calibration completion flag remains false", supplement)
        self.assertIn("recover an unlogged historical version", supplement)
        self.assertIn("retain the analysis actually performed", protocol)
        self.assertIn("separately disclosed post-collection analysis", protocol)

    def test_given_finalization_when_deposit_selected_then_lineage_and_privacy_remain_explicit(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        source_review = " ".join((ANC / "additional-evidence.tex").read_text().split())

        self.assertIn("select the experiment GitHub repository as the deposit", manuscript)
        self.assertIn("v4, v6 and v7 releases retain separate protocol archives", manuscript)
        self.assertIn("verify the registered-protocol archive correspondence", manuscript)
        self.assertIn("historical/raw records and any newly published extracts require their own confidentiality review", manuscript)
        self.assertNotIn("azureuser@", manuscript)
        self.assertNotIn("4.165.128.254", manuscript)
        self.assertIn("39\\% relative", source_review)
        self.assertIn("caption says 35\\%", source_review)
        self.assertIn("institutional-abstract support", source_review)

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
