"""Issue 344 live browser access proof. Reads credentials at runtime; prints only redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
R = {}

ASSETS = ["/app.js", "/assistants.js", "/index.html", "/law.html", "/law.js", "/ops.js", "/panels.js",
          "/timecapture.js", "/chat.js", "/vendor/leaflet.css", "/vendor/leaflet.js"]
API = ["/api/me", "/api/cases", "/api/cases.csv", "/api/facets", "/api/ranking/policy", "/api/ranking/snapshot",
       "/api/stats", "/api/map", "/api/visits", "/api/handoffs", "/api/packages", "/api/workorders",
       "/api/checklists", "/api/finance", "/api/funding", "/api/retention", "/api/briefing", "/api/assistants",
       "/api/governance", "/api/ai/report", "/api/law", "/api/time/status", "/api/audit-check",
       "/api/continuity", "/api/account/photo"]

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    # 1. unauthenticated landing page in a real browser
    r = page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    R["landing_status"] = r.status
    R["landing_title"] = page.title()
    page.screenshot(path=f"{OUT}/1-landing-anonymous.png")
    # anonymous in-page API calls (browser fetch, no redirect following)
    R["anon_fetch"] = page.evaluate("""async()=>{const o={};for(const [k,h] of [['default',{}],['json',{Accept:'application/json'}],['html',{Accept:'text/html'}]]){
      const r=await fetch('/api/me',{headers:h,redirect:'manual'});o[k]=r.type==='opaqueredirect'?'redirect':r.status}
      const h=await fetch('/healthz');o.healthz=h.status;return o}""")
    # 2. click the sign-in action
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    R["signin_click_reaches_entra"] = True
    page.screenshot(path=f"{OUT}/2-entra-signin-page.png")
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
    R["after_signin_path"] = re.sub(r"^https?://[^/]+", "", page.url)[:60]
    R["after_signin_title"] = page.title()
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/3-workbench-after-signin.png")
    # 3. authenticated parity probes (GET only, status codes)
    R["auth_assets"] = {a: c.request.get(APP + a).status for a in ASSETS}
    R["auth_api"] = {a: c.request.get(APP + a).status for a in API}
    R["healthz_auth"] = c.request.get(APP + "/healthz").status
    t = c.request.get(APP + "/api/time/status"); R["time_status_body"] = t.text()[:200]
    R["auth_ctx_anon_after_logout"] = None
    b.close()

txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/access_proof.json", "w").write(txt)
print(txt)
