"""Read-only error probes (GET) on the live staff API; prints status and message text only."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from audit import *
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
    login(pg, u, p, H + "/sign-in")
    out = []
    for path in ["/api/cases/NO-SUCH-CASE", "/api/cases/NO-SUCH-CASE/handoff", "/api/packages/NOPE", "/api/finance/NOPE", "/api/no-such-endpoint"]:
        r = c.request.get(H + path)
        out.append({"path": path, "status": r.status, "body": r.text()[:300]})
    json.dump(out, open(OUT + "/staff-errors.json", "w"), indent=1)
    for o in out: print(o["path"], o["status"], o["body"][:200].replace("\n", " "))
    b.close()
