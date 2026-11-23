import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, scrub, session, call
from playwright.sync_api import sync_playwright

PATHS = ["/api/governance", "/api/assistants", "/api/ai/report"]
out = {}
with sync_playwright() as p:
    b, pg = session(p)
    for path in PATHS:
        st, j = call(pg, "GET", path)
        keep = {"status": st}
        if isinstance(j, dict):
            for k in ("rai_exercise_acceptance", "real_ai_delivery_gate"):
                if k in j:
                    keep[k] = j[k]
            live = j.get("live")
            if isinstance(live, dict):
                for k in ("rai_exercise_acceptance", "real_ai_delivery_gate"):
                    if k in live:
                        keep["live." + k] = live[k]
            keep["keys"] = sorted(j)[:30]
        out[path] = keep
    pg.screenshot(path=os.path.join(OUT, "workbench.png"))
    b.close()
out = scrub(out)
json.dump(out, open(os.path.join(OUT, "probe.json"), "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
