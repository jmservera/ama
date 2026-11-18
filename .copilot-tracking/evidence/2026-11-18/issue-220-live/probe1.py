from playwright.sync_api import sync_playwright
from common import *
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    s, me = call(pg, "GET", "/api/me"); res["me"] = scrub({"s": s, "role": me.get("user", {}).get("role")})
    s, cases = call(pg, "GET", "/api/cases")
    lst = cases if isinstance(cases, list) else cases.get("items", [])
    res["n"] = len(lst); res["sample_keys"] = sorted(lst[0].keys()) if lst else None
    summ = []
    for cs in lst[:60]:
        summ.append({k: cs.get(k) for k in ("id", "stage", "hazards", "awaiting_hazard_action", "closed") if k in cs})
    res["summ"] = summ[:12]
    cid = lst[0]["id"]
    s, d = call(pg, "GET", f"/api/cases/{cid}")
    res["detail_keys"] = sorted(d.keys()) if isinstance(d, dict) else d
    res["nom_perms"] = scrub(d.get("nomination_permissions"))
    res["hazards"] = scrub(d.get("hazards"))
    s, h = call(pg, "GET", f"/api/cases/{cid}?view=nomination-routes-html"); res["html"] = (s, str(h)[:300])
    s, pr = call(pg, "GET", "/api/assistants/proposals"); res["proposals"] = (s, str(pr)[:600])
    b.close()
json.dump(res, open("probe1.json", "w"), indent=1); print(json.dumps(res, indent=1)[:5000])
