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
                self.assertEqual(count, 1)
                with self.assertRaises(AssertionError):
                    self.check_manuscript(without_figure)


if __name__ == "__main__":
    unittest.main()
