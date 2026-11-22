"""Issue 344 signed-in re-check of the endpoints that failed in the eighth pass. Credentials read at runtime only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    bad = []; reqs = []
    page.on('requestfinished', lambda r: reqs.append(re.sub(r'^https?://[^/]+','',r.url)[:80]) if '/api/assistants' in r.url or '/assistants.js' in r.url else None)
    page.on('requestfailed', lambda r: reqs.append('FAILED '+re.sub(r'^https?://[^/]+','',r.url)[:80]+' '+str(r.failure)[:40]))
    page.on("response", lambda r: bad.append(f"{r.status} {re.sub(r'^https?://[^/]+', '', r.url)[:70]}") if r.status >= 400 else None)
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd], input[name=pass]", timeout=30000)
    page.fill("input[name=passwd], input[name=pass]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    page.click("#nav a[href='#/assistants']")
    page.wait_for_timeout(1000)
    R["api"] = {a: c.request.get(APP + a).status for a in ["/api/handoffs/unaccepted", "/api/handoffs/unaccepted.csv", "/api/ai/report", "/api/law", "/api/account/photo", "/api/time/status", "/api/handoffs", "/api/handoffs/unowned", "/api/assistants/proposals"]}
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/gaps_recheck.json", "w").write(txt)
print(txt)
