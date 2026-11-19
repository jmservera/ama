import sys, re, json
from playwright.sync_api import sync_playwright
H="https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
D="shots/"
routes=[("cases","/app#/"),("overview","/app#/overview"),("progress","/app#/progress"),("visits","/app#/visits"),("funding","/app#/funding"),("finance","/app#/finance"),("time","/app#/time"),("law","/law.html")]
with sync_playwright() as pw:
    c=pw.chromium.launch().new_context(storage_state="/tmp/state-staff.json",viewport={"width":1440,"height":900}); pg=c.new_page()
    bad=[]; tiles=[]
    pg.on("response",lambda r:(bad.append((r.status,re.sub(r"\?.*","",r.url)[-80:])) if r.status>=400 else None, tiles.append(r.status) if "tile.openstreetmap" in r.url else None))
    for n,u in routes:
        bad.clear(); tiles.clear()
        pg.goto(H+u); pg.wait_for_timeout(4000); pg.reload() if False else None
        pg.screenshot(path=D+f"staff-{n}.png")
        print(n, pg.title(), "tiles", len(tiles), set(tiles), "bad", bad[:4], "leaflet", pg.locator(".leaflet-container").count(), "h1", pg.locator("h1,h2").first.inner_text()[:60] if pg.locator("h1,h2").count() else None)
