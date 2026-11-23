"""Epic #149: law viewer provision text must wrap so the page reflows at 320 CSS pixels.

Engineering evidence over the served style sheet and script text. It is not WCAG conformance
or browser-rendered acceptance; the rendered measurement is recorded in the research note.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"


class LawViewerReflowTests(unittest.TestCase):
    def test_provision_text_is_scoped_to_the_law_output_and_wraps(self) -> None:
        css = (WEB / "style.css").read_text(encoding="utf-8")
        rules = [
            body
            for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
            if any(part.strip() == "#law-out pre" for part in selector.split(","))
        ]
        self.assertTrue(rules, "no style rule for #law-out pre: provision text would not wrap")
        declarations = "".join(rules)
        self.assertIn("white-space:pre-wrap", declarations)
        self.assertIn("overflow-wrap:anywhere", declarations)

    def test_every_preformatted_block_in_the_law_viewer_renders_inside_the_law_output(self) -> None:
        script = (WEB / "law.js").read_text(encoding="utf-8")
        page = (WEB / "law.html").read_text(encoding="utf-8")
        self.assertIn('id="law-out"', page)
        self.assertIn('document.getElementById("law-out")', script)
        self.assertEqual(script.count('el("pre"'), 1)
        self.assertIn("out.replaceChildren(...nodes)", script)


if __name__ == "__main__":
    unittest.main()
