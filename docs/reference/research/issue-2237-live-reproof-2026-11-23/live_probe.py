"""Live proof for issue 2237: GET /api/retention as the demo employee. Credentials are read at runtime and never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

EMP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
scrub = lambda x: json.loads(EMAIL.sub("[email]", json.dumps(x)))


def emp_login(page):
    page.goto(EMP + "/api/me", wait_until="domcontentloaded", timeout=120000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(EMP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(EMP)), timeout=60000)
    page.goto(EMP + "/", wait_until="networkidle")


def api(page, path):
    js = "async p=>{const x=await fetch(p,{headers:{'X-ZF-CSRF':'1'}});const t=await x.text();let j;try{j=JSON.parse(t)}catch(e){j={raw:t.slice(0,200)}};return [x.status,j]}"
    return page.evaluate(js, path)


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1366, "height": 900}).new_page()
    emp_login(page)
    res = {}
    s, me = api(page, "/api/me")
    res["me"] = {"status": s, "role": (me.get("user") or {}).get("role"), "keys": sorted(me)[:10]}
    s, j = api(page, "/api/retention")
    res["retention"] = {"status": s, "keys": sorted(j), "records": len(j.get("records") or []), "error": str(j.get("error") or j.get("raw") or "")[:150]}
    burst = page.evaluate("async()=>{const h={headers:{'X-ZF-CSRF':'1'}};const seq=[];for(let i=0;i<15;i++){seq.push((await fetch('/api/retention',h)).status)};const par=await Promise.all(Array.from({length:20},()=>fetch('/api/retention',h).then(r=>r.status)));const mixed=await Promise.all(Array.from({length:20},(_,i)=>fetch(i%2?'/api/retention':'/api/cases',h).then(r=>r.status)));return {seq,par,mixed}}")
    res["burst"] = burst
    json.dump(scrub(res), open(os.path.join(OUT, sys.argv[1] if len(sys.argv) > 1 else "result.json"), "w"), indent=2)
    print(json.dumps(scrub(res)))
    b.close()
