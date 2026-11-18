"""Issue 81 live probe: form-encoded nomination submissions on the synthetic demo.
Credentials are read at run time by common.py and never printed or saved."""
import json
import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "../issue-130-live-r2")
from common import APP, OUT as _unused, scrub, session, call  # noqa: E402

CID = "ZF-2025-0331"
OUT = "."
FORM_JS = """async([p,b])=>{const x=await fetch(p,{method:'POST',headers:{'Content-Type':
 'application/x-www-form-urlencoded','X-ZF-CSRF':'1'},body:new URLSearchParams(b).toString()});
 const t=await x.text();let j;try{j=JSON.parse(t)}catch(e){j={_text:t.slice(0,300)}};return [x.status,j]}"""
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    s, d = call(pg, "GET", f"/api/cases/{CID}")
    res["case_status"] = s
    res["n_records_before"] = len(d.get("nomination_records") or [])
    s, h = call(pg, "GET", f"/api/cases/{CID}?view=nomination-routes-html")
    txt = json.dumps(h)
    res["route_view_status"] = s
    res["forms_present"] = {k: (k in txt) for k in ("nomination_acknowledge", "nomination_correct", "challenge_open")}
    res["form_script_present"] = "nomination-route-forms" in txt
    # Form-encoded bodies use a nonexistent nomination id: a transport rejection (400 "Could not read that.")
    # differs from a domain rejection; nothing can be written for an unknown id.
    for action in ("nomination_acknowledge", "nomination_correct", "challenge_open"):
        s, j = pg.evaluate(FORM_JS, [f"/api/cases/{CID}/resident",
                                     {"action": action, "case_id": CID, "nomination_id": "NOM-SYN-DOES-NOT-EXIST"}])
        res[f"form_{action}"] = scrub({"status": s, "err": j.get("error") if isinstance(j, dict) else j})
    s, d2 = call(pg, "GET", f"/api/cases/{CID}")
    res["n_records_after"] = len(d2.get("nomination_records") or [])
    pg.goto(APP + f"/api/cases/{CID}?view=nomination-routes-html", wait_until="networkidle")
    pg.screenshot(path="route-view-81.png", full_page=True)
    b.close()
json.dump(res, open("probe.json", "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
