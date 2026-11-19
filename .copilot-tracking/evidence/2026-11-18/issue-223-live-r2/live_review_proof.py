"""Live demo review-retention probe (issue 223). Credentials read at runtime, never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")


def scrub(x):
    return json.loads(EMAIL.sub("[email]", json.dumps(x)))


def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def call(c, method, path, body=None):
    js = """async([m,p,b])=>{const o={method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'}};
      if(m==='POST')o.body=JSON.stringify(b||{});const x=await fetch(p,o);const t=await x.text();
      let j;try{j=JSON.parse(t)}catch(e){j={_text_len:t.length}};return [x.status,j]}"""
    s, j = PAGE.evaluate(js, [method, path, body])
    return s, j


res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg); pg.goto(APP + "/", wait_until="networkidle"); PAGE = pg
    s, me = call(c, "GET", "/api/me"); res["me"] = {"status": s, "role": me.get("user", {}).get("role")}
    s, cases = call(c, "GET", "/api/cases", None)
    lst = cases if isinstance(cases, list) else cases.get("items", [])
    res["cases"] = {"status": s, "count": len(lst)}
    cid = (lst[0].get("id") if lst else None); res["case_id"] = cid
    runs = {}
    for label, mode in (("workflow_only", "workflow-only"), ("ai_default", None)):
        s, j = call(c, "POST", f"/api/cases/{cid}/ai", {"task": "summary", "mode": mode})
        runs[label] = {"status": s, "keys": sorted(j.keys())[:30] if isinstance(j, dict) else None,
                       "source": j.get("source"), "model": j.get("model"), "verified": j.get("verified"),
                       "rec_status": j.get("status"), "id": j.get("record_id"),
                       "citations": j.get("citations"), "shown_output": str(j.get("shown_output"))[:300],
                       "err": j.get("error")}
    res["runs"] = scrub(runs)
    # review: reject one without reason (must fail), then reject with a source-named reason
    first = next((v["id"] for v in runs.values() if v.get("id")), None)
    if first:
        s, j = call(c, "POST", f"/api/ai/review/{first}/reject", {"reason": ""}); res["reject_no_reason"] = {"status": s, "err": j.get("error")}
        stage = None
        s, cj = call(c, "GET", f"/api/cases/{cid}")
        res["review_target"] = first
        s, j = call(c, "POST", f"/api/ai/review/{first}/reject", {"reason": "unsupported: demo seeded-defect probe [source: Stage:]"})
        res["reject_with_reason"] = scrub({"status": s, "rec_status": j.get("status"), "reviewer_action": j.get("reviewer_action"),
                                            "reviewer_reason": j.get("reviewer_reason"), "resolved_by_present": bool(j.get("resolved_by")),
                                            "review_evidence_keys": sorted((j.get("review_evidence") or {}).keys()),
                                            "source_hashes_present": bool((j.get("review_evidence") or {}).get("source_hashes")),
                                            "err": j.get("error")})
        s, j = call(c, "POST", f"/api/ai/review/{first}/accept", {}); res["second_review"] = scrub({"status": s, "err": j.get("error")})
    pg.goto(APP + "/", wait_until="networkidle"); pg.wait_for_timeout(3000)
    pg.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    pg.screenshot(path=f"{OUT}/live-workbench-r2.png")
    b.close()
json.dump(res, open(f"{OUT}/live_review_r2.json", "w"), indent=1)
print(json.dumps(res, indent=1)[:4000])
