"""Issue 215 live proof: regulatory alerts panel and regulatory chat on the demo workbench."""
import json, os, urllib.request, hashlib
from playwright.sync_api import sync_playwright
from common import *

AXE = os.path.join(OUT, "axe.min.js")
if not os.path.exists(AXE):
    urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js", AXE)
open(os.path.join(OUT, "axe-4.10.3.sha256"), "w").write(hashlib.sha256(open(AXE, "rb").read()).hexdigest() + "\n")
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
res = {}

def axe(pg, sel):
    if not pg.evaluate("typeof axe!=='undefined'"):
        pg.add_init_script(path=AXE) if False else pg.evaluate(open(AXE).read())
    r = pg.evaluate("([s,t])=>axe.run(document.querySelector(s),{runOnly:{type:'tag',values:t}})", [sel, TAGS])
    return {"violations": [{"id": v["id"], "n": len(v["nodes"])} for v in r["violations"]],
            "incomplete": [{"id": v["id"], "n": len(v["nodes"])} for v in r["incomplete"]]}

def shot(pg, sel, name):
    pg.locator(sel).first.scroll_into_view_if_needed()
    pg.locator(sel).first.screenshot(path=os.path.join(OUT, name))

MOCK = {"coverage_status": "partial", "homes": [{"alerts": [
  {"result": "breach risk", "noticed": "Synthetic: hazard report recorded without an acknowledgement time", "safe_action": "Use the human hazard service now and record the awareness time", "decision_owner": "Building Safety Liaison", "escalation_role": "Retrofit Programme Manager", "clock": "Synthetic exercise clock: 24 hours from awareness", "due_at": "2026-11-19T10:00:00Z", "at": "2026-11-18T10:00:00Z", "step": "intake", "card_id": "demo-card", "card_version": "1", "exercise": True, "active_control": True, "latest_result": "breach risk", "latest_evaluated_at": "2026-11-18T10:00:00Z", "usage": True, "requires_acknowledgement": True, "requires_outcome": True,
   "citations": [{"id": "demo-prov-1", "status": "in force", "effective": "2025-10-27", "retrieved": "2026-11-01", "review_status": "demo", "completeness": "excerpt"}]},
  {"result": "unknown", "noticed": "Synthetic: no evidence held", "safe_action": None, "decision_owner": None, "clock": None, "card_id": "demo-card", "card_version": "1", "citations": []},
  {"result": "clear", "noticed": "Synthetic: bounded check clear", "safe_action": "No action beyond ordinary case work", "decision_owner": "Retrofit Coordinator", "escalation_role": "Retrofit Programme Manager", "clock": "None", "card_id": "demo-card", "card_version": "1", "citations": []}]}]}

def tab_walk(pg, root, n=40):
    stops = []
    for _ in range(n):
        pg.keyboard.press("Tab")
        i = pg.evaluate("""r=>{const e=document.activeElement;const root=document.querySelector(r);if(!e||!root.contains(e))return null;
          const cs=getComputedStyle(e);return {tag:e.tagName,name:(e.getAttribute('aria-label')||e.textContent||e.id||'').trim().slice(0,50),
          ring:(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||cs.boxShadow!=='none'}}""", root)
        if i: stops.append(i)
    return stops

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900}); login(pg)
    cases = pg.evaluate("fetch('/api/cases').then(r=>r.json())")
    lst = next(v for v in cases.values() if isinstance(v, list))
    cid = lst[0].get("id") or lst[0].get("case_id")
    res["cases_listed"] = len(lst)

    # A. Live alert panel (law store not loaded on the demo)
    pg.goto(APP+"/app",wait_until="networkidle"); pg.wait_for_timeout(3000); pg.evaluate(f"location.hash='#/case/{cid}'"); pg.wait_for_selector("#regulatory-alerts", timeout=60000); pg.wait_for_timeout(3000)
    mask_emails(pg)
    res["live_alert_status"] = pg.inner_text("#regulatory-alerts [role=status]")
    res["live_alert_notice"] = pg.inner_text("#regulatory-alerts .notice")
    res["live_alert_headings"] = pg.eval_on_selector_all("#regulatory-alerts h2,#regulatory-alerts h3,#regulatory-alerts h4", "e=>e.map(x=>x.textContent)")
    res["live_alerts_api"] = pg.evaluate(f"fetch('/api/law/alerts?case={cid}').then(async r=>[r.status,(await r.text()).slice(0,200)])")
    res["live_alert_axe"] = axe(pg, "#regulatory-alerts"); shot(pg, "#regulatory-alerts", "live-alert-panel-coverage-unknown.png")

    # B. Keyboard: plain-language toggle and refresh
    pg.focus("#alerts-plain-mode")
    before = pg.evaluate("document.querySelector('#regulatory-alerts').classList.contains('plain-language')")
    pg.keyboard.press("Space")
    after = pg.evaluate("document.querySelector('#regulatory-alerts').classList.contains('plain-language')")
    res["plain_toggle_keyboard"] = {"before": before, "after": after, "announcement": pg.evaluate("(document.querySelector('#regulatory-alerts .regulatory-mode-state')||{}).textContent||null"),
        "plain_explanations_hidden_display": pg.evaluate("[...document.querySelectorAll('#regulatory-alerts .plain-explanation')].map(e=>getComputedStyle(e).display)")}
    pg.keyboard.press("Space")
    pg.keyboard.press("Tab"); pg.keyboard.press("Enter")
    res["refresh_by_keyboard_status"] = pg.inner_text("#regulatory-alerts [role=status]"); res["focus_after_refresh"]=pg.evaluate("document.activeElement.textContent")
    pg.focus("#regulatory-alerts h2"); res["alert_tab_walk"] = tab_walk(pg, "#regulatory-alerts", 12)

    # C. Populated alert rendering with the deployed JS against a MOCKED /api/law/alerts response
    pg.route("**/api/law/alerts*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK)))
    pg.evaluate("document.querySelector('#regulatory-alerts button.alt').click()"); pg.wait_for_timeout(1500)
    res["mock_alert_dt_per_alert"] = pg.eval_on_selector_all("#regulatory-alerts article", "a=>a.map(x=>[...x.querySelectorAll('dt')].map(d=>d.textContent))")
    res["mock_alert_headings"] = pg.eval_on_selector_all("#regulatory-alerts article h3", "e=>e.map(x=>x.textContent)")
    res["mock_alert_summaries"] = pg.eval_on_selector_all("#regulatory-alerts .regulatory-plain-summary", "e=>e.map(x=>x.textContent)")
    res["mock_no_source_text"] = pg.eval_on_selector_all("#regulatory-alerts .state-no-source", "e=>e.map(x=>x.textContent)")
    res["mock_status_line"] = pg.inner_text("#regulatory-alerts [role=status]")
    res["mock_status_marker_non_colour"] = pg.eval_on_selector_all("#regulatory-alerts article h3", "e=>e.map(x=>{const s=getComputedStyle(x,'::before');return {text:x.textContent,before:s.content}})")
    res["mock_alert_axe"] = axe(pg, "#regulatory-alerts"); shot(pg, "#regulatory-alerts", "mocked-alert-states.png")
    pg.unroute("**/api/law/alerts*")

    # D. Regulatory chat panel
    pg.goto(APP+"/app",wait_until="networkidle"); pg.wait_for_timeout(3000); pg.evaluate(f"location.hash='#/case/{cid}'"); pg.wait_for_selector("[aria-controls=case-panel-ai]", timeout=60000); pg.click("[aria-controls=case-panel-ai]"); res["chat_tab_label"]=pg.inner_text("[aria-controls=case-panel-ai]"); pg.wait_for_selector("#chat-panel", timeout=20000); pg.wait_for_timeout(2500)
    pg.evaluate("document.querySelector('#chat-panel').open=true")
    pg.focus("#regulatory-chat > summary"); pg.keyboard.press("Enter")
    res["chat_open_by_keyboard"] = pg.evaluate("document.querySelector('#regulatory-chat').open")
    pg.wait_for_timeout(3000)
    res["chat_status"] = pg.inner_text("#regulatory-chat [role=status]")
    res["chat_privacy"] = pg.inner_text("#regulatory-privacy")
    res["chat_guidance_doubt_route"] = pg.inner_text("#regulatory-chat .regulatory-guidance")
    res["chat_question_disabled"] = pg.evaluate("document.querySelector('#regulatory-question').disabled")
    if not res["chat_question_disabled"]:
        pg.fill("#regulatory-question", "Which source covers damp and mould hazards?")
        pg.keyboard.press("Tab"); pg.keyboard.press("Enter"); pg.wait_for_timeout(6000)
        res["chat_turn_text"] = pg.inner_text("#regulatory-chat ol")[:1800]
        res["chat_after_status"] = pg.inner_text("#regulatory-chat [role=status]")
        pg.fill("#regulatory-question", "What is the licensed PAS 2035 clause on ventilation and who funds it?")
        pg.keyboard.press("Tab"); pg.keyboard.press("Enter"); pg.wait_for_timeout(6000)
        res["chat_turn2_text"] = pg.inner_text("#regulatory-chat ol")[-1800:]
    res["chat_axe"] = axe(pg, "#regulatory-chat"); shot(pg, "#regulatory-chat", "live-regulatory-chat.png")
    pg.focus("#regulatory-question") if not res["chat_question_disabled"] else None
    pg.keyboard.press("Escape")
    res["chat_escape_closes_returns_focus"] = pg.evaluate("[!document.querySelector('#regulatory-chat').open, document.activeElement.tagName]")
    pg.evaluate("document.querySelector('#regulatory-chat').open=true")
    res["chat_tab_walk"] = tab_walk(pg, "#regulatory-chat", 20)
    b.close()
json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:6000])
