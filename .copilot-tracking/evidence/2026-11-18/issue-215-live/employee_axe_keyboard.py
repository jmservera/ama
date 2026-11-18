"""Issue 215: axe scan and Tab-only keyboard walk of the alerts and chat panels. Redacted output."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "employee_proof.py")).read().split("r = {}")[0])
AXE = open("/mnt/tmp/ama-run-81a96abb-1844-20261117T1358/axe/axe.min.js").read()
r = {}
def axe(pg, sel, tag):
    pg.evaluate(AXE)
    res = pg.evaluate("s=>axe.run(document.querySelector(s),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})", sel)
    r[tag] = {"violations": [{"id": v["id"], "impact": v["impact"], "nodes": len(v["nodes"])} for v in res["violations"]],
              "incomplete": [{"id": v["id"], "nodes": len(v["nodes"])} for v in res["incomplete"]], "passes": len(res["passes"])}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if pg.locator("text=Pick an account").count(): pg.locator("[data-test-id], .table-row, div[role=button]").first.click()
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000)
    pg.goto(APP + "/app#/case/ZF-2025-0331"); pg.wait_for_timeout(5000)
    pg.get_by_role("tab", name=re.compile("Blockers and safety")).first.click(); pg.wait_for_timeout(2500)
    axe(pg, "#regulatory-alerts", "axe_alerts_panel")
    # Tab-only walk from the alerts heading
    pg.evaluate("document.querySelector('#regulatory-alerts-title').tabIndex=-1;document.querySelector('#regulatory-alerts-title').focus()")
    seen = []
    for _ in range(12):
        pg.keyboard.press("Tab")
        seen.append(pg.evaluate("(()=>{const e=document.activeElement;return (e.id||e.tagName)+':'+((e.textContent||'').trim().slice(0,30))+':in_alerts='+!!e.closest('#regulatory-alerts')+':in_chat='+!!e.closest('#regulatory-chat')})()"))
        if "in_chat=true" in seen[-1] and len([s for s in seen if "in_chat=true" in s]) > 2: break
    r["tab_walk"] = seen
    r["focus_visible_outline"] = pg.evaluate("(()=>{const e=document.activeElement;const s=getComputedStyle(e);return {outlineStyle:s.outlineStyle,outlineWidth:s.outlineWidth,boxShadow:s.boxShadow.slice(0,60)}})()")
    # chat: open with Enter on summary via Tab focus
    pg.get_by_role("tab", name=re.compile("AI assistance")).first.click(); pg.wait_for_timeout(2500)
    chat = pg.locator("#regulatory-chat"); chat.scroll_into_view_if_needed()
    chat.locator("summary").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(1000)
    r["chat_open_after_enter"] = chat.evaluate("e=>e.open")
    if not r["chat_open_after_enter"]:
        pg.keyboard.press("Space"); pg.wait_for_timeout(1000); r["chat_open_after_space"] = chat.evaluate("e=>e.open")
    shot(pg, "chat-3-open-keyboard")
    axe(pg, "#regulatory-chat", "axe_chat_panel_open")
    r["chat_textarea_disabled"] = chat.locator("#regulatory-question").is_disabled()
    r["chat_status_texts"] = [t[:200] for t in chat.locator("[role=status],[aria-live]").all_text_contents()]
    r["doubt_route_text_present"] = "In doubt:" in chat.inner_text() and "Open my exercise doubt" in chat.inner_text()
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    r["chat_closed_by_escape"] = not chat.evaluate("e=>e.open")
    r["summary_focused_after_escape"] = pg.evaluate("document.activeElement.tagName")
    # 200% zoom reflow proxy at 1366x900 desktop: 683 css px width
    pg.set_viewport_size({"width": 683, "height": 900}); pg.wait_for_timeout(1000)
    r["reflow_scroll_overflow_x_at_683"] = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
    pg.get_by_role("tab", name=re.compile("Blockers and safety")).first.click(); pg.wait_for_timeout(2000)
    pg.locator("#regulatory-alerts").scroll_into_view_if_needed(); shot(pg, "alerts-3-zoom200")
    b.close()
json.dump(r, open(f"{OUT}/employee-axe-keyboard.json", "w"), indent=1); print(json.dumps(r, indent=1))
