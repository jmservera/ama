"""Live probe for #2256: compare the case handoff, the three handoff queues and the waiting screen."""
import json, os
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("load"); page.wait_for_timeout(5000)


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    me = c.request.get(H + "/api/me", timeout=120000).json()["user"]
    res["role"] = me["role"]
    for name in ("handoffs", "handoffs/unaccepted", "handoffs/unowned", "handoffs/escalated"):
        r = c.request.get(f"{H}/api/{name}", timeout=90000)
        body = r.json() if r.ok else None
        res[name] = {"status": r.status, "count": len(body) if isinstance(body, list) else None,
                     "case_ids": [x.get("case_id") for x in body][:60] if isinstance(body, list) else None}
    cs = c.request.get(f"{H}/api/cases", timeout=90000)
    items = cs.json() if cs.ok else []
    items = items.get("items", items) if isinstance(items, dict) else items
    res["cases_count"] = len(items)
    offered = []
    for it in items:
        hd = it.get("handoff") or {}
        if hd.get("state") in ("Offered", "Received", "Escalated"):
            offered.append({"id": it["id"], "state": hd["state"], "from_code": hd.get("from_code"),
                            "to_code": hd.get("to_code"), "to_role": hd.get("to_role"), "closed": it.get("closed")})
    res["list_open_offers"] = offered
    one = c.request.get(f"{H}/api/cases/ZF-2025-0030", timeout=90000)
    if one.ok:
        d = one.json()
        res["ZF-2025-0030"] = {"closed": d.get("closed"), "handoff": {k: v for k, v in (d.get("handoff") or {}).items() if k in ("state", "from_code", "to_code", "to_role", "offered_at", "due_at")}}
    pg.goto(H + "/app#/handoff-waiting")
    pg.wait_for_timeout(8000)
    res["screen_text"] = pg.locator("main").inner_text()[:600] if pg.locator("main").count() else pg.inner_text("body")[:600]
    pg.screenshot(path=f"{OUT}/screens/handoff-waiting-live.png", full_page=True)
    b.close()
json.dump(res, open(f"{OUT}/probe-handoff-waiting-result.json", "w"), indent=2)
print(json.dumps(res, indent=1)[:3500])
