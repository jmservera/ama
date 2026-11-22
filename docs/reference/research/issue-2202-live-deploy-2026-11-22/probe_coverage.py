"""Issue 2202: count homes on the live map with a sensor reading and its age. Credentials read at runtime, never printed."""
import json, os, datetime as dt
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(H + "/sign-in")
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
    from collections import Counter
    r = c.request.get(H + "/api/map?zoom=18")
    d = r.json(); print("status", r.status, "total", d["total"], "cap", d["cap"])
    seen = {}

    def walk(box, depth=0):
        q = c.request.get(H + "/api/map?zoom=18&bbox=" + ",".join(f"{v:.6f}" for v in box)).json()
        its = q["items"]
        if any((x.get("sensor") or {}).get("state") == "not-loaded" for x in its) and depth < 8 and len(its) > 1:
            s_, w, n, e = box; ms, mw = (s_ + n) / 2, (w + e) / 2
            for sub in ((s_, w, ms, mw), (s_, mw, ms, e), (ms, w, n, mw), (ms, mw, n, e)):
                walk(sub, depth + 1)
        else:
            for x in its:
                if (x.get("sensor") or {}).get("state") != "not-loaded":
                    seen[x["id"]] = x
    walk(tuple(d["bounds"]))
    items = list(seen.values())
    print("homes with loaded sensor summary", len(items))
    sensors = [x.get("sensor") for x in items]
    print("sensor sample", json.dumps(next((s for s in sensors if s), None))[:400])
    st = Counter((s or {}).get("state") or ("none" if not s else "present") for s in sensors)
    withr = [s for s in sensors if s and isinstance(s.get("temperature_c"), (int, float))]
    now = dt.datetime.now(dt.timezone.utc)
    def age(s):
        t = s.get("observed_at")
        return (now - dt.datetime.fromisoformat(t.replace("Z", "+00:00"))).total_seconds() / 60 if t else None
    ages = [a for a in map(age, withr) if a is not None]
    res = {"total": len(items), "with_reading": len(withr), "states": dict(st),
           "age_min_le_15": sum(a <= 15 for a in ages), "age_min_le_60": sum(a <= 60 for a in ages),
           "newest_age_min": min(ages) if ages else None, "measured_utc": now.isoformat()}
    print(json.dumps(res)); json.dump(res, open(OUT + "/live_coverage.json", "w"), indent=1)
    b.close()
