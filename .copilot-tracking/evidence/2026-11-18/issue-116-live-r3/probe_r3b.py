"""Round 3b: context of reason-value hits on continuity, data-protection and choice-queue csv (synthetic values; contexts trimmed)."""
import json, os, re
exec(open(os.path.dirname(os.path.abspath(__file__)) + "/probe_r3.py").read().split("out = {")[0])
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    items = c.request.get(APP + "/api/cases?view=all").json()["items"]
    vals = {}
    for it in items:
        d = c.request.get(APP + "/api/cases/" + it["id"]).json()
        for f in ("adjustment", "priority_support"):
            v = d.get("resident", {}).get(f)
            if isinstance(v, str) and len(v) > 3: vals[v] = f
    out["values"] = vals
    for path in ("/api/continuity", "/api/data-protection", "/api/resident/choice-queue.csv?limit=2", "/api/continuity/export"):
        t = c.request.get(APP + path).text(); ctx = []
        for v in vals:
            for m in list(re.finditer(re.escape(v), t))[:2]:
                ctx.append(re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t[max(0, m.start() - 90): m.end() + 40]))
        out[path] = {"hits": sum(t.count(v) for v in vals), "contexts": ctx[:4]}
    b.close()
json.dump(out, open(os.path.dirname(os.path.abspath(__file__)) + "/probe_r3b.json", "w"), indent=1)
print(json.dumps(out, indent=1))
