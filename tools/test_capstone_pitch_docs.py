"""Regression checks for the capstone pitch documents (issue #435)."""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "docs" / "capstone"
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def pitch_documents() -> list[Path]:
    return sorted(CAPSTONE.joinpath("pitch").glob("*.md")) + [
        CAPSTONE / "tokenomics-qa-brief.md",
        CAPSTONE / "README.md",
    ]


class CapstonePitchDocsTest(unittest.TestCase):
    def test_relative_links_resolve(self) -> None:
        broken = []
        for doc in pitch_documents():
            for target in LINK.findall(doc.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+:", target):
                    continue
                if not (doc.parent / target).resolve().exists():
                    broken.append(f"{doc.relative_to(ROOT)} -> {target}")
        self.assertEqual([], broken)

    def test_placement_draft_status_matches_delivered_artifacts(self) -> None:
        rows = {}
        draft = CAPSTONE / "pitch" / "tokenomics-placement-draft.md"
        for line in draft.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\| ([1-6]) [A-Z][^|]*\| (.*) \|$", line)
            if match:
                rows[match.group(1)] = match.group(2)
        self.assertEqual(set("123456"), set(rows))
        self.assertIn("capstone-assessment-challenge.md", rows["5"])
        self.assertIn("current-deck-assessment-2026-11-12.md", rows["6"])
        self.assertNotIn("No revised deck exists", rows["5"])
        # Criterion 3 stays open while the rehearsal record is blank.
        notes = (CAPSTONE / "pitch" / "tokenomics-rehearsal-notes.md").read_text(encoding="utf-8")
        record = notes.split("## Rehearsal Record", 1)[1]
        if re.search(r"\| Date and presenter \| *\|", record):
            self.assertIn("rehearsal-notes.md", rows["3"])
            self.assertIn("blank", rows["3"])

    def test_deck_placement_matches_owner_decision(self) -> None:
        pptx = importlib.util.find_spec("pptx")
        if pptx is None:
            self.skipTest("python-pptx is not installed")
        from pptx import Presentation

        deck = Presentation(str(CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx"))

        def text(number: int) -> str:
            shapes = deck.slides[number - 1].shapes
            return "\n".join(s.text_frame.text for s in shapes if s.has_text_frame)

        main, cfo, cto = text(22), text(53), text(55)
        self.assertIn("Measure accepted value", main)
        self.assertIn("E21", main)
        self.assertIn("E19", main)
        self.assertIn("#435 not accepted", main)
        self.assertIn("B25", cfo)
        self.assertIn("Tokenomics", cfo)
        self.assertIn("B27", cto)
        # Every figure is a labelled planning scenario, never a price, saving or payback claim.
        self.assertIn("INFERENCE PLANNING SCENARIO", main)
        self.assertIn("not current verified price", main)
        self.assertIn("accepted-outcome TCA unknown", cfo)

    def test_measured_batch_stays_within_recorded_authority(self) -> None:
        folder = ROOT / "docs/reference/research/evaluation/heldout-batch-432-live-2026-11-18"
        auth = json.loads((folder / "authorization.json").read_text(encoding="utf-8"))
        report = json.loads((folder / "report-live.json").read_text(encoding="utf-8"))
        self.assertTrue(auth["approved_by"] and auth["authority_ref"])
        self.assertEqual("completed", report["outcome"])
        self.assertEqual("measured held-out batch", report["evidence_label"])
        self.assertEqual(auth["authority_ref"], report["spend_authority_ref"])
        self.assertLessEqual(report["calls"], auth["max_calls"])
        self.assertLessEqual(report["tokens"]["total"], auth["max_total_tokens"])
        self.assertLessEqual(Decimal(report["accrued_usd"]), Decimal(auth["max_budget_usd"]))
        self.assertEqual(report["calls"], len(report["rows"]))

    def test_spoken_scripts_do_not_say_the_batch_has_not_run(self) -> None:
        for doc in (
            CAPSTONE / "tokenomics-qa-brief.md",
            CAPSTONE / "pitch" / "tokenomics-rehearsal-notes.md",
        ):
            text = " ".join(doc.read_text(encoding="utf-8").split())
            for stale in ("authorised but not run", "not yet run live", "That batch has not run"):
                self.assertNotIn(stale, text, f"{doc.name}: {stale}")

    def test_rehearsal_route_arithmetic_matches_the_stated_totals(self) -> None:
        notes = (CAPSTONE / "pitch" / "tokenomics-rehearsal-notes.md").read_text(encoding="utf-8")
        row = re.compile(
            r"^\| [\d, to]+ \| ([^|]+)\| (\d+|n/a) \| (\d+) \| (\d\d):(\d\d)-(\d\d):(\d\d) \|",
            re.MULTILINE,
        )
        rows = row.findall(notes)
        self.assertEqual(25, len(rows))
        previous_end = 0
        for name, _, slot, start_m, start_s, end_m, end_s in rows:
            start = int(start_m) * 60 + int(start_s)
            end = int(end_m) * 60 + int(end_s)
            self.assertEqual(previous_end, start, name)
            self.assertEqual(int(slot), end - start, name)
            previous_end = end
        self.assertEqual(900, previous_end)
        self.assertEqual(1470, sum(int(r[1]) for r in rows if r[1] != "n/a"))
        self.assertEqual(840, sum(int(r[2]) for r in rows[:-1]))
        self.assertEqual(60, int(rows[-1][2]))
        slide22 = next(r for r in rows if r[0].startswith("S18 Tokenomics"))
        self.assertEqual("20", slide22[2])

    def test_model_tier_comparison_is_dated_sourced_and_makes_no_saving_claim(self) -> None:
        text = " ".join(
            (CAPSTONE / "pitch" / "tokenomics-model-tier-comparison.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("retrieved 2026-11-24", text)
        for source in (
            "omg.org/spec/DMN",
            "developers.openai.com/api/docs/pricing",
            "model-router",
        ):
            self.assertIn(source, text)
        self.assertIn("not a saving", text)
        self.assertIn("Cost per accepted outcome | Unknown | Unknown | Unknown", text)

    def test_cost_per_home_figures_follow_from_their_stated_inputs(self) -> None:
        text = (CAPSTONE / "pitch" / "tokenomics-cost-per-home-vs-value.md").read_text(
            encoding="utf-8"
        )
        per_home = Decimal(275_360) * Decimal("1.60") / Decimal(1_000_000)
        derived = {
            "0.440576": per_home,
            "6,872.9856": per_home * 15_600,
            "0.881152": per_home * 2,
            "47,439,600": Decimal(3041) * 15_600,
            "210.17": (Decimal(2522) / 12).quantize(Decimal("0.01")),
        }
        for quoted, value in derived.items():
            self.assertIn(quoted, text)
            self.assertEqual(Decimal(quoted.replace(",", "")), value, quoted)

    def test_cost_per_home_page_keeps_gaps_unknown_and_claims_out(self) -> None:
        text = (CAPSTONE / "pitch" / "tokenomics-cost-per-home-vs-value.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("No saving, payback or return can be stated", text)
        lines = text.splitlines()
        for row in ("Measured cost per home", "Settled cost per home", "Time saved"):
            line = next(ln for ln in lines if ln.startswith(f"| {row}"))
            self.assertIn("Unknown", line, row)


if __name__ == "__main__":
    unittest.main()
