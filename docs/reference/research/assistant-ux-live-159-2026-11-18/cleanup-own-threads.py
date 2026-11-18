"""Delete only threads created within the last N minutes on the probe case (the probe's own thread)."""
import json, sys, datetime
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
MIN = int(sys.argv[1])
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(storage_state="<tmp>/state-staff.json"); pg = c.new_page(); pg.goto(H + "/app"); pg.wait_for_load_state("networkidle")
    ts = pg.evaluate("fetch('/api/chat/threads').then(r=>r.json())")
    print("keys", sorted(ts[0].keys()) if ts else None, "count", len(ts))
    now = datetime.datetime.now(datetime.timezone.utc)
    for t in ts:
        cr = next((t[k] for k in ("created_at", "created", "updated_at") if k in t), None)
        age = (now - datetime.datetime.fromisoformat(cr.replace("Z", "+00:00"))).total_seconds() / 60 if cr else None
        if age is not None and age < MIN and t.get("case_id") == "ZF-2025-0122":
            r = pg.evaluate("id => fetch('/api/chat/threads/'+id+'/delete',{method:'POST',headers:{'X-ZF-CSRF':'1','Content-Type':'application/json'},body:'{}'}).then(r=>r.status)", t["id"])
            print("deleted", t["id"], round(age, 1), r)
