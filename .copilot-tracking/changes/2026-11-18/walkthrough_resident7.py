"""Round 7 desktop resident sensor view proof for #1818 (no secrets printed). Usage: walkthrough_resident7.py EVIDENCE_DIR [TAG]"""

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

import walkthrough_probe7 as probe

APP = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"


def main() -> int:
    out = Path(sys.argv[1])
    tag = sys.argv[2] if len(sys.argv) > 2 else "fresh"
    user, password = probe.credentials("resident")
    result: dict[str, object] = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.goto(APP + "/", wait_until="domcontentloaded", timeout=120000)
        time.sleep(20)
        page.locator('input[type="email"], input[name="email"], #email').first.fill(user)
        page.locator('input[type="password"]').first.fill(password)
        page.get_by_role("button", name="Sign in").first.click()
        time.sleep(40)
        sec = page.locator("#sec-sensors")
        result["sec_sensors_count"] = sec.count()
        if sec.count():
            sec.first.scroll_into_view_if_needed()
            text = sec.first.inner_text()
            (out / f"resident-sensors-text-{tag}.txt").write_text(text)
            result["lines"] = [ln for ln in text.splitlines() if ln.strip()][:8]
            sec.first.screenshot(path=str(out / f"resident-sensors-section-{tag}.png"))
        page.screenshot(path=str(out / f"resident-sensors-page-{tag}.png"))
        result["other_home_ids_visible"] = len({w for w in page.inner_text("body").split() if w.startswith("ZF-")})
        browser.close()
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
