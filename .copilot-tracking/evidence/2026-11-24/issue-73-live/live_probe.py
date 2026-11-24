"""Issue 73/149/157 checkpoint probe 2026-11-24. GET only. Reads sign-in values at runtime; prints redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});let t=await r.text();let n=null;try{const j=JSON.parse(t);n=Array.isArray(j)?j.length:(typeof j==='object'&&j?Object.keys(j).slice(0,8):null)}catch(e){}return [r.status,n]}"
R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    try:
        R["anon_api_cases"] = page.evaluate(G, "/api/cases")[0]
    except Exception as e:
        R["anon_api_cases"] = "blocked: " + type(e).__name__
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
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
    page.wait_for_load_state("networkidle")
    page.goto(APP + "/app"); page.wait_for_load_state("networkidle")
    for a in ["/api/me", "/api/cases", "/api/exceptions", "/api/ranking/policy", "/api/ranking/snapshot", "/api/ranking/publication", "/api/retention", "/api/chat/threads", "/api/data-protection", "/api/assistants/rai-metrics", "/api/stats"]:
        R[a] = page.evaluate(G, a)
    cases = json.loads(page.evaluate("async()=>await (await fetch('/api/cases',{credentials:'same-origin'})).text()"))
    items = cases if isinstance(cases, list) else cases.get("items", [])
    cid = None
    for it in items:
        if isinstance(it, dict):
            cid = it.get("id") or it.get("case_id")
            if cid:
                break
    R["case_id_found"] = bool(cid)
    if cid:
        R["/api/cases/{id}"] = page.evaluate(G, f"/api/cases/{cid}")
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/app-signed-in.png")
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    txt = txt.replace(v, "[redacted]")
open(f"{OUT}/live_probe.json", "w").write(txt)
print(txt[:4000])
