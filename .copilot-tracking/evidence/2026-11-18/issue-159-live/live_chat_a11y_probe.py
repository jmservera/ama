"""Live demo chat keyboard and announcement probe (issue 159). Credentials read at runtime, never printed."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
res = {"steps": []}
threads = []


def step(name, **kw):
    res["steps"].append({"step": name, **kw})


def login(page):
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    page.wait_for_selector("#idSIButton9"); page.click("#idSIButton9")
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000, wait_until="commit")
    page.wait_for_timeout(3000)


def active(page):
    return page.evaluate("""()=>{const a=document.activeElement;return {tag:a.tagName,id:a.id,name:(a.getAttribute('aria-label')||a.textContent||'').trim().slice(0,60)}}""")


with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.on("response", lambda r: threads.append(r.url) if r.url.endswith("/api/chat/threads") and r.request.method == "POST" else None)
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    pg.goto(APP + "/", wait_until="networkidle")
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(APP + "/app"), timeout=60000); pg.wait_for_timeout(4000)
    cases = pg.evaluate("""async()=>{const r=await fetch('/api/cases');return r.json()}""")
    items = cases.get("items", cases) if isinstance(cases, dict) else cases
    cid = items[0]["id"]
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    pg.evaluate("document.activeElement.blur()")
    lau = pg.locator("#employee-chat-launcher")
    step("launcher", visible=lau.is_visible(), aria_label=lau.get_attribute("aria-label"), tag=lau.evaluate("e=>e.tagName"))
    # keyboard-only: Tab until launcher is focused
    seq = []
    for _ in range(60):
        pg.keyboard.press("Tab"); a = active(pg); seq.append(a["id"] or a["name"])
        if a["id"] == "employee-chat-launcher": break
    step("tab_reaches_launcher", tab_presses=len(seq), reached=active(pg)["id"] == "employee-chat-launcher")
    pg.keyboard.press("Enter")
    pg.wait_for_selector("#employee-chat:not([hidden])"); pg.wait_for_function("()=>!document.querySelector('#employee-chat-question').disabled", timeout=30000)
    step("enter_opens_dialog_focus", focus=active(pg), role=pg.locator("#employee-chat").get_attribute("role"), expanded=lau.get_attribute("aria-expanded"))
    sem = pg.evaluate("""()=>{const q=s=>document.querySelector(s);const at=(e,n)=>e&&e.getAttribute(n);return {
      log:{role:at(q('#employee-chat .chat-widget-log'),'role'),live:at(q('#employee-chat .chat-widget-log'),'aria-live'),relevant:at(q('#employee-chat .chat-widget-log'),'aria-relevant'),label:at(q('#employee-chat .chat-widget-log'),'aria-label'),tabindex:at(q('#employee-chat .chat-widget-log'),'tabindex')},
      status:{role:at(q('#employee-chat .chat-widget-status'),'role'),live:at(q('#employee-chat .chat-widget-status'),'aria-live'),atomic:at(q('#employee-chat .chat-widget-status'),'aria-atomic')},
      error:{role:at(q('#employee-chat .chat-widget-error'),'role'),live:at(q('#employee-chat .chat-widget-error'),'aria-live')},
      input:{label:at(q('#employee-chat-question'),'aria-label'),describedby:at(q('#employee-chat-question'),'aria-describedby')}}}""")
    step("live_region_semantics", **sem)
    # record announcements: observe log additions and status text changes
    pg.evaluate("""()=>{window.__ann=[];const l=document.querySelector('#employee-chat .chat-widget-log');
      new MutationObserver(m=>m.forEach(x=>x.addedNodes.forEach(n=>window.__ann.push({region:'log',text:(n.textContent||'').trim().slice(0,160)})))).observe(l,{childList:true,subtree:true});
      const s=document.querySelector('#employee-chat .chat-widget-status');
      new MutationObserver(()=>window.__ann.push({region:'status',text:s.textContent})).observe(s,{childList:true,characterData:true,subtree:true});}""")
    path = []
    for _ in range(20):
        pg.keyboard.press("Tab"); a = active(pg); path.append(a["id"] or a["name"] or a["tag"])
        if a["id"] == "employee-chat-question": break
    step("tab_from_heading_to_input", sequence=path, reached=active(pg)["id"] == "employee-chat-question")
    pg.keyboard.type("What is the current stage of this case and which sources support that?")
    pg.keyboard.press("Enter")
    pg.wait_for_function("()=>document.querySelectorAll('#employee-chat .chat-widget-log > *').length>=2", timeout=60000)
    pg.wait_for_timeout(2500)
    ann = pg.evaluate("window.__ann")
    step("enter_sends_and_announces", announcements=[{**a, "text": EMAIL.sub("[email]", a["text"])} for a in ann], focus_after=active(pg),
         log_items=pg.evaluate("document.querySelectorAll('#employee-chat .chat-widget-log > *').length"))
    # follow up with shift+enter newline then send
    pg.keyboard.type("Line one"); pg.keyboard.press("Shift+Enter"); pg.keyboard.type("line two")
    step("shift_enter_newline", value_has_newline="\n" in pg.input_value("#employee-chat-question"))
    pg.keyboard.press("Enter")
    pg.wait_for_function("()=>document.querySelectorAll('#employee-chat .chat-widget-log > *').length>=4", timeout=60000); pg.wait_for_timeout(2000)
    step("second_turn_announced", log_items=pg.evaluate("document.querySelectorAll('#employee-chat .chat-widget-log > *').length"),
         announcements_total=len(pg.evaluate("window.__ann")))
    pg.screenshot(path=os.path.join(OUT, "chat-open-after-keyboard-turns-1366.png"))
    # tab cycle inside dialog, reach log and send via keyboard
    tabs = []
    for _ in range(5):
        pg.keyboard.press("Tab"); a = active(pg); tabs.append(a["id"] or a["name"][:40])
    step("tab_order_in_dialog", sequence=tabs)
    axe = pg.evaluate(AXE + """;(async()=>{const r=await axe.run(document.querySelector('#employee-chat'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length})),passes:r.passes.length}})()""")
    step("axe_wcag22aa_dialog", **axe)
    pg.focus("#employee-chat-question"); pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    step("escape_closes_returns_focus", dialog_hidden=pg.locator("#employee-chat").is_hidden(), focus=active(pg), expanded=lau.get_attribute("aria-expanded"))
    # cleanup: delete created threads through API
    ids = pg.evaluate("""async()=>{const r=await fetch('/api/chat/threads');const j=await r.json();return (j.items||j).map(t=>t.id)}""")
    step("threads_listed", count=len(ids))
    dels = []
    for t in ids:
        d = pg.evaluate("""async t=>{const r=await fetch('/api/chat/threads/'+t+'/delete',{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:'{}'});return r.status}""", t)
        dels.append(d)
    step("threads_deleted", statuses=dels)
    b.close()
json.dump(res, open(os.path.join(OUT, "live_chat_a11y_probe.json"), "w"), indent=1)
for s in res["steps"]: print(json.dumps(s)[:400])
