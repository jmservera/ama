"""Issue 349 live prerequisite proof. Reads credentials at runtime; prints/stores redacted facts only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
USER, PW = rd(".ama-test-user-id")[0].strip(), rd(".ama-test-user")[0].strip()
GUID = re.compile(r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", re.I)
MASK = "()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"


def st(c, path, **kw):
    r = c.request.get(APP + path, max_redirects=0, **kw)
    loc = r.headers.get("location") or ""
    return {"status": r.status, "redirect_host": loc.split("/")[2] if loc.startswith("http") else None}


def signin(page):
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900})
    out["anon"] = {
        "me_browser": st(c, "/api/me", headers={"Accept": "text/html", "User-Agent": "Mozilla/5.0"}),
        "me_nonbrowser_json": st(c, "/api/me", headers={"Accept": "application/json"}),
        "cases": st(c, "/api/cases"),
        "workspace_shell": st(c, "/workspace-shell.js"),
        "xhr": st(c, "/api/me", headers={"X-Requested-With": "XMLHttpRequest"}),
        "bad_bearer": st(c, "/api/me", headers={"Authorization": "Bearer not-a-token"}),
        "forged_principal": st(c, "/api/me", headers={"X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com", "X-MS-CLIENT-PRINCIPAL-ID": "00000000-0000-0000-0000-000000000000"}),
        "forged_principal_blob": st(c, "/api/me", headers={"X-MS-CLIENT-PRINCIPAL": "e30="}),
        "forged_role": st(c, "/api/me", headers={"X-ZF-Role": "Admin"}),
        "healthz": st(c, "/healthz"),
    }
    b.close()

    # wrong password at Entra: denial
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", "wrong-" + PW[::-1]); page.click("#idSIButton9")
    page.wait_for_timeout(4000)
    err = page.query_selector("#passwordError")
    out["entra_wrong_password"] = {"still_on_entra": "login.microsoftonline.com" in page.url, "error_shown": bool(err), "app_session": st(c, "/api/me")["status"]}
    page.evaluate(MASK); page.screenshot(path=f"{OUT}/entra-wrong-password-denied.png")
    b.close()

    # successful sign-in, role, denials, logout, account switch
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/sign-in", wait_until="domcontentloaded")
    out["signin_page_host"] = page.url.split("/")[2] if page.url.startswith("http") else None
    page.screenshot(path=f"{OUT}/employee-1-entra-prompt.png") if False else None
    signin(page)
    r = c.request.get(APP + "/api/me"); d = r.json() if r.status == 200 else {}
    u = d.get("user", {})
    out["session"] = {"me_status": r.status, "role": u.get("role"), "app_roles": u.get("app_roles"), "view_only": u.get("view_only"),
                      "identity_source": u.get("identity_source"), "auth_provider": u.get("auth_provider"), "bound": bool(u.get("bound")),
                      "tid_guid": bool(GUID.match(str(u.get("tid", "")))), "oid_guid": bool(GUID.match(str(u.get("oid", "")))),
                      "navigation_count": len(d.get("navigation", []) or [])}
    out["positive_requests"] = {pth: c.request.get(APP + pth).status for pth in ["/api/cases", "/api/me", "/healthz"]}
    out["forged_with_session"] = {}
    f = c.request.get(APP + "/api/me", headers={"X-ZF-Role": "Admin", "X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com"})
    fu = f.json().get("user", {}) if f.status == 200 else {}
    out["forged_with_session"] = {"status": f.status, "role_unchanged": fu.get("role") == u.get("role"), "identity_unchanged": fu.get("oid") == u.get("oid")}
    out["role_scoped_denial_probe"] = {pth: c.request.get(APP + pth).status for pth in ["/api/admin/simulator-control", "/api/audit-check"]}
    page.goto(APP + "/", wait_until="networkidle")
    page.evaluate(MASK); page.screenshot(path=f"{OUT}/employee-welcome-signed-out.png")
    out["workbench_path"] = re.sub(r"^https?://[^/]+", "", page.url)[:40]
    page.goto(APP + "/.auth/logout", wait_until="domcontentloaded"); page.wait_for_timeout(3000)
    out["after_logout"] = {"me": st(c, "/api/me")}
    page.goto(APP + "/sign-in", wait_until="domcontentloaded"); page.wait_for_timeout(3000)
    out["account_switch"] = {"picker_or_login_shown": "login.microsoftonline.com" in page.url, "other_account_option": bool(page.query_selector("#otherTile, #otherTileText"))}
    page.evaluate(MASK); page.screenshot(path=f"{OUT}/employee-account-picker-after-logout.png")
    b.close()
print(json.dumps(out, indent=1))
