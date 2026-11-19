"""Issue 349 live5 re-proof. Reads credentials at runtime; prints redacted facts only."""
import json, os, re
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
user = open(os.path.join(home, ".ama-test-user-id")).read().split("\n")[0].strip()
pw = open(os.path.join(home, ".ama-test-user")).read().split("\n")[0].strip()
GUID = re.compile(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}", re.I)
mask = lambda s: GUID.sub("<GUID>", s)
out = {}

def scrub(page):
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
    while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}
    document.querySelectorAll('input').forEach(i=>{if(i.type!=='password')i.value=i.value?'[hidden]':''})}""")

def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    # anonymous / forged (no session)
    r = c.request.get(APP + "/api/me", max_redirects=0)
    loc = r.headers.get("location", "")
    q = parse_qs(urlparse(loc).query)
    out["anonymous_browser_api_me"] = {"status": r.status, "host": urlparse(loc).netloc,
        "authorize_redirect_uri": q.get("redirect_uri", [""])[0].replace(urlparse(APP).netloc, "<app-host>"),
        "response_type": q.get("response_type"), "client_id_is_guid": bool(GUID.fullmatch(q.get("client_id", [""])[0]))}
    out["anonymous_xhr"] = c.request.get(APP + "/api/me", headers={"X-Requested-With": "XMLHttpRequest"}, max_redirects=0).status
    out["forged_principal_headers_no_session"] = c.request.get(APP + "/api/me", headers={
        "X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com", "X-MS-CLIENT-PRINCIPAL-ID": "00000000-0000-0000-0000-000000000000",
        "X-ZF-Role": "Admin"}, max_redirects=0).status
    out["bad_bearer"] = c.request.get(APP + "/api/me", headers={"Authorization": "Bearer invalid"}, max_redirects=0).status
    # browser sign-in
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    out["browser_redirected_to_entra"] = "login.microsoftonline.com" in page.url
    login(page)
    out["callback_returned_to_app"] = page.url.startswith(APP)
    m = c.request.get(APP + "/api/me"); out["me_status"] = m.status
    d = m.json(); u = d.get("user", {})
    out["me"] = {"role": u.get("role"), "app_roles": u.get("app_roles"), "view_only": u.get("view_only"),
        "identity_source": u.get("identity_source"), "auth_provider": u.get("auth_provider"),
        "bound": u.get("bound"), "tid_guid": bool(GUID.fullmatch(str(u.get("tid", "")))),
        "navigation_count": len(d.get("navigation") or [])}
    out["authenticated_cases"] = c.request.get(APP + "/api/cases").status
    out["forged_headers_with_session"] = c.request.get(APP + "/api/me", headers={"X-ZF-Role": "Admin", "X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com"}).json().get("user", {}).get("role")
    page.goto(APP + "/app", wait_until="networkidle"); out["app_title"] = page.title()
    # logout then account switching prompt
    page.goto(APP + "/.auth/logout", wait_until="domcontentloaded")
    out["after_logout_api_me"] = c.request.get(APP + "/api/me", max_redirects=0).status
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    out["relogin_shows_entra"] = "login.microsoftonline.com" in page.url
    try:
        page.wait_for_selector("#tilesHolder, input[name=loginfmt]", timeout=15000)
        out["account_picker_or_login_shown"] = "picker" if page.query_selector("#tilesHolder") else "login-form"
    except Exception as e:
        out["account_picker_or_login_shown"] = type(e).__name__
    b.close(); b2 = p.chromium.launch()

    # wrong-role probe: resident test account against the staff API
    rl=[l.strip() for l in open(os.path.join(home,".ama-resident-test-user")).read().split("\n") if l.strip()]
    user, pw = rl[0], rl[1]
    c2 = b2.new_context(viewport={"width":1366,"height":900}); pg = c2.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    try:
        login(pg)
        m = c2.request.get(APP + "/api/me", max_redirects=0)
        out["resident_me_status"] = m.status
        try:
            u = m.json(); out["resident_me"] = {k: (u.get("user") or u).get(k) for k in ("role","app_roles","view_only","identity_source","bound")} if m.status==200 else str(u)[:200]
        except Exception: out["resident_me"]="non-json"
        out["resident_cases_status"] = c2.request.get(APP + "/api/cases", max_redirects=0).status
        r2 = pg.goto(APP + "/app", wait_until="networkidle"); out["resident_app_status"] = r2.status if r2 else None
    except Exception as e:
        out["resident_error"] = type(e).__name__ + ": " + mask(str(e))[:200]
        out["resident_final_host"] = urlparse(pg.url).netloc
        out["resident_page_title"] = pg.title()
    b2.close()
print(mask(json.dumps(out, indent=1)))
