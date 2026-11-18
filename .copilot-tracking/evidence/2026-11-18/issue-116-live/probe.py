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
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = c.request.get(APP + "/api/me").json()
    out["role"] = me["user"]["role"]; out["services"] = me.get("services")
    def get(path):
        r = c.request.get(APP + path); return r, (r.json() if "json" in (r.headers.get("content-type") or "") else None)
    r, cases = get("/api/cases"); out["cases_status"] = r.status
    out["cases_top"] = sorted(cases) if isinstance(cases, dict) else type(cases).__name__
    lst = cases if isinstance(cases, list) else next((v for v in (cases or {}).values() if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]), [])
    out["case_count"] = len(lst)
    out["case_summary_keys"] = sorted(set(k for x in lst[:20] for k in keys(x)))
    cid = lst[0]["id"] if lst else None
    if cid:
        r, d = get("/api/cases/" + cid); out["case_detail_status"] = r.status
        ks = sorted(set(keys(d)))
        out["case_detail_keys"] = ks
        out["case_detail_reason_like_keys"] = [k for k in ks if CANARY.search(k)]
        txt = json.dumps(d)
        out["case_detail_reason_text_hits"] = sorted(set(m.group(0).lower() for m in CANARY.finditer(txt)))
        out["case_detail_vulnerability_fact_present"] = bool(re.search(r"Waiting on:|Adjustment|Vulnerab", txt))
        r2 = c.request.post(APP + f"/api/cases/{cid}/ai", data=json.dumps({"task": "not-a-task"}), headers={"Content-Type": "application/json"})
        out["unknown_ai_task_post"] = {"status": r2.status, "body": redact(r2.text())[:200]}
        r3 = c.request.post(APP + f"/api/cases/{cid}/ai", data=json.dumps({"task": "message", "mode": "x" * 5}), headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}) if False else None
    for path in ["/api/assistants", "/api/assistants/proposals", "/api/assistants/rai-metrics", "/api/chat", "/api/audit-check", "/api/cases.csv", "/api/assistants/proposals.csv", "/api/ai/report", "/api/ai/priority"]:
        r = c.request.get(APP + path)
        ent = {"status": r.status, "ctype": (r.headers.get("content-type") or "")[:40], "len": len(r.text())}
        try:
            j = r.json(); ent["keys"] = sorted(set(keys(j)))[:60]
        except Exception:
            if r.status == 200: ent["csv_header"] = r.text().splitlines()[0][:300] if r.text() else ""
        if r.status == 200:
            t = r.text(); ent["reason_like_hits"] = sorted(set(m.group(0).lower() for m in CANARY.finditer(t)))
        else:
            ent["body"] = redact(r.text())[:160]
        out[path] = ent
    page.goto(APP + "/", wait_until="networkidle")
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/workbench.png")
    b.close()
json.dump(out, open(f"{OUT}/probe2.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:7000])
