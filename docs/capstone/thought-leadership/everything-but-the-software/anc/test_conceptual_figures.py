"""Check conceptual-figure outputs and manuscript integration with unittest."""

import hashlib
import json
import re
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

import xml.etree.ElementTree as ET

PACKAGE = Path(__file__).resolve().parent.parent
STEMS = (
    "fig-state-inheritance",
    "fig-pilot-design",
    "fig-contract-states",
    "fig-experiment-measures",
    "fig-refactoring-economics",
)


def supplement_content_digest(text: str) -> str:
    """Compare body content while allowing heading, link and literal-display changes."""
    text = re.sub(r"\\(?:sub)*section\{([^}]+)\}", lambda match: match.group(1), text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(
        r"\\(ref|pageref|autoref|eqref)\{([^}]+)\}",
        lambda match: "\\" + match.group(1) + "{"
        + match.group(2).removeprefix("M-").removeprefix("sup:") + "}", text,
    )
    text = re.sub(r"\\href\{supplement\.pdf\}\{([^}]+)\}", lambda match: match.group(1), text)
    text = re.sub(r"\\hyperref\[sec:supplement\]\{([^}]+)\}", lambda match: match.group(1), text)
    text = re.sub(
        r"\\(?:VerbatimInput|lstinputlisting)(?:\[[^]]*\])?\s*\{([^}]+)\}",
        lambda match: "literal-input{" + match.group(1) + "}", text,
    )
    return hashlib.sha256(" ".join(text.split()).encode()).hexdigest()


class ConceptualFigureTests(unittest.TestCase):
    def test_given_native_diagrams_when_checked_then_labels_and_bindings_are_editable(self) -> None:
        for stem in STEMS:
            with self.subTest(stem=stem):
                scene = json.loads((PACKAGE / f"{stem}.excalidraw").read_text())
                elements = {element["id"]: element for element in scene["elements"]}

                self.assertEqual(scene["type"], "excalidraw")
                self.assertEqual(len(elements), len(scene["elements"]))
                self.assertNotIn("image", {element["type"] for element in elements.values()})
                for element in elements.values():
                    self.assertGreaterEqual(element["width"], 0)
                    self.assertGreaterEqual(element["height"], 0)
                    if element["type"] == "text":
                        self.assertEqual(element["strokeColor"], "#000000")
                        self.assertGreaterEqual(element["fontSize"], 22)
                        self.assertGreater(element["width"], 0)
                        self.assertGreater(element["height"], 0)
                        if element.get("containerId"):
                            parent = elements[element["containerId"]]
                            self.assertIn({"type": "text", "id": element["id"]}, parent["boundElements"])
                    if element["type"] == "arrow":
                        for end in ("startBinding", "endBinding"):
                            parent = elements[element[end]["elementId"]]
                            self.assertIn({"type": "arrow", "id": element["id"]}, parent["boundElements"])

    def check_exports(self, directory: Path) -> None:
        receipt = json.loads((directory / "diagram-exports.json").read_text())
        self.assertEqual({entry["stem"] for entry in receipt["diagrams"]}, set(STEMS))
        for entry in receipt["diagrams"]:
            stem = entry["stem"]
            source = (PACKAGE / f"{stem}.excalidraw").read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(), entry["source_sha256"])
            for extension in ("svg", "png"):
                data = (directory / f"{stem}.{extension}").read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry[f"{extension}_sha256"])
            svg = ET.fromstring((directory / f"{stem}.svg").read_bytes())
            self.assertEqual(svg.get("data-source-sha256"), entry["source_sha256"])
            png = (directory / f"{stem}.png").read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", png[16:24])
            self.assertAlmostEqual(width, entry["width"] * receipt["png_scale"], delta=1)
            self.assertAlmostEqual(height, entry["height"] * receipt["png_scale"], delta=1)

    def test_given_delivered_exports_when_checked_then_hashes_and_full_raster_dimensions_match(self) -> None:
        self.check_exports(PACKAGE)

    def test_given_native_exporter_when_run_then_exports_without_rewriting_sources(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-figures-") as directory:
            output = Path(directory)

            result = subprocess.run(
                ["node", str(PACKAGE / "anc" / "export_diagrams.mjs"), str(output)],
                capture_output=True, text=True, check=False, timeout=90,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {f"{stem}.{extension}" for stem in STEMS for extension in ("svg", "png")}
                | {"diagram-exports.json"},
            )
            self.check_exports(output)
            self.check_exports(PACKAGE)

    def check_manuscript(self, source: str) -> None:
        narrative = source.split(r"\begin{thebibliography}", 1)[0]
        narrative = re.sub(r"(?m)^%.*$", "", narrative)
        narrative = narrative.replace("[Our study's limitations]", "")

        self.assertNotRegex(narrative, r"\b(?:I|my|My|mine|myself|we|We|our|Our|me)\b")
        for stem in STEMS:
            self.assertIn(f"{{{stem}.png}}", narrative)
        for identifier in ("PF1", "PF2", "PF3"):
            self.assertIn(f"TODO(author): {identifier}", source)
        self.assertIn(r"\resultsfalse", narrative)
        self.assertNotIn(r"\resultstrue", narrative)
        self.assertIn("ten ordered features", narrative)
        self.assertNotIn("Regional access scope change", narrative)

    def test_given_manuscript_when_checked_then_concepts_and_deferred_plots_are_explicit(self) -> None:
        from check_paper import expand_inputs

        source = expand_inputs((PACKAGE / "main.tex").read_text(encoding="utf-8"))

        self.check_manuscript(source)

    def test_given_missing_delivered_figure_when_checked_then_integration_fails(self) -> None:
        from check_paper import expand_inputs

        source = expand_inputs((PACKAGE / "main.tex").read_text(encoding="utf-8"))
        for stem in STEMS:
            with self.subTest(stem=stem):
                pattern = r"\\includegraphics(?:\[[^]]*\])?\{" + re.escape(stem) + r"\.png\}"
                without_figure, count = re.subn(pattern, "", source)
                self.assertGreaterEqual(count, 1)
                with self.assertRaises(AssertionError):
                    self.check_manuscript(without_figure)

    def test_given_additive_supplement_when_checked_then_every_active_body_is_included(self) -> None:
        from check_paper import expand_inputs

        manifest = json.loads((PACKAGE / "anc/supplement-integration.json").read_text())
        source = expand_inputs((PACKAGE / "main.tex").read_text(encoding="utf-8"))
        expected = {
            "anc/additional-evidence.tex",
            "anc/case-audits.tex", "anc/deferred-measures.tex",
        }
        self.assertEqual(set(manifest["files"]), expected)
        for name, entry in manifest["files"].items():
            with self.subTest(name=name):
                body = (PACKAGE / name).read_text(encoding="utf-8")
                self.assertIn(body, source)
                self.assertEqual(supplement_content_digest(body), entry["content_sha256"])
        for name, expected_hash in manifest["literal_inputs"].items():
            self.assertIn("{" + name + "}", source)
            self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(), expected_hash)

    def test_given_additive_supplement_when_checked_then_background_figures_and_case_narratives_do_not_repeat(self) -> None:
        from check_paper import expand_inputs, strip_comments

        source = strip_comments(expand_inputs((PACKAGE / "main.tex").read_text(encoding="utf-8")))
        main, supplement = source.split(r"\section{Supplement}", 1)
        images = r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}"

        self.assertFalse(set(re.findall(images, main)) & set(re.findall(images, supplement)))
        self.assertNotIn(r"\subsection{Background}", supplement)
        self.assertNotIn(r"\subsection{Expanded case interpretations}", supplement)
        self.assertNotIn("Case indicators &", supplement)
        raw = (PACKAGE / "anc/supplement-section.tex").read_text(encoding="utf-8")
        self.assertNotIn("anc/extended-background.tex", raw)
        self.assertNotIn("anc/compact-appendix.tex", raw)

    def test_given_literal_renderer_change_when_digest_checked_then_input_path_remains_bound(self) -> None:
        original = r"\VerbatimInput[breaklines=true]{anc/prompt.txt}"
        current = r"\lstinputlisting[breaklines=true]{anc/prompt.txt}"

        self.assertEqual(supplement_content_digest(original), supplement_content_digest(current))
        self.assertNotEqual(
            supplement_content_digest(original),
            supplement_content_digest(current.replace("anc/prompt.txt", "anc/different.txt")),
        )

    def test_given_unified_delivery_when_checked_then_one_document_has_internal_supplement_links(self) -> None:
        from check_paper import expand_inputs, strip_comments

        manifest = json.loads((PACKAGE / "anc/supplement-integration.json").read_text())
        source = strip_comments(expand_inputs((PACKAGE / "main.tex").read_text(encoding="utf-8")))

        self.assertEqual({path.name for path in PACKAGE.glob("*.pdf")}, {"main.pdf"})
        self.assertEqual(source.count(r"\documentclass"), 1)
        self.assertEqual(source.count(r"\begin{document}"), 1)
        self.assertEqual(source.count(r"\begin{thebibliography}"), 1)
        self.assertIn(r"\section{Supplement}\label{sec:supplement}", source)
        self.assertIn(r"\hyperref[sec:supplement]", source)
        self.assertNotIn(r"\href{supplement.pdf}", source)
        self.assertNotRegex(source, r"\\(?:ref|pageref|autoref|eqref)\{M-")
        for name in manifest["owner_approved_standalone_deletions"]:
            self.assertFalse((PACKAGE / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
