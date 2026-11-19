"""Live demo probe for issue 96. Reads credentials at runtime; GET only; retains redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}

def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

def redact(t):
    t = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t)
    return re.sub(r"\b(?:CASE|ZF|C)-[A-Za-z0-9-]+\b", "[id]", t)

out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = c.request.get(APP + "/api/me").json()
    out["role"] = me["user"]["role"]; out["services"] = me.get("services")
    r = c.request.get(APP + "/api/cases"); cases = r.json()
    lst = cases if isinstance(cases, list) else next((v for v in cases.values() if isinstance(v, list)), [])
    out["case_count"] = len(lst)
    cid = lst[0]["id"] if lst else None
    paths = ["/api/form-schemas", "/api/form-schemas.csv"]
    if cid:
        paths += [f"/api/cases/{cid}/form-candidates", f"/api/cases/{cid}/form-review"]
    for path in paths:
        r = c.request.get(APP + path)
        ent = {"status": r.status, "ctype": (r.headers.get("content-type") or "")[:40], "len": len(r.text())}
        t = r.text()
        ent["body_redacted"] = redact(t)[:1500]
        if "json" in ent["ctype"] and r.status == 200:
            j = r.json()
            ent["top_keys"] = sorted(j) if isinstance(j, dict) else type(j).__name__
            sch = j.get("schemas") if isinstance(j, dict) else None
            if sch is not None:
                ent["schema_count"] = len(sch)
                ent["approvals"] = sorted({s.get("approval") for s in sch})
        out[redact(path)] = ent
    page.goto(APP + "/api/form-schemas", wait_until="domcontentloaded")
    page.screenshot(path=f"{OUT}/form-schemas-response.png")
    page.goto(APP + "/", wait_until="networkidle")
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/workbench.png")
    b.close()
json.dump(out, open(f"{OUT}/probe1.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
