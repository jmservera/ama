from playwright.sync_api import sync_playwright
H = "<demo API URL>"
POST = """async ([p,b])=>{const r=await fetch(p,{method:'POST',headers:{'X-ZF-CSRF':'1','Content-Type':'application/json'},body:JSON.stringify(b),credentials:'same-origin'});return [r.status,(await r.text()).slice(0,200)]}"""
CHK = "async()=>{const r=await fetch('/api/audit-check');const j=await r.json();return [j.intact,j.entries,j.head.slice(0,12)]}"
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(storage_state="state-staff.json", viewport={"width": 1440, "height": 900}); pg = c.new_page()
    pg.goto(H + "/app"); pg.wait_for_load_state("networkidle")
    print("me", pg.evaluate("async()=>{const j=await (await fetch('/api/me')).json();return [j.account&&j.account.role||j.role]}"))
    print("before", pg.evaluate(CHK))
    body = dict(target="other.user@example.invalid", purpose="Investigating reported chat misuse, ticket 162")
    print("refused-full-purpose", pg.evaluate(POST, ["/api/chat/breakglass", body]))
    print("after-1", pg.evaluate(CHK))
    print("refused-short-purpose", pg.evaluate(POST, ["/api/chat/breakglass", dict(body, purpose="x")]))
    print("after-2", pg.evaluate(CHK))
    print("grant-route-get", pg.evaluate("async()=>{const r=await fetch('/api/chat/breakglass');return r.status}"))
