"""Quadtree-tile /api/map?sensors=1 so every tile holds at most 100 homes, then save the merged snapshots. Sign-in values are read at run time, never printed."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
API = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
u = (Path.home() / ".ama-test-user-id").read_text().strip()
p = (Path.home() / ".ama-test-user").read_text().strip()
base = json.loads((OUT / "map-snapshot.json").read_text())["items"]
lats = [i["lat"] for i in base]; lons = [i["lon"] for i in base]
snaps = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(API + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000):
                pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception:
            pass
    pg.wait_for_load_state("networkidle")

    def tile(s, w, n, e, depth=0):
        r = c.request.get(f"{API}/api/map?sensors=1&zoom=12&bbox={s},{w},{n},{e}", timeout=120000)
        if not r.ok:
            return
        items = r.json().get("items", [])
        if any((i.get("sensor") or {}).get("state") == "not-loaded" for i in items) and depth < 8:
            ms, mw = (s + n) / 2, (w + e) / 2
            for a in ((s, w, ms, mw), (s, mw, ms, e), (ms, w, n, mw), (ms, mw, n, e)):
                tile(*a, depth + 1)
        else:
            snaps.append({"items": items})

    tile(min(lats) - 1e-4, min(lons) - 1e-4, max(lats) + 1e-4, max(lons) + 1e-4)
    b.close()
for k, s in enumerate(snaps):
    (OUT / f"tiles/tile-{k:03d}.json").write_text(json.dumps(s))
print(len(snaps), "tiles")
