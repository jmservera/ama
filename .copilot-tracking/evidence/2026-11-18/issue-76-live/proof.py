"""Issue 76 live proof: hazard and safeguarding clock and named owner. Reuses a session saved by explore.py."""
import json, os, re
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 1000}, storage_state="/tmp/s76.json"); page = c.new_page()
    items = c.request.get(APP + "/api/cases").json()["items"]
    out["total_cases"] = len(items)
    out["cases_with_hazard_flag"] = [x["id"] for x in items if x.get("hazard")]
    out["cases_with_support_flag"] = len([x for x in items if x.get("support")])
    clocks = {x["id"]: (x["work"].get("hazard_clocks"), x["work"].get("safeguarding_clocks")) for x in items if x.get("work")}
    out["list_clock_counts"] = {k: [len(v[0] or []), len(v[1] or [])] for k, v in clocks.items() if v[0] or v[1]}
    hz = items and [x for x in items if x.get("hazard")][0]["id"]
    d = c.request.get(f"{APP}/api/cases/{hz}")
    out["detail_status"] = d.status
    dj = d.json()
    out["detail_keys_hazard"] = {k: (len(v) if isinstance(v, list) else None) for k, v in dj.items() if "hazard" in k or "safeguard" in k}
    h = (dj.get("hazards") or [])
    out["detail_hazards"] = [{k: v for k, v in x.items() if k in ("id","clock_text","escalation_clock","owner","accountable_owner","aware_at","response_due_at","responded_at","status","category","urgency")} for x in h]
    out["detail_safeguarding"] = [{k: v for k, v in x.items() if k in ("id","owner","owner_role","referred_at","response_due_at","status")} for x in (dj.get("safeguarding_items") or [])]
    wk = dj.get("work", {})
    out["detail_work_clocks"] = {"hazard": wk.get("hazard_clocks"), "safeguarding": wk.get("safeguarding_clocks")}
    page.goto(APP + "/", wait_until="networkidle"); page.wait_for_timeout(2500)
    page.screenshot(path=f"{OUT}/queue-default.png")
    out["page_text_has_hazard_clock"] = "Hazard clock" in page.inner_text("body")
    out["page_text_has_accountable_owner"] = "Accountable owner" in page.inner_text("body")
    b.close()
print(json.dumps(out, indent=1))
