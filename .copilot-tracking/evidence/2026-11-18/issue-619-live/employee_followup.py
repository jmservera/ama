"""Follow-up live probes (issue 619): blocker disclosure on a case that has one, hz-aware focus indicator,
and chat geometry at the 400 percent zoom-equivalent viewport. Credentials read at runtime, never printed."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
import employee_proof_lib as L

res = {"steps": []}
step = lambda n, **kw: res["steps"].append({"step": n, **kw})

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    L.login(pg); pg.goto(L.APP + "/", wait_until="networkidle")
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(L.APP + "/app"), timeout=60000); pg.wait_for_timeout(4000)
    items = pg.evaluate("""async()=>{const r=await fetch('/api/cases');const j=await r.json();return j.items||j}""")
    found = None
    items = items[:0] + items
    for it in []:
        pg.goto(f"{L.APP}/app#/case/{it['id']}", wait_until="networkidle"); pg.wait_for_timeout(1500)
        t = pg.locator("button").filter(has_text=re.compile("why blocked", re.I))
        if t.count():
            found = it["id"]; break
    pg.goto(f"{L.APP}/app#/case/{items[0]['id']}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    found = pg.locator(".case-blocker-summary").count() > 0
    step("case_with_blocker_found", found=found, summary_count=pg.locator(".case-blocker-summary").count())
    if found:
        trig = pg.locator(".case-blocker-trigger").first
        label = trig.get_attribute('aria-label')[:70]
        step("blocker_summary_text", summary=[e.strip()[:100] for e in pg.locator(".case-blocker-summary").all_inner_texts()][:3], trigger_aria_label=label)
        trig.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(600)
        opened = pg.locator(".case-blocker-popover:popover-open").count()
        pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
        step("blocker_enter_escape", opened=opened, closed=pg.locator(".case-blocker-popover:popover-open").count() == 0,
             focus_on_trigger=pg.evaluate("document.activeElement.getAttribute('aria-label')||''")[:70] == label)
        trig.focus(); pg.keyboard.press("Space"); pg.wait_for_timeout(600)
        step("blocker_space_opens", opened=pg.locator(".case-blocker-popover:popover-open").count())
        pg.keyboard.press("Escape")
        pg.screenshot(path=os.path.join(L.OUT, "case-view-blocker-1366.png"))
        step("axe_blocker_case", **L.axe(pg))
        # hz-aware focus indicator
    hz = pg.locator("#hz-aware")
    if hz.count():
        hz.focus()
        step("hz_aware_focus", tag=hz.evaluate("e=>e.tagName+':'+(e.type||'')"), visible=hz.is_visible(),
             style=pg.evaluate("(()=>{const s=getComputedStyle(document.activeElement);return {outline:s.outlineStyle+' '+s.outlineWidth,shadow:s.boxShadow.slice(0,60),appearance:s.appearance}})()"),
             focus_visible_matches=pg.evaluate("document.activeElement.matches(':focus-visible')"))
    # chat geometry at 320x256
    pg.goto(f"{L.APP}/app#/case/{items[0]['id']}", wait_until="networkidle"); pg.wait_for_timeout(2000)
    pg.set_viewport_size({"width": 320, "height": 256}); pg.wait_for_timeout(500)
    pg.locator("#employee-chat-launcher").click(); pg.wait_for_selector("#employee-chat:not([hidden])")
    pg.wait_for_function("()=>!document.querySelector('#employee-chat-question').disabled", timeout=30000); pg.wait_for_timeout(800)
    geo = pg.evaluate("""()=>{const r=e=>{const x=e.getBoundingClientRect();return [Math.round(x.left),Math.round(x.top),Math.round(x.right),Math.round(x.bottom)]};
      const root=document.querySelector('#employee-chat');const send=[...root.querySelectorAll('button')].find(b=>b.textContent.trim()==='Send');
      return {viewport:[innerWidth,innerHeight],panel:r(root),panelScroll:[root.scrollHeight,root.clientHeight,getComputedStyle(root).overflowY],input:r(document.querySelector('#employee-chat-question')),send:r(send)}}""")
    step("chat_geometry_320x256_open", **geo)
    q = pg.locator("#employee-chat-question"); q.focus(); pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
    step("chat_320_focus_send_reachable", focus=L.active(pg), scrolled_into_view=pg.evaluate("""()=>{const x=document.activeElement.getBoundingClientRect();return x.top>=0&&x.bottom<=innerHeight&&x.left>=0&&x.right<=innerWidth}"""))
    pg.screenshot(path=os.path.join(L.OUT, "chat-open-320x256-followup.png"))
    pg.set_viewport_size({"width": 320, "height": 450}); pg.wait_for_timeout(500)
    step("chat_320x450_input_send_in_view", **pg.evaluate("""()=>{const ok=r=>r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight;const s=[...document.querySelectorAll('#employee-chat button')].find(b=>b.textContent.trim()==='Send');return {input:ok(document.querySelector('#employee-chat-question').getBoundingClientRect()),send:ok(s.getBoundingClientRect())}}"""))
    b.close()
json.dump(res, open(os.path.join(L.OUT, "employee_followup.json"), "w"), indent=1)
for s in res["steps"]:
    print(L.EMAIL.sub("[email]", json.dumps(s))[:500])
