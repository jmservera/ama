"""Read-only live probe: role, script presence and routes view for the first listed cases."""
import json, re
from playwright.sync_api import sync_playwright
from login_lib import APP, sign_in

out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    sign_in(page)
    me = c.request.get(APP + "/api/me")
    j = me.json() if me.status == 200 else {}
    out["me_status"] = me.status
    out["me_keys"] = sorted(j)[:20]
    out["role"] = (j.get("user") or {}).get("role") if isinstance(j.get("user"), dict) else j.get("role")
    for name in ("app.js", "nomination-routes.js", "chat.js"):
        r = c.request.get(f"{APP}/{name}")
        out[f"static_{name}"] = r.status
    cases = c.request.get(APP + "/api/cases").json()
    ids = [x["id"] for x in cases["items"]][:3]
    out["case_ids_sample"] = ids
    out["total"] = cases["total"]
    for cid in ids[:2]:
        h = c.request.get(f"{APP}/api/cases/{cid}?view=nomination-routes-html")
        t = h.text() if h.status == 200 else ""
        out[f"html_{cid}"] = {"status": h.status, "forms": len(re.findall(r"<form ", t)),
                              "script_tag": "nomination-routes.js" in t}
    b.close()
print(json.dumps(out, indent=1))
