import json
from playwright.sync_api import sync_playwright
H="https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
JS="""async ([p,b])=>{const r=await fetch(p,{method:'POST',headers:{'X-ZF-CSRF':'1','Content-Type':'application/json'},body:JSON.stringify(b),credentials:'same-origin'});return [r.status,(await r.text()).slice(0,200)]}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); c=b.new_context(storage_state="/tmp/state-staff.json",viewport={"width":1440,"height":900}); pg=c.new_page(); pg.goto(H+"/app"); pg.wait_for_load_state("networkidle")
    chk=lambda l:print(l,pg.evaluate("async()=>{const r=await fetch('/api/audit-check');const j=await r.json();return [j.intact,j.entries,j.head.slice(0,12)]}"))
    chk("before")
    print("refused-1",pg.evaluate(JS,["/api/chat/breakglass",dict(target="other.user@example.invalid",purpose="Investigating reported chat misuse, ticket 162")]))
    chk("after-1")
    print("refused-2",pg.evaluate(JS,["/api/chat/breakglass",dict(target="other.user@example.invalid",purpose="x")]))
    chk("after-2")
    pg.screenshot(path="shots/app-after-breakglass-probe.png")
# The delete-all "New chat" loop used during the live run was removed here because it deleted unrelated synthetic threads.
