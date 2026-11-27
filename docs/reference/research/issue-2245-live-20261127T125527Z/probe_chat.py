"""Live probe of employee chat on the demo API (issue 2245). Credentials are read at runtime and never written."""
import json, os, time
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
CASE = "ZF-2025-0031"
QUESTIONS = [
    ("rules-first claim", CASE, "Is this case eligible and ready to claim?"),
    ("rules-first sensor", CASE, "What do the sensor readings show?"),
    ("free-form case", CASE, "Summarise in two sentences what is known about this home and who owns the next step."),
    ("free-form case 2", CASE, "Explain why this case is waiting and what a person should check first."),
    ("general no case", "", "What should a programme manager check before scheduling a retrofit visit?"),
]

JS = """async ([path, body]) => {
  const t0 = performance.now();
  const r = await fetch(path, {method: body === null ? 'GET' : 'POST', credentials: 'same-origin',
    headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'}, body: body === null ? undefined : JSON.stringify(body)});
  let j = null; try { j = await r.json(); } catch (e) {}
  return {status: r.status, ms: Math.round(performance.now() - t0), json: j};
}"""


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
    try:
        page.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        pass


def call(pg, path, body=None):
    return pg.evaluate(JS, [path, body])


res = {"revision_note": "recorded separately from az", "creates": [], "asks": []}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(3000)
    res["status"] = call(pg, "/api/chat/status")
    me = call(pg, "/api/me"); res["me"] = {"status": me["status"], "role": (me["json"] or {}).get("role")}
    for _ in range(8):
        r = call(pg, "/api/chat/threads", {"case_id": CASE})
        res["creates"].append({"status": r["status"], "ms": r["ms"], "error": (r["json"] or {}).get("error")})
        time.sleep(0.5)
    for label, case, q in QUESTIONS:
        t = call(pg, "/api/chat/threads", {"case_id": case} if case else {})
        tid = (t["json"] or {}).get("id")
        entry = {"label": label, "create_status": t["status"], "create_error": (t["json"] or {}).get("error")}
        if tid:
            a = call(pg, f"/api/chat/threads/{tid}/ask", {"content": q})
            j = a["json"] or {}
            entry.update(status=a["status"], ms=a["ms"], kind=j.get("kind"), model=j.get("model"),
                         skill=j.get("skill"), receipt=j.get("receipt"), origin=j.get("origin"),
                         text_head=str(j.get("content") or j.get("text") or j)[:300])
            call(pg, f"/api/chat/threads/{tid}/delete", {})
        res["asks"].append(entry)
    pg.goto(H + "/app#/case/" + CASE)
    pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT + "/screens/case-page.png")
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-chat-result.json", "w").write(s)
    print(s[:6000])
    b.close()
