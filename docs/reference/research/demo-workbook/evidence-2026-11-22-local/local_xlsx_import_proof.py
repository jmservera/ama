"""Local Playwright proof that the Check a spreadsheet screen previews the synthetic .xlsx (#2008).

Starts the API on a synthetic test dataset (no real data, no Azure), signs in as a synthetic
staff member, chooses the committed workbook, and records screenshots, the rendered text and
the SHA-256 of the file before and after. Run from the repository root with src/core, src/agents
and src/api installed or on PYTHONPATH, plus src/core/tests for the dataset.
"""

import hashlib
import json
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from dataset import DATA
from playwright.sync_api import sync_playwright
from zava_forward.api.server import App, make_handler
from zava_forward.core.store import Store

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
WORKBOOK = ROOT / "docs" / "reference" / "research" / "demo-workbook" / "demo-case-list.xlsx"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before = sha(WORKBOOK)
    with tempfile.TemporaryDirectory() as folder:
        data = Path(folder) / "zavaforward.json"
        data.write_text(json.dumps(DATA))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(data)), "zf-test")))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_port}"
        captured: dict[str, object] = {}
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.on(
                "response",
                lambda r: captured.update(raw=r.json()) if r.url.endswith("/api/import-check") else None,
            )
            page.goto(base + "/app")
            page.locator("#email").fill("sam@example.test")
            page.locator("#pw").fill("zf-test")
            page.locator("button[type=submit]").click()
            page.locator("#nav").wait_for()
            page.goto(base + "/app#/import")
            page.get_by_role("heading", name="Check a spreadsheet").wait_for()
            page.screenshot(path=str(OUT / "01-before-choosing-a-file.png"))
            page.locator("#f").set_input_files(str(WORKBOOK))
            page.get_by_role("heading", name="Conflicts to resolve").wait_for()
            page.screenshot(path=str(OUT / "02-xlsx-mapping-conflicts-rows.png"), full_page=True)
            text = page.locator("#app").inner_text()
            (OUT / "rendered-text.txt").write_text(text + "\n")
            accept = page.locator("#f").get_attribute("accept")
            browser.close()
        httpd.shutdown()
    after = sha(WORKBOOK)
    (OUT / "raw-import-check-response.json").write_text(
        json.dumps(
            {
                "accept_attribute": accept,
                "source_unchanged": before == after,
                "sha256_before": before,
                "sha256_after": after,
                "response": captured.get("raw"),
            },
            indent=2,
        )
        + "\n"
    )
    print("source_unchanged", before == after)


if __name__ == "__main__":
    main()
