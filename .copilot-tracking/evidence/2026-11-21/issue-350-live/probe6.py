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
    page.goto(APP + "/app", wait_until="networkidle", timeout=60000)
    for label in ["Assistant proposals"]:
        page.get_by_role("link", name=re.compile("^"+re.escape(label))).first.click(timeout=8000)
        for t in (2,5,10,20,40):
            page.wait_for_timeout(t*1000 if t==2 else (t-[2,5,10,20,40][[2,5,10,20,40].index(t)-1])*1000)
            txt=page.inner_text("body")
            out[f"t{t}"]={"working":"working..." in txt,"closed_heading":"Closed cases" in txt,"proposals":"roposal" in txt,"len":len(txt),"url":page.url.replace(APP,"")}
        page.screenshot(path=os.path.join(OUT,"assistant-proposals-40s.png"))
        out["text"]=mask(txt[:900])
    b.close()
open(os.path.join(OUT, "probe6.json"), "w").write(mask(json.dumps(out, indent=1)))
print(mask(json.dumps(out, indent=1))[:12000])
