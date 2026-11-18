"""Live demo sign-in proof (issue 349). Reads credentials at runtime; prints only redacted facts."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
res_l = [x.strip() for x in rd(".ama-resident-test-user") if x.strip()]
res = {"user": res_l[0], "pw": res_l[1]}
GUID = re.compile(r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", re.I)

def shape(d, acct):
    u = d.get("user", {}) if isinstance(d, dict) else {}
    return {
        "role": u.get("role"), "app_roles": u.get("app_roles"), "view_only": u.get("view_only"),
        "identity_source": u.get("identity_source"), "auth_provider": u.get("auth_provider"),
        "tid_is_guid": bool(GUID.match(str(u.get("tid", "")))), "oid_is_guid": bool(GUID.match(str(u.get("oid", "")))),
        "account_provider": d.get("account", {}).get("provider"),
        "services": d.get("services"), "navigation_count": len(d.get("navigation", []) or []),
        "bound": bool(u.get("bound")),
    }

def login(page, acct):
    page.fill("input[name=loginfmt]", acct["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", acct["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

def run(p, name, acct, tag):
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    r = {"account": name}
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    r["redirected_to_entra"] = "login.microsoftonline.com" in page.url
    page.screenshot(path=f"{OUT}/{tag}-1-entra-redirect.png")
    try:
        login(page, acct)
        r["callback_returned_to_app"] = page.url.startswith(APP)
        resp = c.request.get(APP + "/api/me")
        r["me_status"] = resp.status
        if resp.status == 200:
            r["me"] = shape(resp.json(), acct)
        else:
            r["me_body_len"] = len(resp.text())
        page.goto(APP + "/", wait_until="networkidle")
        r["workbench_url_path"] = re.sub(r"^https?://[^/]+", "", page.url)[:60]
        page.evaluate("""u=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""", acct["user"])
        page.screenshot(path=f"{OUT}/{tag}-2-after-signin.png")
        for path in ["/api/cases", "/api/workorders/x/job-pack", "/api/law/alerts"]:
            q = c.request.get(APP + path); r.setdefault("probe_status", {})[path] = q.status
    except Exception as e:
        r["error"] = type(e).__name__
        page.screenshot(path=f"{OUT}/{tag}-err.png")
    b.close(); return r

with sync_playwright() as p:
    out = {}
    b = p.chromium.launch(); c = b.new_context()
    a = c.request.get(APP + "/api/me", max_redirects=0)
    out["anonymous_api_me"] = {"status": a.status, "location_host": (a.headers.get("location") or "")[:40].split("/")[2] if a.headers.get("location") else None}
    a2 = c.request.get(APP + "/api/me", headers={"Accept": "application/json"}, max_redirects=0)
    out["anonymous_api_me_json_accept"] = a2.status
    f = c.request.get(APP + "/api/me", headers={"X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com", "X-MS-CLIENT-PRINCIPAL-ID": "00000000-0000-0000-0000-000000000000"}, max_redirects=0)
    out["forged_header_api_me"] = {"status": f.status}
    h = c.request.get(APP + "/healthz"); out["healthz"] = h.status
    b.close()
    out["employee"] = run(p, "employee-test-account", emp, "employee")
    out["resident"] = run(p, "resident-test-account", res, "resident")
print(json.dumps(out, indent=1))
