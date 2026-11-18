"""Issue 154 round 2: desktop UX audit of the live resident showcase and workbench resident screens.
Credentials are read at run time and never printed or written. Emails are masked in screenshots and output."""
import json, os, re
from playwright.sync_api import sync_playwright

OUT = os.path.dirname(os.path.abspath(__file__))
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
rcred = rd(".ama-resident-test-user")
ecred = (rd(".ama-test-user-id")[0], rd(".ama-test-user")[0])
res = {}
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
ZF = re.compile(r"ZF-\d{4}-\d{4}")
INTERNAL = ["gate", "hold", "provenance", "trace", "envelope", "snapshot", "on hold", "consent pending"]

MASK = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]').replace(/ZF-\\d{4}-\\d{4}/g,'ZF-[id]').replace(/(?:Flat \\d+, )?\\d[\\d,\\- ]*[A-Za-z' ]+? (?:Drive|Road|Avenue|Close|Place|Hill|Walk|Terrace|Lane|Street|Moorfield|Court|Way|Gardens|Crescent|Grove|Park|Square)(?:, [A-Za-z ]+)?/g,'[address]')}}"""

AUDIT = """()=>{
const lum=c=>{const [r,g,b]=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*r+0.7152*g+0.0722*b};
const parse=s=>{const m=s.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;const p=m[1].split(',').map(x=>parseFloat(x));return {c:p.slice(0,3),a:p.length>3?p[3]:1}};
const bg=el=>{while(el){const p=parse(getComputedStyle(el).backgroundColor);if(p&&p.a>0.99)return p.c;el=el.parentElement}return [255,255,255]};
const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
const out={};
out.lang=document.documentElement.lang||null;
out.title=document.title;
out.h1=[...document.querySelectorAll('h1')].filter(vis).map(e=>e.innerText.trim());
out.headings=[...document.querySelectorAll('h1,h2,h3,h4')].filter(vis).map(e=>e.tagName+':'+e.innerText.trim().slice(0,60));
out.landmarks=[...document.querySelectorAll('header,nav,main,footer,aside,[role=banner],[role=main],[role=navigation],[role=contentinfo]')].filter(vis).map(e=>e.tagName.toLowerCase()+(e.getAttribute('role')?'['+e.getAttribute('role')+']':''));
out.skip_link=!!document.querySelector('a[href^="#"][class*=skip],a.skip,.skip-link');
const names=e=>(e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')&&document.getElementById(e.getAttribute('aria-labelledby'))?.innerText||e.innerText||e.value||e.title||'').trim();
out.unnamed_controls=[...document.querySelectorAll('button,a[href],input:not([type=hidden]),select,textarea,[role=button]')].filter(vis).filter(e=>{
 if(e.matches('input,select,textarea')){return !(e.labels&&e.labels.length)&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby')}
 return !names(e)}).map(e=>e.outerHTML.slice(0,80));
out.images_without_alt=[...document.querySelectorAll('img')].filter(vis).filter(e=>!e.hasAttribute('alt')).length;
out.live_regions=[...document.querySelectorAll('[role=status],[role=alert],[aria-live]')].map(e=>(e.getAttribute('role')||'')+'/'+(e.getAttribute('aria-live')||''));
out.expanded_controls=[...document.querySelectorAll('[aria-expanded]')].filter(vis).length;
out.positive_tabindex=document.querySelectorAll('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])').length;
const small=[];let low=[];let checked=0;
for(const e of document.querySelectorAll('button,a[href],input:not([type=hidden]),select,[role=button]')){if(!vis(e))continue;const r=e.getBoundingClientRect();if(r.width<24||r.height<24)small.push((names(e)||e.tagName).slice(0,40)+' '+Math.round(r.width)+'x'+Math.round(r.height))}
out.targets_under_24px=small;
const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;const seen=new Set();
while(n=walker.nextNode()){const t=n.nodeValue.trim();if(!t)continue;const el=n.parentElement;if(!el||!vis(el)||seen.has(el))continue;seen.add(el);
 const s=getComputedStyle(el);const f=parse(s.color);if(!f)continue;const b=bg(el);
 const L1=lum(f.c),L2=lum(b);const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);const px=parseFloat(s.fontSize);const bold=parseInt(s.fontWeight)>=700;const large=px>=24||(px>=18.66&&bold);checked++;
 if(ratio<(large?3:4.5))low.push({t:t.slice(0,40),ratio:Math.round(ratio*100)/100,px})}
out.contrast_checked=checked;out.contrast_failures=low.slice(0,15);out.contrast_failure_count=low.length;
out.horizontal_scroll=document.documentElement.scrollWidth>document.documentElement.clientWidth;
out.reduced_motion_rule=[...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>r.conditionText&&r.conditionText.includes('prefers-reduced-motion'))}catch(e){return false}});
return out}"""


def keyboard(page, limit=40):
    seq = []
    page.evaluate("document.activeElement&&document.activeElement.blur()")
    for _ in range(limit):
        page.keyboard.press("Tab")
        info = page.evaluate("""()=>{const e=document.activeElement;if(!e||e===document.body)return null;const s=getComputedStyle(e);
        return {tag:e.tagName.toLowerCase(),name:(e.getAttribute('aria-label')||e.innerText||e.value||e.id||'').trim().slice(0,40),
        outline:s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0,shadow:s.boxShadow!=='none'}}""")
        if not info:
            break
        seq.append(info)
    return {"stops": len(seq), "without_visible_focus_indicator": [s["name"] or s["tag"] for s in seq if not (s["outline"] or s["shadow"])][:15], "first": [s["tag"] + ":" + s["name"] for s in seq[:8]]}


def words(text):
    t = text.lower()
    return {k: bool(re.search(r"\b" + re.escape(k) + r"\b", t)) for k in INTERNAL}


def terms(text):
    t = text.lower()
    return {k: (k in t) for k in ["representative", "interpreter", "non-digital", "offered", "confirmed", "commitment", "not a booking", "not a promise", "complaint", "withdraw", "pause", "language", "adjustment", "easy read", "large print"]}


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1366, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page(); pg.set_default_timeout(120000)
    pg.goto(RES + "/"); pg.wait_for_load_state("networkidle")
    res["resident_signed_out"] = {"audit": pg.evaluate(AUDIT)}
    em, pw = (rcred[0], rcred[1]) if "@" in rcred[0] else (rcred[1], rcred[0])
    pg.fill("#email", em); pg.fill("#password", pw)
    res["resident_signed_out"]["keyboard"] = keyboard(pg, 12)
    pg.click("#signin-button")
    pg.wait_for_selector("#content", state="visible", timeout=180000); pg.wait_for_timeout(2500)
    pg.evaluate(MASK)
    a = pg.evaluate(AUDIT)
    text = pg.inner_text("body")
    res["resident_signed_in"] = {"audit": a, "internal_terms_present": words(text), "journey_terms": terms(text), "keyboard": keyboard(pg, 40)}
    pg.screenshot(path=os.path.join(OUT, "r2-01-resident-signed-in-1366.png"), full_page=True)
    # expand every disclosure button and re-read for added content
    btns = pg.query_selector_all("button[aria-expanded]")
    res["resident_signed_in"]["expandable_buttons"] = len(btns)
    res["resident_signed_in"]["signout_accessible_name"] = pg.evaluate("(()=>{const e=document.querySelector('#signout');return {text:e.textContent.trim(),aria:e.getAttribute('aria-label'),visible:!!e.offsetParent}})()")
    for bt in btns:
        try:
            bt.click(timeout=3000)
        except Exception:
            pass
    pg.wait_for_timeout(800); pg.evaluate(MASK)
    t2 = pg.inner_text("body")
    res["resident_signed_in"]["expanded"] = {"chars_before": len(text), "chars_after": len(t2), "journey_terms": terms(t2), "internal_terms_present": words(t2)}
    pg.screenshot(path=os.path.join(OUT, "r2-02-resident-expanded-1366.png"), full_page=True)
    # 200% zoom equivalent: halve the CSS viewport
    pg.set_viewport_size({"width": 683, "height": 450}); pg.wait_for_timeout(600)
    res["resident_signed_in"]["zoom200_horizontal_scroll"] = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
    pg.screenshot(path=os.path.join(OUT, "r2-03-resident-200pct-equivalent.png"), full_page=True)
    pg.evaluate("document.querySelector('#signout').click()")
    ctx.close(); b.close()

    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1366, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page(); pg.set_default_timeout(120000)
    pg.goto(EMP + "/sign-in", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", ecred[0]); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]"); pg.fill("input[name=passwd]", ecred[1]); pg.click("#idSIButton9")
    for _ in range(3):
        try:
            pg.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if pg.url.startswith(EMP): break
            (pg.query_selector("#idSIButton9") or pg.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    pg.wait_for_load_state("domcontentloaded")
    me = pg.evaluate("fetch('/api/me').then(r=>r.json())")
    res["employee"] = {"role": me["user"]["role"], "screens": {}}
    routes = {"resident-choice": "#/role/resident_engagement", "resident-service-issues": "#/role/housing_officer",
              "package-queue": "#/role/procurement", "case-list": "#/"}
    for name, h in routes.items():
        try:
            pg.goto(EMP + "/app" + h); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(3500); pg.evaluate(MASK)
            txt = pg.inner_text("body")
            pg.evaluate("window.scrollTo(0,0)")
            if name != "case-list":
                pg.screenshot(path=os.path.join(OUT, f"r2-emp-{name}-1366.png"))
            res["employee"]["screens"][name] = {"hash": h, "chars": len(txt), "audit": pg.evaluate(AUDIT), "journey_terms": terms(txt),
                "internal_terms_present": words(txt), "keyboard": keyboard(pg, 25)}
        except Exception as e:
            res["employee"]["screens"][name] = {"error": EMAIL.sub("[email]", str(e))[:200]}
    # one case detail
    cases = pg.evaluate("fetch('/api/cases').then(r=>r.json())")
    lst = cases if isinstance(cases, list) else cases.get("items", [])
    if lst:
        cid = lst[0].get("id")
        pg.goto(EMP + "/app#/case/" + cid); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000); pg.evaluate(MASK)
        txt = pg.inner_text("body")
        res["employee"]["screens"]["case-detail"] = {"chars": len(txt), "audit": pg.evaluate(AUDIT), "journey_terms": terms(txt), "internal_terms_present": words(txt), "keyboard": keyboard(pg, 25)}
    ctx.close(); b.close()

raw = json.dumps(res, indent=1)
NAMES = re.compile(r"Dawn Brown|Angela Dixon|Kevin Bell|Jack Armstrong|Wendy Robson")
open(os.path.join(OUT, "ux-audit-raw.json"), "w").write(NAMES.sub("[name]", ZF.sub("ZF-[id]", EMAIL.sub("[email]", raw))))
print("done", len(raw))
