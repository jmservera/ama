"""Probe: can Alan Steiner (RuleOwner) sign in to the demo API with Playwright? Credentials are read at run
time from ~/.ama-test-user-id-2 and ~/.ama-test-user-2 and never printed; emails are masked in output."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
B = {"user": rd(".ama-test-user-id-2"), "pw": rd(".ama-test-user-2")}


def mask(s):
    return s.replace(B["user"], "[user]").replace(B["pw"], "[secret]")


with sync_playwright() as p:
    b = p.chromium.launch(); page = b.new_context(viewport={"width": 1366, "height": 900}).new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", B["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", B["pw"]); page.click("#idSIButton9")
    res = {}
    nav=[]
    page.on("framenavigated", lambda f: nav.append(f.url.split("?")[0][-60:]) if f==page.main_frame else None)
    page.on("response", lambda r: nav.append((r.status, r.url.split("?")[0][-50:])) if r.url.startswith(APP) else None)
    for _ in range(5):
        try:
            page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=8000)
            break
        except Exception:
            btn = page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")
            if btn and "Stay signed in" in page.inner_text("body"):
                btn.click()
            else:
                break
    page.wait_for_timeout(3000)
    page.goto(APP + "/api/me", wait_until="networkidle")
    res["url"] = page.url.split("?")[0][:120]
    if page.url.startswith(APP):
        res["me"] = mask(page.inner_text("body"))[:600]
    else:
        res["page_text"] = mask(page.inner_text("body"))[:400].replace("\n", " ")
    res["nav"]=nav
    print(json.dumps(res, indent=1))
    b.close()
