"""Live demo probe for issue 116. Reads credentials at runtime; retains only redacted facts. GET plus one refusing POST (no provider call)."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
CANARY = re.compile(r"vulnerab|disabilit|health|medical|adjustment|reason", re.I)

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

def keys(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield pre + k
            yield from keys(v, pre + k + ".")
    elif isinstance(o, list):
        for v in o[:5]:
            yield from keys(v, pre + "[].")

def redact(t):
    return re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t)

out = {}
H = {"Content-Type": "application/json", "X-ZF-CSRF": "1"}
def post(c, path, body):
    r = c.request.post(APP + path, data=json.dumps(body), headers=H)
    t = r.text()
    try:
        j = r.json()
        shape = {k: (v if isinstance(v, (bool, int, type(None))) or (isinstance(v, str) and len(v) < 160) else type(v).__name__) for k, v in j.items()}
    except Exception:
        shape = {"raw": redact(t)[:160]}
    return {"status": r.status, "body": shape}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    items = c.request.get(APP + "/api/cases").json()["items"]
    cid = items[0]["id"]
    JS = """async([path,body])=>{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:JSON.stringify(body)});return {status:r.status,body:(await r.text()).slice(0,200)}}"""
    out["ai_unknown_task"] = page.evaluate(JS, [f"/api/cases/{cid}/ai", {"task": "not-a-task"}])
    out["ai_missing_task"] = page.evaluate(JS, [f"/api/cases/{cid}/ai", {}])
    out["ai_unknown_case"] = page.evaluate(JS, ["/api/cases/NOPE/ai", {"task": "summary"}])
    out["readdoc_unknown_doc"] = page.evaluate(JS, [f"/api/cases/{cid}/read-doc", {"id": "no-such-doc", "ai_derivative": "bogus"}])
    out["readdoc_unknown_doc_plain"] = page.evaluate(JS, [f"/api/cases/{cid}/read-doc", {"id": "no-such-doc"}])
    docs = []
    for it in items:
        d = c.request.get(APP + "/api/cases/" + it["id"]).json()
        for x in d.get("documents", []):
            if not x.get("generated"): docs.append((it["id"], x["id"], x.get("kind")))
    out["nongenerated_documents"] = len(docs)
    b.close()
json.dump(out, open(f"{OUT}/probe5.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:5000])
