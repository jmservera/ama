"""Issue 184 live probe: employee map and sensors, resident showcase sensor card. Reads sign-in at runtime; prints no credential."""
import json, os, sys
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-11-18", "issue-155-live"))
from common import APP, login, mask_emails
from playwright.sync_api import sync_playwright

RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
RE, RP = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
CASES = ["ZF-2025-0030", "ZF-2025-0331", "ZF-2025-0031"]
out = {}
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
    out["now_utc"] = page.evaluate("new Date().toISOString()")
    m = page.evaluate("""async()=>{const r=await fetch('/api/map?zoom=14');return {s:r.status,j:r.ok?await r.json():null}}""")
    j = m["j"] or {}
    out["map"] = {"status": m["s"], **{k + "_len": len(v) for k, v in j.items() if isinstance(v, list)}}
    out["sensors"] = {}
    for c in CASES:
        r = page.evaluate("""async(c)=>{const r=await fetch('/api/cases/'+c+'/sensors');return {s:r.status,j:r.ok?await r.json():null}}""", c)
        jj = r["j"] or {}
        rd = jj.get("readings") or []
        out["sensors"][c] = {"status": r["s"], "state": jj.get("state"), "freshness": jj.get("freshness"),
                             "readings": len(rd), "latest": max((x.get("observed_at", "") for x in rd), default=None),
                             "keys": sorted(jj)}
    # resident showcase
    rp = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    rp.goto(RES + "/", wait_until="networkidle", timeout=120000)
    rp.fill("input[type=email], input[name=email], #email", RE)
    rp.fill("input[type=password]", RP)
    with rp.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        rp.keyboard.press("Enter")
    out["resident_login"] = ri.value.status
    rp.wait_for_selector("#account:not([hidden])", timeout=90000)
    rp.wait_for_timeout(2000)
    sid = rp.request.get(RES + "/demo/session").json()
    v = rp.request.get(RES + "/demo/view", headers={"X-Resident-Session": sid.get("session_id", "")})
    vj = v.json() if v.ok else {}
    sk = {k: (vj[k] if not isinstance(vj[k], (dict, list)) else None) for k in vj if "sensor" in k.lower()}
    out["resident_view"] = {"status": v.status, "sensor_keys": sorted(k for k in vj if "sensor" in k.lower())}
    for k in vj:
        if "sensor" in k.lower() and isinstance(vj[k], dict):
            out["resident_view"][k] = {kk: (vv if not isinstance(vv, (list, dict)) else "len=%d" % len(vv)) for kk, vv in vj[k].items()}
    h = (vj.get("sensors") or {}).get("history") or []
    out["resident_view"]["history_n"] = len(h)
    out["resident_view"]["history_latest"] = max((x["observed_at"] for x in h), default=None)
    out["resident_view"]["history_earliest"] = min((x["observed_at"] for x in h), default=None)
    out["resident_view"]["freshness_detail"] = (vj.get("sensors") or {}).get("freshness")
    sec = rp.locator("text=/sensor/i").first
    try:
        sec.scroll_into_view_if_needed()
    except Exception:
        pass
    rp.wait_for_timeout(1000)
    rp.screenshot(path=os.path.join(HERE, "resident-signed-in.png"), full_page=True)
    rp.request.post(RES + "/demo/logout", headers={"Origin": RES, "X-CSRF-Token": sid.get("csrf", "")})
    json.dump(out, open(os.path.join(HERE, "probe-result.json"), "w"), indent=1, default=str)
    print(json.dumps(out, default=str)[:5000])
    b.close()
