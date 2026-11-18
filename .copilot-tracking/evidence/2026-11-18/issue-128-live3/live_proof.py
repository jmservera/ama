"""Live desktop axe and route probe for issue 128 on the synthetic demo. Credentials read at runtime, never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "..", "issue-619-live"))
from employee_proof_lib import APP, login, axe  # noqa: E402

R = os.environ["DEMO_RESIDENT_URL"]
home = os.path.expanduser("~")
rr = [x.strip() for x in open(os.path.join(home, ".ama-resident-test-user")).read().split("\n") if x.strip()]
res = {"steps": []}
step = lambda n, **kw: res["steps"].append({"step": n, **kw})
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
KW = re.compile(r"usab|particip|research|survey|sus_|interview", re.I)

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    login(pg); pg.goto(APP + "/", wait_until="networkidle")
    for path in ("/openapi.json", "/docs"):
        r = c.request.get(APP + path)
        step("probe" + path, status=r.status)
    r = c.request.get(APP + "/openapi.json")
    paths = list(r.json().get("paths", {})) if r.status == 200 and "json" in (r.headers.get("content-type") or "") else None
    if paths is not None:
        step("route_inventory", total=len(paths), research_like=[x for x in paths if KW.search(x)])
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(APP + "/app"), timeout=60000); pg.wait_for_timeout(4000)
    step("axe_workbench_1366", url_path="/app", **axe(pg))
    pg.screenshot(path=os.path.join(OUT, "workbench-1366.png"))
    items = pg.evaluate("""async()=>{const r=await fetch('/api/cases');const j=await r.json();return j.items||j}""")
    cid = items[0]["id"]
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(3000)
    step("axe_case_1366", **axe(pg))
    body = EMAIL.sub("[email]", pg.locator("body").inner_text())
    step("case_ownership_text", owner_visible=bool(re.search(r"\bowner\b", body, re.I)), next_action_visible=bool(re.search(r"next (step|action)", body, re.I)),
         human_review_text=bool(re.search(r"human|review", body, re.I)), manual_alt=bool(re.search(r"manual|phone|paper|person can help", body, re.I)))
    pg.screenshot(path=os.path.join(OUT, "case-1366.png"))
    b.close()
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(R + "/", wait_until="domcontentloaded", timeout=120000)
    step("axe_resident_signed_out_1366", **axe(pg))
    pg.click("#email"); pg.keyboard.type(rr[0]); pg.keyboard.press("Tab"); pg.keyboard.type(rr[1]); pg.keyboard.press("Enter")
    pg.wait_for_selector("#signin", state="hidden", timeout=90000)
    try:
        pg.wait_for_function("!/still signing you in/i.test(document.body.innerText)", timeout=90000)
    except Exception:
        step("resident_still_loading_after_90s")
    pg.wait_for_timeout(4000)
    step("axe_resident_signed_in_1366", **axe(pg))
    t = EMAIL.sub("[email]", pg.locator("body").inner_text())
    step("resident_text", manual_route=bool(re.search(r"phone|letter|visit|person can help|paper", t, re.I)))
    pg.screenshot(path=os.path.join(OUT, "resident-1366.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, "live_proof.json"), "w"), indent=1)
print(json.dumps(res)[:3000])
