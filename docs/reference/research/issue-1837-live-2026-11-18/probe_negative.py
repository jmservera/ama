"""Live negative probe: transport, CSRF and isolation responses that write nothing (all requests are refused or hit no record)."""
import json
from playwright.sync_api import sync_playwright
from login_lib import APP, sign_in

out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    sign_in(page)
    cases = c.request.get(APP + "/api/cases").json()["items"]
    cid = cases[0]["id"]
    page.goto(APP + "/app", wait_until="networkidle")
    before = c.request.get(f"{APP}/api/cases/{cid}").json()
    url = f"/api/cases/{cid}/resident"
    form = "action=nomination_acknowledge&case_id=" + cid + "&id=SYN-NONE&expected_version=1"
    JS = """async ([u, ct, body, hdr]) => {
      const h = {"Content-Type": ct}; if (hdr) h["X-ZF-CSRF"] = "1";
      const r = await fetch(u, {method: "POST", headers: h, body, credentials: "same-origin"});
      return [r.status, (await r.text()).slice(0, 90)];
    }"""
    f = lambda u, ct, body, hdr: page.evaluate(JS, [u, ct, body, hdr])
    U = "application/x-www-form-urlencoded"; J = "application/json"
    out["urlencoded_with_csrf_header"] = f(url, U, form, True)
    out["urlencoded_without_csrf_header"] = f(url, U, form, False)
    out["json_without_csrf_header"] = f(url, J, json.dumps({"action": "nomination_acknowledge", "case_id": cid}), False)
    out["malformed_json_with_header"] = f(url, J, "{not json", True)
    out["unknown_case_with_header"] = f("/api/cases/ZF-NOPE-0000/resident", J, json.dumps({"action": "nomination_acknowledge", "case_id": "ZF-NOPE-0000", "id": "X", "expected_version": 1}), True)
    out["body_case_differs_from_url"] = f(url, J, json.dumps({"action": "nomination_acknowledge", "case_id": cases[1]["id"], "id": "X", "expected_version": 1}), True)
    after = c.request.get(f"{APP}/api/cases/{cid}").json()
    out["case_unchanged_after_probes"] = before == after
    h = c.request.get(f"{APP}/api/cases/{cid}?view=nomination-routes-html")
    out["routes_page_has_script_tag"] = "nomination-routes.js" in h.text()
    out["script_asset_status"] = c.request.get(APP + "/nomination-routes.js").status
    b.close()
print(json.dumps(out, indent=1))
