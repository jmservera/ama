"""Live demo probe for issue 119. Credentials read at runtime, never printed; only redacted facts retained."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")
SECRETS = [user, pw]

def clean(t):
    for s in SECRETS:
        t = t.replace(s, "[redacted]")
    return re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t)

def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

out = {"tile": None, "keyboard": {}}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    def on_resp(r):
        if "tile.openstreetmap.org" in r.url and out["tile"] is None:
            h = r.request.all_headers(); rh = r.all_headers()
            out["tile"] = {"status": r.status, "req_referer": h.get("referer"), "req_user_agent": h.get("user-agent"),
                           "resp_cache_control": rh.get("cache-control"), "resp_content_type": rh.get("content-type"),
                           "resp_access_control": rh.get("access-control-allow-origin")}
    page.on("response", on_resp)
    page.goto(APP + "/app", wait_until="domcontentloaded")
    if "login" in page.url: login(page)
    page.goto(APP + "/app#/overview"); page.reload()
    page.wait_for_load_state("networkidle"); page.wait_for_timeout(3000)
    summ = page.locator("details.maplist summary")
    summ.focus()
    out["keyboard"]["summary_focused"] = page.evaluate("document.activeElement.tagName")
    page.keyboard.press("Enter"); page.wait_for_timeout(500)
    out["keyboard"]["open_after_enter"] = page.evaluate("document.querySelector('details.maplist').open")
    page.keyboard.press("Tab")
    out["keyboard"]["next_focus"] = page.evaluate("[document.activeElement.tagName, document.activeElement.getAttribute('href')&&document.activeElement.getAttribute('href').slice(0,8)]")
    page.screenshot(path=f"{OUT}/keyboard-focus-list-1366.png")
    page.keyboard.press("Enter"); page.wait_for_timeout(1500)
    out["keyboard"]["after_activate_hash"] = page.evaluate("location.hash").split("/")[1] if "/" in page.evaluate("location.hash") else page.evaluate("location.hash")
    out["keyboard"]["h1_after"] = page.locator("h1").first.inner_text()
    page.screenshot(path=f"{OUT}/keyboard-opened-case-1366.png")
    # tile-blocked state: abort the provider host, list must still work
    page.goto(APP + "/app#/overview")
    b.close()
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.route("https://tile.openstreetmap.org/**", lambda r: r.abort())
    page.goto(APP + "/app", wait_until="domcontentloaded")
    if "login" in page.url: login(page)
    page.goto(APP + "/app#/overview"); page.reload()
    page.wait_for_load_state("networkidle"); page.wait_for_timeout(3000)
    page.locator("details.maplist summary").click(); page.wait_for_timeout(800)
    out["blocked"] = {"status_texts": page.locator(".map-info [role=status]").all_inner_texts(),
                      "list_items": page.locator("details.maplist ul li").count()}
    page.locator("details.maplist").scroll_into_view_if_needed()
    page.screenshot(path=f"{OUT}/tiles-blocked-list-works-1366.png")
    b.close()
json.dump(out, open(f"{OUT}/probe3.json", "w"), indent=1)
print(json.dumps(out)[:1500])
