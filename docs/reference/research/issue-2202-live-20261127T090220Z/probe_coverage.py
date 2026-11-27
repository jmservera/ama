"""Fetch 4x4 map tiles with sensor states for the readings coverage tool. Credentials read at runtime."""
import json, os
from playwright.sync_api import sync_playwright
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_sensor_loop.py")).read().split("import json as _j")[0].replace("OUT = os.path.dirname(os.path.abspath(__file__))", "OUT = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.'"))
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT + "/tiles", exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(); pg = c.new_page(); login(pg)
    r = c.request.get(H + "/api/map", timeout=90000)
    items = r.json().get("items", [])
    pts = [(i["lat"], i["lon"]) for i in items if "lat" in i] or [(i["latitude"], i["longitude"]) for i in items]
    la = [p[0] for p in pts]; lo = [p[1] for p in pts]
    print("overview status", r.status, "items", len(items), min(la), max(la), min(lo), max(lo))
    s0, n0, w0, e0 = min(la) - .01, max(la) + .01, min(lo) - .01, max(lo) + .01
    k = [0]
    def tile(s, w, n, e, depth=0):
        t = c.request.get(f"{H}/api/map?sensors=1&bbox={s},{w},{n},{e}", timeout=120000)
        its = t.json().get("items", []) if t.ok else []
        if len(its) > 100 and depth < 6:
            ms, mw = (s + n) / 2, (w + e) / 2
            for a, b2, c2, d in ((s, w, ms, mw), (s, mw, ms, e), (ms, w, n, mw), (ms, mw, n, e)):
                tile(a, b2, c2, d, depth + 1)
            return
        open(f"{OUT}/tiles/tile-{k[0]:03d}.json", "w").write(json.dumps({"items": its})); k[0] += 1
    tile(s0, w0, n0, e0)
    print("tiles", k[0])
    b.close()
