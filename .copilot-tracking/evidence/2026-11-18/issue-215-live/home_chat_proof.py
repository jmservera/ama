"""Issue 215: employee home chat launcher (opened, not sent) and resident app chat presence. Redacted."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "employee_proof.py")).read().split("r = {}")[0])
AXE = open("/mnt/tmp/ama-run-81a96abb-1844-20261117T1358/axe/axe.min.js").read()
R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
res = [x.strip() for x in rd(".ama-resident-test-user") if x.strip()]
r = {}
TAGS = "{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}"
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if pg.locator("text=Pick an account").count(): pg.locator("[data-test-id], .table-row, div[role=button]").first.click()
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000)
    L = pg.locator("#employee-chat-launcher")
    r["launcher_visible"] = L.is_visible(); r["launcher_name"] = (L.get_attribute("aria-label") or L.inner_text())[:80]
    L.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
    dlg = pg.locator("[role=dialog]")
    r["dialog_count"] = dlg.count()
    if dlg.count():
        d = dlg.first
        r["dialog_text"] = d.inner_text()[:1800]
        r["dialog_labelled"] = bool(d.get_attribute("aria-label") or d.get_attribute("aria-labelledby"))
        r["focus_in_dialog"] = pg.evaluate("!!document.activeElement.closest('[role=dialog]')")
        pg.evaluate(AXE)
        a = pg.evaluate("()=>axe.run(document.querySelector('[role=dialog]')," + TAGS + ")")
        r["axe_chat_dialog"] = {"violations": [{"id": v["id"], "nodes": len(v["nodes"])} for v in a["violations"]], "incomplete": len(a["incomplete"]), "passes": len(a["passes"])}
        shot(pg, "homechat-1-open")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(800)
        r["closed_by_escape"] = pg.locator("[role=dialog]").count() == 0 or not pg.locator("[role=dialog]").first.is_visible()
        r["focus_back_on_launcher"] = pg.evaluate("document.activeElement.id")
    json.dump(r, open(f"{OUT}/home-chat-run1.json", "w"), indent=1)
    c2 = b.new_context(viewport={"width": 1366, "height": 900}); rp = c2.new_page()
    rp.goto(R + "/", timeout=120000); rp.click("#email"); rp.keyboard.type(res[0]); rp.keyboard.press("Tab"); rp.keyboard.type(res[1])
    with rp.expect_response("**/demo/login") as rr: rp.keyboard.press("Enter")
    r["resident_login_status"] = rr.value.status; rp.wait_for_timeout(4000)
    r["resident_chat_controls"] = [x.strip()[:60] for x in rp.locator("button,summary,[role=button]").all_inner_texts() if re.search("chat|ask|help|message", x, re.I)][:10]
    r["resident_has_regulatory_alert_ui"] = rp.locator("text=Regulatory alerts").count()
    shot(rp, "resident-1-home")
    b.close()
json.dump(r, open(f"{OUT}/home-chat-run1.json", "w"), indent=1); print(json.dumps(r, indent=1))
