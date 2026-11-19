"""The chat helper line and tools must stay visible inside the panel on short desktop windows."""

from __future__ import annotations

import functools
import http.server
import threading
import unittest
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None  # type: ignore[assignment]

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
HARNESS = (
    '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
    '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/chat-widget.css">'
    '</head><body><main>x</main><script src="/chat-widget.js"></script></body></html>'
)
OPEN = """() => {
  const w = ChatWidget.create({id: 'employee-chat', title: 'Employee assistant',
    questionLabel: 'Your work question', skillLabel: 'Agent skill', resizable: true,
    stayOpen: true, size: {width: 40, height: 80}});
  w.beforeInput.append(w.node('small', 'Do not enter personal or sensitive resident information.',
    {id: 'employee-chat-entry-warning', class: 'chat-widget-meta'}));
  w.select.append(w.node('option', 'General work help', {value: 'general'}));
  w.open(); w.fail('Type a question first.'); w.setStatus('Asking the assistant.');
}"""
MEASURE = """() => {
  const keys = document.getElementById('employee-chat-keys');
  const panel = document.getElementById('employee-chat').getBoundingClientRect();
  const tools = document.querySelector('#employee-chat .chat-widget-tools').getBoundingClientRect();
  const k = keys.getBoundingClientRect();
  const hit = document.elementFromPoint((k.left + k.right) / 2, (k.top + k.bottom) / 2);
  return {keysVisible: hit === keys,
    toolsInside: tools.top >= panel.top && tools.bottom <= panel.bottom};
}"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/harness.html":
            body = HARNESS.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, *args: object) -> None:
        return


@unittest.skipIf(sync_playwright is None, "playwright is not installed")
class ChatHelperLineVisibleTests(unittest.TestCase):
    def test_helper_line_and_tools_visible_on_short_desktop_windows(self) -> None:
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(Handler, directory=str(WEB))
        )
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch()
                except Exception as exc:  # pragma: no cover
                    self.skipTest(f"chromium unavailable: {exc}")
                for width, height in ((1366, 700), (1280, 720), (1366, 900)):
                    with self.subTest(width=width, height=height):
                        page = browser.new_page(viewport={"width": width, "height": height})
                        page.goto(f"http://127.0.0.1:{server.server_address[1]}/harness.html")
                        page.evaluate(OPEN)
                        result = page.evaluate(MEASURE)
                        self.assertTrue(result["keysVisible"], result)
                        self.assertTrue(result["toolsInside"], result)
                        page.close()
                browser.close()
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
