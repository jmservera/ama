"""Wrong-role probe, round 6: log redacted navigation hosts for the resident account."""
import json, os, re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
rl = [l.strip() for l in open(os.path.expanduser("~/.ama-resident-test-user")) if l.strip()]
out = {"nav": []}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); pg = c.new_page()
    pg.on("framenavigated", lambda f: out["nav"].append(urlparse(f.url).netloc + urlparse(f.url).path[:40]) if f == pg.main_frame else None)
    pg.on("requestfailed", lambda r: out["nav"].append("FAIL " + urlparse(r.url).netloc + " " + str(r.failure)[:60]))
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    pg.wait_for_selector("input[name=loginfmt]", timeout=20000)
    pg.fill("input[name=loginfmt]", rl[0])
    pg.wait_for_function("!document.querySelector('#idSIButton9').disabled", timeout=20000)
    pg.click("#idSIButton9")
    pg.wait_for_timeout(8000)
    out["host_after_next"] = urlparse(pg.url).netloc
    out["text"] = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", pg.inner_text("body"))[:300] if pg.url.startswith("http") else ""
    b.close()
print(json.dumps(out, indent=1))
