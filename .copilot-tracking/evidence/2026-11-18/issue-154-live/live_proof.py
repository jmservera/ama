"""Issue 154 live proof: resident showcase and employee representative view. Reads credentials at runtime; never prints them."""
import json, os, re
from playwright.sync_api import sync_playwright

OUT = os.path.dirname(os.path.abspath(__file__))
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMPAPP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
rcred = rd(".ama-resident-test-user"); ecred = (rd(".ama-test-user-id")[0], rd(".ama-test-user")[0])
res = {}

def mask(page):
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900})
    pg.set_default_timeout(90000)
    pg.goto(RES + "/"); pg.wait_for_load_state("networkidle")
    pg.screenshot(path=os.path.join(OUT, "01-resident-signed-out.png"))
    em, pw = (rcred[0], rcred[1]) if "@" in rcred[0] else (rcred[1], rcred[0])
    pg.fill("#email", em); pg.fill("#password", pw); pg.click("#signin-button")
    pg.wait_for_selector("#content", state="visible", timeout=180000); pg.wait_for_timeout(2500)
    mask(pg)
    pg.screenshot(path=os.path.join(OUT, "02-resident-signed-in.png"), full_page=True)
    text = pg.inner_text("body")
    res["resident"] = {
        "title": pg.title(),
        "body_chars": len(text),
        "mentions": {k: (k in text.lower()) for k in ["synthetic", "not live", "not available in this showcase", "message", "callback", "appointment", "consent", "complaint", "representative", "alternative", "phone", "offer"]},
        "mailto_tel_links": pg.eval_on_selector_all("a[href^='mailto:'],a[href^='tel:'],a[href^='sms:']", "e=>e.length"),
        "forms": pg.eval_on_selector_all("form", "e=>e.map(f=>({id:f.id,action:f.getAttribute('action')}))"),
        "visible_buttons": [t.strip() for t in pg.eval_on_selector_all("button", "e=>e.filter(x=>x.offsetParent!==null).map(x=>x.innerText)") if t.strip()],
        "visible_inputs": pg.eval_on_selector_all("input,textarea,select", "e=>e.filter(x=>x.offsetParent!==null).map(x=>x.type||x.tagName)"),
    }
    na = re.findall(r"Not available in this showcase[\s\S]{0,700}", text)
    res["resident"]["not_available_excerpt"] = re.sub(r"\s+", " ", na[0])[:700] if na else None
    sess = pg.evaluate("fetch('/demo/session').then(r=>r.status)")
    res["resident"]["demo_session_status"] = sess
    # state-changing and contact routes must not exist
    res["resident"]["write_probes"] = {}
    for path in ["/api/messages", "/api/appointments", "/api/callback", "/demo/message", "/demo/contact", "/api/consent"]:
        res["resident"]["write_probes"][path] = pg.evaluate("p=>fetch(p,{method:'POST'}).then(r=>r.status)", path)
    res["resident"]["control_nonexistent_post"] = pg.evaluate("fetch('/zz-none',{method:'POST'}).then(r=>r.status)")
    pg.evaluate("document.querySelector('#signout').click()")
    b.close()

    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900}); pg.set_default_timeout(90000)
    pg.goto(EMPAPP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", ecred[0]); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]"); pg.fill("input[name=passwd]", ecred[1]); pg.click("#idSIButton9")
    for _ in range(3):
        try:
            pg.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if pg.url.startswith(EMPAPP): break
            (pg.query_selector("#idSIButton9") or pg.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    pg.wait_for_load_state("domcontentloaded")
    me = pg.evaluate("fetch('/api/me').then(r=>r.json())")
    res["employee"] = {"role": me["user"]["role"], "identity_source": me["user"]["identity_source"]}
    cases = pg.evaluate("fetch('/api/cases').then(r=>r.status===200?r.json():{status:r.status})")
    lst = cases if isinstance(cases, list) else (cases.get("items") or [])
    res["employee"]["cases_status"] = "ok" if lst else cases
    res["employee"]["case_count"] = len(lst)
    if lst:
        cid = lst[0].get("id") or lst[0].get("case_id")
        rv = pg.evaluate("p=>fetch(p).then(async r=>({s:r.status,t:await r.text()}))", f"/api/cases/{cid}/representative-view")
        res["employee"]["rep_view_no_ref"] = {"status": rv["s"], "body_head": re.sub(r"[\w.+-]+@[\w.-]+", "[email]", rv["t"])[:300]}
        hv = pg.evaluate("p=>fetch(p).then(async r=>({s:r.status,k:Object.keys(await r.json().catch(()=>({})))}))", f"/api/cases/{cid}/resident-view")
        res["employee"]["resident_view_probe"] = hv
    pg.goto(EMPAPP + "/#/"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2000); mask(pg)
    pg.screenshot(path=os.path.join(OUT, "03-workbench-signed-in.png"))
    t = pg.inner_text("body").lower()
    res["employee"]["body_mentions"] = {k: (k in t) for k in ["representative", "resident", "interpreter", "non-digital", "offer", "commitment"]}
    b.close()
json.dump(res, open(os.path.join(OUT, "live-proof.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
