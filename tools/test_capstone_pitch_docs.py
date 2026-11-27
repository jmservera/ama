"""Regression checks for the capstone pitch documents (issue #435)."""

from __future__ import annotations

import importlib.util
import json
import os
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
        CAPSTONE / "demo" / "runbook.md",
        CAPSTONE / "source" / "README.md",
        CAPSTONE / "source" / "review-2026-11-27.md",
    ]


class CapstonePitchDocsTest(unittest.TestCase):
    def test_demo_first_script_embeds_runbook_and_uses_manifest_route(self) -> None:
        manifest = json.loads((CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8"))
        route = manifest["presentation_route"]
        script = (CAPSTONE / "pitch" / "speaker-script.md").read_text(encoding="utf-8")
        runbook = (CAPSTONE / "demo" / "runbook.md").read_text(encoding="utf-8")
        self.assertEqual(
            900,
            sum(step["seconds"] for step in route["steps"])
            + route["demo_seconds"]
            + route["reserve_seconds"],
        )
        self.assertGreaterEqual(route["reserve_seconds"], 120)
        self.assertEqual(["S01", "S22"], [step["code"] for step in route["steps"][:2]])
        self.assertEqual("S23", route["steps"][-1]["code"])
        for step in route["steps"]:
            self.assertIn("SAY: " + step["say"], script)
        # Rebase relative demo links before comparing the entire embedded text.
        body = re.sub(r"\A---\n.*?\n---\n", "", runbook, count=1, flags=re.DOTALL)

        def relative(match: re.Match[str]) -> str:
            target = match.group(1)
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#|/", target):
                return match.group(0)
            path, marker, fragment = target.partition("#")
            absolute = (CAPSTONE / "demo" / path).resolve()
            result = os.path.relpath(absolute, CAPSTONE / "pitch")
            return "](" + result + (marker + fragment if marker else "") + ")"

        body = re.sub(r"\]\(([^)]+)\)", relative, body)
        self.assertIn(body.strip(), script)
        hook = re.search(r"(?ms)^## Executive Hook\n(.*?)(?=^## |\Z)", body)
        self.assertIsNotNone(hook)
        demo = script.split("### 00:30-02:20", 1)[1].split("### 02:20-", 1)[0]
        self.assertIn(hook.group(1).strip(), demo)
        self.assertIn("00:30-02:20", script)
        self.assertIn("12:10-15:00", script)

    def test_pitch_custom_show_matches_delivered_slide_order(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads((CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8"))
        namespace = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        }
        with zipfile.ZipFile(CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx") as archive:
            presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
            children = [node.tag for node in presentation]
            self.assertLess(
                children.index(f"{{{namespace['p']}}}custShowLst"),
                children.index(f"{{{namespace['p']}}}defaultTextStyle"),
            )
            relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
            targets = {node.attrib["Id"]: node.attrib["Target"] for node in relationships}
            slides = {slide["code"]: slide["part_number"] for slide in manifest["slides"]}
            show = presentation.find("p:custShowLst/p:custShow", namespace)
            self.assertIsNotNone(show)
            self.assertEqual(manifest["presentation_route"]["name"], show.attrib["name"])
            actual = [
                targets[node.attrib[f"{{{namespace['r']}}}id"]]
                for node in show.findall("p:sldLst/p:sld", namespace)
            ]
            expected = [
                f"slides/slide{slides[step['code']]}.xml"
                for step in manifest["presentation_route"]["steps"]
            ]
            self.assertEqual(expected, actual)
            properties = ET.fromstring(archive.read("ppt/presProps.xml"))
            self.assertEqual(
                show.attrib["id"], properties.find("p:showPr/p:custShow", namespace).attrib["id"]
            )
            self.assertEqual(56, len(presentation.findall("p:sldIdLst/p:sldId", namespace)))
            notes = archive.read("ppt/notesSlides/notesSlide56.xml").decode()
            self.assertIn("2,522", notes)
            self.assertIn("not a billing record", notes)

    def test_relative_links_resolve(self) -> None:
        broken = []
        for doc in pitch_documents():
            for target in LINK.findall(doc.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+:", target):
                    continue
                if not (doc.parent / target).resolve().exists():
                    broken.append(f"{doc.relative_to(ROOT)} -> {target}")
        self.assertEqual([], broken)

    def test_revised_appendix_navigation_matches_physical_pages(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads((CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8"))
        slides = {slide["code"]: slide for slide in manifest["slides"]}
        questions = (CAPSTONE / "pitch" / "questions-and-answers.md").read_text(encoding="utf-8")
        with zipfile.ZipFile(CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx") as archive:
            for code, topic in (("B03", "S08"), ("B06", "S12"), ("B13", "S19")):
                with self.subTest(code=code):
                    slide = slides[code]
                    notes = ET.fromstring(
                        archive.read(f"ppt/notesSlides/notesSlide{slide['part_number']}.xml")
                    )
                    navigation = next(
                        node.text
                        for node in notes.iter(
                            "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
                        )
                        if node.text and node.text.startswith("NAVIGATION:")
                    )
                    for target in (
                        f"{code}/page {slide['number']}",
                        f"index {slides['QX']['number']}",
                        f"fixed Topic {topic}/page {slides[topic]['number']}",
                    ):
                        self.assertIn(target, navigation)
                        self.assertIn(target, questions)

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


if __name__ == "__main__":
    unittest.main()
