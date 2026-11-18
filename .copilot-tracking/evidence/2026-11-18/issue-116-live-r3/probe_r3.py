"""Round 3: read-only sweep of every GET endpoint in the repo role inventory as the one signed-in role; status, reason-value leak counts, allowed/denied pattern."""
import ast, json, os, re, sys
from playwright.sync_api import sync_playwright
import os
APP = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.expanduser("~/" + n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")
SRC = "/home/azureuser/source/ama-wt/issue-116-live-20261118T1719Z/src/api/tests/test_role_endpoint_inventory.py"
txt = open(SRC).read()
block = txt[txt.index("GET_ENDPOINTS = ["):txt.index("POST_ENDPOINTS")]
gets = [g for g in re.findall(r'"(/api/[^"]*)"', block) if "REASON" not in g]
def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000); page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception: break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=90000)
out = {"endpoints": {}}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = c.request.get(APP + "/api/me").json(); u = me.get("user", me)
    out["me"] = {k: u.get(k) for k in ("role", "app_roles", "view_only", "identity_source", "provider")}
    items = c.request.get(APP + "/api/cases?view=all").json()["items"]
    vals = set()
    for it in items:
        d = c.request.get(APP + "/api/cases/" + it["id"]).json()
        for f in ("adjustment", "priority_support"):
            v = d.get("resident", {}).get(f)
            if isinstance(v, str) and len(v) > 3 and v != "None": vals.add(v)
    out["distinct_reason_values"] = len(vals); out["cases"] = len(items)
    cid = items[0]["id"]
    for g in gets:
        path = re.sub(r"ZF-1", cid, g)
        if "q=" in path and "Quentin" not in path and "q=x" not in path: path = path.split("q=")[0] + "q=" + sorted(vals)[0][:20] if vals else path
        r = c.request.get(APP + path)
        t = r.text()
        out["endpoints"][g if "q=" not in g else g.split("q=")[0] + "q=<probe>"] = {"status": r.status, "bytes": len(t), "reason_value_hits": sum(t.count(v) for v in vals)}
    # POST refusal before provider call (read-only effect): unknown task
    page.goto(APP + "/app", wait_until="domcontentloaded")
    out["unknown_task_refusal"] = page.evaluate("""async (cid)=>{const r=await fetch('/api/cases/'+cid+'/ai',{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:JSON.stringify({task:'no-such-task'})});return [r.status,(await r.text()).slice(0,80)]}""", cid)
    b.close()
from collections import Counter
out["status_counts"] = dict(Counter(str(e["status"]) for e in out["endpoints"].values()))
out["total_reason_value_hits"] = sum(e["reason_value_hits"] for e in out["endpoints"].values())
out["hit_endpoints"] = [k for k, e in out["endpoints"].items() if e["reason_value_hits"]]
json.dump(out, open(OUT + "/probe_r3.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "endpoints"}, indent=1))
