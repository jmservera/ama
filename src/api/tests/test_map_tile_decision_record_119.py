"""Issue 119: the map tile decision record stays honest and tied to the code it describes."""

import re
import unittest
from pathlib import Path

from zava_forward.api.server import tile_config

ROOT = Path(__file__).resolve().parents[3]
RECORD = ROOT / "docs" / "design" / "map-tile-provider-decision-record.md"
OPTIONS = ROOT / "docs" / "reference" / "research" / "ux" / "map-tile-provider-options.md"
PRD = ROOT / "docs" / "prds" / "zava-forward-retrofit-programme-demonstrator.md"
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


class MapTileDecisionRecord(unittest.TestCase):
    def setUp(self) -> None:
        self.text = RECORD.read_text()

    def test_relative_links_resolve(self) -> None:
        for target in LINK.findall(self.text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            path = target.split("#", 1)[0]
            with self.subTest(target=target):
                self.assertTrue((RECORD.parent / path).exists())

    def test_no_provider_is_selected_and_no_credential_is_recorded(self) -> None:
        self.assertIn("No licensed provider is selected", self.text)
        self.assertNotRegex(self.text, r"(?i)[?&](key|token|apikey|sig)=")
        self.assertIn("unmet", self.text)

    def test_cited_requirements_exist_in_the_prd(self) -> None:
        prd = PRD.read_text()
        for req in sorted(set(re.findall(r"\b(?:FR|AC)-\d+\b", self.text))):
            with self.subTest(requirement=req):
                self.assertRegex(prd, rf"\b{req}\b")

    def test_record_matches_the_code_it_describes(self) -> None:
        self.assertIsNone(tile_config({"ZF_ENV": "production"})["url"])
        js = (WEB / "app.js").read_text()
        self.assertIn("Show the map areas as a list (keyboard and screen reader friendly)", js)
        self.assertIn(
            "Show the map areas as a list (keyboard and screen reader friendly)", self.text
        )
        self.assertIn('class: "maplist"', js)

    def test_options_review_links_the_record(self) -> None:
        self.assertIn("map-tile-provider-decision-record.md", OPTIONS.read_text())


if __name__ == "__main__":
    unittest.main()
