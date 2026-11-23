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
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    login(pg)
    for path in ("/api/me", "/api/stats", "/api/progress"):
        r = c.request.get(H + path)
        try: body = r.json()
        except Exception: body = None
        res[path] = {"status": r.status, "keys": list(body)[:30] if isinstance(body, dict) else None}
        if isinstance(body, dict) and "ai_consumption_economics" in body: res["econ_" + path] = body["ai_consumption_economics"]
    pg.goto(H + "/app#/"); pg.wait_for_timeout(6000)
    pg.get_by_role("link", name="Overview").first.click() if pg.get_by_role("link", name="Overview").count() else None
    pg.wait_for_selector("#ai-economics-heading", timeout=15000)
    found = None
    for h in ("#ai-economics-heading", "text=AI consumption economics", "text=AI economics"):
        if pg.locator(h).count():
            found = h; pg.locator(h).first.scroll_into_view_if_needed(); break
    res["ui_locator"] = found
    pg.screenshot(path=OUT + "/overview-ai-economics.png")
    if found: res["ui_text"] = pg.locator(found).first.locator("xpath=..").inner_text()[:1800]
    pg.screenshot(path=OUT + "/overview-ai-economics.png")
    b.close()
txt = json.dumps(res, indent=1)
assert u not in txt and p not in txt
open(OUT + "/live_probe.json", "w").write(txt)
print(json.dumps({k: v for k, v in res.items() if k.startswith("/")}))
print("ui", res.get("ui_locator"))
