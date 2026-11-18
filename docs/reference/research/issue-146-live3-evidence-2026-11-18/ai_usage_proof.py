"""Issue 146 live proof: AI usage by capability on the deployed demo. Credentials are read at run time and never printed."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")


def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def scrub(page):
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")


out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    login(page)
    me = c.request.get(APP + "/api/me").json()
    out["role"] = me["user"].get("role")
    out["nav"] = [n.get("href") for n in me.get("navigation", [])]
    r = c.request.get(APP + "/api/ai/report")
    out["report_status"] = r.status
    if r.status == 200:
        m = r.json().get("consumption", {})
        out["consumption"] = {k: m.get(k) for k in ("coverage", "reconciliation", "total_cost_of_ai", "token_cost", "currency", "calls", "failures", "reason")}
        out["by_capability"] = {k: {kk: v.get(kk) for kk in ("calls", "total_tokens")} for k, v in (m.get("by_capability") or {}).items()}
        out["owned_alerts_count"] = len(m.get("owned_alerts") or [])
    page.goto(APP + "/", wait_until="networkidle")
    page.click("text=Sign in to the workbench"); page.wait_for_timeout(3000)
    if "login.microsoftonline.com" in page.url:
        if page.locator("text=Pick an account").count():
            page.locator("[data-test-id], .table-row, div[role=button]").first.click()
        elif page.locator("input[name=loginfmt]").count():
            login(page)
        for _ in range(3):
            if page.url.startswith(APP): break
            try:
                btn = page.query_selector("#idSIButton9, #idBtn_Back")
                if btn: btn.click()
            except Exception:
                pass
            page.wait_for_timeout(3000)
        page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    page.wait_for_load_state("networkidle"); page.wait_for_timeout(4000)
    out["after_click_has_nav"] = page.locator("#nav a").count()
    scrub(page); page.screenshot(path=f"{OUT}/page-after-signin.png")
    page.evaluate("h=>{location.hash=h}", "#/screens"); page.wait_for_timeout(4000)
    cj = c.request.get(APP + "/api/cases").json()
    cl = cj if isinstance(cj, list) else (cj.get("cases") or cj.get("items") or [])
    cid = cl[0]["id"] if cl else None
    out["case_count"] = len(cl)
    page.evaluate("h=>{location.hash=h}", f"#/screens?screen=asset-board&case={cid}"); page.wait_for_timeout(9000)
    out["asset_hash"] = page.evaluate("location.hash")
    t = lambda x: page.locator(f"text={x}").count() > 0
    out["asset_view"] = {k: t(k) for k in ("Metered usage by AI capability", "Reconciliation with the bill", "Total Cost of AI", "chat-case-conversation", "Held-call and limit alerts")}
    scrub(page); page.screenshot(path=f"{OUT}/asset-view-top.png", full_page=True)
    out["asset_text_head"] = page.locator("main, #app, body").first.inner_text()[:600]
    el = page.locator("text=Metered usage by AI capability").first
    if el.count():
        el.scroll_into_view_if_needed(); page.wait_for_timeout(800); scrub(page); page.screenshot(path=f"{OUT}/asset-usage-by-capability.png")
        rc = page.locator("text=Reconciliation with the bill").first
        if rc.count():
            rc.scroll_into_view_if_needed(); page.wait_for_timeout(800); scrub(page); page.screenshot(path=f"{OUT}/asset-usage-reconciliation.png")
            out["reconciliation_row_text"] = rc.locator("xpath=ancestor::*[self::div or self::tr or self::dl][1]").inner_text()[:300]
    b.close()
print(json.dumps(out, indent=1))
