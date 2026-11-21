"""Issue 2201 live probe: staff-app sensor readings and map. Reads sign-in at runtime via the shared helper; prints no credential."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-11-18", "issue-155-live"))
from common import APP, login, mask_emails
from playwright.sync_api import sync_playwright

CASES = ["ZF-2025-0031", "ZF-2025-0029", "ZF-2025-0030", "ZF-2025-0148", "ZF-2025-0331"]
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    login(page)
    page.goto(APP + "/app#/overview", wait_until="domcontentloaded")
    page.wait_for_timeout(9000)
    page.get_by_role("link", name="Overview", exact=True).click()
    page.wait_for_timeout(6000)
    page.get_by_role("button", name="Expand map", exact=True).scroll_into_view_if_needed()
    page.wait_for_timeout(3000)
    mask_emails(page)
    page.screenshot(path=os.path.join(HERE, "employee-map.png"))
    out = {"now_utc": page.evaluate("new Date().toISOString()")}
    m = page.evaluate("""async()=>{const r=await fetch('/api/map?zoom=14');return {s:r.status,j:r.ok?await r.json():null}}""")
    j = m["j"] or {}
    out["map"] = {"status": m["s"], "keys": sorted(j.keys()) if isinstance(j, dict) else None}
    for k, v in (j.items() if isinstance(j, dict) else []):
        if isinstance(v, list):
            out["map"][k + "_len"] = len(v)
            out["map"][k + "_first"] = v[0] if v else None
        elif isinstance(v, dict):
            out["map"][k + "_keys"] = sorted(v)[:20]
    out["sensors"] = {}
    for c in CASES:
        r = page.evaluate("""async(c)=>{const r=await fetch('/api/cases/'+c+'/sensors');return {s:r.status,j:r.ok?await r.json():null}}""", c)
        out["sensors"][c] = r
    json.dump(out, open(os.path.join(HERE, "probe-readings.json"), "w"), indent=1, default=str)
    print(json.dumps(out, default=str)[:6000])
    b.close()
