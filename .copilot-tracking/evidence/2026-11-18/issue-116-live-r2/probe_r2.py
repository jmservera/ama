"""Round 2 live probe for #116. Credentials read at runtime, never printed; only redacted facts retained."""
import json, os, re
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.expanduser("~/" + n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")
CANARY = re.compile(r"vulnerab|disabilit|medical|adjustment|priority_support|reason", re.I)
def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception: break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=90000)
def keys(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield pre + k; yield from keys(v, pre + k + ".")
    elif isinstance(o, list):
        for v in o[:3]: yield from keys(v, pre + "[].")
def scrub(t): return re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t)
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = c.request.get(APP + "/api/me").json()
    out["me"] = {"role": me.get("role"), "app_roles": me.get("app_roles"), "view_only": me.get("view_only"), "identity_source": me.get("identity_source")}
    items = c.request.get(APP + "/api/cases").json()["items"]
    out["case_count"] = len(items)
    cid = items[0]["id"]
    paths = {"case_detail": f"/api/cases/{cid}", "cases_csv": "/api/cases.csv", "proposals": "/api/assistants/proposals",
             "proposals_csv": "/api/assistants/proposals.csv", "rai_metrics": "/api/assistants/rai-metrics",
             "audit_check": "/api/audit-check", "ai_report": "/api/ai/report", "assistants": "/api/assistants"}
    for k, path in paths.items():
        r = c.request.get(APP + path); t = r.text(); e = {"status": r.status, "bytes": len(t)}
        try:
            j = r.json(); ks = sorted(set(keys(j))); e["canary_keys"] = [x for x in ks if CANARY.search(x)][:25]
        except Exception:
            e["header"] = scrub(t.split("\n")[0])[:200]
        e["canary_text_hits"] = len(CANARY.findall(t))
        out[k] = e
    # case detail vulnerability values (non-empty?) across all cases
    vals = 0
    for it in items:
        d = c.request.get(APP + "/api/cases/" + it["id"]).json()
        res = d.get("resident", {})
        if res.get("adjustment") or res.get("priority_support"): vals += 1
    out["cases_with_reason_value"] = vals
    page.goto(APP + "/app", wait_until="networkidle"); page.wait_for_timeout(2500)
    page.screenshot(path=OUT + "/workbench-signed-in.png")
    out["app_title"] = page.title()
    b.close()
json.dump(out, open(OUT + "/probe_r2.json", "w"), indent=1)
print("ok", len(out))
