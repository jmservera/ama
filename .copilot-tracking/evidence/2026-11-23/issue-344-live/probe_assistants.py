"""Issue 344 targeted re-check of the Assistant proposals view with a longer wait. Credentials read at runtime only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    bad = []; reqs = []
    page.on('requestfinished', lambda r: reqs.append(re.sub(r'^https?://[^/]+','',r.url)[:80]) if '/api/assistants' in r.url or '/assistants.js' in r.url else None)
    page.on('requestfailed', lambda r: reqs.append('FAILED '+re.sub(r'^https?://[^/]+','',r.url)[:80]+' '+str(r.failure)[:40]))
    page.on("response", lambda r: bad.append(f"{r.status} {re.sub(r'^https?://[^/]+', '', r.url)[:70]}") if r.status >= 400 else None)
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd], input[name=pass]", timeout=30000)
    page.fill("input[name=passwd], input[name=pass]", emp["pw"]); page.click("#idSIButton9")
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
    page.wait_for_timeout(3000)
    page.click("#nav a[href='#/assistants']")
    page.wait_for_timeout(1000)
    import time
    t=time.time()
    try:
        page.wait_for_function("()=>/Role-owned assistant proposals|Assistant proposals/.test(document.querySelector('#app')?.innerText||'')", timeout=90000)
        R["rendered_after_s"] = round(time.time()-t,1)
    except Exception as e:
        R["rendered_after_s"] = "not within 90s"
    page.wait_for_timeout(1500)
    R["headings"] = page.eval_on_selector_all("#app h1, #app h2", "e=>e.map(x=>x.textContent.trim().slice(0,60))")
    R["text_len"] = page.evaluate("()=>document.querySelector('#app').innerText.length")
    R["http_errors"] = sorted(set(bad)); R["requests"]=reqs
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/walk-10-assistants-recheck.png")
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/assistants_recheck.json", "w").write(txt)
print(txt)
