"""Read-only live demo quality sensor probe, run 3 (issue 1288); never invokes the assistant. Credentials read at runtime, never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
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
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 2600}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg); pg.goto(APP + "/", wait_until="networkidle"); PAGE = pg
    s, me = call("GET", "/api/me"); res["me"] = {"status": s, "role": me.get("user", {}).get("role")}
    s, cases = call("GET", "/api/cases")
    lst = cases if isinstance(cases, list) else cases.get("items", [])
    ids = [x.get("id") for x in lst][:12]
    res["case_ids"] = ids
    res["sensors"] = {}
    for cid in ids:
        s, j = call("GET", f"/api/cases/{cid}/sensors")
        res["sensors"][cid] = {"status": s, "body": scrub(j)}
    for name, path in (("assistants", "/api/assistants"), ("forecast", "/api/assistants/forecast"), ("rai_metrics", "/api/assistants/rai-metrics"), ("sim_quality", "/api/assistants/simulation/quality")):
        s, j = call("GET", path); res[name] = {"status": s, "body": scrub(j)}
    ok = [k for k, v in res["sensors"].items() if v["status"] == 200]
    res["ok_cases"] = ok
    s, j = call("GET", "/api/assistants/rai-metrics"); res["rai_metrics_after"] = {"status": s, "body": scrub(j)}
    json.dump(res, open(os.path.join(OUT, "live_probe.json"), "w"), indent=1)
    if ok:
        cid = "ZF-2025-0031" if "ZF-2025-0031" in ok else ok[0]
        pg.goto(APP + f"/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(2500)
        pg.click("[role=tab]:has-text('Home sensors')", timeout=8000)
        pg.wait_for_selector("#sensors table", timeout=20000)
        el = pg.query_selector("#sensors"); el.scroll_into_view_if_needed()
        el.screenshot(path=os.path.join(OUT, "live-sensor-panel.png"))
        res["ui_sensors_text"] = scrub(el.inner_text()[:3000])
        try:
            pg.click("[role=tab]:has-text('AI assistance')", timeout=5000); pg.wait_for_timeout(2500)
            panel = pg.query_selector("[role=tabpanel]:visible")
            res["ai_tab_text"] = scrub(panel.inner_text()[:3000])
            panel.screenshot(path=os.path.join(OUT, "live-ai-tab.png"))
        except Exception as e:
            res["ai_tab_error"] = str(e)[:200]
    b.close()
json.dump(res, open(os.path.join(OUT, "live_probe.json"), "w"), indent=1)
print({k: (v.get("status") if isinstance(v, dict) else None) for k, v in res.items()})
