"""Issue 360 re-run: anonymous denial, staff sign-in, and a second identity (resident account) on the direct API ingress.
Credentials are read at runtime, never printed; every output string is scrubbed of them."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
lines = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
staff = {"user": lines(".ama-test-user-id")[0], "pw": lines(".ama-test-user")[0]}
rl = lines(".ama-resident-test-user")
resident = {"user": rl[0], "pw": rl[1]}
SECRETS = [staff["user"], staff["pw"], resident["user"], resident["pw"]]


def scrub(o):
    s = json.dumps(o, indent=1)
    for v in SECRETS:
        s = s.replace(v, "[redacted]")
    return re.sub(r"[\w.+-]+@[\w.-]+\.\w+", "[email]", s)


def login(page, who, base):
    page.fill("input[name=loginfmt]", who["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", who["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(base):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(base)), timeout=60000)


def probe(ctx, base, paths):
    res = {}
    for p in paths:
        try:
            r = ctx.request.get(base + p, max_redirects=0)
            res[p] = r.status
        except Exception as e:
            res[p] = "err " + type(e).__name__
    return res


out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    anon = b.new_context(viewport={"width": 1366, "height": 900})
    out["anon_api"] = probe(anon, APP, ["/healthz", "/", "/welcome.html", "/api/me", "/api/cases", "/app"])
    br = b.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36",
                       extra_http_headers={"Accept": "application/json"})
    out["anon_browser_mode_json"] = probe(br, APP, ["/api/me", "/api/cases"])
    for label, who, base in (("staff", staff, APP), ("resident", resident, APP)):
        c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
        o = {}
        try:
            page.goto(base + "/app", wait_until="domcontentloaded")
            o["redirect_host"] = re.sub(r"^https?://([^/]+).*", r"\1", page.url)
            login(page, who, base)
            o["returned_to_app"] = page.url.startswith(base)
            page.goto(base + "/app", wait_until="networkidle")
            o["app_title"] = page.title()
            page.evaluate("()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}")
            page.screenshot(path=f"{OUT}/{label}-signed-in.png")
            me = c.request.get(base + "/api/me", max_redirects=0); o["me_status"] = me.status
            if me.status == 200:
                u = me.json().get("user", {})
                o["me"] = {k: u.get(k) for k in ("role", "app_roles", "view_only", "identity_source")}
            o["probes"] = probe(c, base, ["/api/cases?view=all", "/api/stats", "/api/sensors", "/api/chat/status", "/healthz"])
            cs = c.request.get(base + "/api/cases?view=all", max_redirects=0)
            if cs.status == 200:
                o["cases_total"] = cs.json().get("total")
            o["forged_role_header"] = [c.request.get(base + "/api/me", headers={"X-ZF-Role": r}, max_redirects=0).status for r in ("Admin",)]
            o["post_with_session_no_csrf"] = c.request.post(base + "/api/chat/threads", data={}, max_redirects=0).status
        except Exception as e:
            o["error"] = type(e).__name__ + ": " + str(e)[:140]
            page.screenshot(path=f"{OUT}/{label}-err.png")
        out[label] = o
        c.close()
    b.close()
print(scrub(out))
