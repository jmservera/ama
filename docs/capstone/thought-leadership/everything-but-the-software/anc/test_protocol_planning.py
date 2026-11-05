"""Reproduce the active protocol's conditional planning and resource tables."""

import json
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

from check_paper import strip_comments

PACKAGE = Path(__file__).resolve().parent.parent
MODELS = 3
ALLOCATIONS = (12, 21, 33)
CYCLES = 10
CHANGE_REQUEST = (45, 300)
ARM_SESSIONS = {
    "A": ((30, 300),),
    "B": ((30, 300), (15, 300)),
    "C": ((30, 300), (15, 300)),
    "D": ((45, 600),),
    "E": ((30, 300), (15, 300)),
}


def table_rows(source: str, label: str) -> list[list[str]]:
    tables = [
        table for table in re.findall(
            r"\\begin\{table\}(?:\[[^]]*\])?(.*?)\\end\{table\}", source, re.S
        ) if f"\\label{{{label}}}" in table
    ]
    if len(tables) != 1:
        raise AssertionError(f"Expected one active table labelled {label}")
    body = tables[0].split(r"\midrule", 1)[1].split(r"\bottomrule", 1)[0]
    return [
        [cell.strip() for cell in row.strip().split("&")]
        for row in body.split(r"\\") if row.strip()
    ]


def numeric_cell(cell: str) -> Fraction:
    plain = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", cell)
    plain = plain.removesuffix(" (default allocation)").replace(",", "").strip()
    return Fraction(plain)


def resources(n: int) -> dict[str, Fraction]:
    calibration_sessions = MODELS * CYCLES * sum(
        len(sessions) for sessions in ARM_SESSIONS.values()
    )
    calibration_minutes = MODELS * CYCLES * sum(
        minutes for sessions in ARM_SESSIONS.values() for minutes, _ in sessions
    )
    calibration_credits = MODELS * CYCLES * sum(
        credits for sessions in ARM_SESSIONS.values() for _, credits in sessions
    )
    trajectories = MODELS * len(ARM_SESSIONS)
    study_sessions = n * (calibration_sessions + trajectories)
    study_minutes = n * (calibration_minutes + trajectories * CHANGE_REQUEST[0])
    study_credits = n * (calibration_credits + trajectories * CHANGE_REQUEST[1])
    return {
        "Study trajectories per arm, all models": Fraction(MODELS * n),
        "Study trajectories, all arms": Fraction(trajectories * n),
        "Study sessions, including CR1": Fraction(study_sessions),
        "Study maximum agent-hours": Fraction(study_minutes, 60),
        "Study nominal session credits": Fraction(study_credits),
        "Excluded calibration trajectories, no CR1": Fraction(trajectories),
        "Excluded calibration sessions": Fraction(calibration_sessions),
        "Calibration maximum agent-hours": Fraction(calibration_minutes, 60),
        "Calibration nominal session credits": Fraction(calibration_credits),
        "Combined trajectories": Fraction(trajectories * (n + 1)),
        "Combined sessions": Fraction(study_sessions + calibration_sessions),
        "Combined maximum agent-hours": Fraction(
            study_minutes + calibration_minutes, 60
        ),
        "Combined nominal session credits": Fraction(
            study_credits + calibration_credits
        ),
    }


class ProtocolPlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.protocol = strip_comments(
            (PACKAGE / "anc/experiment-protocol.tex").read_text(encoding="utf-8")
        )
        cls.manuscript = strip_comments(
            (PACKAGE / "main.tex").read_text(encoding="utf-8")
        )

    def test_given_arm_schedules_when_compared_then_declared_ceilings_match(self) -> None:
        rows = table_rows(self.protocol, "tab:protocolsummary")
        self.assertEqual(len(rows), len(ARM_SESSIONS))
        for row, (arm, sessions) in zip(rows, ARM_SESSIONS.items()):
            with self.subTest(arm=arm):
                self.assertEqual(row[0].split()[0], arm)
                self.assertEqual(
                    [int(value) for value in re.findall(r"\d+", row[2])],
                    [minutes for minutes, _ in sessions]
                    + [credits for _, credits in sessions],
                )

    def test_given_allocation_choices_when_totaled_then_all_39_resource_cells_match(self) -> None:
        rows = table_rows(self.protocol, "tab:pilotresources")
        expected = [resources(n) for n in ALLOCATIONS]
        self.assertEqual([row[0] for row in rows], list(expected[0]))
        for row in rows:
            self.assertEqual(len(row), 1 + len(ALLOCATIONS))
            for column, n in enumerate(ALLOCATIONS, 1):
                with self.subTest(quantity=row[0], n=n):
                    self.assertEqual(
                        numeric_cell(row[column]), expected[column - 1][row[0]]
                    )

    def test_given_assumed_sds_when_sized_then_conditional_planning_rows_match(self) -> None:
        rows = table_rows(self.protocol, "tab:replicationchoices")
        self.assertEqual(len(rows), len(ALLOCATIONS))
        quantiles = NormalDist().inv_cdf(0.975) + NormalDist().inv_cdf(0.80)
        for row, sd, n in zip(rows, (15, 20, 25), ALLOCATIONS):
            with self.subTest(sd=sd):
                minimum = math.ceil(2 * quantiles**2 * sd**2 / (MODELS * 10**2))
                self.assertEqual(numeric_cell(row[0]), sd)
                self.assertEqual(numeric_cell(row[1]), minimum)
                self.assertEqual(minimum, n)
        equation = (
            r"\frac{2(z_{1-\alpha/2}+z_{1-\beta})^2\sigma^2}"
            r"{M\Delta_*^2}"
        )
        self.assertIn(equation, re.sub(r"\s+", "", self.protocol))

    def test_given_default_n_and_sd_25_when_planned_then_power_is_below_80_percent(self) -> None:
        normal = NormalDist()
        standard_error = math.sqrt(2 * 25**2 / (MODELS * ALLOCATIONS[0]))
        critical = normal.inv_cdf(0.975)
        shift = 10 / standard_error
        power = 1 - normal.cdf(critical - shift) + normal.cdf(-critical - shift)
        self.assertAlmostEqual(power, 0.396438, places=6)
        self.assertLess(power, 0.80)

    def test_given_session_caps_when_totaled_then_no_allocation_fits_the_envelope(self) -> None:
        prose = " ".join(self.protocol.split())
        self.assertIn("aggregate envelope remains 300,000 AI credits", prose)
        self.assertIn("270,000-credit local admission ceiling", prose)
        for n in ALLOCATIONS:
            with self.subTest(n=n):
                self.assertGreater(
                    resources(n)["Combined nominal session credits"], 300_000
                )

    def test_given_matched_ceilings_when_compared_then_session_structure_stays_distinct(self) -> None:
        b, d = ARM_SESSIONS["B"], ARM_SESSIONS["D"]
        self.assertEqual(sum(minutes for minutes, _ in b), sum(minutes for minutes, _ in d))
        self.assertEqual(sum(credits for _, credits in b), sum(credits for _, credits in d))
        self.assertNotEqual(len(b), len(d))
        self.assertIn("D also has fewer fresh sessions", self.protocol)

    def test_given_selected_allocation_when_rendered_then_abstract_and_native_labels_agree(self) -> None:
        abstract = self.manuscript.split(r"\begin{abstract}", 1)[1].split(
            r"\end{abstract}", 1
        )[0]
        self.assertIn("12 (default), 21 or 33", " ".join(abstract.split()))
        labels = {}
        for stem in ("fig-pilot-design", "fig-experiment-measures"):
            scene = json.loads((PACKAGE / f"{stem}.excalidraw").read_text())
            labels[stem] = "\n".join(
                element["text"] for element in scene["elements"]
                if element["type"] == "text"
            )
        self.assertIn("Default: 180 trajectories", labels["fig-pilot-design"])
        for text in labels.values():
            self.assertIn("12 (default), 21 or 33 trajectories per model per arm", text)

    def test_given_current_kit_source_when_described_then_capability_and_reporting_limits_agree(self) -> None:
        availability = self.manuscript.split(r"\section*{Data availability}", 1)[1]
        for marker in (
            "protocol-frozen-v6",
            "5ab24be4556876500a40e56201f6efc3930cc8b8",
            "7de2f0d42955c62b52906747de480df2b3f1e0ca",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, availability)
        self.assertNotIn("only A/B/C are implemented", availability)
        prose = " ".join(self.protocol.split())
        self.assertNotIn("implements only A/B/C", prose)
        for marker in (
            "prospective reporting requirements",
            "candidate independent-cell analysis",
            "scheduling label alone",
            "forecast and approval are required separately",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, prose)
        for stem, marker in (
            ("fig-pilot-design", "V6 implements A-E"),
            ("fig-experiment-measures", "F9/F10 strata (planned)"),
        ):
            scene = json.loads((PACKAGE / f"{stem}.excalidraw").read_text())
            text = "\n".join(
                element["text"] for element in scene["elements"]
                if element["type"] == "text"
            )
            self.assertIn(marker, text)

    def test_given_cost_sensitivity_when_evaluated_then_all_nine_cells_match(self) -> None:
        rows = table_rows(self.manuscript, "tab:costscenario")
        self.assertEqual(len(rows), 3)
        for row, delta in zip(rows, (Fraction(0), Fraction(1, 2), Fraction(1))):
            self.assertEqual(len(row), 4)
            for cell, cycles in zip(row[1:], (10, 20, 40)):
                with self.subTest(delta=delta, cycles=cycles):
                    expected = delta * cycles * (cycles - 1) / 2 - 5 * cycles
                    self.assertEqual(numeric_cell(cell), expected)

    def test_given_positive_cost_parameters_when_rounded_then_break_even_is_discrete(self) -> None:
        for investment, delta, expected in (
            (5, Fraction(1, 2), 21), (5, Fraction(1), 11), (100, Fraction(1), 201)
        ):
            with self.subTest(investment=investment, delta=delta):
                first = math.ceil(1 + 2 * investment / delta)
                self.assertEqual(first, expected)
                for cycles, nonnegative in ((first - 1, False), (first, True)):
                    net = delta * cycles * (cycles - 1) / 2 - investment * cycles
                    self.assertEqual(net >= 0, nonnegative)
        for cycles in (1, 10, 40, 201):
            self.assertLess(Fraction(0) * cycles * (cycles - 1) / 2 - 5 * cycles, 0)


if __name__ == "__main__":
    unittest.main()
