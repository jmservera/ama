"""Control probe: unrelated unknown paths behave identically to discovery paths."""
from playwright.sync_api import sync_playwright
from common import *
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    for path in ["/api/zzz-nonexistent-control", "/api/discovery-assistant"]:
        s, d = call(pg, "GET", path); res["GET " + path] = [s, scrub(str(d)[:100])]
        s, d = call(pg, "POST", path, {}); res["POST " + path] = [s, scrub(str(d)[:100])]
    b.close()
json.dump(res, open(f"{OUT}/probe2.json", "w"), indent=1); print(json.dumps(res, indent=1))
