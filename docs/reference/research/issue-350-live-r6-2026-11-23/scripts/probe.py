"""Issue 350 pass 6 live probe. Reads credentials at runtime; prints redacted summaries only. GET only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(OUT, "..", "raw")
home = os.path.expanduser("~")
user = open(os.path.join(home, ".ama-test-user-id")).read().split("\n")[0].strip()
pw = open(os.path.join(home, ".ama-test-user")).read().split("\n")[0].strip()
GUID = re.compile(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}", re.I)
mask = lambda s: GUID.sub("<GUID>", re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s))
KEEP = ("status", "state", "mode", "enabled", "provider", "configured", "reason", "role", "detail",
        "message", "code", "error", "ok", "intact", "entries", "total", "count", "services", "gate")


def shape(d, depth=0):
    if isinstance(d, list):
        return {"list": len(d), "first_keys": sorted(d[0].keys())[:10] if d and isinstance(d[0], dict) else None}
    if isinstance(d, dict):
        r = {}
        for k, v in list(d.items())[:30]:
            if isinstance(v, (bool, int, float)) or v is None:
                r[k] = v
            elif isinstance(v, str):
                r[k] = v[:90] if (k in KEEP or len(v) < 40) else "str"
            elif depth < 1:
                r[k] = shape(v, depth + 1)
            else:
                r[k] = type(v).__name__
        return r
    return type(d).__name__


EPS = ["/api/me", "/api/stats", "/api/cases", "/api/map", "/api/visits", "/api/workorders", "/api/finance",
       "/api/funding", "/api/packages", "/api/closed-cases", "/api/assistants", "/api/proposals", "/api/briefing",
       "/api/audit-check", "/api/ledger/digest", "/api/time/status", "/api/time/mine", "/api/law",
       "/api/law/cards", "/api/law/alerts", "/api/law/sources", "/api/account/photo", "/api/export",
       "/api/staff", "/api/sensors", "/api/documents", "/api/handoffs", "/api/health/deployment"]
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", user)
    page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw)
    page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    for ep in EPS:
        try:
            r = c.request.get(APP + ep, timeout=60000)
            try:
                body = shape(r.json())
            except Exception:
                body = (r.text() or "")[:120]
            out[ep] = {"status": r.status, "body": body}
        except Exception as ex:
            out[ep] = {"err": type(ex).__name__}
    page.goto(APP + "/law.html", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    out["law_page_text"] = mask(page.inner_text("body")[:500])
    page.screenshot(path=os.path.join(RAW, "law-page.png"))
    page.goto(APP + "/app", wait_until="networkidle", timeout=60000)
    for label in ["Time capture"]:
        try:
            page.get_by_role("link", name=re.compile("^" + label)).first.click(timeout=8000)
            page.wait_for_timeout(5000)
            out["time_view_text"] = mask(page.inner_text("main")[:700])
            page.screenshot(path=os.path.join(RAW, "time-capture.png"))
        except Exception as ex:
            out["time_view_text"] = "ERR " + type(ex).__name__
    b.close()
open(os.path.join(RAW, "03-staff-probe.json"), "w").write(mask(json.dumps(out, indent=1)))
print(mask(json.dumps(out, indent=1))[:14000])
