"""Live probe of the regulatory alerts panel on the synthetic demo (issue 215).
Needs $STATE_DIR/state-staff.json from login.py and a trusted axe.min.js. Prints no credentials."""
import hashlib, json, os, sys
from playwright.sync_api import sync_playwright

H = os.environ["DEMO_API_URL"]
CASE = "ZF-2025-0122"
AXE = open(sys.argv[1]).read()
assert hashlib.sha256(AXE.encode()).hexdigest() == "880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb"
SHOTS = sys.argv[2]
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900}, storage_state=os.environ["STATE_DIR"] + "/state-staff.json")
    pg = c.new_page()
    pg.goto(f"{H}/app#/case/{CASE}")
    pg.wait_for_load_state("networkidle")
    pg.wait_for_selector("#regulatory-alerts", timeout=20000)
    pg.wait_for_timeout(3000)
    panel = pg.locator("#regulatory-alerts")
    out["status_text"] = panel.locator("[role=status]").first.inner_text()
    out["alert_count"] = panel.locator(".regulatory-alert-list > *").count()
    out["state_labels"] = panel.locator(".regulatory-state").evaluate_all(
        "ns => ns.map(n => ({text: n.textContent.trim(), cls: n.className}))")
    out["plain_toggle"] = panel.locator("input[type=checkbox]").count()
    out["panel_text_sample"] = panel.inner_text()[:600]
    # alert fields: noticed, source, status, safe action, owner, clock
    txt = panel.inner_text().lower()
    out["fields_present"] = {k: (k in txt) for k in ["source", "status", "owner", "action", "clock", "due", "doubt", "no source"]}
    panel.scroll_into_view_if_needed()
    panel.screenshot(path=f"{SHOTS}/01-alerts-panel.png")
    # keyboard
    pg.evaluate("() => document.querySelector('#regulatory-alerts').scrollIntoView()")
    pg.evaluate("() => { const f = document.querySelector('#regulatory-alerts').querySelector('summary, a[href], button, input, select, textarea'); if (f) f.focus(); }")
    path = []
    for _ in range(25):
        d = pg.evaluate("""() => { const e = document.activeElement; const p = document.querySelector('#regulatory-alerts');
          if (!e || !p.contains(e)) return null;
          const cs = getComputedStyle(e);
          return {tag: e.tagName, label: (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 40),
                  outline: cs.outlineStyle + ' ' + cs.outlineWidth, shadow: cs.boxShadow !== 'none'}; }""")
        if d is None:
            break
        path.append(d)
        pg.keyboard.press("Tab")
    out["keyboard_tab_path"] = path
    # keyboard-only plain-language toggle
    cb = panel.locator("input[type=checkbox]").first
    if cb.count():
        cb.focus()
        out["plain_before"] = {"checked": cb.is_checked(), "root_class": panel.get_attribute("class")}
        pg.keyboard.press("Space")
        pg.wait_for_timeout(300)
        out["plain_after_space"] = {"checked": cb.is_checked(), "root_class": panel.get_attribute("class"),
                                    "announce": pg.evaluate("() => document.querySelector('#regulatory-alerts .regulatory-mode-state')?.textContent ?? ('MISSING; ids=' + [...document.querySelectorAll('#alerts-plain-mode')].length)")}
        panel.screenshot(path=f"{SHOTS}/02-plain-off.png")
        pg.keyboard.press("Space")
        pg.wait_for_timeout(300)
        out["plain_restored"] = {"checked": cb.is_checked(), "announce": pg.evaluate("() => document.querySelector('#regulatory-alerts .regulatory-mode-state')?.textContent ?? ('MISSING; ids=' + [...document.querySelectorAll('#alerts-plain-mode')].length)")}
    # axe on the panel
    pg.evaluate(AXE)
    res = pg.evaluate("""async () => { const r = await axe.run('#regulatory-alerts', {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});
      return {violations: r.violations.map(v => ({id: v.id, impact: v.impact, nodes: v.nodes.length})),
              incomplete: r.incomplete.map(v => ({id: v.id, nodes: v.nodes.length})), passes: r.passes.length}; }""")
    out["axe"] = res
    # target sizes
    out["small_targets"] = pg.locator("#regulatory-alerts").locator("summary:visible, a[href]:visible, button:visible, input:visible, select:visible").evaluate_all(
        "ns => ns.map(n => { const r = n.getBoundingClientRect(); return {w: Math.round(r.width), h: Math.round(r.height)}; }).filter(s => s.w < 24 || s.h < 24)")
    # colour-only check: every state label has text; strip colour and compare
    out["text_without_colour"] = pg.evaluate("""() => { const p = document.querySelector('#regulatory-alerts');
      const s = document.createElement('style'); s.textContent = '*{color:#000!important;background:#fff!important;border-color:#000!important}'; document.head.appendChild(s);
      const labels = [...p.querySelectorAll('.regulatory-state')].map(n => n.textContent.trim()); s.remove(); return labels; }""")
    # home chat: cited regulatory lookup, keyboard only
    pg.locator("#case-tab-ai").focus()
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(1000)
    out["ai_tab_selected"] = pg.get_attribute("#case-tab-ai", "aria-selected")
    out["chat_panel_html_head"] = pg.evaluate("() => document.querySelector('#chat-panel')?.innerText.slice(0, 300)")
    pg.locator("#chat-panel > summary").focus()
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(800)
    out["outer_chat_open"] = pg.evaluate("() => document.querySelector('#chat-panel').open")
    chat = pg.locator("#regulatory-chat")
    out["chat_panel"] = chat.count()
    if chat.count():
        chat.locator("summary").first.focus()
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(800)
        out["chat_open_after_enter"] = pg.evaluate("() => document.querySelector('#regulatory-chat').open")
        out["chat_text_sample"] = chat.inner_text()[:700]
        out["chat_controls"] = chat.locator("input:visible, button:visible, textarea:visible, select:visible").evaluate_all(
            "ns => ns.map(n => ({tag: n.tagName, type: n.type, disabled: n.disabled, label: (n.labels && n.labels[0] ? n.labels[0].textContent : n.getAttribute('aria-label') || n.textContent || '').trim().slice(0, 50)}))")
        try:
            chat.screenshot(path=f"{SHOTS}/03-chat-open.png", timeout=8000)
        except Exception as e:
            out["chat_screenshot_error"] = str(e).splitlines()[0]
            out["chat_box"] = chat.bounding_box()
            out["chat_visible"] = chat.is_visible()
        res2 = pg.evaluate("""async () => { const r = await axe.run('#regulatory-chat', {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});
          return {violations: r.violations.map(v => ({id: v.id, impact: v.impact, nodes: v.nodes.length})), incomplete: r.incomplete.map(v => ({id: v.id, nodes: v.nodes.length})), passes: r.passes.length}; }""")
        out["chat_axe"] = res2
        pg.evaluate("() => document.querySelector('#regulatory-chat').querySelector('input, textarea, button')?.focus()")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)
        out["chat_after_escape"] = pg.evaluate("() => ({open: document.querySelector('#regulatory-chat').open, focus: document.activeElement.tagName})")
    print(json.dumps(out, indent=1))
    c.close(); b.close()
