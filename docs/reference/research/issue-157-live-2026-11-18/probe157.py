"""Live read-mostly probe for issue 157 (synthetic demo). Needs $STATE_DIR/state-staff.json. Prints no credentials."""
import json, os
from playwright.sync_api import sync_playwright
H = os.environ["DEMO_API_URL"]
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});let t=await r.text();return [r.status,t.slice(0,600)]}"
P = "async([p,b])=>{const r=await fetch(p,{method:'POST',headers:{'X-ZF-CSRF':'1','Content-Type':'application/json'},body:JSON.stringify(b),credentials:'same-origin'});return [r.status,(await r.text()).slice(0,600)]}"
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(storage_state=os.environ["STATE_DIR"] + "/state-staff.json", viewport={"width": 1440, "height": 900}); pg = c.new_page()
    pg.goto(H + "/app"); pg.wait_for_load_state("networkidle")
    for p in ["/api/chat/status", "/api/chat/threads", "/api/chat/threads/not-my-thread-0000", "/api/audit-check", "/api/time/status", "/api/chat/regulatory/usage"]:
        out[p] = pg.evaluate(G, p)
    out["breakglass_refused"] = pg.evaluate(P, ["/api/chat/breakglass", {"target": "other.user@example.invalid", "purpose": "Investigating reported chat misuse, ticket 157"}])
    out["audit_after"] = pg.evaluate(G, "/api/audit-check")
    pg.screenshot(path="probe157-app.png")
print(json.dumps(out, indent=1))
