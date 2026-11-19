"""Live demo probe for issue 119. Credentials read at runtime, never printed; only redacted facts retained."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.<app-fqdn-suffix>"
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

out = {"tile_requests": [], "tile_failures": [], "console": []}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.on("request", lambda r: out["tile_requests"].append(r.url) if "tile." in r.url else None)
    page.on("requestfailed", lambda r: out["tile_failures"].append(r.url))
    page.on("console", lambda m: out["console"].append(clean(m.text)[:200]))
    page.goto(APP + "/app", wait_until="domcontentloaded")
    if "login" in page.url: login(page)
    page.goto(APP + "/app#/overview"); page.reload()
    page.wait_for_load_state("networkidle"); page.wait_for_timeout(3000)
    me = c.request.get(APP + "/api/me").json()
    out["me_map"] = me.get("map")
    out["csp"] = c.request.get(APP + "/app").headers.get("content-security-policy")
    out["landing_url"] = page.url.replace(APP, "<app>")
    out["leaflet_present"] = page.locator("#leaflet").count()
    out["maplist_present"] = page.locator("details.maplist").count()
    page.screenshot(path=f"{OUT}/landing.png")
    if out["leaflet_present"]:
        page.locator("details.maplist summary").scroll_into_view_if_needed()
        page.screenshot(path=f"{OUT}/map-desktop-1366.png")
        page.locator("details.maplist summary").click()
        page.wait_for_timeout(1500)
        out["list_items"] = page.locator("details.maplist ul li").count()
        out["list_first_items"] = [clean(t)[:120] for t in page.locator("details.maplist ul li").all_inner_texts()[:5]]
        out["tile_note"] = page.locator(".map-info [role=status]").all_inner_texts()
        out["tile_imgs_loaded"] = page.evaluate("[...document.querySelectorAll('img.leaflet-tile')].filter(i=>i.complete&&i.naturalWidth>0).length")
        out["attribution"] = clean(page.locator(".leaflet-control-attribution").inner_text()) if page.locator(".leaflet-control-attribution").count() else None
        page.screenshot(path=f"{OUT}/map-list-open-1366.png")
        out["aria_snapshot_map_info"] = clean(page.locator("aside.map-info").aria_snapshot())
    b.close()
out["tile_requests"] = {"count": len(out["tile_requests"]), "sample": out["tile_requests"][:3]}
json.dump(out, open(f"{OUT}/probe2.json", "w"), indent=1)
print({k: (v if k in ("leaflet_present","maplist_present","list_items","tile_imgs_loaded","landing_url") else "...") for k, v in out.items()})
