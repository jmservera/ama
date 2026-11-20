"""Live: submit the real acknowledge form with an unknown record id; nothing can be written."""
import json, re
from playwright.sync_api import sync_playwright
from login_lib import APP, sign_in
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    sign_in(page)
    cid = c.request.get(APP + "/api/cases").json()["items"][0]["id"]
    before = c.request.get(f"{APP}/api/cases/{cid}").json()
    page.goto(f"{APP}/api/cases/{cid}?view=nomination-routes-html", wait_until="networkidle")
    reqs = []
    page.on("request", lambda r: reqs.append((r.method, r.url.split("/api")[-1], r.headers.get("content-type"), "x-zf-csrf" in r.headers)) if r.method == "POST" else None)
    resp = []
    page.on("response", lambda r: resp.append(r.status) if r.request.method == "POST" else None)
    out["forms"] = page.eval_on_selector_all("form", "e=>e.map(f=>f.querySelector('[name=action]')?.value)")
    page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    f = page.query_selector("form")
    out["fields"] = f.eval_on_selector_all("input,select,textarea","e=>e.map(x=>[x.name,x.type,x.required])")
    for sel, v in (("[name=id]", "SYN-NONE"), ("[name=expected_version]", "1")):
        el = f.query_selector(sel)
        if el: el.fill(v)
    f.query_selector("button[type=submit], button").click()
    page.wait_for_timeout(2500)
    out["posts"] = reqs; out["post_statuses"] = resp
    out["status_text"] = (page.inner_text("[role=status], [role=alert], .status, #route-status") or "")[:120] if page.query_selector("[role=status], [role=alert], .status, #route-status") else None
    page.screenshot(path="/tmp/p1837/live-form-submit.png")
    out["case_unchanged"] = before == c.request.get(f"{APP}/api/cases/{cid}").json()
    b.close()
print(json.dumps(out, indent=1))
