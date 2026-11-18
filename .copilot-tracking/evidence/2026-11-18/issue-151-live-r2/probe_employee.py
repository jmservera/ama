"""Issue 151 live round 2: resident app axe+keyboard, employee title/contrast/dialog probes. Credentials read at runtime, never printed."""
import hashlib, json, os, re, sys
from playwright.sync_api import sync_playwright
from common import *
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
rl = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
RU, RP = rl[0].strip(), rl[1].strip()
raw = open(f"{OUT}/axe.min.js", "rb").read()
assert hashlib.sha256(raw).hexdigest() == open(f"{OUT}/axe-4.10.3.sha256").read().strip()
AXE = raw.decode()
TAGS = ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']
exec(open(os.path.join(OUT, "../issue-151-live/scan.py")).read().split("res = {")[0].split("from common import *")[1])  # reuse axe_scan, keyboard, FOCUS_JS
CONTRAST_JS = """() => {
  const lum=c=>{const [r,g,b]=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
  const parse=s=>{const m=s.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;const p=m[1].split(',').map(Number);return {c:p.slice(0,3),a:p.length>3?p[3]:1}};
  const bg=e=>{let acc=[255,255,255];const chain=[];for(let n=e;n;n=n.parentElement){const p=parse(getComputedStyle(n).backgroundColor);if(p&&p.a>0){chain.push(p);if(p.a>=1)break}}
    for(const p of chain.reverse()){acc=acc.map((v,i)=>Math.round(p.c[i]*p.a+v*(1-p.a)))}return acc};
  const out={n:0,fail:0,worst:[],imgbg:0};const seen=[];
  for(const e of document.querySelectorAll('body *')){
    if(![...e.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim()))continue;
    const s=getComputedStyle(e);if(s.visibility==='hidden'||s.display==='none')continue;const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;
    const fg=parse(s.color);if(!fg)continue;const b=bg(e);
    const f=fg.c.map((v,i)=>Math.round(v*fg.a+b[i]*(1-fg.a)));
    const L1=lum(f),L2=lum(b);const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
    const size=parseFloat(s.fontSize),bold=parseInt(s.fontWeight)>=700;const large=size>=24||(size>=18.66&&bold);
    out.n++;const need=large?3:4.5;if(ratio<need){out.fail++;seen.push({text:e.textContent.trim().slice(0,30),ratio:Math.round(ratio*100)/100,need,size})}
  }
  out.worst=seen.sort((a,b)=>a.ratio-b.ratio).slice(0,8);return out}"""
res = {"axe": "4.10.3", "viewport": "1366x900", "resident": {}, "employee": {}}
def shot(pg, name):
    pg.screenshot(path=f"{OUT}/{name}.png")
with sync_playwright() as p:
    b = p.chromium.launch()
    # Employee
    ctx = b.new_context(viewport={"width": 1366, "height": 900}); pg = ctx.new_page(); login(pg)
    pg.goto(APP + "/app", wait_until="networkidle"); pg.wait_for_timeout(4000)
    e = res["employee"]; e["titles"] = {}; e["contrast"] = {}
    for s in ["", "all", "overview", "progress", "visits", "funding", "finance", "capacity", "closed", "assistants", "time", "aftercare", "screens"]:
        pg.evaluate(f"location.hash='#/{s}'"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
        e["titles"][s or "my-cases"] = {"title": pg.title(), "h1": pg.locator("h1").first.inner_text() if pg.locator("h1").count() else None}
        e["contrast"][s or "my-cases"] = pg.evaluate(CONTRAST_JS)
    # case detail dialog / detail keyboard
    pg.evaluate("location.hash='#/'"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
    pg.evaluate("document.activeElement&&document.activeElement.blur()")
    opened = None
    for i in range(30):
        pg.keyboard.press("Tab"); f = pg.evaluate("()=>{const e=document.activeElement;return {tag:e.tagName.toLowerCase(),text:(e.textContent||'').trim().slice(0,40),href:e.getAttribute('href')}}")
        if f["tag"] in ("a", "button") and f["href"] and "case" in (f["href"] or ""):
            opened = f; pg.keyboard.press("Enter"); break
    pg.wait_for_timeout(1500)
    e["keyboard_open_case"] = {"activated": opened is not None, "hash_after": pg.evaluate("location.hash"),
        "title_after": pg.title(), "focus_after": pg.evaluate("()=>{const e=document.activeElement;return e.tagName.toLowerCase()+':'+(e.textContent||'').trim().slice(0,40)}")}
    e["case_axe"] = axe_scan(pg); e["case_keyboard"] = keyboard(pg, 80)
    mask_emails(pg); shot(pg, "employee-case-detail")
    e["escape_dialogs"] = pg.evaluate("document.querySelectorAll('dialog[open],[role=dialog]:not([hidden])').length")
    ctx.close(); b.close()
json.dump(res, open(f"{OUT}/probe-results-employee.json", "w"), indent=1)
print("done")
