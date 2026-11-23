import json, os
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")
res = {}
PATHS = ["/api/me","/api/cases","/api/packages","/api/workorders","/api/funding","/api/coordinator","/api/progress","/api/stats","/api/ranking/policy","/api/exceptions","/api/law/cards","/api/law/alerts","/api/chat/threads","/api/resident/choice-queue","/api/asset/stock-queue","/api/checklists"]
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/"); pg.wait_for_timeout(6000)
    pg.screenshot(path=OUT + "/workbench-home.png")
    for path in PATHS:
        r = c.request.get(H + path)
        try: body = r.json()
        except Exception: body = None
        n = len(body) if isinstance(body, (list, dict)) else None
        res[path] = {"status": r.status, "type": type(body).__name__, "len": n, "keys": list(body)[:12] if isinstance(body, dict) else None}
    b.close()
txt = json.dumps(res, indent=1)
assert u not in txt and p not in txt
open(OUT + "/live_probe.json", "w").write(txt)
for k, v in res.items(): print(k, v["status"], v["type"], v["len"])
