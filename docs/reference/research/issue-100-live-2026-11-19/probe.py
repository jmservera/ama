import json, os, re, sys
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
def walk(o, pre="", out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, pre + k + ".", out)
    elif isinstance(o, list):
        for i, v in enumerate(o[:5]): walk(v, f"{pre}{i}.", out)
    else: out.append((pre.rstrip("."), o))
    return out
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    me = c.request.get(H + "/api/me"); print("me", me.status, json.dumps({k: v for k, v in (me.json() if me.ok else {}).items() if k in ("role", "roles")}))
    r = c.request.get(H + "/api/progress"); print("progress", r.status)
    d = r.json() if r.ok else {}
    print("keys", list(d)[:30]); print("subkeys", {k: list(v)[:25] for k, v in d.items() if isinstance(v, dict)})
    def find(o):
        if isinstance(o, dict):
            if "ai_consumption_economics" in o: return o["ai_consumption_economics"]
            for v in o.values():
                x = find(v)
                if x is not None: return x
    eco = find(d)
    json.dump(eco, open(OUT + "/ai-economics.json", "w"), indent=1)
    print(json.dumps(eco)[:1800])
    pg.screenshot(path=OUT + "/screens/01-landing.png")
    for path in ("/progress", "/#progress", "/#/progress"):
        pg.goto(H + path); pg.wait_for_timeout(2500)
        if pg.locator("#ai-economics-heading").count():
            pg.locator("#ai-economics-heading").scroll_into_view_if_needed()
            pg.screenshot(path=OUT + "/screens/02-ai-economics.png"); print("heading at", path)
            print(pg.locator("#ai-economics-heading").locator("xpath=..").inner_text()[:1500]); break
    b.close()
