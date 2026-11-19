"""Issue 215 live demo proof. Reads credentials at runtime; prints only redacted facts."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
REDACT = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""


def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def shot(page, name):
    page.evaluate(REDACT); page.screenshot(path=f"{OUT}/{name}.png")


r = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    me = c.request.get(APP + "/api/me").json()
    r["role"] = me["user"]["role"]; r["services"] = me.get("services")
    cases = c.request.get(APP + "/api/cases")
    r["cases_status"] = cases.status
    cj = cases.json()
    items = cj.get("items", [])
    r["case_count"] = len(items)
    cid = items[0].get("id") or items[0].get("case_id")
    r["case_id_shape"] = re.sub(r"\d", "9", str(cid))
    a = c.request.get(APP + f"/api/law/alerts?case={cid}")
    r["law_alerts_status"] = a.status
    r["law_alerts_body"] = a.text()[:300]
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if pg.locator("text=Pick an account").count(): pg.locator("[data-test-id], .table-row, div[role=button]").first.click()
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000)
    r["workbench_title"] = pg.title()
    pg.goto(APP + f"/app#/case/{cid}"); pg.wait_for_timeout(5000)
    r["case_h1_h2"] = pg.locator("h1,h2").all_inner_texts()[:8]
    r["tabs"] = [x for x in pg.locator("button,[role=tab]").all_inner_texts() if x.strip()][:30]
    # open the blockers tab holding the alerts panel
    tab = pg.get_by_role("tab", name=re.compile("Blockers and safety"))
    r["blockers_tab_found"] = tab.count()
    if tab.count():
        tab.first.click(); pg.wait_for_timeout(2500)
    panel = pg.locator("#regulatory-alerts")
    r["alerts_panel_present"] = panel.count()
    if panel.count():
        panel.scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
        r["alerts_status_text"] = panel.locator("[role=status]").first.inner_text()[:400]
        r["alert_articles"] = panel.locator("article.regulatory-alert").count()
        r["plain_mode_default_checked"] = panel.locator("#alerts-plain-mode").is_checked()
        r["plain_visible_on"] = panel.locator(".plain-explanation").first.is_visible() if panel.locator(".plain-explanation").count() else None
        shot(pg, "alerts-1-panel-plain-on")
        # keyboard: focus the checkbox, press Space to toggle off
        panel.locator("#alerts-plain-mode").focus()
        pg.keyboard.press("Space"); pg.wait_for_timeout(500)
        r["plain_after_space_checked"] = panel.locator("#alerts-plain-mode").is_checked()
        r["mode_html"] = panel.locator(".regulatory-mode").first.evaluate("e=>e.outerHTML")[:500] if panel.locator(".regulatory-mode").count() else None
        r["plain_mode_state_text"] = panel.locator(".regulatory-mode-state").first.text_content(timeout=3000) if panel.locator(".regulatory-mode-state").count() else None
        r["plain_visible_off"] = panel.locator(".plain-explanation").first.is_visible() if panel.locator(".plain-explanation").count() else None
        shot(pg, "alerts-2-panel-plain-off")
        pg.keyboard.press("Space"); pg.wait_for_timeout(300)
        # keyboard: refresh button reachable and operable
        rb = panel.get_by_role("button", name="Refresh alerts")
        rb.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(2500)
        r["refresh_keyboard_status_text"] = panel.locator("[role=status]").first.inner_text()[:400]
        # tab order inside the panel: every interactive element reachable
        r["panel_interactives"] = panel.locator("button,a[href],input,summary,[tabindex]").count()
        # non-colour check: every .regulatory-state has visible text
        states = panel.locator(".regulatory-state")
        r["state_elements"] = states.count()
        r["state_elements_with_text"] = sum(1 for i in range(states.count()) if states.nth(i).inner_text().strip())
        r["state_text_samples"] = [states.nth(i).inner_text()[:80] for i in range(min(states.count(), 6))]
    # chat panel on same case
    chat = pg.locator("#regulatory-chat")
    r["regulatory_chat_present"] = chat.count()
    if chat.count():
        chat.locator("summary").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
        r["chat_open_by_keyboard"] = chat.evaluate("e=>e.open")
        r["chat_plain_checked"] = chat.locator("#chat-plain-mode").is_checked()
        shot(pg, "chat-1-open")
        q = chat.locator("#regulatory-question")
        r["chat_input_disabled"] = q.is_disabled()
        r["chat_input_label_for"] = chat.locator("label[for=regulatory-question]").first.text_content(timeout=3000) if chat.locator("label[for=regulatory-question]").count() else None
        r["chat_panel_text"] = chat.inner_text()[:1400]
        r["chat_ask_buttons_disabled"] = [bt.is_disabled() for bt in chat.get_by_role("button").all()]
        r["chat_usage_text"] = chat.locator("#regulatory-usage").text_content(timeout=3000) if chat.locator("#regulatory-usage").count() else None
        shot(pg, "chat-2-state")
        pg.keyboard.press("Escape")
        r["chat_closed_by_escape"] = not chat.evaluate("e=>e.open")
    b.close()
json.dump(r, open(f"{OUT}/employee-run1.json", "w"), indent=1)
print(json.dumps(r, indent=1)[:5000])
