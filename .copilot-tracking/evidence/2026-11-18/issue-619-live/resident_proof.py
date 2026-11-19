"""Live resident chat consent journey and keyboard proof (issue 619), synthetic resident test account only.
Credentials read at runtime, never printed. Output is redacted."""
import json, os, re
from playwright.sync_api import sync_playwright

R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
U, PW = rd(".ama-resident-test-user")[:2]
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
res = {"steps": []}
step = lambda n, **kw: res["steps"].append({"step": n, **kw})
posts = []


def active(pg):
    return pg.evaluate("""()=>{const a=document.activeElement;return {tag:a.tagName,id:a.id,name:(a.getAttribute('aria-label')||a.textContent||'').trim().slice(0,60)}}""")


def txt(pg, sel):
    return EMAIL.sub("[email]", pg.locator(sel).inner_text()).strip()


with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.on("request", lambda r: posts.append(r.url.split("?")[0].replace(R, "")) if r.method == "POST" else None)
    pg.goto(R + "/", wait_until="domcontentloaded", timeout=120000)
    pg.click("#email"); pg.keyboard.type(U); pg.keyboard.press("Tab"); pg.keyboard.type(PW)
    pg.keyboard.press("Enter")
    pg.wait_for_selector("#signin", state="hidden", timeout=90000); pg.wait_for_function("()=>document.querySelector('#status').textContent.includes('signed in')", timeout=60000); pg.wait_for_timeout(3000)
    step("signed_in", session=c.request.get(R + "/demo/session").json().get("signed_in"))
    posts.clear()
    lau = pg.locator("#chat-launcher")
    pg.evaluate("document.activeElement.blur()")
    for _ in range(80):
        pg.keyboard.press("Tab")
        if active(pg)["id"] == "chat-launcher":
            break
    reached = active(pg)["id"] == "chat-launcher"
    step("launcher_keyboard", focused_by_tab=reached, last_focus=active(pg), name=lau.get_attribute("aria-label"), visible=lau.is_visible())
    if not reached:
        lau.focus()
    pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    pg.wait_for_selector("#assistant-question", state="visible")
    root = pg.locator("section.chat-widget[role=dialog]")
    step("panel_open", role=root.get_attribute("role"), labelled_by=root.get_attribute("aria-labelledby"), expanded=lau.get_attribute("aria-expanded"), focus=active(pg),
         notice=pg.locator("#assistant-notice").text_content().strip(), notice_visible=pg.locator("#assistant-notice").is_visible(), saving_notice_present=pg.locator("#assistant-saving").count() == 1,
         consent_label=txt(pg, "label:has(#assistant-consent)"), consent_checked=pg.locator("#assistant-consent").is_checked(),
         intro_human_route="A person can help instead" in pg.locator("section.chat-widget").text_content(),
         disclaimer_ai_label="Each answer says whether AI or rules were used" in pg.locator("section.chat-widget").text_content())
    pg.screenshot(path=os.path.join(OUT, "resident-chat-consent-unticked.png"))
    # 1 question without consent
    q = pg.locator("#assistant-question"); q.focus(); pg.keyboard.type("Which documents are missing from my case?"); posts.clear()
    pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    step("ask_without_consent", chat_posts=[u for u in posts if "assistant" in u], error_text=txt(pg, ".chat-widget-error"),
         focus=active(pg), aria_invalid=pg.locator("#assistant-consent").get_attribute("aria-invalid"), log_text=pg.locator("#assistant-result").inner_text()[:80])
    # 2 tick via keyboard, ask
    pg.keyboard.press("Space"); pg.wait_for_timeout(300)
    step("ticked_by_space", checked=pg.locator("#assistant-consent").is_checked(), invalid_cleared=pg.locator("#assistant-consent").get_attribute("aria-invalid") is None)
    q.focus(); pg.keyboard.type("Which documents are missing from my case?"); posts.clear()
    with pg.expect_response("**/demo/assistant", timeout=90000) as r:
        pg.keyboard.press("Enter")
    pg.wait_for_timeout(2500)
    body = r.value.json() if r.value.status == 200 else {}
    step("ask_with_consent", status=r.value.status, posts=posts[:], label=body.get("label"), sources=len(body.get("sources") or []), answer_excerpt=EMAIL.sub("[email]", (body.get("answer") or "")[:200]),
         status_region=txt(pg, ".chat-widget-status"), log_items=pg.evaluate("document.querySelectorAll('#assistant-result > *').length"))
    pg.screenshot(path=os.path.join(OUT, "resident-chat-answer-labelled.png"))
    step("axe_open_panel", **pg.evaluate(AXE + """;(async()=>{const r=await axe.run(document.querySelector('section.chat-widget'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return {version:axe.version,violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length})),passes:r.passes.length}})()"""))
    # 3 untick
    pg.locator("#assistant-consent").focus(); pg.keyboard.press("Space"); pg.wait_for_timeout(500)
    step("unticked_clears", checked=pg.locator("#assistant-consent").is_checked(), log_items=pg.evaluate("document.querySelectorAll('#assistant-result > *').length"),
         question_value=pg.locator("#assistant-question").input_value(), status_text=txt(pg, ".chat-widget-status"))
    # 4 works consent question
    pg.keyboard.press("Space"); q.focus(); pg.keyboard.type("Have I given consent to the works?"); posts.clear()
    with pg.expect_response("**/demo/assistant", timeout=90000) as r2:
        pg.keyboard.press("Enter")
    pg.wait_for_timeout(2000)
    b2 = r2.value.json() if r2.value.status == 200 else {}
    step("works_consent_question", status=r2.value.status, label=b2.get("label"), answer_excerpt=EMAIL.sub("[email]", (b2.get("answer") or "")[:260]))
    # 5 escape and focus return
    pg.focus("#assistant-question"); pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    step("escape_closes", hidden=root.is_hidden(), focus=active(pg), expanded=lau.get_attribute("aria-expanded"))
    # 6 reflow 320x256 and reduced motion
    pg.set_viewport_size({"width": 320, "height": 256}); pg.wait_for_timeout(600)
    step("reflow_400pct_equiv", no_horizontal_scroll=pg.evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth"))
    pg.set_viewport_size({"width": 1366, "height": 900}); pg.emulate_media(reduced_motion="reduce"); pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    step("reduced_motion_page", running_long_animations=pg.evaluate("document.getAnimations().filter(a=>{const t=a.effect&&a.effect.getTiming();return t&&(t.duration>10||t.iterations===Infinity)&&a.playState==='running'}).length"))
    step("reload_session_state", signed_in=c.request.get(R + "/demo/session").json().get("signed_in"))
    b.close()
json.dump(res, open(os.path.join(OUT, "resident_proof.json"), "w"), indent=1)
for s in res["steps"]:
    print(EMAIL.sub("[email]", json.dumps(s))[:700])
