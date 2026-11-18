"""Issue 215: deployed client JS against MOCKED /api/me, /api/law/alerts and /api/chat/regulatory/* responses.
Proves client rendering, keyboard and axe behaviour of populated states only; server data is synthetic and local to this script."""
import json, os
from playwright.sync_api import sync_playwright
from common import *
import prove_lib as L

me_patch = lambda m: (m["services"].update(law_alerts=True), m["user"].update(rule_roles=list(set((m["user"].get("rule_roles") or []) + ["regulatory_chat"]))), m)[2]
ANS_OK = {"schema": "regulatory-chat-v1", "kind": "answer", "turn": 2, "label": "synthetic-demo: not legal advice or approval", "plain_summary": "Sources were found. A person decides what applies.",
  "usage": True, "sections": {"what_sources_say": [{"citation": "demo-prov-1", "quote": "Synthetic excerpt about hazard awareness"}], "recorded_home_facts": [{"id": "F1", "text": "Synthetic recorded fact"}],
  "unknown_or_missing": ["Contract incorporation not held"], "safe_next_action": "Ask the named owner", "who_decides": "Building Safety Liaison"},
  "citations": [{"id": "demo-prov-1", "status": "in force", "effective": "2025-10-27", "retrieved": "2026-11-01"}], "cards": []}
ANS_NONE = {"schema": "regulatory-chat-v1", "kind": "refused", "turn": 4, "label": "synthetic-demo: not legal advice or approval", "reply": "No source held for this question.", "citations": [], "usage": True}
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900}); login(pg)
    def me(route):
        r = route.fetch(); m = r.json(); route.fulfill(response=r, json=me_patch(m))
    jf = lambda body, status=200: (lambda r: r.fulfill(status=status, content_type="application/json", body=json.dumps(body)))
    pg.route("**/api/me", me)
    pg.route("**/api/law/alerts*", jf(L.MOCK))
    pg.route("**/api/chat/regulatory/status", jf({"warning": "Synthetic data only.", "privacy": {"chat": {"status": "simulated", "days": 30}}, "usage": {"period": "2026-11-18", "role": "Retrofit Programme Manager", "recorded_turns": 0, "outcomes": {"answer": 0, "refused": 0, "conflict": 0}, "coverage": "audit"}}))
    pg.route("**/api/chat/regulatory/usage", jf({"period": "2026-11-18", "role": "Retrofit Programme Manager", "recorded_turns": 2, "outcomes": {"answer": 1, "refused": 1, "conflict": 0}, "coverage": "audit"}))
    pg.route("**/api/chat/threads", jf([]))
    pg.route("**/api/chat/regulatory/threads", jf({"id": "T-demo"}))
    answers = iter([ANS_OK, ANS_NONE])
    pg.route("**/api/chat/regulatory/threads/T-demo/ask", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(next(answers))))
    pg.route("**/api/chat/regulatory/threads/T-demo/doubt", jf({"label": "synthetic-demo", "owner": "Juan Manuel Servera"}))
    pg.goto(APP + "/app", wait_until="networkidle"); pg.wait_for_timeout(3000)
    pg.evaluate("location.hash='#/case/ZF-2025-0331'"); pg.wait_for_selector("#regulatory-alerts", timeout=60000); pg.wait_for_timeout(2500)
    mask_emails(pg)
    R = "#regulatory-alerts"
    res["dt_per_alert"] = pg.eval_on_selector_all(R + " article", "a=>a.map(x=>[...x.querySelectorAll('dt')].map(d=>d.textContent))")
    res["alert_headings"] = pg.eval_on_selector_all(R + " article h3", "e=>e.map(x=>x.textContent)")
    res["plain_summaries"] = pg.eval_on_selector_all(R + " .regulatory-plain-summary", "e=>e.map(x=>x.textContent)")
    res["no_source_items"] = pg.eval_on_selector_all(R + " .state-no-source", "e=>e.map(x=>x.textContent)")
    res["alert_status_line"] = pg.inner_text(R + " [role=status]")
    res["alert_first_dd"] = pg.eval_on_selector_all(R + " article:first-of-type dd", "e=>e.map(x=>x.textContent)")
    res["alert_axe_plain_on"] = L.axe(pg, R); L.shot(pg, R, "mocked-alerts-populated.png")
    pg.focus("#alerts-plain-mode"); res["alert_tab_walk"] = L.tab_walk(pg, R, 12)
    pg.focus("#alerts-plain-mode"); pg.keyboard.press("Space")
    res["plain_off_class"] = pg.evaluate("document.querySelector('#regulatory-alerts').className")
    res["plain_off_display"] = pg.evaluate("[...document.querySelectorAll('#regulatory-alerts .plain-explanation')].map(e=>getComputedStyle(e).display)")
    res["alert_axe_plain_off"] = L.axe(pg, R)
    # contrast of each state heading: text colour vs background
    res["state_colours"] = pg.evaluate("[...document.querySelectorAll('#regulatory-alerts article h3')].map(e=>{const c=getComputedStyle(e);return [e.textContent,c.color,c.backgroundColor,c.borderLeftWidth+' '+c.borderLeftStyle]})")
    pg.keyboard.press("Space")
    pg.click("[aria-controls=case-panel-ai]"); pg.wait_for_selector("#chat-panel"); pg.evaluate("document.querySelector('#chat-panel').open=true")
    pg.focus("#regulatory-chat > summary"); pg.keyboard.press("Enter"); pg.wait_for_timeout(2500)
    C = "#regulatory-chat"
    res["chat_status"] = pg.inner_text(C + " [role=status]")
    for q in ["Which source covers hazard awareness?", "What does the contract say about funding?"]:
        pg.fill("#regulatory-question", q); pg.keyboard.press("Tab"); pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    res["chat_turns"] = pg.inner_text(C + " ol")
    res["chat_turn_headings"] = pg.eval_on_selector_all(C + " ol h3", "e=>e.map(x=>x.textContent)")
    res["chat_doubt_buttons"] = pg.eval_on_selector_all(C + " ol button", "e=>e.map(x=>x.textContent)")
    pg.locator(C + " ol button").first.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    res["chat_doubt_after"] = [pg.inner_text(C + " [role=status]"), pg.eval_on_selector_all(C + " ol button", "e=>e.map(x=>x.textContent+'|'+x.getAttribute('aria-disabled'))")]
    res["chat_axe"] = L.axe(pg, C); L.shot(pg, C, "mocked-chat-populated.png")
    b.close()
json.dump(res, open(os.path.join(OUT, "results-mocked.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:7000])
