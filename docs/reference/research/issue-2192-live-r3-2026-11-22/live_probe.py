"""Live demo proof for issue 2192: resident consent checkbox against the employee sensor view. Credentials are read at runtime and never printed."""
import json, os, re, time
from playwright.sync_api import sync_playwright

RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
ru, rp = [x.strip() for x in rd(".ama-resident-test-user")[:2]]
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
scrub = lambda x: json.loads(EMAIL.sub("[email]", json.dumps(x)))
res = {}


def emp_login(page):
    page.goto(EMP + "/api/me", wait_until="domcontentloaded", timeout=120000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(EMP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(EMP)), timeout=60000)
    page.goto(EMP + "/", wait_until="networkidle")


def api(page, path):
    js = "async p=>{const x=await fetch(p,{headers:{'X-ZF-CSRF':'1'}});const t=await x.text();let j;try{j=JSON.parse(t)}catch(e){j={}};return [x.status,j]}"
    return page.evaluate(js, path)


def employee_states(page, ids):
    out = {}
    for cid in ids:
        s, j = api(page, f"/api/cases/{cid}/sensors")
        out[cid] = {"status": s, "state": j.get("state") or j.get("status"), "readings": len(j.get("readings") or j.get("items") or []), "message": (j.get("message") or j.get("reason") or "")[:120], "keys": sorted(j)[:12]}
    return scrub(out)


with sync_playwright() as p:
    b = p.chromium.launch()
    ec = b.new_context(viewport={"width": 1366, "height": 1000}); ep = ec.new_page()
    emp_login(ep)
    s, cases = api(ep, "/api/cases"); lst = cases if isinstance(cases, list) else cases.get("items", [])
    allids = [x.get("id") for x in lst]; res["case_count"] = len(allids)

    rc = b.new_context(viewport={"width": 1366, "height": 1200}); rpg = rc.new_page()
    rpg.goto(RES + "/", wait_until="load", timeout=180000)
    rpg.wait_for_selector("#signin:not([hidden]), #content:not([hidden])", timeout=120000)
    if rpg.locator("#signin").is_visible():
        rpg.fill("#email", ru); rpg.fill("#password", rp); rpg.click("#signin-button")
    rpg.wait_for_selector("#content:not([hidden])", timeout=120000); rpg.wait_for_timeout(2500)
    m = re.search(r"ZF-\d{4}-\d{4}", rpg.locator("#content").inner_text())
    res["resident_case"] = m.group(0) if m else None
    # The resident page does not print its case reference; the case is Flat 1, Tebay Drive, Contact paused (ZF-2025-0029,
    # confirmed from the employee map card in issue-2202-live-2026-11-21/probe-staff-result.json), outside the first 50 listed cases.
    ids = ["ZF-2025-0029"]; res["resident_case"] = ids[0]
    res["employee_before"] = employee_states(ep, ids)
    box = rpg.locator("#sensor-consent"); res["checkbox_present"] = box.count() == 1
    sec = rpg.locator(".sensor-consent")
    res["resident_text"] = sec.inner_text() if sec.count() else None
    res["initial_checked"] = box.is_checked() if box.count() else None
    res["checkbox_attrs"] = rpg.evaluate("()=>{const i=document.getElementById('sensor-consent');return i?{type:i.type,labelWrapped:!!i.closest('label'),described:i.getAttribute('aria-describedby'),role:i.getAttribute('role')}:null}")
    sec.scroll_into_view_if_needed(); sec.screenshot(path=f"{OUT}/resident-initial.png")
    initial = res["initial_checked"]

    def set_state(want):
        box.focus()
        if box.is_checked() != want:
            rpg.keyboard.press("Space")
        rpg.wait_for_function("()=>!document.getElementById('sensor-consent').disabled", timeout=90000)
        rpg.wait_for_timeout(1500)
        return {"checked": box.is_checked(), "status": rpg.locator("#sensor-consent-status").inner_text(), "focus_on_checkbox": rpg.evaluate("()=>document.activeElement&&document.activeElement.id")}

    if box.count() and initial is not None:
        try:
            res["step1_set_opposite"] = set_state(not initial)
            sec.screenshot(path=f"{OUT}/resident-changed.png"); time.sleep(3)
            res["employee_after_step1"] = employee_states(ep, ids)
            res["step2_back_to_initial"] = set_state(initial)
            sec.screenshot(path=f"{OUT}/resident-restored.png"); time.sleep(3)
            res["employee_after_step2"] = employee_states(ep, ids)
        finally:
            res["final_restore"] = set_state(initial)
        rpg.reload(wait_until="load"); rpg.wait_for_selector("#content:not([hidden])", timeout=120000); rpg.wait_for_timeout(2500)
        res["reload_checked"] = rpg.locator("#sensor-consent").is_checked()
    b.close()
json.dump(res, open(f"{OUT}/live_probe.json", "w"), indent=1)
print({k: (v if not isinstance(v, (dict, list)) or k in ("step1_set_opposite","step2_back_to_initial","final_restore") else "...") for k, v in res.items() if k != "resident_text"})
