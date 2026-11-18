"""Live demo probe for issue 531 criterion 7 (loading feedback and HAX briefing). Credentials read at runtime, never printed.

Synthetic simulations are labelled: route holds/aborts only delay or block requests in the browser; the server is not changed.
"""
import hashlib, json, os, re, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(OUT, "../../../../../src/api/src/zava_forward/api/web"))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
res = {"steps": []}


def clean(t):
    t = EMAIL.sub("[email]", t or "")
    return t.replace(USER, "[user]")


def step(name, **kw):
    res["steps"].append({"step": name, **kw})
    print(name, json.dumps(kw)[:300], flush=True)


def login(page):
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    page.wait_for_selector("#idSIButton9"); page.click("#idSIButton9")
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000, wait_until="commit")
    page.wait_for_timeout(3000)


def open_workbench(pg):
    pg.goto(APP + "/", wait_until="networkidle")
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(APP + "/app"), timeout=60000)
    pg.wait_for_selector(".briefing [data-record-id]", timeout=90000)


def shot(pg, name):
    pg.screenshot(path=os.path.join(OUT, name))


def run_axe(pg, selector):
    return pg.evaluate(AXE + """;(async(sel)=>{const r=await axe.run(document.querySelector(sel),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {version:axe.version,violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length})),passes:r.passes.length}})""" + f"({json.dumps(selector)})")



import hashlib
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    parity = {}
    for f in ("workspace-shell.js", "app.js", "async-action.js", "style.css"):
        r = c.request.get(f"{APP}/{f}")
        parity[f] = {"status": r.status, "match": hashlib.sha256(r.body()).hexdigest() == hashlib.sha256(open(os.path.join(WEB, f), "rb").read()).hexdigest()}
    step("asset_parity_with_branch", **parity)
    pg = c.new_page(); pg.goto(APP + "/app", wait_until="domcontentloaded"); open_workbench(pg); pg.wait_for_timeout(1500)
    br = pg.locator(".briefing")
    reqs = []
    pg.on("response", lambda r: reqs.append((r.url.split("?")[0].replace(APP, ""), r.request.method, r.status)) if "/api/ai/review/" in r.url else None)
    before = br.locator("[data-record-id]").get_attribute("data-record-id")
    br.get_by_role("button", name="Do not use this draft", exact=True).click()
    br.get_by_label("Reason", exact=True).fill("Synthetic live check for issue 531: reject path, no action taken")
    br.get_by_role("button", name="Record rejection", exact=True).click()
    pg.wait_for_timeout(4000)
    step("reject_recorded_via_ui", review_responses=[list(x) for x in reqs], status=clean(br.locator(".briefing-status").inner_text()),
         review_state=br.locator("[data-record-id]").first.get_attribute("data-review-state"),
         text=[clean(x.inner_text()) for x in br.locator("[role=status], .review-outcome, .flag").all()][:6],
         buttons=[x.inner_text() for x in br.locator("button:visible").all()])
    shot(pg, "briefing-reject-recorded-1366.png")
    # new load of /app timing and cache headers (observed, not cold)
    t0 = time.time(); r = c.request.get(APP + "/app"); step("app_get_ms", ms=round((time.time()-t0)*1000), status=r.status)
    json.dump(res, open(os.path.join(OUT, "live_531_delta.json"), "w"), indent=1)
    b.close()
