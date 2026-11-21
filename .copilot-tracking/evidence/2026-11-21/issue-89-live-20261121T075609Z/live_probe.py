"""Issue 89 live read-only probe 2026-11-21. Reads credentials at runtime; prints redacted shape facts only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
R = {}

def shape(v):
    if isinstance(v, list):
        return {"count": len(v), "keys": sorted(v[0].keys())[:25] if v and isinstance(v[0], dict) else None}
    return {"type": type(v).__name__, "keys": sorted(v.keys())[:25] if isinstance(v, dict) else None}

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
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
    R["me_role"] = c.request.get(APP + "/api/me").json().get("user", {}).get("role")
    for a in ["/api/packages", "/api/workorders", "/api/checklists", "/api/handoffs"]:
        r = c.request.get(APP + a)
        R[a] = {"status": r.status}
        if r.status == 200:
            R[a].update(shape(r.json()))
    pk = c.request.get(APP + "/api/packages")
    if pk.status == 200 and isinstance(pk.json(), list):
        R["package_sample"] = {k: (v if not isinstance(v, (dict, list)) else (list(v)[:8] if isinstance(v, dict) else v[:3])) for k, v in pk.json()[0].items() if k not in ("scope_history", "consultation_history")}
        R["package_status_values"] = sorted({str(x.get("status")) for x in pk.json()})
        R["package_capacity_fields"] = sorted({k for x in pk.json() for k in x if re.search("capac|commit|offer", k)})
    wo = c.request.get(APP + "/api/workorders")
    if wo.status == 200 and isinstance(wo.json(), list):
        R["workorder_keys"] = sorted(wo.json()[0].keys())
        R["workorder_sample"] = {k: v for k, v in wo.json()[0].items() if not isinstance(v, (dict, list)) and not re.search("name|email|address", k)}
        R["workorder_status_values"] = sorted({str(x.get("status")) for x in wo.json()})
        R["workorder_instruction_flags"] = sorted({str(x.get("instruction", x.get("is_instruction"))) for x in wo.json()})
    R["nav_hrefs"] = page.evaluate("()=>[...document.querySelectorAll('a[href^=\\'#/\\']')].map(e=>e.getAttribute('href')).slice(0,30)")
    page.evaluate("()=>{location.hash='#/capacity'}")
    page.wait_for_timeout(8000)
    R["capacity_headings"] = [t.strip()[:100] for t in page.locator("h1,h2,h3").all_inner_texts()][:12]
    R["capacity_text"] = [t.strip()[:140] for t in page.locator("main, body").first.inner_text().split("\n") if t.strip()][:25]
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/capacity-screen.png")
    b.close()

txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/live_probe_output.json", "w").write(txt)
print(txt)
