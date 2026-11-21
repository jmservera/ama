"""Issue 157 live probe 2026-11-21. Reads credentials at runtime; prints only redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});let t=await r.text();return [r.status,t.slice(0,500)]}"
P = "async([p,b])=>{const r=await fetch(p,{method:'POST',headers:{'X-ZF-CSRF':'1','Content-Type':'application/json'},body:JSON.stringify(b),credentials:'same-origin'});return [r.status,(await r.text()).slice(0,500)]}"
R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
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
    R["me_role"] = page.evaluate(G, "/api/me")[0]
    for a in ["/api/chat/status", "/api/chat/threads", "/api/chat/threads/not-my-thread-0000", "/api/audit-check", "/api/chat/regulatory/usage"]:
        R[a] = page.evaluate(G, a)
    R["breakglass"] = page.evaluate(P, ["/api/chat/breakglass", {"target": "other.user@example.invalid", "purpose": "Investigating reported chat misuse, ticket 157"}])
    R["audit_after"] = page.evaluate(G, "/api/audit-check")
    R["memory_off"] = page.evaluate(G, "/api/chat/memory")
    R["chat_nav"] = page.evaluate("()=>[...document.querySelectorAll('a,button')].map(e=>(e.getAttribute('href')||'')+'|'+e.innerText.trim().slice(0,40)).filter(x=>/chat|assistant/i.test(x)).slice(0,8)")
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/app-signed-in.png")
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    txt = txt.replace(v, "[redacted]")
open(f"{OUT}/live_probe.json", "w").write(txt)
print(txt)
