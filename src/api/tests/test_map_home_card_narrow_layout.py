"""Browser-free pin for #1844: the home summary must not float over map controls when narrow."""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CSS = (WEB / "style.css").read_text()
APP = (WEB / "app.js").read_text()
MEDIA = re.compile(r"@media\([^)]*\)\{.*?\}\}", re.S)


def declarations(selector: str, media: str | None = None) -> list[str]:
    """Declaration text of each exact-selector rule, top level or inside one media query."""
    if media:
        blocks = re.findall(r"@media\(" + re.escape(media) + r"\)\{(.*?\})\}", CSS)
        scope = "\n".join(blocks)
    else:
        scope = MEDIA.sub("", CSS)
    return re.findall(r"(?:^|\})\s*" + re.escape(selector) + r"\{([^}]*)\}", scope)


class MapHomeCardNarrowLayout(unittest.TestCase):
    def test_desktop_card_still_overlays_the_map(self) -> None:
        base = declarations(".map-home-card")
        self.assertEqual(1, len(base))
        self.assertIn("position:absolute", base[0])

    def test_narrow_card_flows_below_the_map(self) -> None:
        narrow = declarations(".map-home-card", media="max-width:600px")
        self.assertEqual(1, len(narrow))
        for rule in ("position:static", "width:auto", "max-height:none"):
            self.assertIn(rule, narrow[0])

    def test_narrow_breakpoint_covers_the_assessed_widths(self) -> None:
        self.assertIn("@media(max-width:600px){.map-home-card{", CSS)

    def test_expanded_dialog_card_stays_static(self) -> None:
        rules = declarations(".map-dialog .map-home-card")
        self.assertTrue(any("position:static" in d for d in rules))

    def test_card_is_still_placed_with_the_map_stage(self) -> None:
        self.assertIn('h("div", { class: "map-stage" }, el, homeCard)', APP)


if __name__ == "__main__":
    unittest.main()
