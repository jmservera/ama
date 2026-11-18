"""Issue 215 run 3: live re-check of law-store state, home chat open (screenshots), axe incomplete detail. Redacted."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "..", "issue-215-live", "employee_proof.py")).read().split("r = {}")[0]
exec(src)
OUT = HERE
AXE = open(os.environ.get("AXE_JS", "axe.min.js")).read()
TAGS = "{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}"
r = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if pg.locator("text=Pick an account").count(): pg.locator("[data-test-id], .table-row, div[role=button]").first.click()
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000)
    me = pg.evaluate("fetch('/api/me').then(r=>r.json())")
    r["me_services"] = me.get("services"); r["me_role"] = me.get("role") or me.get("roles")
    al = pg.evaluate("fetch('/api/law/alerts?case=ZF-2025-0331').then(async r=>({s:r.status,b:await r.text()}))")
    r["alerts_status"] = al["s"]; r["alerts_body"] = al["b"][:400]
    pg.goto(APP + "/app#/case/ZF-2025-0331"); pg.wait_for_timeout(5000)
    pg.get_by_role("tab", name=re.compile("Blockers and safety")).first.click(); pg.wait_for_timeout(2500)
    r["alert_cards"] = pg.locator("#regulatory-alerts article, #regulatory-alerts li").count()
    r["alerts_text"] = pg.locator("#regulatory-alerts").inner_text()[:700]
    r["mode_state_text_present"] = pg.locator(".regulatory-mode-state").count()
    shot(pg, "r3-alerts-panel")
    L = pg.locator("#employee-chat-launcher")
    L.scroll_into_view_if_needed(); L.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
    d = pg.locator("[role=dialog]").first
    r["dialog_visible"] = d.is_visible()
    r["dialog_text"] = d.inner_text()[:900]
    a = pg.evaluate("()=>axe.run(document.querySelector('[role=dialog]')," + TAGS + ")") if pg.evaluate(AXE) is None or True else None
    r["axe_chat_dialog"] = {"violations": [{"id": v["id"], "nodes": len(v["nodes"])} for v in a["violations"]], "passes": len(a["passes"]),
        "incomplete": [{"id": v["id"], "impact": v["impact"], "nodes": [n["html"][:160] for n in v["nodes"]][:3], "why": v["nodes"][0]["any"][0]["message"][:200] if v["nodes"][0]["any"] else None} for v in a["incomplete"]]}
    shot(pg, "r3-home-chat-open")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(800)
    r["chat_closed_by_escape"] = pg.locator("[role=dialog]").count() == 0 or not pg.locator("[role=dialog]").first.is_visible()
    r["focus_back_on_launcher"] = pg.evaluate("document.activeElement.id")
    b.close()
json.dump(r, open(f"{OUT}/run3-results.json", "w"), indent=1); print(json.dumps(r, indent=1))
