"""Wrong-role probe: resident test account against the staff API. Redacted output only."""
import json, os, re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
rl = [l.strip() for l in open(os.path.expanduser("~/.ama-resident-test-user")) if l.strip()]
GUID = re.compile(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}", re.I)
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", rl[0]); pg.wait_for_function("!document.querySelector('#idSIButton9').disabled", timeout=20000)
    pg.click("#idSIButton9")
    try:
        pg.wait_for_selector("input[name=passwd]", timeout=15000)
        pg.fill("input[name=passwd]", rl[1]); pg.click("#idSIButton9")
    except Exception as e:
        out["step"] = "password-field-missing"
        out["page_text"] = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", pg.inner_text("body"))[:300]
    for _ in range(3):
        try:
            pg.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if pg.url.startswith(APP): break
            (pg.query_selector("#idSIButton9") or pg.query_selector("#idBtn_Back")).click()
        except Exception: break
    out["final_host"] = urlparse(pg.url).netloc
    if pg.url.startswith(APP):
        m = c.request.get(APP + "/api/me", max_redirects=0); out["me_status"] = m.status
        out["cases_status"] = c.request.get(APP + "/api/cases", max_redirects=0).status
        out["me_body"] = GUID.sub("<GUID>", re.sub(r"[\w.+-]+@[\w.-]+", "[email]", m.text()))[:300]
    else:
        out["page_text"] = out.get("page_text") or re.sub(r"[\w.+-]+@[\w.-]+", "[email]", pg.inner_text("body"))[:300]
    b.close()
print(json.dumps(out, indent=1))
