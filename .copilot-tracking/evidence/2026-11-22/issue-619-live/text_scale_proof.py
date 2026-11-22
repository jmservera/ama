"""Text scaling (200 percent root font size) and WCAG 1.4.12 text spacing on the live resident page. Credentials read at runtime, never printed."""
import json, os
from playwright.sync_api import sync_playwright
R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
U, PW = [x.strip() for x in open(os.path.expanduser("~/.ama-resident-test-user")).read().split("\n") if x.strip()][:2]
res = []
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}, bypass_csp=True); pg = c.new_page()
    pg.goto(R + "/", wait_until="domcontentloaded", timeout=120000)
    pg.click("#email"); pg.keyboard.type(U); pg.keyboard.press("Tab"); pg.keyboard.type(PW); pg.keyboard.press("Enter")
    pg.wait_for_selector("#signin", state="hidden", timeout=90000); pg.wait_for_timeout(3000)
    pg.click("#chat-launcher"); pg.wait_for_selector("#assistant-question", state="visible")
    for name, css in [("text_200pct", "html{font-size:200% !important}"),
                      ("text_spacing_1_4_12", "*{line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important} p{margin-bottom:2em !important}")]:
        h = pg.add_style_tag(content=css); pg.wait_for_timeout(500)
        r = pg.evaluate("""()=>{const q=document.querySelector('#assistant-question').getBoundingClientRect();
        const s=document.querySelector('section.chat-widget');const cl=[...s.querySelectorAll('button,input,label,h2')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left<-1)}).length;
        const lab=document.querySelector('label:has(#assistant-consent)');const lr=lab.getBoundingClientRect();let a=lab,sc=null;while(a&&a!==document.body){const o=getComputedStyle(a).overflowY;if(a.scrollHeight>a.clientHeight+1&&/auto|scroll|hidden/.test(o)){sc={tag:a.tagName,cls:a.className,overflowY:o,clientH:a.clientHeight,scrollH:a.scrollHeight};break}a=a.parentElement}
        const qa=document.querySelector('#assistant-question').getBoundingClientRect();
        return {consent_label_h:Math.round(lr.height),clipping_ancestor:sc,question_rect:[Math.round(qa.left),Math.round(qa.top),Math.round(qa.width),Math.round(qa.height)],viewport_h:innerHeight,no_horizontal_scroll:document.documentElement.scrollWidth<=innerWidth+1,controls_outside_viewport_x:cl,panel_overflow_y:s.scrollHeight>s.clientHeight,question_w:Math.round(q.width)}}""")
        pg.screenshot(path=os.path.join(OUT, name + ".png")); res.append({"step": name, **r})
        h.evaluate("e=>e.remove()")
    b.close()
json.dump({"steps": res}, open(os.path.join(OUT, "text_scale_proof.json"), "w"), indent=1)
print(json.dumps(res))
