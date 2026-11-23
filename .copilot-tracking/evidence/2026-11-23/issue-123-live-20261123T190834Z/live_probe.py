"""Issue 123 live observation 2026-11-21. Reads credentials at runtime; prints only redacted facts."""
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
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    R["healthz"] = page.evaluate("async()=>(await fetch('/healthz')).status")
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
    R["after_signin_title"] = page.title()
    R["api"] = {a: c.request.get(APP + a).status for a in
                ["/api/me", "/api/continuity", "/api/assistants/releases", "/api/handoffs/unaccepted.csv", "/api/handoffs/unaccepted", "/api/handoffs/unowned"]}
    rel = c.request.get(APP + "/api/assistants/releases")
    try:
        j = rel.json()
        R["releases_body"] = sorted(j.keys()) if isinstance(j, dict) else type(j).__name__
    except Exception:
        R["releases_body"] = rel.text()[:200]
    R["me_role"] = c.request.get(APP + "/api/me").json().get("user", {}).get("role")
    page.goto(APP + "/app#/handoff-waiting")
    page.wait_for_timeout(6000)
    R["screen_text"] = [t.strip()[:140] for t in page.locator("body").inner_text().split("\n") if t.strip()][:25]
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/handoff-waiting-screen.png")
    b.close()

txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/live_probe_output.json", "w").write(txt)
print(txt)
