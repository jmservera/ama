"""Resident consent checkbox probe for #2202 (re-run of the resident part of probe_live.py with diagnostics). Sign-in values are read at run time, never printed."""
import json, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
API = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = Path.home()
u = (home / ".ama-test-user-id").read_text().strip()
p = (home / ".ama-test-user").read_text().strip()
EMAIL, PASSWORD = (home / ".ama-resident-test-user").read_text().splitlines()[:2]
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    rp = c.new_page()
    rp.goto(RES + "/", wait_until="networkidle", timeout=90000)
    rp.fill("input[type=email], input[name=email], #email", EMAIL)
    rp.fill("input[type=password]", PASSWORD)
    with rp.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        rp.keyboard.press("Enter")
    res["resident_login"] = ri.value.status
    res["login_body_keys"] = sorted((ri.value.json() or {}).keys()) if ri.value.ok else None
    rp.wait_for_timeout(5000)
    res["account_visible"] = rp.locator("#account:not([hidden])").count()
    res["page_text"] = re.sub(r"\s+", " ", rp.inner_text("body"))[:600]
    rp.screenshot(path=str(OUT / "screens/resident-after-login.png"))
    if res["account_visible"]:
        rp.click("#chat-launcher"); rp.wait_for_timeout(800)
        cb = rp.locator("#assistant-consent")
        res["consent_visible"] = cb.is_visible()
        res["consent_checked_before"] = cb.is_checked()
        cb.check()
        res["consent_checked_after"] = cb.is_checked()
        res["consent_label"] = rp.evaluate("(document.querySelector('label[for=assistant-consent]')||{}).innerText||null")
        res["consent_aria_name"] = rp.evaluate("document.querySelector('#assistant-consent').labels.length")
        rp.screenshot(path=str(OUT / "screens/resident-consent.png"))
    b.close()
(OUT / "probe-resident-result.json").write_text(json.dumps(res, indent=1))
print(res)
