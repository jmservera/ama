"""Issue 350 live probe. Reads credentials at runtime; prints redacted summaries only."""
import json, os, re
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
user = open(os.path.join(home, ".ama-test-user-id")).read().split("\n")[0].strip()
pw = open(os.path.join(home, ".ama-test-user")).read().split("\n")[0].strip()
GUID = re.compile(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}", re.I)
mask = lambda s: GUID.sub("<GUID>", re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s))
EPS = ["/api/me","/api/cases","/api/stats","/api/visits","/api/workorders","/api/finance","/api/funding","/api/governance","/api/assistants","/api/assistants/proposals","/api/assistants/releases","/api/map","/api/law","/api/law/cards","/api/law/alerts","/api/ledger/digest","/api/audit-check","/api/time/status","/api/time/mine","/api/retention","/api/data-protection","/api/continuity","/api/packages","/api/closed-cases","/api/checklists","/api/exceptions","/api/account/photo","/api/briefing","/api/progress","/api/facets","/api/ranking/snapshot","/api/aftercare","/api/handoffs"]
def shape(d, depth=0):
    if isinstance(d, list): return {"list": len(d), "first_keys": sorted(d[0].keys())[:12] if d and isinstance(d[0], dict) else None}
    if isinstance(d, dict):
        return {k: (shape(v, depth+1) if depth < 1 and isinstance(v,(list,dict)) else (v if isinstance(v,(bool,int,float)) or (isinstance(v,str) and len(v)<60 and k in ("status","state","mode","enabled","provider","configured","reason","role","detail","message","code","error")) else type(v).__name__)) for k, v in list(d.items())[:25]}
    return type(d).__name__
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width":1366,"height":900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception: break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    for e in EPS:
        try:
            r = c.request.get(APP + e, max_redirects=0, timeout=60000)
            ct = r.headers.get("content-type", "")
            rec = {"status": r.status, "ct": ct.split(";")[0]}
            if "json" in ct:
                try: rec["shape"] = shape(r.json())
                except Exception: rec["shape"] = "unparsable"
            elif r.status != 200:
                rec["body"] = mask(r.text()[:160])
            else: rec["bytes"] = len(r.body())
            out[e] = rec
        except Exception as ex:
            out[e] = {"error": type(ex).__name__}
    for name, path in [("app","/app"),("map","/map.html"),("law","/law.html"),("time","/time.html")]:
        try:
            page.goto(APP + path, wait_until="networkidle", timeout=60000)
            page.screenshot(path=os.path.join(OUT, f"{name}.png"))
            out["page_"+name] = {"title": page.title(), "url_path": page.url.replace(APP, "")}
        except Exception as ex:
            out["page_"+name] = {"error": type(ex).__name__}
    b.close()
open(os.path.join(OUT, "probe2.json"), "w").write(mask(json.dumps(out, indent=1)))
print(mask(json.dumps(out, indent=1))[:9000])
