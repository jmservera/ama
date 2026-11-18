"""Live employee case view and chat widget keyboard, axe, reflow and reduced-motion proof (issue 619).
Credentials read at runtime, never printed. Output is redacted."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
TAGS = "['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']"
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
res = {"steps": []}


def step(_n, **kw):
    res["steps"].append({"step": _n, **kw})


def login(page):
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def active(page):
    return page.evaluate("""()=>{const a=document.activeElement;return {tag:a.tagName,id:a.id,role:a.getAttribute('role'),name:(a.getAttribute('aria-label')||a.textContent||'').trim().slice(0,50)}}""")


def focus_visible(page):
    return page.evaluate("""()=>{const a=document.activeElement;const s=getComputedStyle(a);const o=s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0;const sh=s.boxShadow!=='none';return o||sh}""")


def axe(page, sel=None):
    ctx = f"document.querySelector('{sel}')" if sel else "document"
    return page.evaluate(AXE + f""";(async()=>{{const r=await axe.run({ctx},{{runOnly:{{type:'tag',values:{TAGS}}}}});return {{version:axe.version,violations:r.violations.map(v=>({{id:v.id,impact:v.impact,nodes:v.nodes.length}})),passes:r.passes.length}}}})()""")


def no_hscroll(page):
    return page.evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth")


LONG_ANIM = "document.getAnimations().filter(a=>{const t=a.effect&&a.effect.getTiming();return t&&(t.duration>10||t.iterations===Infinity)&&a.playState==='running'}).length"
STRUCT = """()=>({tablist:[...document.querySelectorAll('[role=tablist]')].map(e=>e.getAttribute('aria-label')),
  tabs:[...document.querySelectorAll('[role=tab]')].map(e=>({n:e.textContent.trim().slice(0,30),sel:e.getAttribute('aria-selected'),ctl:!!e.getAttribute('aria-controls')})),
  panels:[...document.querySelectorAll('[role=tabpanel]')].map(e=>({label:e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')})),
  blockers:[...document.querySelectorAll('.case-blocker-summary')].map(e=>e.textContent.trim().slice(0,80)),
  blockerButtons:[...document.querySelectorAll('button')].filter(b=>/why blocked/i.test(b.getAttribute('aria-label')||b.textContent)).map(b=>(b.getAttribute('aria-label')||b.textContent).trim().slice(0,60))})"""

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    login(pg); pg.goto(APP + "/", wait_until="networkidle")
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(APP + "/app"), timeout=60000); pg.wait_for_timeout(4000)
    items = pg.evaluate("""async()=>{const r=await fetch('/api/cases');const j=await r.json();return j.items||j}""")
    cid = items[0]["id"]
    step("cases_available", count=len(items))
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(3000)
    step("case_structure", **pg.evaluate(STRUCT))
    step("axe_case_view_1366", **axe(pg))
    tabs = pg.get_by_role("tab")
    if tabs.count():
        tabs.first.focus()
        seq = [active(pg)["name"]]
        for _ in range(tabs.count()):
            pg.keyboard.press("ArrowRight"); seq.append(active(pg)["name"])
        pg.keyboard.press("End"); end = active(pg)["name"]
        pg.keyboard.press("Home"); home_ = active(pg)["name"]
        sel = pg.evaluate("document.querySelector('[role=tab][aria-selected=true]')?.textContent.trim()")
        step("tab_arrow_keys", sequence=seq, end=end, home=home_, selected_after=sel)
        pg.keyboard.press("Tab"); step("tab_moves_to_panel", focus=active(pg))
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    pg.evaluate("document.activeElement.blur()")
    walk, bad = [], []
    for _ in range(80):
        pg.keyboard.press("Tab"); a = active(pg); fv = focus_visible(pg)
        walk.append(a["id"] or a["name"] or a["tag"])
        if not fv:
            bad.append(a["id"] or a["name"] or a["tag"])
    step("tab_walk_focus_indicators", stops=len(walk), without_indicator=bad[:15], without_indicator_count=len(bad))
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    trig = pg.locator("button").filter(has_text=re.compile("why blocked", re.I))
    if trig.count():
        label = trig.first.inner_text().strip()[:40]
        trig.first.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(600)
        op = pg.locator(".case-blocker-popover:popover-open").count()
        pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
        step("blocker_keyboard", opened_by_enter=op, closed_by_escape=pg.locator(".case-blocker-popover:popover-open").count() == 0,
             focus_back_on_trigger=pg.evaluate("document.activeElement.textContent").strip()[:40] == label)
    else:
        step("blocker_keyboard", note="no blocker trigger on the first case")
    pg.screenshot(path=os.path.join(OUT, "case-view-1366.png"))
    for label, w, h in [("200pct_zoom_equiv_683x450", 683, 450), ("400pct_zoom_equiv_320x256", 320, 256)]:
        pg.set_viewport_size({"width": w, "height": h}); pg.wait_for_timeout(800)
        step("reflow_" + label, no_horizontal_scroll=no_hscroll(pg), tabs_visible=pg.get_by_role("tab").count())
        if w == 320:
            pg.screenshot(path=os.path.join(OUT, "case-view-320x256.png"))
    pg.set_viewport_size({"width": 1366, "height": 900})
    pg.emulate_media(reduced_motion="reduce"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000)
    step("reduced_motion_case_view", running_long_animations=pg.evaluate(LONG_ANIM))
    pg.emulate_media(reduced_motion="no-preference")
    pg.goto(f"{APP}/app#/case/{cid}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    pg.evaluate("document.activeElement.blur()")
    lau = pg.locator("#employee-chat-launcher")
    for _ in range(80):
        pg.keyboard.press("Tab")
        if active(pg)["id"] == "employee-chat-launcher":
            break
    step("chat_launcher_keyboard", focused=active(pg)["id"] == "employee-chat-launcher", name=lau.get_attribute("aria-label"), focus_indicator=focus_visible(pg))
    pg.keyboard.press("Space"); pg.wait_for_selector("#employee-chat:not([hidden])")
    pg.wait_for_function("()=>!document.querySelector('#employee-chat-question').disabled", timeout=30000)
    step("chat_space_opens", role=pg.locator("#employee-chat").get_attribute("role"), expanded=lau.get_attribute("aria-expanded"), focus=active(pg))
    step("chat_axe_open", **axe(pg, "#employee-chat"))
    stops, off = [], 0
    for _ in range(12):
        pg.keyboard.press("Tab"); a = active(pg); stops.append(a["id"] or a["name"] or a["tag"])
        inside = pg.evaluate("document.querySelector('#employee-chat').contains(document.activeElement)||document.activeElement.id==='employee-chat-launcher'")
        if not inside:
            off += 1
    step("chat_tab_cycle", sequence=stops, stops_outside_panel_or_launcher=off)
    for label, w, h in [("200pct_zoom_equiv_683x450", 683, 450), ("400pct_zoom_equiv_320x256", 320, 256)]:
        pg.set_viewport_size({"width": w, "height": h}); pg.wait_for_timeout(800)
        inv = pg.evaluate("""()=>{const q=document.querySelector('#employee-chat-question').getBoundingClientRect();const s=[...document.querySelectorAll('#employee-chat button')].find(b=>b.textContent.trim()==='Send').getBoundingClientRect();
          const ok=r=>r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight;return {input_in_view:ok(q),send_in_view:ok(s)}}""")
        step("chat_reflow_" + label, no_horizontal_scroll=no_hscroll(pg), **inv)
        if w == 320:
            pg.screenshot(path=os.path.join(OUT, "chat-open-320x256.png"))
    pg.set_viewport_size({"width": 1366, "height": 900})
    pg.emulate_media(reduced_motion="reduce"); pg.wait_for_timeout(500)
    step("reduced_motion_chat", running_long_animations=pg.evaluate(LONG_ANIM))
    pg.focus("#employee-chat-question"); pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    step("chat_escape", hidden=pg.locator("#employee-chat").is_hidden(), focus=active(pg))
    b.close()
json.dump(res, open(os.path.join(OUT, "employee_proof.json"), "w"), indent=1)
for s in res["steps"]:
    print(EMAIL.sub("[email]", json.dumps(s))[:600])
