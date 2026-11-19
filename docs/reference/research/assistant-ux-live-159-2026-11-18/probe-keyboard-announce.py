"""Keyboard-only and live-region probe of the employee assistant on the live demo.
Needs <tmp>/state-staff.json from login.py. Prints no credentials or personal names."""
import json, re, sys
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
CASE = "ZF-2025-0122"
OBS = """() => { window.__log = []; const log = document.querySelector('#employee-chat [role=log]');
  new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => window.__log.push({t: Date.now(), tag: n.nodeName, txt: (n.textContent||'').slice(0,60)})))).observe(log, {childList: true, subtree: true});
  const st = document.querySelector('#employee-chat [role=status]');
  window.__st = []; new MutationObserver(() => window.__st.push(st.textContent.slice(0,120))).observe(st, {childList: true, characterData: true, subtree: true}); }"""
out = {}
def desc(pg):
    return pg.evaluate("() => { const e = document.activeElement; return e ? (e.tagName + '|' + (e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,40) + '|' + (e.id||'')) : null }")
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}, storage_state="<tmp>/state-staff.json"); pg = c.new_page()
    pg.goto(f"{H}/app#/case/{CASE}"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2500)
    out["launcher_present"] = pg.locator("#employee-chat-launcher:not([hidden])").count()
    pg.keyboard.press("Tab")
    path = []
    for i in range(120):
        d = desc(pg); path.append(d)
        if d and d.endswith("|employee-chat-launcher"): out["tabs_to_launcher"] = i + 1; break
        pg.keyboard.press("Tab")
    out["tab_path_tail"] = path[-4:]
    pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
    out["dialog_open"] = pg.evaluate("() => !document.getElementById('employee-chat').hidden")
    out["focus_after_open"] = desc(pg)
    out["launcher_expanded"] = pg.get_attribute("#employee-chat-launcher", "aria-expanded")
    out["log_attrs"] = pg.evaluate("() => { const l = document.querySelector('#employee-chat [role=log]'); return {role: l.getAttribute('role'), live: l.getAttribute('aria-live'), relevant: l.getAttribute('aria-relevant'), label: l.getAttribute('aria-label'), tabindex: l.getAttribute('tabindex')} }")
    out["dialog_attrs"] = pg.evaluate("() => { const d = document.getElementById('employee-chat'); return {role: d.getAttribute('role'), labelledby: d.getAttribute('aria-labelledby'), title: document.getElementById(d.getAttribute('aria-labelledby')).textContent} }")
    pg.wait_for_function("() => !document.querySelector('#employee-chat textarea').disabled", timeout=30000)
    pg.evaluate(OBS)
    # keyboard-only walk through the panel controls
    order = []
    for _ in range(14):
        pg.keyboard.press("Tab"); order.append(desc(pg))
        if "employee-chat" not in (pg.evaluate("() => document.activeElement.closest('#employee-chat') ? 'employee-chat' : ''") or ""): break
    out["panel_tab_order"] = order
    pg.focus("#employee-chat textarea")
    turns = []
    for q in ["What is the status of this case and what should I do next?", "Which of those sources support that?"]:
        pg.keyboard.type(q); pg.keyboard.press("Enter")
        pg.wait_for_function("() => !document.querySelector('#employee-chat form').hasAttribute('aria-busy') || document.querySelector('#employee-chat form').getAttribute('aria-busy')==='false'", timeout=90000)
        pg.wait_for_timeout(1500)
        n = pg.locator("#employee-chat article.chat-widget-assistant").count()
        last = pg.locator("#employee-chat article.chat-widget-assistant").last
        turns.append({"assistant_messages": n, "label_present": "AI suggestion, not approved" in last.inner_text(), "focus": desc(pg), "text_head": re.sub(r"\s+", " ", last.inner_text())[:200]})
    out["turns"] = turns
    out["log_additions"] = pg.evaluate("() => window.__log.map(x => x.tag + ':' + x.txt)")
    out["status_changes"] = pg.evaluate("() => window.__st")
    out["error_role"] = pg.evaluate("() => document.querySelector('#employee-chat [role=alert]') ? 'role=alert present, hidden=' + document.querySelector('#employee-chat [role=alert]').hidden : null")
    pg.locator("#employee-chat .chat-widget-log").screenshot(path="shots/panel-log-cropped.png") if False else None
    pg.locator("#employee-chat").screenshot(path="shots/employee-panel-keyboard.png")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    out["after_escape"] = {"hidden": pg.evaluate("() => document.getElementById('employee-chat').hidden"), "focus": desc(pg)}
    print(json.dumps(out, indent=1))
