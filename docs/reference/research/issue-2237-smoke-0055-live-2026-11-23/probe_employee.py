"""Employee smoke on the demo API: retention, chat thread, map sensor overlay. Credentials are read at runtime and never printed or saved."""
import json, os, re
from collections import Counter
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().split("\n")[0].strip()
pw_ = open(home + "/.ama-test-user").read().split("\n")[0].strip()


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", pw_); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")


res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    failed = []
    pg.on("requestfailed", lambda r: failed.append(r.url.replace(H, "")[:60]))
    res["health_unauth"] = c.request.get(H + "/healthz", timeout=60000).status
    login(pg)
    me = c.request.get(H + "/api/me", timeout=60000)
    res["me_status"] = me.status
    res["role"] = me.json().get("user", {}).get("role") if me.ok else None
    hdr = {"X-ZF-CSRF": "1"}
    seq = []
    for _ in range(15):
        seq.append(c.request.get(H + "/api/retention", headers=hdr, timeout=90000).status)
    r = c.request.get(H + "/api/retention", headers=hdr, timeout=90000)
    j = r.json() if r.ok else {}
    res["retention"] = {"status": r.status, "burst_15_sequential": dict(Counter(seq)), "records": len(j.get("records") or []), "keys": sorted(j)[:8]}
    cj = c.request.get(H + "/api/cases?view=all&limit=5", headers=hdr, timeout=90000)
    cases = cj.json() if cj.ok else []
    if isinstance(cases, dict):
        cases = next((v for v in cases.values() if isinstance(v, list)), [])
    cid = cases[0].get("id") if cases else None
    jh = {**hdr, "Content-Type": "application/json"}
    pgfetch = "async([p,b])=>{const x=await fetch(p,{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:JSON.stringify(b)});const t=await x.text();let j={};try{j=JSON.parse(t)}catch(e){j={raw:t.slice(0,120)}};return [x.status,j]}"
    pg.goto(H + "/app#/overview", wait_until="networkidle")
    ts, tj = pg.evaluate(pgfetch, ["/api/chat/threads", {"case_id": cid}])
    scrub = lambda v: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", str(v))[:200]
    res["chat_thread"] = {"cases_status": cj.status, "case_found": bool(cid), "status": ts, "keys": sorted(tj)[:8], "error": scrub(tj.get("error") or tj.get("raw") or "")}
    if tj.get("id"):
        ms, mj = pg.evaluate(pgfetch, [f"/api/chat/threads/{tj['id']}/ask", {"content": "What is the status of this case?"}])
        res["chat_ask"] = {"status": ms, "keys": sorted(mj)[:8], "error": scrub(mj.get("error") or mj.get("raw") or "")}
    items = []
    mr = None
    for _ in range(4):
        mr = c.request.get(H + "/api/map", timeout=90000)
        if mr.ok and "items" in mr.json():
            items = mr.json()["items"]
            break
        pg.wait_for_timeout(5000)
    res["map"] = {"status": mr.status if mr else None, "homes": len(items), "sensor_states": dict(Counter((i.get("sensor") or {}).get("state") for i in items))}
    pg.goto(H + "/app#/overview")
    pg.wait_for_timeout(9000)
    pg.screenshot(path=f"{OUT}/screens/employee-map.png")
    res["map"]["markers_in_dom"] = pg.locator(".leaflet-marker-icon, .leaflet-interactive").count()
    res["map"]["unavailable_text"] = pg.get_by_text("Map unavailable").count()
    res["requestfailed"] = failed
    s = json.dumps(res, indent=1)
    assert u not in s and pw_ not in s
    open(OUT + "/probe-employee-result.json", "w").write(s)
    print(s)
    b.close()
