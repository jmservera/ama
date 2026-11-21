"""Live role proof (issue 2204). Reads credentials at runtime; prints only redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
MASK = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""


def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
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
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    out["entra_redirect"] = "login.microsoftonline.com" in page.url
    login(page)
    me = c.request.get(APP + "/api/me"); out["me_status"] = me.status
    d = me.json(); u = d["user"]
    out["me"] = {"role": u.get("role"), "app_roles": u.get("app_roles"), "app_admin": u.get("app_admin"),
                 "view_only": u.get("view_only"), "identity_source": u.get("identity_source"),
                 "navigation": [{"label": n["label"], "href": n["href"], "access": n.get("access")} for n in d.get("navigation", [])],
                 "services": d.get("services")}
    probes = {}
    for path in ["/api/cases", "/api/stats", "/api/finance", "/api/packages", "/api/funding",
                 "/api/admin/simulator-control", "/api/audit-check", "/api/retention", "/api/no-such-route"]:
        r = c.request.get(APP + path); probes[path] = r.status
    r = c.request.get(APP + "/api/admin/simulator-control")
    try:
        probes["simulator_body_keys"] = sorted(r.json().keys())
        probes["simulator_error"] = r.json().get("error")
    except Exception:
        pass
    out["probes"] = probes
    shots = {"01-workbench": "/app#/", "02-denied-simulator": "/app#/simulator", "03-denied-repairs-role-screen": "/app#/role/repairs",
             "04-permitted-pm-queue": "/app#/role/programme_manager"}
    out["views"] = {}
    for tag, route in shots.items():
        page.goto(APP + route, wait_until="networkidle"); page.reload(wait_until="networkidle"); page.wait_for_timeout(2500)
        page.evaluate(MASK)
        page.evaluate("()=>{const a=document.getElementById('account');if(a)a.style.visibility='hidden'}")
        out["views"][tag] = {"route": route, "h1": [h.inner_text()[:80] for h in page.query_selector_all("h1,h2")][:4],
                              "text_has_unavailable": "unavailable" in page.inner_text("body").lower()}
        if tag in ("02-denied-simulator", "03-denied-repairs-role-screen"):
            page.screenshot(path=f"{OUT}/live-{tag}.png")
    b.close()
print(json.dumps(out, indent=1))
