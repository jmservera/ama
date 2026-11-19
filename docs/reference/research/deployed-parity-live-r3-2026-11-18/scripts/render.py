"""Render each staff route on the demo at desktop size; record title, heading, failed responses and console errors."""
import re
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
routes = [("cases", "/app#/"), ("all", "/app#/all"), ("overview", "/app#/overview"), ("progress", "/app#/progress"),
          ("visits", "/app#/visits"), ("funding", "/app#/funding"), ("finance", "/app#/finance"),
          ("capacity", "/app#/capacity"), ("closed", "/app#/closed"), ("assistants", "/app#/assistants"),
          ("time", "/app#/time"), ("aftercare", "/app#/aftercare"), ("screens", "/app#/screens"),
          ("law", "/law.html")]
with sync_playwright() as pw:
    ctx = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json", viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    bad, tiles, cons = [], [], []
    pg.on("response", lambda r: (bad.append((r.status, re.sub(r"\?.*", "", r.url)[-60:])) if r.status >= 400 else None,
                                 tiles.append(r.status) if "tile.openstreetmap" in r.url else None))
    pg.on("console", lambda m: cons.append(m.text[:80]) if m.type == "error" else None)
    for n, u in routes:
        bad.clear(); tiles.clear(); cons.clear()
        pg.goto(H + u)
        pg.wait_for_timeout(4500)
        pg.screenshot(path=f"screens/staff-{n}.png")
        h = pg.locator("h1,h2").first
        head = h.inner_text()[:70].replace("\n", " ") if h.count() else "-"
        main = pg.locator("main").inner_text()[:140].replace("\n", " ") if pg.locator("main").count() else "-"
        print(f"{n} | {pg.title()} | h={head} | tiles={len(tiles)}{sorted(set(tiles))} | failed={bad[:4]} | console_errors={len(cons)} | main={main}")
