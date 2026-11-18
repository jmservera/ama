"""Live demo review-retention probe (issue 108). Credentials read at runtime, never printed."""
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


def call(c, method, path, body=None):
    js = """async([m,p,b])=>{const o={method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'}};
      if(m==='POST')o.body=JSON.stringify(b||{});const x=await fetch(p,o);const t=await x.text();
      let j;try{j=JSON.parse(t)}catch(e){j={_text_len:t.length}};return [x.status,j]}"""
    s, j = PAGE.evaluate(js, [method, path, body])
    return s, j


res = {}
PATHS = ["/healthz", "/api/me", "/api/ai/report", "/api/ai/heldout-evaluation", "/api/ai/cohort-evaluation", "/api/ai/candidate-comparison", "/api/ai/priority"]
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg); pg.goto(APP + "/", wait_until="networkidle"); PAGE = pg
    for path in PATHS:
        s, j = call(c, "GET", path)
        res[path] = {"status": s, "body": scrub(j)}
    pg.screenshot(path=os.path.join(OUT, "live-landing-signed-in.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, "live_ai_endpoints.json"), "w"), indent=1)
for k, v in res.items():
    print(k, v["status"], (sorted(v["body"].keys())[:12] if isinstance(v["body"], dict) else type(v["body"]).__name__))
