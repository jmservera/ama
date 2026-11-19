"""Live demo assistant release/denial probe (issue 107). Credentials read at runtime, never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.abspath(__file__))
INVOKE = len(sys.argv) > 1 and sys.argv[1] == "invoke"
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")


def scrub(x):
    return json.loads(EMAIL.sub("[email]", json.dumps(x)))


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


def call(method, path, body=None):
    js = """async([m,p,b])=>{const o={method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'}};
      if(m==='POST')o.body=JSON.stringify(b||{});const x=await fetch(p,o);const t=await x.text();
      let j;try{j=JSON.parse(t)}catch(e){j={_text_len:t.length}};return [x.status,j]}"""
    return PAGE.evaluate(js, [method, path, body])


def shape(j, depth=0):
    if isinstance(j, dict):
        return {k: (shape(v, depth + 1) if depth < 2 else type(v).__name__) for k, v in list(j.items())[:40]}
    if isinstance(j, list):
        return [len(j), shape(j[0], depth + 1) if j else None]
    return j if isinstance(j, (int, bool, type(None))) or len(str(j)) < 80 else "str"


res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg); pg.goto(APP + "/", wait_until="networkidle"); PAGE = pg
    s, me = call("GET", "/api/me"); res["me"] = {"status": s, "role": me.get("user", {}).get("role")}
    for name, path in (("assistants", "/api/assistants"), ("forecast", "/api/assistants/forecast"),
                       ("rai_metrics", "/api/assistants/rai-metrics"), ("proposals", "/api/assistants/proposals")):
        s, j = call("GET", path)
        res[name] = {"status": s, "full": scrub(j)}
    if INVOKE:
        s, cases = call("GET", "/api/cases")
        lst = cases if isinstance(cases, list) else cases.get("items", [])
        cid = lst[0].get("id") if lst else None
        res["case_ids"] = [x.get("id") for x in lst][:12]
        res["case_id"] = cid
        caps = [t.get("id") or t.get("task") for t in (res["assistants"]["full"].get("assistants") or res["assistants"]["full"].get("tasks") or [])] if isinstance(res["assistants"]["full"], dict) else []
        res["invoke"] = {}
        for cap in caps:
            for cid in res["case_ids"]:
                s, j = call("POST", f"/api/assistants/{cap}/invoke", {"case_id": cid})
                res["invoke"][cap + ":" + str(cid)] = scrub({"status": s, "body": j})
                if s != 403:
                    break
        s, j = call("GET", "/api/assistants/proposals"); res["proposals_after"] = {"status": s, "full": scrub(j)}
    pg.screenshot(path=os.path.join(OUT, "live-workbench.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, "live_probe_invoke.json" if INVOKE else "live_probe_read.json"), "w"), indent=1)
print({k: (v.get("status") if isinstance(v, dict) else None) for k, v in res.items()})
