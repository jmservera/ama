"""Shared live-demo helpers for issue 125. Credentials are read at runtime and never printed."""
import json, os, re
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


JS = """async([m,p,b])=>{const o={method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'}};
  if(m==='POST')o.body=JSON.stringify(b||{});const x=await fetch(p,o);const t=await x.text();
  let j;try{j=JSON.parse(t)}catch(e){j={_text:t.slice(0,3000)}};return [x.status,j]}"""


def call(page, method, path, body=None):
    return page.evaluate(JS, [method, path, body])


def session(p):
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg); pg.goto(APP + "/", wait_until="networkidle")
    return b, pg
