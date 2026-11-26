"""Keep current measurement explanations and literal prompt examples source-bound."""

import hashlib
import json
import math
import re
import struct
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
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


def read_source_register() -> dict[str, str]:
    """Read the end register's record identifiers and full digests.

    Returns:
        Record-to-digest bindings from the active manuscript register.
    """
    manuscript = (PACKAGE / "main.tex").read_text()
    register = manuscript.split(r"\section{Source and digest register}", 1)[1]
    return dict(re.findall(
        r"\\label\{prov:(R\d+)\}.*?\\nolinkurl\{([0-9a-f]{64}|[0-9a-f]{40})\}",
        register, re.DOTALL,
    ))


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
        previous = bindings["scientific_voice_revision"]
        self.assertEqual(previous["prior_delivery_revision"], "copy_review_revision")
        current = bindings["publication_readiness_revision"]
        self.assertEqual(current["prior_delivery_revision"], "scientific_voice_revision")
        cleanup = bindings["results_switch_cleanup"]
        self.assertEqual(cleanup["prior_delivery_revision"], "publication_readiness_revision")
        warning_cleanup = bindings["latex_warning_cleanup"]
        self.assertEqual(warning_cleanup["prior_delivery_revision"], "results_switch_cleanup")
        comment_cleanup = bindings["final_source_comment_cleanup"]
        self.assertEqual(comment_cleanup["prior_delivery_revision"], "latex_warning_cleanup")
        example_revision = bindings["generic_claims_revision"]
        self.assertEqual(
            example_revision["prior_delivery_revision"], "final_source_comment_cleanup"
        )
        unsupported_revision = bindings["unsupported_claims_revision"]
        self.assertEqual(
            unsupported_revision["prior_delivery_revision"], "generic_claims_revision"
        )
        author_context_revision = bindings["author_context_revision"]
        self.assertEqual(
            author_context_revision["prior_delivery_revision"], "unsupported_claims_revision"
        )
        annotation_cleanup = bindings["review_annotation_cleanup"]
        self.assertEqual(
            annotation_cleanup["prior_delivery_revision"], "author_context_revision"
        )
        editorial = bindings[bindings["current_editorial_revision"]]
        self.assertEqual(
            editorial["prior_delivery_revision"], "final_editorial_revision_2026_11_26"
        )
        for name, sha256 in {
            **current["evidence_sha256"], **editorial["source_sha256"],
        }.items():
            with self.subTest(source=name):
                self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(), sha256)
        self.assertEqual(
            hashlib.sha256((PACKAGE / "main.pdf").read_bytes()).hexdigest(),
            editorial["retained_pdf_sha256"],
        )

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
        supplement = (ANC / "measurement-provenance.tex").read_text()
        self.assertIn("without calling an LLM-as-judge", protocol)
        self.assertIn(r"\label{tab:measurementprovenance}", supplement)
        self.assertIn("distinct from instrumented", protocol)
        self.assertIn("comprehension was not measured", protocol)

    def test_current_ruff_limit_is_explicit_not_claimed_remedied(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        supplement = (ANC / "measurement-provenance.tex").read_text()
        self.assertIn("Inline lint suppressions were not independently counted", protocol)
        self.assertIn(r"\texttt{--ignore-noqa}", supplement)
        self.assertIn("exports no separate suppression", supplement)
        self.assertIn("changes no running instrumentation", supplement)

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
        self.assertIn("inventory based on inspected code", text)

    def test_given_completed_judging_when_described_then_original_endpoints_remain_distinct(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        text = (ANC / "measurement-provenance.tex").read_text()

        self.assertIn(r"\label{sec:postrunjudging}", protocol)
        self.assertIn(r"\ref{app:postrunjudging}", protocol)
        self.assertIn("original coverage, retained-contract-loss", protocol)
        self.assertIn("supplementary exploratory evidence", protocol)
        self.assertIn("not a replacement for", text)
        records = read_source_register()
        self.assertIn(r"\sourceref{R36}", text)
        self.assertIn(r"\sourceref{R37}", text)
        self.assertEqual(records["R36"], "b7973e200a6edbb1d19355badae3b7e03a066b09")
        self.assertEqual(records["R37"], "6cc0c236e4ca093198d38909dceb80f850196faa")
        self.assertIn(r"\label{sec:resultsledger}", protocol)
        methods = protocol.split(r"\label{sec:postrunjudging}", 1)[1].split(
            r"\subsection{Replication and uncertainty}", 1
        )[0]
        self.assertIn("Designed after development", methods)
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
        self.assertIn("No preparation-cost measurement is reported", text)
        self.assertIn("separate explicit operator authorisation", text)
        self.assertIn("unknown-charge reservations", text)
        self.assertIn("hard provider spending cap", text)
        self.assertIn("raw packets and mappings", text)

    def test_human_readability_binding_preserves_the_historical_measurement_record(self):
        bindings = json.loads((ANC / "supplement-integration.json").read_text())
        previous = bindings["author_voice_revision"]
        style = bindings["style_revision"]
        current = bindings["human_readability_revision"]
        finalization = bindings["finalization_revision"]
        runtime_flow = bindings["runtime_flow_revision"]
        historical = bindings["measurement_provenance_revision"]

        self.assertEqual(
            previous["delivery_sha256"],
            "8fc72c56d892fdf7be42a6f06c8c3880d51372e64ac2822d32887c4949c91908",
        )
        self.assertEqual(previous["delivery_pages"], 71)
        self.assertEqual(
            previous["source_sha256"]["main.tex"],
            "8ace88a8a0d2de39cf58130d94f12db938092ee4049cb3a406f3571ce60058a9",
        )
        self.assertEqual(
            style["delivery_sha256"],
            "6125792d2db26738fbcb74876e1d89423898641236ffc8e6a1a7bfca00e59868",
        )
        self.assertEqual(style["prior_delivery_revision"], "author_voice_revision")
        self.assertEqual(style["delivery_pages"], 72)
        self.assertEqual(style["supplement_start_page"], 45)
        self.assertEqual(current["prior_delivery_revision"], "style_revision")
        self.assertEqual(current["delivery_status"], "source-only; existing main.pdf excluded")
        self.assertEqual(len(current["source_sha256"]), 8)
        self.assertEqual(bindings["provenance_readability_revision"]["delivery_pages"], 70)
        self.assertEqual(bindings["chart_interpretation_revision"]["delivery_pages"], 70)
        self.assertEqual(bindings["chart_interpretation_revision"]["supplement_start_page"], 51)
        self.assertEqual(bindings["final_results_revision"]["delivery_pages"], 69)
        self.assertEqual(bindings["final_results_revision"]["supplement_start_page"], 50)
        self.assertEqual(bindings["falsifiability_revision"]["delivery_pages"], 66)
        self.assertEqual(bindings["falsifiability_revision"]["supplement_start_page"], 47)
        self.assertEqual(finalization["delivery_pages"], 64)
        self.assertEqual(finalization["supplement_start_page"], 45)
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
            "primary_estimates_available=true",
            "intervention-coverage/v1",
            "pilot-estimation-gemini-4-argon-E-15",
            "pilot-estimation-gpt-6.1-sol-C-20",
            "62,299.76",
            "19,200.0",
            "783.16",
            "418.64",
            "human-calibration-guidance/v3",
            "review_status=in_progress",
            "42,664",
            "5,372",
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

        records = read_source_register()
        self.assertIn(r"\sourceref{R38}", supplement)
        self.assertIn(r"\sourceref{R43}", supplement)
        self.assertEqual(records["R38"], "fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f256f2de1")
        self.assertEqual(records["R43"], "c10e6d6f62785a5028406a9963acdd499f6bd6b6")

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
        self.assertEqual(sum(int(row[0].split("/")[0]) for row in coverage.values()), 315)
        self.assertEqual(coverage[("Gemini 4 Argon", "E")][0], "21/21")
        self.assertEqual(coverage[("GPT 6.1 Sol", "C")][0], "21/21")
        self.assertEqual(
            [coverage[("GPT 6.1 Sol", arm)][2] for arm in "ABDE"],
            ["5", "12", "6", "12"],
        )
        for identity, row in adaptation.items():
            with self.subTest(cell=identity):
                self.assertEqual(sum(int(value) for value in row[:3]), 21)
        self.assertEqual(adaptation[("Gemini 4 Argon", "B")][0], "8")
        self.assertEqual(adaptation[("Gemini 4 Argon", "C")][0], "16")
        results = protocol.split(r"\label{sec:resultsledger}", 1)[1]
        self.assertNotIn(r"\scriptsize", results)

    def test_given_structural_summary_when_read_then_target_shortfalls_are_explicit(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())

        self.assertIn("not uniformly achieved", protocol)
        self.assertIn("2.26 lint warnings", protocol)
        self.assertIn("did not satisfy every B target", protocol)
        self.assertIn("Matching resource ceilings did not match spending", manuscript)
        self.assertNotIn("baseline code already satisfied", manuscript)
        self.assertNotIn("enforced its structural stopping targets", protocol)

    def test_given_report_refresh_when_read_then_attestation_and_gates_remain_distinct(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())

        self.assertIn("All 315 allocated trajectories completed", protocol)
        self.assertIn("Isabel Cabezas Martin supplied the attestation", protocol)
        self.assertIn("was not an independent auditor", protocol)
        self.assertIn("primary_estimates_available=true", supplement)
        self.assertIn("Two completed GPT trajectories", supplement)
        self.assertIn("63 versus 63", supplement)
        self.assertIn("exploratory", protocol)
        self.assertNotIn("attestation remains absent", protocol)
        self.assertNotIn("missing intervention attestation", manuscript)
        self.assertIn("have not been independently verified", supplement)
        self.assertIn("does not match trajectories into statistical pairs", supplement)
        self.assertIn("not multiplicity-adjusted", supplement)

    def test_given_report_refresh_when_coverage_compared_then_intervals_and_bounds_stay_separate(self):
        from fractions import Fraction
        from statistics import NormalDist

        from test_protocol_planning import table_rows

        supplement = (ANC / "measurement-provenance.tex").read_text()
        pooled = {
            row[0]: row[1:] for row in table_rows(supplement, "tab:resultsh1contrasts")
        }
        model_rows = table_rows(supplement, "tab:resultsh1modelintervals")
        cr_rows = table_rows(supplement, "tab:resultscrintervals")
        observed = {
            (row[0].removeprefix(r"\midrule").strip(), row[1]): int(row[2])
            for row in table_rows((ANC / "experiment-protocol.tex").read_text(),
                                  "tab:resultsadaptation")
            if "GPT" not in row[0]
        }
        z = NormalDist().inv_cdf(0.975)

        def wilson(successes):
            p, n = successes / 21, 21
            denominator = 1 + z * z / n
            centre = (p + z * z / (2 * n)) / denominator
            radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
            return centre - radius, centre + radius

        self.assertEqual(pooled, {
            "B -- D": ["63/63", "+1.1874", "[+0.1000, +2.2247]", "[+1.1874, +1.1874]"],
            "B -- A": ["63/63", "+1.4123", "[+0.3250, +2.4497]", "[+1.4123, +1.4123]"],
            "B -- C": ["63/63", "+0.6624", "[-0.4499, +1.7498]", "[+0.6624, +0.6624]"],
            "E -- B": ["63/63", "+0.0375", "[-1.0749, +1.1374]", "[+0.0375, +0.0375]"],
        })
        self.assertEqual(len(model_rows), 12)
        self.assertEqual(sum(row[2] == "---" and row[3] == "---" for row in model_rows), 0)
        self.assertEqual(len(cr_rows), 8)
        self.assertFalse(any(row[0].startswith("GPT") for row in cr_rows))
        for row in cr_rows:
            with self.subTest(model=row[0], contrast=row[1]):
                lower, upper = [float(value) for value in row[-1].strip("[]").split(",")]
                model = row[0].removeprefix(r"\midrule").strip()
                left, right = (arm.strip() for arm in row[1].split("--"))
                x, y = observed[(model, left)], observed[(model, right)]
                l1, u1 = wilson(x)
                l2, u2 = wilson(y)
                difference = (x - y) / 21
                expected_lower = 100 * (difference - math.hypot(x / 21 - l1, u2 - y / 21))
                expected_upper = 100 * (difference + math.hypot(u1 - x / 21, y / 21 - l2))
                self.assertAlmostEqual(float(row[2]), 100 * difference, places=4)
                self.assertAlmostEqual(lower, expected_lower, places=4)
                self.assertAlmostEqual(upper, expected_upper, places=4)

                successes, failures = x + y, 42 - x - y

                def probability(k, successes=successes, failures=failures):
                    return Fraction(
                        math.comb(successes, k) * math.comb(failures, 21 - k),
                        math.comb(42, 21),
                    )

                observed_probability = probability(x)
                fisher = sum(
                    (probability(k)
                     for k in range(max(0, 21 - failures), min(21, successes) + 1)
                     if probability(k) <= observed_probability),
                    Fraction(),
                )
                self.assertAlmostEqual(float(row[-2]), float(fisher), places=5)
                self.assertLessEqual(lower, 0)
                if (model, row[1]) == ("Gemini 4 Argon", "B -- C"):
                    self.assertLess(upper, 0)
                else:
                    self.assertGreaterEqual(upper, 0)
        self.assertIn("Newcombe hybrid-score", supplement)
        self.assertIn("two-sided Fisher exact", supplement)
        self.assertIn("unadjusted for multiplicity", supplement)

    def test_given_reporting_reconciliation_when_tabulated_then_denominators_and_holds_match(self):
        from test_protocol_planning import table_rows

        evidence = json.loads((ANC / "publication-evidence-2026-11-24.json").read_text())
        supplement = (ANC / "measurement-provenance.tex").read_text()
        models = {
            "Sonnet 5.5": "claude-sonnet-5.5",
            "Gemini 4 Argon": "gemini-4-argon",
            "GPT 6.1 Sol": "gpt-6.1-sol",
        }
        prerequisite_rows = table_rows(supplement, "tab:crprerequisites")
        self.assertEqual(len(prerequisite_rows), sum(
            len(evidence["CR1_prerequisite_strata"][model]) for model in models.values()
        ))
        for model, arm, complete, other, unknown in prerequisite_rows:
            model = models[model.removeprefix(r"\midrule").strip()]
            groups = evidence["CR1_prerequisite_strata"][model][arm]
            with self.subTest(model=model, arm=arm):
                for observed, name in ((complete, "both_complete"), (other, "not_both_complete")):
                    successes, allocated, _ = groups[name]
                    expected = f"{successes}/{allocated}" if allocated else r"\textendash{}"
                    self.assertEqual(observed, expected)
                self.assertEqual(groups["both_complete"][2], 0)
                self.assertEqual(int(unknown), groups["not_both_complete"][2])

        held_rows = table_rows(supplement, "tab:heldbillingcells")
        column_totals = [0] * 5
        for model, *counts in held_rows[:-1]:
            expected = evidence["held_attempts_by_model_arm"][models[model]]
            observed = [int(value) for value in counts]
            self.assertEqual(observed, [*[expected[arm] for arm in "ABCDE"],
                                        sum(expected.values())])
            column_totals = [a + b for a, b in zip(column_totals, observed[:-1])]
        self.assertEqual([int(value) for value in held_rows[-1][1:]],
                         [*column_totals, sum(column_totals)])

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
        self.assertIn("different question from a comparison covering every scheduled scenario", normalised)
        self.assertIn("not the unrated dimensions within observed trajectories", normalised)
        self.assertIn("not substituted for the full-allocation bounds", normalised)

    def test_given_finalization_when_approval_recorded_then_cela_clearance_is_not_invented(self):
        manuscript = (PACKAGE / "main.tex").read_text()
        report = (ANC / "revision-report.md").read_text()
        checklist_row = next(
            line for line in report.splitlines()
            if line.startswith("| 21 | Human clearance and approval |")
        )

        self.assertNotIn("CELA", manuscript)
        self.assertNotIn("AICC", manuscript)
        self.assertIn("Record manager approval", checklist_row)
        self.assertIn("14 November AICC receipt", checklist_row)
        self.assertIn("14-day no-objection window maturing 29 November 2026", checklist_row)
        self.assertIn("Written CELA policy was not independently inspected", checklist_row)
        self.assertIn("29 November 2026 has not yet elapsed", checklist_row)
        self.assertIn("cover this exact 24 November draft", checklist_row)
        self.assertNotIn("CELA approved", report)

    def test_given_finalization_when_metadata_recovered_then_history_is_not_rerun(self):
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())

        self.assertIn("all 5,357 attempts", supplement)
        self.assertIn(".study/pilot-estimation/state.json", supplement)
        self.assertIn("no separate finish or boot/launch IDs", supplement)
        self.assertIn("human-calibration completion flag remains false", supplement)
        self.assertIn("recover an unlogged historical version", supplement)
        self.assertIn("retain the analysis actually performed", supplement)
        self.assertIn("separately disclosed post-collection analysis", supplement)

    def test_given_finalization_when_deposit_selected_then_lineage_and_privacy_remain_explicit(self):
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        source_review = " ".join((ANC / "additional-evidence.tex").read_text().split())
        revision_report = " ".join((ANC / "revision-report.md").read_text().split())

        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())
        self.assertIn("provides the selected public deposit with checksums", manuscript)
        for version in ("v4", "v6", "v7"):
            with self.subTest(version=version):
                self.assertIn(f"protocol-frozen-{version}", supplement)
        self.assertIn("releases retain separate protocol archives", supplement)
        self.assertIn("results-exploratory-s1-v1", manuscript)
        self.assertIn("No post-collection OSF deposit was created", manuscript)
        self.assertIn(
            "Raw packets, specimen mappings and runtime workspaces stay outside Git", manuscript,
        )
        self.assertIn(
            "Historical/raw records and newly released excerpts require confidentiality review.",
            revision_report,
        )
        self.assertNotIn("azureuser@", manuscript)
        self.assertNotIn("4.165.128.254", manuscript)
        self.assertIn(
            r"Exchange Act Release No.~\nolinkurl{34-70694}, Paragraphs~1, 12--17", source_review,
        )
        self.assertIn("late 2024 with IDE and chat assistants", source_review)
        self.assertIn("Non-essential citations that had only abstract, excerpt or unverified third-party caption access were removed", source_review)

    def test_given_falsifiable_predictions_when_read_then_verdicts_and_future_design_are_explicit(self):
        from check_paper import expand_inputs
        from test_protocol_planning import table_rows

        manuscript = " ".join(expand_inputs((PACKAGE / "main.tex").read_text()).split())
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())
        rows = table_rows(protocol, "tab:predictionverdicts")

        self.assertEqual(len(rows), 4)
        self.assertEqual(
            [row[0].split(":", 1)[0] for row in rows],
            ["P1", "P2", "P3", "Manipulation check"],
        )
        for marker in (
            "P1 (Short-horizon decay premise)",
            "P2 (Primary coverage gain threshold)",
            "P3 (Change-request adaptability and short-horizon payback)",
            "Manipulation check (Structural treatment fidelity)",
            r"\label{sec:futureexperiment}",
            "N=30",
            "Latin-square",
            r"2\times2",
            "Sonnet~5.5 and Gemini~4 Argon showed small B--D gains",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, manuscript)
        self.assertIn("comes almost entirely from GPT~6.1 Sol acquiring the ninth feature", protocol)

    def test_runtime_flow_separates_development_commands_from_tool_free_judging(self):
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())

        self.assertIn(r"\label{sec:runtimeboundaries}", protocol)
        self.assertIn(r"{fig-runtime-boundaries.png}", protocol)
        self.assertIn(r"\texttt{isolated\_exec}", supplement)
        self.assertIn("fresh container", protocol)
        self.assertIn("Validated filesystem and Git state", protocol)
        self.assertIn("candidate processes and process memory do not", protocol)
        self.assertIn("without command tools or", protocol)
        self.assertIn("candidate-repository access", protocol)
        self.assertIn("outside the replay container", protocol)
        self.assertIn("Isolation failures made a checkpoint unavailable", protocol)
        self.assertIn("observed candidate failures stayed", protocol)
        self.assertIn("re-adds four for its protected supervisor", supplement)
        self.assertIn("capabilities remain at the container level", supplement)

    def test_given_final_results_when_tables_checked_then_snapshot_values_and_unknowns_match(self):
        from test_protocol_planning import table_rows

        snapshot = json.loads((ANC / "study-results-2026-11-15.json").read_text())
        protocol = (ANC / "experiment-protocol.tex").read_text()
        models = {"claude-sonnet-5.5": "Sonnet 5.5", "gemini-4-argon": "Gemini 4 Argon", "gpt-6.1-sol": "GPT 6.1 Sol"}
        tables = {
            label: {(row[0].removeprefix(r"\midrule").strip(), row[1]): row[2:]
                    for row in table_rows(protocol, label)}
            for label in ("tab:resultsbenchmark", "tab:resultsadaptation", "tab:resultsstructural")
        }

        self.assertTrue(snapshot["primary_estimates_available"])
        self.assertEqual(len(snapshot["cells"]), 15)
        self.assertEqual(sum(cell["cr1_missing"] for cell in snapshot["cells"]), 2)
        self.assertEqual(sum(cell["p10_open_reg_runs"] for cell in snapshot["cells"]), 1)
        self.assertIn("all 252 trajectories", protocol)
        for cell in snapshot["cells"]:
            identity = (models[cell["model"]], cell["arm"])
            with self.subTest(cell=identity):
                self.assertEqual(cell["allocated"], 21)
                self.assertEqual(cell["completed"], 21)
                coverage = tables["tab:resultsbenchmark"][identity]
                self.assertEqual(coverage[0], "21/21")
                self.assertAlmostEqual(float(coverage[1]), cell["p10_mean"], delta=0.005)
                self.assertEqual(int(coverage[2]), cell["p10_100_runs"])
                self.assertEqual(int(coverage[3]), cell["p10_open_reg_runs"])
                adaptation = tables["tab:resultsadaptation"][identity]
                self.assertEqual([int(value) for value in adaptation[:3]],
                                 [cell["cr1_pass"], cell["cr1_fail"], cell["cr1_missing"]])
                for value, field in zip(tables["tab:resultsstructural"][identity],
                                        ("ccn_over_10_pct", "dup_pct", "lint_per_kloc")):
                    self.assertAlmostEqual(float(value), cell[field], delta=0.005)

    def test_given_empirical_charts_when_checked_then_full_rasters_and_data_binding_match(self):
        payload = (ANC / "study-results-2026-11-15.json").read_bytes()
        expected_hash = hashlib.sha256(payload).hexdigest()
        sizes = {"fig-study-trajectories": (2880, 2400), "fig-study-outcomes-costs": (2880, 2940)}
        manifest = json.loads((ANC / "supplement-integration.json").read_text())
        bindings = manifest[manifest["current_figure_revision"]]
        previous = manifest["chart_interpretation_revision"]
        self.assertEqual(bindings["prior_figure_revision"], "chart_interpretation_revision")
        self.assertEqual(
            previous["source_sha256"]["anc/study-results-2026-11-15.json"], expected_hash
        )
        for name, digest in bindings["source_sha256"].items():
            self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(), digest)

        for stem, size in sizes.items():
            with self.subTest(chart=stem):
                svg = ET.fromstring((PACKAGE / f"{stem}.svg").read_bytes())
                self.assertEqual(svg.get("data-source-sha256"), expected_hash)
                png = (PACKAGE / f"{stem}.png").read_bytes()
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", png[16:24]), size)
                for extension in ("svg", "png"):
                    name = f"{stem}.{extension}"
                    self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(),
                                     bindings["charts"][name])

    def test_given_results_charts_at_sixteen_cm_when_read_then_all_text_is_at_least_seven_pt(self):
        manifest = json.loads((ANC / "supplement-integration.json").read_text())
        bindings = manifest[manifest["current_figure_revision"]]
        excluded_titles = {
            "fig-study-trajectories": "Mean Hidden-Test Pass Rate and Complexity Hotspots",
            "fig-study-outcomes-costs": "Complete 315/315 Benchmark Outcomes:",
        }
        for stem, title in excluded_titles.items():
            svg = ET.fromstring((PACKAGE / f"{stem}.svg").read_bytes())
            self.assertNotIn(title, " ".join(svg.itertext()))
            if stem == "fig-study-outcomes-costs":
                self.assertNotIn("Settled ledger:", " ".join(svg.itertext()))
            width = float(svg.get("width"))
            measured = []
            for node in svg.findall(".//{http://www.w3.org/2000/svg}text"):
                points = float(node.get("font-size")) * 16 / 2.54 * 72 / width
                with self.subTest(chart=stem, text=node.text):
                    self.assertGreaterEqual(points, 7)
                measured.append(points)
            self.assertAlmostEqual(min(measured), bindings["minimum_text_pt"][stem])

    def test_given_relaid_out_trajectories_when_plotted_then_all_source_points_are_preserved(self):
        data = json.loads((ANC / "study-results-2026-11-15.json").read_bytes())
        models = ["claude-sonnet-5.5", "gemini-4-argon", "gpt-6.1-sol"]
        maximum = math.ceil(max(
            point["share_ccn_over_10_pct"]
            for arms in data["series_means"].values()
            for points in arms.values() for point in points
        ))
        svg = ET.fromstring((PACKAGE / "fig-study-trajectories.svg").read_bytes())
        paths = {
            (node.get("data-model"), node.get("data-arm"), node.get("data-metric")): node
            for node in svg.findall(".//{http://www.w3.org/2000/svg}path")
        }
        self.assertEqual(set(paths), {
            (model, arm, metric) for model in models for arm in "ABCDE"
            for metric in ("pass_rate", "share_ccn_over_10_pct")
        })
        for (model, arm, metric), node in paths.items():
            y0, low, high = (145, 88, 100.5) if metric == "pass_rate" else (484, 0, maximum)
            actual = re.findall(r"[ML]([-\d.]+),([-\d.]+)", node.get("d"))
            source = data["series_means"][model][arm]
            self.assertEqual(len(actual), len(source))
            for (x, y), point in zip(actual, source):
                with self.subTest(model=model, arm=arm, metric=metric, k=point["k"]):
                    self.assertAlmostEqual(
                        float(x), 85 + models.index(model) * 300 + (point["k"] - 1) / 9 * 250,
                        delta=0.051,
                    )
                    self.assertAlmostEqual(
                        float(y), y0 + 180 - (point[metric] - low) / (high - low) * 180,
                        delta=0.051,
                    )

    def test_given_relaid_out_outcomes_when_plotted_then_estimates_counts_and_costs_are_preserved(self):
        data = json.loads((ANC / "study-results-2026-11-15.json").read_bytes())
        svg = ET.fromstring((PACKAGE / "fig-study-outcomes-costs.svg").read_bytes())
        ns = {"s": "http://www.w3.org/2000/svg"}
        forest = svg.findall(".//s:g[@data-contrast]", ns)
        self.assertEqual(len(forest), 11)
        for node in forest:
            model, contrast = node.get("data-model"), node.get("data-contrast")
            estimate = (data["pooled_contrasts"][contrast] if model == "pooled"
                        else data["within_model_contrasts"][model][contrast])
            value = (estimate["h1_pass_rate_diff_pct_points"] if model == "pooled"
                     else estimate["h1_diff"])
            interval = (estimate["h1_bootstrap_95_ci"] if model == "pooled"
                        else estimate["h1_ci"])
            point = node.find("s:circle", ns)
            whisker = node.find("s:line", ns)
            self.assertAlmostEqual(float(point.get("cx")), 215 + (value + 3.8) / 14.4 * 215)
            self.assertAlmostEqual(float(whisker.get("x1")), 215 + (interval[0] + 3.8) / 14.4 * 215)
            self.assertAlmostEqual(float(whisker.get("x2")), 215 + (interval[1] + 3.8) / 14.4 * 215)
        bars = {
            (node.get("data-model"), node.get("data-arm")): node
            for node in svg.findall(".//s:g[@data-metric='cr1']", ns)
        }
        points = {
            (node.get("data-model"), node.get("data-arm")): node
            for node in svg.findall(".//s:circle[@data-metric='cost-coverage']", ns)
        }
        identities = {(cell["model"], cell["arm"]) for cell in data["cells"]}
        self.assertEqual(set(bars), identities)
        self.assertEqual(set(points), identities)
        models = ["claude-sonnet-5.5", "gemini-4-argon", "gpt-6.1-sol"]
        for cell in data["cells"]:
            key = cell["model"], cell["arm"]
            start = 590
            for field in ("cr1_pass", "cr1_fail", "cr1_missing"):
                rect = bars[key].find(f"s:rect[@data-outcome='{field}']", ns)
                if not cell[field]:
                    self.assertIsNone(rect)
                    continue
                self.assertAlmostEqual(float(rect.get("x")), start)
                self.assertAlmostEqual(float(rect.get("width")), cell[field] / 21 * 340)
                start += cell[field] / 21 * 340
            self.assertAlmostEqual(float(points[key].get("cx")),
                85 + models.index(cell["model"]) * 300 + (cell["delivery_credits_mean"] - 35) / 290 * 250)
            self.assertAlmostEqual(float(points[key].get("cy")),
                800 - (cell["p10_mean"] - 90.5) / 9.9 * 200)
        labels = {"".join(node.itertext()) for node in svg.findall(".//s:text", ns)}
        for model in models:
            counts = " ".join(
                f"{cell['arm']}[{cell['delivery_credits_n']}]"
                for cell in data["cells"] if cell["model"] == model
            )
            self.assertIn(f"n: {counts}", labels)

    def test_given_chart_generator_when_run_then_layout_checks_pass_without_changing_data(self):
        source = (ANC / "study-results-2026-11-15.json").read_bytes()
        with tempfile.TemporaryDirectory(prefix=".paper-charts-", dir=ANC) as directory:
            result = subprocess.run(
                ["node", str(ANC / "export_results_charts.mjs"), directory],
                capture_output=True, text=True, check=False, timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.count("no clipped or overlapping text"), 2)
            for stem in ("fig-study-trajectories", "fig-study-outcomes-costs"):
                self.assertEqual(
                    (Path(directory) / f"{stem}.svg").read_bytes(),
                    (PACKAGE / f"{stem}.svg").read_bytes(),
                )
                self.assertEqual(
                    (Path(directory) / f"{stem}.png").read_bytes()[16:24],
                    (PACKAGE / f"{stem}.png").read_bytes()[16:24],
                )
        self.assertEqual((ANC / "study-results-2026-11-15.json").read_bytes(), source)

    def test_given_chart_reading_cues_when_rendered_then_directions_and_limits_are_explicit(self):
        cues = {
            "fig-study-trajectories": ("Higher pass rate is better", "Lower is better", "21-run means"),
            "fig-study-outcomes-costs": (
                "Right of 0 favors first arm", "CI includes 0: direction uncertain",
                "More passes is better; grey is unknown", "Up = more coverage; left = fewer credits",
                "Prefer upper-left at comparable outcomes", "Coverage uses all 21",
            ),
        }

        for stem, expected in cues.items():
            text = " ".join(ET.fromstring((PACKAGE / f"{stem}.svg").read_bytes()).itertext())
            for cue in expected:
                with self.subTest(chart=stem, cue=cue):
                    self.assertIn(cue, text)
        protocol = " ".join((ANC / "experiment-protocol.tex").read_text().split())
        self.assertIn("contract sets expand across cycles", protocol)
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        self.assertIn("treating cheap failure as efficiency", manuscript)
        self.assertIn("95\\% bootstrap intervals", protocol)

    def test_given_full_identifiers_when_read_then_register_is_unique_linked_and_last(self):
        from check_paper import expand_inputs

        source = expand_inputs((PACKAGE / "main.tex").read_text())
        narrative, register = source.split(r"\section{Source and digest register}", 1)
        records = read_source_register()
        labels = re.findall(r"\\label\{prov:(R\d+)\}", register)
        digests = re.findall(r"(?<![0-9a-f])(?:[0-9a-f]{64}|[0-9a-f]{40})(?![0-9a-f])", register)
        targets = set(re.findall(r"\\sourceref\{(R\d+)\}", source))
        bindings = json.loads((ANC / "supplement-integration.json").read_text())
        final_results = bindings["final_results_revision"]

        self.assertEqual(set(labels), {f"R{index:02}" for index in range(1, 62)})
        self.assertEqual(len(labels), len(records))
        self.assertEqual(len(digests), len(set(digests)))
        self.assertEqual(set(digests), set(records.values()))
        self.assertFalse(targets - records.keys())
        self.assertNotRegex(narrative, r"(?<![0-9a-f])(?:[0-9a-f]{64}|[0-9a-f]{40})(?![0-9a-f])")
        self.assertRegex(register, r"\\end\{longtable\}\s*\\endgroup\s*\\end\{document\}")
        for record, expected in {
            "R17": final_results["results_main_commit"],
            "R19": final_results["experiment_results_report_git_blob"],
            "R20": final_results["experiment_results_report_sha256"],
            "R26": final_results["study_state_sha256"],
            "R27": final_results["intervention_manifest_sha256"],
            "R35": bindings["literal_inputs"]["anc/consolidation-frozen-v4.prompt.txt"],
            "R60": PROMPTS["consolidation-active-e71037d9.prompt.txt"][0],
            "R61": PROMPTS["review-only-active-e71037d9.prompt.txt"][0],
        }.items():
            with self.subTest(record=record):
                self.assertEqual(records[record], expected)

    def test_given_results_when_read_then_arm_checkpoint_and_uncertainty_context_is_local(self):
        protocol = (ANC / "experiment-protocol.tex").read_text()
        manuscript = " ".join((PACKAGE / "main.tex").read_text().split())
        prose = " ".join(protocol.split())
        tables = re.findall(r"\\begin\{table\}.*?\\end\{table\}", protocol, re.DOTALL)

        for label in ("tab:resultsbenchmark", "tab:resultsadaptation", "tab:resultsstructural", "tab:resultscosts"):
            table = next(table for table in tables if f"\\label{{{label}}}" in table)
            with self.subTest(table=label):
                self.assertIn(r"\armlegend", table)
        self.assertIn("final ten-feature repository before the withheld extension", prose)
        self.assertIn("acquisition of a new feature from retention", prose)
        supplement = " ".join((ANC / "measurement-provenance.tex").read_text().split())
        self.assertIn("assigned first to failure and then to success", supplement)
        self.assertIn("sampling uncertainty", supplement)
        self.assertIn("prospectively registered study", manuscript)
        self.assertIn("until its design and resources are approved", manuscript)
        self.assertNotIn("those options execution", manuscript)

if __name__ == "__main__":
    unittest.main()
