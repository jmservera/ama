"""Epic #149: landmarks, skip link, focus indicator, reduced motion and forced colours.

Engineering evidence on the served workbench pages and style sheets, over a real local HTTP
server on constructed data (the API is a standard-library server, so there is no TestClient).
It is not WCAG conformance, assistive-technology or browser-rendered focus-order acceptance,
which stay with human testers.
"""

import copy
import json
import re
import tempfile
import threading
import unittest
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer
from pathlib import Path

import dataset
from test_quality_procurement import STAFF
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler

ROUTES = ("/", "/app", "/law.html")
WORKBENCH = "/app"
# Recorded gaps, shrink-only: a fix must remove the route here so the check then enforces it.
NO_SKIP_LINK = {"/", "/law.html"}
NO_NAV = {"/", "/law.html"}
LANG = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = ""
        self.title = ""
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.links: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == "html":
            self.lang = a.get("lang") or ""
        elif tag == "title":
            self._in_title = True
        elif tag == "link" and a.get("rel") == "stylesheet" and a.get("href"):
            self.links.append(a["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data

    def find(self, tag: str) -> list[dict[str, str | None]]:
        return [a for t, a in self.tags if t == tag]


class Rendered(unittest.TestCase):
    tmp: tempfile.TemporaryDirectory[str]
    store: SqlStore
    httpd: ThreadingHTTPServer
    thread: threading.Thread
    base: str
    pages: dict[str, str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        data = copy.deepcopy(dataset.DATA)
        data["staff"] = copy.deepcopy(STAFF)
        path = Path(cls.tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        cls.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        cls.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            make_handler(App(cls.store, "SYN-landmarks-test")),  # type: ignore[no-untyped-call]
        )
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_port}"
        cls.pages = {route: cls.fetch(route) for route in ROUTES}

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=5)
        cls.store.db.close()
        cls.tmp.cleanup()

    @classmethod
    def fetch(cls, route: str) -> str:
        with urllib.request.urlopen(cls.base + route, timeout=10) as response:
            assert response.status == 200, route
            return str(response.read().decode("utf-8"))

    def parse(self, route: str) -> Page:
        page = Page()
        page.feed(self.pages[route])
        return page

    def css(self) -> str:
        sheets = []
        for href in self.parse(WORKBENCH).links:
            if href.startswith("/vendor/"):
                continue
            sheets.append(self.fetch(href))
        return "\n".join(sheets)


class PageStructure(Rendered):
    def test_language_and_title_are_valid_and_descriptive(self) -> None:
        titles = set()
        for route in ROUTES:
            page = self.parse(route)
            self.assertRegex(page.lang, LANG, route)
            self.assertEqual(page.lang, "en-GB", route)
            title = page.title.strip()
            self.assertIn("Zava Forward", title, route)
            self.assertGreater(len(title), len("Zava Forward"), route)
            titles.add(title)
        self.assertEqual(len(titles), len(ROUTES), "each page needs a distinct title")

    def test_each_page_has_one_banner_and_one_main_landmark(self) -> None:
        for route in ROUTES:
            tags = Counter(t for t, _ in self.parse(route).tags)
            self.assertEqual(tags["header"], 1, route)
            self.assertEqual(tags["main"], 1, route)

    def test_workbench_has_a_named_nav_landmark_before_main(self) -> None:
        page = self.parse(WORKBENCH)
        navs = page.find("nav")
        self.assertEqual(len(navs), 1)
        self.assertTrue((navs[0].get("aria-label") or "").strip())
        order = [t for t, _ in page.tags if t in ("header", "nav", "main")]
        self.assertEqual(order, ["header", "nav", "main"])

    def test_nav_gaps_are_recorded_and_shrink_only(self) -> None:
        for route in ROUTES:
            has_nav = bool(self.parse(route).find("nav"))
            self.assertEqual(has_nav, route not in NO_NAV, f"{route}: update NO_NAV")

    def test_ids_are_unique_so_skip_targets_resolve(self) -> None:
        for route in ROUTES:
            ids = [a["id"] for _, a in self.parse(route).tags if a.get("id")]
            self.assertEqual([i for i, n in Counter(ids).items() if n > 1], [], route)


class SkipLink(Rendered):
    def test_workbench_skip_link_is_first_focusable_and_targets_main(self) -> None:
        page = self.parse(WORKBENCH)
        focusable = [
            (t, a)
            for t, a in page.tags
            if t in ("a", "button", "input", "select", "textarea", "summary")
        ]
        tag, skip = focusable[0]
        self.assertEqual((tag, skip.get("class")), ("a", "skip-link"))
        href = skip.get("href") or ""
        self.assertRegex(href, r"^#[\w-]+$")
        main = page.find("main")[0]
        self.assertEqual(main.get("id"), href[1:])
        self.assertEqual(main.get("tabindex"), "-1", "main must take programmatic focus")

    def test_skip_link_gaps_are_recorded_and_shrink_only(self) -> None:
        for route in ROUTES:
            has_skip = any("skip-link" in (a.get("class") or "") for _, a in self.parse(route).tags)
            self.assertEqual(has_skip, route not in NO_SKIP_LINK, f"{route}: update NO_SKIP_LINK")

    def test_skip_link_is_hidden_until_focused_and_then_visible(self) -> None:
        css = self.css()
        hidden = re.search(r"\.skip-link\{([^}]*)\}", css)
        shown = re.search(r"\.skip-link:focus\{([^}]*)\}", css)
        assert hidden and shown
        self.assertRegex(hidden.group(1), r"position:absolute")
        self.assertRegex(hidden.group(1), r"top:-\d")
        self.assertNotRegex(hidden.group(1), r"display:none|visibility:hidden")
        self.assertRegex(shown.group(1), r"top:var\(--sp-\d\)")


class StyleSheets(Rendered):
    def test_focus_visible_outline_is_kept_and_never_removed(self) -> None:
        css = self.css()
        rule = re.search(r"(?:^|\})\s*:focus-visible\{([^}]*)\}", css, re.M)
        assert rule
        self.assertRegex(rule.group(1), r"outline:var\(--focus-w\) solid var\(--focus-ink\)")
        self.assertIn("outline-offset", rule.group(1))
        self.assertNotRegex(css, r"outline\s*:\s*(none|0)\b")
        self.assertNotRegex(css, r"outline-style\s*:\s*none")

    def test_focus_does_not_depend_on_a_dropped_forced_colours_property(self) -> None:
        css = self.css()
        self.assertNotIn("forced-color-adjust:none", css.replace(" ", ""))
        rule = re.search(r"(?:^|\})\s*:focus-visible\{([^}]*)\}", css, re.M)
        assert rule
        # Forced colours drops box-shadow, so the solid outline must carry the indicator alone.
        self.assertIn("outline:", rule.group(1))

    def test_reduced_motion_suppresses_every_animation_and_transition(self) -> None:
        for href in self.parse(WORKBENCH).links:
            if href.startswith("/vendor/"):
                continue
            css = self.fetch(href)
            reduced = "".join(
                re.findall(r"@media\(prefers-reduced-motion:reduce\)\{(.*?)\}\}", css, re.S)
            )
            outside = re.sub(
                r"@media\(prefers-reduced-motion:reduce\)\{.*?\}\}", "", css, flags=re.S
            )
            for name in re.findall(r"animation:([\w-]+)\s", outside):
                self.assertRegex(
                    reduced, r"animation:none", f"{href}: {name} has no reduced-motion override"
                )
            transitions = re.findall(r"transition:([^;}]+)", outside)
            for value in transitions:
                if "var(--motion)" in value:
                    continue
                self.assertIn("transition:none", reduced, f"{href}: transition {value!r}")
            if "var(--motion)" in outside:
                self.assertRegex(
                    "".join(re.findall(r"@media\(prefers-reduced-motion:reduce\)\{(.*?)\}", css)),
                    r"--motion:0s",
                )

    def test_motion_token_is_zeroed_under_reduced_motion(self) -> None:
        css = self.css()
        self.assertRegex(css, r"@media\(prefers-reduced-motion:reduce\)\{:root\{--motion:0s\}\}")
        self.assertRegex(css, r"--motion:var\(--durationFast\)")

    def test_forced_colours_blocks_use_system_colours_for_state(self) -> None:
        css = self.css()
        blocks = re.findall(r"@media\(forced-colors:active\)\{(.*?\})\}", css, re.S)
        self.assertGreaterEqual(len(blocks), 2)
        joined = "".join(blocks)
        for system_colour in ("Highlight", "CanvasText", "Canvas"):
            self.assertIn(system_colour, joined)
        self.assertNotRegex(
            joined, r"#[0-9a-fA-F]{3,6}\b", "forced-colours rules must not hard-code colours"
        )
        self.assertIn(".step[aria-current=step]", joined)
        self.assertIn(".tile[aria-pressed=true]", joined)

    def test_state_is_not_colour_alone_under_forced_colours(self) -> None:
        css = self.css()
        self.assertIn("border-style:double", css)
        self.assertRegex(css, r"\.case-tabs \[aria-selected=true\]\{outline:2px solid Highlight\}")


if __name__ == "__main__":
    unittest.main()
