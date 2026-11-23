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


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(3000)
    r = call(pg, "/api/continuity")
    j = r["json"] or {}
    res["status"] = r["status"]
    res["keys"] = list(j)[:20] if isinstance(j, dict) else type(j).__name__
    res["suspensions"] = j.get("suspensions") if isinstance(j, dict) else None
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-continuity-result.json", "w").write(s)
    print(s[:3000])
    b.close()
