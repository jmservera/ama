"""Polish after the final reviews: title row spacing, check rows, coordinator links, the chat
composer, the end of the page and a missing invoice kind.

The stylesheet cases run the shipped CSS and the shipped chat widget in Chromium on small
constructed pages, and the invoice case runs the shipped panels.js in Node. They are engineering
checks of layout and wording on constructed data, not accessibility or participant evidence.
"""

from __future__ import annotations

import contextlib
import functools
import http.server
import re
import threading
import unittest
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from test_app_wide_ux import H, run

try:
    from playwright.sync_api import Page, sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None  # type: ignore[assignment]

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
PAGE = (
    '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/chat-widget.css">'
    "</head><body>%s</body></html>"
)


@contextlib.contextmanager
def constructed_page(body: str, width: int, height: int = 800) -> Iterator[Page]:
    """The shipped stylesheets and widget script with `body` inside, at one viewport."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path != "/page.html":
                return super().do_GET()
            page = (PAGE % body).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)

        def log_message(self, *args: object) -> None:
            return

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Handler, directory=str(WEB))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except Exception as error:  # pragma: no cover
                raise unittest.SkipTest(f"chromium unavailable: {error}") from error
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"http://127.0.0.1:{server.server_address[1]}/page.html")
            try:
                yield page
            finally:
                browser.close()
    finally:
        server.shutdown()


needs_browser = unittest.skipIf(sync_playwright is None, "playwright is not installed")


@needs_browser
class TitleRowSpacing(unittest.TestCase):
    LIST = (
        '<main id="app"><div class="row between"><h1>My cases today</h1><div class="row">'
        '<a class="btn alt" href="#x">See all cases</a><a class="btn alt" href="#x">Handoff</a>'
        '<a class="btn alt" href="#x">Check a spreadsheet</a></div></div>'
        '<div class="layout"><aside class="side"><h2>Filter</h2></aside>'
        '<div class="main"><p>Briefing</p></div></div></main>'
    )
    GAP = """() => {
      const row = document.querySelector('#app > .row.between').getBoundingClientRect();
      const layout = document.querySelector('.layout').getBoundingClientRect();
      return layout.top - row.bottom;
    }"""

    def test_the_title_row_of_a_work_list_keeps_clear_of_the_filter_and_briefing(self) -> None:
        for width in (1440, 390):
            with self.subTest(width=width), constructed_page(self.LIST, width) as page:
                self.assertGreaterEqual(page.evaluate(self.GAP), 15.5)

    def test_a_row_that_is_not_the_first_thing_on_the_page_keeps_its_own_spacing(self) -> None:
        heading = (
            '<main id="app"><ul class="case-links"><li><a href="#x">Back</a></li></ul>'
            '<div class="row between"><h1>Pat Cedar</h1><span>Reference ZF-1</span></div></main>'
        )
        with constructed_page(heading, 1440) as page:
            margin = page.evaluate(
                "() => getComputedStyle(document.querySelector('.row.between')).marginBottom"
            )
        self.assertEqual(margin, "0px")


@needs_browser
class CheckRows(unittest.TestCase):
    ROW = (
        '<main id="app"><div class="check"><input type="checkbox" id="tick" '
        'aria-describedby="tick-hint"><label for="tick">Show only homes with stale or offline '
        'sensors</label><p class="field-hint" id="tick-hint">Zoom in until homes are shown one '
        'by one.</p><p class="field-error" id="tick-error">Tick the box once the resident has '
        "been told.</p></div></main>"
    )
    MEASURE = """() => {
      const box = document.getElementById('tick').getBoundingClientRect();
      const label = document.querySelector('label');
      const words = document.createRange();
      words.selectNodeContents(label);
      const text = words.getBoundingClientRect();
      const left = (selector) => document.querySelector(selector).getBoundingClientRect().left;
      const hint = document.querySelector('.field-hint');
      const hintText = document.createRange();
      hintText.selectNodeContents(hint);
      return {boxRight: box.right, labelLeft: label.getBoundingClientRect().left,
        textLeft: text.left, hintLeft: hintText.getBoundingClientRect().left,
        errorLeft: left('.field-error') + parseFloat(getComputedStyle(
          document.querySelector('.field-error')).paddingInlineStart),
        hintTop: hint.getBoundingClientRect().top, rowTop: label.getBoundingClientRect().bottom};
    }"""

    def test_the_whole_row_is_clickable_and_the_hint_lines_up_under_the_label_text(self) -> None:
        for width in (1440, 390):
            with self.subTest(width=width), constructed_page(self.ROW, width) as page:
                seen = page.evaluate(self.MEASURE)
                self.assertAlmostEqual(seen["labelLeft"], seen["boxRight"], delta=0.5)
                # The space between the box and the words belongs to the label, so a click ticks.
                between = (seen["boxRight"] + seen["textLeft"]) / 2
                top = page.evaluate(
                    "() => document.querySelector('label').getBoundingClientRect().top + 4"
                )
                page.mouse.click(between, top)
                self.assertTrue(page.evaluate("() => document.getElementById('tick').checked"))
                self.assertAlmostEqual(seen["hintLeft"], seen["textLeft"], delta=0.5)
                self.assertAlmostEqual(seen["errorLeft"], seen["textLeft"], delta=0.5)


@needs_browser
class CoordinatorLinks(unittest.TestCase):
    PAGE = (
        '<main id="app"><section class="coordinator"><p><a id="sentence" href="#x">3</a> '
        'currently cannot move on.</p><table><tbody><tr><th scope="row">Survey</th><td>'
        '<a id="count" href="#x">3</a> / 9</td></tr></tbody></table></section></main>'
    )
    MEASURE = """() => {
      const box = (id) => document.getElementById(id).getBoundingClientRect();
      return {sentence: getComputedStyle(document.getElementById('sentence')).display,
        countWidth: box('count').width, countHeight: box('count').height,
        align: getComputedStyle(document.getElementById('count')).textAlign,
        minimum: parseFloat(getComputedStyle(document.documentElement).fontSize) * 1.5};
    }"""

    def test_a_count_in_a_sentence_stays_inline_and_a_count_in_a_table_stays_tappable(self) -> None:
        with constructed_page(self.PAGE, 1280) as page:
            seen = page.evaluate(self.MEASURE)
        self.assertEqual(seen["sentence"], "inline", "a link in a sentence does not grow its line")
        self.assertGreaterEqual(seen["countWidth"], seen["minimum"] - 0.5)
        self.assertGreaterEqual(seen["countHeight"], seen["minimum"] - 0.5)
        self.assertEqual(seen["align"], "center")


@needs_browser
class ChatComposer(unittest.TestCase):
    OPEN = """() => {
      const w = ChatWidget.create({id: 'employee-chat', title: 'Employee assistant',
        questionLabel: 'Your work question', skillLabel: 'Agent skill', visibleLabels: true,
        resizable: true, stayOpen: true, size: {width: 40, height: 80}});
      w.beforeInput.append(w.node('small', 'Do not enter personal or sensitive resident '
        + 'information. Chat cannot approve or change records.',
        {id: 'employee-chat-entry-warning', class: 'chat-widget-meta'}));
      w.select.append(w.node('option', 'General work help', {value: 'general'}));
      w.open();
    }"""
    MEASURE = """() => {
      const entry = document.querySelector('#employee-chat .chat-widget-entry');
      const reason = document.getElementById('employee-chat-unsupported').getBoundingClientRect();
      const box = entry.getBoundingClientRect();
      return {scrolls: entry.scrollHeight > entry.clientHeight + 1,
        reasonInside: reason.top >= box.top - 0.5 && reason.bottom <= box.bottom + 0.5};
    }"""

    def test_a_narrow_phone_shows_the_whole_attach_and_voice_explanation(self) -> None:
        with constructed_page('<main id="app"><p>Cases</p></main>', 390, 800) as page:
            page.add_script_tag(url="/chat-widget.js")
            page.evaluate(self.OPEN)
            seen = page.evaluate(self.MEASURE)
        self.assertEqual(seen, {"scrolls": False, "reasonInside": True})

    def test_wide_windows_keep_their_composer_as_it_was(self) -> None:
        with constructed_page('<main id="app"><p>Cases</p></main>', 1440, 900) as page:
            page.add_script_tag(url="/chat-widget.js")
            page.evaluate(self.OPEN)
            seen = page.evaluate(
                "() => getComputedStyle(document.querySelector("
                "'#employee-chat .chat-widget-composer')).maxHeight"
            )
        self.assertEqual(seen, "55%")


@needs_browser
class PageEnd(unittest.TestCase):
    CARDS = (
        '<main id="app">'
        + "".join(
            f'<section class="card"><h2>Card {n}</h2><p>{"Text. " * 60}</p></section>'
            for n in range(6)
        )
        + '</main><button id="employee-chat-launcher" class="chat-widget-launcher" type="button" '
        'aria-label="Chat">Chat</button>'
    )
    CLEARANCE = """() => {
      window.scrollTo(0, document.documentElement.scrollHeight);
      const last = [...document.querySelectorAll('.card')].at(-1).getBoundingClientRect();
      const launcher = document.getElementById('employee-chat-launcher').getBoundingClientRect();
      return {lastBottom: last.bottom, launcherTop: launcher.top};
    }"""

    def test_the_launcher_never_covers_the_last_card_on_a_phone(self) -> None:
        for width in (390, 320, 600):
            with self.subTest(width=width), constructed_page(self.CARDS, width, 800) as page:
                seen = page.evaluate(self.CLEARANCE)
                self.assertLessEqual(seen["lastBottom"], seen["launcherTop"], seen)


class StrayZero(unittest.TestCase):
    def test_no_script_lists_a_node_after_a_bare_count(self) -> None:
        """`items.length && h(...)` as a child prints the number 0 when there are no items."""
        bare_count = re.compile(r"(?<![!.\w\]?])[\w.?\[\]]+\.length\s*&&\s*(?:h\(|\[)")
        for script in sorted(WEB.glob("*.js")):
            with self.subTest(script=script.name):
                self.assertEqual(bare_count.findall(script.read_text()), [])


class MissingInvoiceKind(unittest.TestCase):
    STUBS = (
        H
        + (WEB / "panels.js").read_text()
        + """
const me = {user: {role: "Retrofit Programme Manager", name: "Pam"}};
const api = async () => ({});
"""
    )

    def test_an_invoice_without_a_kind_still_lists_and_names_its_reference(self) -> None:
        out: Any = run(
            """
const invoice = extra => ({id: "INV-1", ref: "SYN-INV-7", supplier: "Test Ltd", status: "Received",
  payment_status: "Not payable yet", exceptions: [], ...extra});
const lines = extra => {
  const panel = financePanel({finance: {budget: null, commitments: [], invoices: [invoice(extra)]}},
    "ZF-1", async () => {});
  return byTag(panel, "strong").map(node => node.textContent);
};
return {withKind: lines({kind: "Invoice"}), without: lines({})};
""",
            self.STUBS,
        )
        self.assertEqual(out["withKind"], ["INV-1: invoice SYN-INV-7 from Test Ltd. Received."])
        self.assertRegex(out["without"][0], r"^INV-1:\s+SYN-INV-7 from Test Ltd\. Received\.$")


if __name__ == "__main__":
    unittest.main()
