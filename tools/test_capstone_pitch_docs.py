"""Regression checks for the capstone pitch documents (issue #435)."""

from __future__ import annotations

import hashlib
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
        manifest = json.loads(
            (CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8")
        )
        route = manifest["presentation_route"]
        script = (CAPSTONE / "pitch" / "speaker-script.md").read_text(encoding="utf-8")
        runbook = (CAPSTONE / "demo" / "runbook.md").read_text(encoding="utf-8")
        receipt = json.loads((CAPSTONE / "source/validation.json").read_text())
        canonical = (
            (CAPSTONE / "demo/runbook.md")
            .read_bytes()
            .replace(b"\r\n", b"\n")
            .replace(b"\r", b"\n")
        )
        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(), receipt["pitch"]["runbook_sha256"]
        )
        self.assertEqual(
            900,
            sum(step["seconds"] for step in route["steps"])
            + route["demo_seconds"]
            + route["reserve_seconds"],
        )
        prepared = route["slot_seconds"] - route["reserve_seconds"]
        reserve = route["reserve_seconds"]
        allocation = (
            f"{prepared // 60}:{prepared % 60:02} prepared narration/demo and "
            f"{reserve // 60}:{reserve % 60:02} questions/recovery."
        )
        self.assertIn(allocation, runbook)
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
        self.assertIn(f"{prepared // 60:02}:{prepared % 60:02}-15:00", script)

    def test_privacy_and_responsible_ai_are_visible_on_the_main_route(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads((CAPSTONE / "source/slides.json").read_text())
        slides = {slide["code"]: slide for slide in manifest["slides"]}
        spoken = {
            step["code"]: step["say"]
            for step in manifest["presentation_route"]["steps"]
        }
        expected = {
            "S01": ("Not-for-profit", "resident benefit"),
            "S11A": ("UK processing is the target", "Proof comes before release"),
            "S15": ("Responsible AI", "NAMED HUMAN REVIEW"),
            "S17": ("UK GDPR", "retention", "rights", "Legal/DPO approval"),
        }
        with zipfile.ZipFile(
            CAPSTONE / "deck/zava-forward-cowork-v2-draft.pptx"
        ) as deck:
            for code, phrases in expected.items():
                self.assertIn(code, spoken)
                page = ET.fromstring(
                    deck.read(f"ppt/slides/slide{slides[code]['part_number']}.xml")
                )
                visible = " ".join(
                    node.text or ""
                    for node in page.iter(
                        "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
                    )
                )
                for phrase in phrases:
                    self.assertIn(phrase, visible)
        self.assertIn("before anything affects a resident", spoken["S15"])
        self.assertIn("Works consent is separate", spoken["S17"])
        self.assertIn("release criteria", spoken["S15"])
        self.assertIn("synthetic demo", spoken["S15"])

    def test_uk_target_and_model_price_scope_do_not_claim_live_residency(self) -> None:
        from pptx import Presentation

        manifest = json.loads((CAPSTONE / "source/slides.json").read_text())
        spoken = {
            step["code"]: step["say"]
            for step in manifest["presentation_route"]["steps"]
        }
        self.assertIn("proposed boundary", spoken["S11A"])
        self.assertIn("Standard-model inference", spoken["S11A"])
        self.assertIn("doesn't prove a UK-only deployment", spoken["S11A"])
        self.assertIn("Identity, provider access and backups", spoken["S11A"])
        self.assertIn("UK-only model choice needs repricing", spoken["B28"])
        cost_page = next(
            slide["number"] - 1
            for slide in manifest["slides"]
            if slide["code"] == "B28"
        )
        copy = "\n".join(
            shape.text
            for shape in Presentation(
                CAPSTONE / "deck/zava-forward-cowork-v2-draft.pptx"
            )
            .slides[cost_page]
            .shapes
            if shape.has_text_frame
        )
        self.assertIn("Global nano is not a UK-resident rate", copy)
        runbook = (CAPSTONE / "demo/runbook.md").read_text()
        self.assertIn("UK Standard-model inference", runbook)
        self.assertIn("UK GDPR permits safeguarded international transfers", runbook)

    def test_full_azure_cost_arithmetic_and_delivery_binding(self) -> None:
        model_path = CAPSTONE / "source" / "azure-cost-model-2026-11-27.json"
        model = json.loads(model_path.read_text(encoding="utf-8"))
        manifest = json.loads(
            (CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8")
        )
        cost_slide = next(
            slide for slide in manifest["slides"] if slide["code"] == "B28"
        )
        copy = "\n".join(item.get("text", "") for item in cost_slide["elements"])
        for column in ("low", "high"):
            total = sum(
                Decimal(row["rate_usd"]) * Decimal(row[f"{column}_quantity"])
                for row in model["components"]
            )
            self.assertEqual(total, Decimal(model["totals_usd"][column]))
            displayed = model["display"]["monthly"].removeprefix("USD ").split("-")
            self.assertLess(
                abs(total - Decimal(displayed[column == "high"].replace(",", ""))), 5
            )
        persistent = sum(
            Decimal(row["rate_usd"]) * Decimal(row["low_quantity"])
            for row in model["components"]
            if row["category"] == "persistent"
        )
        self.assertEqual(persistent, Decimal(model["totals_usd"]["persistent"]))
        self.assertIn(model["display"]["persistent"], copy)
        self.assertIn(model["display"]["monthly"], copy)
        self.assertEqual(
            Decimal(model["ai_policy"]["aggregate_monthly_usd"]),
            Decimal(
                next(row for row in model["components"] if row["id"] == "model-usage")[
                    "high_quantity"
                ]
            ),
        )
        for attempt in model["ai_request"]["models"]:
            maximum = (
                (
                    Decimal(attempt["input_usd_per_1000"])
                    * model["ai_request"]["max_provider_input_tokens"]
                    + Decimal(attempt["output_usd_per_1000"])
                    * model["ai_request"]["max_output_tokens"]
                )
                / 1000
                * model["ai_request"]["max_attempts"]
            )
            self.assertEqual(maximum, Decimal(attempt["attempt_ceiling_usd"]))
            self.assertIn(
                attempt["attempt_ceiling_usd"],
                "\n".join(
                    next(
                        slide for slide in manifest["slides"] if slide["code"] == "B27"
                    )["revised_notes"]
                ),
            )
        receipt = json.loads(
            (CAPSTONE / "source" / "validation.json").read_text(encoding="utf-8")
        )
        canonical = (
            model_path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        )
        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(),
            receipt["source_verification"]["azure_cost_model_sha256"],
        )

    def test_priority_budget_arithmetic_and_spoken_route(self) -> None:
        model = json.loads(
            (CAPSTONE / "source" / "azure-cost-model-2026-11-27.json").read_text(
                encoding="utf-8"
            )
        )
        policy = model["ai_policy"]
        pools = {pool["id"]: pool for pool in policy["pools"]}
        self.assertEqual(len(pools), len(policy["pools"]))
        for period in ("daily", "monthly"):
            ceiling = Decimal(policy[f"aggregate_{period}_usd"])
            allocations = [Decimal(pool[f"{period}_usd"]) for pool in pools.values()]
            self.assertLessEqual(sum(allocations), ceiling)
            priority = sum(
                Decimal(pools[name][f"{period}_usd"])
                for name in ("recommendations", "document-judging")
            )
            after_chat = ceiling - Decimal(pools["chat"][f"{period}_usd"])
            self.assertGreaterEqual(after_chat, priority)
        period_maximum = sum(
            min(
                Decimal(pool["daily_usd"]) * model["month_days"],
                Decimal(pool["monthly_usd"]),
            )
            for pool in pools.values()
        )
        self.assertLessEqual(period_maximum, Decimal(policy["aggregate_monthly_usd"]))
        manifest = json.loads(
            (CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8")
        )
        codes = [step["code"] for step in manifest["presentation_route"]["steps"]]
        self.assertEqual(
            ["B28", "B27", "S18"], codes[codes.index("B28") : codes.index("B28") + 3]
        )
        script = (CAPSTONE / "pitch" / "speaker-script.md").read_text(encoding="utf-8")
        self.assertIn("Chat cannot borrow the protected business allocations.", script)
        self.assertIn("unknown liability, safety or aggregate holds", script)
        questions = (CAPSTONE / "pitch" / "questions-and-answers.md").read_text(
            encoding="utf-8"
        )
        for text in (
            model["display"]["monthly"],
            "maximum Azure bill",
            "not spending authority",
            "cannot consume",
            "scheduled jobs",
            "S3",
        ):
            self.assertIn(text.casefold(), questions.casefold())

    def test_pitch_custom_show_matches_delivered_slide_order(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads(
            (CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8")
        )
        namespace = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        }
        with zipfile.ZipFile(
            CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx"
        ) as archive:
            presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
            children = [node.tag for node in presentation]
            self.assertLess(
                children.index(f"{{{namespace['p']}}}custShowLst"),
                children.index(f"{{{namespace['p']}}}defaultTextStyle"),
            )
            relationships = ET.fromstring(
                archive.read("ppt/_rels/presentation.xml.rels")
            )
            targets = {
                node.attrib["Id"]: node.attrib["Target"] for node in relationships
            }
            slides = {
                slide["code"]: slide["part_number"] for slide in manifest["slides"]
            }
            show = presentation.find("p:custShowLst/p:custShow", namespace)
            self.assertIsNotNone(show)
            self.assertEqual(
                manifest["presentation_route"]["name"], show.attrib["name"]
            )
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
                show.attrib["id"],
                properties.find("p:showPr/p:custShow", namespace).attrib["id"],
            )
            self.assertEqual(
                56, len(presentation.findall("p:sldIdLst/p:sldId", namespace))
            )
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

    def test_optional_story_is_separate_and_matches_both_native_shows(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads((CAPSTONE / "source/slides.json").read_text())
        extra = manifest["appendix_route"]
        self.assertEqual(360, sum(step["seconds"] for step in extra["steps"]))
        script = (CAPSTONE / "pitch/speaker-script.md").read_text()
        self.assertIn("six additional minutes", script)
        self.assertIn("two-minute question reserve", script)
        for step in extra["steps"]:
            self.assertIn("SAY: " + step["say"], script)
        questions = (CAPSTONE / "pitch/questions-and-answers.md").read_text()
        self.assertEqual(
            "See B22/page 50", re.search(r"See B22/page \d+", questions).group()
        )
        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        }
        with zipfile.ZipFile(CAPSTONE / "deck/zava-forward-cowork-v2-draft.pptx") as z:
            presentation = ET.fromstring(z.read("ppt/presentation.xml"))
            targets = {
                node.attrib["Id"]: node.attrib["Target"]
                for node in ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
            }
            shows = presentation.findall("p:custShowLst/p:custShow", ns)
            self.assertEqual(2, len(shows))
            parts = {s["code"]: s["part_number"] for s in manifest["slides"]}
            for show, route in zip(
                shows, (manifest["presentation_route"], extra), strict=True
            ):
                self.assertEqual(route["name"], show.attrib["name"])
                self.assertEqual(
                    [f"slides/slide{parts[s['code']]}.xml" for s in route["steps"]],
                    [
                        targets[node.attrib[f"{{{ns['r']}}}id"]]
                        for node in show.findall("p:sldLst/p:sld", ns)
                    ],
                )
            props = ET.fromstring(z.read("ppt/presProps.xml"))
            self.assertEqual("0", props.find("p:showPr/p:custShow", ns).attrib["id"])

    def test_page_six_only_adds_azure_summary_to_existing_financial_shapes(
        self,
    ) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        }
        with (
            zipfile.ZipFile(CAPSTONE / "source/baseline.pptx") as before,
            zipfile.ZipFile(
                CAPSTONE / "deck/zava-forward-cowork-v2-draft.pptx"
            ) as after,
        ):
            old = ET.fromstring(before.read("ppt/slides/slide6.xml"))
            new = ET.fromstring(after.read("ppt/slides/slide6.xml"))
            old_shapes = list(old.find("p:cSld/p:spTree", ns))
            new_shapes = list(new.find("p:cSld/p:spTree", ns))
            self.assertEqual(len(old_shapes) + 2, len(new_shapes))
            for original, delivered in zip(old_shapes, new_shapes):
                self.assertEqual(ET.tostring(original), ET.tostring(delivered))
            visible = " ".join(t.text or "" for t in new.findall(".//a:t", ns))
            model = json.loads(
                (CAPSTONE / "source/azure-cost-model-2026-11-27.json").read_text()
            )
            self.assertIn(model["display"]["monthly"] + "/month, AI included", visible)
            self.assertIn(model["display"]["persistent"] + "/month", visible)
            notes = ET.fromstring(after.read("ppt/notesSlides/notesSlide6.xml"))
            self.assertIn(
                "AZURE PLANNING UPDATE",
                " ".join(t.text or "" for t in notes.findall(".//a:t", ns)),
            )

    def test_progress_counts_use_a_single_line_native_grid(self) -> None:
        from pptx import Presentation

        page = Presentation(CAPSTONE / "deck/zava-forward-cowork-v2-draft.pptx").slides[
            6
        ]
        expected = {"2023", "2038", "358", "264", "85", "9", "28", "5"}
        counts = [s for s in page.shapes if getattr(s, "text", "") in expected]
        self.assertEqual(expected, {s.text for s in counts})
        self.assertEqual(8, len(counts))
        self.assertEqual(1, len({s.width for s in counts}))
        self.assertEqual(2, len({s.top for s in counts}))
        for shape in counts:
            self.assertEqual(40, shape.text_frame.paragraphs[0].runs[0].font.size.pt)

    def test_revised_appendix_navigation_matches_physical_pages(self) -> None:
        import zipfile
        from xml.etree import ElementTree as ET

        manifest = json.loads(
            (CAPSTONE / "source" / "slides.json").read_text(encoding="utf-8")
        )
        slides = {slide["code"]: slide for slide in manifest["slides"]}
        questions = (CAPSTONE / "pitch" / "questions-and-answers.md").read_text(
            encoding="utf-8"
        )
        with zipfile.ZipFile(
            CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx"
        ) as archive:
            for code, topic in (("B03", "S08"), ("B06", "S12"), ("B13", "S19")):
                with self.subTest(code=code):
                    slide = slides[code]
                    notes = ET.fromstring(
                        archive.read(
                            f"ppt/notesSlides/notesSlide{slide['part_number']}.xml"
                        )
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
        notes = (CAPSTONE / "pitch" / "tokenomics-rehearsal-notes.md").read_text(
            encoding="utf-8"
        )
        record = notes.split("## Rehearsal Record", 1)[1]
        if re.search(r"\| Date and presenter \| *\|", record):
            self.assertIn("rehearsal-notes.md", rows["3"])
            self.assertIn("blank", rows["3"])

    def test_deck_placement_matches_owner_decision(self) -> None:
        pptx = importlib.util.find_spec("pptx")
        if pptx is None:
            self.skipTest("python-pptx is not installed")
        from pptx import Presentation

        deck = Presentation(
            str(CAPSTONE / "deck" / "zava-forward-cowork-v2-draft.pptx")
        )

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
        folder = (
            ROOT
            / "docs/reference/research/evaluation/heldout-batch-432-live-2026-11-18"
        )
        auth = json.loads((folder / "authorization.json").read_text(encoding="utf-8"))
        report = json.loads((folder / "report-live.json").read_text(encoding="utf-8"))
        self.assertTrue(auth["approved_by"] and auth["authority_ref"])
        self.assertEqual("completed", report["outcome"])
        self.assertEqual("measured held-out batch", report["evidence_label"])
        self.assertEqual(auth["authority_ref"], report["spend_authority_ref"])
        self.assertLessEqual(report["calls"], auth["max_calls"])
        self.assertLessEqual(report["tokens"]["total"], auth["max_total_tokens"])
        self.assertLessEqual(
            Decimal(report["accrued_usd"]), Decimal(auth["max_budget_usd"])
        )
        self.assertEqual(report["calls"], len(report["rows"]))

    def test_spoken_scripts_do_not_say_the_batch_has_not_run(self) -> None:
        for doc in (
            CAPSTONE / "tokenomics-qa-brief.md",
            CAPSTONE / "pitch" / "tokenomics-rehearsal-notes.md",
        ):
            text = " ".join(doc.read_text(encoding="utf-8").split())
            for stale in (
                "authorised but not run",
                "not yet run live",
                "That batch has not run",
            ):
                self.assertNotIn(stale, text, f"{doc.name}: {stale}")

    def test_model_tier_comparison_is_dated_sourced_and_makes_no_saving_claim(
        self,
    ) -> None:
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
