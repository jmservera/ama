"""Live demo probe for #223. Reads sign-in values at runtime; never prints them. Synthetic demo data only."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plain-language-live-153-2026-11-18", "scripts"))
from audit import login, H
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..")
home = os.path.expanduser("~")
log = []
HDR = {"X-ZF-CSRF": "1"}

class R:
    def __init__(self, d): self.status = d["status"]; self._t = d["text"]; self.headers = {}
    def json(self): import json as j; return j.loads(self._t)
    def text(self): return self._t

def post(pg, path, data):
    d = pg.evaluate("""async ([p, b]) => { const r = await fetch(p, {method: "POST", headers: {"Content-Type": "application/json", "X-ZF-CSRF": "1"}, body: JSON.stringify(b)}); return {status: r.status, text: await r.text()}; }""", [path, data])
    return R(d)

def rec(step, r):
    try:
        body = r.json()
    except Exception:
        body = r.text()[:300]
    log.append({"step": step, "status": r.status, "body": body})
    print(step, r.status, json.dumps(body)[:260])
    return body

with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
    login(pg, u, p, H + "/sign-in")
    pg.screenshot(path=OUT + "/screens/01-staff-briefing.png")
    me = rec("whoami", c.request.get(H + "/api/me"))
    cases = rec("cases", c.request.get(H + "/api/cases"))
    items = cases.get("cases") or cases.get("items") or cases if isinstance(cases, (dict, list)) else []
    cid = (items[0].get("id") if isinstance(items, list) and items else None)
    print("case", cid)
    if cid:
        run = rec("ai-summary", post(pg, f"/api/cases/{cid}/ai", {"task": "summary"}))
        rid = run.get("id") or run.get("record_id") if isinstance(run, dict) else None
        print("record", rid)
        if rid:
            rec("review-accept-no-reason", post(pg, f"/api/ai/review/{rid}/reject", {"reason": ""}))
            rec("review-reject-with-reason", post(pg, f"/api/ai/review/{rid}/reject", {"reason": "Demo probe: contradicts source [source: Stage: x]"}))
        rec("ai-report", c.request.get(H + "/api/ai/report"))
    json.dump(log, open(OUT + "/live-probe.json", "w"), indent=1)
    b.close()
