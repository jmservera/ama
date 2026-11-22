"""Live check for #2256: pending handoffs versus the waiting list. Sign-in values are read at run time, never printed."""
import json, os, re
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
    page.wait_for_load_state("networkidle")


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    for name, path in (("handoffs", "/api/handoffs"), ("unaccepted", "/api/handoffs/unaccepted")):
        r = c.request.get(H + path, timeout=90000)
        try:
            body = r.json()
        except Exception:
            body = None
        rows = body if isinstance(body, list) else (body or {}).get("items", (body or {}).get("rows", []))
        res[name] = {"status": r.status, "rows": len(rows), "keys": sorted(rows[0].keys()) if rows else [],
                     "sample": [{k: v for k, v in x.items() if k in ("case_id", "status", "offered_at", "due_at", "age_hours", "reasons", "chase_owner", "needs_escalation", "receiver")} for x in rows[:4]]}
    pg.goto(H + "/app#/handoff-waiting")
    pg.wait_for_timeout(8000)
    res["screen_text"] = re.sub(r"\s+", " ", pg.inner_text("main"))[:1500]
    pg.screenshot(path=f"{OUT}/screens/handoff-waiting.png")
    b.close()
json.dump(res, open(f"{OUT}/probe-handoff-result.json", "w"), indent=2)
print(json.dumps(res, indent=1)[:3500])
