"""Static page structure for the three served HTML pages (#149).

Source-level checks only. They are not WCAG conformance or assistive technology evidence.
"""

import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
PAGES = ("index.html", "welcome.html", "law.html")
CONTROLS = {"input", "select", "textarea"}


class Page(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.label_for: set[str] = set()
        self.wrapped: set[int] = set()
        self.button_text: dict[int, str] = {}
        self._label_depth = 0
        self._button: int | None = None
        self.title = ""
        self._in_title = False
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        self.tags.append((tag, a))
        index = len(self.tags) - 1
        if tag == "title":
            self._in_title = True
        if tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.label_for.add(a["for"] or "")
        if tag in CONTROLS and self._label_depth:
            self.wrapped.add(index)
        if tag == "button":
            self._button = index
            self.button_text[index] = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "label":
            self._label_depth -= 1
        if tag == "button":
            self._button = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._button is not None:
            self.button_text[self._button] += data

    def named(self, name: str) -> list[tuple[str, dict[str, str | None]]]:
        return [t for t in self.tags if t[0] == name]


def load(name: str) -> Page:
    return Page((WEB / name).read_text())


class StaticPageStructure(unittest.TestCase):
    def test_document_has_title_viewport_and_charset(self) -> None:
        for name in PAGES:
            page = load(name)
            self.assertTrue(page.title.strip(), name)
            metas = [a for _, a in page.named("meta")]
            self.assertTrue(any(a.get("charset") for a in metas), name)
            viewport = [a for a in metas if a.get("name") == "viewport"]
            self.assertEqual(len(viewport), 1, name)
            self.assertIn("width=device-width", viewport[0]["content"] or "", name)
            self.assertNotIn("user-scalable=no", viewport[0]["content"] or "", name)

    def test_single_focusable_main_and_single_h1(self) -> None:
        for name in PAGES:
            page = load(name)
            mains = page.named("main")
            self.assertEqual(len(mains), 1, name)
            self.assertEqual(mains[0][1].get("tabindex"), "-1", name)
            self.assertEqual(len(page.named("h1")), 1, name)

    def test_ids_are_unique(self) -> None:
        for name in PAGES:
            ids = [a["id"] for _, a in load(name).tags if a.get("id")]
            self.assertEqual([i for i, n in Counter(ids).items() if n > 1], [], name)

    def test_skip_links_target_existing_elements(self) -> None:
        for name in ("index.html", "welcome.html"):
            page = load(name)
            ids = {a["id"] for _, a in page.tags if a.get("id")}
            skips = [a for t, a in page.named("a") if "skip-link" in (a.get("class") or "")]
            self.assertEqual(len(skips), 1, name)
            self.assertIn((skips[0]["href"] or "").lstrip("#"), ids, name)

    def test_form_controls_have_labels(self) -> None:
        for name in PAGES:
            page = load(name)
            for index, (tag, a) in enumerate(page.tags):
                if tag not in CONTROLS or a.get("type") == "hidden":
                    continue
                labelled = (
                    index in page.wrapped
                    or a.get("id") in page.label_for
                    or a.get("aria-label")
                    or a.get("aria-labelledby")
                )
                self.assertTrue(labelled, (name, a))

    def test_images_have_alt_and_buttons_have_names(self) -> None:
        for name in PAGES:
            page = load(name)
            for _, a in page.named("img"):
                self.assertIn("alt", a, (name, a.get("src")))
            for index, (tag, a) in enumerate(page.tags):
                if tag == "button":
                    named = page.button_text[index].strip() or a.get("aria-label")
                    self.assertTrue(named, (name, a))

    def test_new_tab_links_use_noopener(self) -> None:
        for name in PAGES:
            for _, a in load(name).named("a"):
                if a.get("target") == "_blank":
                    self.assertIn("noopener", a.get("rel") or "", (name, a.get("href")))


if __name__ == "__main__":
    unittest.main()
