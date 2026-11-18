import os, hashlib
from playwright.sync_api import sync_playwright
H = os.environ["DEMO_API_URL"]
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state=os.environ["I76_SCRATCH"] + "/state-staff.json")
    for p in ("/app.js", "/web/app.js", "/static/app.js"):
        r = c.request.get(H + p, timeout=90000)
        t = r.text() if r.status == 200 else ""
        print(p, r.status, len(t), "safeguarding-clock" in t, "Safeguarding clock in this recorded view" in t,
              hashlib.sha256(t.encode()).hexdigest()[:16])
