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
EPS=[]
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
    def J(path):
        r = c.request.get(APP + path, max_redirects=0, timeout=60000)
        try: return r.status, r.json()
        except Exception: return r.status, None
    st, me = J("/api/me")
    out["me.counts"] = me.get("counts"); out["me.staff"] = {"count": len(me.get("staff") or []), "roles": sorted({str(x.get("role")) for x in (me.get("staff") or []) if isinstance(x,dict)})}
    out["me.account"] = me.get("account"); out["me.services"] = me.get("services"); out["me.map"] = me.get("map")
    out["me.user"] = {k:(v if k in ("role","app_roles","view_only","identity_source") else "..") for k,v in me.get("user",{}).items()}
    out["me.nav"] = [n.get("label") or n.get("title") or n for n in (me.get("navigation") or [])][:30]
    st, a = J("/api/assistants")
    out["assistants"] = [{k:x.get(k) for k in ("id","binding","release","roles")} for x in a["assistants"]]
    out["assistants.disabled"] = a.get("disabled"); out["assistants.manual"]=a.get("manual")
    out["registered_tasks"] = [{k:t.get(k) for k in ("id","approval_state","activation","authority_gap")} for t in a["registered_tasks"]]
    out["gate"] = {k:a["real_ai_delivery_gate"].get(k) for k in ("passed","status","blocking_reasons")}
    out["rai_exercise"] = {k:a["rai_exercise_acceptance"].get(k) for k in ("passed","status","note")}
    st, pr = J("/api/assistants/proposals")
    out["proposals"] = [{k:x.get(k) for k in ("capability","display_state","attempts","actionable")} for x in pr["proposals"]]
    out["proposals.disabled"] = pr.get("disabled")
    st, br = J("/api/briefing"); out["briefing"] = {k:br.get(k) for k in ("source","model","mode","validated","reason","task","verified")}
    st, ac = J("/api/audit-check"); out["audit"] = {k:ac.get(k) for k in ("intact","entries","digests_checked")}
    st, ap = J("/api/account/photo"); out["photo"] = (st, ap)
    st, t = J("/api/time/status"); out["time"] = {k:t.get(k) for k in ("enabled","flag_on","dpia_recorded","consultation_recorded","notice_approved","reason")}
    st, g = J("/api/governance"); out["gov"] = {"capture_open":g.get("capture_open"),"releases":g.get("releases"),"release_gaps":g.get("release_gaps")}
    st, m = J("/api/map"); out["map"]={k:m.get(k) for k in ("mode","total","shown","cap")}
    st, ex = J("/api/exceptions"); out["exceptions_state"]=ex.get("state")
    st, d = J("/api/stats"); out["kpis"]=d.get("kpis")
    st, w = J("/api/workorders"); out["wo_status_counts"]={}
    for x in w:
        k=str(x.get("status")); out["wo_status_counts"][k]=out["wo_status_counts"].get(k,0)+1
    for p_ in ["/api/export","/api/continuity/export","/api/ledger/digest","/api/law","/api/docs/"]:
        r=c.request.get(APP+p_, max_redirects=0); out["probe "+p_]=[r.status, r.headers.get("content-type","")[:30], len(r.body())]
    for name, path in [("map","/map.html"),("time","/time.html"),("law","/law.html")]:
        try:
            page.goto(APP + path, wait_until="networkidle", timeout=60000)
            out["page_"+name] = {"title": page.title(), "path": page.url.replace(APP, ""), "text": mask(page.inner_text("body")[:300])}
        except Exception as ex: out["page_"+name]={"error":type(ex).__name__}
    b.close()
open(os.path.join(OUT, "probe3.json"), "w").write(mask(json.dumps(out, indent=1)))
print(mask(json.dumps(out, indent=1))[:12000])
