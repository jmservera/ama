"""Resident demo app sign-in proof (issue 349). Reads credentials at runtime; prints redacted facts only."""
import json, os, re
from playwright.sync_api import sync_playwright

R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: [x.strip() for x in open(os.path.expanduser(n)).read().split("\n") if x.strip()]
res = rd("~/.ama-resident-test-user"); emp_user = rd("~/.ama-test-user-id")[0]; emp_pw = rd("~/.ama-test-user")[0]
out = {}

def signin(page, email, pw):
    page.goto(R + "/"); page.click("#email"); page.keyboard.type(email); page.keyboard.press("Tab")
    page.keyboard.type(pw)
    with page.expect_response("**/demo/login") as r:
        page.keyboard.press("Enter")
    return r.value.status

def mask(page):
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}document.querySelectorAll('input').forEach(i=>i.value='')}""")

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    out["anonymous_view"] = c.request.get(R + "/demo/view").status
    pg.goto(R + "/"); pg.screenshot(path=f"{OUT}/resident-1-signin-form.png")
    out["resident_login_status"] = signin(pg, res[0], res[1])
    pg.wait_for_timeout(1500)
    s = c.request.get(R + "/demo/session").json()
    out["resident_signed_in"] = s.get("signed_in"); sid = s.get("session_id")
    v = c.request.get(R + "/demo/view", headers={"X-Resident-Session": sid or ""})
    out["resident_view_status"] = v.status
    if v.status == 200:
        j = v.json(); out["resident_view_keys"] = sorted(j.keys())[:12]
    for path in ["/api/me", "/api/cases", "/api/staff", "/demo/staff", "/demo/admin"]:
        out.setdefault("staff_path_probe", {})[path] = c.request.get(R + path, headers={"X-Resident-Session": sid or ""}).status
    mask(pg); pg.screenshot(path=f"{OUT}/resident-2-signed-in.png")
    b.close()
    # wrong credential classes
    for tag, u, pw in [("wrong_password", res[0], "x" + res[1][::-1]), ("employee_entra_account_on_resident_app", emp_user, emp_pw)]:
        b = p.chromium.launch(); c = b.new_context(); pg = c.new_page()
        out[tag + "_login_status"] = signin(pg, u, pw)
        out[tag + "_signed_in"] = c.request.get(R + "/demo/session").json().get("signed_in")
        out[tag + "_view"] = c.request.get(R + "/demo/view").status
        b.close()
    # sign-out
    b = p.chromium.launch(); c = b.new_context(); pg = c.new_page()
    signin(pg, res[0], res[1]); pg.wait_for_timeout(1000)
    sid = c.request.get(R + "/demo/session").json()["session_id"]
    btn = pg.locator("#signout")
    out["signout_control_found"] = btn.count() > 0
    pg.locator("#account > summary").click()
    btn.click(); pg.wait_for_selector("#signin:not([hidden])")
    out["after_signout_view_old_fence"] = c.request.get(R + "/demo/view", headers={"X-Resident-Session": sid}).status
    out["after_signout_signed_in"] = c.request.get(R + "/demo/session").json().get("signed_in")
    b.close()
print(json.dumps(out, indent=1))
