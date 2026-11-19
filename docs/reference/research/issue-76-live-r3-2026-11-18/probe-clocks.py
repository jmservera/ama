import json, os
from playwright.sync_api import sync_playwright
H = os.environ["DEMO_API_URL"]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(storage_state=os.environ["I76_SCRATCH"] + "/state-staff.json")
    r = c.request.get(H + "/api/cases", timeout=90000)
    cases = r.json()
    cases = cases["items"]
    out = dict(status=r.status, n=len(cases), rows=[])
    for cs in cases:
        d = c.request.get(H + "/api/cases/" + cs["id"], timeout=90000).json()
        w = d.get("work") or {}
        hz, sg = w.get("hazard_clocks") or [], w.get("safeguarding_clocks") or []
        out["rows"].append(dict(
            id=cs["id"],
            hazard=[dict(owner_named=x.get("owner_named"), owner_role=x.get("owner_role"),
                         response_state=x.get("response_state"), elapsed_hours=x.get("elapsed_hours"),
                         aware_at=x.get("aware_at"), response_due_at=x.get("response_due_at"),
                         as_of=x.get("as_of")) for x in hz],
            safeguarding=[dict(owner_named=x.get("owner_named"), response_state=x.get("response_state"),
                               elapsed_hours=x.get("elapsed_hours"), response_due_at=x.get("response_due_at"))
                          for x in sg],
            hazard_keys=sorted(hz[0].keys()) if hz else None))
    print(json.dumps(out, indent=1))
